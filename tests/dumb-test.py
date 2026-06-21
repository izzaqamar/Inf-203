import os
import sys
import json

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
sys.path.insert(0, BASE_DIR)

from graph_project.jsonLD_parser import JsonLD_parser
from graph_project.OntologyTransformer import OntologyTransformer

file_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "use_case_Inf203.jsonld")
)

parser = JsonLD_parser()
json_path = os.path.join(BASE_DIR, "..", "tests", "use_case_Inf203.jsonld")
graph = parser.load_jsonld(json_path, remove_duplicates=False)

node_d = graph.nodes["http://example.org/_d"]
for e in node_d.outgoing:
    print(e.label, "->", e.target.label)

