from SiteCheck.utils import *


def main(url: str, depth: int, visited: set, api_responses: list):
    """
    Parse the given URL, extract the links and images, does preprocessing and writes the results to the outputs directory.
    :param url: url of the website to parse and test
    :param depth: depth of the recursion
    :param visited: set of visited urls
    :param api_responses: list of api responses
    :return: response across all the pages
    """
    if depth == 0:
        return api_responses

    if url in visited:
        return api_responses

    visited.add(url)

    api = {'current_url': url}

    start_time = time.time()
    warnings, errors = [], []
    try:
        response = requests.get(url)
        warnings, errors, ok = check_link(url, response, warnings, errors)
        if not ok:
            return api_responses
    except requests.exceptions.RequestException as e:
        errors.append(str(e))
        return api_responses
        
    soup = BeautifulSoup(response.text, 'html.parser')
    response_time = time.time() - start_time
    api['load_page_time'] = response_time

    links = extract_links(soup)
    api['links'] = links
    writelines('outputs/links.txt', links)
    images = extract_images(soup)
    api['images'] = json.dumps([str_repr.__repr__() for str_repr in images])
    writelines('outputs/images.txt', images)

    start_time = time.time()
    working_imgs = []
    for image in images:
        working_imgs, warnings, errors = check_image(img_tag=image, url=url, working_imgs=working_imgs,
                                                     warnings=warnings, errors=errors)
    images_check = time.time() - start_time
    api['check_imgs_time'] = images_check

    tag_counts = get_tag_counts(soup)
    tag_counts = dict(sorted(tag_counts.items(), key=lambda item: item[1], reverse=True))
    # filter only tags with more than 1 occurrence, ex: html, body, head, etc.
    tag_counts = {k: v for k, v in tag_counts.items() if v > 1}
    api['tag_counts'] = tag_counts

    lang_counts = get_lang_counts(soup)
    lang_counts = dict(sorted(lang_counts.items(), key=lambda item: item[1], reverse=True))
    api['lang_counts'] = lang_counts

    links = get_links(url)
    local_links = [link[0] for link in links if link[0].startswith(url) and not link[0].split('/')[-1].startswith('#')]
    nonlocal_links = get_nonlocal_links(url)
    nonlocal_links = [link[0] for link in nonlocal_links]
    api['local_links'] = local_links
    api['nonlocal_links'] = nonlocal_links

    violations = eval_accessibility(url)
    api['accessibility_violations'] = violations

    hierarchy = build_url_hierarchy(local_links)
    api['hierarchy'] = remove_empty_keys(hierarchy)

    api_responses.append(api)
    
    # send get request to nonlocal links and check response
    for link in nonlocal_links:
        if link not in visited:
            visited.add(link)
            try:
                link_response = requests.get(link)
                warnings, errors, ok = check_link(link, link_response, warnings, errors)
            except requests.exceptions.RequestException as e:
                errors.append(str(e))

    api['warnings'] = warnings
    api['errors'] = errors

    for link in local_links:
        api_responses = main(link, depth - 1, visited, api_responses)

    return api_responses


if __name__ == '__main__':
    url = "https://www.cs.jhu.edu/~schaud31/"
    depth = 2
    api_response = main(url, depth, set(), [])
    save_object(api_response, 'api.pkl')
    print('Saved api response to api.pkl')
