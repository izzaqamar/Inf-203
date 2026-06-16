import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from graph_project.jsonLD_parser import JsonLD_parser
from graph_project.Filters import filter_orphans, filter_by_name, filter_by_type
from graph_project.AnalysisTools import shortest_path


def main():
    """
    Runs tests for
        - filter_orphans
        - filter_by_name
        - filter_by_type
        - shortest_path
    """

    parser = JsonLD_parser()
    graph = parser.load_jsonld(file_path, False)

    # Path to your JSON-LD file
    file_path = os.path.join(os.path.dirname(__file__), "use_case_Inf203.jsonld")

    print("Loading JSON-LD file:", file_path)

    parser = JsonLD_parser()
    graph = parser.load_jsonld(file_path, False)

    print("\nGraph loaded.")
    print(f"Nodes: {len(graph.nodes)}")
    print(f"Edges: {len(graph.edges)}")
