# SiteCheck

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](<https://opensource.org/licenses/MIT>)

A web crawler that can check websites for broken links, missing images, and other issues.

## Installation

These instructions assume a working installation of [Anaconda](https://www.anaconda.com/).

```bash
git clone git@github.com:shreayan98c/SiteCheck.git
conda create --name SiteCheck
conda activate SiteCheck
pip install -r requirements.txt
```

## Dependencies

Download [ChromeDriver](https://chromedriver.chromium.org/downloads) or [GeckoDriver](https://github.com/mozilla/geckodriver/releases)
Update the path in the file utils.py in the function eval_accessibility() to the location of the driver.

## Usage

To view the interface through the flask app:
```bash
flask run
```
OR
```bash
python app.py
```
And open the localhost link (http://127.0.0.1:5000/) in your browser.


To run the test functions without the interface:
```bash
python main.py
```

## Applications

1. Broken Links/Tags detection on the website
2. Find out missing images or images that are not displaying properly
3. Get a compliance report for the website whether it meets the standards or not
4. Get suggestions for increasing the usability and accessibility of the website
5. Get an hierarchy of the website in the form of a tree and check easy of navigation

## Extensions

1. Check permission and cookies and access to see if resources are accessible or not
2. Flag all the non trusted links and do not recursively traverse them
3. Further detailed analyses and reports for the website in form of drilldown charts
4. Interactive interface and charts for the users to drill down


## License

This project is licensed under the terms of the MIT license.
