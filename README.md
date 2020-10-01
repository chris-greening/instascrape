![instascrape logo](/media/logo.png?raw=true)

# instascrape: super lightweight Instagram scraping toolkit

## What is it?
> **instascrape** is an incredibly lightweight set of tools geared towards scraping Instagram data. It makes *no* assumptions about your project and is instead designed for flexibility and developer productivity. It is excellent for for the seasoned data scientist trying to quickly get an idea of a pages engagement as well as beginners looking to explore web scraping and the beauty of Python for the very first time. 

[![Version](https://img.shields.io/pypi/pyversions/insta-scrape)](https://www.python.org/downloads/release/python-360/)
[![Language](https://img.shields.io/github/languages/top/chris-greening/instascrape)](https://www.python.org/) 
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Release](https://img.shields.io/pypi/v/insta-scrape)](https://pypi.org/project/insta-scrape/)
[![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](https://opensource.org/licenses/MIT) 

[![Downloads](https://pepy.tech/badge/insta-scrape)](https://pepy.tech/project/insta-scrape)
[![Activity](https://img.shields.io/github/last-commit/chris-greening/instascrape)](https://github.com/chris-greening/instascrape) 
[![Dependencies](https://img.shields.io/librariesio/github/chris-greening/instascrape)](https://github.com/chris-greening/instascrape/blob/master/requirements.txt)
[![Size](https://img.shields.io/github/repo-size/chris-greening/instascrape)](https://github.com/chris-greening/instascrape) 

![Sample programming gif](/media/sample_code.gif?raw=true)

---

## Table of Contents 
* [Installation](#installation)
  * [pip](#pip)
  * [clone](#clone)
* [Documentation](#documentation)
* [Features](#features)
  * [Profile](#profile)
  * [Post](#post)
  * [Hashtag](#hashtag)
* [License](#license)
* [Support](#support)

![Graph of instagram data](/media/realpython.png?raw=true)
Example of Instagram likes per post data scraped using instascrape (this repository and its author(s) are not affiliated with Real Python)

---

## Installation

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
> and install required dependencies using 
```shell
$ pip3 install -f requirements.txt
```

---

## Documentation 
The official documentation can be found on [Read The Docs](https://instascrape.readthedocs.io/en/latest/index.html)

---

## Features

### Profile 
> Representation of an Instagram profile. Calling static_load takes care of requesting and scraping static HTML regarding the given URL or username. 
> Profile.static_load scrapes 36 data points including 

<img src="media/profile_example 0.png" width=700>

### Post
> Representation of a single Instagram post. Calling static_load takes care of requesting and scraping static HTML regarding the given URL or post shortcode.
> Post.static_load scrapes 29 data points including
```python
likes: int
amount_of_comments: int
hashtags: List[str]
tagged_users: List[str]
caption: str
location: str
#etc. 
```
> Sample code:
```python
from instascrape import Post 
url = 'https://www.instagram.com/p/CFcSLyBgseW/'
post = Post(url)
post.static_load()
```

### Hashtag
> Representation of an Instagram hashtag page. Calling static_load takes care of requesting and scraping static HTML regarding the given URL or hashtag name.
> Hashtag.static_load scrapes 10 data points including
```python
amount_of_posts: int
name: str
is_following: bool
allow_following: bool
#etc. 
```
> Sample code:
```python
from instascrape import Hashtag 
url = 'https://www.instagram.com/explore/tags/python/'
hashtag = Hashtag(url)
hashtag.static_load()
```
---

## License
[MIT](LICENSE)

---

## Support 
Reach out to me if you have questions or ideas!
- chris@christophergreening.com
