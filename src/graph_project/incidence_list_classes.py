# Inf-203 Project
# Group:04
# Worksheet:1
# Task: 03


class Node:
    """Represents a node (vertex) in a directed graph.

    Parameters
    label : A unique identifier for the node.

    Attributes
    label : The unique ID of the node.
    outgoing : list of Edges for which this node is the source.
    incoming : list of Edges for which this node is the target.
    attributes : Optional dictionary for storing literal values or metadata.
    """

    def __init__(self, label):
        self.label = label
        self.outgoing = []
        self.incoming = []
        self.attributes = {}

    def __repr__(self):
        return f"Node({self.label})"


class Edge:
    """Represents a directed edge between two nodes.

    Parameters
    label : A descriptive label for the edge (not required to be unique).
    source : The node from which the edge originates.
    target : The node at which the edge terminates.

    Attributes
    label : The edge label.
    source : The source node.
    target : The target node.
    """

    def __init__(self, label, source, target):
        self.label = label
        self.source = source
        self.target = target

    def __repr__(self):
        return f"Edge({self.label}, {self.source.label} -> {self.target.label})"


class Graph:
    """Represents a directed graph consisting of nodes and edges.

    Nodes are stored in a dictionary to enforce unique labels.

    Attributes
    nodes : dict[str, Node]
        Mapping from node labels to Node objects.
    edges : List of all edges in the graph.
    """

    def __init__(self):
        self.nodes = {}
        self.edges = []

    def add_node(self, label):
        """Add a node to the graph if it does not already exist.

        Parameters
        label : Unique identifier for the node.

        Returns the existing or newly created node.
        """
        if label not in self.nodes:
            self.nodes[label] = Node(label)
        return self.nodes[label]

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
        self.edges.append(edge)
        source.outgoing.append(edge)
        target.incoming.append(edge)
        return edge
