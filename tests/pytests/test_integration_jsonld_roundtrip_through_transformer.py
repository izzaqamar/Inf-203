"""
Pytest for the round trip of JsonLD_parser -> Graph -> OntologyTransformer -> JsonLD_parser

Uses the existing file tests/linked-data-intro-context.json
"""

import os
import sys
import json

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "src"))
sys.path.insert(0, BASE_DIR)

from graph_project.jsonLD_parser import JsonLD_parser
from graph_project.OntologyTransformer import OntologyTransformer

file_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "linked-data-intro-context.json")
)


def test_integration_jsonld_roundtrip_through_transformer(tmp_path):
    """
    Integration test: JsonLD_parser -> Graph -> OntologyTransformer -> export_jsonld -> JsonLD_parser
    1. Parse the ISSON25 fixture into a graph
    2. Write an alignment mapping schema:Person to test:Person
    3. Transform the graph and export it back to JSON-LD
    4. Re-parse the exported file with JsonLD_parser
    5. Validate the re-parsed graph matches the transformed graph
    """
    # 1. Parse the ISSON25 fixture into a graph
    parser = JsonLD_parser()
    source_graph = parser.load_jsonld(file_path, remove_duplicates=False)

    # 2. Write an alignment mapping schema:Person to test:Person
    alignment_data = {
        "concepts": {
            "schema:Person": {"target": "test:Person", "match": "skos:exactMatch"}
        }
    }
    alignment_file = tmp_path / "alignment.json"
    alignment_file.write_text(json.dumps(alignment_data))

    # 3. Transform the graph and export it back to JSON-LD
    transformer = OntologyTransformer()
    target_graph = transformer.transform(source_graph, str(alignment_file))

    output_file = tmp_path / "output" / "isson_transformed.jsonld"
    transformer.export_jsonld(target_graph, str(output_file))

    # 4. Re-parse the exported file with JsonLD_parser
    reparsed_graph = parser.load_jsonld(str(output_file), remove_duplicates=False)

    # 5. Validate the re-parsed graph matches the transformed graph
    assert None not in reparsed_graph.nodes

    reparsed_labels = set(reparsed_graph.nodes.keys())
    target_labels = set(target_graph.nodes.keys())
    assert reparsed_labels == target_labels

    argiris_node = reparsed_graph.nodes["example-abox:Argiris_Laskarakis"]
    type_targets = [e.target.label for e in argiris_node.outgoing if e.label == "type"]
    assert "test:Person" in type_targets