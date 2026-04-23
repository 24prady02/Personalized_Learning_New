"""
Learn COKE Cognitive Chains from ProgSnap2 Action Sequences
Extracts cognitive state → behavioral response patterns
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

import pandas as pd
import json
from collections import defaultdict, Counter
from typing import Dict, List, Tuple
import re


class ProgSnap2COKELearner:
    """Learn COKE chains from ProgSnap2 debugging sessions"""
    
    def __init__(self, progsnap_dir: str = "data/progsnap2"):
        self.progsnap_dir = Path(progsnap_dir)
        self.cognitive_chains = []
        
        # Event type to behavioral response mapping
        self.event_to_behavior = {
            "Run.Program": "try_again",
            "Compile.Error": "try_again",
            "Run.Error": "try_again",
            "File.Edit": "try_again",
            "File.Open": "search_info",
            "Webpage.Open": "search_info",
            "Webpage.Close": "search_info",
            "Webpage.Focus": "search_info",
            "Submit": "continue",
            "HelpRequest": "ask_question",
            "Resource.View": "search_info",
            "Video.Play": "search_info",
            "Video.Pause": "search_info",
            "Video.Seek": "search_info"
        }
        
        # Patterns that indicate cognitive states
        self.cognitive_state_patterns = {
            "confused": [
                ("Run.Program", 3),  # Run 3+ times without success
                ("Compile.Error", 2),  # Multiple compile errors
                ("Run.Error", 2),  # Multiple runtime errors
            ],
            "frustrated": [
                ("Run.Program", 5),  # Many attempts
                ("Compile.Error", 3),  # Many errors
                ("Run.Error", 3),
            ],
            "understanding": [
                ("Submit", 1),  # Submitted after edits
                ("Run.Program", 1),  # Single successful run
            ],
            "engaged": [
                ("File.Edit", 3),  # Active editing
                ("Resource.View", 1),  # Looking at resources
            ],
            "insight": [
                ("File.Edit", 1),  # Quick edit after error
                ("Run.Program", 1),  # Immediate success
            ]
        }
    
    def load_progsnap2_data(self) -> pd.DataFrame:
        """Load ProgSnap2 MainTable data"""
        print("=" * 60)
        print("LOADING PROGSNAP2 DATA")
        print("=" * 60)
        
        # Try MainTable_cs1.csv first (larger dataset)
        csv_files = [
            self.progsnap_dir / "MainTable_cs1.csv",
            self.progsnap_dir / "MainTable.csv"
        ]
        
        df = None
        for csv_file in csv_files:
            if csv_file.exists():
                print(f"\nLoading {csv_file.name}...")
                try:
                    # Read in chunks if file is large
                    df = pd.read_csv(csv_file, nrows=100000)  # Limit for performance
                    print(f"[OK] Loaded {len(df)} rows")
                    break
                except Exception as e:
                    print(f"[FAIL] Error loading {csv_file.name}: {e}")
                    continue
        
        if df is None:
            raise FileNotFoundError("No ProgSnap2 data file found")
        
        return df
    
    def extract_sessions(self, df: pd.DataFrame) -> List[Dict]:
        """Extract individual debugging sessions"""
        print("\n" + "=" * 60)
        print("EXTRACTING DEBUGGING SESSIONS")
        print("=" * 60)
        
        sessions = []
        
        # Group by SubjectID and ProblemID
        for (subject_id, problem_id), group in df.groupby(['SubjectID', 'ProblemID']):
            session = {
                "subject_id": subject_id,
                "problem_id": problem_id,
                "events": [],
                "has_error": False,
                "action_sequence": []
            }
            
            # Sort by timestamp
            group_sorted = group.sort_values('ServerTimestamp')
            
            for _, row in group_sorted.iterrows():
                event_type = str(row.get('EventType', ''))
                session["events"].append({
                    "event_type": event_type,
                    "timestamp": row.get('ServerTimestamp', 0),
                    "has_error": "Error" in event_type
                })
                
                if "Error" in event_type:
                    session["has_error"] = True
                
                # Map to behavioral response
                behavior = self.event_to_behavior.get(event_type, "continue")
                session["action_sequence"].append(behavior)
            
            if len(session["events"]) > 2:  # Need at least 3 events
                sessions.append(session)
        
        print(f"[OK] Extracted {len(sessions)} sessions")
        return sessions
    
    def infer_cognitive_state(self, session: Dict) -> str:
        """Infer cognitive state from session patterns"""
        event_types = [e["event_type"] for e in session["events"]]
        event_counts = Counter(event_types)
        
        # Check patterns
        for state, patterns in self.cognitive_state_patterns.items():
            for event_type, min_count in patterns:
                if event_counts.get(event_type, 0) >= min_count:
                    return state
        
        # Default based on errors
        if session["has_error"]:
            error_count = sum(1 for e in session["events"] if "Error" in e["event_type"])
            if error_count >= 3:
                return "frustrated"
            elif error_count >= 1:
                return "confused"
        
        return "engaged"
    
    def extract_cognitive_chains(self, sessions: List[Dict]) -> List[Dict]:
        """Extract cognitive chains from sessions"""
        print("\n" + "=" * 60)
        print("EXTRACTING COGNITIVE CHAINS")
        print("=" * 60)
        
        # Count chains: (cognitive_state, behavioral_response)
        chain_counts = defaultdict(int)
        chain_contexts = defaultdict(list)
        
        for session in sessions:
            cognitive_state = self.infer_cognitive_state(session)
            
            # Get behavioral responses from action sequence
            for i, behavior in enumerate(session["action_sequence"]):
                # Determine context
                if session["has_error"]:
                    context = "encountering_error"
                elif i == len(session["action_sequence"]) - 1:
                    context = "solved_problem"
                else:
                    context = "working_on_problem"
                
                chain_key = (cognitive_state, behavior, context)
                chain_counts[chain_key] += 1
                chain_contexts[chain_key].append(context)
        
        # Create cognitive chains
        total_chains = sum(chain_counts.values())
        cognitive_chains = []
        
        for (cognitive_state, behavioral_response, context), count in chain_counts.items():
            if count < 5:  # Need at least 5 occurrences
                continue
            
            frequency = count / total_chains if total_chains > 0 else 0.0
            confidence = min(1.0, count / 50.0)  # Confidence based on evidence
            
            # Map to COKE enums
            state_map = {
                "confused": "confused",
                "frustrated": "frustrated",
                "understanding": "understanding",
                "engaged": "engaged",
                "insight": "insight"
            }
            
            behavior_map = {
                "ask_question": "ask_question",
                "search_info": "search_info",
                "try_again": "try_again",
                "continue": "continue",
                "explain": "explain"
            }
            
            coke_state = state_map.get(cognitive_state, "engaged")
            coke_behavior = behavior_map.get(behavioral_response, "continue")
            
            chain = {
                "id": f"chain_{coke_state}_to_{coke_behavior}",
                "mental_activity": coke_state,
                "context": context,
                "behavioral_response": coke_behavior,
                "affective_response": self._get_affective_response(coke_state),
                "confidence": round(confidence, 2),
                "frequency": round(frequency, 3),
                "source": "progsnap2",
                "evidence_count": count
            }
            
            cognitive_chains.append(chain)
            print(f"\n[OK] Extracted chain: {chain['id']}")
            print(f"  State: {coke_state} -> Behavior: {coke_behavior}")
            print(f"  Frequency: {frequency:.1%}")
            print(f"  Evidence: {count} occurrences")
        
        return cognitive_chains
    
    def _get_affective_response(self, cognitive_state: str) -> str:
        """Get affective response for cognitive state"""
        affective_map = {
            "confused": "frustrated",
            "frustrated": "determined",
            "understanding": "satisfied",
            "engaged": "motivated",
            "insight": "satisfied"
        }
        return affective_map.get(cognitive_state, "neutral")
    
    def save_cognitive_chains(self, chains: List[Dict], output_file: str = "data/pedagogical_kg/coke_chains_learned.json"):
        """Save learned cognitive chains to file"""
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(chains, f, indent=2, ensure_ascii=False)
        
        print(f"\n[OK] Saved {len(chains)} cognitive chains to {output_path}")
        return output_path


def main():
    """Main function"""
    learner = ProgSnap2COKELearner()
    
    try:
        # Load ProgSnap2 data
        df = learner.load_progsnap2_data()
        
        # Extract sessions
        sessions = learner.extract_sessions(df)
        
        if not sessions:
            print("\n[WARN] No sessions extracted. Check ProgSnap2 data format.")
            return
        
        # Extract cognitive chains
        chains = learner.extract_cognitive_chains(sessions)
        
        if not chains:
            print("\n[WARN] No cognitive chains extracted. Check session data.")
            return
        
        # Save chains
        output_path = learner.save_cognitive_chains(chains)
        
        print("\n" + "=" * 60)
        print("SUMMARY")
        print("=" * 60)
        print(f"Total sessions analyzed: {len(sessions)}")
        print(f"Cognitive chains extracted: {len(chains)}")
        print(f"Output file: {output_path}")
        print("\nNext step: Run learn_misconceptions_from_assistments.py")
        
    except Exception as e:
        print(f"\n[FAIL] Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()





