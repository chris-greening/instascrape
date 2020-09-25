# instascrape

> Lightweight Python 3 web scraper for data mining Instagram easily and efficiently!

## Table of Contents 
* [Installation](#installation)
* [Features](#features)
  * [Profile](#profile)
  * [Post](#post)
  * [Hashtag](#hashtag)
* [Support](#support)

---

## Installation

### Clone 
- Clone to your local machine using 
```shell
$ git clone https://github.com/chris-greening/instascrape.git 
```
### Setup 
- Install required dependencies using 
```shell
$ pip3 install -f requirements.txt
```

---

## Features

### Profile 
> Representation of an Instagram profile. Calling static_load takes care of requesting and scraping static HTML regarding the given URL or username. 
> Profile.static_load scrapes 36 data points including 
- followers:        int
- following:        int
- post count:       int 
- profile pic URL:  str
- business account: bool
- verified:         bool 
- etc. 
```python
from instascrape import Profile
url = 'https://www.instagram.com/gvanrossum/'
post = Profile(url)
post.static_load()
```

### Post
> Representation of a single Instagram post. Calling static_load takes care of requesting and scraping static HTML regarding the given URL or post shortcode.
> Post.static_load scrapes 29 data points including
- amount of likes:    int
- amount of comments: int
- hashtags used:      List[str]
- usernames tagged:   List[str]
- caption:            str
- location:           str
- etc. 
```python
from instascrape import Post 
url = 'https://www.instagram.com/p/CFcSLyBgseW/'
post = Post(url)
post.static_load()
```

### Hashtag
> Representation of an Instagram hashtag page. Calling static_load takes care of requesting and scraping static HTML regarding the given URL or hashtag name.
> Hashtag.static_load scrapes 10 data points including
- amount of posts:    int
- pic URL:            str
- name:               str
- user is following:  bool
- allowed to follow:  bool
- etc. 
```python
from instascrape import Hashtag 
url = 'https://www.instagram.com/explore/tags/python/'
hashtag = Hashtag(url)
hashtag.static_load()
```
---

## Support 
Reach out to me if you have questions or ideas!
- chris@christophergreening.com
