from .Graph import Graph
from collections import deque


class AnalysisTools(Graph):
    def shortest_path(self, graph, start_node, end_node):
        """
        Finds the shortest path between two nodes in the graph using Breadth-First Search (BFS)

        Args: 
            graph (Graph): The graph to search.
            start_node (Node): The node to start the search from.
            end_node (Node): The node to find the path to.

        Returns:
            list: A list of nodes representing the shortest path from start_node to end_node. 
            If there is no path, returns an empty list.
        """

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
    
