import json
from abc import ABC, abstractmethod
import datetime

from typing import List, Any

class JSONScraper(ABC):
    """
    Abstract base class containing methods for handling and parsing Instagram
    JSON data

    Attributes
    ----------
    json_dict : dict
        Python dictionary containing the Instagram JSON data
    name : str, optional
        Custom name that will represent this JSON data

    Methods
    -------
    parse_json() -> None
        Parses JSON data that every Instagram type has
    load_value(data_dict: dict, key: str, fail_return: Any=None)
        Returns value in dictionary at the specified key. If value doesn't
        exist, returns a default value
    from_json_string(json_str: str, name: str = None)
        Loads a json string as a dictionary and returns a JSONData object with
        that dictionary.
    from_json_file(json_fpath: str, name: str = None)
        Loads a json file at a given JSON filepath into a dictionary and
        returns a JSONData object with that dictionary
    """

    _METADATA_KEYS = ["json_dict", "name"]

    def __init__(self, json_dict: dict, name: str = None) -> None:
        """Container for storing all scraped data from Instagram JSON"""
        self.json_dict = json_dict
        if name is not None:
            self.name = name

    def parse_json(self) -> None:
        """Parse JSON object"""
        config = self.json_dict["config"]
        self.csrf_token = self.load_value(config, "csrf_token")

        self.country_code = self.load_value(self.json_dict, "country_code")
        self.language_code = self.load_value(self.json_dict, "language_code")
        self.locale = self.load_value(self.json_dict, "locale")

        self.hostname = self.load_value(self.json_dict, "hostname")
        self.is_whitelisted_crawl_bot = self.load_value(
            self.json_dict, "is_whitelisted_crawl_bot"
        )
        self.connection_quality_rating = self.load_value(
            self.json_dict, "connection_quality_rating"
        )
        self.platform = self.load_value(self.json_dict, "platform")

        self.browser_push_pub_key = self.load_value(
            self.json_dict, "browser_push_pub_key"
        )
        self.device_id = self.load_value(self.json_dict, "device_id")
        self.encryption = self.load_value(self.json_dict, "encryption")

        self.rollout_hash = self.load_value(self.json_dict, "rollout_hash")

    @property
    def scraped_attr(self) -> List[str]:
        """Return list of names of attributes that have been scraped from the JSON"""
        return [
            attr for attr in self.__dict__ if attr not in JSONScraper._METADATA_KEYS
        ]

    def to_dict(self) -> dict:
        """Return a dictionary containing all of the data that has been scraped"""
        return {
            key: val
            for key, val in self.__dict__.items()
            if key not in JSONScraper._METADATA_KEYS
        }

    def to_json(self, fpath: str) -> None:
        """Write data to .json file"""
        with open(fpath, 'w') as outjson:
            json.dump(self.to_dict(), outjson)

    def load_value(self, data_dict: dict, key: str, fail_default: Any = None) -> Any:
        """
        Returns the value of a dictionary at a given key, returning a specified
        value if the key does not exsit.

        Parameters
        ----------
        data_dict : dict
            Dictionary of key: val pairs that you want to look for
        key : str
            Key in dictionary to search for
        fail_return : Any, optional

        Returns
        -------
        return_val : Any
            Value or default return of the dictionary lookup
        """
        try:
            return_val = data_dict[key]
        except KeyError:
            return_val = fail_default
        return return_val

    @classmethod
    def from_json_string(cls, json_string: str, name: str = None):
        """
        Factory method for returning a JSONData object given a string
        representation of JSON data.

        Parameters
        ----------
        json_string : str
            String representation of the JSON data for loading into dict
        name : str, optional
            Optional name of the JSON data

        Returns
        -------
        JSONData : JSONData
            JSONData  object containing the JSON data loaded from string as a dictionary

        """
        return cls(json.loads(json_string), name)

    @classmethod
    def from_json_file(cls, json_fpath: str, name: str = None):
        """
        Factory method for returning a JSONData object given a filepath
        to a .json file that contains valid JSON data.

        Parameters
        ----------
        json_fpath : str
            Filepath to the .json file
        name : str, optional
            Optional name of the JSON data

        Returns
        -------
        JSONData : JSONData
            JSONData object containing the JSON data loaded from file as a dictionary

        """
        with open(json_fpath, "r") as infile:
            json_data = json.load(infile)
        return cls(json_data, name)

    def __repr__(self) -> str:
        class_name = type(self).__name__
        output_str = "<{}: " + f"{class_name}>"
        if hasattr(self, "name"):
            return output_str.format(self.name)
        return output_str.format("unnamed")
