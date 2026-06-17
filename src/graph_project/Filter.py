from .Graph import Graph


class FilterByType:
    """
    Callable filter that filters nodes by types
    Either:
        - Used per node
            - Returns True if node has type
        - On entire graph using apply()
            - Returns list of nodes
    """

    def __init__(self, node_type):
        """
        Args:
            node_type (str): The type label to filter by, e.g. "schema:Person"
        """

        self.node_type = node_type

    def __call__(self, node):
        """
        Returns true if the node matches the type
        Args:
            node (Node): The node to check.
        """

        for edge in node.outgoing:
            if edge.label == "type" and edge.target.label == self.node_type:
                return True
        return False

    def apply(self, graph):
        """
        Returns all nodes of the type in a graph
        Args:
            graph (Graph): The graph to filter.
        """

        nodesWithType = []
        for node in graph.nodes.values():
            if self(node):
                nodesWithType.append(node)
        return nodesWithType


class FilterByName:
    """
    Callable filter that filters nodes by name
    Either:
        - Used per node
            - Returns True if node has lable)
        - On entire graph using apply()
            - Returns list of nodes
    """

    def __init__(self, name):
        """
        Args:
            name (str): The name or partial name to filter by
        """

        self.name = name

    def __call__(self, node):
        """
        Returns true if the name is found in the node lable
        Args:
            node (Node): The node to check
        """

        return self.name in node.label

    def apply(self, graph):
        """
        Returns all nobes that have the spesific name
        Args:
            graph (Graph): The graph to filter.
        """

        nodesWithName = []
        for node in graph.nodes.values():
            if self(node):
                nodesWithName.append(node)
        return nodesWithName


class FilterOrphans:
    """
    Callable filter that filters orphans
    Either:
        - Used per node
            - Returns True if node is orphan
        - On entire graph using apply()
            - Returns list of nodes
    """

    def __call__(self, node):
        """
        Returns true if node has no edges
        Args:
            node (Node): The node to check
        """

        if (len(node.incoming) == 0) and (len(node.outgoing) == 0):
            return True
        else:
            return False

    def apply(self, graph):
        """
        Returns all orphan nodes in the graph
        Args:
            graph (Graph): The graph to filter
        """

        orphanNodes = []
        for node in graph.nodes.values():
            if self(node):
                orphanNodes.append(node)
        return orphanNodes
