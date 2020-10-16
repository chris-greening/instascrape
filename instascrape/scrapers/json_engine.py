from __future__ import annotations

from collections import deque
from typing import Dict, Union, Any, List

JSONDict = Dict[str, Any]

class _JsonParseEngine:
    """
    Generalized version of the JSONScraper classes that will act more as a backend engine that
    the user doesn't have to ever worry about or think of
    """

    DEFAULT_VAL = float('nan')
    METADATA_KEYS = ['json_data', 'map_dict']

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

    def to_dict(self):
        return {
            key: val
            for key, val in self.__dict__.items()
                if key not in self.METADATA_KEYS
            }

