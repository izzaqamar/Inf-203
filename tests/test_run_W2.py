import os
import sys

# Make sure Python can find your src/ folder
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from graph_project.jsonLD_parser import JsonLD_parser


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

    # TASK 6: Run forward path query

    print("TASK 6: forward path query ")

    labels = [
        "https://w3id.org/dppo/ontology/containsInformation",
        "https://w3id.org/dppo/ontology/hasPart",
    ]

    print("Query labels:", labels)
    print("\nResults:\n")

    graph.query_path_forward(labels)

    # TASK 9: We test  backward path query

    print("TASK 9: backward path query ")

    labels = ["https://w3id.org/dppo/ontology/hasPart"]
    directions = [False]

    print("Query labels:", labels)
    print("Directions:", directions)
    print("\nResults:\n")

    graph.query_path(labels, directions)


if __name__ == "__main__":
    main()
