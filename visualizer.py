"""
Needs more comments
"""


import networkx as nx
#pip install networkx
import matplotlib.pyplot as plt
from jsonLD_parser import load_jsonld

graph = load_jsonld("test_data\\linked-data-intro-context.json")

G = nx.DiGraph()

def short_label(x):
    # Helper function to remove the left part of : "example-abox:NANOTEXNOLOGY_2025"
    if x is None:
        return None
    return x.split(":")[-1]

for edge in graph.edges:
    G.add_edge(
        short_label(edge.source.label),
        short_label(edge.target.label),
        label=edge.label
    )

pos = nx.spring_layout(G)

nx.draw(
    G,
    pos,
    with_labels=True,
    arrows=True
)

nx.draw_networkx_edge_labels(
    G,
    pos,
    edge_labels=nx.get_edge_attributes(G, "label")
)



plt.show()
print(list(G.edges(data=True)))