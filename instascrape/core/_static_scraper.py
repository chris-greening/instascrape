from __future__ import annotations

import datetime
import json
import csv
from abc import ABC, abstractmethod
from typing import Union, Dict, List, Any
import warnings

import requests
from bs4 import BeautifulSoup

from instascrape.core._json_flattener import FlatJSONDict
from instascrape.scrapers.json_tools import parse_json_from_mapping, determine_json_type
from instascrape.exceptions.exceptions import InstagramLoginRedirectError

# pylint: disable=no-member

JSONDict = Dict[str, Any]
warnings.simplefilter("always", DeprecationWarning)

class _StaticHtmlScraper(ABC):
    """
    Base class for all of the scrapers, handles general functionality that all
    scraper objects will have

    Methods
    -------
    scrape(self, keys: List[str] = [], exclude: List[str] = []) -> None
        Scrape the static data from the page
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
        "soup",
        "html",
        "source",
    ]
    _ASSOCIATED_JSON_TYPE = None

    def __init__(self, source: Union[str, BeautifulSoup, JSONDict]) -> None:
        """
        Parameters
        ----------
        source : Union[str, BeautifulSoup, JSONDict]
            The given source for scraping the data from. Available sources are
            a URL, HTML, JSON dictionary, BeautifulSoup, etc.
        """
        self.source = source

        # Instance variables that are given values elsewhere
        self.url = None
        self.html = None
        self.soup = None
        self.json_dict = None
        self.flat_json_dict = None
        self.scrape_timestamp = None

    def __getitem__(self, key):
        return getattr(self, key)

    def __repr__(self):
        return f"<{type(self).__name__}>"

    def load(self, mapping=None, keys: List[str] = None, exclude: List[str] = None):
        msg = "f{type(self).__name__}.load will be permanently renamed to {type(self).__name__}.scrape, use that method instead for future compatibility"
        warnings.warn(msg, DeprecationWarning)
        self.scrape(mapping, keys, exclude)

    def scrape(self, mapping=None, keys: List[str] = None, exclude: List[str] = None) -> None:
        """
        Scrape data from self.source and load as instance attributes

        Parameters
        ----------
        mapping : Dict[str, deque]
            Dictionary of parsing queue's that tell the JSON engine how to
            process the JSON data
        keys : List[str]
            List of strings that correspond to desired attributes for scraping
        exclude : List[str]
            List of strings that correspond to which attributes to exclude from
            being scraped
        """
        if mapping is None:
            mapping = self._Mapping
        if keys is None:
            keys = []
        if exclude is None:
            exclude = []

        # If the passed source was already an object, construct data from
        # source else parse it
        if type(self.source) is type(self):
            scraped_dict = self.source.to_dict()
        else:
            self.json_dict = self._get_json_from_source(self.source)
            self.flat_json_dict = FlatJSONDict(self.json_dict)
            scraped_dict = parse_json_from_mapping(
                json_dict=self.flat_json_dict,
                map_dict=self._Mapping.return_mapping(keys=keys, exclude=exclude),
            )
        self._load_into_namespace(scraped_dict)

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
        data_dict : Dict[str, Any]
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
        with open(fp, "w", newline="", encoding="utf-8") as csv_file:
            writer = csv.writer(csv_file)
            for key, value in self.to_dict().items():
                writer.writerow([key, str(value)])

    def to_json(self, fp: str) -> None:
        """
        Write scraped data to .json file at the given filepath

        Parameters
        ----------
        fp : str
            Filepath to write data to
        """
        outdict = {key: str(val) for key, val in self.to_dict().items()}
        with open(fp, "w") as outjson:
            json.dump(outdict, outjson)

    @abstractmethod
    def _url_from_suburl(self, suburl):
        pass

    # @abstractmethod
    # def _verify_correct_json_type(self, json_dict):
    #     pass

    def _get_json_from_source(self, source):
        """Parses the JSON data out from the source based on what type the source is"""
        initial_type = True
        if isinstance(source, str):
            source_type = self._determine_string_type(source)
        elif isinstance(source, dict):
            json_dict = source
            return json_dict
        elif isinstance(source, BeautifulSoup):
            source_type = "soup"

        if source_type == "suburl":
            if initial_type:
                suburl = self.source
            self.url = self._url_from_suburl(suburl=suburl)
            source_type = "url"
            initial_type = False

        if source_type == "url":
            if initial_type:
                self.url = self.source
            self.html = self._html_from_url(url=self.url)
            source_type = "html"
            initial_type = False

        if source_type == "html":
            if initial_type:
                self.html = self.source
            self.soup = self._soup_from_html(self.html)
            source_type = "soup"
            initial_type = False

        if source_type == "soup":
            if initial_type:
                self.soup = self.source
            json_dict_str = self._json_str_from_soup(self.soup)
            source_type = "JSON dict str"
            initial_type = False

        if source_type == "JSON dict str":
            if initial_type:
                json_dict_str = self.source
            json_dict = self._dict_from_json_str(json_dict_str)

        return json_dict

    def _load_into_namespace(self, scraped_dict):
        """Loop through the scraped dictionary and set them as instance attr"""
        for key, val in scraped_dict.items():
            setattr(self, key, val)
        self.scrape_timestamp = datetime.datetime.now()

    @staticmethod
    def _html_from_url(url) -> str:
        """Requests page at given URL to get given HTML"""
        response = requests.get(url)
        return response.text

    @staticmethod
    def _soup_from_html(html):
        """Instantiates BeautifulSoup from the given source"""
        return BeautifulSoup(html, features="lxml")

    @staticmethod
    def _json_str_from_soup(soup):
        """Instantiates a JSON dictionary from BeautifulSoup"""
        json_script = [str(script) for script in soup.find_all("script") if "config" in str(script)][0]
        left_index = json_script.find("{")
        right_index = json_script.rfind("}") + 1
        json_str = json_script[left_index:right_index]

        return json_str

    def _dict_from_json_str(self, json_str):
        """Load JSON data from a string"""
        json_dict = json.loads(json_str)
        json_type = determine_json_type(json_dict)
        if json_type == 'LoginAndSignupPage' and not type(self).__name__ == 'LoginAndSignupPage':
            raise InstagramLoginRedirectError
        return json_dict

    @staticmethod
    def _determine_string_type(string_data):
        """Determine's what type of source the string is"""
        string_type_map = [("https://", "url"), ("window._sharedData", "html"), ('{"config"', "JSON dict str")]
        for substr, str_type in string_type_map:
            if substr in string_data:
                if substr == "https://" and "!DOCTYPE" in string_data:
                    continue
                break
        else:
            str_type = "suburl"
        return str_type
