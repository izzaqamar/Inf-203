"""
Pytest for the Edge class
Recycles lots of the node tests
User story: 4.2, 4.6

"""

import os
import sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "src"))
sys.path.insert(0, BASE_DIR)

from graph_project.Node import Node
from graph_project.Edge import Edge


def test_edge_creation_sets_label():
    """
    A new Edge should store the label it was given
    """
    source = Node("A")
    target = Node("B")
    # Edge: def __init__(self, label, source, target):
    e = Edge("connects", source, target)
    assert e.label == "connects"


def test_edge_creation_sets_source_and_target():
    """
    A new Edge should store THE exact Node objects passed in for source/target
    """
    source = Node("A")
    target = Node("B")
    e = Edge("connects", source, target)
    # asserts actual that they are the same object, not same value
    assert e.source is source
    assert e.target is target


def test_edge_label_setter_updates_label():
    """
    The label property should be settable after creation
    """
    source = Node("A")
    target = Node("B")
    e = Edge("connects", source, target)
    e.label = "relates_to"
    assert e.label == "relates_to"


def test_edge_source_setter_updates_source():
    """
    The source property should be settable after creation
    """
    source = Node("A")
    target = Node("B")
    new_source = Node("C")
    e = Edge("connects", source, target)
    e.source = new_source
    assert e.source is new_source


def test_edge_target_setter_updates_target():
    """
    The target property should be settable after creation
    """
    source = Node("A")
    target = Node("B")
    new_target = Node("D")
    e = Edge("connects", source, target)
    e.target = new_target
    assert e.target is new_target


def test_edge_repr_format():
    """
    __repr__ should follow the Edge(<label>, <source.label> -> <target.label>) format
    """
    source = Node("A")
    target = Node("B")
    e = Edge("connects", source, target)
    assert repr(e) == "Edge(connects, A -> B)"


def test_edge_rename_source_updates_edge():
    """
    Creates edge, renames source node, checks if edge repr() shows new name
    """
    source = Node("A")
    target = Node("B")
    e = Edge("connects", source, target)
    source.label = "Z"
    assert repr(e) == "Edge(connects, Z -> B)"
