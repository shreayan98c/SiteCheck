import requests
from PIL import Image
from bs4 import BeautifulSoup


def extract_links(url):
    """
    Extracts all links from a given url.
    :param url: website url to extract all the links from
    :return: list of links, both foreign and internal
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = []
    for link in soup.find_all('a'):
        href = link.get('href')
        if href and href.startswith('http'):
            links.append(href)
    return links


def extract_images(url):
    """
    Extracts all images from a given url.
    :param url: website url to extract all the images from
    :return: list of images
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    images = []
    for img in soup.find_all('img'):
        src = img.get('src')
        if src and src.startswith('http'):
            images.append(src)
    return images


def check_image(url):
    """
    Checks if the image is valid or broken.
    :param url: src attribute of the image url to check validity
    :return:
    """
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with Image.open(response.raw) as img:
            return img.format
    else:
        return None
