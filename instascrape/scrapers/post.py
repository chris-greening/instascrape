from __future__ import annotations

import datetime
from typing import List, Any

import requests

from instascrape.scrapers import static_scraper

class Post(static_scraper.StaticHTMLScraper):
    @classmethod
    def from_shortcode(cls, shortcode: str) -> Post:
        url = f"https://www.instagram.com/p/{shortcode}/"
        return cls(url, name=shortcode)


if __name__ == "__main__":
    url = r"https://www.instagram.com/p/CFQNno8hSDX/"
    post = Post(url)
    post.static_load()
