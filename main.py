from SiteCheck.utils import *


def main(url: str):

    print(f"Parsing URL: {url}")

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    links = extract_links(soup)
    print(f'{len(links)} links found')
    writelines('links.txt', links)
    images = extract_images(soup)
    print(f'{len(images)} links found')
    writelines('images.txt', images)

    for image in images:
        check_image(img_tag=image, url=url)


if __name__ == '__main__':
    url = "https://www.cs.jhu.edu/~schaud31/"
    # url = "https://www.w3schools.com/tags/tryit.asp?filename=tryhtml_image_test"
    main(url)
