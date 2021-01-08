from __future__ import annotations

import json
from typing import Any, Dict, Union

import requests
from bs4 import BeautifulSoup

from instascrape.core._json_engine import _JsonEngine
from instascrape.core._json_flattener import FlatJSONDict

JSONDict = Dict[str, Any]

def parse_json_from_mapping(json_dict, map_dict):
    _json_engine = _JsonEngine(json_dict, map_dict)
    return_data = _json_engine.parse_mapping()
    return return_data

def flatten_json(json_dict: JSONDict) -> JSONDict:
    """Returns a flattened dictionary of JSON data"""
    return FlatJSONDict(json_dict).flat_json

def json_from_html(source: Union[str, BeautifulSoup], as_dict: bool = True, json_index = 0, flatten=False) -> Union[JSONDict, str]:
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

    amt_json_dicts = source.count("window._shared")
    for i in range(0, amt_json_dicts):
        json_str = _get_json_str(source=source)

        # If matches, break otherwise replace and look for next JSON dict
        if i == json_index:
            break
        source = source.replace(json_str, "")
    else:
        raise IndexError(f"{json_index} is not in valid range, pick value between 0 and {amt_json_dicts}")

    json_data = json.loads(json_str) if as_dict else json_str
    if flatten:
        json_data = flatten_json(json_data)
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

def json_from_url(
    url: str,
    as_dict: bool = True,
    headers={
        "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Mobile Safari/537.36 Edg/87.0.664.57"
    },
    json_index=0,
    flatten=False
) -> Union[JSONDict, str]:
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
    source = requests.get(url, headers=headers).text
    return json_from_html(source, as_dict=as_dict, json_index=json_index, flatten=flatten)

def _get_json_str(source: str) -> str:
    """Return the parsed string of JSON data from the HTML"""
    if not isinstance(source, BeautifulSoup):
        soup = BeautifulSoup(source, features="html.parser")
    json_script = [str(script) for script in soup.find_all("script") if "config" in str(script)][0]
    left_index = json_script.find("{")
    right_index = json_script.rfind("}") + 1
    json_str = json_script[left_index:right_index]
    return json_str
