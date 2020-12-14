from __future__ import annotations

from typing import List

from instascrape.core._mappings import _LocationMapping, _PostMapping
from instascrape.core._static_scraper import _StaticHtmlScraper
from instascrape.scrapers.post import Post


class Location(_StaticHtmlScraper):
    """Scraper for an Instagram profile page"""

    _Mapping = _LocationMapping

    def get_recent_posts(self, amt: int = 24) -> List[Post]:
        """
        Return a list of recent posts to the location

        Parameters
        ----------
        amt : int
            Amount of recent posts to return

        Returns
        -------
        posts : List[Post]
            List containing the recent 24 posts and their available data
        """
        posts = []
        post_arr = self.json_dict["entry_data"]["LocationsPage"][0]["graphql"]["location"]["edge_location_to_media"][
            "edges"
        ]
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

    def _url_from_suburl(self, suburl):
        return f"https://www.instagram.com/explore/locations/{suburl}/"
