import time
from SiteCheck.utils import *


def main(url: str, depth, visited: set, api_responses: list):
    """
    Parse the given URL, extract the links and images, does preprocessing and writes the results to the outputs directory.
    :param url: url of the website to parse and test
    :param depth: depth of the recursion
    :param visited: set of visited urls
    :param links_to_visit: list of links
    :param api_responses: list of api responses
    :return: response across all the pages
    """
    if depth == 0:
        return api_responses

    if url in visited:
        return api_responses

    visited.add(url)

    api = {}

    start_time = time.time()
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    response_time = time.time() - start_time
    api['load_page_time'] = response_time

    links = extract_links(soup)
    api['links'] = json.dumps(links)
    writelines('outputs/links.txt', links)
    images = extract_images(soup)
    api['images'] = json.dumps([str_repr.__repr__() for str_repr in images])
    writelines('outputs/images.txt', images)

    start_time = time.time()
    working_imgs, warnings, errors = [], [], []
    for image in images:
        working_imgs, warnings, errors = check_image(img_tag=image, url=url, working_imgs=working_imgs,
                                                     warnings=warnings, errors=errors)
    images_check = time.time() - start_time
    api['check_imgs_time'] = json.dumps(images_check)

    tag_counts = get_tag_counts(soup)
    tag_counts = dict(sorted(tag_counts.items(), key=lambda item: item[1], reverse=True))
    # filter only tags with more than 1 occurrence, ex: html, body, head, etc.
    tag_counts = {k: v for k, v in tag_counts.items() if v > 1}
    api['tag_counts'] = json.dumps(tag_counts)

    lang_counts = get_lang_counts(soup)
    lang_counts = dict(sorted(lang_counts.items(), key=lambda item: item[1], reverse=True))
    api['lang_counts'] = json.dumps(lang_counts)

    links = get_links(url)
    local_links = [link[0] for link in links if link[0].startswith(url) and not link[0].split('/')[-1].startswith('#')]
    nonlocal_links = get_nonlocal_links(url)
    nonlocal_links = [link[0] for link in nonlocal_links]
    api['local_links'] = json.dumps(local_links)
    api['nonlocal_links'] = json.dumps(nonlocal_links)

    violations = eval_accessibility(url)
    api['accessibility_violations'] = json.dumps(violations)

    hierarchy = build_url_hierarchy(local_links)
    api['hierarchy'] = json.dumps(hierarchy)

    api_responses.append(api)

    for link in local_links:
        api_responses = main(link, depth - 1, visited, api_responses)

    return api_responses

    # image1_path = 'test_images/jhu_logo_1.png'
    # image2_path = 'test_images/jhu_logo_2.png'
    # similarity = compare_images(image1_path, image2_path)
    # print('Similarity:', similarity)


if __name__ == '__main__':
    url = "https://www.cs.jhu.edu/~schaud31/"
    depth = 2
    # url = "https://www.w3schools.com/tags/tryit.asp?filename=tryhtml_image_test"
    api_response = main(url, depth, set(), [])
    print(api_response)
