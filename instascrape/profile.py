from __future__ import annotations

from .insta_scraper import StaticInstaScraper
from .jsontools import ProfileJSON

class Profile(StaticInstaScraper):
    def __init__(self, url):
        super().__init__(url)

    def _scrape_json(self, json_data: dict):
        self.data = ProfileJSON(json_data)
        self.data.parse_json()

    @classmethod
    def from_username(cls, username: str):
        url = f"https://www.instagram.com/{username}/"
        return cls(url)

if __name__ == "__main__":
    url = r"https://www.instagram.com/chris_greening/"
    profile = Profile(url)
    profile.static_load()
