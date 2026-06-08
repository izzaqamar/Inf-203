# Inf-203 Project
# Group:04
# Worksheet:1
# Task: 03


class Node:
    def __init__(self, label):
        # Each node here has a unique label (its ID in the graph)
        self.label = label
        self.out = []  # edges where this node is the source
        self.inc = []  # edges where this node is the target
        self.attributes = {}  # this store literal values if required

    def __repr__(self):
        return f"Node({self.label})"


class Edge:
    def __init__(self, label, source, target):
        # Here Edge label not required to be unique
        self.label = label
        self.source = source
        self.target = target

    def __repr__(self):
        return f"Edge({self.label}, {self.source.label} -> {self.target.label})"


class Graph:
    def __init__(self):
        # Here we Store nodes in a dictionary so we can enforce unique labels
        self.nodes = {}
        self.edges = []  # list of all edges

    def add_node(self, label):
        if label not in self.nodes:
            self.nodes[label] = Node(label)
        return self.nodes[label]

    def add_edge(self, label, source_label, target_label):
        # We make sure both nodes exist (we create them if they do not exist)
        source = self.add_node(source_label)
        target = self.add_node(target_label)
        edge = Edge(label, source, target)
        self.edges.append(edge)
        source.outgoing.append(edge)
        target.incoming.append(edge)
        return edge

#test
