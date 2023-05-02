import time
from SiteCheck.utils import *


def main(url: str):
    """
    Parse the given URL, extract the links and images, does preprocessing and writes the results to the outputs directory.
    :param url: url of the website to parse and test
    :return: None
    """
    print(f"Parsing URL: {url}")

    start_time = time.time()
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    response_time = time.time() - start_time
    print(f'Loading the page took {response_time} seconds')
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

    start_time = time.time()
    for image in images:
        check_image(img_tag=image, url=url)
    images_check = time.time() - start_time
    print(f'Checking the images took {images_check} seconds')

    tag_counts = get_tag_counts(soup)
    tag_counts = dict(sorted(tag_counts.items(), key=lambda item: item[1], reverse=True))
    # filter only tags with more than 1 occurrence, ex: html, body, head, etc.
    tag_counts = {k: v for k, v in tag_counts.items() if v > 1}
    print(f'Tag counts: {tag_counts}')

    lang_counts = get_lang_counts(soup)
    lang_counts = dict(sorted(lang_counts.items(), key=lambda item: item[1], reverse=True))
    print(f'Language counts: {lang_counts}')

    links = get_links(url)
    local_links = [link[0] for link in links if link[0].startswith(url) and not link[0].split('/')[-1].startswith('#')]
    nonlocal_links = get_nonlocal_links(url)
    nonlocal_links = [link[0] for link in nonlocal_links]
    print(f'Local links: {local_links}')
    print(f'Nonlocal links: {nonlocal_links}')

    hierarchy = build_url_hierarchy(local_links)
    print(json.dumps(hierarchy, indent=4))

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
