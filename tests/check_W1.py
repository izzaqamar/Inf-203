import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from graph_project.jsonLD_parser import JsonLD_parser
from graph_project.Visualizer import GraphVisualizer


def main():
    """
    Runs a test of the JSON-LD parser and graph construction.

    This function:
    - Loads a JSON-LD file
    - Converts it into a directed graph using JsonLD_parser()
    - Prints all nodes in the graph
    - Prints all edges in the graph
    - Displays a sample node with its outgoing and incoming edges
    - Visualizes the graph using NetworkX and Matplotlib
    """

    file_path = os.path.join(
        os.path.dirname(__file__), "linked-data-intro-context.json"
    )  #  JSON-LD file

    parser = JsonLD_parser()
    graph = parser.load_jsonld(file_path, False)

    print("\nNodes:")
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

    # Visualization

    visualizer = GraphVisualizer()
    visualizer.visualize(graph)


if __name__ == "__main__":
    main()
