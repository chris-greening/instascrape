import requests 
from bs4 import BeautifulSoup 

class Post: 
    def __init__(self, url):
        self.url = url
         
    def load_page_source(self):
        """Load the static HTML into a BeautifulSoup object at the url"""
        self.page_source = requests.get(self.url)
        self.soup = BeautifulSoup(self.page_source)

        self._scrape_soup()

    def _scrape_soup(self):
        """Scrape data from the soup"""
        self.title = self.soup.find("title").text

    @classmethod
    def from_shortcode(cls, shortcode: str) -> Post:
        """Return a Post given a shortcode"""
        url = f'https://www.instagram.com/{shortcode}/'
        return Post(url)
    