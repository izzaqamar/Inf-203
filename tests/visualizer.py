import os
import sys

import networkx as nx
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from graph_project.jsonLD_parser import jsonLD_parser

file_path = os.path.join(
    os.path.dirname(__file__), "linked-data-intro-context.json"
)  #  JSON-LD file


parser = jsonLD_parser()
graph = parser.load_jsonld(file_path)


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


plt.figure(figsize=(14, 10))
pos = nx.spring_layout(G, k=1.5, seed=42)
nx.draw(
    G,
    pos,
    with_labels=True,
    arrows=True,
    node_size=2000,
    font_size=8,
    arrowsize=15
)
nx.draw_networkx_edge_labels(
    G,
    pos,
    edge_labels=nx.get_edge_attributes(G, "label"),
    font_size=7
)

plt.tight_layout()
plt.show()
print(list(G.edges(data=True)))