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

    def __init__(self, url):
        """
        Parameters
        ----------
        url : str
            Full URL to an Instagram page
        """
        self.url = url

    def static_load(self, session=requests.Session()):
        self._scrape_url(self.url, session=session)

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

    @abstractmethod
    def _scrape_json(self, json_data):
        """
        Specific way of scraping the JSON data is left up to the subclasses
        """
        pass

    def __repr__(self):
        return f"<{self.url}: {type(self).__name__}>"

