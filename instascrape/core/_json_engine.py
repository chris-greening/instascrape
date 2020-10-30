"""
_JsonEngine handles crunching the data from JSON data based on mapping from
_mappings into a dictionary.
"""

from __future__ import annotations

from collections import deque
from typing import Any, Dict

JSONDict = Dict[str, Any]


class _JsonEngine:
    """
    Engine for crunching JSON dictionary's using a system of mapping directives
    to access the JSON with a key value for the end user
    """

    DEFAULT_VAL = float("nan")

    def __init__(self, json_data: JSONDict, map_dict: Dict[str, deque]) -> None:
        self.json_data = json_data
        self.map_dict = map_dict

    def parse_mapping(self):
        """
        Loop through each key in map_dict and set dictionary value given queue
        of directives that tell the engine how to parse the value from JSONDict
        """
        return_data = {}
        for key in self.map_dict:
            self._set_value(return_data, key, self.json_data, self.map_dict[key])
        return return_data

    def _set_value(self, data_dict, orig_key: str, container: dict, directive_queue: deque):
        """
        Recursively step through a queue of directives until the queue is
        empty. When there are no more directives left in queue, we have arrived
        at our value and orig_key becomes the user facing attribute and value
        becomes the value of that attribute
        """

        current_key = directive_queue.popleft()
        try:
            value = container[current_key]
        except (KeyError, IndexError, TypeError):
            value = self.DEFAULT_VAL

        if len(directive_queue) == 0:
            data_dict[orig_key] = value
        else:
            self._set_value(data_dict, orig_key, value, directive_queue)
