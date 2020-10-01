from __future__ import annotations

import json
import datetime
from typing import Dict
from abc import ABC, abstractmethod

import requests
from bs4 import BeautifulSoup

class StaticInstaScraper(ABC):
    """
    Abstract base class for the Profile, Post, and Hashtag subclasses
    that handles much of the routine scraping methods

    Attribues
    ---------
    url : str
        Full URL to an Instagram page

    Methods
    -------
    static_load(session=requests.Session())
        Makes request to URL, instantiates BeautifulSoup, finds JSON data,
        then parses JSON data.
    """

    _METADATA_KEYS = ['url', 'name', 'data']

    def __init__(self, url, name=None):
        """
        Parameters
        ----------
        url : str
            Full URL to an Instagram page
        """
        self.url = url
        if name is not None:
            self.name = name

    def static_load(self, session=requests.Session()):
        self._scrape_url(self.url, session=session)

    def to_dict(self) -> dict:
        """Return a dictionary containing all of the data that has been scraped"""
        return {key: val for key, val in self.__dict__.items() if key not in StaticInstaScraper._METADATA_KEYS}

    def to_list(self) -> dict:
        return [(key, val) for key, val in self.__dict__.items() if key not in StaticInstaScraper._METADATA_KEYS]

    def _scrape_url(self, url, session=requests.Session()) -> None:
        """Load url and scrape data"""
        page_source = session.get(url).text
        self._scrape_html(page_source)

    def _scrape_html(self, page_source):
        soup = BeautifulSoup(page_source, features='lxml')
        self._scrape_soup(soup)

    def _scrape_soup(self, soup):
        json_data = self._get_json_from_soup(soup)
        self._scrape_json(json_data)

    def _get_json_from_soup(self, soup) -> dict:
        """Return JSON data as a dictionary"""
        json_script = [
            str(script)
            for script in soup.find_all("script")
            if "config" in str(script)
        ][0]
        left_index = json_script.find("{")
        right_index = json_script.rfind("}") + 1
        json_str = json_script[left_index:right_index]
        return json.loads(json_str)

    def _load_json_into_namespace(self, data):
        """Parse and load JSON data into objects namespace"""
        data.parse_json()
        self.__dict__.update(data.to_dict())

    @abstractmethod
    def _scrape_json(self, json_data):
        """
        Specific way of scraping the JSON data is left up to the subclasses
        """
        pass

    def __repr__(self):
        return f"<{self.url}: {type(self).__name__}>"

