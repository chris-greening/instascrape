from __future__ import annotations

import datetime
from typing import List

from .insta_scraper import StaticInstaScraper
from .jsontools import PostJSON

class Post(StaticInstaScraper):
    def __init__(self, url: str) -> None:
        super().__init__(url)

    def _scrape_soup(self, soup) -> None:
        """Scrape data from the soup"""
        self.hashtags = self._get_hashtags(soup)
        super()._scrape_soup(soup)

    def _get_hashtags(self, soup) -> List[str]:
        hashtags_meta = soup.find_all("meta", {"property": "instapp:hashtags"})
        return [tag["content"] for tag in hashtags_meta]

    def _scrape_json(self, json_data: dict) -> None:
        """Scrape data from the posts json"""
        # TODO: might be a good idea to store these vars in a dataclass
        self.data = PostJSON(json_data)
        self.data.parse_json()

    @classmethod
    def from_shortcode(cls, shortcode: str) -> Post:
        """Return a Post given a shortcode"""
        url = f"https://www.instagram.com/p/{shortcode}/"
        return cls(url)


if __name__ == "__main__":
    url = r"https://www.instagram.com/p/CFQNno8hSDX/"
    post = Post(url)
    post.static_load()
