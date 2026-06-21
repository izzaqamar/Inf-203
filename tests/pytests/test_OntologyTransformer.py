"""
Pytest for the OntologyTransformer class
User story: 1.1, 1.2, 2.3

Uses pytests built in tmp_path  to create alignment files and export output on the fly, so nothing is left behind on disk after the tests run.
"""
import os
import sys
import json

# UPDATE IF MOVED FROM src/tests/pytests
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "src"))
sys.path.insert(0, BASE_DIR)

from graph_project.Graph import Graph
from graph_project.OntologyTransformer import OntologyTransformer


def test_ontologytransformer_load_alignment_reads_valid_mapping(tmp_path):
    """
    load_alignment should read a JSON file and return a dict mapping source labels to target labels, for entries with a supported match type
    """
    alignment_data = {
        "concepts": {
            "old:Person": {"target": "new:Human", "match": "skos:exactMatch"}
        }
    }
    alignment_file = tmp_path / "alignment.json"
    alignment_file.write_text(json.dumps(alignment_data))

    transformer = OntologyTransformer()
    alignment_map = transformer.load_alignment(str(alignment_file))

    assert alignment_map == {"old:Person": "new:Human"}


def test_ontologytransformer_load_alignment_accepts_other_supported_match_types(tmp_path):
    """
    load_alignment should not be hardcoded to only accept skos:exactMatch
    Other supported types (like  without the skos: prefix) should also be included in the result
    """
    alignment_data = {
        "concepts": {
            "old:A": {"target": "new:A", "match": "closeMatch"}
        }
    }
    alignment_file = tmp_path / "alignment.json"
    alignment_file.write_text(json.dumps(alignment_data))
 
    transformer = OntologyTransformer()
    alignment_map = transformer.load_alignment(str(alignment_file))
 
    assert alignment_map == {"old:A": "new:A"}


def test_ontologytransformer_transform_label_uses_mapping():
    """
    _transform_label should return the mapped label when one exists in the alignment map
    """
    transformer = OntologyTransformer()
    alignment_map = {"old:Person": "new:Human"}

    assert transformer._transform_label("old:Person", alignment_map) == "new:Human"


def test_ontologytransformer_transform_label_keeps_unmapped_label():
    """
    _transform_label should return the original label unchanged if no mapping exists for it
    """
    transformer = OntologyTransformer()
    alignment_map = {"old:Person": "new:Human"}

    assert transformer._transform_label("old:Unmapped", alignment_map) == "old:Unmapped"


def test_ontologytransformer_transform_replaces_mapped_labels(tmp_path):
    """
    transform() should produce a new graph where node/edge labels with a matching alignment rule are replaced, while everything else stays the same
    """
    alignment_data = {
        "concepts": {
            "old:Person": {"target": "new:Human", "match": "skos:exactMatch"}
        }
    }
    alignment_file = tmp_path / "alignment.json"
    alignment_file.write_text(json.dumps(alignment_data))

    source_graph = Graph()
    source_graph.add_edge("knows", "old:Person", "old:Other")

    transformer = OntologyTransformer()
    target_graph = transformer.transform(source_graph, str(alignment_file))

    target_labels = list(target_graph.nodes.keys())
    assert "new:Human" in target_labels
    assert "old:Other" in target_labels
    assert "old:Person" not in target_labels


def test_ontologytransformer_export_jsonld_writes_expected_structure(tmp_path):
    """
    export_jsonld should write a JSON-LD file where each node becomes an object with an @id, and edges become properties on the source node
    """
    graph = Graph()
    graph.add_edge("type", "ex:Martin", "schema:Person")

    transformer = OntologyTransformer()
    output_file = tmp_path / "output" / "result.jsonld"

    transformer.export_jsonld(graph, str(output_file))

    with open(output_file, "r") as f:
        data = json.load(f)

    nodes_by_id = {n["@id"]: n for n in data["@graph"]}
    martin_node = nodes_by_id["ex:Martin"]

    # type edges are renamed to @type in the JSON-LD export
    assert martin_node["@type"] == ["schema:Person"]
