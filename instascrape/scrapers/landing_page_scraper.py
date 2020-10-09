from __future__ import annotations

from . import static_scraper
from . import json_scraper

class LandingPageScraper(static_scraper.StaticHTMLScraper):
    """
    Representation of an Instagram profile page.

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
        self.data = LandingPageJSON(json_data)
        self._load_json_into_namespace(self.data)

class LandingPageJSON(json_scraper.JSONScraper):
    def parse_json(self, *args, **kwargs) -> None:
        super().parse_json(*args, **kwargs)

if __name__ == "__main__":
    url = r"https://www.instagram.com"
    landing_page = LandingPageScraper(url)
    landing_page.static_load()
