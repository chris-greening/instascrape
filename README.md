# instascrape

> Super lightweight Python 3 web scraping tools for data mining Instagram

[![Dependencies](https://img.shields.io/librariesio/github/chris-greening/instascrape)](https://github.com/chris-greening/instascrape/blob/master/requirements.txt)
[![Release](https://img.shields.io/pypi/v/insta-scrape)](https://pypi.org/project/insta-scrape/)
[![Activity](https://img.shields.io/github/last-commit/chris-greening/instascrape)](https://github.com/chris-greening/instascrape) 
[![Language](https://img.shields.io/github/languages/top/chris-greening/instascrape)](https://www.python.org/) 
[![Size](https://img.shields.io/github/repo-size/chris-greening/instascrape)](https://github.com/chris-greening/instascrape) 
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](https://opensource.org/licenses/MIT) 
---

## Table of Contents 
* [Installation](#installation)
  * [pip](#pip)
  * [clone](#clone)
* [Features](#features)
  * [Profile](#profile)
  * [Post](#post)
  * [Hashtag](#hashtag)
* [License](#license)
* [Support](#support)

---

## Installation

### pip
> Install from PyPI using
```shell
pip3 install insta-scrape
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

## Features

### Profile 
> Representation of an Instagram profile. Calling static_load takes care of requesting and scraping static HTML regarding the given URL or username. 
> Profile.static_load scrapes 36 data points including 
```python
followers: int
following: int
posts: int 
profile_pic_url: str
is_business_account: bool
is_verified: bool 
#etc. 
```
> Sample code:
```python
from instascrape import Profile
url = 'https://www.instagram.com/gvanrossum/'
post = Profile(url)
post.static_load()
```

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
