"""
Pytest for the Node class.
User story: 4.1, 4.3, 4.6
"""

import os
import sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "src"))
sys.path.insert(0, BASE_DIR)

from graph_project.Node import Node


def test_node_creation_sets_label():
    """
    Basic test: A new Node should store the label it was given.
    """
    n = Node("A")
    assert n.label == "A"


def test_node_creation_initializes_empty_collections():
    """
    A new Node should start with empty outgoing/incoming edge lists and attributes
    """
    n = Node("A")

    assert n.outgoing == tuple()
    assert n.incoming == tuple()
    assert n.attributes == {}


def test_node_label_setter_updates_label():
    """
    The label property should be settable after creation
    """
    n = Node("A")
    n.label = "B"
    assert n.label == "B"


def test_node_repr_format():
    """
    __repr__ should follow the Node(<label>) format
    """
    n = Node("A")
    assert repr(n) == "Node(A)"


def test_node_attributes_dict_is_independent():
    """
    Each Node instance should have its own attributes dict, chechs too see if they can see each others attributes
    """
    n1 = Node("A")
    n2 = Node("B")
    n1.attributes["color"] = "red"
    assert "color" not in n2.attributes
