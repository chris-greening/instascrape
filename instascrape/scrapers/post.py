from __future__ import annotations
# pylint: disable=no-member

import datetime
from typing import List, Any

from instascrape.core._static_scraper import _StaticHtmlScraper
from instascrape.core._mappings import _PostMapping

class Post(_StaticHtmlScraper):
    _Mapping = _PostMapping

    def load(self, keys: List[str]):
        super().load(keys=keys)
        self.upload_date = datetime.datetime.fromtimestamp(self.upload_date)

    @classmethod
    def from_shortcode(cls, shortcode: str) -> Post:
        url = f"https://www.instagram.com/p/{shortcode}/"
        return cls(url, name=shortcode)


