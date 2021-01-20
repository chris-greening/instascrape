from __future__ import annotations

import json
from typing import Any, Dict, Union, Callable, List
from collections import deque
import datetime
from functools import partial
import copy
import time

import requests
from bs4 import BeautifulSoup

from instascrape.core.json_algos import _JSONTree, _parse_json_str

JSONDict = Dict[str, Any]

def parse_data_from_json(json_dict, map_dict, default_value=float('nan')):
    """
    Parse data from a JSON dictionary using a mapping dictionary that tells
    the program how to parse the data
    """
    return_data = {}
    for key in map_dict:
        steps_to_value = map_dict[key]

        # Loop through all steps into the JSON dict that will give us our data
        first_step = steps_to_value.popleft()
        try:
            value = json_dict[first_step]
        except KeyError:
            value = default_value
        else:
            for step in steps_to_value:
                value = json_dict[step]
        finally:
            return_data[key] = value
    return return_data

def flatten_dict(json_dict: JSONDict) -> JSONDict:
    """
    Returns a flattened dictionary of data

    Parameters
    ----------
    json_dict : dict
        Input dictionary for flattening

    Returns
    -------
    flattened_dict : dict
        Flattened dictionary
    """
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

def json_from_html(source: Union[str, "BeautifulSoup"], as_dict: bool = True, flatten=False) -> Union[JSONDict, str]:
    """
    Return JSON data parsed from Instagram source HTML

    Parameters
    ----------
    source : Union[str, BeautifulSoup]
        Instagram HTML source code to parse the JSON from
    as_dict : bool = True
        Return JSON as dict if True else return JSON as string
    flatten : bool
        Flatten the dictionary prior to returning it

    Returns
    -------
    json_data : Union[JSONDict, str]
        Parsed JSON data from the HTML source as either a JSON-like dictionary
        or just the string serialization
    """

    soup = BeautifulSoup(source, features="html.parser")
    json_data = json_from_soup(source=soup, as_dict=as_dict, flatten=flatten)
    return json_data

def json_from_soup(source, as_dict: bool = True, flatten=False):
    json_data = _parse_json_str(source=source)

    if as_dict:
        json_data = [json.loads(json_str) for json_str in json_data]
    if flatten:
        json_data = [flatten_dict(json_dict) for json_dict in json_data]

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
    try:
        instagram_type = list(json_data["entry_data"])[0]
    except KeyError:
        instagram_type = "Inconclusive"
    return instagram_type

def json_from_url(
    url: str,
    as_dict: bool = True,
    headers={
        "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Mobile Safari/537.36 Edg/87.0.664.57"
    },
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
    headers : Dict[str, str]
            Dictionary of request headers to be passed on the GET request
    flatten : bool
        Flatten the dictionary prior to returning it

    Returns
    -------
    json_data : Union[JSONDict, str]
        Parsed JSON data from the URL as either a JSON-like dictionary
        or just the string serialization
    """
    source = requests.get(url, headers=headers).text
    return json_from_html(source, as_dict=as_dict, flatten=flatten)


def scrape_posts(
        posts: List["Post"],
        session: requests.Session = None,
        webdriver: "selenium.webdriver.chrome.webdriver.WebDriver" = None,
        limit: Union[int, datetime.datetime] = None,
        headers: dict = {
            "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Mobile Safari/537.36 Edg/87.0.664.57"
        },
        pause: int = 5,
        on_exception: str = "raise",
        silent: bool = True,
        inplace: bool = False
    ):

    # Default setup
    if not inplace:
        posts = copy.deepcopy(posts)
    if limit is None:
        limit = len(posts)

    scraped_posts = []
    for i, post in enumerate(posts):
        temporary_post = copy.deepcopy(post)
        try:
            post.scrape(session=session, webdriver=webdriver, headers=headers)
            scraped_posts.append(post)
        except Exception as e:
            if on_exception == "raise":
                raise
            elif on_exception == "pass":
                if not silent:
                    print(f"PASSING EXCEPTION: {e}")
                pass
            elif on_exception == "return":
                if not silent:
                    print(f"{e}, RETURNING SCRAPED AND UNSCRAPED")
                break
        if not silent:
            output_str = f"{i}: {post.shortcode} - {post.upload_date}"
            print(output_str)
        if _stop_scraping(limit, post, i):
            break
        time.sleep(pause)

    unscraped_posts = list(set(posts) - set(scraped_posts))
    if not isinstance(limit, int):
        scraped_posts.pop()
        unscraped_posts.insert(0, temporary_post)

    return scraped_posts, unscraped_posts if not inplace else None

def _stop_scraping(limit, post, i):
    stop = False
    if isinstance(limit, int):
        if i == limit - 1:
            stop = True
    elif (isinstance(limit, datetime.datetime) or isinstance(limit, datetime.date)):
        if post.upload_date <= limit:
            stop = True
    return stop
