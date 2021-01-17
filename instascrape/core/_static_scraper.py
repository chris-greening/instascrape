from __future__ import annotations

import datetime
import json
import csv
from abc import ABC, abstractmethod
from typing import Union, Dict, List, Any
import sys
import os
from collections import namedtuple
import warnings

import requests
from bs4 import BeautifulSoup

from instascrape.scrapers.scrape_tools import parse_data_from_json, determine_json_type, flatten_dict, json_from_soup
from instascrape.exceptions.exceptions import InstagramLoginRedirectError, MissingSessionIDWarning, MissingCookiesWarning

# pylint: disable=no-member

JSONDict = Dict[str, Any]

class _StaticHtmlScraper(ABC):
    """
    Base class for all of the scrapers, handles general functionality that all
    scraper objects will have
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

    session = requests.Session()

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

    def __getitem__(self, key: str) -> Any:
        return getattr(self, key)

    def __repr__(self) -> str:
        return f"<{type(self).__name__}>"

    def scrape(
        self,
        mapping=None,
        keys: List[str] = None,
        exclude: List[str] = None,
        headers={
            "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Mobile Safari/537.36 Edg/87.0.664.57"
        },
        inplace=True,
        session=None,
        webdriver=None
    ) -> None:
        """
        Scrape data from the source

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
        headers : Dict[str, str]
            Dictionary of request headers to be passed on the GET request
        inplace : bool
            Determines if data modified inplace or return a new object with the
            scraped data
        session : requests.Session
            Session for making the GET request
        webdriver : selenium.webdriver.chrome.webdriver.WebDriver
            Webdriver for scraping the page, overrides any default or passed
            session

        Returns
        -------
        return_instance
            Optionally returns a scraped instance instead of modifying inplace
            if inplace arg is True
        """

        if mapping is None:
            mapping = self._Mapping.return_mapping(keys=keys, exclude=exclude)
        if session is None:
            session = self.session
        if webdriver is not None:
            session = webdriver
        if keys is None:
            keys = []
        if exclude is None:
            exclude = []

        if webdriver is None:
            try:
                if "sessionid" not in headers["cookie"]:
                    warnings.warn(
                        "Session ID not in cookies! It's recommended you pass a valid sessionid otherwise Instagram will likely redirect you to their login page.",
                        MissingSessionIDWarning
                    )
            except KeyError:
                warnings.warn(
                    "Request header does not contain cookies! It's recommended you pass at least a valid sessionid otherwise Instagram will likely redirect you to their login page.",
                    MissingCookiesWarning
                    )

        # If the passed source was already an object, construct data from
        # source else parse it
        if isinstance(self.source, type(self)):
            scraped_dict = self.source.to_dict()
        else:
            return_data = self._get_json_from_source(self.source, headers=headers, session=session)
            flat_json_dict = flatten_dict(return_data["json_dict"])
            scraped_dict = parse_data_from_json(
                json_dict=flat_json_dict,
                map_dict=mapping,
            )
        return_data["scrape_timestamp"] = datetime.datetime.now()
        return_data["flat_json_dict"] = flat_json_dict
        return_instance = self._load_into_namespace(
                            scraped_dict=scraped_dict,
                            return_data=return_data,
                            inplace=inplace
        )
        return None if return_instance is self else return_instance

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
    def _url_from_suburl(self, suburl: str) -> str:
        pass

    def _get_json_from_source(self, source: Any, headers: dict, session: requests.Session) -> JSONDict:
        """Parses the JSON data out from the source based on what type the source is"""
        initial_type = True
        return_data = {"source": self.source}
        if isinstance(source, str):
            source_type = self._determine_string_type(source)
        elif isinstance(source, dict):
            json_dict = source
            source_type = "json dict"
        elif isinstance(source, BeautifulSoup):
            source_type = "soup"

        if source_type == "suburl":
            if initial_type:
                suburl = self.source
            url = self._url_from_suburl(suburl=suburl)
            source_type = "url"
            initial_type = False
            return_data["url"] = url

        if source_type == "url":
            if initial_type:
                url = self.source
            html = self._html_from_url(url=url, headers=headers, session=session)
            source_type = "html"
            initial_type = False
            return_data["html"] = html

        if source_type == "html":
            if initial_type:
                html = self.source
            soup = self._soup_from_html(html)
            source_type = "soup"
            initial_type = False
            return_data["soup"] = soup

        if source_type == "soup":
            if initial_type:
                soup = self.source
            json_dict_arr = json_from_soup(soup)
            if len(json_dict_arr) == 1:
                json_dict = json_dict_arr[0]
            else:
                json_dict = json_dict_arr[1]
            self._validate_scrape(json_dict)

        return_data["json_dict"] = json_dict

        return return_data

    def _load_into_namespace(self, scraped_dict: dict, return_data, inplace) -> None:
        """Loop through the scraped dictionary and set them as instance attr"""
        instance = self if inplace else type(self)(return_data["source"])
        for key, val in scraped_dict.items():
            setattr(instance, key, val)
        for key, val in return_data.items():
            setattr(instance, key, val)
        return instance


    @staticmethod
    def _html_from_url(url: str, headers: dict, session: requests.Session) -> str:
        """Return HTML from requested URL"""
        if isinstance(session, requests.Session):
            response = session.get(url, headers=headers)
            page_source = response.text
        else:
            session.get(url)
            page_source = session.page_source
        return page_source

    @staticmethod
    def _soup_from_html(html: str) -> BeautifulSoup:
        """Return BeautifulSoup from source HTML"""
        return BeautifulSoup(html, features="html.parser")

    def _validate_scrape(self, json_dict: str) -> JSONDict:
        """Raise exceptions if the scrape did not properly execute"""
        json_type = determine_json_type(json_dict)
        if json_type == "LoginAndSignupPage" and not type(self).__name__ == "LoginAndSignupPage":
            raise InstagramLoginRedirectError
        elif json_type == "HttpErrorPage" and not type(self).__name__ == "HttpErrorPage":
            source_str = self.url if hasattr(self, "url") else "Source"
            raise ValueError(f"{source_str} is not a valid Instagram page. Please provide a valid argument.")

    @staticmethod
    def _determine_string_type(string_data: str) -> str:
        """Match and return string representation of appropriate source"""
        string_type_map = [("https://", "url"), ("window._sharedData", "html"), ('{"config"', "JSON dict str")]
        for substr, str_type in string_type_map:
            if substr in string_data:
                #BUG: !DOCTYPE isnt returned in selenium source code, use </html> as secondary identifier instead
                if substr == "https://" and "!DOCTYPE" in string_data:
                    continue
                break
        else:
            str_type = "suburl"
        return str_type
