"""
Learn Learning Progressions from MOOCCubeX Dataset
Extracts concept sequences and prerequisites from course data
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

import json
from collections import defaultdict
from typing import Dict, List
import networkx as nx


class MOOCCubeXProgressionLearner:
    """Learn learning progressions from MOOCCubeX course data"""
    
    def __init__(self, mooccubex_dir: str = "data/moocsxcube"):
        self.mooccubex_dir = Path(mooccubex_dir)
        self.progressions = []
    
    def load_mooccubex_data(self) -> Dict:
        """Load MOOCCubeX entities and prerequisites"""
        print("=" * 60)
        print("LOADING MOOCCUBEX DATA")
        print("=" * 60)
        
        data = {}
        
        # Load concepts
        concepts_file = self.mooccubex_dir / "entities" / "concept.json"
        if concepts_file.exists():
            with open(concepts_file, 'r', encoding='utf-8') as f:
                data['concepts'] = json.load(f)
                print(f"✓ Loaded {len(data['concepts'])} concepts")
        
        # Load prerequisites
        prereq_files = [
            self.mooccubex_dir / "prerequisites" / "cs.json",
            self.mooccubex_dir / "prerequisites" / "math.json"
        ]
        
        data['prerequisites'] = {}
        for prereq_file in prereq_files:
            if prereq_file.exists():
                with open(prereq_file, 'r', encoding='utf-8') as f:
                    prereqs = json.load(f)
                    data['prerequisites'].update(prereqs)
                    print(f"✓ Loaded prerequisites from {prereq_file.name}")
        
        # Load course-concept relationships
        relations_file = self.mooccubex_dir / "relations" / "course-field.json"
        if relations_file.exists():
            with open(relations_file, 'r', encoding='utf-8') as f:
                data['course_concepts'] = json.load(f)
                print(f"✓ Loaded course-concept relationships")
        
        return data
    
    def extract_progressions(self, data: Dict) -> List[Dict]:
        """Extract learning progressions from MOOCCubeX data"""
        print("\n" + "=" * 60)
        print("EXTRACTING LEARNING PROGRESSIONS")
        print("=" * 60)
        
        progressions = []
        
        # Build prerequisite graph
        prereq_graph = nx.DiGraph()
        
        # Add prerequisites to graph
        for concept, prereqs in data.get('prerequisites', {}).items():
            if isinstance(prereqs, list):
                for prereq in prereqs:
                    prereq_graph.add_edge(prereq, concept)
            elif isinstance(prereqs, dict):
                for prereq in prereqs.get('prerequisites', []):
                    prereq_graph.add_edge(prereq, concept)
        
        # Find all paths (progressions) in graph
        # Get concepts with no prerequisites (starting points)
        starting_concepts = [n for n in prereq_graph.nodes() if prereq_graph.in_degree(n) == 0]
        
        # For each starting concept, find paths to advanced concepts
        for start_concept in starting_concepts[:10]:  # Limit for performance
            # Find all reachable concepts
            reachable = nx.descendants(prereq_graph, start_concept)
            
            if not reachable:
                continue
            
            # Build progression sequence using topological sort
            try:
                subgraph = prereq_graph.subgraph([start_concept] + list(reachable))
                topo_order = list(nx.topological_sort(subgraph))
                
                if len(topo_order) >= 3:  # Need at least 3 concepts
                    progression = self._create_progression(topo_order, prereq_graph)
                    if progression:
                        progressions.append(progression)
                        print(f"\n✓ Extracted progression: {progression['id']}")
                        print(f"  Concepts: {len(progression['concept_sequence'])} concepts")
            except nx.NetworkXError:
                # Cycle detected, skip
                continue
        
        return progressions
    
    def _create_progression(self, concept_sequence: List[str], graph: nx.DiGraph) -> Dict:
        """Create learning progression from concept sequence"""
        if not concept_sequence:
            return None
        
        # Determine difficulty levels (1-5 scale)
        difficulty_levels = []
        for i, concept in enumerate(concept_sequence):
            # Earlier concepts are easier
            difficulty = min(5, 1 + (i * 4) // len(concept_sequence))
            difficulty_levels.append(difficulty)
        
        # Extract prerequisites
        prerequisites = {}
        for concept in concept_sequence:
            prereqs = list(graph.predecessors(concept))
            if prereqs:
                prerequisites[concept] = prereqs
        
        # Estimate time (based on difficulty)
        estimated_time = {}
        for i, concept in enumerate(concept_sequence):
            # More difficult concepts take more time
            time_hours = 1.0 + (difficulty_levels[i] * 0.5)
            estimated_time[concept] = time_hours
        
        # Mastery thresholds (higher for foundational concepts)
        mastery_thresholds = {}
        for i, concept in enumerate(concept_sequence):
            if i < len(concept_sequence) // 2:
                # Foundational concepts need higher mastery
                threshold = 0.85
            else:
                # Advanced concepts
                threshold = 0.75
            mastery_thresholds[concept] = threshold
        
        progression_id = f"prog_{concept_sequence[0]}_to_{concept_sequence[-1]}"
        
        return {
            "id": progression_id,
            "concept_sequence": concept_sequence,
            "difficulty_levels": difficulty_levels,
            "prerequisites": prerequisites,
            "estimated_time": estimated_time,
            "mastery_thresholds": mastery_thresholds,
            "source": "mooccubex"
        }
    
    def save_progressions(self, progressions: List[Dict], output_file: str = "data/pedagogical_kg/learning_progressions.json"):
        """Save learned progressions to file"""
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Load existing progressions and merge
        existing_progressions = []
        if output_path.exists():
            with open(output_path, 'r', encoding='utf-8') as f:
                existing_progressions = json.load(f)
        
        # Merge (avoid duplicates)
        existing_ids = {p.get('id') for p in existing_progressions}
        new_progressions = [p for p in progressions if p.get('id') not in existing_ids]
        
        all_progressions = existing_progressions + new_progressions
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(all_progressions, f, indent=2, ensure_ascii=False)
        
        print(f"\n✓ Saved {len(new_progressions)} new progressions to {output_path}")
        print(f"  Total progressions: {len(all_progressions)}")
        return output_path


def main():
    """Main function"""
    learner = MOOCCubeXProgressionLearner()
    
    try:
        # Load MOOCCubeX data
        data = learner.load_mooccubex_data()
        
        if not data.get('prerequisites'):
            print("\n⚠ No prerequisites found. Check MOOCCubeX data.")
            return
        
        # Extract progressions
        progressions = learner.extract_progressions(data)
        
        if not progressions:
            print("\n⚠ No progressions extracted. Check data format.")
            return
        
        # Save progressions
        output_path = learner.save_progressions(progressions)
        
        print("\n" + "=" * 60)
        print("SUMMARY")
        print("=" * 60)
        print(f"Total progressions extracted: {len(progressions)}")
        print(f"Output file: {output_path}")
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()





