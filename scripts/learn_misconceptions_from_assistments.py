"""
Learn Misconceptions from ASSISTments Wrong Answer Patterns
Extracts misconception patterns from student incorrect responses
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

import pandas as pd
import json
from collections import defaultdict, Counter
from typing import Dict, List
import re


class ASSISTmentsMisconceptionLearner:
    """Learn misconceptions from ASSISTments wrong answers"""
    
    def __init__(self, assistments_dir: str = "data/assistments"):
        self.assistments_dir = Path(assistments_dir)
        self.misconceptions = []
    
    def load_assistments_data(self) -> pd.DataFrame:
        """Load ASSISTments data"""
        print("=" * 60)
        print("LOADING ASSISTMENTS DATA")
        print("=" * 60)
        
        # Try different file names
        csv_files = [
            self.assistments_dir / "2012-2013-data-with-predictions-4-final.csv",
            self.assistments_dir / "skill_builder_data.csv"
        ]
        
        df = None
        for csv_file in csv_files:
            if csv_file.exists():
                print(f"\nLoading {csv_file.name}...")
                try:
                    # Read in chunks if file is large
                    if csv_file.stat().st_size > 100 * 1024 * 1024:  # > 100MB
                        print("  File is large, reading sample...")
                        df = pd.read_csv(csv_file, nrows=50000)  # Sample for performance
                    else:
                        df = pd.read_csv(csv_file)
                    print(f"✓ Loaded {len(df)} rows")
                    break
                except Exception as e:
                    print(f"✗ Error loading {csv_file.name}: {e}")
                    continue
        
        if df is None:
            raise FileNotFoundError("No ASSISTments data file found")
        
        return df
    
    def analyze_wrong_answers(self, df: pd.DataFrame) -> Dict:
        """Analyze wrong answer patterns"""
        print("\n" + "=" * 60)
        print("ANALYZING WRONG ANSWER PATTERNS")
        print("=" * 60)
        
        # Filter wrong answers
        wrong_answers = df[df.get('correct', df.get('is_correct', 0)) == 0].copy()
        print(f"Total wrong answers: {len(wrong_answers)}")
        
        # Group by skill/concept
        skill_errors = defaultdict(lambda: {
            "total_attempts": 0,
            "wrong_count": 0,
            "wrong_patterns": Counter(),
            "attempt_counts": Counter(),
            "students": set()
        })
        
        # Determine skill column name
        skill_col = None
        for col in ['skill_name', 'skill_id', 'skill', 'concept']:
            if col in wrong_answers.columns:
                skill_col = col
                break
        
        if skill_col is None:
            print("⚠ No skill column found. Using problem_id as concept.")
            skill_col = 'problem_id'
        
        # Analyze by skill
        for skill, group in wrong_answers.groupby(skill_col):
            skill_errors[skill]["total_attempts"] = len(group)
            skill_errors[skill]["wrong_count"] = len(group)
            
            # Count attempt patterns
            if 'attempt_count' in group.columns:
                attempt_counts = group['attempt_count'].value_counts()
                skill_errors[skill]["attempt_counts"] = Counter(attempt_counts.to_dict())
            
            # Track students
            if 'user_id' in group.columns:
                skill_errors[skill]["students"].update(group['user_id'].unique())
        
        return skill_errors, skill_col
    
    def extract_misconceptions(self, skill_errors: Dict, skill_col: str) -> List[Dict]:
        """Extract misconceptions from skill error patterns"""
        print("\n" + "=" * 60)
        print("EXTRACTING MISCONCEPTIONS")
        print("=" * 60)
        
        misconceptions = []
        total_wrong = sum(data["wrong_count"] for data in skill_errors.values())
        
        for skill, data in skill_errors.items():
            if data["wrong_count"] < 10:  # Need at least 10 wrong answers
                continue
            
            # Calculate frequency
            frequency = data["wrong_count"] / total_wrong if total_wrong > 0 else 0.0
            
            # Determine severity based on frequency and attempt patterns
            avg_attempts = 0
            if data["attempt_counts"]:
                total_attempts = sum(data["attempt_counts"].values())
                weighted_attempts = sum(count * attempts for attempts, count in data["attempt_counts"].items())
                avg_attempts = weighted_attempts / total_attempts if total_attempts > 0 else 0
            
            if frequency > 0.2 or avg_attempts > 3:
                severity = "high"
            elif frequency > 0.1 or avg_attempts > 2:
                severity = "medium"
            else:
                severity = "low"
            
            # Get common indicators
            common_indicators = []
            if avg_attempts > 2:
                common_indicators.append(f"Multiple attempts (avg: {avg_attempts:.1f})")
            if len(data["students"]) > 50:
                common_indicators.append(f"Affects many students ({len(data['students'])} students)")
            
            misconception = {
                "id": f"mc_assistments_{skill.lower().replace(' ', '_')}",
                "concept": skill,
                "description": f"Common misconception in {skill} - students frequently answer incorrectly",
                "common_indicators": common_indicators,
                "severity": severity,
                "frequency": round(frequency, 3),
                "related_concepts": self._get_related_concepts(skill),
                "correction_strategy": self._generate_correction_strategy(skill),
                "source": "assistments",
                "evidence_count": data["wrong_count"],
                "affected_students": len(data["students"]),
                "avg_attempts": round(avg_attempts, 2)
            }
            
            misconceptions.append(misconception)
            print(f"\n✓ Extracted misconception: {misconception['id']}")
            print(f"  Concept: {skill}")
            print(f"  Frequency: {frequency:.1%}")
            print(f"  Wrong answers: {data['wrong_count']}")
            print(f"  Affected students: {len(data['students'])}")
        
        return misconceptions
    
    def _get_related_concepts(self, skill: str) -> List[str]:
        """Get related concepts based on skill name"""
        # Simple keyword-based mapping
        skill_lower = skill.lower()
        
        if "addition" in skill_lower or "subtract" in skill_lower:
            return ["arithmetic", "number_operations", "basic_math"]
        elif "multiplication" in skill_lower or "division" in skill_lower:
            return ["arithmetic", "number_operations", "basic_math"]
        elif "fraction" in skill_lower:
            return ["fractions", "rational_numbers", "arithmetic"]
        elif "algebra" in skill_lower:
            return ["algebra", "equations", "variables"]
        elif "geometry" in skill_lower:
            return ["geometry", "shapes", "spatial_reasoning"]
        else:
            return []
    
    def _generate_correction_strategy(self, skill: str) -> str:
        """Generate correction strategy based on skill"""
        skill_lower = skill.lower()
        
        if "addition" in skill_lower or "subtract" in skill_lower:
            return "Review basic number operations. Practice with visual aids and step-by-step examples."
        elif "multiplication" in skill_lower or "division" in skill_lower:
            return "Review multiplication and division tables. Practice with word problems and real-world examples."
        elif "fraction" in skill_lower:
            return "Explain fraction concepts with visual representations. Practice equivalent fractions and operations."
        elif "algebra" in skill_lower:
            return "Review algebraic manipulation rules. Practice solving equations step by step."
        elif "geometry" in skill_lower:
            return "Use visual aids and diagrams. Practice identifying shapes and calculating areas/perimeters."
        else:
            return f"Review {skill} fundamentals. Provide step-by-step examples and practice problems."
    
    def save_misconceptions(self, misconceptions: List[Dict], output_file: str = "data/pedagogical_kg/misconceptions_assistments_learned.json"):
        """Save learned misconceptions to file"""
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(misconceptions, f, indent=2, ensure_ascii=False)
        
        print(f"\n✓ Saved {len(misconceptions)} misconceptions to {output_path}")
        return output_path


def main():
    """Main function"""
    learner = ASSISTmentsMisconceptionLearner()
    
    try:
        # Load ASSISTments data
        df = learner.load_assistments_data()
        
        # Analyze wrong answers
        skill_errors, skill_col = learner.analyze_wrong_answers(df)
        
        if not skill_errors:
            print("\n⚠ No skill errors found. Check ASSISTments data format.")
            return
        
        # Extract misconceptions
        misconceptions = learner.extract_misconceptions(skill_errors, skill_col)
        
        if not misconceptions:
            print("\n⚠ No misconceptions extracted. Check data quality.")
            return
        
        # Save misconceptions
        output_path = learner.save_misconceptions(misconceptions)
        
        print("\n" + "=" * 60)
        print("SUMMARY")
        print("=" * 60)
        print(f"Total skills analyzed: {len(skill_errors)}")
        print(f"Misconceptions extracted: {len(misconceptions)}")
        print(f"Output file: {output_path}")
        print("\nNext step: Run merge_learned_data.py to combine all learned data")
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()





