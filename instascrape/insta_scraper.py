from __future__ import annotations

import json
import datetime
from typing import Dict
from abc import ABC, abstractmethod

import requests
from bs4 import BeautifulSoup


class StaticInstaScraper(ABC):
    def __init__(self, url):
        self.url = url

    def static_load(self) -> None:
        """Load static HTML at the given URL"""
        self.page_source = requests.get(self.url).text
        self.soup = BeautifulSoup(self.page_source, features="lxml")

        self._scrape_soup()

    def _scrape_soup(self) -> None:
        """Scrape data from soup, intended to be extendible by subclasses"""

        self.title = self.soup.find("title").text

        json_data = self._get_json()
        self._scrape_json(json_data)

    def _get_json(self) -> dict:
        """Return JSON data as a dictionary"""
        json_script = [
            str(script)
            for script in self.soup.find_all("script")
            if "config" in str(script)
        ][0]
        left_index = json_script.find("{")
        right_index = json_script.rfind("}") + 1
        json_str = json_script[left_index:right_index]
        return json.loads(json_str)

    @abstractmethod
    def _scrape_json(self, json_data: dict):
        """Specific implementation of how to scrape JSON left to sublasses"""
        pass
