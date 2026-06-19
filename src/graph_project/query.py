# Task 06 + Task 09(partially)
from collections import deque
from .Filter import FilterByType, FilterByName, FilterOrphans


class Query:
    """
    Performs graph queries and analysis
    """

    def __init__(self, graph):
        self._graph = graph

    @property
    def graph(self):
        return self._graph

    def query_path_forward(self, labels):
        """
        - Executes a forward-only path query by following a sequence of edge labels.
        - Starts from all nodes in the graph.
        - At each step, only outgoing edges are considered.
        - Paths are extended only when an edge matches the current label.
        - If no valid continuation exists, the result becomes empty.

        Parameters

        labels : list of str
            Edge labels to follow in order, using outgoing edges only.

        Returns

        list[list[Node]]
            All valid paths as lists of nodes from start to end.
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

    # Task  09: Backward path and Mixed path
    def query_path(self, labels, directions):
        """
        Executes a path query over the graph following labeled edges in sequence,
        with support for both forward and backward traversal.
        - Starts from all nodes in the graph.
        - Each step filters and extends existing paths based on label + direction.
        - Forward uses outgoing edges; backward uses incoming edges.
        - Returns an empty list if no paths match at any step.

        Parameters

        labels : list of str
            Edge labels to follow in order.
        directions : list of bool
            Direction for each label (True = outgoing/forward,
            False = incoming/backward).

        Returns

        list[list[Node]]
            All valid paths as lists of nodes from start to end.
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
                        new_paths.append(path + [next_node])

            paths = new_paths

        # Print results
        print("x0\t\tx{}".format(len(labels)))
        print("-" * 40)
        for p in paths:
            print(f"{p[0].label}\t{p[-1].label}")

        return paths
    
    def shortest_path(self, start_node, end_node):
        """
        Args:
            start_node (Node): The node to start the search from.
            end_node (Node): The node to find the path to.

        Returns:
            list: A list of nodes representing the shortest path from start_node to end_node. 
            If there is no path, returns an empty list.
        """
        if start_node == end_node:
            return [start_node]
        
        visited = set()
        queue = deque([(start_node, [start_node])])

        # BFS algorithm to find the shortest path
        while queue:
            i = queue.popleft()
            current_node = i[0]
            path = i[1]

            if current_node == end_node:
                return path
            if current_node not in visited:
                visited.add(current_node)
                for edge in current_node.outgoing:
                    neighbor = edge.target
                    if neighbor not in visited:
                        queue.append((neighbor, path + [neighbor]))

        # If there is no path between the start and end nodes, return an empty list
        return []
