"""
Extract and display CSE-KG 2.0 structure and configuration
Shows what data can be extracted from the knowledge graph
"""

import yaml
import json
from pathlib import Path


def show_cse_kg_structure():
    """Show CSE-KG 2.0 structure from config"""
    print("="*80)
    print("CSE-KG 2.0 STRUCTURE AND CONFIGURATION")
    print("="*80)
    
    # Load config
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    cse_kg_config = config.get('cse_kg', {})
    
    print(f"\n1. SPARQL ENDPOINT")
    print(f"   URL: {cse_kg_config.get('sparql_endpoint', 'N/A')}")
    print(f"   Namespace: {cse_kg_config.get('namespace', 'N/A')}")
    print(f"   Local Cache: {cse_kg_config.get('local_cache', False)}")
    print(f"   Cache Directory: {cse_kg_config.get('cache_dir', 'N/A')}")
    
    print(f"\n2. ENTITY TYPES (What can be queried)")
    entity_types = cse_kg_config.get('entity_types', [])
    for i, entity_type in enumerate(entity_types, 1):
        print(f"   {i}. {entity_type}")
    
    print(f"\n3. RELATIONSHIP TYPES (How entities are connected)")
    relation_types = cse_kg_config.get('relation_types', [])
    for i, relation_type in enumerate(relation_types, 1):
        print(f"   {i}. {relation_type}")
        if relation_type == 'requiresKnowledge':
            print(f"      -> Concept A requiresKnowledge Concept B (prerequisite)")
        elif relation_type == 'isPrerequisiteOf':
            print(f"      -> Concept A isPrerequisiteOf Concept B (dependency)")
        elif relation_type == 'usesMethod':
            print(f"      -> Concept usesMethod Algorithm/Technique")
        elif relation_type == 'solvesTask':
            print(f"      -> Method solvesTask Problem")
        elif relation_type == 'relatedTo':
            print(f"      -> Concept A relatedTo Concept B (general relationship)")
    
    print(f"\n4. EXAMPLE SPARQL QUERIES")
    print(f"\n   Query 1: Get concept information")
    print(f"   PREFIX cskg: <{cse_kg_config.get('namespace', '')}>")
    print(f"   SELECT ?concept ?label WHERE {{")
    print(f"       ?concept rdfs:label ?label .")
    print(f"       FILTER(CONTAINS(LCASE(?label), \"recursion\"))")
    print(f"   }}")
    
    print(f"\n   Query 2: Get prerequisites")
    print(f"   PREFIX cskg: <{cse_kg_config.get('namespace', '')}>")
    print(f"   SELECT ?prereq WHERE {{")
    print(f"       cskg:recursion cskg:requiresKnowledge ?prereq .")
    print(f"   }}")
    
    print(f"\n   Query 3: Get related concepts")
    print(f"   PREFIX cskg: <{cse_kg_config.get('namespace', '')}>")
    print(f"   SELECT ?related WHERE {{")
    print(f"       {{ cskg:recursion cskg:relatedTo ?related . }}")
    print(f"       UNION")
    print(f"       {{ ?related cskg:relatedTo cskg:recursion . }}")
    print(f"   }}")
    
    print(f"\n5. CACHE STATUS")
    cache_dir = Path(cse_kg_config.get('cache_dir', 'data/cse_kg_cache'))
    if cache_dir.exists():
        cache_files = list(cache_dir.glob('*.pkl'))
        print(f"   Cache directory: {cache_dir}")
        print(f"   Cached queries: {len(cache_files)}")
        if cache_files:
            print(f"   Sample cached files:")
            for f in cache_files[:5]:
                print(f"      - {f.name}")
    else:
        print(f"   Cache directory does not exist yet: {cache_dir}")
        print(f"   Will be created on first query")
    
    print(f"\n6. WHAT DATA CAN BE EXTRACTED")
    print(f"\n   From CSE-KG 2.0, you can extract:")
    print(f"   - Concept definitions and descriptions")
    print(f"   - Prerequisite relationships (what to learn first)")
    print(f"   - Related concepts (what's similar)")
    print(f"   - Methods for solving tasks")
    print(f"   - Learning resources (papers, datasets)")
    print(f"   - Concept hierarchies (broader/narrower)")
    print(f"   - Common misconceptions")
    
    print(f"\n7. EXAMPLE CONCEPTS THAT CAN BE QUERIED")
    example_concepts = [
        "recursion",
        "object_oriented_programming",
        "linked_list",
        "sorting",
        "searching",
        "dynamic_programming",
        "tree",
        "graph",
        "hash_table",
        "stack",
        "queue"
    ]
    for concept in example_concepts:
        print(f"   - {concept}")
    
    print(f"\n8. HOW IT'S USED IN THE SYSTEM")
    print(f"\n   Step 1: Student code/question -> ConceptRetriever")
    print(f"   Step 2: Extract concepts from text/code")
    print(f"   Step 3: Query CSE-KG for:")
    print(f"           - Concept information")
    print(f"           - Prerequisites")
    print(f"           - Related concepts")
    print(f"           - Learning resources")
    print(f"   Step 4: Use this to:")
    print(f"           - Identify knowledge gaps")
    print(f"           - Suggest learning paths")
    print(f"           - Generate explanations")
    print(f"           - Recommend resources")
    
    print("\n" + "="*80)
    print("TO EXTRACT ACTUAL DATA:")
    print("="*80)
    print("1. Install dependencies:")
    print("   pip install SPARQLWrapper rdflib")
    print("\n2. Run the full extraction script:")
    print("   python extract_cse_kg_data.py")
    print("\n3. Or use the API:")
    print("   GET /api/concept/recursion")
    print("   POST /api/query/concepts")
    print("="*80)


def show_mooccubex_structure():
    """Show MOOCCubeX dataset structure"""
    print("\n" + "="*80)
    print("MOOCCubeX DATASET STRUCTURE")
    print("="*80)
    
    mooccubex_path = Path('data/moocsxcube')
    if not mooccubex_path.exists():
        print(f"   MOOCCubeX directory not found: {mooccubex_path}")
        return
    
    print(f"\n1. ENTITIES")
    entities_path = mooccubex_path / 'entities.json'
    if entities_path.exists():
        size_mb = entities_path.stat().st_size / (1024 * 1024)
        print(f"   entities.json: {size_mb:.2f} MB")
        print(f"   Contains: student, course, concept, video, problem, etc.")
    
    print(f"\n2. RELATIONS")
    relations_path = mooccubex_path / 'relations'
    if relations_path.exists():
        relation_files = list(relations_path.glob('*.txt'))
        relation_files.extend(list(relations_path.glob('*.json')))
        
        print(f"   Found {len(relation_files)} relation files:")
        for rel_file in relation_files[:10]:
            if rel_file.stat().st_size > 0:
                size_mb = rel_file.stat().st_size / (1024 * 1024)
                print(f"   - {rel_file.name}: {size_mb:.2f} MB")
    
    print(f"\n3. EXAMPLE RELATIONS")
    print(f"   - user-comment.txt: User -> Comment mappings")
    print(f"   - concept-video.txt: Concept -> Video mappings")
    print(f"   - concept-problem.txt: Concept -> Problem mappings")
    print(f"   - course-comment.txt: Course -> Comment mappings")
    
    print(f"\n4. HOW IT'S USED")
    print(f"   - Maps concepts to learning resources (videos, problems)")
    print(f"   - Tracks student-concept interactions")
    print(f"   - Provides learning paths")
    print(f"   - Enriches CSE-KG with educational data")


def main():
    """Main execution"""
    show_cse_kg_structure()
    show_mooccubex_structure()
    
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    print("\nCSE-KG 2.0 provides:")
    print("  - 26K+ computer science concepts")
    print("  - Relationships (prerequisites, related concepts)")
    print("  - Methods and algorithms")
    print("  - Learning resources")
    print("\nMOOCCubeX provides:")
    print("  - Concept-resource mappings (videos, problems)")
    print("  - Student interaction data")
    print("  - Learning path information")
    print("\nTogether, they enable:")
    print("  - Concept extraction from code/text")
    print("  - Knowledge gap identification")
    print("  - Personalized learning resource recommendations")
    print("  - Prerequisite analysis")
    print("="*80)


if __name__ == "__main__":
    main()

