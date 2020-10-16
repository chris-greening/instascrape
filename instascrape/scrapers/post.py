from __future__ import annotations
# pylint: disable=no-member

import datetime
from typing import List, Any

import requests

from instascrape.core._static_scraper import _StaticHtmlScraper

class Post(_StaticHtmlScraper):
    def load(self):
        super().load()
        self.upload_date = datetime.datetime.fromtimestamp(self.taken_at_timestamp)

    @classmethod
    def from_shortcode(cls, shortcode: str) -> Post:
        url = f"https://www.instagram.com/p/{shortcode}/"
        return cls(url, name=shortcode)


