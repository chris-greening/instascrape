"""
Algorithm for flattening a JSON dictionary of variable depths into a
flat dictionary that contains the deepest key: value pairs
"""

from collections import deque
from collections.abc import MutableMapping
from typing import Any, Dict, List, Union

JSONDict = Dict[str, Any]


class FlatJSONDict(MutableMapping):
    """Takes a dictionary with JSON-like data and creates an instance that
    behaves exactly like a dict but with the flattened data"""

    def __init__(self, json_dict):

        self.json_dict = json_dict

        self.json_tree = JsonTree(self.json_dict)

        self.flat_json = self._flatten_json()

        self.__dict__.update(self.flat_json)

    def _flatten_json(self):
        """
        Primary algorithm that creates the flattened dictionary from a mapped
        tree of JSON data
        """
        flattened_dict = {}
        for leaf_node in self.json_tree.leaf_nodes:
            key_arr = deque([])
            for key in leaf_node.prior_keys[::-1]:
                new_key = self._new_key(key, key_arr)
                if new_key not in flattened_dict:
                    break
            flattened_dict[new_key] = list(leaf_node.json_data.values())[0]
        return flattened_dict

    @staticmethod
    def _new_key(key: str, key_arr: deque) -> str:
        key_arr.appendleft(str(key))
        return "_".join(key_arr)

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def __getitem__(self, key):
        return self.__dict__[key]

    def __delitem__(self, key):
        del self.__dict__[key]

    def __iter__(self):
        return iter(self.__dict__)

    def __len__(self):
        return len(self.__dict__)

    # The final two methods aren't required, but nice for demo purposes:

    def __str__(self):
        """returns simple dict representation of the mapping"""
        return str(self.__dict__)

    def __repr__(self):
        """echoes class, id, & reproducible representation in the REPL"""
        return "{}, D({})".format(super(FlatJSONDict, self).__repr__(), self.__dict__)


class JsonTree:
    """Tree of linked lists that map out the JSON data"""

    def __init__(self, json_dict: JSONDict):
        self.json_dict = json_dict
        self.map_tree(self.json_dict)

    def map_tree(self, json_dict):
        """Map the entire JSON tree and get access to leaf nodes"""
        self.leaf_nodes = []
        self.root_node = Node(json_data=json_dict, tree=self)


class Node:
    """
    Representation of one step into a JSON Tree
    """

    def __init__(
        self, json_data: Any, tree: JsonTree, linked_list: deque = None, prior_keys: List[Union[str, int]] = None
    ) -> None:
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
    def is_leaf(self):
        """
        If the dtype of self.json_data is not a dict or a list then it must be
        a leaf node
        """
        return self.dtype is not list and self.dtype is not dict

    def get_edges(self):
        """
        Get all edges connected to current Node
        """
        if self.dtype is list:
            iter_arr = zip(range(len(self.json_data)), self.json_data)
        else:
            iter_arr = self.json_data.items()

        for key, value in iter_arr:
            next_linked_list = self.linked_list + deque([self])
            next_key = self.prior_keys + [key]
            node = Node(value, self.tree, next_linked_list, next_key)
            self.nodes.append(node)

    def __repr__(self):
        return str(self.json_data)
