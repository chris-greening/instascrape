from typing import List, Dict, Any
from copy import deepcopy

JSONDict = Dict[str, Any]

class JsonTree:
    """Flatten a nested dictionary of JSON-data as much as possible"""
    def __init__(self, json_dict):
        self.json_dict = json_dict 
        self.map_tree(self.json_dict)

    def map_tree(self, json_dict):
        self.root_node = Node(json_data=json_dict)

class Node:
    leaf_nodes = []
    def __init__(self, json_data: JSONDict, linked_list: List['Node'] = [], prior_key: str = ''):
        self.json_data = json_data
        self.linked_list = linked_list

        self.dtype = type(self.json_data)
        self.next_linked_list = self.linked_list + [self]
        self.edges = []

        if self.is_leaf:
            self.json_data = {prior_key: self.json_data}
            Node.append_leaf_node(self)
        else:
            self.get_edges()

    @property
    def is_leaf(self):
        """
        If the type of self.json_data is not a list or dict, then this Node
        must be a leaf
        """
        return self.dtype is not list and self.dtype is not dict

    def get_edges(self):
        if type(self.json_data) is list:
            for i, next_step in enumerate(self.json_data):
                node = Node(next_step, self.next_linked_list, i)
                self.edges.append(node)
        else:
            for key, next_step in self.json_data.items():
                node = Node(next_step, self.next_linked_list, key)
                self.edges.append(node)

    @classmethod
    def append_leaf_node(cls, node):
        cls.leaf_nodes.append(node)
