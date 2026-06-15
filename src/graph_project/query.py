# Task 06 + Task 09(partially)


class Query:
    """Performs path queries on a graph."""

    def __init__(self, graph):
        self._graph = graph

    @property
    def graph(self):
        return self._graph

    def query_path_forward(self, labels):
        """
        Follow a sequence of edge labels in the forward direction.
        Example type: ["https://schema.org/superEvent", "https://schema.org/organizer"]
        """

        # We start with all nodes as possible x0
        paths = [[node] for node in self.graph.nodes.values()]

        # Follow each label in order
        for label in labels:
            # This will store all the new paths we discover for this labe
            new_paths = []
            for path in paths:
                # The last node in the path is where we currently stand
                last = path[-1]
                for edge in last.outgoing:
                    # we check if this edge has the label we are supposed to follow, if yes then wwe extend the path
                    if edge.label == label:
                        new_paths.append(path + [edge.target])
            paths = new_paths

        # Print results in table form
        print("x0\t\tx{}".format(len(labels)))
        print("-" * 40)
        for p in paths:
            print(f"{p[0].label}\t{p[-1].label}")

        return paths

    # Task 08 & 09: Passing function object and backward paath
    def query_path(self, labels, directions, node_filter=None):
        """
        Follow a sequence of edge labels with specified directions.
        labels:      list of edge labels
        directions:  list of booleans (True = forward, False = backward)
        """

        # Start with all nodes as possible x0
        paths = [[node] for node in self.graph.nodes.values()]

        for label, forward in zip(labels, directions):
            new_paths = []

            for path in paths:
                last = path[-1]

                # Choose outgoing or incoming edges
                edges = last.outgoing if forward else last.incoming

                for edge in edges:
                    if edge.label == label:
                        # If forward: last : target
                        # If backward: last : source
                        next_node = edge.target if forward else edge.source
                        # Apply filter if provided
                        if node_filter is None or node_filter(next_node):
                            new_paths.append(path + [next_node])

            paths = new_paths

        # Print results
        print("x0\t\tx{}".format(len(labels)))
        print("-" * 40)
        for p in paths:
            print(f"{p[0].label}\t{p[-1].label}")

        return paths
