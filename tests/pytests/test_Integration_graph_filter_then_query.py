import os
import sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "src"))
sys.path.insert(0, BASE_DIR)

from graph_project.Graph import Graph
from graph_project.query import Query
from graph_project.Filter import FilterByType


def test_integration_graph_filter_then_query():
    """
    Integration test: Graph → Filter → Query

    This test verifies that graph construction, filtering, and query traversal work correctly as independent components in the system.

    1. Build a graph with multiple node types
    2. Apply a FilterByType independently from Query
    3. Run a forward query over the full graph
    4. Validate both filtering and query results
    """

    # 1. Build graph with mixed node types
    graph = Graph()
    graph.add_edge("type", "A", "schema:Person")
    graph.add_edge("type", "B", "schema:Person")
    graph.add_edge("type", "C", "schema:Organization")

    query = Query(graph)

    # 2. Run query traversal (no filtering inside Query)
    paths = query.query_path_forward(["type"])

    # 3. Apply filter independently
    person_filter = FilterByType("schema:Person")
    filtered_nodes = person_filter.apply(graph)
    filtered_labels = {n.label for n in filtered_nodes}

    # 4. Extract and validate results
    results = {(p[0].label, p[-1].label) for p in paths}

    assert "A" in filtered_labels
    assert "B" in filtered_labels
    assert "C" not in filtered_labels

    assert ("A", "schema:Person") in results
    assert ("B", "schema:Person") in results