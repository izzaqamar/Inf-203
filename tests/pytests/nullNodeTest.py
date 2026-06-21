"""
test_integration_json_roundtrip failed

STATUS: SOLVED
Solution: @graph as a wrapper when the transformer creates a json

Error below:

# 5. Validate the re-parsed graph matches the transformed graph
>       assert None not in reparsed_graph.nodes
E       AssertionError: assert None not in {None: Node(None), 'example-abox:ISSON25': Node(example-abox:ISSON25), 'schema:EducationEvent': Node(schema:EducationEvent), 'example-abox:Halliru_Ibrahim': Node(example-abox:Halliru_Ibrahim), ...}
E        +  where {None: Node(None), 'example-abox:ISSON25': Node(example-abox:ISSON25), 'schema:EducationEvent': Node(schema:EducationEvent), 'example-abox:Halliru_Ibrahim': Node(example-abox:Halliru_Ibrahim), ...} = Graph(nodes=10, edges=21).nodes

test_integration_jsonld_roundtrip_through_transformer.py:55: AssertionError
============ short test summary info =============
FAILED test_integration_jsonld_roundtrip_through_transformer.py::test_integration_jsonld_roundtrip_through_transformer - AssertionError: assert None not in {None: Node...
"""

import sys
import os
import json

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SRC_DIR = os.path.join(BASE_DIR, "src")
DATA_PATH = os.path.join(BASE_DIR, "tests", "linked-data-intro-context.json")
OUTPUT_PATH = os.path.join(BASE_DIR, "tests", "pytests", "debug_output.jsonld")

sys.path.insert(0, SRC_DIR)

from graph_project.jsonLD_parser import JsonLD_parser
from graph_project.OntologyTransformer import OntologyTransformer

parser = JsonLD_parser()
graph = parser.load_jsonld(DATA_PATH, remove_duplicates=False)

transformer = OntologyTransformer()
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
transformer.export_jsonld(graph, OUTPUT_PATH)

with open(OUTPUT_PATH, "r", encoding="utf-8") as f:
    print(f.read())