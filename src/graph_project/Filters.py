from .Graph import Graph


class Filter(Graph):
    def filter_by_type(self, graph, node_type):
        """
        Filters the graph to find all nodes of a specific type

        Args: 
            graph (Graph): The graph to filter.
            node_type (str): The type of nodes to find.

        """

        listOfNodesWithType = []

        for node in graph.nodes:
            for edge in node.outgoing:
                if edge.label == "type" and edge.target.label == node_type:
                    listOfNodesWithType.append(node)
        
        return listOfNodesWithType
    
    def filter_by_name(self, graph, name):
        """
        Filters the graph to find all nodes with a specific name

        Args: 
            graph (Graph): The graph to filter.
            name (str): The name of nodes to find.

        """

        listOfNodesWithName = []

        for node in graph.nodes:
            if name in node.label:
                listOfNodesWithName.append(node)
        
        return listOfNodesWithName
    
    def filter_orphans(self, graph):
        """
        Filters the graph to find all orphan nodes (nodes with no incoming or outgoing edges)

        Args: 
            graph (Graph): The graph to filter.

        """

        listOfOrphanNodes = []

        for node in graph.nodes:
            if len(node.incoming) == 0 and len(node.outgoing) == 0:
                listOfOrphanNodes.append(node)
        
        return listOfOrphanNodes
    
