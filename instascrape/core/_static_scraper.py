from __future__ import annotations

import json
import datetime
from typing import Dict, Any
from abc import ABC, abstractmethod
import csv
import json

import requests
from bs4 import BeautifulSoup

from instascrape.scrapers.json_scraper import JsonScraper
from instascrape.core._mappings import _MetaMapping

class _StaticHtmlScraper(ABC):
    _METADATA_KEYS = ['json_dict', 'url', '_json_scraper']

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

    def to_dict(self, metadata: bool = False) -> Dict[str, Any]:
        data_dict = {
            key: val
            for key, val in self.__dict__.items()
                if key not in self._METADATA_KEYS
        } if not metadata else self.__dict__
        return data_dict

    def to_csv(self, fp: str, metadata: bool = False):
        with open(fp, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            for key, value in self.to_dict(metadata=metadata).items():
                writer.writerow([key, value])

    def to_json(self, fp: str, metadata: bool = False):
        with open(fp, 'w') as outjson:
            json.dump(self.to_dict(metadata=metadata), outjson)

    def __getitem__(self, key):
        return getattr(self, key)

    def _load_into_namespace(self, scraped_dict):
        for key, val in scraped_dict.items():
            setattr(self, key, val)



