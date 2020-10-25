![instascrape logo](/media/logo.png?raw=true)

# instascrape: super lightweight Instagram scraping toolkit

## What is it?
> **instascrape** is an incredibly lightweight set of tools geared towards scraping Instagram data. It makes *no* assumptions about your project and is instead designed for flexibility and developer productivity. It is excellent for the seasoned data scientist trying to quickly get an idea of a page's engagement as well as beginners looking to explore web scraping and the beauty of Python for the very first time.

[![Version](https://img.shields.io/pypi/pyversions/insta-scrape)](https://www.python.org/downloads/release/python-360/)
[![Language](https://img.shields.io/github/languages/top/chris-greening/instascrape)](https://www.python.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Release](https://img.shields.io/pypi/v/insta-scrape)](https://pypi.org/project/insta-scrape/)
[![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](https://opensource.org/licenses/MIT)

[![Downloads](https://pepy.tech/badge/insta-scrape)](https://pepy.tech/project/insta-scrape)
[![Activity](https://img.shields.io/github/last-commit/chris-greening/instascrape)](https://github.com/chris-greening/instascrape)
[![Dependencies](https://img.shields.io/librariesio/github/chris-greening/instascrape)](https://github.com/chris-greening/instascrape/blob/master/requirements.txt)
[![Issues](https://img.shields.io/github/issues/chris-greening/instascrape?style=flat)](https://github.com/chris-greening/instascrape/issues)
[![Size](https://img.shields.io/github/repo-size/chris-greening/instascrape)](https://github.com/chris-greening/instascrape)

![Example gif of instascrape](/media/instascrape.gif?raw=true)

---

## Table of Contents
* [:computer: Installation](#installation)
  * [pip](#pip)
  * [clone](#clone)
* [:books: Documentation](#documentation)
* [:newspaper: Blog Posts](#blog-posts)
* [:pray: Contributing](#contributing)
* [:spider_web: Dependencies](#dependencies)
* [:jack_o_lantern: Hacktoberfest 2020](#hacktoberfest-2020)
* [:credit_card: License](#license)
* [:grey_question: Support](#support)

<img src="media/6x6scatter_matrix.png" width="700"/>

---

## :computer: Installation <a name="installation"></a>

### Minimum Python version

This library currently requires [Python 3.7](https://www.python.org/downloads/release/python-370/) or higher.


### pip
> Install from PyPI using
```shell
$ pip3 install insta-scrape
```

### Clone
> Clone right from Github to your local machine using
```shell
$ git clone https://github.com/chris-greening/instascrape.git
```

> Install required dependencies using
```shell
$ pip3 install -r requirements.txt
```
---

## :books: Documentation <a name="documentation"></a>
The official documentation can be found on [Read The Docs](https://instascrape.readthedocs.io/en/latest/index.html) :newspaper:

---

## :newspaper: Blog Posts <a name="blog-posts"></a>

Check out blog posts on [DEV](https://dev.to/) for ideas and tutorials!
- [Scrape data from Instagram with instascrape](https://dev.to/chrisgreening/scrape-data-from-instagram-with-instascrape-5e3e) 
- [Visualizing Instagram engagement with instascrape](https://dev.to/chrisgreening/visualizing-instagram-engagement-with-instascrape-326h)
- [Exploratory data analysis of Instagram using instascrape and Python](https://dev.to/chrisgreening/exploratory-data-analysis-of-instagram-using-python-1o5c)
- [Creating a scatter matrix of Instagram data using Python](https://dev.to/chrisgreening/visualizing-the-relationship-between-instagram-variables-using-python-55gg)

![Heatmap](/media/likes_heatmap.png?raw=true)

![Graph of instagram data](/media/realpython.png?raw=true)
(this repository and its author(s) are not affiliated with Real Python)

---

## :pray: Contributing <a name="contributing"></a>
All contributions, bug reports, bug fixes, documentation improvements, enhancements, and ideas are welcome!

Feel free to [open an Issue](https://github.com/chris-greening/instascrape/issues/new/choose) or look at existing [Issues](https://github.com/chris-greening/instascrape/issues) to get a dialogue going on what you want to see added/changed/fixed!

---

## :spider_web: Dependencies <a name="dependencies"></a>

Instascrape primarily relies on two third-party libraries for requesting and scraping Instagram HTML content:

1. [Requests](https://requests.readthedocs.io/en/master/): HTTP requests
2.  [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/): Scraping and parsing HTML data.

The rest of its functionality is provided directly from Python 3's standard library for clear and concise code under the hood.

---



## :jack_o_lantern: Hacktoberfest 2020 <a name="hacktoberfest-2020"></a>
<img src="https://hacktoberfest.digitalocean.com/assets/HF-full-logo-b05d5eb32b3f3ecc9b2240526104cf4da3187b8b61963dd9042fdc2536e4a76c.svg" width="350"/>

This repo is participating in [Hacktoberfest 2020](https://hacktoberfest.digitalocean.com/)! I would love for this repo to be a resource to absolute beginners looking to make some of their first contributions. Check out [Issues](https://github.com/chris-greening/instascrape/issues) for some easy ideas or [open your own](https://github.com/chris-greening/instascrape/issues/new/choose) with something you want to work on! Please see the [official Hacktober FAQ](https://hacktoberfest.digitalocean.com/faq) for rules/questions.

Happy hacking!

---

## :credit_card: License <a name="license"></a>
[MIT](LICENSE)

---

## :grey_question: Support <a name="support"></a>
Reach out to me if you have questions or ideas!
- chris@christophergreening.com
:trollface: :rage2:

---

## Background 

The inspiration for this project began a long time ago in a galaxy far, far away (a.k.a. Summer 2019 on Long Island). I was mindlessly scrolling Instagram for the 1000th hour that week and thought, "How could I access this data programatically?". After 30 seconds of searching it became clear that Instagram's API was not going to be of any use so I was going to have to figure it out myself, and thus the beginning of instascrape was born. 
