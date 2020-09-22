import json

import requests 
from bs4 import BeautifulSoup 

class Post: 
    def __init__(self, url):
        self.url = url
         
    def load_page_source(self):
        """Load the static HTML into a BeautifulSoup object at the url"""
        self.page_source = requests.get(self.url).text
        self.soup = BeautifulSoup(self.page_source, features='lxml')

        self._scrape_soup()

    def _scrape_soup(self):
        """Scrape data from the soup"""
        self.title = self.soup.find("title").text
        
        self._scrape_post_json()

    def _scrape_post_json(self): 
        """Get the posts json data as a dictionary"""
        post_json_script = [str(script) for script in self.soup.find_all('script') if 'config' in str(script)][0]
        left_index = post_json_script.find('{')
        right_index = post_json_script.rfind('}') + 1
        json_str = post_json_script[left_index:right_index]
        self.post_json = json.loads(json_str)

    @classmethod
    def from_shortcode(cls, shortcode: str) -> 'Post':
        """Return a Post given a shortcode"""
        url = f'https://www.instagram.com/{shortcode}/'
        return Post(url)
    
if __name__ == '__main__':
    url = r'https://www.instagram.com/p/CFQNno8hSDX/'
    post = Post(url)
    post.load_page_source()