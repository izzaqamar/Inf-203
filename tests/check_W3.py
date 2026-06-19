import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "src"))

sys.path.insert(0, SRC_DIR)

from graph_project.jsonLD_parser import JsonLD_parser
from graph_project.OntologyTransformer import OntologyTransformer


def main():
    """
    Runs a simple test for Task 11.

    The script loads a JSON-LD source graph, applies the mappings
    from the alignment file, and exports the transformed graph as
    a new JSON-LD file.

    It also prints basic information before and after the
    transformation, so the result can be checked in the terminal.
    """

    # Input source graph
    source_file = os.path.abspath(
        os.path.join(BASE_DIR, "..", "tests", "use_case_Inf203.jsonld")
    )

    PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, ".."))

    alignment_file = os.path.join(PROJECT_ROOT, "src", "data", "alignment.json")
    output_file = os.path.join(
        PROJECT_ROOT, "src", "output", "transformed_graph.jsonld"
    )

    print("Source file:")
    print(source_file)
    print("Exists:", os.path.exists(source_file))

    print("\nAlignment file:")
    print(alignment_file)
    print("Exists:", os.path.exists(alignment_file))

    if not os.path.exists(source_file):
        print("\nERROR: Source file was not found.")
        return

    if not os.path.exists(alignment_file):
        print("\nERROR: Alignment file was not found.")
        return

    # Load source graph
    print("\nLoading source graph...")

    parser = JsonLD_parser()
    source_graph = parser.load_jsonld(source_file, False)

    print("\nSource graph loaded.")
    print(f"Nodes: {len(source_graph.nodes)}")
    print(f"Edges: {len(source_graph.edges)}")

    print("\nOriginal sample edges:")
    for edge in source_graph.edges[:10]:
        print(f"{edge.source.label} " f"--{edge.label}--> " f"{edge.target.label}")

    # Transform graph
    transformer = OntologyTransformer()

    print("\nTransforming graph...")

    transformed_graph = transformer.transform(source_graph, alignment_file)

    print("\nTransformation complete.")
    print(f"Nodes: {len(transformed_graph.nodes)}")
    print(f"Edges: {len(transformed_graph.edges)}")

    print("\nTransformed sample edges:")
    for edge in transformed_graph.edges[:10]:
        print(f"{edge.source.label} " f"--{edge.label}--> " f"{edge.target.label}")

    # Export transformed graph
    print("\nExporting graph...")

    transformer.export_jsonld(transformed_graph, output_file)

    print("\nDone.")
    print("Output file:")
    print(output_file)


if __name__ == "__main__":
    main()
