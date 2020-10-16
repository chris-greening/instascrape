from abc import ABC
from typing import Dict, Union, Any, List
from collections import deque

JSONDict = Dict[str, Any]

class GeneralMapping:
    """General mappings to the JSON data that are present in all JSON data"""
    mapping = {
        'config': deque(['config', 'csrf_token']),
        'viewer': deque(['config', 'viewer']),
        'country_code': deque(['country_code']),
        'language_code': deque(['language_code']),
        'locale': deque(['locale']),
        'device_id': deque(['device_id']),
        'browser_push_pub_key': deque(['browser_push_pub_key']),
        'key_id': deque(['encryption', 'key_id']),
        'public_key': deque(['encryption', 'public_key']),
        'version': deque(['encryption', 'version']),
        'is_dev': deque(['is_dev']),
        'rollout_hash': deque(['rollout_hash']),
        'bundle_variant': deque(['bundle_variant']),
        'frontend_dev': deque(['frontend_env'])
    }

    @classmethod
    def return_mapping(cls, keys=[]):
        if not keys:
            keys = list(cls.mapping)
        return {key: cls.mapping[key] for key in keys}


class ProfileMapping:
    pass
    # mapping.update(GeneralMapping.mapping)

class JsonEngine:
    """
    Generalized version of the JSONScraper classes that will act more as a backend engine that
    the user doesn't have to ever worry about or think of
    """

    DEFAULT_VAL = float('nan')

    def __init__(self, json_data: JSONDict, map_dict: Dict[str, deque]) -> None:
        self.json_data = json_data
        self.map_dict = map_dict

        self._fill_default_values()

    def _fill_default_values(self):
        for key in self.map_dict:
            self._set_value(key, self.json_data, self.map_dict[key])

    def _set_value(self, orig_key: str, container: dict, directive_queue: deque):
        current_key = directive_queue.popleft()
        value = container[current_key]
        print(value)
        if len(directive_queue) == 0:
            setattr(self, orig_key, value)
        else:
            self._set_value(orig_key, value, directive_queue)

    def scrape_data_point(self, key, directive: List[Union[str, int]]):
        pass

if __name__ == '__main__':
    from instascrape import json_from_url

    json_dict = json_from_url('https://www.instagram.com/chris_greening')
    data = JsonEngine(json_dict, GeneralMapping.return_mapping())
