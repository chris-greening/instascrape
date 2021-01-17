"""
Algorithms and implementations for working with/manipulating JSON data. NOT
intended for top level use but instead imported for top level functions to leverage
"""

from collections import deque
from typing import Any, Dict, List, Union

from bs4 import BeautifulSoup

JSONDict = Dict[str, Any]

class _JSONTree:
    """Tree of linked lists that map out the JSON data"""

    def __init__(self, json_dict: JSONDict) -> None:
        self.json_dict = json_dict
        self.map_tree(self.json_dict)

    def map_tree(self, json_dict) -> None:
        """Map the entire JSON tree and get access to leaf _JSONNodes"""
        self.leaf_nodes = []
        self.root_node = _JSONNode(json_data=json_dict, tree=self)

class _JSONNode:
    """Representation of one step into a JSON Tree"""

    def __init__(self, json_data: Any, tree: _JSONTree, linked_list: deque = None, prior_keys: List[Union[str, int]] = None) -> None:
        self.json_data = json_data
        self.tree = tree

        self.linked_list = linked_list if linked_list is not None else deque([])
        self.prior_keys = prior_keys if prior_keys is not None else []

        self.dtype = type(self.json_data)

        self.nodes = []

        # If the node is a leaf then it has no edges
        if self.is_leaf:
            self.json_data = {prior_keys[-1]: self.json_data}
            self.tree.leaf_nodes.append(self)

        else:
            self.get_edges()

    @property
    def is_leaf(self) -> bool:
        """
        If the dtype of self.json_data is not a dict or a list then it must be
        a leaf node
        """
        return self.dtype is not list and self.dtype is not dict

    def get_edges(self) -> None:
        """Get all edges connected to current _JSONNode"""
        if self.dtype is list:
            iter_arr = zip(range(len(self.json_data)), self.json_data)
        else:
            iter_arr = self.json_data.items()

        for key, value in iter_arr:
            next_linked_list = self.linked_list + deque([self])
            next_key = self.prior_keys + [key]
            node = _JSONNode(value, self.tree, next_linked_list, next_key)
            self.nodes.append(node)

    def __repr__(self) -> str:
        return str(self.json_data)


def _parse_json_str(source: str) -> str:
    """Return the parsed string of JSON data from the BeautifulSoup"""
    json_data = []
    json_scripts = [str(script) for script in source.find_all("script") if "config" in str(script)]
    for script_tag in json_scripts:
        left_index = script_tag.find("{")
        right_index = script_tag.rfind("}") + 1
        json_str = script_tag[left_index:right_index]
        json_data.append(json_str)
    return json_data
