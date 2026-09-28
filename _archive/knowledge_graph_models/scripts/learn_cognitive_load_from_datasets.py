"""
Learn Cognitive Load from ASSISTments and ProgSnap2 Datasets
Infers cognitive load from time spent, attempts, and error patterns
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

import pandas as pd
import json
from collections import defaultdict
from typing import Dict, List


class CognitiveLoadLearner:
    """Learn cognitive load from datasets"""
    
    def __init__(self):
        self.cognitive_loads = {}
    
    def learn_from_assistments(self, assistments_file: str = "data/assistments/skill_builder_data.csv") -> Dict:
        """
        Learn cognitive load from ASSISTments data
        
        Infers from:
        - attempt_count (more attempts = higher load)
        - wrong answers (errors = higher extraneous load)
        """
        print("=" * 60)
        print("LEARNING COGNITIVE LOAD FROM ASSISTMENTS")
        print("=" * 60)
        
        assistments_path = Path(assistments_file)
        if not assistments_path.exists():
            print(f"⚠ ASSISTments file not found: {assistments_path}")
            return {}
        
        try:
            df = pd.read_csv(assistments_path)
            print(f"✓ Loaded {len(df)} responses")
        except Exception as e:
            print(f"✗ Error loading ASSISTments: {e}")
            return {}
        
        # Group by skill/concept
        skill_loads = defaultdict(lambda: {
            "total_attempts": 0,
            "wrong_count": 0,
            "avg_attempts": 0.0,
            "students": set()
        })
        
        # Determine skill column
        skill_col = None
        for col in ['skill_name', 'skill_id', 'skill', 'concept']:
            if col in df.columns:
                skill_col = col
                break
        
        if skill_col is None:
            print("⚠ No skill column found")
            return {}
        
        # Analyze each skill
        for skill, group in df.groupby(skill_col):
            skill_loads[skill]["total_attempts"] = len(group)
            skill_loads[skill]["wrong_count"] = len(group[group.get('correct', 0) == 0])
            
            if 'attempt_count' in group.columns:
                skill_loads[skill]["avg_attempts"] = group['attempt_count'].mean()
            
            if 'user_id' in group.columns:
                skill_loads[skill]["students"].update(group['user_id'].unique())
        
        # Convert to cognitive loads
        cognitive_loads = {}
        for skill, data in skill_loads.items():
            if data["total_attempts"] < 5:  # Need at least 5 data points
                continue
            
            # Infer intrinsic load (concept complexity)
            # Higher wrong rate = higher intrinsic complexity
            wrong_rate = data["wrong_count"] / data["total_attempts"] if data["total_attempts"] > 0 else 0.0
            
            if wrong_rate > 0.5:
                intrinsic_load = 5
            elif wrong_rate > 0.3:
                intrinsic_load = 4
            elif wrong_rate > 0.2:
                intrinsic_load = 3
            else:
                intrinsic_load = 2
            
            # Infer extraneous load (from attempts)
            # More attempts = higher extraneous load (confusion, poor presentation)
            avg_attempts = data["avg_attempts"] or 1.0
            if avg_attempts > 3:
                extraneous_load = min(5, intrinsic_load + 2)
            elif avg_attempts > 2:
                extraneous_load = min(5, intrinsic_load + 1)
            else:
                extraneous_load = intrinsic_load
            
            # Germane load (inverse of extraneous)
            germane_load = max(1, 5 - extraneous_load)
            
            # Total load
            total_load = max(intrinsic_load, extraneous_load)
            
            cognitive_loads[skill] = {
                "concept": skill,
                "intrinsic_load": intrinsic_load,
                "extraneous_load": extraneous_load,
                "germane_load": germane_load,
                "total_load": total_load,
                "factors": [
                    f"wrong_rate_{wrong_rate:.2f}",
                    f"avg_attempts_{avg_attempts:.2f}",
                    f"affected_students_{len(data['students'])}"
                ],
                "source": "assistments",
                "evidence_count": data["total_attempts"]
            }
            
            print(f"\n✓ Learned cognitive load for: {skill}")
            print(f"  Intrinsic: {intrinsic_load}, Extraneous: {extraneous_load}, Total: {total_load}")
            print(f"  Evidence: {data['total_attempts']} responses, {len(data['students'])} students")
        
        return cognitive_loads
    
    def learn_from_progsnap2(self, progsnap_file: str = "data/progsnap2/MainTable_cs1.csv") -> Dict:
        """
        Learn cognitive load from ProgSnap2 data
        
        Infers from:
        - Time between actions (longer = higher load)
        - Error frequency (more errors = higher load)
        - Session duration
        """
        print("\n" + "=" * 60)
        print("LEARNING COGNITIVE LOAD FROM PROGSNAP2")
        print("=" * 60)
        
        progsnap_path = Path(progsnap_file)
        if not progsnap_path.exists():
            print(f"⚠ ProgSnap2 file not found: {progsnap_path}")
            return {}
        
        try:
            df = pd.read_csv(progsnap_path, nrows=50000)  # Sample for performance
            print(f"✓ Loaded {len(df)} events")
        except Exception as e:
            print(f"✗ Error loading ProgSnap2: {e}")
            return {}
        
        # Group by problem (concept)
        problem_loads = defaultdict(lambda: {
            "sessions": [],
            "error_count": 0,
            "total_time": 0.0,
            "avg_time_per_session": 0.0
        })
        
        # Group by ProblemID
        for problem_id, group in df.groupby('ProblemID'):
            # Calculate session metrics
            for subject_id, subject_group in group.groupby('SubjectID'):
                session_events = len(subject_group)
                errors = len(subject_group[subject_group['EventType'].str.contains('Error', na=False)])
                
                # Estimate time (if timestamps available)
                if 'ServerTimestamp' in subject_group.columns:
                    timestamps = pd.to_numeric(subject_group['ServerTimestamp'], errors='coerce')
                    if timestamps.notna().any():
                        time_span = timestamps.max() - timestamps.min()
                        problem_loads[problem_id]["total_time"] += time_span
                
                problem_loads[problem_id]["sessions"].append({
                    "events": session_events,
                    "errors": errors
                })
                problem_loads[problem_id]["error_count"] += errors
        
        # Convert to cognitive loads
        cognitive_loads = {}
        for problem_id, data in problem_loads.items():
            if len(data["sessions"]) < 3:  # Need at least 3 sessions
                continue
            
            # Calculate averages
            avg_events = sum(s["events"] for s in data["sessions"]) / len(data["sessions"])
            avg_errors = data["error_count"] / len(data["sessions"])
            avg_time = data["total_time"] / len(data["sessions"]) if data["total_time"] > 0 else 0
            
            # Infer intrinsic load (from problem complexity)
            # More events/errors = more complex
            if avg_events > 20 or avg_errors > 5:
                intrinsic_load = 5
            elif avg_events > 15 or avg_errors > 3:
                intrinsic_load = 4
            elif avg_events > 10 or avg_errors > 2:
                intrinsic_load = 3
            else:
                intrinsic_load = 2
            
            # Infer extraneous load (from time and errors)
            # Longer time or more errors = higher extraneous load
            if avg_time > 300 or avg_errors > 3:  # 5 minutes or 3+ errors
                extraneous_load = min(5, intrinsic_load + 2)
            elif avg_time > 120 or avg_errors > 1:  # 2 minutes or 1+ error
                extraneous_load = min(5, intrinsic_load + 1)
            else:
                extraneous_load = intrinsic_load
            
            # Germane load
            germane_load = max(1, 5 - extraneous_load)
            
            # Total load
            total_load = max(intrinsic_load, extraneous_load)
            
            # Map problem_id to concept (simplified)
            concept = f"problem_{problem_id}"  # Could be improved with problem metadata
            
            cognitive_loads[concept] = {
                "concept": concept,
                "intrinsic_load": intrinsic_load,
                "extraneous_load": extraneous_load,
                "germane_load": germane_load,
                "total_load": total_load,
                "factors": [
                    f"avg_events_{avg_events:.1f}",
                    f"avg_errors_{avg_errors:.1f}",
                    f"avg_time_{avg_time:.1f}s"
                ],
                "source": "progsnap2",
                "evidence_count": len(data["sessions"])
            }
            
            print(f"\n✓ Learned cognitive load for: {concept}")
            print(f"  Intrinsic: {intrinsic_load}, Extraneous: {extraneous_load}, Total: {total_load}")
            print(f"  Evidence: {len(data['sessions'])} sessions")
        
        return cognitive_loads
    
    def save_cognitive_loads(self, cognitive_loads: Dict, output_file: str = "data/pedagogical_kg/cognitive_loads.json"):
        """Save learned cognitive loads"""
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Load existing and merge
        existing_loads = []
        if output_path.exists():
            with open(output_path, 'r', encoding='utf-8') as f:
                existing_loads = json.load(f)
        
        existing_concepts = {cl.get('concept') for cl in existing_loads}
        new_loads = [cl for cl in cognitive_loads.values() if cl.get('concept') not in existing_concepts]
        
        all_loads = existing_loads + new_loads
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(all_loads, f, indent=2, ensure_ascii=False)
        
        print(f"\n✓ Saved {len(new_loads)} new cognitive loads to {output_path}")
        print(f"  Total cognitive loads: {len(all_loads)}")
        return output_path


def main():
    """Main function"""
    learner = CognitiveLoadLearner()
    
    all_loads = {}
    
    # Learn from ASSISTments
    assistments_loads = learner.learn_from_assistments()
    all_loads.update(assistments_loads)
    
    # Learn from ProgSnap2
    progsnap_loads = learner.learn_from_progsnap2()
    all_loads.update(progsnap_loads)
    
    if not all_loads:
        print("\n⚠ No cognitive loads learned. Check datasets.")
        return
    
    # Save
    output_path = learner.save_cognitive_loads(all_loads)
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Total cognitive loads learned: {len(all_loads)}")
    print(f"  From ASSISTments: {len(assistments_loads)}")
    print(f"  From ProgSnap2: {len(progsnap_loads)}")
    print(f"Output file: {output_path}")


if __name__ == "__main__":
    main()





