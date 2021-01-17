"""
Hashtag
-------
    Scrape data from a Hashtag page
"""
from __future__ import annotations

from typing import List
import time

from instascrape.core._mappings import _HashtagMapping, _PostMapping
from instascrape.core._static_scraper import _StaticHtmlScraper
from instascrape.scrapers.post import Post

class Hashtag(_StaticHtmlScraper):
    """Scraper for an Instagram hashtag page"""

    _Mapping = _HashtagMapping

    def get_recent_posts(self, amt: int = 71) -> List[Post]:
        """
        Return a list of recent posts to the hasthag

        Parameters
        ----------
        amt : int
            Amount of recent posts to return

        Returns
        -------
        posts : List[Post]
            List containing the recent 12 posts and their available data
        """
        posts = []
        post_arr = self.json_dict["entry_data"]["TagPage"][0]["graphql"]["hashtag"]["edge_hashtag_to_media"]["edges"]
        amount_of_posts = len(post_arr)
        if amt > amount_of_posts:
            amt = amount_of_posts
        for post in post_arr[:amt]:
            json_dict = post["node"]
            mapping = _PostMapping.post_from_hashtag_mapping()
            post = Post(json_dict)
            post.scrape(mapping=mapping)
            posts.append(post)
        return posts

    def _url_from_suburl(self, suburl: str) -> str:
        return f"https://www.instagram.com/tags/{suburl}/"