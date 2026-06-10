import json
from .incidence_list_classes import Node, Edge, Graph


def load_jsonld(file_path):
    """
    Loads a JSON-LD file, converts it into a graph and returns the graph.

    Args:
        file_path (str): The path to the JSON-LD file to be loaded.

    This function:
    - Reads the JSON-LD file
    - Extracts triples (subject, predicate, object) from the JSON structure
    - Builds a graph using the extracted triples
    - Returns the constructed graph

    Possible improvements:
    - No handling of duplicate triples, which could lead to multiple identical edges in the graph
    - Validate / normalize the triples
    - In case that node_id becomes "none", unrelated nodes could merge

    """
    # Creates a graph object
    graph = Graph()

    # Creates a list of facts (triples)
    triples = []

    # Loads the JSON file
    with open(file_path, "r") as f:
        data = json.load(f)

    def extract(obj, subject=None):
        # This function extracts triples from the JSON file and adds it to the triples list.
        # It creates facts like Martin thought us from class

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
                    triples.append((node_id, "type", value))
                    continue

                # case 1.1 for values
                if isinstance(value, dict):
                    # recursivly extracts the nested dictionary
                    obj_id = value.get("@id")
                    if obj_id is not None:
                        # if @id is not present, then obj_id will get a "none" value
                        triples.append((node_id, key, obj_id))
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
                                triples.append((node_id, key, item_id))
                                extract(item, item_id)
                            else:
                                extract(item, node_id)
                        else:
                            triples.append((node_id, key, str(item)))

                # case 1.3 for litreal values
                else:
                    triples.append((node_id, key, str(value)))

            return node_id

        elif isinstance(obj, list):
            for item in obj:
                extract(item, subject)

        else:
            # case 3: obj is a literal values
            triples.append((subject, "value", str(obj)))

    # Extract data
    extract(data)

    # Buld the graph from the triples
    for s, p, o in triples:
        # for each triple, we add two nodes and one edge to the graph
        # s is the subject, p is the predicate (relationship for us normal people), o is the object
        graph.add_node(s)
        graph.add_edge(p, s, o)
        graph.add_node(o)

    # return
    return graph
