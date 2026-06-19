import os
import sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "src"))
sys.path.insert(0, BASE_DIR)

from graph_project.jsonLD_parser import JsonLD_parser
from graph_project.query import Query


def test_integration_jsonld_to_graph_to_query_simple_path():
    """
    Integration test: JSON-LD → Graph → Query traversal

    1. Load JSON-LD file
    2. Build graph from parser
    3. Run forward query
    4. Verify expected relationship exists
    """

    # 1. Load and parse JSON-LD into graph
    parser = JsonLD_parser()
    graph = parser.load_jsonld(
        os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "linked-data-intro-context.json")
        ),
        remove_duplicates=False
    )

    # 2. Run query over constructed graph
    query = Query(graph)
    paths = query.query_path_forward(["schema:superEvent"])

    # 3. Extract start/end pairs
    results = {
        (p[0].label, p[-1].label)
        for p in paths
    }

    # 4. Verify known expected relation exists
    assert (
        "example-abox:ISSON25",
        "example-abox:NANOTEXNOLOGY_2025"
    ) in results