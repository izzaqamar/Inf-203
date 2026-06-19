"""
Pytest for the Filter classes
"""

import os
import sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "src"))
sys.path.insert(0, BASE_DIR)

from graph_project.Graph import Graph
from graph_project.Filter import FilterByType, FilterByName, FilterOrphans

# FilterByType


def test_filterbytype_call_returns_true_for_matching_node():
    """
    Calling the filter directly on a single node should return True if that node has a type edge pointing to the matching type label
    """
    graph = Graph()
    graph.add_edge("type", "Argiris", "schema:Person")

    node = graph.nodes["Argiris"]
    f = FilterByType("schema:Person")

    assert f(node) is True


def test_filterbytype_call_returns_false_for_non_matching_node():
    """
    Calling the filter on a node with a different type should return False
    """
    graph = Graph()
    graph.add_edge("type", "Argiris", "schema:Person")

    node = graph.nodes["Argiris"]
    f = FilterByType("schema:Organization")

    assert f(node) is False


def test_filterbytype_apply_returns_only_matching_nodes():
    """
    apply() should return every node in the graph that matches the type (not others)
    """
    graph = Graph()
    graph.add_edge("type", "Argiris", "schema:Person")
    graph.add_edge("type", "Stratos", "schema:Person")
    graph.add_edge("type", "NMBU", "schema:Organization")

    f = FilterByType("schema:Person")
    results = f.apply(graph)
    result_labels = [n.label for n in results]

    assert "Argiris" in result_labels
    assert "Stratos" in result_labels
    assert "NMBU" not in result_labels
    assert len(results) == 2


# FilterByName


def test_filterbyname_call_returns_true_for_substring_match():
    """
    Calling the filter directly should return True if the search string appears anywhere inside the node's label
    """
    graph = Graph()
    node = graph.add_node("example-abox:Argiris_Laskarakis")
    f = FilterByName("Argiris")

    assert f(node) is True


def test_filterbyname_call_returns_false_when_not_found():
    """
    Calling the filter on a node whose label does not contain the search string should return False
    """
    graph = Graph()
    node = graph.add_node("example-abox:Stratos_Saliakas")
    f = FilterByName("Argiris")

    assert f(node) is False


def test_filterbyname_apply_returns_only_matching_nodes():
    """
    apply() should return every node whose label contains the search string
    """
    graph = Graph()
    graph.add_node("example-abox:Argiris_Laskarakis")
    graph.add_node("example-abox:Argiris_Other")
    graph.add_node("example-abox:Stratos_Saliakas")

    f = FilterByName("Argiris")
    results = f.apply(graph)
    result_labels = [n.label for n in results]

    assert "example-abox:Argiris_Laskarakis" in result_labels
    assert "example-abox:Argiris_Other" in result_labels
    assert "example-abox:Stratos_Saliakas" not in result_labels
    assert len(results) == 2


# FilterOrphans


def test_filterorphans_call_returns_true_for_node_with_no_edges():
    """
    A node with no incoming or outgoing edges should be considered an orphan
    """
    graph = Graph()
    node = graph.add_node("LonelyNode")
    f = FilterOrphans()

    assert f(node) is True


def test_filterorphans_call_returns_false_for_connected_node():
    """
    A node that has at least one edge should NOT be considered an orphan
    """
    graph = Graph()
    graph.add_edge("connects", "A", "B")

    node = graph.nodes["A"]
    f = FilterOrphans()

    assert f(node) is False


def test_filterorphans_apply_returns_only_orphan_nodes():
    """
    apply() should return only the nodes with zero edges and skip any node that is connected to something
    """
    graph = Graph()
    graph.add_edge("connects", "A", "B")
    graph.add_node("LonelyNode")

    f = FilterOrphans()
    results = f.apply(graph)
    result_labels = [n.label for n in results]

    assert "LonelyNode" in result_labels
    assert "A" not in result_labels
    assert "B" not in result_labels
    assert len(results) == 1
