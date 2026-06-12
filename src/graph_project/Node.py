# Task: 03 + Task 05

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
        return self._outgoing

    @property
    def incoming(self):
        return self._incoming

    @property
    def attributes(self):
        return self._attributes

    def __repr__(self):
        return f"Node({self.label})"


