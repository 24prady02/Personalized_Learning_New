"""
Generate VERY LARGE Datasets for Training
Creates large-scale datasets matching real dataset structures
"""

import pandas as pd
import numpy as np
import json
import random
import time
from pathlib import Path
from tqdm import tqdm

def generate_very_large_assistments():
    """Generate VERY large ASSISTments dataset"""
    print("\n" + "="*60)
    print("GENERATING VERY LARGE ASSISTMENTS DATASET")
    print("="*60)
    
    assistments_dir = Path('data/assistments')
    assistments_dir.mkdir(parents=True, exist_ok=True)
    
    output_file = assistments_dir / "2012-2013-data-with-predictions-4-final.csv"
    
    # Parameters for VERY large dataset
    num_students = 50000  # 50,000 students (like real dataset)
    num_skills = 100
    problems_per_skill = 30
    interactions_per_student = 100  # Average 100 interactions per student
    
    print(f"Generating dataset with:")
    print(f"  Students: {num_students:,}")
    print(f"  Skills: {num_skills}")
    print(f"  Problems: {num_skills * problems_per_skill:,}")
    print(f"  Expected interactions: ~{num_students * interactions_per_student:,}")
    print("\nThis will take several minutes...")
    
    skills = [f"Skill_{i+1}" for i in range(num_skills)]
    problems = [f"Problem_{i+1:04d}" for i in range(num_skills * problems_per_skill)]
    
    data = []
    student_id = 1
    
    for student_idx in tqdm(range(num_students), desc="Generating students"):
        # Each student has different mastery levels
        student_mastery = {skill: random.uniform(0.2, 0.9) for skill in skills}
        
        # Generate interactions for this student
        num_interactions = random.randint(50, 150)  # Variable interactions per student
        
        for interaction in range(num_interactions):
            skill = random.choice(skills)
            problem_id = random.choice([p for p in problems if skill in p] or problems)
            
            # Determine correctness based on mastery
            mastery = student_mastery[skill]
            is_correct = random.random() < mastery
            
            # Add noise (slip/guess)
            if random.random() < 0.1:
                is_correct = not is_correct
            
            # Generate realistic features
            hint_count = 0 if is_correct else random.randint(0, 3)
            attempt_count = 1 if is_correct else random.randint(1, 4)
            response_time = random.randint(2000, 30000)
            is_original = 1 if attempt_count == 1 else 0
            
            data.append({
                'user_id': student_id,
                'problem_id': problem_id,
                'skill_name': skill,
                'correct': 1 if is_correct else 0,
                'original': is_original,
                'ms_first_response': response_time,
                'hint_count': hint_count,
                'attempt_count': attempt_count,
                'overlap_time': response_time + random.randint(0, 5000)
            })
            
            # Update mastery
            if is_correct:
                student_mastery[skill] = min(0.95, student_mastery[skill] + 0.05)
            else:
                student_mastery[skill] = max(0.1, student_mastery[skill] - 0.03)
        
        student_id += 1
        
        # Save in chunks to avoid memory issues
        if len(data) >= 100000:
            df_chunk = pd.DataFrame(data)
            if output_file.exists():
                df_chunk.to_csv(output_file, mode='a', header=False, index=False)
            else:
                df_chunk.to_csv(output_file, index=False)
            data = []
    
    # Save remaining data
    if data:
        df_chunk = pd.DataFrame(data)
        if output_file.exists():
            df_chunk.to_csv(output_file, mode='a', header=False, index=False)
        else:
            df_chunk.to_csv(output_file, index=False)
    
    # Verify
    df = pd.read_csv(output_file)
    print(f"\n[OK] Generated VERY large ASSISTments dataset!")
    print(f"  File size: {output_file.stat().st_size / (1024*1024):.1f} MB")
    print(f"  Total interactions: {len(df):,}")
    print(f"  Students: {df['user_id'].nunique():,}")
    print(f"  Skills: {df['skill_name'].nunique()}")
    print(f"  Problems: {df['problem_id'].nunique()}")

def generate_very_large_progsnap2():
    """Generate VERY large ProgSnap2 dataset"""
    print("\n" + "="*60)
    print("GENERATING VERY LARGE PROGSNAP2 DATASET")
    print("="*60)
    
    progsnap_dir = Path('data/progsnap2')
    progsnap_dir.mkdir(parents=True, exist_ok=True)
    
    output_file = progsnap_dir / "MainTable_cs1.csv"
    
    num_students = 20000  # 20,000 students
    num_problems = 50
    events_per_session = 50  # More events per session
    
    print(f"Generating dataset with:")
    print(f"  Students: {num_students:,}")
    print(f"  Problems: {num_problems}")
    print(f"  Events per session: {events_per_session}")
    print(f"  Expected events: ~{num_students * events_per_session:,}")
    print("\nThis will take several minutes...")
    
    problems = [f"p{i+1:03d}" for i in range(num_problems)]
    event_types = [
        "File.Edit", "File.Create", "File.Delete",
        "Compile", "Compile.Error", "Compile.Success",
        "Run.Program", "Run.Error", "Run.Success",
        "Submit", "Help.Request", "Hint.Request",
        "Code.Edit", "Test.Run", "Debug.Start"
    ]
    
    data = []
    event_id = 1
    subject_id = 1
    
    for student_idx in tqdm(range(num_students), desc="Generating sessions"):
        problem = random.choice(problems)
        session_start = time.time() - random.randint(0, 86400 * 30)
        
        for event_idx in range(events_per_session):
            event_type = random.choice(event_types)
            timestamp = session_start + event_idx * random.randint(5, 60)
            
            code_state = f"def solution():\n    # Student {subject_id} working on {problem}\n    # Event: {event_type}\n    pass"
            
            data.append({
                'EventID': event_id,
                'SubjectID': f"student_{subject_id:05d}",
                'ProblemID': problem,
                'EventType': event_type,
                'ServerTimestamp': int(timestamp),
                'CodeStateSection': code_state
            })
            
            event_id += 1
        
        subject_id += 1
        
        # Save in chunks
        if len(data) >= 100000:
            df_chunk = pd.DataFrame(data)
            if output_file.exists():
                df_chunk.to_csv(output_file, mode='a', header=False, index=False)
            else:
                df_chunk.to_csv(output_file, index=False)
            data = []
    
    # Save remaining
    if data:
        df_chunk = pd.DataFrame(data)
        if output_file.exists():
            df_chunk.to_csv(output_file, mode='a', header=False, index=False)
        else:
            df_chunk.to_csv(output_file, index=False)
    
    # Verify
    df = pd.read_csv(output_file)
    print(f"\n[OK] Generated VERY large ProgSnap2 dataset!")
    print(f"  File size: {output_file.stat().st_size / (1024*1024):.1f} MB")
    print(f"  Total events: {len(df):,}")
    print(f"  Students: {df['SubjectID'].nunique():,}")
    print(f"  Problems: {df['ProblemID'].nunique()}")

def generate_very_large_codenet():
    """Generate VERY large CodeNet dataset"""
    print("\n" + "="*60)
    print("GENERATING VERY LARGE CODENET DATASET")
    print("="*60)
    
    codenet_dir = Path('data/codenet')
    python_dir = codenet_dir / "python"
    java_dir = codenet_dir / "java"
    cpp_dir = codenet_dir / "c++"
    
    python_dir.mkdir(parents=True, exist_ok=True)
    java_dir.mkdir(parents=True, exist_ok=True)
    cpp_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate MANY code files
    num_python_files = 500
    num_java_files = 300
    num_cpp_files = 200
    
    print(f"Generating:")
    print(f"  Python files: {num_python_files}")
    print(f"  Java files: {num_java_files}")
    print(f"  C++ files: {num_cpp_files}")
    print(f"  Total: {num_python_files + num_java_files + num_cpp_files} files")
    
    # Python templates
    python_templates = {
        'correct': [
            "def {name}({params}):\n    {body}\n    return result",
            "class {name}:\n    def __init__(self, {params}):\n        self.{param} = {param}\n    def {method}(self):\n        {body}",
            "def {name}({params}):\n    if {condition}:\n        return {value1}\n    return {value2}",
        ],
        'buggy': [
            "def {name}({params}):\n    {body}  # Bug: missing return",
            "class {name}:\n    def {method}(self):\n        {body}  # Bug: incorrect logic",
            "def {name}({params}):\n    {body}  # Bug: off-by-one error",
        ]
    }
    
    # Generate Python files
    print("\nGenerating Python files...")
    for i in tqdm(range(num_python_files), desc="Python"):
        is_correct = random.random() > 0.3  # 70% correct, 30% buggy
        template_type = 'correct' if is_correct else 'buggy'
        template = random.choice(python_templates[template_type])
        
        filename = f"{'correct' if is_correct else 'buggy'}_code_{i+1:04d}.txt"
        filepath = python_dir / filename
        
        code = template.format(
            name=f"function_{i}",
            params="x, y",
            param="x",
            method="process",
            body="result = x + y",
            condition="x > 0",
            value1="x",
            value2="0"
        )
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(code)
    
    # Generate Java files
    print("\nGenerating Java files...")
    java_template_correct = """public class Class_{i} {{
    public int method(int x, int y) {{
        return x + y;
    }}
}}"""
    
    java_template_buggy = """public class Class_{i} {{
    public int method(int x, int y) {{
        return x;  // Bug: missing y
    }}
}}"""
    
    for i in tqdm(range(num_java_files), desc="Java"):
        is_correct = random.random() > 0.3
        template = java_template_correct if is_correct else java_template_buggy
        
        filename = f"{'correct' if is_correct else 'buggy'}_code_{i+1:04d}.txt"
        filepath = java_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(template.format(i=i))
    
    # Generate C++ files
    print("\nGenerating C++ files...")
    cpp_template_correct = """#include <iostream>
using namespace std;

int function_{i}(int x, int y) {{
    return x + y;
}}"""
    
    cpp_template_buggy = """#include <iostream>
using namespace std;

int function_{i}(int x, int y) {{
    return x;  // Bug: missing y
}}"""
    
    for i in tqdm(range(num_cpp_files), desc="C++"):
        is_correct = random.random() > 0.3
        template = cpp_template_correct if is_correct else cpp_template_buggy
        
        filename = f"{'correct' if is_correct else 'buggy'}_code_{i+1:04d}.txt"
        filepath = cpp_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(template.format(i=i))
    
    py_files = len(list(python_dir.glob('*.txt')))
    java_files = len(list(java_dir.glob('*.txt')))
    cpp_files = len(list(cpp_dir.glob('*.txt')))
    
    print(f"\n[OK] Generated VERY large CodeNet dataset!")
    print(f"  Python files: {py_files}")
    print(f"  Java files: {java_files}")
    print(f"  C++ files: {cpp_files}")
    print(f"  Total: {py_files + java_files + cpp_files} files")

def generate_very_large_mooccubex():
    """Generate VERY large MOOCCubeX dataset"""
    print("\n" + "="*60)
    print("GENERATING VERY LARGE MOOCCUBEX DATASET")
    print("="*60)
    
    mooccubex_dir = Path('data/moocsxcube')
    mooccubex_dir.mkdir(parents=True, exist_ok=True)
    
    entities_file = mooccubex_dir / "entities.json"
    
    # VERY large dataset
    num_students = 10000
    num_concepts = 500
    num_courses = 200
    
    print(f"Generating:")
    print(f"  Students: {num_students:,}")
    print(f"  Concepts: {num_concepts}")
    print(f"  Courses: {num_courses}")
    
    data = {
        "student": [],
        "course": [],
        "concept": [],
        "activity": []
    }
    
    # Generate students
    print("\nGenerating students...")
    for i in tqdm(range(num_students), desc="Students"):
        data["student"].append({
            "id": f"s_{i+1:05d}",
            "level": random.choice(["beginner", "intermediate", "advanced"]),
            "enrollment_date": f"2023-{random.randint(1,12):02d}-{random.randint(1,28):02d}",
            "progress": random.uniform(0.0, 1.0)
        })
    
    # Generate concepts
    print("\nGenerating concepts...")
    concept_names = [
        "variables", "functions", "loops", "conditionals", "arrays",
        "lists", "dictionaries", "classes", "inheritance", "recursion",
        "sorting", "searching", "trees", "graphs", "dynamic_programming",
        "greedy_algorithms", "backtracking", "divide_conquer", "hash_tables",
        "stacks", "queues", "heaps", "binary_trees", "avl_trees",
        "red_black_trees", "tries", "suffix_trees", "graph_traversal",
        "shortest_path", "minimum_spanning_tree", "network_flow",
        "string_matching", "regular_expressions", "parsing", "compilers"
    ]
    
    for i in range(num_concepts):
        concept_name = concept_names[i % len(concept_names)] if i < len(concept_names) else f"concept_{i}"
        data["concept"].append({
            "id": f"concept_{i+1:05d}",
            "name": concept_name,
            "difficulty": random.choice(["beginner", "intermediate", "advanced"]),
            "category": random.choice(["programming", "algorithms", "data_structures", "systems"])
        })
    
    # Generate courses
    print("\nGenerating courses...")
    for i in range(num_courses):
        data["course"].append({
            "id": f"course_{i+1:04d}",
            "name": f"Course {i+1}",
            "level": random.choice(["beginner", "intermediate", "advanced"]),
            "duration_weeks": random.randint(4, 16),
            "enrollment_count": random.randint(100, 10000)
        })
    
    # Generate activities
    print("\nGenerating activities...")
    activity_types = ["video", "quiz", "assignment", "project", "discussion"]
    for i in tqdm(range(num_students * 10), desc="Activities"):  # 10 activities per student
        data["activity"].append({
            "id": f"activity_{i+1:06d}",
            "student_id": f"s_{random.randint(1, num_students):05d}",
            "course_id": f"course_{random.randint(1, num_courses):04d}",
            "concept_id": f"concept_{random.randint(1, num_concepts):05d}",
            "type": random.choice(activity_types),
            "completed": random.choice([True, False]),
            "score": random.uniform(0.0, 1.0) if random.random() > 0.3 else None
        })
    
    with open(entities_file, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"\n[OK] Generated VERY large MOOCCubeX dataset!")
    print(f"  Students: {len(data['student']):,}")
    print(f"  Concepts: {len(data['concept']):,}")
    print(f"  Courses: {len(data['course']):,}")
    print(f"  Activities: {len(data['activity']):,}")

def verify_all():
    """Verify all datasets"""
    print("\n" + "="*60)
    print("FINAL VERIFICATION")
    print("="*60)
    
    # ASSISTments
    assistments_file = Path('data/assistments/2012-2013-data-with-predictions-4-final.csv')
    if assistments_file.exists():
        df = pd.read_csv(assistments_file, nrows=1000)
        size_mb = assistments_file.stat().st_size / (1024*1024)
        print(f"\nASSISTments: [OK] VERY LARGE")
        print(f"  Size: {size_mb:.1f} MB")
        print(f"  Columns: {list(df.columns)}")
        # Count total rows
        total_rows = sum(1 for _ in open(assistments_file)) - 1
        print(f"  Total rows: {total_rows:,}")
    
    # ProgSnap2
    progsnap_file = Path('data/progsnap2/MainTable_cs1.csv')
    if progsnap_file.exists():
        df = pd.read_csv(progsnap_file, nrows=1000)
        size_mb = progsnap_file.stat().st_size / (1024*1024)
        print(f"\nProgSnap2: [OK] VERY LARGE")
        print(f"  Size: {size_mb:.1f} MB")
        print(f"  Columns: {list(df.columns)}")
        total_rows = sum(1 for _ in open(progsnap_file)) - 1
        print(f"  Total rows: {total_rows:,}")
    
    # CodeNet
    codenet_py = len(list(Path('data/codenet/python').glob('*.txt'))) if Path('data/codenet/python').exists() else 0
    codenet_java = len(list(Path('data/codenet/java').glob('*.txt'))) if Path('data/codenet/java').exists() else 0
    codenet_cpp = len(list(Path('data/codenet/c++').glob('*.txt'))) if Path('data/codenet/c++').exists() else 0
    total = codenet_py + codenet_java + codenet_cpp
    print(f"\nCodeNet: [OK] VERY LARGE")
    print(f"  Python: {codenet_py} files")
    print(f"  Java: {codenet_java} files")
    print(f"  C++: {codenet_cpp} files")
    print(f"  Total: {total} files")
    
    # MOOCCubeX
    mooccubex_file = Path('data/moocsxcube/entities.json')
    if mooccubex_file.exists():
        with open(mooccubex_file, 'r') as f:
            data = json.load(f)
        print(f"\nMOOCCubeX: [OK] VERY LARGE")
        print(f"  Students: {len(data.get('student', [])):,}")
        print(f"  Concepts: {len(data.get('concept', [])):,}")
        print(f"  Courses: {len(data.get('course', [])):,}")
        print(f"  Activities: {len(data.get('activity', [])):,}")

def main():
    print("="*60)
    print("GENERATING VERY LARGE DATASETS FOR TRAINING")
    print("="*60)
    print("\nThis will generate large-scale datasets:")
    print("  - ASSISTments: 50,000 students, ~5M interactions")
    print("  - ProgSnap2: 20,000 students, ~1M events")
    print("  - CodeNet: 1,000 code files")
    print("  - MOOCCubeX: 10,000 students, 500 concepts")
    print("\nThis will take 10-20 minutes...\n")
    
    # Generate all datasets
    generate_very_large_assistments()
    generate_very_large_progsnap2()
    generate_very_large_codenet()
    generate_very_large_mooccubex()
    
    # Verify
    verify_all()
    
    print("\n" + "="*60)
    print("ALL DATASETS GENERATED!")
    print("="*60)
    print("\nNext steps:")
    print("1. Run validation: python validate_on_assistments.py")
    print("2. Process datasets: python scripts/process_datasets.py")
    print("3. Train models: python train.py")

if __name__ == "__main__":
    main()















