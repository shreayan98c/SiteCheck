import re
import os
import sys
import json
import time
import pickle
import logging
import requests
from PIL import Image, UnidentifiedImageError
from skimage import io
from bs4 import BeautifulSoup
from selenium import webdriver
from queue import PriorityQueue
from urllib import parse, request, error
import skimage.metrics as metrics
from axe_selenium_python import Axe
from skimage.transform import resize

logging.basicConfig(level=logging.DEBUG, filename='output.log', filemode='w')

visitlog = logging.getLogger('visited')
extractlog = logging.getLogger('extracted')


def extract_links(html):
    """
    Extracts all links from a given url.
    :param html: html content of the website
    :return: list of links, both foreign and internal
    """
    links = []
    for link in html.find_all('a'):
        href = link.get('href')
        if href and href.startswith('http'):
            links.append(href)
    return links


def extract_images(html):
    """
    Extracts all images from a given url.
    :param html: html content of the website url to extract all the images from
    :return: list of images
    """
    images = []
    for img in html.find_all('img'):
        images.append(img)
    return images


def check_image(img_tag, url, working_imgs, warnings, errors):
    """
    Checks if the image is valid or broken.
    :param img_tag: src attribute of the image url to check validity
    :param url: url of the website
    :param working_imgs: list of sizes working images
    :param warnings: list of warnings
    :param errors: list of errors
    :return: list of working images, list of warnings, list of errors
    """
    alt_text = img_tag.get('alt')
    img_line = img_tag.sourceline

    # if no alt-text is provided, write a warning to the warning file
    if alt_text is None:
        warning_message = f'Please add the alt-text for the image on line {img_line} with {img_tag}'
        warnings.append(warning_message)
        # writelines('outputs/warnings.txt', warning_message)

    # if image is relatively pathed - add the base url to the relative path and check for it
    if not img_tag.get('src').startswith('http'):
        img_tag['src'] = parse.urljoin(url, img_tag['src'])

    # hit the url of the image and check the status code
    response = None
    try:
        response = requests.get(img_tag['src'], stream=True)
    except:
        errors.append(f'Unable to access the image on the server')
    if response and response.status_code == 200:
        try:
            with Image.open(response.raw) as img:
                working_imgs.append(img.size)
        except UnidentifiedImageError:
            errors.append(f'Unable to open the image using PIL')
    else:
        # write error to the error file
        error_message = f'Broken image found on line {img_line} with {img_tag}'
        errors.append(error_message)
        # writelines('outputs/errors.txt', error_message)
    return working_imgs, warnings, errors


def get_nonlocal_links(url):
    """
    Get a list of links on the page specified by the url,
    but only keep non-local links and non self-references.
    Return a list of (link, title) pairs, just like get_links()
    """
    links = get_links(url)
    filtered = []
    for link in links:
        if parse.urlparse(link[0]).hostname != parse.urlparse(url).hostname:
            filtered.append(link)
    return filtered


def parse_links(root, html):
    soup = BeautifulSoup(html, 'html.parser')
    for link in soup.find_all('a'):
        href = link.get('href')
        if href:
            text = link.string
            if not text:
                text = ''
            text = re.sub(r'\s+', ' ', text).strip()
            yield parse.urljoin(root, link.get('href')), text


def relevance_func(link, keywords):
    if len(keywords) == 0:
        return 0
    for w in keywords:
        if w in link:
            return 0
    else:
        return 1


def parse_links_sorted(root, html, keywords):
    soup = BeautifulSoup(html, 'html.parser')
    for link in soup.find_all('a'):
        href = link.get('href')
        if href:
            text = link.string
            if not text:
                text = ''
            text = re.sub(r'\s+', ' ', text).strip()
            url = parse.urljoin(root, link.get('href'))
            yield (relevance_func(url, keywords), url), text


def get_links(url):
    res = request.urlopen(url)
    return list(parse_links(url, res.read()))
            
def check_link(url, response, warnings, errors):
    '''
    Checks whether any HTTPErrors occurred when sending GET request to a url.
    :param url: the url to which the GET request was sent
    :param response: the response to the request
    :param warnings: list of warnings
    :param errors: list of errors
    :return list of warnings, list of errors, boolean indicating whether request was successful
    '''
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        if e.code == 401:
            warnings.append(f'Accessing link {url} requires authentication, is this intended?')
        else:
            errors.append(f'Opening link {url} resulted in HTTP Error with status \
                          code {response.status_code}: {response.reason}')
        return warnings, errors, False
    
    return warnings, errors, True

def build_url_hierarchy(urls):
    hierarchy = {}
    for url in urls:
        parts = url.split('/')
        node = hierarchy
        for part in parts[1:]:
            if part not in node:
                node[part] = {}
            node = node[part]
    return hierarchy


def compare_images(image1_path, image2_path):
    """
    Compare two images using the SSIM index metric
    :param image1_path: path to the first image
    :param image2_path: path to the second image
    :return: SSIM index value
    """
    # Load the images
    image1 = io.imread(image1_path)
    image2 = io.imread(image2_path)

    # slice off the alpha channels
    if len(image1.shape) > 2 and image1.shape[2] == 4:
        image1 = image1[:, :, :3]
    if len(image2.shape) > 2 and image2.shape[2] == 4:
        image2 = image2[:, :, :3]

    # resize the images to 500x500
    image1_resized = resize(image1, (500, 500))
    image2_resized = resize(image2, (500, 500))

    # Calculate the SSIM index
    ssim = metrics.structural_similarity(image1_resized, image2_resized, multichannel=True)

    return ssim


def get_tag_counts(soup):
    """
    Get a dictionary of tag counts from a BeautifulSoup object
    :param soup: BeautifulSoup object
    :return: dictionary of tag counts
    """
    tag_counts = {}
    for tag in soup.find_all():
        tag_name = tag.name
        if tag_name in tag_counts:
            tag_counts[tag_name] += 1
        else:
            tag_counts[tag_name] = 1
    return tag_counts


def get_lang_counts(soup):
    """
    Get a dictionary of language counts from a BeautifulSoup object
    :param soup: BeautifulSoup object
    :return: dictionary of language counts
    """
    language_counts = {}
    for tag in soup.find_all():
        if tag.has_attr('lang'):
            lang = tag['lang']
            if lang in language_counts:
                language_counts[lang] += 1
            else:
                language_counts[lang] = 1
    return language_counts


def eval_accessibility(url):
    """
    Get the accessibility violations for a given URL using the Axe engine
    :param url: URL to calculate the accessibility score for
    :return: accessibility score
    """

    # Initialize the Axe engine and configure it to run in Chrome
    # driver = webdriver.Firefox(executable_path=r'C:\NonOSFiles\BlueJayCodes\IRWA\geckodriver-v0.33.0-win32\geckodriver.exe')
    driver = webdriver.Chrome(executable_path=r'C:\NonOSFiles\BlueJayCodes\IRWA\chromedriver_win32\chromedriver.exe')
    driver.get(url)
    axe = Axe(driver)
    axe.inject()

    # Analyze the page using Axe
    results = axe.run()

    # close the browser
    driver.close()

    violations = []

    if results["violations"] is None:
        return None

    for violation in results["violations"]:
        vio_id = violation["id"]
        description = violation["description"]
        vio_help = violation["help"]
        impact = violation["impact"]
        violations.append((vio_id, description, vio_help, impact))

    return violations


def remove_empty_keys(d):
    """
    Remove empty keys from a dictionary
    :param d: dictionary to remove empty keys from
    :return: dictionary with empty keys removed
    """
    if '' in d:
        d = d['']
    for k, v in list(d.items()):
        if k == '':
            del d[k]
        else:
            remove_empty_keys(v)
    return d


def writelines(filename, data):
    with open(filename, 'a') as fout:
        for d in data:
            print(d, file=fout)


def save_object(obj, filename):
    with open(filename, 'wb') as outp:  # Overwrites any existing file.
        pickle.dump(obj, outp, pickle.HIGHEST_PROTOCOL)


def main():
    site = sys.argv[1]

    links = get_links(site)
    writelines('links.txt', links)

    nonlocal_links = get_nonlocal_links(site)
    writelines('nonlocal.txt', nonlocal_links)
