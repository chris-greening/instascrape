from __future__ import annotations

import datetime
from typing import List

import requests

from .insta_scraper import StaticInstaScraper
from .hashtag import Hashtag
from .jsontools import PostJSON

class Post(StaticInstaScraper):
    """
    Representation of a single Instagram post.

    Attribues
    ---------
    url : str
        Full URL to an existing Instagram profile

    Methods
    -------
    static_load(session=requests.Session())
        Makes request to URL, instantiates BeautifulSoup, finds JSON data,
        then parses JSON data.
    scrape_hashtags
    """
    def _scrape_soup(self, soup) -> None:
        """Scrape data from the soup"""
        self.hashtags = self._get_hashtags(soup)
        super()._scrape_soup(soup)

    def _get_hashtags(self, soup) -> List[str]:
        hashtags_meta = soup.find_all("meta", {"property": "instapp:hashtags"})
        return [tag["content"] for tag in hashtags_meta]

    def _scrape_json(self, json_data: dict) -> None:
        """Scrape data from the posts json"""
        self.data = PostJSON(json_data)
        self._load_json_into_namespace(self.data)

    def scrape_hashtags(self, session=requests.Session(), status_output=False):
        """Load hashtags used in post as Hashtag objects"""
        self.hashtag_objects = []
        for tag in self.hashtags:
            if status_output: print(f"Loading {tag}")
            tag_obj = Hashtag.from_hashtag(tag)
            tag_obj.static_load(session=session)

    @classmethod
    def from_shortcode(cls, shortcode: str) -> Post:
        """
        Factory method for convenience to create Post instance given
        just a shortcode instead of a full URL.

        Parameters
        ----------
        shortcode : str
            Shortcode of the Post for scraping

        Returns
        -------
        Post(url)
            Instance of Post with URL at the given shortcode

        Example
        -------
        >>>Post.from_shortcode('CFcSLyBgseW')
        <https://www.instagram.com/p/CFcSLyBgseW/: Post>
        """
        url = f"https://www.instagram.com/p/{shortcode}/"
        return cls(url, name=shortcode)


if __name__ == "__main__":
    url = r"https://www.instagram.com/p/CFQNno8hSDX/"
    post = Post(url)
    post.static_load()
