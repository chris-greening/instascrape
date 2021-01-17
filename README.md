
<p align="center">
  <img src="media/logo.png" width="800px">
</p>

# _instascrape_: powerful Instagram data scraping toolkit 

[![Version](https://img.shields.io/pypi/pyversions/insta-scrape)](https://www.python.org/downloads/release/python-360/)
[![Downloads](https://pepy.tech/badge/insta-scrape)](https://pepy.tech/project/insta-scrape)
[![Release](https://img.shields.io/pypi/v/insta-scrape)](https://pypi.org/project/insta-scrape/)
[![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](https://opensource.org/licenses/MIT)

[![Activity](https://img.shields.io/github/last-commit/chris-greening/instascrape)](https://github.com/chris-greening/instascrape)
[![Dependencies](https://img.shields.io/librariesio/github/chris-greening/instascrape)](https://github.com/chris-greening/instascrape/blob/master/requirements.txt)
[![Issues](https://img.shields.io/github/issues/chris-greening/instascrape?style=flat)](https://github.com/chris-greening/instascrape/issues)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## What is it?
_instascrape_ is a lightweight Python package that provides an expressive and flexible API for scraping Instagram data. It is geared towards being a high-level building block on the data scientist's toolchain and can be seamlessly integrated and extended with industry standard tools for web scraping, data science, and analysis. 

<!-- ![Example showing tech profile scrapes](/media/techprofiles.gif) -->

## Key features  
Here are a few of the things that `instascrape` does well:

* Powerful, object-oriented scraping tools for profiles, posts, hashtags, reels, and IGTV
* Scrapes HTML, BeautifulSoup, and JSON
* Download content to your computer as _png_, _jpg_, _mp4_, and _mp3_
* Dynamically retrieve HTML embed code for posts
* Expressive and consistent API for concise and elegant code
* Designed for seamless integration with [_Selenium_](https://selenium-python.readthedocs.io/), [_Pandas_](https://pandas.pydata.org/), and other industry standard tools for data collection and analysis
* Lightweight; no boilerplate or configurations necessary 
* The only hard dependencies are [_Requests_](https://requests.readthedocs.io/en/master/) and [_Beautiful Soup_](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
* Proven to work as of January, 2021
---

## Table of Contents
* [Installation](#installation)
* [Sample Usage](#features)
* [Documentation](#documentation)
* [Blog Posts](#blog-posts)
* [Contributing](#contributing)
* [Dependencies](#dependencies)
* [License](#license)
* [Support](#support)

---

## :computer: Installation <a name="installation"></a>

### Minimum Python version

This library currently requires [Python 3.7](https://www.python.org/downloads/release/python-370/) or higher.


### pip
Install from PyPI using
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

print(google.followers)
print(google_post['hashtags'])
print(google_hashtag.amount_of_posts)
>>> 12262794
>>> ['growwithgoogle']
>>> 9053408
```

See the [Scraped data points](https://github.com/chris-greening/instascrape/wiki/Scraped-data-points) section of the [Wiki](https://github.com/chris-greening/instascrape/wiki) for a complete list of the scraped attributes provided by each scraper. 

## :books: Documentation <a name="documentation"></a>
The official documentation can be found on [Read The Docs](https://instascrape.readthedocs.io/en/latest/index.html)

---

## :newspaper: Blog Posts <a name="blog-posts"></a>


Check out blog posts on the [official site](https://chris-greening.github.io/instascrape/blog/) or [DEV](https://dev.to/) for ideas and tutorials!

- [Scrape data from Instagram with instascrape](https://dev.to/chrisgreening/scrape-data-from-instagram-with-instascrape-5e3e) 
- [Visualizing Instagram engagement with instascrape](https://dev.to/chrisgreening/visualizing-instagram-engagement-with-instascrape-326h)
- [Exploratory data analysis of Instagram using instascrape and Python](https://dev.to/chrisgreening/exploratory-data-analysis-of-instagram-using-python-1o5c)
- [Creating a scatter matrix of Instagram data using Python](https://dev.to/chrisgreening/visualizing-the-relationship-between-instagram-variables-using-python-55gg)
- [Downloading an Instagram profile's recent photos using Python](https://dev.to/chrisgreening/downloading-an-instagram-profile-s-recent-photos-using-python-25b2)
- [Scraping 25,000 data points from Joe Biden's Instagram using instascrape](https://dev.to/chrisgreening/scraping-25-000-data-points-from-joe-biden-s-instagram-using-instascrape-1026)
- [Compare major tech Instagram page's with instascrape](https://dev.to/chrisgreening/compare-major-tech-instagram-page-s-with-instascrape-2419)
- [Tracking an Instagram posts engagement in real time with instascrape](https://dev.to/chrisgreening/tracking-an-instagram-posts-engagement-in-real-time-with-instascrape-1m1j)
- [Dynamically generate embeddable Instagram HTML with instascrape](https://dev.to/chrisgreening/dynamically-generate-embeddable-instagram-html-using-instascrape-3o4b)
- [Scraping an Instagram location tag with instascrape](https://dev.to/chrisgreening/scraping-an-instagram-location-tag-with-instascrape-554f)
- [Scraping Instagram reels with instascrape](https://dev.to/chrisgreening/scraping-instagram-reels-with-instascrape-3khb)
- [Scraping IGTV data with instascrape](https://dev.to/chrisgreening/scraping-igtv-data-with-instascrape-595f)
- [Scraping 10,000 data points from Donald Trump's Instagram with Python](https://dev.to/chrisgreening/scraping-10-000-data-points-from-donald-trump-s-instagram-page-with-python-2jcg)
---

## :pray: Contributing <a name="contributing"></a>
All contributions, bug reports, bug fixes, documentation improvements, enhancements, and ideas are welcome!

Feel free to [open an Issue](https://github.com/chris-greening/instascrape/issues/new/choose), check out existing [Issues](https://github.com/chris-greening/instascrape/issues), or [start a discussion](https://github.com/chris-greening/instascrape/discussions). 

Beginners to open source are highly encouraged to participate and ask questions if you're unsure what to do/where to start :heart:

---

## :spider_web: Dependencies <a name="dependencies"></a>

- [Requests](https://requests.readthedocs.io/en/master/)
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)

---


## :credit_card: License <a name="license"></a>
This library operates under the [MIT](LICENSE) license.

---

## :grey_question: Support <a name="support"></a>

Check out the [FAQ](https://github.com/chris-greening/instascrape/wiki/Frequently-Asked-Questions)

Reach out to me if you want to connect or have any questions!
* Email:
  * chris@christophergreening.com
* Twitter:
  * [@ChrisGreening](https://twitter.com/ChrisGreening)
* LinkedIn
  * [Chris Greening](https://www.linkedin.com/in/chris-greening-646411139/)

---


<!-- The inspiration for this project began a long time ago in a galaxy far, far away (a.k.a. Summer 2019 on Long Island). I was mindlessly scrolling Instagram for the 1000th hour that week and thought, "How could I access this data programatically?". After 30 seconds of searching it became clear that Instagram's API was not going to be of any use so I was going to have to figure it out myself, and thus the beginning of instascrape was born. -->

DISCLAIMER: _With great power comes great responsibility_. This is a research project and I am not responsible for how you use it. Independently, the library is designed to be responsible and respectful and it is up to you to decide what you do with it. 

<p align="center">
  <img src="media/logopic.png" width="150px">
</p>
