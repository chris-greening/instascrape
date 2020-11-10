from __future__ import annotations

from typing import List
import warnings

from instascrape.core._mappings import _PostMapping, _ProfileMapping
from instascrape.core._static_scraper import _StaticHtmlScraper
from instascrape.scrapers.post import Post

warnings.simplefilter("always", DeprecationWarning)


class Profile(_StaticHtmlScraper):
    """
    Scraper for an Instagram profile page

    Methods
    -------
    from_username(shortcode: str) -> Post
        Factory method that returns a Profile object from a shortcode
    """

    _Mapping = _ProfileMapping

    def get_recent_posts(self, amt: int = 12) -> List[Post]:
        """
        Return a list of the profiles recent posts

        Parameters
        ----------
        amt : int
            Amount of recent posts to return

        Returns
        -------
        posts : List[Post]
            List containing the recent 12 posts and their available data
        """
        if amt > 12:
            raise IndexError(f"{amt} is too large, 12 is max available posts")
        posts = []
        post_arr = self.json_dict["entry_data"]["ProfilePage"][0]["graphql"]["user"]["edge_owner_to_timeline_media"][
            "edges"
        ]
        for post in post_arr[:amt]:
            json_dict = post["node"]
            mapping = _PostMapping.post_from_profile_mapping()
            post = Post(json_dict)
            post.scrape(mapping=mapping)
            posts.append(post)
        return posts

    def _url_from_suburl(self, suburl):
        return f"https://www.instagram.com/{suburl}/"

    @classmethod
    def from_username(cls, username):
        warnings.warn(
            "This will be deprecated in the near future. You no longer need to use from_username, simply pass username as argument to Profile",
            DeprecationWarning,
        )
        return Profile(username)
