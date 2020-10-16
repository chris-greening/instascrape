from __future__ import annotations

from typing import Any

from instascrape.core._static_scraper import _StaticHtmlScraper
from instascrape.core._mappings import _ProfileMapping

class Profile(_StaticHtmlScraper):
    """
    Scraper for an Instagram profile page

    Attributes
    ----------
    _Mapping
        Mapping class with directives specific to scraping JSON from an
        Instagram profile page

    Methods
    -------
    from_username(shortcode: str) -> Post
        Factory method that returns a Profile object from a shortcode
    """
    _Mapping = _ProfileMapping

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
