"""
Analyze CSE-KG downloaded graph statistics
Count nodes, edges, and structure
"""

from pathlib import Path
import json
import pickle

def analyze_local_graph():
    """Analyze locally downloaded CSE-KG graph"""
    print("="*60)
    print("CSE-KG Downloaded Graph Analysis")
    print("="*60)
    
    # Check for local graph
    local_graph_pkl = Path("data/cse_kg_local/graph.pkl")
    local_graph_json = Path("data/cse_kg_local/graph.json")
    
    if local_graph_pkl.exists():
        try:
            import networkx as nx
            with open(local_graph_pkl, 'rb') as f:
                G = pickle.load(f)
            
            print(f"\n[OK] Local NetworkX Graph Found:")
            print(f"   Nodes: {G.number_of_nodes()}")
            print(f"   Edges: {G.number_of_edges()}")
            print(f"   Density: {nx.density(G):.4f}")
            print(f"   Average Degree: {sum(dict(G.degree()).values()) / G.number_of_nodes():.2f}")
            
            # Count by attributes
            if G.number_of_nodes() > 0:
                print("\n   Node Categories:")
                categories = {}
                for node in G.nodes():
                    cat = G.nodes[node].get('type', 'unknown')
                    categories[cat] = categories.get(cat, 0) + 1
                for cat, count in sorted(categories.items()):
                    print(f"     {cat}: {count}")
                
                print("\n   Edge Relations:")
                relations = {}
                for u, v in G.edges():
                    rel = G[u][v].get('relation', 'unknown')
                    relations[rel] = relations.get(rel, 0) + 1
                for rel, count in sorted(relations.items(), key=lambda x: -x[1]):
                    print(f"     {rel}: {count}")
        except Exception as e:
            print(f"\n[ERROR] Error loading NetworkX graph: {e}")
    
    if local_graph_json.exists():
        try:
            with open(local_graph_json, 'r', encoding='utf-8') as f:
                graph_data = json.load(f)
            
            print(f"\n[OK] Local JSON Graph Found:")
            print(f"   Nodes: {len(graph_data.get('nodes', []))}")
            print(f"   Edges: {len(graph_data.get('edges', []))}")
        except Exception as e:
            print(f"\n[ERROR] Error loading JSON graph: {e}")
    
    # Check TTL files (actual downloaded data)
    ttl_dir = Path("data/cse_kg_full/extracted/cskg")
    if ttl_dir.exists():
        ttl_files = list(ttl_dir.glob("cskg_*.ttl"))
        print(f"\n[OK] TTL Files (RDF Triples) Found:")
        print(f"   Total TTL files: {len(ttl_files)}")
        
        # Sample one file to count triples
        if ttl_files:
            sample_file = ttl_files[0]
            try:
                with open(sample_file, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()
                    # Count triples (statements starting with cskg:)
                    triple_lines = [l for l in lines if 'cskg:' in l and 'a cskg-ont:' in l]
                    print(f"   Sample file ({sample_file.name}):")
                    print(f"     Total lines: {len(lines):,}")
                    print(f"     Estimated triples: ~{len(triple_lines):,}")
                    print(f"     Estimated total triples (all files): ~{len(triple_lines) * len(ttl_files):,}")
            except Exception as e:
                print(f"   Error reading sample file: {e}")

def analyze_visualization_graph():
    """Analyze the visualization graph structure"""
    print("\n" + "="*60)
    print("Visualization Graph Analysis")
    print("="*60)
    
    try:
        from visualize_cse_kg import create_cse_kg_visualization
        G, node_categories = create_cse_kg_visualization()
        
        print(f"\n[OK] Visualization Graph Created:")
        print(f"   Nodes: {G.number_of_nodes()}")
        print(f"   Edges: {G.number_of_edges()}")
        
        print("\n   Node Categories:")
        categories = {}
        for node in G.nodes():
            cat = G.nodes[node].get('category', 'unknown')
            categories[cat] = categories.get(cat, 0) + 1
        for cat, count in sorted(categories.items()):
            print(f"     {cat}: {count}")
        
        print("\n   Edge Relations:")
        relations = {}
        for u, v in G.edges():
            rel = G[u][v].get('relation', 'unknown')
            relations[rel] = relations.get(rel, 0) + 1
        for rel, count in sorted(relations.items(), key=lambda x: -x[1]):
            print(f"     {rel}: {count}")
    except Exception as e:
        print(f"\n[ERROR] Error creating visualization graph: {e}")

if __name__ == "__main__":
    analyze_local_graph()
    analyze_visualization_graph()
    
    print("\n" + "="*60)
    print("Visualization Method:")
    print("="*60)
    print("""
The visualizations are created using:

1. NetworkX: Creates graph structure
   - Nodes represent concepts/methods/tasks
   - Edges represent relationships (prerequisite, uses, etc.)

2. Matplotlib: Visual rendering
   - Hierarchical layout: Nodes positioned by level
   - Spring layout: Force-directed positioning
   - Subgraph layout: Focused domain view

3. Layout Algorithms:
   - Hierarchical: Groups nodes by level, arranges horizontally
   - Spring: Uses force-directed algorithm (Fruchterman-Reingold)
   - Circular: Places nodes in a circle for subgraphs

4. Visual Elements:
   - Node colors: Different colors for concepts/methods/tasks
   - Edge colors: Different colors for relation types
   - Labels: Node names and edge labels
   - Legends: Explain colors and symbols
    """)

