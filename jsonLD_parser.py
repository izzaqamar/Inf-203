"""
Something that can parse JSON-LD and extract relevant information from it
Opens the JSON-LD file, extracts the data as triples, and then adds the nodes and edges to the graph.
Returns the graph

#Possible improvements:
- No handeling of duplicate triples, which could lead to multiple identical edges in the graph
- Validate / normalize the triples
- In case that node_id becomes "none", unrelated nodes could merge
    Danger: 
        #Creates a graph object
        graph = Graph()

        # Creates a list of facts (triples)
        triples = []

"""


import json
from incidence_list_classes import Node, Edge, Graph

def load_jsonld(file_path):
    # Creates a graph object
    graph = Graph()

    # Creates a list of facts (triples)
    triples = []


    """
    #Test data
    file__path = 'test_data\\linked-data-intro-context.json'
    """

    # Loads the JSON file
    with open(file_path, 'r') as f:
        data = json.load(f)


    def extract(obj, subject=None):
        # This function extracts triples from the JSON file and adds it to the triples list.
        # It creates facts like Martin thought us from class

        if isinstance(obj, dict):
            #case 1: obj is a dictionary

            node_id = obj.get("@id", subject)
            #if no @id is found, we reuse parent identity

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
                    #recursivly extracts the nested dictionary
                    obj_id = value.get("@id")
                    if obj_id is not None:
                        #if @id is not present, then obj_id will get a "none" value
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
                                #if @id is not present, then item_id will get a "none" value
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
            #case 3: obj is a literal values
            triples.append((subject, "value", str(obj)))
            
    # Extract data 
    extract(data)

    # Buld the graph from the triples
    for s, p, o in triples:
        #for each triple, we add the nodes and edges to the graph
        #s is the subject, p is the predicate (relationship for us normal people), o is the object
        graph.add_node(s)
        graph.add_edge(p, s, o)
        graph.add_node(o)
    
    #return
    return graph
