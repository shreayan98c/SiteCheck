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

## License

This project is licensed under the terms of the MIT license.
