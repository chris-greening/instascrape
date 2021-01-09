from __future__ import annotations

import json
from typing import Any, Dict, Union
from collections import deque

import requests

from instascrape.core.json_algos import _JSONTree, _parse_json_str

JSONDict = Dict[str, Any]

def parse_data_from_json(json_dict, map_dict):
    """
    Parse data from a JSON dictionary using a mapping dictionary that tells
    the program how to parse the data
    """
    return_data = {}
    for key in map_dict:
        steps_to_value = map_dict[key]

        # Loop through all steps into the JSON dict that will give us our data
        first_step = steps_to_value.popleft()
        value = json_dict[first_step]
        for step in steps_to_value:
            value = json_dict[step]
        return_data[key] = value
    return return_data

def flatten_dict(json_dict: JSONDict) -> JSONDict:
    """Returns a flattened dictionary of data"""
    json_tree = _JSONTree(json_dict)
    flattened_dict = {}
    for leaf_node in json_tree.leaf_nodes:
        key_arr = deque([])
        for key in leaf_node.prior_keys[::-1]:
            key_arr.appendleft(str(key))
            new_key = "_".join(key_arr)
            if new_key not in flattened_dict:
                break
        flattened_dict[new_key] = list(leaf_node.json_data.values())[0]
    return flattened_dict

def json_from_html(source: Union[str, "BeautifulSoup"], as_dict: bool = True, json_index = 0, flatten=False) -> Union[JSONDict, str]:
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
        json_str = _parse_json_str(source=source)

        # If matches, break otherwise replace and look for next JSON dict
        if i == json_index:
            break
        source = source.replace(json_str, "")
    else:
        raise IndexError(f"{json_index} is not in valid range, pick value between 0 and {amt_json_dicts}")

    json_data = json.loads(json_str) if as_dict else json_str
    if flatten:
        json_data = flatten_dict(json_data)
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




