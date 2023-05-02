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

```bash
python main.py
```

## License

This project is licensed under the terms of the MIT license.

