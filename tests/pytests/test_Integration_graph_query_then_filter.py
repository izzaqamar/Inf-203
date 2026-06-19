import os
import sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "src"))
sys.path.insert(0, BASE_DIR)

from graph_project.Graph import Graph
from graph_project.query import Query
from graph_project.Filter import FilterByType


def test_integration_graph_query_then_external_filter():
    """
    Integration test: Graph → Query → External Filter validation

    This test verifies that query traversal and filtering behave consistently
    when used as separate, independent components.

    1. Build a graph with multiple node types
    2. Run a forward query over the graph
    3. Apply a FilterByType independently from Query
    4. Validate consistency between filtered nodes and query results
    """

    # 1. Build graph with mixed node types
    graph = Graph()
    graph.add_edge("type", "A", "schema:Person")
    graph.add_edge("type", "B", "schema:Person")
    graph.add_edge("type", "C", "schema:Organization")

    # 2. Run query traversal (no filtering inside Query)
    query = Query(graph)
    paths = query.query_path_forward(["type"])

    # 3. Apply filter independently on full graph
    person_filter = FilterByType("schema:Person")
    filtered_nodes = person_filter.apply(graph)
    filtered_labels = {node.label for node in filtered_nodes}

    # 4. Extract and validate query results
    results = {(p[0].label, p[-1].label) for p in paths}

    assert "A" in filtered_labels
    assert "B" in filtered_labels
    assert "C" not in filtered_labels

    assert ("A", "schema:Person") in results
    assert ("B", "schema:Person") in results