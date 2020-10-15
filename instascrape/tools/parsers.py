from __future__ import annotations

from typing import Union, Dict, Any
import json 
from bs4 import BeautifulSoup

JSONDict = Dict[str, Any]

def json_from_source(source: Union[str, BeautifulSoup], as_dict: bool = True) -> Union[JSONDict, str]:
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
        or just the string
    """
    if type(source) is not BeautifulSoup:
        source = BeautifulSoup(source, features='lxml')

    json_script = [
        str(script) for script in source.find_all("script") if "config" in str(script)
    ][0]
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

    Returns
    -------

    """

if __name__ == '__main__':
    import requests
    source = requests.get('https://www.instagram.com/chris_greening').text
    data = json_from_source(source)
