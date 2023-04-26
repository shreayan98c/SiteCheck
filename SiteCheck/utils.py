import re
import sys
import logging
import requests
from PIL import Image
from bs4 import BeautifulSoup
from queue import PriorityQueue
from urllib import parse, request

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


def check_image(img_tag, url):
    """
    Checks if the image is valid or broken.
    :param img_tag: src attribute of the image url to check validity
    :param url: url of the website
    :return: True if image is valid, False otherwise
    """
    alt_text = img_tag.get('alt')
    img_line = img_tag.sourceline

    # if no alt-text is provided, write a warning to the warning file
    if alt_text is None:
        warning_message = [f'Please add the alt-text for the image on line {img_line} with {img_tag}']
        writelines('warnings.txt', warning_message)

    # if image is relatively pathed - add the base url to the relative path and check for it
    if not img_tag.get('src').startswith('http'):
        img_tag['src'] = parse.urljoin(url, img_tag['src'])

    # hit the url of the image and check the status code
    response = requests.get(img_tag['src'], stream=True)
    if response.status_code == 200:
        with Image.open(response.raw) as img:
            print("Image works!, Size:", img.size)
    else:
        print("Image does not work!")
        # write error to the error file
        error_message = [f'Broken image found on line {img_line} with {img_tag}']
        writelines('errors.txt', error_message)


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


def crawl(root, wanted_content=None, within_domain=True, num_link=10, keywords=None):
    """
    Crawl the url specified by `root`.
    `wanted_content` is a list of content types to crawl
    `within_domain` specifies whether the crawler should limit itself to the domain of `root`
    """
    queue = PriorityQueue()
    queue.put((relevance_func(root, keywords), root))

    visited = set()
    extracted = []

    wanted_content = [] if wanted_content is None else wanted_content
    keywords = [] if keywords is None else keywords

    while not queue.empty():
        if len(visited) > num_link:
            break
        rank, url = queue.get()
        try:
            req = request.urlopen(url)
            wanted_content = [x.lower() for x in wanted_content]
            content = req.headers['Content-Type'].lower()
            if wanted_content and (content not in wanted_content):
                continue
            html = req.read().decode('utf-8')

            visited.add(url)
            visitlog.debug(url)

            for ex in extract_information(url, html):
                extracted.append(ex)
                extractlog.debug(ex)

            for (rank, link), title in parse_links_sorted(url, html, keywords):
                if (link in visited) or (parse.urlparse(link) == parse.urlparse(root)) or (
                        within_domain and parse.urlparse(link).hostname != parse.urlparse(url).hostname):
                    continue
                queue.put((rank, link))

        except Exception as e:
            print(e, url)

    return visited, extracted


def extract_information(address, html):
    """
    Extract contact information from html, returning a list of (url, category, content) pairs,
    where category is one of PHONE, ADDRESS, EMAIL
    """
    results = []
    for match in re.findall(r'\d\d\d-\d\d\d-\d\d\d\d', str(html)):
        results.append((address, 'PHONE', match))

    for match in re.findall(r'([a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z0-9.-]+)', str(html)):
        results.append((address, 'EMAIL', match))

    for match in re.findall(r'([A-Z]([a-z])+(\.?)(\x20[A-Z]([a-z])+){0,2},\s[A-Za-z]+\.{0,1}\s(?!0{5})\d{5})',
                            str(html)):
        results.append((address, 'ADDRESS', match[0]))
    return results


def writelines(filename, data):
    with open(filename, 'w') as fout:
        for d in data:
            print(d, file=fout)


def main():
    site = sys.argv[1]
    num_l = 1000
    keywords = ['book', 'homework', 'hw', 'assignment']

    links = get_links(site)
    writelines('links.txt', links)

    nonlocal_links = get_nonlocal_links(site)
    writelines('nonlocal.txt', nonlocal_links)

    visited, extracted = crawl(site, wanted_content=[], within_domain=True, num_link=num_l, keywords=keywords)
    writelines('visited.txt', visited)
    writelines('extracted.txt', extracted)


if __name__ == '__main__':
    main()
