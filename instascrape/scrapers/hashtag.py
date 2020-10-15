from __future__ import annotations
# pylint: disable=used-before-assignment

import datetime
from typing import Any
# sys.path.insert(0, os.path.abspath('..'))

from instascrape.scrapers import static_scraper
from instascrape.scrapers import json_scraper

class Hashtag(static_scraper.StaticHTMLScraper):
    """
    Scraper for gathering data from a hashtag page.

    Attributes
    ---------
    hashtag : str
        Full URL to a Instagram hashtag

    Methods
    -------
    from_hashtag(hashtag)
        Creates a StaticHTMLScraper to scrape hastags page
    """

    def _scrape_json(self, json_dict: dict):
        """Scrape the JSON"""
        super()._scrape_json(json_dict)

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

class HashtagJSON(json_scraper.JSONScraper):
    """
    Tool for parsing data from Instagram hashtag JSON data

    Attributes
    ----------
    json_dict : dict
        Python dictionary containing the Instagram JSON data
    name : str, optional
        Custom name that will represent this JSON data

    Methods
    -------
    parse_full(self, window_dict: dict, missing: Any = "ERROR", exception: bool = True) -> None
        Parse .json data from window
    parse_partial(self, tag_dict: dict, missing: Any = "ERROR", exception: bool = True) -> None
        Parse partial data from tag dictionary
    """

    def parse_full(self, window_dict: dict, missing: Any = "ERROR", exception: bool = True) -> None:
        """Parse .json data from window"""
        self.json_dict = window_dict
        self.parse_base(window_dict, missing, exception)
        tag_dict = window_dict["entry_data"]["TagPage"][0]["graphql"]["hashtag"]
        self.parse_partial(tag_dict, missing, exception)

        self.scrape_timestamp = datetime.datetime.now()

    def parse_partial(self, tag_dict: dict, missing: Any = "ERROR", exception: bool = True) -> None:
        self.id = tag_dict["id"]
        self.name = tag_dict["name"]
        self.allow_following = tag_dict["allow_following"]
        self.is_following = tag_dict["is_following"]
        self.is_top_media_only = tag_dict["is_top_media_only"]
        self.profile_pic_url = tag_dict["profile_pic_url"]
        self.amount_of_posts = tag_dict["edge_hashtag_to_media"]["count"]

        self.scrape_timestamp = datetime.datetime.now()


Hashtag.set_associated_json(HashtagJSON)


if __name__ == "__main__":
    url = "https://www.instagram.com/explore/tags/worldviewmag/"
    worldviewmag = Hashtag(url)
    worldviewmag.static_load()
