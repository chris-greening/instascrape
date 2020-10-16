from __future__ import annotations

import json
import datetime
from typing import Dict, Any
from abc import ABC, abstractmethod

import requests
from bs4 import BeautifulSoup

from instascrape.scrapers.json_scraper import JsonScraper
from instascrape.scrapers._mappings import _MetaMapping

class _StaticHtmlScraper(ABC):
    _METADATA_KEYS = ['json_dict', 'url']

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
        self.json_dict = self._json_scraper.json_from_url(self.url)
        map_type = self._json_scraper.determine_json_type(self.json_dict)
        mapper = _MetaMapping.get_mapper(map_type)
        scraped_dict = self._json_scraper.parse_json(json_dict=self.json_dict, map_dict=mapper.return_mapping())
        self._load_into_namespace(scraped_dict=scraped_dict)

    def to_dict(self, include_metadata: bool = False) -> Dict[str, Any]:
        pass

    def _load_into_namespace(self, scraped_dict):
        for key, val in scraped_dict.items():
            setattr(self, key, val)



