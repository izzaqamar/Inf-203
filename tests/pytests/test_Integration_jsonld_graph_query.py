"""
Pytest for integration
Recycled parts (as we like the envirorment) from test_integration_graph_filter_then_query
User story: 1.1, 1.2, 1.5
"""
import os
import sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "src"))
sys.path.insert(0, BASE_DIR)

from graph_project.jsonLD_parser import JsonLD_parser
from graph_project.query import Query


def test_integration_jsonld_to_graph_to_query_simple_path():
    """
    Integration test: JSON-LD → Graph → Query
    1. Load JSON-LD input file
    2. Build graph from parser
    3. Run forward query on graph
    4. Validate expected relationship exists
    """
    # 1. Load JSON-LD input file
    parser = JsonLD_parser()
    graph = parser.load_jsonld(
        os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "linked-data-intro-context.json")
        ),
        remove_duplicates=False
    )

    # 2. Build graph from parser
    query = Query(graph)

    # 3. Run forward query on graph
    paths = query.query_path_forward(["schema:superEvent"])
    query_results = set()
    for path in paths:
        start_label = path[0].label
        end_label = path[-1].label
        query_results.add((start_label, end_label))

    # 4. Validate expected relationship exists
    assert ("example-abox:ISSON25", "example-abox:NANOTEXNOLOGY_2025") in query_results