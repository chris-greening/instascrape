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
    source : str 
        Instagram HTML source code to parse the JSON from 
    as_dict : bool = True 
        Return JSON as dict if True else return JSON as string
    
    Returns
    -------
    json_data : Union[JSONDict, str]
        Parsed JSON data from the HTML source as either a JSON-like dictionary
        or just the string
    """
    pass

def determine_json_type(json_data: Union[JSONDict, str]) -> str:
    pass