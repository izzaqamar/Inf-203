import os
import sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
sys.path.insert(0, BASE_DIR)

from graph_project.jsonLD_parser import JsonLD_parser
from graph_project.query import Query
from graph_project.Filter import FilterByType


def main():
    """
    Test script for Task 6:
    - Loads a JSON-LD file
    - Builds the graph
    - Runs a forward path query
    - Prints the results
    """

    # Path to your JSON-LD file
    file_path = os.path.join(os.path.dirname(__file__), "use_case_Inf203.jsonld")

    print("Loading JSON-LD file:", file_path)

    parser = JsonLD_parser()
    graph = parser.load_jsonld(file_path, False)

    print("\nGraph loaded.")
    print(f"Nodes: {len(graph.nodes)}")
    print(f"Edges: {len(graph.edges)}")

    # Creating Query object
    query = Query(graph)

    # TASK 6: Run forward path query

    print("TASK 6: forward path query ")

    labels = [
        "https://w3id.org/dppo/ontology/containsInformation",
        "https://w3id.org/dppo/ontology/hasPart",
    ]

    print("Query labels:", labels)
    print("\nResults:\n")

    query.query_path_forward(labels)

    # TASK 9: We test  backward path query

    print("TASK 9: backward path query ")

    labels = ["https://w3id.org/dppo/ontology/hasPart"]
    directions = [False]

    print("Query labels:", labels)
    print("Directions:", directions)
    print("\nResults:\n")

    query.query_path(labels, directions)

    # Task 9: We test forward + filter
    print("TASK: forward + filter")

    labels = ["https://w3id.org/dppo/ontology/hasPart"]
    directions = [True]

    filters = [FilterByType("https://w3id.org/glass/ontology/WindowGlass")]
    print("Query labels:", labels)
    print("Directions:", directions)
    print("Filter:", "WindowGlass")
    print()

    print("Results:\n")

    query.query_path(labels, directions, filters)


if __name__ == "__main__":
    main()
