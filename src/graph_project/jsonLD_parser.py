import json
from .Graph import Graph


class JsonLD_parser:
    def load_jsonld(self, file_path, remove_duplicates):
        """
        Loads a JSON-LD file, converts it into a graph and returns the graph.

        Args:
            file_path (str): The path to the JSON-LD file to be loaded.
            remove_duplicates (bool): A flag indicating whether to accept duplicate triples.

        This function:
        - Reads the JSON-LD file
        - Extracts triples (subject, predicate, object) from the JSON structure
        - Builds a graph using the extracted triples
        - Returns the constructed graph

        Possible improvements:
        - Validate / normalize the triples
        - In case that node_id becomes "none", unrelated nodes could merge

        """
        
        graph = Graph()

        
        triples_list = []
        triples_set = set()  

        # Loads the JSON file
        with open(file_path, "r") as f:
            data = json.load(f)

        def extract(obj, subject=None):
            """
            Recursively extracts triples from the JSON object and adds them to the triples list.

            Args:
                obj: The current JSON object (can be a dict, list, or literal value).
                subject: The subject node ID for the current context.
            """

            if isinstance(obj, dict):
                # case 1: obj is a dictionary

                node_id = obj.get("@id", subject)
                # if no @id is found, we reuse parent identity

                for key, value in obj.items():

                    # for keys
                    if key == "@id":
                        # we have already used this
                        continue
                    if key == "@type":
                        # @type can be a list or a single string
                        if isinstance(value, list):
                            for t in value:
                                if remove_duplicates:
                                    triples_list.append((node_id, "type", t))
                                else:
                                    triples_set.add((node_id, "type", t))
                        else:
                            if remove_duplicates:
                                triples_list.append((node_id, "type", value))
                            else:
                                triples_set.add((node_id, "type", value))
                        continue

                    # case 1.1 for values
                    if isinstance(value, dict):
                        # recursivly extracts the nested dictionary
                        obj_id = value.get("@id")
                        if obj_id is not None:
                            # if @id is not present, then obj_id will get a "none" value
                            if remove_duplicates:
                                triples_list.append((node_id, key, obj_id))
                            else:
                                triples_set.add((node_id, key, obj_id))
                            extract(value, obj_id)
                        else:
                            extract(value, node_id)

                    # case 1.2 for lists
                    elif isinstance(value, list):
                        for item in value:

                            if isinstance(item, dict):
                                item_id = item.get("@id")

                                if item_id is not None:
                                    # if @id is not present, then item_id will get a "none" value
                                    if remove_duplicates:
                                        triples_list.append((node_id, key, item_id))
                                    else:
                                        triples_set.add((node_id, key, item_id))
                                    extract(item, item_id)
                                else:
                                    extract(item, node_id)
                            else:
                                if remove_duplicates:
                                    triples_list.append((node_id, key, str(item)))
                                else:
                                    triples_set.add((node_id, key, str(item)))

                    # case 1.3 for litreal values
                    else:
                        if remove_duplicates:
                            triples_list.append((node_id, key, str(value)))
                        else:
                            triples_set.add((node_id, key, str(value)))

                return node_id

            elif isinstance(obj, list):
                for item in obj:
                    extract(item, subject)

            else:
                # case 3: obj is a literal values
                if remove_duplicates:
                    triples_list.append((subject, "value", str(obj)))
                else:
                    triples_set.add((subject, "value", str(obj)))

        # Extract data
        extract(data)

        
        if remove_duplicates:
            triples = triples_list
        else:
            triples = list(triples_set)

        # Build the graph from the triples
        for s, p, o in triples:
            # for each triple, we add two nodes and one edge to the graph
            # s is the subject, p is the predicate (relationship for us normal people), o is the object
            graph.add_node(s)
            graph.add_edge(p, s, o)
            graph.add_node(o)

        # return
        return graph
