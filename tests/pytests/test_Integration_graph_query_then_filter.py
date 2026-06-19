import os
import sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "src"))
sys.path.insert(0, BASE_DIR)

from graph_project.Graph import Graph
from graph_project.query import Query
from graph_project.Filter import FilterByType


def test_integration_graph_query_then_external_filter():
    """
    Integration test: Graph → Query → Filter validation

    1. Build graph with multiple node types
    2. Run forward query over graph
    3. Apply filter independently from query system
    4. Validate filtered nodes match expectations
    """

    # 1. Build graph with multiple node types
    graph = Graph()
    graph.add_edge("type", "A", "schema:Person")
    graph.add_edge("type", "B", "schema:Person")
    graph.add_edge("type", "C", "schema:Organization")

    # 2. Run forward query over graph
    query = Query(graph)
    paths = query.query_path_forward(["type"])

    # 3. Apply filter independently from query system
    person_filter = FilterByType("schema:Person")
    filtered_nodes = person_filter.apply(graph)

    filtered_labels = set()
    for node in filtered_nodes:
        filtered_labels.add(node.label)

    # 4. Validate filtered nodes match expectations
    query_results = set()
    for path in paths:
        start_label = path[0].label
        end_label = path[-1].label
        query_results.add((start_label, end_label))

    assert "A" in filtered_labels
    assert "B" in filtered_labels
    assert "C" not in filtered_labels

    assert ("A", "schema:Person") in query_results
    assert ("B", "schema:Person") in query_results