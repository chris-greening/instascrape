from __future__ import annotations

from insta_scraper import StaticInstaScraper

class Profile(StaticInstaScraper):
    def __init__(self, url):
       super().__init__(url)

    def _scrape_soup(self):
        """Scrape data from the profile page"""
        super()._scrape_soup()

    def _scrape_json(self, prof_json: dict):
        self.country_code = prof_json['country_code']
        self.language_code = prof_json['language_code']
        self.locale = prof_json['locale']

        #Convenience definition for post info 
        self.prof_info = prof_json['entry_data']['ProfilePage'][0]#['graphql']['shortcode_media']

    @classmethod 
    def from_username(cls, username: str):
        url = f'https://www.instagram.com/{username}/'
        return cls(url)

if __name__ == '__main__':
    url = r'https://www.instagram.com/chris_greening/'
    profile = Profile(url)
    profile.static_load()