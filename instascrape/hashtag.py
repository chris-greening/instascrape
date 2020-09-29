from __future__ import annotations

from .insta_scraper import StaticInstaScraper
from .jsontools import HashtagJSON


class Hashtag(StaticInstaScraper):
    """
    Representation of an Instagram hashtag page.

    Attribues
    ---------
    url : str
        Full URL to a Instagram hashtag

    Methods
    -------
    static_load(session=requests.Session())
        Makes request to URL, instantiates BeautifulSoup, finds JSON data,
        then parses JSON data.
    """
    def _scrape_json(self, json_data: dict):
        """Scrape the JSON"""
        self.data = HashtagJSON(json_data)
        self._load_json_into_namespace(self.data)

    @classmethod
    def from_hashtag(cls, hashtag: str):
        """
        Factory method for convenience to create Hashtag instance given
        just a hashtag name instead of a full URL.

        Parameters
        ----------
        hashtag : str
            Name of the Hashtag for scraping

        Returns
        -------
        Hashtag(url: str)
            Instance of Hashtag with URL created from the given hashtag name

        Example
        -------
        >>>Hashtag.from_hashtag('pythonprogramming')
        <https://www.instagram.com/tags/pythonprogramming/: Hashtag>
        """
        url = f"https://www.instagram.com/tags/{hashtag}/"
        return cls(url, name=hashtag)


if __name__ == "__main__":
    url = "https://www.instagram.com/explore/tags/worldviewmag/"
    worldviewmag = Hashtag(url)
    worldviewmag.static_load()
