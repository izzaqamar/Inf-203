"""
Pytest for the JsonLD_parser class

Uses the existing file tests/linked-data-intro-context.json
"""
import os
import sys

# UPDATE IF MOVED FROM src/tests/pytests
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "src"))
sys.path.insert(0, BASE_DIR)

from graph_project.jsonLD_parser import JsonLD_parser

# The data is in  tests but the test file is in tests/pytests/
file_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "linked-data-intro-context.json")
)


def test_jsonld_parser_root_gets_type_edge():
    """
    The root node (ISSON25) should get a 'type' edge to schema:EducationEvent
    """
    parser = JsonLD_parser()
    graph = parser.load_jsonld(file_path, remove_duplicates=False)

    root = graph.nodes["example-abox:ISSON25"]
    type_targets = [e.target.label for e in root.outgoing if e.label == "type"]
    assert "schema:EducationEvent" in type_targets


def test_jsonld_parser_nested_object_in_list():
    """
    schema:performer is a list of 3 nested objects, so the root node should get 3 separate schema:performer edges, one per performer [or one per-former hehe ;) ]
    """
    parser = JsonLD_parser()
    graph = parser.load_jsonld(file_path, remove_duplicates=False)

    root = graph.nodes["example-abox:ISSON25"]
    performer_targets = [e.target.label for e in root.outgoing if e.label == "schema:performer"]

    assert "example-abox:Halliru_Ibrahim" in performer_targets
    assert "example-abox:Argiris_Laskarakis" in performer_targets
    assert "example-abox:Stratos_Saliakas" in performer_targets
    assert len(performer_targets) == 3


def test_jsonld_parser_nested_single_object():
    """
    schema:superEvent is a single nested object (not a list)
    Checks 
        1. root gets one edge (schema:superEvent)
        2. the nested object gets its own type edge (BusinessEvent)
    """
    parser = JsonLD_parser()
    graph = parser.load_jsonld(file_path, remove_duplicates=False)
    root = graph.nodes["example-abox:ISSON25"]

    super_event_targets = []
    for e in root.outgoing:
        if e.label == "schema:superEvent":
            super_event_targets.append(e.target.label)
    assert super_event_targets == ["example-abox:NANOTEXNOLOGY_2025"]

    super_event_node = graph.nodes["example-abox:NANOTEXNOLOGY_2025"]
    type_targets = []
    for e in super_event_node.outgoing:
        if e.label == "type":
            type_targets.append(e.target.label)
    assert "schema:BusinessEvent" in type_targets


def test_jsonld_parser_node_the_same():
    """
    'Argiris_Laskarakis' appears twice in the source file 
        1. A performer
        2. The organizer of the super event 
    The parser should treat both references as the SAME node, not create two separate nodes.
    """
    parser = JsonLD_parser()
    graph = parser.load_jsonld(file_path, remove_duplicates=False)

    # Only one node should exist for this label
    assert "example-abox:Argiris_Laskarakis" in graph.nodes
    shared_node = graph.nodes["example-abox:Argiris_Laskarakis"]

    # It should have incoming edges from BOTH the performer and organizer relations
    incoming_labels = []
    for e in shared_node.incoming:
        incoming_labels.append(e.label)
    assert "schema:performer" in incoming_labels
    assert "schema:organizer" in incoming_labels


def test_jsonld_parser_remove_duplicates_false_keeps_all_triples():
    """
    With remove_duplicates=False, every real triple extracted from the file should become an edge. 
    @context is namespace metadata (not graph data) so it is skipped and does NOT count toward this total.
    """
    parser = JsonLD_parser()
    graph = parser.load_jsonld(file_path, remove_duplicates=False)

    # traced by hand against the parser logic: 12 real triples in this fixture
    # (14 total minus the 2 @context entries, which are skipped)
    assert len(graph.edges) == 12


def test_jsonld_parser_context_is_not_added_to_graph():
    """
    @context should be skipped entirely: it must not appear as an edge label,
    and the namespace prefix values (the URIs) must not appear as node labels.
    """
    parser = JsonLD_parser()
    graph = parser.load_jsonld(file_path, remove_duplicates=False)

    root = graph.nodes["example-abox:ISSON25"]

    edge_labels = []
    for e in root.outgoing:
        edge_labels.append(e.label)

    assert "example-abox" not in edge_labels
    assert "schema" not in edge_labels
    assert "https://schema.org/" not in graph.nodes
    assert "https://www.nanotexnology.com/index.php/isson/data#" not in graph.nodes
