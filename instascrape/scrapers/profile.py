from __future__ import annotations

from typing import Any

from instascrape.scrapers import static_scraper

class Profile(static_scraper.StaticHTMLScraper):
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


if __name__ == "__main__":
    url = r"https://www.instagram.com/chris_greening/"
    profile = Profile(url)
    profile.static_load()
