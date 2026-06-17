# Task 11: Knowledge graph transformation

import json
from graph_project.Graph import Graph


class OntologyTransformer:
    """
    Transforms a source knowledge graph into a target graph
    using mappings defined in an alignment file.

    The alignment file describes how concepts and relations
    from the source ontology correspond to concepts and
    relations in the target ontology. During transformation,
    matching labels are replaced according to these mappings,
    while labels without a matching rule remain unchanged.
    """

    def __init__(self):
        self.supported_matches = [
            "skos:exactMatch",
            "skos:closeMatch",
            "skos:broadMatch",
            "skos:narrowMatch",
            "exactMatch",
            "closeMatch",
            "broadMatch",
            "narrowMatch"
        ]

    def load_alignment(self, alignment_file):
        """
        Loads an alignment file and extracts all valid mappings.

        The alignment file contains relationships between source
        ontology terms and target ontology terms. Only mappings
        with supported match types are included in the resulting
        dictionary.

        Args:
            alignment_file (str): Path to the alignment JSON file.

        Returns:
            dict: A dictionary where source labels are mapped
            to their corresponding target labels.
        """

        with open(alignment_file, "r") as f:
            alignment_data = json.load(f)

        alignment_map = {}

        if "concepts" in alignment_data:
            self._add_mappings(
                alignment_data["concepts"],
                alignment_map
            )

        if "relations" in alignment_data:
            self._add_mappings(
                alignment_data["relations"],
                alignment_map
            )

        return alignment_map

    def _add_mappings(self, mappings, alignment_map):
        """
        Processes a section of the alignment file and adds
        valid mappings to the alignment dictionary.

        Only mappings that contain both a target label and
        a supported match type are included.

        Args:
            mappings (dict): Concept or relation mappings from
                the alignment file.
            alignment_map (dict): Dictionary used to store the
                extracted mappings.
        """

        for source_label, info in mappings.items():

            target_label = info.get("target")
            match_type = info.get("match")

            if (
                target_label is not None
                and match_type in self.supported_matches
            ):
                alignment_map[source_label] = target_label

    def transform(self, source_graph, alignment_file):
        """
        Creates a transformed version of the source graph.

        Every node label and edge label is checked against
        the alignment mappings. If a matching rule exists,
        the label is replaced with its corresponding target
        ontology label. Otherwise, the original label is kept.

        Args:
            source_graph (Graph): The graph to transform.
            alignment_file (str): Path to the alignment file.

        Returns:
            Graph: A new graph containing the transformed
            nodes and edges.
        """

        alignment_map = self.load_alignment(
            alignment_file
        )

        target_graph = Graph()

        #Add all nodes
        for node in source_graph.nodes.values():

            new_label = self._transform_label(
                node.label,
                alignment_map
            )

            target_graph.add_node(new_label)

        #Add transformed edges
        for edge in source_graph.edges:

            new_source = self._transform_label(
                edge.source.label,
                alignment_map
            )

            new_edge = self._transform_label(
                edge.label,
                alignment_map
            )

            new_target = self._transform_label(
                edge.target.label,
                alignment_map
            )

            target_graph.add_edge(
                new_edge,
                new_source,
                new_target
            )

        return target_graph

    def _transform_label(
        self,
        label,
        alignment_map
    ):
        """
        Applies a label transformation if a mapping exists.

        The method looks up the given label in the alignment
        dictionary and returns the mapped value when available.
        If no mapping is found, the original label is returned.

        Args:
            label (str): Label to be checked and transformed.
            alignment_map (dict): Dictionary containing label
                mappings.

        Returns:
            str: The transformed label or the original label.
        """

        if label in alignment_map:
            return alignment_map[label]

        return label

    def export_jsonld(
        self,
        graph,
        output_file
    ):
        """
        Exports a graph to JSON-LD format.

        The graph structure is converted into a JSON-LD
        representation where nodes become JSON objects and
        edges become properties connecting those objects.

        Args:
            graph (Graph): Graph to export.
            output_file (str): Destination file path.
        """

        data = {
            "@graph": []
        }

        nodes_json = {}

        #Create JSON object for each node
        for node in graph.nodes.values():

            nodes_json[node.label] = {
                "@id": node.label
            }

        #Add edges
        for edge in graph.edges:

            source = edge.source.label
            label = edge.label
            target = edge.target.label

            if label == "type":
                label = "@type"

            if label not in nodes_json[source]:
                nodes_json[source][label] = []

            if self._looks_like_uri(target):
                value = {
                    "@id": target
                }
            else:
                value = target

            nodes_json[source][label].append(
                value
            )

        for node in nodes_json.values():
            data["@graph"].append(node)

        with open(output_file, "w") as f:
            json.dump(
                data,
                f,
                indent=4
            )

    def _looks_like_uri(self, value):
        """
        Determines whether a string appears to be a URI.

        A value is considered a URI if it starts with
        'http://' or 'https://'.

        Args:
            value (str): Value to check.

        Returns:
            bool: True if the value appears to be a URI,
            otherwise False.
        """

        return (
            value.startswith("http://")
            or value.startswith("https://")
        )