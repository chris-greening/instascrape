from __future__ import annotations

import json
import datetime
from typing import Dict, List
from abc import ABC, abstractmethod

import requests
from bs4 import BeautifulSoup

from instascrape.scrapers.json_scraper import JsonScraper
from instascrape.scrapers.mappings import MetaMapping

class StaticHTMLScraper(ABC):
    def __init__(self, url, name=None):
        """
        Parameters
        ----------
        url : str
            Full URL to an Instagram page
        """
        self.url = url
        self._json_scraper = JsonScraper()

    def load(self):
        json_dict = self._json_scraper.json_from_url(self.url)
        mapper = MetaMapping.get_mapper(json_dict)
        scraped_dict = self._json_scraper.parse_json(json_dict=json_dict, map_dict=mapper.return_mapping())
        self._load_into_namespace(scraped_dict=scraped_dict)

    def _load_into_namespace(self, scraped_dict):
        for key, val in scraped_dict.items():
            setattr(self, key, val)



