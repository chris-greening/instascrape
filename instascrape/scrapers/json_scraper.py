import json
import csv
from abc import ABC, abstractmethod
import datetime

from typing import List, Any

from ..exceptions import exceptions

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

    _METADATA_KEYS = ["json_dict", "name", 'parse_timestamp']

    def parse_base(self, json_dict, missing: Any = 'ERROR', exception: bool = True):
        config = json_dict["config"]
        self.csrf_token = self.load_value(config, "csrf_token", missing, exception)

        self.country_code = self.load_value(
            json_dict, "country_code", missing, exception)
        self.language_code = self.load_value(
            json_dict, "language_code", missing, exception)
        self.locale = self.load_value(
            json_dict, "locale", missing, exception)

        self.hostname = self.load_value(
            json_dict, "hostname", missing, exception)
        self.is_whitelisted_crawl_bot = self.load_value(
            json_dict, "is_whitelisted_crawl_bot", missing, exception
        )
        self.connection_quality_rating = self.load_value(
            json_dict, "connection_quality_rating", missing, exception
        )
        self.platform = self.load_value(
            json_dict, "platform", missing, exception)

        self.browser_push_pub_key = self.load_value(
            json_dict, "browser_push_pub_key", missing, exception
        )
        self.device_id = self.load_value(
            json_dict, "device_id", missing, exception)
        self.encryption = self.load_value(
            json_dict, "encryption", missing, exception)

        self.rollout_hash = self.load_value(
            json_dict, "rollout_hash", missing, exception)

    def parse_json(self,) -> None:
        """Parse JSON object"""

        #Time the scrape was performed
        self.scrape_timestamp = datetime.datetime.now()


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
        """
        Write scraped data to .json file

        Parameters
        ----------
        fpath : str
            Filepath of the .json to write data to

        """
        with open(fpath, 'w') as outjson:
            json.dump(self.to_dict(), outjson)

    def to_csv(self, fpath: str) -> None:
        """
        Write scraped data to .csv

        Parameters
        ----------
        fpath : str
            Filepath of the .csv to write data to
        """
        with open(fpath, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            for key, value in self.to_dict().items():
                writer.writerow([key, value])

    def load_value(self, data_dict: dict, key: str, missing: Any = None, exception: bool = True) -> Any:
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
            if exception:
                raise exceptions.JSONKeyError(key)
            return_val = missing
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
