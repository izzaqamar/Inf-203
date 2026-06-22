# Task: 03 + Task 05

from copy import deepcopy


class Node:
    """Represents a node (vertex) in a directed graph.

    Parameters
    label : A unique identifier for the node.

    Attributes
    label : The unique ID of the node.
    outgoing : list of Edges for which this node is the source.
    incoming : list of Edges for which this node is the target.
    attributes : Optional dictionary for storing literal values or metadata.
    """

    def __init__(self, label):
        self._label = label
        self._outgoing = []
        self._incoming = []
        self._attributes = {}

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, value):
        self._label = value

    @property
    def outgoing(self):
        return deepcopy(self._outgoing)

    @property
    def incoming(self):
        return deepcopy(self._incoming)

    @property
    def attributes(self):
        return deepcopy(self._attributes)

    def add_outgoing_edge(self, edge):
        self._outgoing.append(edge)

    def add_incoming_edge(self, edge):
        self._incoming.append(edge)

    def add_attribute(self, key, value):
        self._attributes[key] = value

    def __repr__(self):
        return f"Node({self.label})"
