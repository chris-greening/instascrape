import requests 
from bs4 import BeautifulSoup 

class Post: 
    def __init__(self, url):
        self.url = url
         
    @classmethod
    def from_shortcode(cls, shortcode: str) -> Post:
        """Return a Post given a shortcode"""
        url = f'https://www.instagram.com/{shortcode}/'
        return Post(url)
    