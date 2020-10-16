from __future__ import annotations

from collections import deque
from typing import Dict, Union, Any, List

JSONDict = Dict[str, Any]

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
        """Loop through each key in map_dict and set value given a list of directives"""
        for key in self.map_dict:
            self._set_value(key, self.json_data, self.map_dict[key])

    def _set_value(self, orig_key: str, container: dict, directive_queue: deque):
        """Recursively set each value from the mapping"""
        current_key = directive_queue.popleft()
        value = container[current_key]
        if len(directive_queue) == 0:
            setattr(self, orig_key, value)
        else:
            self._set_value(orig_key, value, directive_queue)

if __name__ == '__main__':
    from instascrape.tools.parsers import json_from_url
    from instascrape.scrapers.mappings import ProfileMapping

    json_dict = json_from_url('https://www.instagram.com/p/CGX0G64hu4Q/')
    data = JsonEngine(json_dict, ProfileMapping.return_mapping())
