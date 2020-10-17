from __future__ import annotations

# pylint: disable=no-member

import datetime
from typing import List, Any
import abc

from instascrape.core._static_scraper import _StaticHtmlScraper
from instascrape.core._mappings import _PostMapping
from instascrape.scrapers.json_scraper import JsonScraper


class Post(_StaticHtmlScraper):
    """
    Scraper for an Instagram post page

    Methods
    -------
    from_shortcode(shortcode: str) -> Post
        Factory method that returns a Post object from a shortcode
    """

    _Mapping = _PostMapping

    def load(self, keys: List[str] = [], exclude: List[str] = []):
        super().load(keys=keys)
        self.upload_date = datetime.datetime.fromtimestamp(self.upload_date)

    def to_json(self, fp: str):
        # have to convert to serializable format
        self.upload_date = datetime.datetime.timestamp(self.upload_date)
        super().to_json(fp=fp)
        self.upload_date = datetime.datetime.fromtimestamp(self.upload_date)

    def to_csv(self, fp: str):
        # have to convert to serializable format
        self.upload_date = datetime.datetime.timestamp(self.upload_date)
        super().to_csv(fp=fp)
        self.upload_date = datetime.datetime.fromtimestamp(self.upload_date)

    @classmethod
    def load_from_profile(self, json_dict, map_dict):
        json_scraper = JsonScraper()
        data_dict = json_scraper.parse_json(json_dict, map_dict)
        post = Post.from_shortcode(data_dict['shortcode'])
        for key, val in data_dict.items():
            setattr(post, key, val)
        return post

    @classmethod
    def from_shortcode(cls, shortcode: str) -> Post:
        url = f"https://www.instagram.com/p/{shortcode}/"
        return cls(url, name=shortcode)
