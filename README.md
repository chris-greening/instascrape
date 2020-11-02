![instascrape logo](/media/logo.png?raw=true)

# Instagram scraping for humans

## What is it?
> _instascrape_ is a powerful, lightweight library for scraping Instagram data with no configurations necessary! It is designed with flexibility and developer productivity in mind so you can stop wasting valuable time collecting data and just start analyzing :muscle:

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

![Example showing tech profile scrapes](/media/techprofiles.gif)

## Key features  
* :muscle: Powerful, object-oriented scraping tools as well as a variety of useful functions
* :dancer: Flexibly determines whether you want to scrape HTML, JSON, BeautifulSoup, or request and scrape the URL itself
* :floppy_disk: Download content to your computer as _png_, _jpg_, _mp4_, and _mp3_
* :musical_score: Expressive and consistent API for concise and elegant code
* :bar_chart: Designed for seamless integration with [_Selenium_](https://selenium-python.readthedocs.io/), [_Pandas_](https://pandas.pydata.org/), and other industry standard tools for data collection and analysis
* :hammer: Lightweight: you don't have to build a hammer factory when all you need is the hammer 
* :spider_web: The only hard dependencies are [_Requests_](https://requests.readthedocs.io/en/master/) and [_Beautiful Soup_](https://www.crummy.com/software/BeautifulSoup/bs4/doc/); no more worrying about configurations or webdrivers
* :watch: Proven to work as of October 29, 2020
---

## Table of Contents
* [:computer: Installation](#installation)
* [:mag_right: Sample Usage](#features)
* [:books: Documentation](#documentation)
* [:newspaper: Blog Posts](#blog-posts)
* [:pray: Contributing](#contributing)
* [:spider_web: Dependencies](#dependencies)
* [:credit_card: License](#license)
* [:grey_question: Support](#support)

---

## :computer: Installation <a name="installation"></a>

### Minimum Python version

This library currently requires [Python 3.7](https://www.python.org/downloads/release/python-370/) or higher.


### pip
> Install from PyPI using
```shell
$ pip3 install insta-scrape
```
WARNING: make sure you install _insta-scrape_ and not a package with a similar name! 

---

## :mag_right: Sample Usage <a name="features"></a>
All top-level, ready-to-use features can be imported using:
```python
from instascrape import *
```

_instascrape_ uses clean, consistent, and expressive syntax to make the developer experience as _painless_ as possible. 

```python
# Instantiate the scraper objects 
google = Profile('https://www.instagram.com/google/')
google_post = Post('https://www.instagram.com/p/CG0UU3ylXnv/')
google_hashtag = Hashtag('https://www.instagram.com/explore/tags/google/')

# Scrape their respective data 
google.scrape()
google_post.scrape()
google_hashtag.scrape()
```

After being scraped, relevant attributes can be accessed with dot (.) or bracket (\[\]) notation
```python
print(google.followers)
print(google_post['hashtags'])
print(google_hashtag.amount_of_posts)
>>> 12262794
>>> ['growwithgoogle']
>>> 9053408
```

## :books: Documentation <a name="documentation"></a>
The official documentation can be found on [Read The Docs](https://instascrape.readthedocs.io/en/latest/index.html) :newspaper:

---

## :newspaper: Blog Posts <a name="blog-posts"></a>

Check out blog posts on [DEV](https://dev.to/) for ideas and tutorials!
- [Scrape data from Instagram with instascrape](https://dev.to/chrisgreening/scrape-data-from-instagram-with-instascrape-5e3e) 
- [Visualizing Instagram engagement with instascrape](https://dev.to/chrisgreening/visualizing-instagram-engagement-with-instascrape-326h)
- [Exploratory data analysis of Instagram using instascrape and Python](https://dev.to/chrisgreening/exploratory-data-analysis-of-instagram-using-python-1o5c)
- [Creating a scatter matrix of Instagram data using Python](https://dev.to/chrisgreening/visualizing-the-relationship-between-instagram-variables-using-python-55gg)
- [Downloading an Instagram profile's recent photos using Python](https://dev.to/chrisgreening/downloading-an-instagram-profile-s-recent-photos-using-python-25b2)

---

## :pray: Contributing <a name="contributing"></a>
All contributions, bug reports, bug fixes, documentation improvements, enhancements, and ideas are welcome!

Feel free to [open an Issue](https://github.com/chris-greening/instascrape/issues/new/choose) or look at existing [Issues](https://github.com/chris-greening/instascrape/issues) to get a dialogue going on what you want to see added/changed/fixed.

Beginners to open source are highly encouraged to participate and ask questions :heart:

---

## :spider_web: Dependencies <a name="dependencies"></a>

Instascrape primarily relies on two third-party libraries for requesting and scraping Instagram HTML content:

1. [Requests](https://requests.readthedocs.io/en/master/): HTTP requests
2.  [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/): Scraping and parsing HTML data.

The rest of its functionality is provided directly from Python 3's standard library for unobtrusive code under the hood with little to no overhead.

---


## :credit_card: License <a name="license"></a>
[MIT](LICENSE)

---

## :grey_question: Support <a name="support"></a>
Reach out to me if you have questions or ideas!
* Email:
  * chris@christophergreening.com
* Instagram: 
  * [@chris_greening](https://www.instagram.com/chris_greening/)
* Twitter:
  * [@ChrisGreening2](https://twitter.com/ChrisGreening2)

---


<!-- The inspiration for this project began a long time ago in a galaxy far, far away (a.k.a. Summer 2019 on Long Island). I was mindlessly scrolling Instagram for the 1000th hour that week and thought, "How could I access this data programatically?". After 30 seconds of searching it became clear that Instagram's API was not going to be of any use so I was going to have to figure it out myself, and thus the beginning of instascrape was born. -->

<p align="center">
  <img src="media/logopic.png">
</p>
