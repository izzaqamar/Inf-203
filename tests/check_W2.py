import os
import sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
sys.path.insert(0, BASE_DIR)

from graph_project.JsonLD_parser import JsonLD_parser
from graph_project.Query import Query
from graph_project.Filter import FilterByType, FilterByName, FilterOrphans


def main():
    """
    Test script for Task 6:
    - Loads a JSON-LD file
    - Builds the graph
    - Runs a forward path query
    - Prints the results
    """

    # Path to  JSON-LD file
    file_path = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__), "..", "src", "data", "use_case_Inf203.jsonld"
        )
    )

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

    # TASK 9.1: We test  backward path query

    print("TASK 9: backward path query ")

    labels = ["https://w3id.org/dppo/ontology/hasPart"]
    directions = [False]

    print("Query labels:", labels)
    print("Directions:", directions)
    print("\nResults:\n")

    query.query_path(labels, directions)

    # TASK 9.2: We test filter by type

    print("\nFILTER TEST 1: FilterByType")
    f_type = FilterByType("https://w3id.org/glass/ontology/WindowGlass")
    results = f_type.apply(graph)
    print(f"Nodes of type WindowGlass: {len(results)}")
    for node in results:
        print(f"  - {node.label}")

    # TASK 9.3: We test filter by name

    print("\nFILTER TEST 2: FilterByName")
    f_name = FilterByName("example.org")
    results = f_name.apply(graph)
    print(f"Nodes with 'example.org' in name: {len(results)}")
    for node in results:
        print(f"  - {node.label}")

    # TASK 9.4: We test filter orphans

    print("\nFILTER TEST 3: FilterOrphans")
    f_orphan = FilterOrphans()
    results = f_orphan.apply(graph)
    print(f"Orphan nodes: {len(results)}")
    for node in results:
        print(f"  - {node.label}")


if __name__ == "__main__":
    main()
