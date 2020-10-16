from __future__ import annotations
# pylint: disable=used-before-assignment

import datetime
from typing import Any

from instascrape.core._static_scraper import _StaticHtmlScraper
from instascrape.core._mappings import _HashtagMapping

class Hashtag(_StaticHtmlScraper):
    _Mapping = _HashtagMapping

    @classmethod
    def from_hashtag(cls, hashtag: str):
        """
        Factory method for convenience to create Hashtag instance given
        just a hashtag name instead of a full URL.

        Parameters
        ----------
        hashtag : str
            Name of the Hashtag for scraping

        Returns
        -------
        Hashtag(url: str)
            Instance of Hashtag with URL created from the given hashtag name

        Example
        -------
        >>>Hashtag.from_hashtag('pythonprogramming')
        <https://www.instagram.com/tags/pythonprogramming/: Hashtag>
        """
        url = f"https://www.instagram.com/tags/{hashtag}/"
        return cls(url, name=hashtag)
