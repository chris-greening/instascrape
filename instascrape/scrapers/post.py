from __future__ import annotations

import datetime
from typing import List

from instascrape.core._mappings import _PostMapping
from instascrape.core._static_scraper import _StaticHtmlScraper
from instascrape.scrapers.json_tools import parse_json_from_mapping

# pylint: disable=no-member


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
    def load_from_mapping(self, json_dict, map_dict):
        data_dict = parse_json_from_mapping(json_dict, map_dict)
        post = Post.from_shortcode(data_dict["shortcode"])
        for key, val in data_dict.items():
            setattr(post, key, val)
        # TODO: Bad encapsulation, figure a better way of handling timestamp
        post.upload_date = datetime.datetime.fromtimestamp(post.upload_date)
        return post

    @classmethod
    def from_shortcode(cls, shortcode: str) -> Post:
        url = f"https://www.instagram.com/p/{shortcode}/"
        return cls(url, name=shortcode)
