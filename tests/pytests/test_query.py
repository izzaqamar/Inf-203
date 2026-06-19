"""
Pytest tests for the Query class.
"""

import os
import sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "src"))
sys.path.insert(0, BASE_DIR)

from graph_project.Graph import Graph
from graph_project.query import Query


def test_query_creation_stores_graph():
    """
    Query should store reference to graph.
    """
    g = Graph()
    q = Query(g)

    assert q.graph is g


def test_query_forward_simple_path():
    """
    Forward path traversal.

    Graph:
        A -connects-> B -connects-> C

    Query:
        connects -> connects

    Expected:
        A -> B -> C
    """
    g = Graph()

    g.add_edge("connects", "A", "B")
    g.add_edge("connects", "B", "C")

    q = Query(g)

    paths = q.query_path_forward(["connects", "connects"])

    assert len(paths) == 1

    labels = [n.label for n in paths[0]]

    assert labels == ["A", "B", "C"]


def test_query_forward_no_match():
    """
    Should return empty list when no path exists.
    """
    g = Graph()

    g.add_edge("connects", "A", "B")

    q = Query(g)

    paths = q.query_path_forward(["submits"])

    assert paths == []


def test_query_backward_single_step():
    """
    Backward traversal.

    Graph:
        A -connects-> B

    Query:
        connects (backward)

    Expected:
        B -> A
    """
    g = Graph()

    g.add_edge("connects", "A", "B")

    q = Query(g)

    paths = q.query_path(["connects"], [False])

    assert len(paths) == 1

    labels = [n.label for n in paths[0]]

    assert labels == ["B", "A"]


def test_query_mixed_direction_path():
    """
    Mixed traversal.

    Graph:
        A -connects-> B
        B -links-> C
        C -relates-> D

    Query:
        connects (backward)
        links (forward)
        relates (forward)

    Expected:
        No valid path, because A has no outgoing 'links' edge.
    """
    g = Graph()

    g.add_edge("connects", "A", "B")
    g.add_edge("links", "B", "C")
    g.add_edge("relates", "C", "D")

    q = Query(g)

    paths = q.query_path(["connects", "links", "relates"], [False, True, True])

    assert paths == []


def test_query_multiple_results():
    """
    Multiple valid paths.

    Graph:
        A -connects-> B
        C -connects-> D

    Query:
        connects

    Expected:
        two paths
    """
    g = Graph()

    g.add_edge("connects", "A", "B")
    g.add_edge("connects", "C", "D")

    q = Query(g)

    paths = q.query_path_forward(["connects"])

    assert len(paths) == 2

    results = {(p[0].label, p[-1].label) for p in paths}

    assert ("A", "B") in results
    assert ("C", "D") in results
