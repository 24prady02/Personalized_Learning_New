"""
Learn Misconceptions from MOOCCubeX Dataset
Extracts conceptual misconceptions from prerequisites, concept relationships, and student activity patterns
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

import json
import re
from collections import defaultdict, Counter
from typing import Dict, List, Tuple
import pandas as pd


class MOOCCubeXMisconceptionLearner:
    """Learn misconceptions from MOOCCubeX prerequisite and concept relationship data"""
    
    def __init__(self, mooccubex_dir: str = "data/moocsxcube"):
        self.mooccubex_dir = Path(mooccubex_dir)
        self.misconceptions = []
        
        # Concept name normalization (MOOCCubeX uses Chinese, we map to English)
        self.concept_mapping = {
            "递归": "recursion",
            "循环": "loops",
            "数组": "arrays",
            "函数": "functions",
            "变量": "variables",
            "条件语句": "conditional_statements",
            "数据结构": "data_structures",
            "算法": "algorithms",
            "面向对象": "object_oriented_programming",
            "类": "classes",
            "继承": "inheritance",
            "多态": "polymorphism",
            "列表": "lists",
            "字典": "dictionaries",
            "树": "trees",
            "图": "graphs",
            "排序": "sorting",
            "搜索": "searching"
        }
    
    def load_prerequisites(self) -> Dict:
        """Load prerequisite data from MOOCCubeX"""
        print("=" * 60)
        print("LOADING MOOCCUBEX PREREQUISITES")
        print("=" * 60)
        
        prerequisites = {}
        prereq_files = [
            self.mooccubex_dir / "prerequisites" / "cs.json",
            self.mooccubex_dir / "prerequisites" / "math.json"
        ]
        
        for prereq_file in prereq_files:
            if prereq_file.exists():
                print(f"\nLoading {prereq_file.name}...")
                try:
                    # Read line by line (JSONL format)
                    with open(prereq_file, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                        print(f"  Found {len(lines)} prerequisite pairs")
                        
                        for line in lines[:10000]:  # Limit for performance
                            try:
                                data = json.loads(line.strip())
                                c1 = data.get('c1', '')
                                c2 = data.get('c2', '')
                                ground_truth = data.get('ground_truth', 0)
                                
                                if c1 and c2:
                                    key = (c1, c2)
                                    prerequisites[key] = {
                                        'is_prerequisite': ground_truth == 1,
                                        'confidence': data.get('graph_predict', [0, 0])[1] if 'graph_predict' in data else 0.5
                                    }
                            except json.JSONDecodeError:
                                continue
                except Exception as e:
                    print(f"  [WARN] Error loading {prereq_file.name}: {e}")
        
        print(f"\n[OK] Loaded {len(prerequisites)} prerequisite pairs")
        return prerequisites
    
    def load_concept_problems(self) -> Dict:
        """Load concept-problem relationships"""
        print("\n" + "=" * 60)
        print("LOADING CONCEPT-PROBLEM RELATIONSHIPS")
        print("=" * 60)
        
        concept_problems = defaultdict(list)
        concept_file = self.mooccubex_dir / "relations" / "concept-problem.txt"
        
        if concept_file.exists():
            try:
                with open(concept_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    print(f"  Found {len(lines)} concept-problem relationships")
                    
                    for line in lines[:5000]:  # Limit for performance
                        parts = line.strip().split('\t')
                        if len(parts) >= 2:
                            concept = parts[0]
                            problem = parts[1]
                            concept_problems[concept].append(problem)
            except Exception as e:
                print(f"  [WARN] Error loading concept-problem: {e}")
        
        print(f"[OK] Loaded relationships for {len(concept_problems)} concepts")
        return dict(concept_problems)
    
    def extract_prerequisite_misconceptions(self, prerequisites: Dict) -> List[Dict]:
        """Extract misconceptions from incorrect prerequisite beliefs"""
        print("\n" + "=" * 60)
        print("EXTRACTING PREREQUISITE MISCONCEPTIONS")
        print("=" * 60)
        
        misconceptions = []
        
        # Group by concept pairs
        concept_pair_errors = defaultdict(lambda: {
            'incorrect_beliefs': 0,
            'correct_relationships': 0,
            'total': 0
        })
        
        for (c1, c2), data in prerequisites.items():
            # Normalize concept names
            concept1 = self._normalize_concept(c1)
            concept2 = self._normalize_concept(c2)
            
            if concept1 == concept2 or not concept1 or not concept2:
                continue
            
            key = (concept1, concept2)
            concept_pair_errors[key]['total'] += 1
            
            if not data['is_prerequisite']:
                # This is NOT a prerequisite, but students might think it is
                concept_pair_errors[key]['incorrect_beliefs'] += 1
            else:
                concept_pair_errors[key]['correct_relationships'] += 1
        
        # Create misconceptions for common incorrect prerequisite beliefs
        for (concept1, concept2), data in concept_pair_errors.items():
            if data['incorrect_beliefs'] >= 3:  # Need at least 3 occurrences
                error_rate = data['incorrect_beliefs'] / data['total'] if data['total'] > 0 else 0
                
                if error_rate > 0.3:  # At least 30% error rate
                    # Create ASCII-safe ID
                    concept1_id = self._create_safe_id(concept1)
                    concept2_id = self._create_safe_id(concept2)
                    misconception = {
                        "id": f"mc_prereq_{concept1_id}_to_{concept2_id}",
                        "concept": concept1,
                        "description": f"Believes {concept2} is a prerequisite for {concept1} (incorrect)",
                        "common_indicators": [
                            f"confuses {concept1} with {concept2}",
                            f"thinks {concept2} must be learned before {concept1}",
                            f"incorrect prerequisite relationship"
                        ],
                        "severity": "medium",
                        "frequency": round(error_rate, 3),
                        "related_concepts": [concept2],
                        "correction_strategy": f"Clarify that {concept2} is not required before learning {concept1}. Show correct prerequisite path.",
                        "source": "mooccubex",
                        "evidence_count": data['incorrect_beliefs'],
                        "misconception_type": "prerequisite_confusion"
                    }
                    misconceptions.append(misconception)
                    # Print summary (use counter to avoid encoding issues)
                    print(f"\n[OK] Extracted prerequisite misconception #{len(misconceptions)}")
                    print(f"  Error rate: {error_rate:.1%}, Evidence: {data['incorrect_beliefs']} incorrect beliefs")
        
        return misconceptions
    
    def extract_concept_relationship_misconceptions(self, concept_problems: Dict) -> List[Dict]:
        """Extract misconceptions from concept-problem relationship patterns"""
        print("\n" + "=" * 60)
        print("EXTRACTING CONCEPT RELATIONSHIP MISCONCEPTIONS")
        print("=" * 60)
        
        misconceptions = []
        
        # Find concepts that are frequently confused (appear in similar problem sets)
        concept_similarity = defaultdict(set)
        
        for concept, problems in concept_problems.items():
            normalized = self._normalize_concept(concept)
            if normalized:
                concept_similarity[normalized].update(problems)
        
        # Find concepts with overlapping problem sets (might be confused)
        concept_pairs = []
        concepts_list = list(concept_similarity.keys())
        
        for i, concept1 in enumerate(concepts_list):
            for concept2 in concepts_list[i+1:]:
                overlap = len(concept_similarity[concept1] & concept_similarity[concept2])
                total1 = len(concept_similarity[concept1])
                total2 = len(concept_similarity[concept2])
                
                if overlap > 0 and total1 > 0 and total2 > 0:
                    similarity = overlap / max(total1, total2)
                    if similarity > 0.5:  # High overlap
                        concept_pairs.append((concept1, concept2, similarity, overlap))
        
        # Create misconceptions for frequently confused concepts
        for concept1, concept2, similarity, overlap in concept_pairs[:10]:  # Top 10
            # Create ASCII-safe IDs
            concept1_id = self._create_safe_id(concept1)
            concept2_id = self._create_safe_id(concept2)
            misconception = {
                "id": f"mc_confusion_{concept1_id}_and_{concept2_id}",
                "concept": concept1,
                "description": f"Confuses {concept1} with {concept2} due to similar problem contexts",
                "common_indicators": [
                    f"uses {concept1} when {concept2} is needed",
                    f"applies {concept2} to {concept1} problems",
                    f"overlapping problem contexts"
                ],
                "severity": "medium",
                "frequency": round(similarity, 3),
                "related_concepts": [concept2],
                "correction_strategy": f"Clarify differences between {concept1} and {concept2}. Show distinct use cases and problem types.",
                "source": "mooccubex",
                "evidence_count": overlap,
                "misconception_type": "concept_confusion"
            }
            misconceptions.append(misconception)
            # Print summary (use counter to avoid encoding issues)
            print(f"\n[OK] Extracted concept confusion #{len(misconceptions)}")
            print(f"  Similarity: {similarity:.1%}, Overlapping problems: {overlap}")
        
        return misconceptions
    
    def _create_safe_id(self, concept: str) -> str:
        """Create ASCII-safe ID from concept name"""
        # Remove non-ASCII characters and replace spaces/underscores
        safe = ''.join(c if c.isalnum() or c in '_-' else '_' for c in concept)
        # Limit length
        return safe[:30] if safe else "concept"
    
    def _normalize_concept(self, concept: str) -> str:
        """Normalize concept name (Chinese to English, or keep English)"""
        # Check direct mapping
        if concept in self.concept_mapping:
            return self.concept_mapping[concept]
        
        # Try to find English equivalent
        concept_lower = concept.lower()
        for chinese, english in self.concept_mapping.items():
            if chinese in concept or concept in chinese:
                return english
        
        # If already in English or common CS terms, return as-is
        common_terms = [
            "recursion", "loops", "arrays", "functions", "variables",
            "conditional", "data_structures", "algorithms", "object_oriented",
            "classes", "inheritance", "polymorphism", "lists", "dictionaries",
            "trees", "graphs", "sorting", "searching"
        ]
        
        for term in common_terms:
            if term in concept_lower:
                return term
        
        # Return normalized version (lowercase, replace spaces)
        return concept_lower.replace(' ', '_').replace('-', '_')
    
    def save_misconceptions(self, misconceptions: List[Dict], 
                          output_file: str = "data/pedagogical_kg/misconceptions_learned_mooccubex.json"):
        """Save learned misconceptions to file"""
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(misconceptions, f, indent=2, ensure_ascii=False)
        
        print(f"\n[OK] Saved {len(misconceptions)} misconceptions to {output_path}")
        return output_path


def main():
    """Main function"""
    learner = MOOCCubeXMisconceptionLearner()
    
    # Load MOOCCubeX data
    prerequisites = learner.load_prerequisites()
    concept_problems = learner.load_concept_problems()
    
    if not prerequisites and not concept_problems:
        print("\n[WARN] No MOOCCubeX data found. Make sure data is downloaded.")
        return
    
    all_misconceptions = []
    
    # Extract prerequisite misconceptions
    if prerequisites:
        prereq_misconceptions = learner.extract_prerequisite_misconceptions(prerequisites)
        all_misconceptions.extend(prereq_misconceptions)
    
    # Extract concept relationship misconceptions
    if concept_problems:
        relationship_misconceptions = learner.extract_concept_relationship_misconceptions(concept_problems)
        all_misconceptions.extend(relationship_misconceptions)
    
    if not all_misconceptions:
        print("\n[WARN] No misconceptions extracted. Check MOOCCubeX data format.")
        return
    
    # Save misconceptions
    output_path = learner.save_misconceptions(all_misconceptions)
    
    # Merge with existing misconceptions
    existing_file = Path("data/pedagogical_kg/misconceptions.json")
    if existing_file.exists():
        with open(existing_file, 'r', encoding='utf-8') as f:
            existing = json.load(f)
        
        # Add new misconceptions
        merged = existing + all_misconceptions
        with open(existing_file, 'w', encoding='utf-8') as f:
            json.dump(merged, f, indent=2, ensure_ascii=False)
        
        print(f"\n[OK] Merged {len(all_misconceptions)} new misconceptions with {len(existing)} existing")
        print(f"  Total misconceptions: {len(merged)}")
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Prerequisite misconceptions: {len([m for m in all_misconceptions if m.get('misconception_type') == 'prerequisite_confusion'])}")
    print(f"Concept confusion misconceptions: {len([m for m in all_misconceptions if m.get('misconception_type') == 'concept_confusion'])}")
    print(f"Total new misconceptions: {len(all_misconceptions)}")
    print(f"Output file: {output_path}")
    print("\nNext step: Misconceptions are now merged into misconceptions.json")


if __name__ == "__main__":
    main()

