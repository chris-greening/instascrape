from __future__ import annotations

from .insta_scraper import StaticInstaScraper
from .jsontools import LoginAndSignupJSON


class LoginAndSignupPage(StaticInstaScraper):
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
        self.data = LoginAndSignupJSON(json_data)
        self._load_json_into_namespace(self.data)

if __name__ == "__main__":
    url = r"https://www.instagram.com/accounts/login"
    login = LoginAndSignupPage(url)
    login.static_load()