"""
Learn Misconceptions from CodeNet Buggy Code Patterns
Extracts common error patterns and creates misconception data
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

import re
import json
import ast
from collections import defaultdict, Counter
from typing import Dict, List, Tuple
import pandas as pd


class CodeNetMisconceptionLearner:
    """Learn misconceptions from CodeNet buggy code patterns"""
    
    def __init__(self, codenet_dir: str = "data/codenet"):
        self.codenet_dir = Path(codenet_dir)
        self.misconceptions = []
        self.error_patterns = defaultdict(list)
        
        # Error type to concept mapping
        self.error_to_concept = {
            "RecursionError": "recursion",
            "IndexError": "arrays",
            "UnboundLocalError": "variable_scope",
            "NameError": "variable_scope",
            "TypeError": "type_system",
            "AttributeError": "object_oriented",
            "KeyError": "dictionaries",
            "ZeroDivisionError": "arithmetic",
            "ValueError": "input_validation",
            "IndentationError": "syntax",
            "SyntaxError": "syntax"
        }
        
        # Common bug patterns
        self.bug_patterns = {
            "recursion": [
                r"def\s+\w+\([^)]*\):\s*return\s+[^i]*\w+\([^)]*\)",  # Missing base case
                r"recursion.*without.*if",  # No base case check
            ],
            "arrays": [
                r"\[\w+\s*\+\s*\d+\]",  # Off-by-one
                r"range\(len\([^)]+\)\)",  # Potential index error
                r"\[\s*len\([^)]+\)\s*\]",  # Index out of bounds
            ],
            "variable_scope": [
                r"def\s+\w+\([^)]*\):\s*[^=]*=\s*\w+",  # Local variable assignment
                r"global\s+\w+",  # Global keyword usage
            ],
            "loops": [
                r"for\s+\w+\s+in\s+range\([^)]*\):\s*[^:]*\[\w+\]",  # Loop indexing
                r"while\s+True:",  # Infinite loop potential
            ]
        }
    
    def analyze_code_file(self, filepath: Path) -> Dict:
        """Analyze a single code file for errors"""
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                code = f.read()
        except Exception as e:
            return {"error": str(e)}
        
        # Check if it's buggy code
        is_buggy = "buggy" in filepath.name.lower()
        
        result = {
            "file": str(filepath),
            "is_buggy": is_buggy,
            "code_length": len(code),
            "errors": [],
            "concepts": [],
            "patterns": []
        }
        
        if not is_buggy:
            return result
        
        # Try to parse code
        try:
            ast.parse(code)
            syntax_valid = True
        except SyntaxError as e:
            result["errors"].append({
                "type": "SyntaxError",
                "message": str(e),
                "line": getattr(e, 'lineno', None)
            })
            syntax_valid = False
        except Exception:
            syntax_valid = False
        
        # Extract error patterns from code comments
        error_indicators = re.findall(r"#\s*(Bug|Error|TODO|FIXME):\s*(.+)", code, re.IGNORECASE)
        for indicator_type, description in error_indicators:
            result["errors"].append({
                "type": indicator_type,
                "description": description.strip()
            })
        
        # Match bug patterns
        for concept, patterns in self.bug_patterns.items():
            for pattern in patterns:
                if re.search(pattern, code, re.MULTILINE | re.IGNORECASE):
                    result["patterns"].append({
                        "concept": concept,
                        "pattern": pattern
                    })
                    if concept not in result["concepts"]:
                        result["concepts"].append(concept)
        
        # Extract error types from filename or code
        for error_type, concept in self.error_to_concept.items():
            if error_type.lower() in filepath.name.lower():
                result["errors"].append({
                    "type": error_type,
                    "source": "filename"
                })
                if concept not in result["concepts"]:
                    result["concepts"].append(concept)
        
        return result
    
    def process_codenet_directory(self) -> List[Dict]:
        """Process all CodeNet files"""
        print("=" * 60)
        print("LEARNING MISCONCEPTIONS FROM CODENET")
        print("=" * 60)
        
        all_analyses = []
        languages = ["python", "java", "cpp"]
        
        for lang in languages:
            lang_dir = self.codenet_dir / lang
            if not lang_dir.exists():
                continue
            
            print(f"\nProcessing {lang} files...")
            buggy_files = list(lang_dir.glob("buggy*.txt")) + list(lang_dir.glob("buggy*.py"))
            
            for buggy_file in buggy_files:
                analysis = self.analyze_code_file(buggy_file)
                if analysis.get("is_buggy") and (analysis.get("errors") or analysis.get("patterns")):
                    all_analyses.append(analysis)
            
            print(f"  Found {len([a for a in all_analyses if a.get('is_buggy')])} buggy files")
        
        return all_analyses
    
    def extract_misconceptions(self, analyses: List[Dict]) -> List[Dict]:
        """Extract misconception patterns from analyses"""
        print("\n" + "=" * 60)
        print("EXTRACTING MISCONCEPTION PATTERNS")
        print("=" * 60)
        
        # Group by concept
        concept_errors = defaultdict(lambda: {
            "error_types": Counter(),
            "patterns": Counter(),
            "descriptions": [],
            "count": 0
        })
        
        for analysis in analyses:
            for concept in analysis.get("concepts", []):
                concept_errors[concept]["count"] += 1
                
                for error in analysis.get("errors", []):
                    error_type = error.get("type", "Unknown")
                    concept_errors[concept]["error_types"][error_type] += 1
                    
                    if "description" in error:
                        concept_errors[concept]["descriptions"].append(error["description"])
                
                for pattern in analysis.get("patterns", []):
                    pattern_str = pattern.get("pattern", "")
                    concept_errors[concept]["patterns"][pattern_str] += 1
        
        # Create misconceptions
        misconceptions = []
        total_buggy = sum(c["count"] for c in concept_errors.values())
        
        for concept, data in concept_errors.items():
            if data["count"] < 3:  # Need at least 3 occurrences
                continue
            
            # Get most common error type
            most_common_error = data["error_types"].most_common(1)
            error_type = most_common_error[0][0] if most_common_error else "Unknown"
            
            # Calculate frequency
            frequency = data["count"] / total_buggy if total_buggy > 0 else 0.0
            
            # Determine severity
            if frequency > 0.3:
                severity = "high"
            elif frequency > 0.1:
                severity = "medium"
            else:
                severity = "low"
            
            # Extract common indicators
            common_indicators = []
            for error_type_name, count in data["error_types"].most_common(3):
                common_indicators.append(error_type_name)
            
            # Get description from most common descriptions
            descriptions = [d for d in data["descriptions"] if d]
            description = descriptions[0] if descriptions else f"Common {concept} misconception"
            
            misconception = {
                "id": f"mc_{concept}_{error_type.lower()}",
                "concept": concept,
                "description": description,
                "common_indicators": common_indicators,
                "severity": severity,
                "frequency": round(frequency, 3),
                "related_concepts": self._get_related_concepts(concept),
                "correction_strategy": self._generate_correction_strategy(concept, error_type),
                "source": "codenet",
                "evidence_count": data["count"]
            }
            
            misconceptions.append(misconception)
            print(f"\n[OK] Extracted misconception: {misconception['id']}")
            print(f"  Concept: {concept}")
            print(f"  Frequency: {frequency:.1%}")
            print(f"  Evidence: {data['count']} buggy files")
        
        return misconceptions
    
    def _get_related_concepts(self, concept: str) -> List[str]:
        """Get related concepts based on concept hierarchy"""
        concept_map = {
            "recursion": ["base_case", "conditional_statements", "functions"],
            "arrays": ["loops", "indexing", "lists"],
            "variable_scope": ["functions", "namespaces", "global"],
            "loops": ["arrays", "conditionals", "iteration"],
            "type_system": ["variables", "functions", "classes"],
            "object_oriented": ["classes", "inheritance", "methods"],
            "dictionaries": ["data_structures", "key_value_pairs"],
            "syntax": ["language_fundamentals", "code_structure"]
        }
        return concept_map.get(concept, [])
    
    def _generate_correction_strategy(self, concept: str, error_type: str) -> str:
        """Generate correction strategy based on concept and error"""
        strategies = {
            "recursion": "Explain base case necessity with examples. Show how recursion needs a stopping condition.",
            "arrays": "Practice with boundary cases. Show how to check array bounds before accessing.",
            "variable_scope": "Show scope visualization and examples. Explain local vs global variables.",
            "loops": "Practice with boundary cases. Show how to correctly set loop bounds.",
            "type_system": "Explain type checking and type conversion. Show examples of type errors.",
            "object_oriented": "Explain object instantiation and method calls. Show attribute access patterns.",
            "dictionaries": "Explain key existence checking. Show how to safely access dictionary values.",
            "syntax": "Review syntax rules. Show common syntax error patterns and fixes."
        }
        return strategies.get(concept, f"Review {concept} fundamentals and common pitfalls.")
    
    def save_misconceptions(self, misconceptions: List[Dict], output_file: str = "data/pedagogical_kg/misconceptions_learned.json"):
        """Save learned misconceptions to file"""
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(misconceptions, f, indent=2, ensure_ascii=False)
        
        print(f"\n[OK] Saved {len(misconceptions)} misconceptions to {output_path}")
        return output_path


def main():
    """Main function"""
    learner = CodeNetMisconceptionLearner()
    
    # Process CodeNet files
    analyses = learner.process_codenet_directory()
    
    if not analyses:
        print("\n⚠ No buggy code files found. Make sure CodeNet data is downloaded.")
        return
    
    # Extract misconceptions
    misconceptions = learner.extract_misconceptions(analyses)
    
    if not misconceptions:
        print("\n⚠ No misconceptions extracted. Check CodeNet data format.")
        return
    
    # Save misconceptions
    output_path = learner.save_misconceptions(misconceptions)
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Total buggy files analyzed: {len(analyses)}")
    print(f"Misconceptions extracted: {len(misconceptions)}")
    print(f"Output file: {output_path}")
    print("\nNext step: Run learn_coke_chains_from_progsnap2.py")


if __name__ == "__main__":
    main()





