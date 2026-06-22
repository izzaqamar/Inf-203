"""
Pytest for integration
User story: 1.2, 1.5
"""

import os
import sys
import json

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "src"))
sys.path.insert(0, BASE_DIR)

from graph_project.Graph import Graph
from graph_project.OntologyTransformer import OntologyTransformer
from graph_project.Query import Query


def test_integration_ontology_transformer_then_query():
    """
    Integration test: Graph → OntologyTransformer → Query

    1. Build source graph
    2. Apply ontology transformation
    3. Run forward query on transformed graph
    4. Check that transformation is in query_results
    """

    # 1. Build source graph
    source_graph = Graph()
    source_graph.add_edge("knows", "old:Person", "old:Other")

    # 2. Apply ontology transformation (something made up)
    alignment_data = {
        "concepts": {
            "old:Person": {
                "target": "new:Human",
                "match": "skos:exactMatch"
            }
        }
    }

    alignment_file = "temp_alignment.json"
    with open(alignment_file, "w") as f:
        json.dump(alignment_data, f)

    transformer = OntologyTransformer()
    transformed_graph = transformer.transform(source_graph, alignment_file)

    # 3. Run forward query on transformed graph
    query = Query(transformed_graph)
    paths = query.query_path_forward(["knows"])

    query_results = set()
    for path in paths:
        start_label = path[0].label
        end_label = path[-1].label
        query_results.add((start_label, end_label))

    # 4. Check that transformation is in query_results
    assert ("new:Human", "old:Other") in query_results

    os.remove(alignment_file)