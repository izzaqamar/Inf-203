from graph_project.jsonLD_parser import load_jsonld
import os


def main():
    """
    Runs a test of the JSON-LD parser and graph construction.

    This function:
    - Loads a JSON-LD file
    - Converts it into a directed graph using load_jsonld()
    - Prints all nodes in the graph
    - Prints all edges in the graph
    - Displays a sample node with its outgoing and incoming edges"""

    file_path = os.path.join(
        os.path.dirname(__file__), "linked-data-intro-context.json"
    )  #  JSON-LD file

    graph = load_jsonld(file_path)

    print("Nodes:")
    for label, node in graph.nodes.items():
        print(label, node)

    print("\nEdges:")
    for edge in graph.edges:
        print(edge)

    print("\nSample structure check:")
    # we pick first node in the dictionary
    exmaple_node = next(iter(graph.nodes.values()))
    print("Node:", exmaple_node)
    print("Outgoing edges:", exmaple_node.outgoing)
    print("Incoming edges:", exmaple_node.incoming)


if __name__ == "__main__":
    main()
