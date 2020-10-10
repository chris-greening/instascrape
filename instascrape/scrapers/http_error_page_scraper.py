from __future__ import annotations

from typing import Any
import datetime

from . import static_scraper
from . import json_scraper

class HttpErrorScraper(static_scraper.StaticHTMLScraper):
    """
    Scraper for an HTTP Error page.

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

    def _scrape_json(self, json_data: dict):
        """Scrape JSON data and load into instances namespace"""
        self.data = HttpErrorPageJSON()
        self.data.parse_full(json_data)
        self._load_json_into_namespace(self.data)

class HttpErrorPageJSON(json_scraper.JSONScraper):
    def parse_full(self, window_dict: dict, missing: Any = "ERROR", exception: bool = True) -> None:
        """Parse .json data from window"""
        self.json_dict = window_dict
        self.parse_base(window_dict, missing, exception)

        self.scrape_timestamp = datetime.datetime.now()

if __name__ == "__main__":
    url = r"https://www.instagram.com/idkdidkdidkdidkdkdidkkdidikd"
    http_error_page = HttpErrorScraper(url)
    http_error_page.static_load()
