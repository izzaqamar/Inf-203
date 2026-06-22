"""
Pytest for the ERROR handeling for missing files
User story: 2.1
"""

import os
import sys
import json
import pytest

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "src"))
sys.path.insert(0, BASE_DIR)

from graph_project.JsonLD_parser import JsonLD_parser
from graph_project.OntologyTransformer import OntologyTransformer
from graph_project.Graph import Graph


def test_jsonld_parser_raises_error_for_missing_file():
    """
    Passing a non-existent file path should raise a FileNotFoundError
    """
    parser = JsonLD_parser()

    with pytest.raises(FileNotFoundError):
        parser.load_jsonld("non_existent_file.json", remove_duplicates=False)


def test_jsonld_parser_raises_error_for_malformed_json(tmp_path):
    """
    Passing a file with invalid JSON content should raise a json.JSONDecodeError
    """
    bad_file = tmp_path / "bad.json"
    bad_file.write_text("this is not valid json {{{{")

    parser = JsonLD_parser()

    with pytest.raises(json.JSONDecodeError):
        parser.load_jsonld(str(bad_file), remove_duplicates=False)


def test_ontology_transformer_raises_error_for_missing_alignment_file():
    """
    Passing a non-existent alignment file should raise a FileNotFoundError
    """
    transformer = OntologyTransformer()
    graph = Graph()
    graph.add_edge("type", "ex:A", "ex:B")

    with pytest.raises(FileNotFoundError):
        transformer.transform(graph, "non_existent_alignment.json")