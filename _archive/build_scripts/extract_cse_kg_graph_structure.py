"""
Extract CSE-KG 2.0 graph structure as nodes and edges
Queries the SPARQL endpoint and displays the actual graph structure
"""

import sys
import yaml
import json
from pathlib import Path
from collections import defaultdict

# Try to import SPARQLWrapper
try:
    from SPARQLWrapper import SPARQLWrapper, JSON
    SPARQL_AVAILABLE = True
except ImportError:
    SPARQL_AVAILABLE = False
    print("[WARNING] SPARQLWrapper not installed. Install with: pip install SPARQLWrapper")
    print("Showing graph structure from config and example queries only.")


def query_cse_kg(query, endpoint, use_cache=False):
    """Execute SPARQL query"""
    if not SPARQL_AVAILABLE:
        return []
    
    try:
        sparql = SPARQLWrapper(endpoint)
        sparql.setReturnFormat(JSON)
        sparql.setQuery(query)
        results = sparql.query().convert()
        return results['results']['bindings']
    except Exception as e:
        print(f"   [ERROR] Query failed: {e}")
        return []


def extract_graph_structure():
    """Extract nodes and edges from CSE-KG 2.0"""
    print("="*80)
    print("CSE-KG 2.0 GRAPH STRUCTURE EXTRACTION")
    print("="*80)
    
    # Load config
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    cse_kg_config = config.get('cse_kg', {})
    endpoint = cse_kg_config.get('sparql_endpoint', '')
    namespace = cse_kg_config.get('namespace', '')
    
    print(f"\nSPARQL Endpoint: {endpoint}")
    print(f"Namespace: {namespace}")
    
    if not SPARQL_AVAILABLE:
        print("\n[NOTE] Cannot query live endpoint without SPARQLWrapper")
        print("Showing example graph structure based on configuration...")
        show_example_structure(cse_kg_config)
        return
    
    # Extract nodes (concepts)
    print("\n" + "="*80)
    print("1. EXTRACTING NODES (Concepts)")
    print("="*80)
    
    nodes = []
    node_query = f"""
    PREFIX cskg: <{namespace}>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    
    SELECT DISTINCT ?concept ?label ?type WHERE {{
        ?concept rdf:type ?type .
        ?concept rdfs:label ?label .
        FILTER(STRSTARTS(STR(?type), STR(cskg:)))
    }}
    LIMIT 50
    """
    
    print("   Querying for concepts...")
    results = query_cse_kg(node_query, endpoint)
    
    if results:
        print(f"   [OK] Found {len(results)} concepts")
        for i, result in enumerate(results[:10], 1):
            concept_uri = result.get('concept', {}).get('value', '')
            label = result.get('label', {}).get('value', '')
            node_type = result.get('type', {}).get('value', '').split('/')[-1]
            
            node = {
                'id': concept_uri,
                'label': label,
                'type': node_type
            }
            nodes.append(node)
            print(f"   {i}. {label} ({node_type})")
            print(f"      URI: {concept_uri}")
    else:
        print("   [WARNING] No concepts found or query failed")
        print("   Showing example structure...")
        show_example_structure(cse_kg_config)
        return
    
    # Extract edges (relationships)
    print("\n" + "="*80)
    print("2. EXTRACTING EDGES (Relationships)")
    print("="*80)
    
    edges = []
    relation_types = cse_kg_config.get('relation_types', [])
    
    for relation_type in relation_types:
        print(f"\n   Querying {relation_type} relationships...")
        
        edge_query = f"""
        PREFIX cskg: <{namespace}>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        
        SELECT DISTINCT ?source ?sourceLabel ?target ?targetLabel WHERE {{
            ?source cskg:{relation_type} ?target .
            OPTIONAL {{ ?source rdfs:label ?sourceLabel . }}
            OPTIONAL {{ ?target rdfs:label ?targetLabel . }}
        }}
        LIMIT 20
        """
        
        results = query_cse_kg(edge_query, endpoint)
        
        if results:
            print(f"      [OK] Found {len(results)} {relation_type} relationships")
            for result in results[:5]:
                source_uri = result.get('source', {}).get('value', '')
                source_label = result.get('sourceLabel', {}).get('value', 'N/A')
                target_uri = result.get('target', {}).get('value', '')
                target_label = result.get('targetLabel', {}).get('value', 'N/A')
                
                edge = {
                    'source': source_uri,
                    'target': target_uri,
                    'relation': relation_type,
                    'source_label': source_label,
                    'target_label': target_label
                }
                edges.append(edge)
                print(f"      - {source_label} --[{relation_type}]--> {target_label}")
        else:
            print(f"      [WARNING] No {relation_type} relationships found")
    
    # Display graph structure
    print("\n" + "="*80)
    print("3. GRAPH STRUCTURE SUMMARY")
    print("="*80)
    
    print(f"\nNodes (Concepts): {len(nodes)}")
    print(f"Edges (Relationships): {len(edges)}")
    
    # Group edges by relation type
    edges_by_type = defaultdict(list)
    for edge in edges:
        edges_by_type[edge['relation']].append(edge)
    
    print(f"\nEdges by type:")
    for rel_type, rel_edges in edges_by_type.items():
        print(f"  - {rel_type}: {len(rel_edges)} edges")
    
    # Show sample subgraph
    print("\n" + "="*80)
    print("4. SAMPLE SUBGRAPH")
    print("="*80)
    
    if nodes and edges:
        # Find a concept with multiple relationships
        concept_edges = defaultdict(list)
        for edge in edges:
            concept_edges[edge['source']].append(edge)
        
        if concept_edges:
            sample_concept = list(concept_edges.keys())[0]
            sample_edges = concept_edges[sample_concept]
            
            # Find the node
            sample_node = next((n for n in nodes if n['id'] == sample_concept), None)
            
            if sample_node:
                print(f"\nConcept: {sample_node['label']} ({sample_node['type']})")
                print(f"URI: {sample_concept}")
                print(f"\nRelationships:")
                for edge in sample_edges[:5]:
                    print(f"  --[{edge['relation']}]--> {edge['target_label']}")
    
    # Save to JSON
    graph_structure = {
        'nodes': nodes[:50],  # Limit to 50 nodes
        'edges': edges[:100],  # Limit to 100 edges
        'metadata': {
            'total_nodes_found': len(nodes),
            'total_edges_found': len(edges),
            'endpoint': endpoint,
            'namespace': namespace
        }
    }
    
    output_file = Path('cse_kg_graph_structure.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(graph_structure, f, indent=2, ensure_ascii=False)
    
    print(f"\n[OK] Graph structure saved to: {output_file}")
    
    return graph_structure


def show_example_structure(cse_kg_config):
    """Show example graph structure when live querying is not available"""
    print("\n" + "="*80)
    print("EXAMPLE CSE-KG 2.0 GRAPH STRUCTURE")
    print("="*80)
    
    namespace = cse_kg_config.get('namespace', '')
    
    # Example nodes
    print("\n1. EXAMPLE NODES (Concepts)")
    example_nodes = [
        {"id": f"{namespace}recursion", "label": "Recursion", "type": "Concept"},
        {"id": f"{namespace}base_case", "label": "Base Case", "type": "Concept"},
        {"id": f"{namespace}functions", "label": "Functions", "type": "Concept"},
        {"id": f"{namespace}linked_list", "label": "Linked List", "type": "Concept"},
        {"id": f"{namespace}node", "label": "Node", "type": "Concept"},
        {"id": f"{namespace}quicksort", "label": "Quicksort", "type": "Method"},
        {"id": f"{namespace}sorting", "label": "Sorting", "type": "Task"},
    ]
    
    for node in example_nodes:
        print(f"   - {node['label']} ({node['type']})")
        print(f"     URI: {node['id']}")
    
    # Example edges
    print("\n2. EXAMPLE EDGES (Relationships)")
    example_edges = [
        {
            "source": f"{namespace}recursion",
            "target": f"{namespace}functions",
            "relation": "requiresKnowledge",
            "source_label": "Recursion",
            "target_label": "Functions"
        },
        {
            "source": f"{namespace}recursion",
            "target": f"{namespace}base_case",
            "relation": "requiresKnowledge",
            "source_label": "Recursion",
            "target_label": "Base Case"
        },
        {
            "source": f"{namespace}linked_list",
            "target": f"{namespace}node",
            "relation": "requiresKnowledge",
            "source_label": "Linked List",
            "target_label": "Node"
        },
        {
            "source": f"{namespace}quicksort",
            "target": f"{namespace}sorting",
            "relation": "solvesTask",
            "source_label": "Quicksort",
            "target_label": "Sorting"
        },
        {
            "source": f"{namespace}recursion",
            "target": f"{namespace}linked_list",
            "relation": "relatedTo",
            "source_label": "Recursion",
            "target_label": "Linked List"
        }
    ]
    
    for edge in example_edges:
        print(f"   {edge['source_label']} --[{edge['relation']}]--> {edge['target_label']}")
    
    # Graph visualization
    print("\n3. GRAPH VISUALIZATION")
    print("\n   Recursion")
    print("   |--[requiresKnowledge]--> Functions")
    print("   |--[requiresKnowledge]--> Base Case")
    print("   |--[relatedTo]--> Linked List")
    print("   |")
    print("   Linked List")
    print("   |--[requiresKnowledge]--> Node")
    print("   |")
    print("   Quicksort (Method)")
    print("   |--[solvesTask]--> Sorting (Task)")
    
    # Save example structure
    graph_structure = {
        'nodes': example_nodes,
        'edges': example_edges,
        'metadata': {
            'note': 'Example structure - not from live query',
            'namespace': namespace
        }
    }
    
    output_file = Path('cse_kg_graph_structure_example.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(graph_structure, f, indent=2, ensure_ascii=False)
    
    print(f"\n[OK] Example graph structure saved to: {output_file}")


def show_graph_statistics():
    """Show statistics about the graph structure"""
    print("\n" + "="*80)
    print("GRAPH STATISTICS")
    print("="*80)
    
    # Try to load extracted structure
    structure_file = Path('cse_kg_graph_structure.json')
    if not structure_file.exists():
        structure_file = Path('cse_kg_graph_structure_example.json')
    
    if structure_file.exists():
        with open(structure_file, 'r', encoding='utf-8') as f:
            structure = json.load(f)
        
        nodes = structure.get('nodes', [])
        edges = structure.get('edges', [])
        
        print(f"\nTotal Nodes: {len(nodes)}")
        print(f"Total Edges: {len(edges)}")
        
        # Node types
        node_types = defaultdict(int)
        for node in nodes:
            node_types[node.get('type', 'Unknown')] += 1
        
        print(f"\nNode Types:")
        for node_type, count in node_types.items():
            print(f"  - {node_type}: {count}")
        
        # Edge types
        edge_types = defaultdict(int)
        for edge in edges:
            edge_types[edge.get('relation', 'Unknown')] += 1
        
        print(f"\nEdge Types:")
        for edge_type, count in edge_types.items():
            print(f"  - {edge_type}: {count}")
        
        # Degree distribution
        node_degrees = defaultdict(int)
        for edge in edges:
            node_degrees[edge['source']] += 1
            node_degrees[edge['target']] += 1
        
        if node_degrees:
            max_degree = max(node_degrees.values())
            avg_degree = sum(node_degrees.values()) / len(node_degrees)
            print(f"\nNode Degrees:")
            print(f"  - Maximum: {max_degree}")
            print(f"  - Average: {avg_degree:.2f}")
    else:
        print("\n[WARNING] No graph structure file found")


def main():
    """Main execution"""
    print("\nExtracting CSE-KG 2.0 graph structure...")
    print("This will query the SPARQL endpoint and extract nodes and edges.\n")
    
    try:
        structure = extract_graph_structure()
        show_graph_statistics()
        
        print("\n" + "="*80)
        print("EXTRACTION COMPLETE")
        print("="*80)
        print("\nGraph structure saved as JSON file.")
        print("You can visualize it using NetworkX or other graph tools.")
        
    except KeyboardInterrupt:
        print("\n\n[WARNING] Interrupted by user")
    except Exception as e:
        print(f"\n\n[ERROR] Unexpected error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()















