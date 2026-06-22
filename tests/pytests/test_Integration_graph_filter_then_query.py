"""
Pytest for integration
User story: 1.3, 1.4, 1.5
"""

import os
import sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "src"))
sys.path.insert(0, BASE_DIR)

from graph_project.Graph import Graph
from graph_project.Query import Query
from graph_project.Filter import FilterByType


def test_integration_graph_filter_then_query():
    """
    Integration test: Graph → Filter → Query

    1. Build graph
    2. Apply filter
    3. Run forward query
    4. Validate filter results against query results
    """

    # 1. Build graph
    graph = Graph()
    graph.add_edge("type", "A", "schema:Person")
    graph.add_edge("type", "B", "schema:Person")
    graph.add_edge("type", "C", "schema:Organization")

    query = Query(graph)

    # 2. Apply filter
    person_filter = FilterByType("schema:Person")
    filtered_nodes = person_filter.apply(graph)

    filtered_labels = set()
    for node in filtered_nodes:
        filtered_labels.add(node.label)

    # 3. Run forward query
    paths = query.query_path_forward(["type"])

    query_results = set()
    for path in paths:
        start_label = path[0].label
        end_label = path[-1].label
        query_results.add((start_label, end_label))

    # 4. Validate filter results against query results
    assert "A" in filtered_labels
    assert "B" in filtered_labels
    assert "C" not in filtered_labels

    assert ("A", "schema:Person") in query_results
    assert ("B", "schema:Person") in query_results