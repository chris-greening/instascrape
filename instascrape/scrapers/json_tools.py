from __future__ import annotations

import json
from typing import Any, Dict, Union

import requests
from bs4 import BeautifulSoup

from instascrape.core._json_engine import _JsonEngine

JSONDict = Dict[str, Any]


def parse_json_from_mapping(json_dict, map_dict):
    _json_engine = _JsonEngine(json_dict, map_dict)
    return_data = _json_engine.parse_mapping()
    return return_data


def json_from_html(source: Union[str, BeautifulSoup], as_dict: bool = True) -> Union[JSONDict, str]:
    """
    Return JSON data parsed from Instagram source HTML

    Parameters
    ----------
    source : Union[str, BeautifulSoup]
        Instagram HTML source code to parse the JSON from
    as_dict : bool = True
        Return JSON as dict if True else return JSON as string

    Returns
    -------
    json_data : Union[JSONDict, str]
        Parsed JSON data from the HTML source as either a JSON-like dictionary
        or just the string serialization
    """
    if type(source) is not BeautifulSoup:
        source = BeautifulSoup(source, features="lxml")

    json_script = [str(script) for script in source.find_all("script") if "config" in str(script)][0]
    left_index = json_script.find("{")
    right_index = json_script.rfind("}") + 1
    json_str = json_script[left_index:right_index]

    json_data = json.loads(json_str) if as_dict else json_str
    return json_data


def determine_json_type(json_data: Union[JSONDict, str]) -> str:
    """
    Return the type of Instagram page based on the JSON data parsed from source

    Parameters
    ----------
    json_data: Union[JSONDict, str]
        JSON data that will be checked and parsed to determine what type of page
        the program is looking at (Profile, Post, Hashtag, etc)

    Returns
    -------
    instagram_type : str
        Name of the type of page the program is currently parsing or looking at
    """
    if not isinstance(json_data, dict):
        json_data = json.loads(json_data)
    instagram_type = list(json_data["entry_data"])[0]
    return instagram_type


def json_from_url(url: str, as_dict: bool = True) -> Union[JSONDict, str]:
    """
    Return JSON data parsed from a provided Instagram URL

    Parameters
    ----------
    url : str
        URL of the page to get the JSON data from
    as_dict : bool = True
        Return JSON as dict if True else return JSON as string

    Returns
    -------
    json_data : Union[JSONDict, str]
        Parsed JSON data from the URL as either a JSON-like dictionary
        or just the string serialization
    """
    source = requests.get(url).text
    json_data = json_from_html(source=source, as_dict=as_dict)
    return json_data
