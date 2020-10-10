from __future__ import annotations

from typing import Any
import datetime

from . import static_scraper
from . import json_scraper

class LoginAndSignupPage(static_scraper.StaticHTMLScraper):
    """
    Scraper for the login and signup page.

    Attribues
    ---------
    url : str
        Full URL to an existing Instagram profile

    Methods
    -------
    static_load(session=requests.Session())
        Makes request to URL, instantiates BeautifulSoup, finds JSON data,
        then parses JSON data.
    """

    def _scrape_json(self, json_dict: dict):
        """Scrape the JSON"""
        super()._scrape_json(json_dict)

class LoginAndSignupJSON(json_scraper.JSONScraper):
    def parse_full(self, window_dict: dict, missing: Any = "ERROR", exception: bool = True) -> None:
        """Parse .json data from window"""
        self.json_dict = window_dict
        self.parse_base(window_dict, missing, exception)

        self.scrape_timestamp = datetime.datetime.now()


LoginAndSignupPage.set_associated_json(LoginAndSignupJSON)

if __name__ == "__main__":
    url = r"https://www.instagram.com/accounts/login"
    login = LoginAndSignupPage(url)
    login.static_load()
