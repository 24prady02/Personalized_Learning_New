"""
Example: How to use the downloaded CSE-KG 2.0 full dataset
"""

import json
import pickle
from pathlib import Path
import networkx as nx

def load_cse_kg_full():
    """Load the full CSE-KG 2.0 dataset"""
    data_dir = Path("data/cse_kg_full")
    
    print("="*80)
    print("LOADING CSE-KG 2.0 FULL DATASET")
    print("="*80)
    
    # Load concepts
    concepts_file = data_dir / "concepts.json"
    if concepts_file.exists():
        with open(concepts_file, 'r', encoding='utf-8') as f:
            concepts = json.load(f)
        print(f"  Loaded {len(concepts)} concepts")
    else:
        print("  [ERROR] concepts.json not found")
        return None
    
    # Load relations
    relations_file = data_dir / "relations.json"
    if relations_file.exists():
        with open(relations_file, 'r', encoding='utf-8') as f:
            relations = json.load(f)
        print(f"  Loaded {len(relations)} relations")
    else:
        print("  [ERROR] relations.json not found")
        return None
    
    # Load graph
    graph_file = data_dir / "graph.pkl"
    if graph_file.exists():
        with open(graph_file, 'rb') as f:
            graph = pickle.load(f)
        print(f"  Loaded graph: {len(graph.nodes())} nodes, {len(graph.edges())} edges")
    else:
        print("  [WARNING] graph.pkl not found, creating from concepts and relations")
        graph = nx.DiGraph()
        for concept_id, concept_data in concepts.items():
            graph.add_node(concept_id, **concept_data)
        for rel in relations:
            graph.add_edge(rel['source'], rel['target'], relation=rel['relation'])
    
    # Load keyword index
    keyword_file = data_dir / "keyword_index.json"
    if keyword_file.exists():
        with open(keyword_file, 'r', encoding='utf-8') as f:
            keyword_index = json.load(f)
        print(f"  Loaded {len(keyword_index)} keyword mappings")
    else:
        keyword_index = {}
    
    return {
        'concepts': concepts,
        'relations': relations,
        'graph': graph,
        'keyword_index': keyword_index
    }


def example_1_search_concept(cse_kg, query):
    """Example 1: Search for a concept by name"""
    print(f"\n{'='*80}")
    print(f"EXAMPLE 1: Searching for concept '{query}'")
    print("="*80)
    
    concepts = cse_kg['concepts']
    query_lower = query.lower()
    
    # Search by label
    matches = []
    for concept_id, concept_data in concepts.items():
        label = concept_data.get('label', '').lower()
        if query_lower in label or query_lower in concept_id.lower():
            matches.append(concept_data)
    
    print(f"Found {len(matches)} matching concepts:")
    for match in matches[:5]:
        print(f"  - {match['label']} ({match['type']})")
        print(f"    ID: {match['id']}")
        if match.get('description'):
            print(f"    Description: {match['description'][:100]}...")
    
    return matches


def example_2_get_related_concepts(cse_kg, concept_id):
    """Example 2: Get concepts related to a given concept"""
    print(f"\n{'='*80}")
    print(f"EXAMPLE 2: Getting concepts related to '{concept_id}'")
    print("="*80)
    
    graph = cse_kg['graph']
    concepts = cse_kg['concepts']
    
    if concept_id not in graph:
        print(f"  [ERROR] Concept '{concept_id}' not found in graph")
        return []
    
    # Get neighbors (related concepts)
    neighbors = list(graph.neighbors(concept_id))
    print(f"Found {len(neighbors)} related concepts:")
    
    for neighbor_id in neighbors[:10]:
        neighbor_data = concepts.get(neighbor_id, {})
        edge_data = graph.get_edge_data(concept_id, neighbor_id, {})
        relation = edge_data.get('relation', 'relatedTo')
        
        print(f"  - {neighbor_data.get('label', neighbor_id)}")
        print(f"    Relation: {relation}")
    
    return neighbors


def example_3_search_by_keywords(cse_kg, keywords):
    """Example 3: Search concepts by keywords"""
    print(f"\n{'='*80}")
    print(f"EXAMPLE 3: Searching by keywords: {keywords}")
    print("="*80)
    
    keyword_index = cse_kg['keyword_index']
    concepts = cse_kg['concepts']
    
    # Find concepts matching keywords
    concept_scores = {}
    for keyword in keywords:
        keyword_lower = keyword.lower()
        if keyword_lower in keyword_index:
            for concept_id in keyword_index[keyword_lower]:
                concept_scores[concept_id] = concept_scores.get(concept_id, 0) + 1
    
    # Sort by score
    ranked = sorted(concept_scores.items(), key=lambda x: x[1], reverse=True)
    
    print(f"Found {len(ranked)} matching concepts:")
    for concept_id, score in ranked[:10]:
        concept_data = concepts.get(concept_id, {})
        print(f"  - {concept_data.get('label', concept_id)} (score: {score})")
    
    return ranked


def example_4_get_concept_path(cse_kg, source_id, target_id):
    """Example 4: Find path between two concepts"""
    print(f"\n{'='*80}")
    print(f"EXAMPLE 4: Finding path from '{source_id}' to '{target_id}'")
    print("="*80)
    
    graph = cse_kg['graph']
    concepts = cse_kg['concepts']
    
    if source_id not in graph or target_id not in graph:
        print("  [ERROR] One or both concepts not found in graph")
        return None
    
    try:
        # Find shortest path
        path = nx.shortest_path(graph, source_id, target_id)
        
        print(f"Found path with {len(path)-1} steps:")
        for i, concept_id in enumerate(path):
            concept_data = concepts.get(concept_id, {})
            print(f"  {i+1}. {concept_data.get('label', concept_id)}")
            
            if i < len(path) - 1:
                edge_data = graph.get_edge_data(concept_id, path[i+1], {})
                relation = edge_data.get('relation', 'relatedTo')
                print(f"      --[{relation}]-->")
        
        return path
    except nx.NetworkXNoPath:
        print("  [INFO] No path found between these concepts")
        return None


def example_5_get_concept_info(cse_kg, concept_id):
    """Example 5: Get detailed information about a concept"""
    print(f"\n{'='*80}")
    print(f"EXAMPLE 5: Getting detailed info for '{concept_id}'")
    print("="*80)
    
    concepts = cse_kg['concepts']
    graph = cse_kg['graph']
    
    if concept_id not in concepts:
        print(f"  [ERROR] Concept '{concept_id}' not found")
        return None
    
    concept_data = concepts[concept_id]
    
    print(f"Concept: {concept_data['label']}")
    print(f"  ID: {concept_data['id']}")
    print(f"  Type: {concept_data['type']}")
    print(f"  URI: {concept_data['uri']}")
    if concept_data.get('description'):
        print(f"  Description: {concept_data['description']}")
    
    # Get statistics
    if concept_id in graph:
        in_degree = graph.in_degree(concept_id)
        out_degree = graph.out_degree(concept_id)
        print(f"  Incoming relations: {in_degree}")
        print(f"  Outgoing relations: {out_degree}")
    
    return concept_data


def main():
    """Main function demonstrating usage"""
    print("\n" + "="*80)
    print("CSE-KG 2.0 FULL DATASET - USAGE EXAMPLES")
    print("="*80)
    
    # Load dataset
    cse_kg = load_cse_kg_full()
    if not cse_kg:
        print("\n[ERROR] Could not load CSE-KG 2.0 dataset")
        print("Please run: python download_cse_kg_zip.py")
        return
    
    # Example 1: Search for a concept
    example_1_search_concept(cse_kg, "recursion")
    
    # Example 2: Get related concepts
    if "recursion" in cse_kg['concepts']:
        example_2_get_related_concepts(cse_kg, "recursion")
    
    # Example 3: Search by keywords
    example_3_search_by_keywords(cse_kg, ["algorithm", "sort"])
    
    # Example 4: Find path between concepts
    if "recursion" in cse_kg['concepts'] and "tree" in cse_kg['concepts']:
        example_4_get_concept_path(cse_kg, "recursion", "tree")
    
    # Example 5: Get concept info
    if "recursion" in cse_kg['concepts']:
        example_5_get_concept_info(cse_kg, "recursion")
    
    print("\n" + "="*80)
    print("EXAMPLES COMPLETE!")
    print("="*80)
    print("\nYou can now use this dataset in your personalized learning system!")


if __name__ == "__main__":
    main()















