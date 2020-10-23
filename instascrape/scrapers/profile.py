from __future__ import annotations

from typing import List

from instascrape.core._mappings import _PostMapping, _ProfileMapping
from instascrape.core._static_scraper import _StaticHtmlScraper
from instascrape.scrapers.post import Post


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
            post = Post.load_from_mapping(json_dict, mapping)
            posts.append(post)
        return posts

    @classmethod
    def from_username(cls, username: str) -> Profile:
        """
        Factory method for convenience to create Profile instance given
        just a username instead of a full URL.

        Parameters
        ----------
        username : str
            Username of the Profile for scraping

        Returns
        -------
        Profile(url)
            Instance of Profile with URL at the given username

        Example
        -------
        >>>Profile.from_username('gvanrossum')
        <https://www.instagram.com/gvanrossum/: Profile>
        """

        url = f"https://www.instagram.com/{username}/"
        return cls(url, name=username)
