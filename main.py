from src.graph_project.Graph import Graph

"""Demo script for testing the Graph, Node and Edge classes."""


def main():
    graph = Graph()

    #  Build a small example graph
    graph.add_edge("likes", "Martin", "Python")
    graph.add_edge("studies", "Martin", "NMBU")
    graph.add_edge("works_at", "Martin", "Elkjøp")
    graph.add_edge("walks", "Martin", "Home")

    #  Show all nodes
    print("Nodes:")
    for node in graph.nodes.values():
        print(node)

    #  Show all edges
    print("\nEdges:")
    for edge in graph.edges:
        print(edge)

    # Outgoing edges from Martin
    print("\nOutgoing from Martin:")
    for edge in graph.nodes["Martin"].outgoing:
        print(edge)

    # Incoming edges
    print("\nIncoming to Python:")
    for edge in graph.nodes["Python"].incoming:
        print(edge)

    print("\nIncoming to NMBU:")
    for edge in graph.nodes["NMBU"].incoming:
        print(edge)

    print("\nIncoming to Elkjøp:")
    for edge in graph.nodes["Elkjøp"].incoming:
        print(edge)

    print("\nIncoming to Home:")
    for edge in graph.nodes["Home"].incoming:
        print(edge)


if __name__ == "__main__":
    main()
