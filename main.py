from SiteCheck.utils import *


def main(url: str):
    """
    Parse the given URL, extract the links and images, does preprocessing and writes the results to the outputs directory.
    :param url: url of the website to parse and test
    :return: None
    """
    print(f"Parsing URL: {url}")

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    try:
        os.mkdir('outputs')
    except:
        pass

    links = extract_links(soup)
    print(f'{len(links)} links found')
    writelines('outputs/links.txt', links)
    images = extract_images(soup)
    print(f'{len(images)} images found')
    writelines('outputs/images.txt', images)

    for image in images:
        check_image(img_tag=image, url=url)

    links = get_links(url)
    local_links = [link[0] for link in links if link[0].startswith(url) and not link[0].split('/')[-1].startswith('#')]
    nonlocal_links = get_nonlocal_links(url)
    nonlocal_links = [link[0] for link in nonlocal_links]
    print(local_links)
    print(nonlocal_links)

    hierarchy = build_url_hierarchy(local_links)
    print(hierarchy)

    image1_path = 'test_images/jhu_logo_1.png'
    image2_path = 'test_images/jhu_logo_2.png'

    similarity = compare_images(image1_path, image2_path)
    print('Similarity:', similarity)
    similarity = compare_images(image1_path, image1_path)
    print('Similarity:', similarity)
    similarity = compare_images(image2_path, image2_path)
    print('Similarity:', similarity)


if __name__ == '__main__':
    url = "https://www.cs.jhu.edu/~schaud31/"
    # url = "https://www.w3schools.com/tags/tryit.asp?filename=tryhtml_image_test"
    main(url)
