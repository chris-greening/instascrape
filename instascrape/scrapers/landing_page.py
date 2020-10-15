from __future__ import annotations

from typing import Any
import datetime

from instascrape.scrapers import static_scraper
from instascrape.scrapers import json_scraper

class LandingPage(static_scraper.StaticHTMLScraper):
    """
    Scraper for the landing page.

    Attributes
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

class LandingPageJSON(json_scraper.JSONScraper):
    def parse_full(self, window_dict: dict, missing: Any = "ERROR", exception: bool = True) -> None:
        """Parse .json data from window"""
        self.json_dict = window_dict
        self.parse_base(window_dict, missing, exception)

        self.scrape_timestamp = datetime.datetime.now()


LandingPage.set_associated_json(LandingPageJSON)

if __name__ == "__main__":
    url = r"https://www.instagram.com"
    landing_page = LandingPage(url)
    landing_page.static_load()
