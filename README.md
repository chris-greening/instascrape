# instascrape

> Lightweight Python 3 web scraper for data mining Instagram easily and efficiently!

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

## Features
- Post
> Instantly scrape dozens of data points from a single Instagram post
```python
from instascrape.post import Post 
url = 'https://www.instagram.com/p/CFcSLyBgseW/'
post = Post(url)
post.load()
print(post.likes)        
print(post.upload_date)
```

## Support 
Reach out to me if you have questions or ideas!
- chris@christophergreening.com
