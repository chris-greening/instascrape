from __future__ import annotations

# pylint: disable=used-before-assignment

import datetime
from typing import Any

from instascrape.core._static_scraper import _StaticHtmlScraper
from instascrape.core._mappings import _HashtagMapping


class Hashtag(_StaticHtmlScraper):
    """
    Scraper for an Instagram hashtag page
    """

    _Mapping = _HashtagMapping

    @classmethod
    def from_hashtag(cls, hashtag: str) -> Hashtag:
        url = f"https://www.instagram.com/tags/{hashtag}/"
        return cls(url, name=hashtag)