"""
Enhance local CSE-KG graph with prerequisites from MOOCCubeX
"""

import json
import pickle
import networkx as nx
from pathlib import Path

def enhance_local_kg():
    """Add prerequisites to local CSE-KG graph"""
    
    # Load current graph
    graph_path = Path("data/cse_kg_local/graph.pkl")
    if not graph_path.exists():
        print("Error: graph.pkl not found")
        return
    
    print("Loading local graph...")
    with open(graph_path, 'rb') as f:
        graph = pickle.load(f)
    
    print(f"  Current: {len(graph.nodes())} nodes, {len(graph.edges())} edges")
    
    # MOOCCubeX prerequisites are in JSONL format (one JSON per line)
    # We'll use manual mapping instead for now
    print("\nUsing manual prerequisite mappings...")
    
    # Manual prerequisite mappings (common CS concepts)
    manual_prereqs = {
        "recursion": {
            "prerequisites": ["functions", "conditional_statements", "base_case"],
            "related": ["iteration", "loops", "tail_recursion", "stack"]
        },
        "arrays": {
            "prerequisites": ["variables", "loops", "indexing"],
            "related": ["lists", "dictionaries", "tuples"]
        },
        "functions": {
            "prerequisites": ["variables", "parameters"],
            "related": ["methods", "procedures", "call_stack"]
        },
        "object_oriented": {
            "prerequisites": ["functions", "classes", "variables"],
            "related": ["inheritance", "polymorphism", "encapsulation"]
        },
        "loops": {
            "prerequisites": ["conditional_statements", "variables"],
            "related": ["iteration", "recursion", "control_flow"]
        },
        "dictionaries": {
            "prerequisites": ["arrays", "key_value_pairs"],
            "related": ["hash_tables", "maps", "sets"]
        },
        "strings": {
            "prerequisites": ["variables", "arrays"],
            "related": ["text_processing", "regular_expressions"]
        },
        "variable_scope": {
            "prerequisites": ["variables", "functions"],
            "related": ["global_variables", "local_variables", "closures"]
        }
    }
    
    # Add prerequisites to graph
    added_edges = 0
    added_nodes = 0
    
    print("\nAdding prerequisites to graph...")
    
    for concept, prereq_data in manual_prereqs.items():
        # Ensure concept node exists
        if concept not in graph:
            graph.add_node(concept)
            added_nodes += 1
        
        # Add prerequisite edges
        for prereq in prereq_data.get("prerequisites", []):
            if prereq not in graph:
                graph.add_node(prereq)
                added_nodes += 1
            
            # Add edge: prereq -> concept (prereq is required for concept)
            if not graph.has_edge(prereq, concept):
                graph.add_edge(prereq, concept, relation="isPrerequisiteOf")
                added_edges += 1
        
        # Add related concept edges
        for related in prereq_data.get("related", []):
            if related not in graph:
                graph.add_node(related)
                added_nodes += 1
            
            # Add bidirectional related edge
            if not graph.has_edge(concept, related):
                graph.add_edge(concept, related, relation="relatedTo")
                added_edges += 1
            if not graph.has_edge(related, concept):
                graph.add_edge(related, concept, relation="relatedTo")
                added_edges += 1
    
    print(f"  Added {added_nodes} nodes, {added_edges} edges")
    print(f"  Final: {len(graph.nodes())} nodes, {len(graph.edges())} edges")
    
    # Save enhanced graph
    print("\nSaving enhanced graph...")
    with open(graph_path, 'wb') as f:
        pickle.dump(graph, f)
    
    print(f"  Saved to {graph_path}")
    
    # Verify prerequisites work
    print("\nVerifying prerequisites...")
    test_concept = "recursion"
    if test_concept in graph:
        prereqs = [n for n in graph.predecessors(test_concept) 
                  if graph.get_edge_data(n, test_concept, {}).get('relation', '').lower() in ['isprerequisiteof', 'prerequisite', 'requires']]
        print(f"  '{test_concept}' prerequisites: {prereqs}")
    
    print("\n[OK] Local KG enhanced with prerequisites!")

if __name__ == "__main__":
    enhance_local_kg()

