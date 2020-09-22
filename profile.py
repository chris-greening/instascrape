import json

import requests 
from bs4 import BeautifulSoup

#TODO: A lot of the code from this and Post can probably be consolidated into a 
#super class (Hashtags might also work the same way)

class Profile:
    def __init__(self, url):
        self.url = url
    
    def load(self):
        """Load the static HTML into a BeautifulSoup object at the url"""
        self.page_source = requests.get(self.url).text
        self.soup = BeautifulSoup(self.page_source, features='lxml')

        self._scrape_soup()

    def _scrape_soup(self):
        """Scrape data from the soup"""
        self.title = self.soup.find("title").text
        
        prof_json = self._get_json()
        self._scrape_json(prof_json)

    def _get_json(self):
        json_script = [str(script) for script in self.soup.find_all('script') if 'config' in str(script)][0]
        left_index = json_script.find('{')
        right_index = json_script.rfind('}') + 1
        json_str = json_script[left_index:right_index]
        return json.loads(json_str)

    def _scrape_json(self, prof_json):
        self.country_code = prof_json['country_code']
        self.language_code = prof_json['language_code']
        self.locale = prof_json['locale']

        #Convenience definition for post info 
        self.prof_info = prof_json['entry_data']['ProfilePage'][0]#['graphql']['shortcode_media']


    @classmethod 
    def from_username(cls, username):
        url = f'https://www.instagram.com/{username}/'
        return cls(url)

if __name__ == '__main__':
    url = r'https://www.instagram.com/chris_greening/'
    profile = Profile(url)
    profile.load()