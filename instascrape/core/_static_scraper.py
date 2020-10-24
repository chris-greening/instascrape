from __future__ import annotations

import datetime
import json
import csv
from abc import ABC
from typing import Any, Dict, List

from instascrape.core._json_flattener import FlatJSONDict
from instascrape.scrapers.json_tools import json_from_url, parse_json_from_mapping

# pylint: disable=no-member


class _StaticHtmlScraper(ABC):
    """
    Base class for all of the scrapers, handles general functionality that all
    scraper objects will have

    Methods
    -------
    load(self, keys: List[str] = [], exclude: List[str] = []) -> None
        Load the static data from the page type
    to_dict(self, metadata: bool = False) -> Dict[str, Any]
        Returns a dictionary of the scraped data
    to_csv(self, fp: str, metadata: bool = False) -> None
        Writes the scraped data to a csv at the given filepath
    to_json(self, fp: str, metadata: bool = False) -> None
        Writes the scraped data to a json file at the given filepath
    """

    # Keys that represent metadata attr that the user doesn't necessarily need
    # to worry about
    _METADATA_KEYS = [
        "json_dict",
        "url",
        "_json_scraper",
        "scrape_timestamp",
        "map_dict",
        "json_data",
        "json_flattener",
        "flat_json_dict",
    ]

    def __init__(self, url, name=None):
        """
        Parameters
        ----------
        url : str
            Full URL to an Instagram page
        name : str
            Optional name for the user to pass
        """
        self.url = url
        if name is None:
            self.name = self.url

    def load(self, keys: List[str] = [], exclude: List[str] = []) -> None:
        """
        Scrape data at self.url and parse into attributes

        Parameters
        ----------
        keys : List[str]
            Specify what keys to exclusively load as strings in a list. If no
            keys are specified then the scrape will default load all data points.
        exclude : List[str]
            Specify what keys to exclude from being loaded. If no keys are
            specified, then no data points will be excluded.
        """
        if type(keys) == str:
            keys = [keys]
        if type(exclude) == str:
            exclude = [exclude]
        self.json_dict = json_from_url(self.url)
        self.flat_json_dict = FlatJSONDict(self.json_dict)
        scraped_dict = parse_json_from_mapping(
            json_dict=self.flat_json_dict,
            map_dict=self._Mapping.return_mapping(keys=keys, exclude=exclude),
        )
        self._load_into_namespace(scraped_dict=scraped_dict)
        self.scrape_timestamp = datetime.datetime.now()

    def to_dict(self, metadata: bool = False) -> Dict[str, Any]:
        """
        Return a dictionary containing all of the data that has been scraped

        Parameters
        ----------
        metadata : bool
            Boolean value that determines if metadata specified in self._METADATA_KEYS
            will be included in the dictionary.

        Returns
        -------
        data_dict : Dict[str, str]
            Dictionary containing the scraped data
        """
        data_dict = (
            {key: val for key, val in self.__dict__.items() if key not in self._METADATA_KEYS}
            if not metadata
            else self.__dict__
        )
        return data_dict

    def to_csv(self, fp: str) -> None:
        """
        Write scraped data to .csv at the given filepath

        Parameters
        ----------
        fp : str
            Filepath to write data to
        """
        with open(fp, "w", newline="") as csv_file:
            writer = csv.writer(csv_file)
            for key, value in self.to_dict().items():
                writer.writerow([key, value])

    def to_json(self, fp: str) -> None:
        """
        Write scraped data to .json file at the given filepath

        Parameters
        ----------
        fp : str
            Filepath to write data to
        """
        with open(fp, "w") as outjson:
            json.dump(self.to_dict(), outjson)

    def __getitem__(self, key):
        return getattr(self, key)

    def _load_into_namespace(self, scraped_dict):
        for key, val in scraped_dict.items():
            setattr(self, key, val)
