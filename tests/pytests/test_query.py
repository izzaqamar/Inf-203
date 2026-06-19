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


def test_shortest_path_returns_path_between_connected_nodes():
    """
    shortest_path() should return the shortest path between two connected nodes
    """
    graph = Graph()

    graph.add_edge("connects", "A", "B")
    graph.add_edge("connects", "B", "C")

    q = Query(graph)

    path = q.shortest_path(graph.nodes["A"], graph.nodes["C"])
    labels = [n.label for n in path]

    assert labels == ["A", "B", "C"]


def test_shortest_path_returns_single_node_when_start_equals_end():
    """
    shortest_path() should return a list containing only the start node when start and end are identical
    """
    graph = Graph()
    graph.add_node("A")

    q = Query(graph)

    path = q.shortest_path(graph.nodes["A"], graph.nodes["A"])
    labels = [n.label for n in path]

    assert labels == ["A"]


def test_shortest_path_returns_empty_list_when_no_path_exists():
    """
    shortest_path() should return an empty list when no path exists between the nodes
    """
    graph = Graph()

    graph.add_edge("connects", "A", "B")
    graph.add_node("C")

    q = Query(graph)

    path = q.shortest_path(graph.nodes["A"], graph.nodes["C"])

    assert path == []


def test_shortest_path_returns_one_of_the_shortest_routes():
    """
    shortest_path() should return a shortest path when multiple valid routes exist
    """
    graph = Graph()

    graph.add_edge("connects", "A", "B")
    graph.add_edge("connects", "A", "C")
    graph.add_edge("connects", "B", "D")
    graph.add_edge("connects", "C", "D")

    q = Query(graph)

    path = q.shortest_path(graph.nodes["A"], graph.nodes["D"])
    labels = [n.label for n in path]

    assert labels[0] == "A"
    assert labels[-1] == "D"
    assert len(labels) == 3