import networkx as nx
import matplotlib.pyplot as plt


class GraphVisualizer:
    """
    Usage:
        visualizer = GraphVisualizer()
        visualizer.visualize(graph)

    Takes a Graph object from the project and displays it as a directed graph
    using NetworkX and Matplotlib.
    """

    def short_label(self, label):
        """
        Returns a shortened version of a node label
        Args:
            label (str): The original node label
        Returns:
            str: The shortened label
        """

        if label is None:
            return None

        return label.split(":")[-1]

    def visualize(self, graph):
        """
        Converts the project's Graph object into a NetworkX graph
        and visualizes it.

        Args:
            graph: A Graph object containing nodes and edges.

        This function:
        - Creates a directed NetworkX graph
        - Adds all graph edges
        - Draws nodes and edge labels
        - Displays the graph
        """

        G = nx.DiGraph()

        # Convert project graph edges into NetworkX edges
        for edge in graph.edges:
            G.add_edge(
                self.short_label(edge.source.label),
                self.short_label(edge.target.label),
                label=edge.label
            )

        plt.figure(figsize=(14, 10))
        pos = nx.spring_layout(G, k=1.5, seed=42)

        # Draw graph
        nx.draw(
            G,
            pos,
            with_labels=True,
            arrows=True,
            node_size=2000,
            font_size=8,
            arrowsize=15
        )

        # Draw edge labels
        nx.draw_networkx_edge_labels(
            G,
            pos,
            edge_labels=nx.get_edge_attributes(G, "label"),
            font_size=7
        )

        plt.tight_layout()
        plt.show()

    def print_edges(self, graph):
        """
        Prints all graph edges, used for debugging

        Args:
            graph: A Graph object containing nodes and edges
        """

        G = nx.DiGraph()

        # Convert project graph edges into NetworkX edges
        for edge in graph.edges:
            G.add_edge(
                self.short_label(edge.source.label),
                self.short_label(edge.target.label),
                label=edge.label
            )

        print(list(G.edges(data=True)))