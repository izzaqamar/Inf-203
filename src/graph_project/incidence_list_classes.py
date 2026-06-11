# Inf-203 Project
# Group:04
# Worksheet:1
# Task: 03 + 05


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
        self._label = label
        self._outgoing = []
        self._incoming = []
        self._attributes = {}

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, value):
        self._label = value

    @property
    def outgoing(self):
        return self._outgoing

    @property
    def incoming(self):
        return self._incoming

    @property
    def attributes(self):
        return self._attributes

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
        self._label = label
        self._source = source
        self._target = target

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, value):
        self._label = value

    @property
    def source(self):
        return self._source

    @source.setter
    def source(self, value):
        self._source = value

    @property
    def target(self):
        return self._target

    @target.setter
    def target(self, value):
        self._target = value

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
'''
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
'''