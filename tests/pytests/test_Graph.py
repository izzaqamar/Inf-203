"""
Pytest for the Graph class
Recycles lots of the node/edge tests
"""

import os
import sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "src"))
sys.path.insert(0, BASE_DIR)

from graph_project.Graph import Graph


def test_graph_start_empty():
    """
    A new Graph should start with no nodes and no edges
    """
    g = Graph()
    assert g.nodes == {}
    assert g.edges == []


def test_graph_add_node_creates_node():
    """
    add_node should create a Node with the given label and store it in graph.nodes
    """
    g = Graph()
    n = g.add_node("A")
    assert n.label == "A"
    assert g.nodes["A"] is n


def test_graph_add_node_no_duplicates():
    """
    Calling add_node twice with the same label should return the same Node,
    not create a second one
    """
    g = Graph()
    n1 = g.add_node("A")
    n2 = g.add_node("A")
    assert n1 is n2
    assert len(g.nodes) == 1


def test_graph_add_edge_creates_edge():
    """
    add_edge should return an Edge with the correct label, source, and target
    """
    g = Graph()
    e = g.add_edge("connects", "A", "B")
    assert e.label == "connects"
    assert e.source.label == "A"
    assert e.target.label == "B"


def test_graph_add_edge_creates_missing_nodes():
    """
    add_edge should automatically create (source / target) nodes if they don't exist yet
    """
    g = Graph()
    g.add_edge("connects", "A", "B")
    assert "A" in g.nodes
    assert "B" in g.nodes


def test_graph_add_edge_updates_node_outgoing_incoming():
    """
    After add_edge, the edge should appear in source.outgoing and target.incoming
    """
    g = Graph()
    e = g.add_edge("connects", "A", "B")
    source = g.nodes["A"]
    target = g.nodes["B"]
    assert e in source.outgoing
    assert e in target.incoming


def test_graph_add_edge_appends_to_graph_edges_list():
    """
    add_edge should add the new edge to graph.edges
    """
    g = Graph()
    e = g.add_edge("connects", "A", "B")
    assert e in g.edges
    assert len(g.edges) == 1
