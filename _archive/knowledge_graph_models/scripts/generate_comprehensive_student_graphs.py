"""
Generate comprehensive visual graphs for each student:
1. Code Correctness Progression
2. Errors Encountered
3. CSE-KG Graph Visualization
4. Pedagogical KG Graph Visualization
5. COKE Graph Visualization
6. Student Performance Dashboard
"""

import json
import pickle
from pathlib import Path
from collections import defaultdict
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import numpy as np
import networkx as nx
from typing import Dict, List, Tuple

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
colors = plt.cm.Set3(np.linspace(0, 1, 12))

def load_conversation(conversation_file: str) -> Dict:
    """Load conversation JSON"""
    with open(conversation_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_cse_kg_graph() -> nx.DiGraph:
    """Load CSE-KG graph from pickle"""
    graph_file = Path("data/cse_kg_local/graph.pkl")
    if graph_file.exists():
        with open(graph_file, 'rb') as f:
            return pickle.load(f)
    return nx.DiGraph()

def load_pedagogical_misconceptions() -> Dict:
    """Load pedagogical misconceptions"""
    misconceptions_file = Path("data/pedagogical_kg/misconceptions.json")
    if misconceptions_file.exists():
        with open(misconceptions_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def load_coke_chains() -> Dict:
    """Load COKE cognitive chains"""
    chains_file = Path("data/coke/coke_chains.json")
    if chains_file.exists():
        with open(chains_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def generate_comprehensive_graphs(conversation_file: str, output_dir: str = "output"):
    """Generate all comprehensive graphs for a student"""
    
    conversation = load_conversation(conversation_file)
    student_id = conversation.get('student_id', 'unknown')
    turns = conversation.get('turns', [])
    
    # Create figure with multiple subplots (removed DINA mastery plots)
    fig = plt.figure(figsize=(20, 18))
    gs = fig.add_gridspec(3, 2, hspace=0.3, wspace=0.3)
    
    # Extract turn numbers and other data
    turn_numbers = []
    correctness_scores = []
    cognitive_states = []
    errors_encountered = []
    
    for turn in turns:
        turn_num = turn.get('turn_number', 0)
        turn_numbers.append(turn_num)
        
        metrics = turn.get('metrics', {})
        quantitative = metrics.get('quantitative', {})
        
        # Code correctness
        codebert = quantitative.get('codebert_analysis', {})
        correctness = codebert.get('correctness_score', 0.5) if codebert else 0.5
        correctness_scores.append(correctness)
        
        # Cognitive state
        coke = quantitative.get('coke_analysis', {})
        cognitive_state = coke.get('cognitive_state', 'unknown') if coke else 'unknown'
        cognitive_states.append(cognitive_state)
        
        # Errors
        student_input = turn.get('student_input', {})
        error = student_input.get('error_message', '')
        errors_encountered.append(1 if error else 0)
    
    # ========== PLOT 1: Code Correctness Progression ==========
    ax1 = fig.add_subplot(gs[0, 0])
    
    ax1.plot(turn_numbers, correctness_scores, marker='o', linewidth=3, markersize=10, 
             color='#27AE60', label='Code Correctness', zorder=3)
    ax1.fill_between(turn_numbers, correctness_scores, alpha=0.3, color='#27AE60')
    ax1.axhline(y=0.8, color='green', linestyle='--', alpha=0.7, linewidth=2, label='Good (0.8)')
    ax1.axhline(y=0.5, color='orange', linestyle='--', alpha=0.7, linewidth=2, label='Fair (0.5)')
    ax1.set_xlabel('Turn Number', fontsize=11, fontweight='bold')
    ax1.set_ylabel('Correctness Score', fontsize=11, fontweight='bold')
    ax1.set_title('Code Correctness Progression', fontsize=12, fontweight='bold')
    ax1.set_ylim(0, 1)
    ax1.grid(True, alpha=0.3, zorder=0)
    ax1.legend(loc='best', fontsize=9)
    
    # ========== PLOT 2: Errors Encountered ==========
    ax2 = fig.add_subplot(gs[0, 1])
    
    colors_errors = ['red' if e else 'green' for e in errors_encountered]
    bars = ax2.bar(turn_numbers, errors_encountered, color=colors_errors, alpha=0.7, 
                   edgecolor='black', linewidth=1.5, zorder=2)
    ax2.set_xlabel('Turn Number', fontsize=11, fontweight='bold')
    ax2.set_ylabel('Error Occurred', fontsize=11, fontweight='bold')
    ax2.set_title('Errors Encountered per Turn', fontsize=12, fontweight='bold')
    ax2.set_ylim(-0.1, 1.1)
    ax2.set_yticks([0, 1])
    ax2.set_yticklabels(['No Error', 'Error'], fontsize=9)
    ax2.grid(True, alpha=0.3, axis='y', zorder=0)
    
    # Legend
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor='green', alpha=0.7, label='No Error'),
                       Patch(facecolor='red', alpha=0.7, label='Error')]
    ax2.legend(handles=legend_elements, loc='upper right', fontsize=9)
    
    # ========== PLOT 3: CSE-KG Graph Visualization ==========
    ax3 = fig.add_subplot(gs[1, 0])
    
    # Load and visualize CSE-KG
    cse_kg_graph = load_cse_kg_graph()
    
    # Extract concepts from conversation
    conversation_concepts = set()
    for turn in turns:
        system_analysis = turn.get('system_analysis', {})
        cse_kg_queries = system_analysis.get('cse_kg_queries', {})
        if isinstance(cse_kg_queries, dict):
            # Extract concepts from prerequisites and related concepts
            prereqs = cse_kg_queries.get('prerequisites', [])
            related = cse_kg_queries.get('related_concepts', [])
            for p in prereqs:
                if isinstance(p, dict):
                    concept = p.get('concept', '')
                    if concept:
                        conversation_concepts.add(concept.split('/')[-1] if '/' in concept else concept)
            for r in related:
                if isinstance(r, dict):
                    concept = r.get('concept', '')
                    if concept:
                        conversation_concepts.add(concept.split('/')[-1] if '/' in concept else concept)
    
    # Create subgraph with conversation concepts
    if cse_kg_graph and conversation_concepts:
        # Find nodes in CSE-KG that match conversation concepts
        subgraph_nodes = []
        for node in cse_kg_graph.nodes():
            node_name = str(node).split('/')[-1].lower()
            for conv_concept in conversation_concepts:
                if conv_concept.lower() in node_name or node_name in conv_concept.lower():
                    subgraph_nodes.append(node)
                    break
        
        if subgraph_nodes:
            subgraph = cse_kg_graph.subgraph(subgraph_nodes[:15])  # Limit to 15 nodes
            if subgraph.number_of_nodes() > 0:
                pos = nx.spring_layout(subgraph, k=2, iterations=50)
                
                # Calculate graph metrics
                degree_centrality = nx.degree_centrality(subgraph)
                betweenness_centrality = nx.betweenness_centrality(subgraph)
                closeness_centrality = nx.closeness_centrality(subgraph)
                
                # Node sizes based on degree centrality
                node_sizes = [800 + degree_centrality.get(node, 0) * 2000 for node in subgraph.nodes()]
                
                nx.draw_networkx_nodes(subgraph, pos, node_color='#4A90E2', node_size=node_sizes, 
                                      alpha=0.8, ax=ax3)
                nx.draw_networkx_edges(subgraph, pos, edge_color='gray', alpha=0.6, 
                                      arrows=True, arrowsize=15, ax=ax3)
                nx.draw_networkx_labels(subgraph, pos, font_size=7, font_weight='bold', ax=ax3)
                
                # Add metrics text
                metrics_text = f"Nodes: {subgraph.number_of_nodes()}, Edges: {subgraph.number_of_edges()}\n"
                metrics_text += f"Avg Degree: {sum(degree_centrality.values())/len(degree_centrality):.3f}\n"
                metrics_text += f"Max Betweenness: {max(betweenness_centrality.values()):.3f}"
                ax3.text(0.02, 0.98, metrics_text, transform=ax3.transAxes, fontsize=8,
                        verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
                
                ax3.set_title('CSE-KG Graph (Concepts from Conversation)', fontsize=12, fontweight='bold')
                ax3.axis('off')
            else:
                ax3.text(0.5, 0.5, 'No CSE-KG nodes found', ha='center', va='center', 
                        transform=ax3.transAxes, fontsize=11)
                ax3.set_title('CSE-KG Graph', fontsize=12, fontweight='bold')
        else:
            ax3.text(0.5, 0.5, 'No matching CSE-KG concepts', ha='center', va='center', 
                    transform=ax3.transAxes, fontsize=11)
            ax3.set_title('CSE-KG Graph', fontsize=12, fontweight='bold')
    else:
        ax3.text(0.5, 0.5, 'CSE-KG graph not available', ha='center', va='center', 
                transform=ax3.transAxes, fontsize=11)
        ax3.set_title('CSE-KG Graph', fontsize=12, fontweight='bold')
    
    # ========== PLOT 4: Pedagogical KG Graph (Misconceptions) ==========
    ax4 = fig.add_subplot(gs[1, 1])
    
    # Extract misconceptions from conversation
    misconceptions_graph = nx.DiGraph()
    misconception_concepts = set()
    
    for turn in turns:
        system_analysis = turn.get('system_analysis', {})
        learned_misconceptions = system_analysis.get('learned_misconceptions', [])
        for mc in learned_misconceptions:
            mc_id = mc.get('id', 'unknown')
            concept = mc.get('concept', 'unknown')
            misconception_concepts.add(concept)
            misconceptions_graph.add_node(mc_id, concept=concept, 
                                         severity=mc.get('severity', 'medium'),
                                         frequency=mc.get('frequency', 0.0))
            misconceptions_graph.add_edge(concept, mc_id, relation='has_misconception')
    
    if misconceptions_graph.number_of_nodes() > 0:
        pos = nx.spring_layout(misconceptions_graph, k=1.5, iterations=50)
        
        # Calculate graph metrics
        degree_centrality = nx.degree_centrality(misconceptions_graph)
        betweenness_centrality = nx.betweenness_centrality(misconceptions_graph)
        
        # Color nodes by severity and size by degree centrality
        node_colors = []
        node_sizes = []
        for node in misconceptions_graph.nodes():
            severity = misconceptions_graph.nodes[node].get('severity', 'medium')
            if severity == 'high':
                node_colors.append('#E74C3C')
            elif severity == 'medium':
                node_colors.append('#F39C12')
            else:
                node_colors.append('#3498DB')
            # Size based on degree centrality
            node_sizes.append(800 + degree_centrality.get(node, 0) * 1500)
        
        nx.draw_networkx_nodes(misconceptions_graph, pos, node_color=node_colors, 
                              node_size=node_sizes, alpha=0.8, ax=ax4)
        nx.draw_networkx_edges(misconceptions_graph, pos, edge_color='#E67E22', 
                              alpha=0.6, arrows=True, arrowsize=15, ax=ax4)
        
        # Labels
        labels = {node: node[:15] for node in misconceptions_graph.nodes()}
        nx.draw_networkx_labels(misconceptions_graph, pos, labels, font_size=7, 
                               font_weight='bold', ax=ax4)
        
        # Add metrics text
        metrics_text = f"Nodes: {misconceptions_graph.number_of_nodes()}\n"
        metrics_text += f"Edges: {misconceptions_graph.number_of_edges()}\n"
        metrics_text += f"Avg Degree: {sum(degree_centrality.values())/len(degree_centrality):.3f}\n"
        metrics_text += f"Max Betweenness: {max(betweenness_centrality.values()):.3f}"
        ax4.text(0.02, 0.98, metrics_text, transform=ax4.transAxes, fontsize=8,
                verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        
        ax4.set_title('Pedagogical KG (Misconceptions Learned)', fontsize=12, fontweight='bold')
        ax4.axis('off')
        
        # Legend
        high_patch = mpatches.Patch(color='#E74C3C', label='High Severity')
        med_patch = mpatches.Patch(color='#F39C12', label='Medium Severity')
        low_patch = mpatches.Patch(color='#3498DB', label='Low Severity')
        ax4.legend(handles=[high_patch, med_patch, low_patch], loc='upper right', fontsize=8)
    else:
        ax4.text(0.5, 0.5, 'No misconceptions learned', ha='center', va='center', 
                transform=ax4.transAxes, fontsize=11)
        ax4.set_title('Pedagogical KG (Misconceptions)', fontsize=12, fontweight='bold')
    
    # ========== PLOT 5: COKE Cognitive Graph ==========
    ax5 = fig.add_subplot(gs[2, 0])
    
    # Extract COKE cognitive states and chains
    coke_graph = nx.DiGraph()
    cognitive_states = []
    
    for turn in turns:
        system_analysis = turn.get('system_analysis', {})
        coke_analysis = system_analysis.get('coke_analysis', {})
        if isinstance(coke_analysis, dict):
            cognitive_state = coke_analysis.get('cognitive_state', 'unknown')
            theory_of_mind = coke_analysis.get('theory_of_mind', {})
            behavioral_response = theory_of_mind.get('predicted_behavior', 'continue')
            
            cognitive_states.append(cognitive_state)
            coke_graph.add_node(cognitive_state, type='state')
            coke_graph.add_node(behavioral_response, type='behavior')
            coke_graph.add_edge(cognitive_state, behavioral_response, 
                              weight=theory_of_mind.get('chain_confidence', 0.5))
    
    if coke_graph.number_of_nodes() > 0:
        pos = nx.spring_layout(coke_graph, k=2, iterations=50)
        
        # Calculate graph metrics
        degree_centrality = nx.degree_centrality(coke_graph)
        betweenness_centrality = nx.betweenness_centrality(coke_graph)
        closeness_centrality = nx.closeness_centrality(coke_graph)
        
        # Color nodes by type and size by degree centrality
        node_colors = []
        node_sizes = []
        for node in coke_graph.nodes():
            node_type = coke_graph.nodes[node].get('type', 'state')
            node_colors.append('#9B59B6' if node_type == 'state' else '#1ABC9C')
            node_sizes.append(1000 + degree_centrality.get(node, 0) * 2000)
        
        nx.draw_networkx_nodes(coke_graph, pos, node_color=node_colors, 
                              node_size=node_sizes, alpha=0.8, ax=ax5)
        
        # Edge widths based on confidence
        edge_widths = [coke_graph[u][v].get('weight', 0.5) * 3 for u, v in coke_graph.edges()]
        nx.draw_networkx_edges(coke_graph, pos, edge_color='#34495E', 
                              alpha=0.7, arrows=True, arrowsize=20, width=edge_widths, ax=ax5)
        
        labels = {node: node[:12] for node in coke_graph.nodes()}
        nx.draw_networkx_labels(coke_graph, pos, labels, font_size=8, 
                               font_weight='bold', ax=ax5)
        
        # Add metrics text
        metrics_text = f"Nodes: {coke_graph.number_of_nodes()}\n"
        metrics_text += f"Edges: {coke_graph.number_of_edges()}\n"
        metrics_text += f"Avg Degree: {sum(degree_centrality.values())/len(degree_centrality):.3f}\n"
        metrics_text += f"Max Betweenness: {max(betweenness_centrality.values()):.3f}\n"
        metrics_text += f"Avg Closeness: {sum(closeness_centrality.values())/len(closeness_centrality):.3f}"
        ax5.text(0.02, 0.98, metrics_text, transform=ax5.transAxes, fontsize=8,
                verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        
        ax5.set_title('COKE Cognitive Graph (Theory of Mind)', fontsize=12, fontweight='bold')
        ax5.axis('off')
        
        # Legend
        state_patch = mpatches.Patch(color='#9B59B6', label='Cognitive State')
        behavior_patch = mpatches.Patch(color='#1ABC9C', label='Behavioral Response')
        ax5.legend(handles=[state_patch, behavior_patch], loc='upper right', fontsize=8)
    else:
        ax5.text(0.5, 0.5, 'No COKE data available', ha='center', va='center', 
                transform=ax5.transAxes, fontsize=11)
        ax5.set_title('COKE Cognitive Graph', fontsize=12, fontweight='bold')
    
    # ========== PLOT 6: Student Performance Dashboard ==========
    ax6 = fig.add_subplot(gs[2, 1])
    ax6.axis('off')
    
    # Create dashboard text (without DINA mastery)
    dashboard_lines = []
    dashboard_lines.append("=" * 30)
    dashboard_lines.append("STUDENT PERFORMANCE DASHBOARD")
    dashboard_lines.append("=" * 30)
    
    # Get latest metrics
    if turns:
        latest_turn = turns[-1]
        metrics = latest_turn.get('metrics', {})
        quantitative = metrics.get('quantitative', {})
        
        # Code correctness
        codebert = quantitative.get('codebert_analysis', {})
        if codebert:
            correctness = codebert.get('correctness_score', 0.0)
            syntax_errors = codebert.get('syntax_errors', 0.0)
            logic_errors = codebert.get('logic_errors', 0.0)
            quality = codebert.get('code_quality', 'unknown')
            dashboard_lines.append(f"\nCode Correctness: {correctness:.2f}")
            dashboard_lines.append(f"Syntax Errors: {syntax_errors:.2f}")
            dashboard_lines.append(f"Logic Errors: {logic_errors:.2f}")
            dashboard_lines.append(f"Code Quality: {quality}")
        
        # Cognitive state
        coke = quantitative.get('coke_analysis', {})
        if coke:
            cognitive_state = coke.get('cognitive_state', 'unknown')
            confidence = coke.get('confidence', 0.0)
            behavioral = coke.get('behavioral_response', 'unknown')
            dashboard_lines.append(f"\nCognitive State: {cognitive_state}")
            dashboard_lines.append(f"Confidence: {confidence:.2f}")
            dashboard_lines.append(f"Behavioral Response: {behavioral}")
        
        # Time tracking
        time_tracking = quantitative.get('time_tracking', {})
        if time_tracking:
            duration = time_tracking.get('turn_duration_seconds', 0.0)
            stuck = time_tracking.get('time_stuck_seconds', 0.0)
            dashboard_lines.append(f"\nTurn Duration: {duration:.1f}s")
            dashboard_lines.append(f"Time Stuck: {stuck:.1f}s")
    
    # Display dashboard
    dashboard_str = "\n".join(dashboard_lines)
    ax6.text(0.05, 0.95, dashboard_str, transform=ax6.transAxes, fontsize=10,
             verticalalignment='top', family='monospace',
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.7, pad=10))
    
    # Main title
    fig.suptitle(f'Comprehensive Student Understanding Analysis: {student_id}', 
                fontsize=18, fontweight='bold', y=0.995)
    
    # Save figure
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    graph_file = output_path / f"comprehensive_graphs_{Path(conversation_file).stem}.png"
    plt.savefig(graph_file, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    
    print(f"[OK] Comprehensive graphs saved to: {graph_file}")
    return graph_file

if __name__ == "__main__":
    import sys
    
    output_dir = "output"
    
    if len(sys.argv) > 1:
        conversation_file = sys.argv[1]
        generate_comprehensive_graphs(conversation_file, output_dir)
    else:
        # Generate for all conversations
        for i in range(1, 11):
            json_file = Path(output_dir) / f"sample_conversation_{i:02d}.json"
            if json_file.exists():
                print(f"\nGenerating comprehensive graphs for conversation {i}...")
                generate_comprehensive_graphs(str(json_file), output_dir)
        
        print("\n[OK] All comprehensive graphs generated!")

