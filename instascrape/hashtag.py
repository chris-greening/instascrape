from __future__ import annotations

from .insta_scraper import StaticInstaScraper
from .jsontools import HashtagJSON

class Hashtag(StaticInstaScraper):
    def __init__(self, url):
        super().__init__(url)

    def _scrape_json(self, json_data: dict):
        """Scrape the JSON"""
        self.data = HashtagJSON(json_data)
        self.data.parse_json()

    @classmethod
    def from_hashtag(cls, hashtag: str):
        url = f"https://www.instagram.com/tags/{hashtag}/"
        return cls(url)


if __name__ == "__main__":
    url = "https://www.instagram.com/explore/tags/worldviewmag/"
    worldviewmag = Hashtag(url)
    worldviewmag.static_load()
