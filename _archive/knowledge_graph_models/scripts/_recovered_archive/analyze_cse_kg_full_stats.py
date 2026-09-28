"""
Analyze full CSE-KG statistics from TTL files
Count nodes, edges, and relationship types using RDF parsing
"""

from pathlib import Path
from collections import defaultdict
import re

def analyze_cse_kg_stats():
    """Analyze full CSE-KG statistics"""
    print("="*70)
    print("CSE-KG 2.0 Full Graph Statistics Analysis")
    print("="*70)
    
    ttl_dir = Path("data/cse_kg_full/extracted/cskg")
    
    if not ttl_dir.exists():
        print(f"\n[ERROR] TTL directory not found: {ttl_dir}")
        return
    
    ttl_files = sorted(list(ttl_dir.glob("cskg_*.ttl")))
    
    if not ttl_files:
        print(f"\n[ERROR] No TTL files found in {ttl_dir}")
        return
    
    print(f"\nFound {len(ttl_files)} TTL files")
    
    # Counters
    nodes = set()
    relationships = set()  # (subject, object, predicate) triple
    relationship_types = set()  # unique predicates
    total_lines = 0
    total_statements = 0
    
    # Process sample files
    sample_size = min(5, len(ttl_files))
    print(f"\nAnalyzing {sample_size} sample files...\n")
    
    for ttl_file in ttl_files[:sample_size]:
        try:
            print(f"  Processing {ttl_file.name}...")
            with open(ttl_file, 'r', encoding='utf-8', errors='ignore') as f:
                for line_num, line in enumerate(f, 1):
                    total_lines += 1
                    
                    # Skip comments and prefixes
                    line_stripped = line.strip()
                    if not line_stripped or line_stripped.startswith('@') or line_stripped.startswith('#'):
                        continue
                    
                    # Look for statement patterns
                    # Pattern: cskg:subject cskg-ont:predicate cskg:object .
                    # Pattern: cskg:statement_0 a cskg-ont:Statement ;
                    
                    # Extract URIs (cskg:something or <uri>)
                    uris = re.findall(r'(cskg:[a-zA-Z0-9_]+|cskg-ont:[a-zA-Z0-9_]+|<[^>]+>|"[^"]+")', line)
                    
                    if len(uris) >= 2:
                        # Check if it's a statement declaration
                        if 'cskg:statement_' in line:
                            # Statement definition - we'll look for rdf:subject, rdf:predicate, rdf:object
                            statement_id = None
                            for uri in uris:
                                if 'cskg:statement_' in uri:
                                    statement_id = uri
                                    break
                            # Note: Need to parse multiline statements
                            total_statements += 1
                    
                    # Look for direct triples (simpler pattern)
                    # Pattern: subject predicate object .
                    if line_stripped.endswith('.') and 'cskg:' in line:
                        parts = line_stripped[:-1].split(None, 2)  # Split into max 3 parts
                        if len(parts) >= 3:
                            subj = parts[0].rstrip(';,').strip()
                            pred = parts[1].rstrip(';,').strip()
                            obj = parts[2].rstrip(';,').strip()
                            
                            # Clean up
                            subj = subj.strip('<>')
                            pred = pred.strip('<>')
                            obj = obj.strip('<>').strip('"\'')
                            
                            if (subj.startswith('cskg:') or subj.startswith('cskg-ont:') or 
                                obj.startswith('cskg:') or obj.startswith('cskg-ont:')):
                                nodes.add(subj)
                                nodes.add(obj)
                                relationship_types.add(pred)
                                relationships.add((subj, pred, obj))
                    
                    if line_num % 100000 == 0:
                        print(f"    Processed {line_num:,} lines... "
                              f"(Found {len(nodes):,} nodes, {len(relationship_types)} relation types)")
            
            print(f"    Completed: {total_lines:,} lines, {len(nodes):,} nodes, "
                  f"{len(relationship_types)} relation types, {len(relationships):,} relationships")
        
        except Exception as e:
            print(f"    Error processing {ttl_file.name}: {e}")
            continue
    
    print(f"\n" + "="*70)
    print(f"Analysis Results (from {sample_size} sample files):")
    print("="*70)
    
    print(f"\n1. NODES (Unique Entities):")
    print(f"   Total Unique Nodes Found: {len(nodes):,}")
    
    # Categorize nodes
    concept_nodes = [n for n in nodes if 'cskg:' in n and 'statement' not in n]
    method_nodes = [n for n in nodes if 'method' in n.lower()]
    task_nodes = [n for n in nodes if 'task' in n.lower()]
    statement_nodes = [n for n in nodes if 'statement' in n.lower()]
    
    print(f"   Concept/Entity nodes: {len(concept_nodes):,}")
    print(f"   Statement nodes: {len(statement_nodes):,}")
    print(f"   Method nodes: {len(method_nodes):,}")
    print(f"   Task nodes: {len(task_nodes):,}")
    
    print(f"\n2. RELATIONSHIP TYPES (Unique Predicates):")
    print(f"   Total Unique Relationship Types: {len(relationship_types):,}")
    
    # Count occurrences per type
    rel_type_counts = defaultdict(int)
    for _, pred, _ in relationships:
        rel_type_counts[pred] += 1
    
    print(f"\n   Relationship Types Found ({min(20, len(relationship_types))} shown):")
    for rel_type, count in sorted(rel_type_counts.items(), key=lambda x: -x[1])[:20]:
        print(f"     - {rel_type}: {count:,} occurrences")
    if len(relationship_types) > 20:
        print(f"     ... and {len(relationship_types) - 20} more types")
    
    print(f"\n3. RELATIONSHIPS (Edges/Triples):")
    print(f"   Total Unique Relationships: {len(relationships):,}")
    
    # Estimate for full dataset
    if sample_size > 0:
        avg_nodes_per_file = len(nodes) / sample_size
        avg_rels_per_file = len(relationships) / sample_size
        avg_rel_types = len(relationship_types)
        
        print(f"\n4. ESTIMATES FOR FULL DATASET ({len(ttl_files)} files):")
        print(f"   Files analyzed: {sample_size} / {len(ttl_files)}")
        print(f"   Estimated total nodes: ~{int(avg_nodes_per_file * len(ttl_files)):,}")
        print(f"   Estimated total relationships: ~{int(avg_rels_per_file * len(ttl_files)):,}")
        print(f"   Estimated relationship types: ~{avg_rel_types:,} (may increase with more files)")
    
    # Sample nodes
    print(f"\n5. SAMPLE NODES (First 10 unique):")
    sample_concepts = [n for n in sorted(concept_nodes) if 'statement' not in n][:10]
    for i, node in enumerate(sample_concepts):
        print(f"   {i+1}. {node}")
    
    print(f"\n6. FILE STATISTICS:")
    print(f"   Total lines processed: {total_lines:,}")
    print(f"   Total statements found: {total_statements:,}")
    
    print(f"\n" + "="*70)
    print("Analysis Complete!")
    print("="*70)
    print("\nNote: These are estimates based on sample files.")
    print("For exact counts, use an RDF parser like rdflib to process all files.")

if __name__ == "__main__":
    analyze_cse_kg_stats()
