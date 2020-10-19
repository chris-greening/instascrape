from collections import deque
from typing import List, Dict, Any
from copy import deepcopy

JSONDict = Dict[str, Any]

class JsonTree:
    """Build a tree of linked lists that map out the JSON data"""
    def __init__(self, json_dict):
        self.json_dict = json_dict 
        self.map_tree(self.json_dict)

    def map_tree(self, json_dict):
        self.leaf_nodes = []
        self.root_node = Node(json_data=json_dict, tree=self)

class Node:
    def __init__(self, json_data, tree, linked_list=deque([]), prior_keys=[]):
        self.json_data = json_data
        self.tree = tree
        self.linked_list = linked_list
        self.prior_keys = prior_keys

        self.dtype = type(self.json_data)

        self.nodes = []

        if self.is_leaf:
            self.json_data = {prior_keys[-1]: self.json_data}
            self.tree.leaf_nodes.append(self)

        else:
            self.get_edges()

    @property
    def is_leaf(self):
        return self.dtype is not list and self.dtype is not dict

    def get_edges(self):
        #If dict, only iterate over the values
        iter_arr = zip(range(len(self.json_data)), self.json_data) if self.dtype is list else self.json_data.items()

        for key, value in iter_arr:
            next_linked_list = self.linked_list + deque([self])
            next_key = self.prior_keys + [key]
            node = Node(value, self.tree, next_linked_list, next_key)
            self.nodes.append(node)

    def __repr__(self):
        return str(self.json_data)
