"""
Display CSE-KG 2.0 graph structure as nodes and edges
Shows the actual structure that would be extracted from queries
"""

import json
from pathlib import Path


def display_graph_structure():
    """Display the graph structure clearly"""
    print("="*80)
    print("CSE-KG 2.0 GRAPH STRUCTURE: NODES AND EDGES")
    print("="*80)
    
    # Load the structure
    structure_file = Path('cse_kg_graph_structure_example.json')
    if structure_file.exists():
        with open(structure_file, 'r', encoding='utf-8') as f:
            structure = json.load(f)
    else:
        # Create example structure
        structure = {
            "nodes": [
                {"id": "http://cse.ckcest.cn/cskg/recursion", "label": "Recursion", "type": "Concept"},
                {"id": "http://cse.ckcest.cn/cskg/base_case", "label": "Base Case", "type": "Concept"},
                {"id": "http://cse.ckcest.cn/cskg/functions", "label": "Functions", "type": "Concept"},
                {"id": "http://cse.ckcest.cn/cskg/linked_list", "label": "Linked List", "type": "Concept"},
                {"id": "http://cse.ckcest.cn/cskg/node", "label": "Node", "type": "Concept"},
                {"id": "http://cse.ckcest.cn/cskg/quicksort", "label": "Quicksort", "type": "Method"},
                {"id": "http://cse.ckcest.cn/cskg/sorting", "label": "Sorting", "type": "Task"}
            ],
            "edges": [
                {"source": "http://cse.ckcest.cn/cskg/recursion", "target": "http://cse.ckcest.cn/cskg/functions", "relation": "requiresKnowledge"},
                {"source": "http://cse.ckcest.cn/cskg/recursion", "target": "http://cse.ckcest.cn/cskg/base_case", "relation": "requiresKnowledge"},
                {"source": "http://cse.ckcest.cn/cskg/linked_list", "target": "http://cse.ckcest.cn/cskg/node", "relation": "requiresKnowledge"},
                {"source": "http://cse.ckcest.cn/cskg/quicksort", "target": "http://cse.ckcest.cn/cskg/sorting", "relation": "solvesTask"},
                {"source": "http://cse.ckcest.cn/cskg/recursion", "target": "http://cse.ckcest.cn/cskg/linked_list", "relation": "relatedTo"}
            ]
        }
    
    nodes = structure.get('nodes', [])
    edges = structure.get('edges', [])
    
    # Display nodes
    print("\n" + "="*80)
    print("NODES (Entities in the Graph)")
    print("="*80)
    print(f"\nTotal Nodes: {len(nodes)}\n")
    
    for i, node in enumerate(nodes, 1):
        print(f"{i}. Node ID: {node['id']}")
        print(f"   Label: {node['label']}")
        print(f"   Type: {node['type']}")
        print()
    
    # Display edges
    print("="*80)
    print("EDGES (Relationships in the Graph)")
    print("="*80)
    print(f"\nTotal Edges: {len(edges)}\n")
    
    for i, edge in enumerate(edges, 1):
        # Find source and target labels
        source_node = next((n for n in nodes if n['id'] == edge['source']), None)
        target_node = next((n for n in nodes if n['id'] == edge['target']), None)
        
        source_label = source_node['label'] if source_node else edge['source'].split('/')[-1]
        target_label = target_node['label'] if target_node else edge['target'].split('/')[-1]
        
        print(f"{i}. Edge: {source_label} --[{edge['relation']}]--> {target_label}")
        print(f"   Source: {edge['source']}")
        print(f"   Target: {edge['target']}")
        print(f"   Relation Type: {edge['relation']}")
        print()
    
    # Graph visualization
    print("="*80)
    print("GRAPH VISUALIZATION (Node -> Edge -> Node)")
    print("="*80)
    print()
    
    # Build adjacency list
    adjacency = {}
    for edge in edges:
        source_node = next((n for n in nodes if n['id'] == edge['source']), None)
        target_node = next((n for n in nodes if n['id'] == edge['target']), None)
        
        if source_node and target_node:
            source_label = source_node['label']
            target_label = target_node['label']
            
            if source_label not in adjacency:
                adjacency[source_label] = []
            adjacency[source_label].append((target_label, edge['relation']))
    
    # Display graph
    for node in nodes:
        node_label = node['label']
        if node_label in adjacency:
            print(f"{node_label} ({node['type']})")
            for target, relation in adjacency[node_label]:
                print(f"  |--[{relation}]--> {target}")
            print()
    
    # Statistics
    print("="*80)
    print("GRAPH STATISTICS")
    print("="*80)
    
    # Node types
    node_types = {}
    for node in nodes:
        node_type = node['type']
        node_types[node_type] = node_types.get(node_type, 0) + 1
    
    print(f"\nNode Types:")
    for node_type, count in node_types.items():
        print(f"  - {node_type}: {count} nodes")
    
    # Edge types
    edge_types = {}
    for edge in edges:
        edge_type = edge['relation']
        edge_types[edge_type] = edge_types.get(edge_type, 0) + 1
    
    print(f"\nEdge Types:")
    for edge_type, count in edge_types.items():
        print(f"  - {edge_type}: {count} edges")
    
    # Node degrees
    node_degrees = {}
    for edge in edges:
        source_node = next((n for n in nodes if n['id'] == edge['source']), None)
        target_node = next((n for n in nodes if n['id'] == edge['target']), None)
        
        if source_node:
            source_label = source_node['label']
            node_degrees[source_label] = node_degrees.get(source_label, 0) + 1
        if target_node:
            target_label = target_node['label']
            node_degrees[target_label] = node_degrees.get(target_label, 0) + 1
    
    if node_degrees:
        print(f"\nNode Degrees (number of connections):")
        for node_label, degree in sorted(node_degrees.items(), key=lambda x: x[1], reverse=True):
            print(f"  - {node_label}: {degree} connections")
    
    # Show as JSON structure
    print("\n" + "="*80)
    print("JSON STRUCTURE (for programmatic access)")
    print("="*80)
    print("\nNodes format:")
    print(json.dumps(nodes[0], indent=2))
    print("\nEdges format:")
    print(json.dumps(edges[0], indent=2))
    
    print("\n" + "="*80)
    print("HOW TO QUERY THIS STRUCTURE")
    print("="*80)
    print("\nWhen querying CSE-KG 2.0, you get:")
    print("1. Nodes: Concepts, Methods, Tasks, Materials")
    print("2. Edges: Relationships between nodes (requiresKnowledge, usesMethod, etc.)")
    print("\nThis structure enables:")
    print("- Finding prerequisites (follow requiresKnowledge edges)")
    print("- Finding related concepts (follow relatedTo edges)")
    print("- Finding methods for tasks (follow solvesTask edges)")
    print("- Building learning paths (traverse the graph)")
    print("="*80)


if __name__ == "__main__":
    display_graph_structure()















