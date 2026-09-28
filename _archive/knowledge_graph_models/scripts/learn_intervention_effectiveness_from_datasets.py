"""
Learn Intervention Effectiveness from ASSISTments Dataset
Extracts which interventions/strategies lead to correct answers
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

import pandas as pd
import json
from collections import defaultdict
from typing import Dict, List


class InterventionEffectivenessLearner:
    """Learn intervention effectiveness from datasets"""
    
    def __init__(self):
        self.interventions = {}
    
    def learn_from_assistments(self, assistments_file: str = "data/assistments/skill_builder_data.csv") -> Dict:
        """
        Learn intervention effectiveness from ASSISTments
        
        Infers from:
        - Wrong → Correct transitions (what helped student succeed)
        - Attempt patterns (which strategies work)
        """
        print("=" * 60)
        print("LEARNING INTERVENTION EFFECTIVENESS FROM ASSISTMENTS")
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
        
        # Group by user and skill to track learning progression
        interventions = defaultdict(lambda: {
            "success_count": 0,
            "total_usage": 0,
            "concepts": set(),
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
        
        # Track wrong → correct transitions (indicates effective intervention)
        for (user_id, skill), group in df.groupby(['user_id', skill_col]):
            group_sorted = group.sort_values('attempt_count')
            
            # Find wrong → correct transitions
            for i in range(len(group_sorted) - 1):
                current = group_sorted.iloc[i]
                next_row = group_sorted.iloc[i + 1]
                
                # If went from wrong to correct, something helped!
                if current.get('correct', 0) == 0 and next_row.get('correct', 0) == 1:
                    # Infer intervention type from attempt pattern
                    attempt_diff = next_row.get('attempt_count', 1) - current.get('attempt_count', 1)
                    
                    if attempt_diff == 1:
                        # Immediate success after one attempt
                        intervention_type = "example"  # Likely saw an example
                    elif attempt_diff <= 3:
                        # Success after a few attempts
                        intervention_type = "practice"  # Practice helped
                    else:
                        # Success after many attempts
                        intervention_type = "explanation"  # Explanation helped
                    
                    intervention_id = f"int_{intervention_type}_{skill}"
                    interventions[intervention_id]["success_count"] += 1
                    interventions[intervention_id]["total_usage"] += 1
                    interventions[intervention_id]["concepts"].add(skill)
                    interventions[intervention_id]["students"].add(user_id)
        
        # Also track direct successes (first attempt correct)
        for (user_id, skill), group in df.groupby(['user_id', skill_col]):
            first_attempt = group[group.get('attempt_count', 1) == 1]
            if len(first_attempt) > 0 and first_attempt.iloc[0].get('correct', 0) == 1:
                # Student got it right first try (good prior knowledge or good initial explanation)
                intervention_id = f"int_initial_explanation_{skill}"
                interventions[intervention_id]["success_count"] += 1
                interventions[intervention_id]["total_usage"] += 1
                interventions[intervention_id]["concepts"].add(skill)
                interventions[intervention_id]["students"].add(user_id)
        
        # Convert to interventions
        learned_interventions = {}
        for intervention_id, data in interventions.items():
            if data["total_usage"] < 3:  # Need at least 3 occurrences
                continue
            
            # Calculate effectiveness
            effectiveness = data["success_count"] / data["total_usage"] if data["total_usage"] > 0 else 0.0
            
            # Extract intervention type and concept
            parts = intervention_id.split('_')
            if len(parts) >= 3:
                intervention_type = parts[1]  # example, practice, explanation
                concept = '_'.join(parts[2:])  # skill name
            else:
                intervention_type = "explanation"
                concept = "general"
            
            # Map to InterventionType enum
            type_map = {
                "example": "example",
                "practice": "practice",
                "explanation": "explanation",
                "initial_explanation": "explanation"
            }
            
            learned_interventions[intervention_id] = {
                "id": intervention_id,
                "name": f"{intervention_type.title()} for {concept}",
                "type": type_map.get(intervention_type, "explanation"),
                "target_concept": concept,
                "description": f"Effective {intervention_type} intervention for {concept}",
                "content_template": f"Use {intervention_type} approach for {concept}",
                "effectiveness_score": effectiveness,
                "usage_count": data["total_usage"],
                "source": "assistments",
                "evidence_count": data["success_count"]
            }
            
            print(f"\n✓ Learned intervention: {intervention_id}")
            print(f"  Type: {intervention_type}, Concept: {concept}")
            print(f"  Effectiveness: {effectiveness:.1%} ({data['success_count']}/{data['total_usage']})")
            print(f"  Evidence: {len(data['students'])} students, {len(data['concepts'])} concepts")
        
        return learned_interventions
    
    def learn_from_progsnap2(self, progsnap_file: str = "data/progsnap2/MainTable_cs1.csv") -> Dict:
        """
        Learn intervention effectiveness from ProgSnap2
        
        Infers from:
        - Action sequences that lead to success
        - Help requests → success (effective help)
        - Resource views → success (effective resources)
        """
        print("\n" + "=" * 60)
        print("LEARNING INTERVENTION EFFECTIVENESS FROM PROGSNAP2")
        print("=" * 60)
        
        progsnap_path = Path(progsnap_file)
        if not progsnap_path.exists():
            print(f"⚠ ProgSnap2 file not found: {progsnap_path}")
            return {}
        
        try:
            df = pd.read_csv(progsnap_path, nrows=50000)  # Sample
            print(f"✓ Loaded {len(df)} events")
        except Exception as e:
            print(f"✗ Error loading ProgSnap2: {e}")
            return {}
        
        interventions = defaultdict(lambda: {
            "success_count": 0,
            "total_usage": 0,
            "sessions": []
        })
        
        # Group by session (SubjectID + ProblemID)
        for (subject_id, problem_id), group in df.groupby(['SubjectID', 'ProblemID']):
            group_sorted = group.sort_values('ServerTimestamp')
            events = group_sorted['EventType'].tolist()
            
            # Check if session ended successfully
            has_success = 'Run.Success' in events or 'Compile.Success' in events or 'Submit' in events
            has_error = any('Error' in str(e) for e in events)
            
            # Track interventions that led to success
            if has_success:
                # Check what happened before success
                if 'Help.Request' in events:
                    # Help request → success
                    intervention_id = "int_help_request_success"
                    interventions[intervention_id]["success_count"] += 1
                    interventions[intervention_id]["total_usage"] += 1
                
                if 'Resource.View' in events or 'Webpage.Open' in events:
                    # Resource view → success
                    intervention_id = "int_resource_view_success"
                    interventions[intervention_id]["success_count"] += 1
                    interventions[intervention_id]["total_usage"] += 1
                
                if 'File.Edit' in events and events.count('File.Edit') > 2:
                    # Multiple edits → success (practice/iteration)
                    intervention_id = "int_iterative_practice_success"
                    interventions[intervention_id]["success_count"] += 1
                    interventions[intervention_id]["total_usage"] += 1
            
            # Track interventions that didn't help
            if has_error and not has_success:
                if 'Help.Request' in events:
                    intervention_id = "int_help_request_failure"
                    interventions[intervention_id]["total_usage"] += 1
        
        # Convert to interventions
        learned_interventions = {}
        for intervention_id, data in interventions.items():
            if data["total_usage"] < 5:  # Need at least 5 occurrences
                continue
            
            effectiveness = data["success_count"] / data["total_usage"] if data["total_usage"] > 0 else 0.0
            
            # Extract type
            if "help_request" in intervention_id:
                intervention_type = "help"
                name = "Help Request"
            elif "resource_view" in intervention_id:
                intervention_type = "resource"
                name = "Resource View"
            elif "iterative_practice" in intervention_id:
                intervention_type = "practice"
                name = "Iterative Practice"
            else:
                intervention_type = "explanation"
                name = "General Intervention"
            
            learned_interventions[intervention_id] = {
                "id": intervention_id,
                "name": name,
                "type": intervention_type,
                "target_concept": "general",
                "description": f"{name} intervention",
                "content_template": f"Use {name} approach",
                "effectiveness_score": effectiveness,
                "usage_count": data["total_usage"],
                "source": "progsnap2",
                "evidence_count": data["success_count"]
            }
            
            print(f"\n✓ Learned intervention: {intervention_id}")
            print(f"  Effectiveness: {effectiveness:.1%} ({data['success_count']}/{data['total_usage']})")
        
        return learned_interventions
    
    def save_interventions(self, interventions: Dict, output_file: str = "data/pedagogical_kg/interventions.json"):
        """Save learned interventions"""
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Load existing and merge
        existing_interventions = []
        if output_path.exists():
            with open(output_path, 'r', encoding='utf-8') as f:
                existing_interventions = json.load(f)
        
        existing_ids = {intv.get('id') for intv in existing_interventions}
        new_interventions = [intv for intv in interventions.values() if intv.get('id') not in existing_ids]
        
        all_interventions = existing_interventions + new_interventions
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(all_interventions, f, indent=2, ensure_ascii=False)
        
        print(f"\n✓ Saved {len(new_interventions)} new interventions to {output_path}")
        print(f"  Total interventions: {len(all_interventions)}")
        return output_path


def main():
    """Main function"""
    learner = InterventionEffectivenessLearner()
    
    all_interventions = {}
    
    # Learn from ASSISTments
    assistments_interventions = learner.learn_from_assistments()
    all_interventions.update(assistments_interventions)
    
    # Learn from ProgSnap2
    progsnap_interventions = learner.learn_from_progsnap2()
    all_interventions.update(progsnap_interventions)
    
    if not all_interventions:
        print("\n⚠ No interventions learned. Check datasets.")
        return
    
    # Save
    output_path = learner.save_interventions(all_interventions)
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Total interventions learned: {len(all_interventions)}")
    print(f"  From ASSISTments: {len(assistments_interventions)}")
    print(f"  From ProgSnap2: {len(progsnap_interventions)}")
    print(f"Output file: {output_path}")


if __name__ == "__main__":
    main()





