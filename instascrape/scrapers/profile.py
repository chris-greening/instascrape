from __future__ import annotations

from typing import Any

from instascrape.core._static_scraper import _StaticHtmlScraper
from instascrape.core._mappings import _ProfileMapping

class Profile(_StaticHtmlScraper):
    _Mapping = _ProfileMapping

    @classmethod
    def from_username(cls, username: str):
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
