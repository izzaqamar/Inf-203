import os
import sys
import json

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "src"))
sys.path.insert(0, BASE_DIR)

from graph_project.Graph import Graph
from graph_project.OntologyTransformer import OntologyTransformer
from graph_project.query import Query


def test_integration_ontology_transformer_then_query():
    """
    Integration test: Graph → OntologyTransformer → Query traversal

    1. Build a source graph
    2. Apply ontology transformation
    3. Run query on transformed graph
    4. Verify labels were transformed and query still works
    """

    # 1. Build source graph
    source_graph = Graph()
    source_graph.add_edge("knows", "old:Person", "old:Other")

    # 2. Create temporary alignment file
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

    # 3. Transform graph
    transformer = OntologyTransformer()
    transformed_graph = transformer.transform(source_graph, alignment_file)

    # 4. Run query on transformed graph
    query = Query(transformed_graph)
    paths = query.query_path_forward(["knows"])

    results = {
        (p[0].label, p[-1].label)
        for p in paths
    }

    # 5. Verify transformation + query correctness
    assert ("new:Human", "old:Other") in results

    # cleanup
    os.remove(alignment_file)