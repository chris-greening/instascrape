from __future__ import annotations

from typing import List

from instascrape.core._mappings import _LocationMapping, _PostMapping
from instascrape.core._static_scraper import _StaticHtmlScraper
from instascrape.scrapers.post import Post

class Location(_StaticHtmlScraper):
    """Scraper for an Instagram profile page"""

    _Mapping = _LocationMapping

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
        post_arr = self.json_dict["entry_data"]["LocationsPage"][0]["graphql"]["location"]["edge_location_to_media"]["edges"]
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
        raise ValueError("suburl not currently supported for Location scrape, please pass a full URL to the location you want to scrape")
