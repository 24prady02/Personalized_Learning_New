"""
Visualize CSE-KG 2.0 Knowledge Graph Structure
Creates visualizations showing nodes, edges, and relationships
"""

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from matplotlib.patches import FancyBboxPatch
import json

def create_cse_kg_visualization():
    """Create a comprehensive visualization of CSE-KG 2.0 structure"""
    
    # Create a directed graph
    G = nx.DiGraph()
    
    # Define node categories and their colors
    node_categories = {
        'concept': '#4A90E2',      # Blue
        'method': '#50C878',       # Green
        'task': '#FF6B6B',         # Red
        'material': '#FFA500'      # Orange
    }
    
    # Add nodes with categories
    # Top-level concepts
    G.add_node('programming_fundamentals', category='concept', level=0)
    G.add_node('data_structures', category='concept', level=1)
    G.add_node('algorithms', category='concept', level=1)
    G.add_node('object_oriented_programming', category='concept', level=1)
    
    # Data Structures sub-concepts
    G.add_node('array', category='concept', level=2)
    G.add_node('linked_list', category='concept', level=2)
    G.add_node('tree', category='concept', level=2)
    G.add_node('graph', category='concept', level=2)
    G.add_node('stack', category='concept', level=2)
    G.add_node('queue', category='concept', level=2)
    
    # Linked List related concepts
    G.add_node('node', category='concept', level=3)
    G.add_node('pointer', category='concept', level=3)
    G.add_node('memory_management', category='concept', level=3)
    G.add_node('dynamic_allocation', category='concept', level=3)
    
    # Algorithms
    G.add_node('sorting', category='concept', level=2)
    G.add_node('searching', category='concept', level=2)
    G.add_node('recursion', category='concept', level=2)
    G.add_node('dynamic_programming', category='concept', level=2)
    
    # Recursion related
    G.add_node('base_case', category='concept', level=3)
    G.add_node('recursive_call', category='concept', level=3)
    G.add_node('call_stack', category='concept', level=3)
    
    # OOP concepts
    G.add_node('class', category='concept', level=2)
    G.add_node('object', category='concept', level=2)
    G.add_node('inheritance', category='concept', level=2)
    G.add_node('polymorphism', category='concept', level=2)
    G.add_node('encapsulation', category='concept', level=2)
    
    # Methods
    G.add_node('quicksort', category='method', level=2)
    G.add_node('binary_search', category='method', level=2)
    G.add_node('depth_first_search', category='method', level=2)
    G.add_node('breadth_first_search', category='method', level=2)
    
    # Tasks
    G.add_node('tree_traversal', category='task', level=2)
    G.add_node('path_finding', category='task', level=2)
    G.add_node('data_organization', category='task', level=2)
    
    # Add edges (relationships)
    # Hierarchical relationships
    G.add_edge('programming_fundamentals', 'data_structures', relation='contains')
    G.add_edge('programming_fundamentals', 'algorithms', relation='contains')
    G.add_edge('programming_fundamentals', 'object_oriented_programming', relation='contains')
    
    # Data structures hierarchy
    G.add_edge('data_structures', 'array', relation='contains')
    G.add_edge('data_structures', 'linked_list', relation='contains')
    G.add_edge('data_structures', 'tree', relation='contains')
    G.add_edge('data_structures', 'graph', relation='contains')
    G.add_edge('data_structures', 'stack', relation='contains')
    G.add_edge('data_structures', 'queue', relation='contains')
    
    # Linked list prerequisites
    G.add_edge('array', 'linked_list', relation='prerequisite')
    G.add_edge('pointer', 'linked_list', relation='prerequisite')
    G.add_edge('node', 'linked_list', relation='prerequisite')
    G.add_edge('memory_management', 'linked_list', relation='prerequisite')
    G.add_edge('dynamic_allocation', 'linked_list', relation='prerequisite')
    
    # Linked list relationships
    G.add_edge('linked_list', 'node', relation='uses')
    G.add_edge('linked_list', 'pointer', relation='uses')
    G.add_edge('linked_list', 'memory_management', relation='uses')
    
    # Algorithms hierarchy
    G.add_edge('algorithms', 'sorting', relation='contains')
    G.add_edge('algorithms', 'searching', relation='contains')
    G.add_edge('algorithms', 'recursion', relation='contains')
    G.add_edge('algorithms', 'dynamic_programming', relation='contains')
    
    # Recursion prerequisites
    G.add_edge('functions', 'recursion', relation='prerequisite')
    G.add_edge('base_case', 'recursion', relation='prerequisite')
    G.add_edge('recursive_call', 'recursion', relation='prerequisite')
    G.add_edge('recursion', 'dynamic_programming', relation='prerequisite')
    G.add_edge('call_stack', 'recursion', relation='related')
    
    # OOP hierarchy
    G.add_edge('object_oriented_programming', 'class', relation='contains')
    G.add_edge('object_oriented_programming', 'object', relation='contains')
    G.add_edge('object_oriented_programming', 'inheritance', relation='contains')
    G.add_edge('object_oriented_programming', 'polymorphism', relation='contains')
    G.add_edge('object_oriented_programming', 'encapsulation', relation='contains')
    
    # OOP relationships
    G.add_edge('class', 'object', relation='creates')
    G.add_edge('class', 'inheritance', relation='uses')
    G.add_edge('inheritance', 'polymorphism', relation='enables')
    
    # Method relationships
    G.add_edge('sorting', 'quicksort', relation='uses_method')
    G.add_edge('searching', 'binary_search', relation='uses_method')
    G.add_edge('tree', 'depth_first_search', relation='uses_method')
    G.add_edge('tree', 'breadth_first_search', relation='uses_method')
    G.add_edge('graph', 'depth_first_search', relation='uses_method')
    G.add_edge('graph', 'breadth_first_search', relation='uses_method')
    
    # Task relationships
    G.add_edge('tree_traversal', 'depth_first_search', relation='solves')
    G.add_edge('tree_traversal', 'breadth_first_search', relation='solves')
    G.add_edge('path_finding', 'breadth_first_search', relation='solves')
    G.add_edge('data_organization', 'linked_list', relation='uses')
    G.add_edge('data_organization', 'tree', relation='uses')
    
    # Cross-domain connections
    G.add_edge('linked_list', 'tree', relation='related')
    G.add_edge('tree', 'graph', relation='related')
    G.add_edge('array', 'sorting', relation='uses')
    G.add_edge('linked_list', 'sorting', relation='uses')
    
    # Add missing prerequisite node
    G.add_node('functions', category='concept', level=1)
    G.add_edge('programming_fundamentals', 'functions', relation='contains')
    
    return G, node_categories


def visualize_hierarchical_layout(G, node_categories, filename='cse_kg_hierarchical.png'):
    """Create a hierarchical layout visualization"""
    
    fig, ax = plt.subplots(figsize=(20, 14))
    
    # Create hierarchical layout
    pos = {}
    levels = {}
    
    # Group nodes by level
    for node in G.nodes():
        level = G.nodes[node].get('level', 0)
        if level not in levels:
            levels[level] = []
        levels[level].append(node)
    
    # Position nodes by level
    max_level = max(levels.keys()) if levels else 0
    y_spacing = 1.0
    x_spacing = 2.0
    
    for level in sorted(levels.keys()):
        nodes_at_level = levels[level]
        num_nodes = len(nodes_at_level)
        start_x = -(num_nodes - 1) * x_spacing / 2
        
        for i, node in enumerate(nodes_at_level):
            x = start_x + i * x_spacing
            y = (max_level - level) * y_spacing
            pos[node] = (x, y)
    
    # Draw edges
    edge_colors = []
    for u, v in G.edges():
        relation = G[u][v].get('relation', 'related')
        if relation == 'prerequisite':
            edge_colors.append('#FF4444')  # Red for prerequisites
        elif relation == 'contains':
            edge_colors.append('#4444FF')  # Blue for hierarchy
        elif relation == 'uses' or relation == 'uses_method':
            edge_colors.append('#44FF44')  # Green for usage
        elif relation == 'solves':
            edge_colors.append('#FF8844')  # Orange for solves
        else:
            edge_colors.append('#888888')  # Gray for other
    
    nx.draw_networkx_edges(G, pos, edge_color=edge_colors, 
                          arrows=True, arrowsize=15, alpha=0.6, 
                          connectionstyle='arc3,rad=0.1', ax=ax)
    
    # Draw nodes by category
    for category, color in node_categories.items():
        nodes = [n for n in G.nodes() if G.nodes[n].get('category') == category]
        if nodes:
            nx.draw_networkx_nodes(G, pos, nodelist=nodes, 
                                 node_color=color, node_size=1500,
                                 alpha=0.8, ax=ax)
    
    # Draw labels
    labels = {node: node.replace('_', '\n') for node in G.nodes()}
    nx.draw_networkx_labels(G, pos, labels, font_size=7, 
                           font_weight='bold', ax=ax)
    
    # Create legend
    legend_elements = [
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=node_categories['concept'], 
                  markersize=15, label='Concept'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=node_categories['method'], 
                  markersize=15, label='Method'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=node_categories['task'], 
                  markersize=15, label='Task'),
        plt.Line2D([0], [0], color='#FF4444', label='Prerequisite'),
        plt.Line2D([0], [0], color='#4444FF', label='Contains/Hierarchy'),
        plt.Line2D([0], [0], color='#44FF44', label='Uses'),
        plt.Line2D([0], [0], color='#FF8844', label='Solves'),
    ]
    ax.legend(handles=legend_elements, loc='upper left', fontsize=10)
    
    ax.set_title('CSE-KG 2.0 Knowledge Graph Structure\n(Hierarchical Layout)', 
                fontsize=16, fontweight='bold', pad=20)
    ax.axis('off')
    
    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"[OK] Saved hierarchical visualization to {filename}")
    plt.close()


def visualize_spring_layout(G, node_categories, filename='cse_kg_spring.png'):
    """Create a spring layout visualization showing relationships"""
    
    fig, ax = plt.subplots(figsize=(20, 16))
    
    # Use spring layout for better relationship visualization
    pos = nx.spring_layout(G, k=2, iterations=50, seed=42)
    
    # Draw edges with different styles
    prerequisite_edges = [(u, v) for u, v in G.edges() 
                         if G[u][v].get('relation') == 'prerequisite']
    other_edges = [(u, v) for u, v in G.edges() 
                  if G[u][v].get('relation') != 'prerequisite']
    
    nx.draw_networkx_edges(G, pos, edgelist=other_edges, 
                          edge_color='#CCCCCC', alpha=0.3,
                          arrows=True, arrowsize=10, ax=ax)
    nx.draw_networkx_edges(G, pos, edgelist=prerequisite_edges, 
                          edge_color='#FF4444', alpha=0.7, width=2,
                          arrows=True, arrowsize=15, ax=ax)
    
    # Draw nodes by category
    for category, color in node_categories.items():
        nodes = [n for n in G.nodes() if G.nodes[n].get('category') == category]
        if nodes:
            nx.draw_networkx_nodes(G, pos, nodelist=nodes, 
                                 node_color=color, node_size=2000,
                                 alpha=0.9, ax=ax)
    
    # Draw labels
    labels = {node: node.replace('_', '\n') for node in G.nodes()}
    nx.draw_networkx_labels(G, pos, labels, font_size=8, 
                           font_weight='bold', ax=ax)
    
    # Create legend
    legend_elements = [
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=node_categories['concept'], 
                  markersize=15, label='Concept'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=node_categories['method'], 
                  markersize=15, label='Method'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=node_categories['task'], 
                  markersize=15, label='Task'),
        plt.Line2D([0], [0], color='#FF4444', linewidth=2, label='Prerequisite (Red)'),
        plt.Line2D([0], [0], color='#CCCCCC', label='Other Relationships (Gray)'),
    ]
    ax.legend(handles=legend_elements, loc='upper right', fontsize=11)
    
    ax.set_title('CSE-KG 2.0 Knowledge Graph Structure\n(Spring Layout - Emphasizing Relationships)', 
                fontsize=16, fontweight='bold', pad=20)
    ax.axis('off')
    
    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"[OK] Saved spring layout visualization to {filename}")
    plt.close()


def visualize_linked_list_subgraph(G, node_categories, filename='cse_kg_linked_list_subgraph.png'):
    """Visualize a focused subgraph for linked list learning domain"""
    
    fig, ax = plt.subplots(figsize=(14, 10))
    
    # Extract linked list related subgraph
    linked_list_nodes = ['linked_list', 'node', 'pointer', 'array', 
                        'memory_management', 'dynamic_allocation', 
                        'data_structures', 'data_organization']
    
    subgraph = G.subgraph(linked_list_nodes).copy()
    
    # Create circular layout
    pos = nx.circular_layout(subgraph)
    
    # Adjust positions for better visualization
    pos['data_structures'] = (0, 1.5)
    pos['linked_list'] = (0, 0.5)
    pos['node'] = (-1, -0.5)
    pos['pointer'] = (1, -0.5)
    pos['array'] = (-1.5, 0.5)
    pos['memory_management'] = (1.5, 0.5)
    pos['dynamic_allocation'] = (0, -1.5)
    pos['data_organization'] = (0, -0.5)
    
    # Draw edges
    prerequisite_edges = [(u, v) for u, v in subgraph.edges() 
                         if subgraph[u][v].get('relation') == 'prerequisite']
    other_edges = [(u, v) for u, v in subgraph.edges() 
                  if subgraph[u][v].get('relation') != 'prerequisite']
    
    nx.draw_networkx_edges(subgraph, pos, edgelist=other_edges, 
                          edge_color='#4444FF', alpha=0.5,
                          arrows=True, arrowsize=12, ax=ax)
    nx.draw_networkx_edges(subgraph, pos, edgelist=prerequisite_edges, 
                          edge_color='#FF4444', alpha=0.8, width=2.5,
                          arrows=True, arrowsize=15, ax=ax)
    
    # Draw nodes
    for category, color in node_categories.items():
        nodes = [n for n in subgraph.nodes() if subgraph.nodes[n].get('category') == category]
        if nodes:
            nx.draw_networkx_nodes(subgraph, pos, nodelist=nodes, 
                                 node_color=color, node_size=3000,
                                 alpha=0.9, ax=ax)
    
    # Highlight linked_list node
    nx.draw_networkx_nodes(subgraph, pos, nodelist=['linked_list'], 
                         node_color='#FFD700', node_size=4000,
                         alpha=0.9, ax=ax, edgecolors='black', linewidths=3)
    
    # Draw labels
    labels = {node: node.replace('_', '\n') for node in subgraph.nodes()}
    nx.draw_networkx_labels(subgraph, pos, labels, font_size=10, 
                           font_weight='bold', ax=ax)
    
    # Add edge labels for prerequisites
    edge_labels = {}
    for u, v in prerequisite_edges:
        edge_labels[(u, v)] = 'prereq'
    nx.draw_networkx_edge_labels(subgraph, pos, edge_labels, 
                                font_size=8, ax=ax)
    
    ax.set_title('CSE-KG 2.0: Linked List Learning Domain Subgraph', 
                fontsize=16, fontweight='bold', pad=20)
    ax.axis('off')
    
    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"[OK] Saved linked list subgraph to {filename}")
    plt.close()


def print_graph_statistics(G):
    """Print statistics about the knowledge graph"""
    
    print("\n" + "="*60)
    print("CSE-KG 2.0 Knowledge Graph Statistics")
    print("="*60)
    
    print(f"\nTotal Nodes: {G.number_of_nodes()}")
    print(f"Total Edges: {G.number_of_edges()}")
    
    # Count by category
    categories = {}
    for node in G.nodes():
        cat = G.nodes[node].get('category', 'unknown')
        categories[cat] = categories.get(cat, 0) + 1
    
    print("\nNodes by Category:")
    for cat, count in sorted(categories.items()):
        print(f"  {cat.capitalize()}: {count}")
    
    # Count by relation type
    relations = {}
    for u, v in G.edges():
        rel = G[u][v].get('relation', 'unknown')
        relations[rel] = relations.get(rel, 0) + 1
    
    print("\nEdges by Relation Type:")
    for rel, count in sorted(relations.items(), key=lambda x: -x[1]):
        print(f"  {rel}: {count}")
    
    # Graph density
    density = nx.density(G)
    print(f"\nGraph Density: {density:.4f}")
    
    # Average degree
    avg_degree = sum(dict(G.degree()).values()) / G.number_of_nodes()
    print(f"Average Degree: {avg_degree:.2f}")
    
    print("="*60 + "\n")


def main():
    """Main function to generate all visualizations"""
    
    print("Creating CSE-KG 2.0 Knowledge Graph Visualizations...")
    print("="*60)
    
    # Create the graph
    G, node_categories = create_cse_kg_visualization()
    
    # Print statistics
    print_graph_statistics(G)
    
    # Generate visualizations
    print("Generating visualizations...")
    visualize_hierarchical_layout(G, node_categories, 'cse_kg_hierarchical.png')
    visualize_spring_layout(G, node_categories, 'cse_kg_spring.png')
    visualize_linked_list_subgraph(G, node_categories, 'cse_kg_linked_list_subgraph.png')
    
    print("\n" + "="*60)
    print("[OK] All visualizations generated successfully!")
    print("="*60)
    print("\nGenerated files:")
    print("  1. cse_kg_hierarchical.png - Hierarchical layout")
    print("  2. cse_kg_spring.png - Spring layout (relationship-focused)")
    print("  3. cse_kg_linked_list_subgraph.png - Linked list domain subgraph")
    print("\n")


if __name__ == "__main__":
    main()

