# Task: 03 + Task 05 + task 06 + Task 08 + Partial Task 09

from .Node import Node
from .Edge import Edge


class Graph:
    """Represents a directed graph consisting of nodes and edges.

    Nodes are stored in a dictionary to enforce unique labels.

    Attributes
    nodes : dict[str, Node]
        Mapping from node labels to Node objects.
    edges : List of all edges in the graph.
    """

    def __init__(self):
        self._nodes = {}
        self._edges = []

    @property
    def nodes(self):
        return self._nodes

    @property
    def edges(self):
        return self._edges

    def add_node(self, label):
        """Add a node to the graph if it does not already exist.

        Parameters
        label : Unique identifier for the node.

        Returns the existing or newly created node.
        """

        if label not in self._nodes:
            self._nodes[label] = Node(label)

        return self._nodes[label]

    def add_edge(self, label, source_label, target_label):
        """Create a directed edge between two nodes.

        If the source or target nodes do not exist, they are created.

        Parameters
        label : Label for the edge.
        source_label : Label of the source node.
        target_label : Label of the target node.

        Returns the newly created edge.
        """

        source = self.add_node(source_label)
        target = self.add_node(target_label)

        edge = Edge(label, source, target)

        self._edges.append(edge)
        source.outgoing.append(edge)
        target.incoming.append(edge)

        return edge

    def __repr__(self):
        return f"Graph(nodes={len(self.nodes)}, edges={len(self.edges)})"


### TEST ###
"""
if __name__ == "__main__":

    graph = Graph()

    graph.add_edge("likes", "Martin", "Python")
    graph.add_edge("studies", "Martin", "NMBU")
    graph.add_edge("works_at", "Martin", "Elkjøp")
    graph.add_edge("Walks", "Martin", "Home")

    print("Nodes:")
    for node in graph.nodes.values():
        print(node)

    print("\nEdges:")
    for edge in graph.edges:
        print(edge)

    print("\nOutgoing from Martin:")
    for edge in graph.nodes["Martin"].outgoing:
        print(edge)

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
        
"""
