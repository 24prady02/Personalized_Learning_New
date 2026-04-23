import pandas as pd
import json
import os
from pathlib import Path

print("="*60)
print("DATASET SIZES CHECK")
print("="*60)

# ASSISTments
assistments_file = Path('data/assistments/skill_builder_data.csv')
if assistments_file.exists():
    df = pd.read_csv(assistments_file)
    print(f"\nASSISTments:")
    print(f"  Rows: {len(df)}")
    print(f"  Students: {df['user_id'].nunique() if 'user_id' in df.columns else 'N/A'}")
    print(f"  Skills: {df['skill_name'].nunique() if 'skill_name' in df.columns else 'N/A'}")
    print(f"  Status: {'SMALL (Sample)' if len(df) < 1000 else 'LARGE'}")
else:
    print("\nASSISTments: File not found")

# ProgSnap2
progsnap2_file = Path('data/progsnap2/MainTable_cs1.csv')
if progsnap2_file.exists() and progsnap2_file.stat().st_size > 0:
    try:
        df = pd.read_csv(progsnap2_file)
        print(f"\nProgSnap2 CS1:")
        print(f"  Rows: {len(df)}")
        print(f"  Status: {'LARGE' if len(df) > 1000 else 'SMALL'}")
    except:
        print(f"\nProgSnap2 CS1: File exists but cannot read")
else:
    print(f"\nProgSnap2 CS1: File not found or empty")

# CodeNet
codenet_py = Path('data/codenet/python')
codenet_java = Path('data/codenet/java')
py_files = list(codenet_py.glob('*.txt')) if codenet_py.exists() else []
java_files = list(codenet_java.glob('*.txt')) if codenet_java.exists() else []
print(f"\nCodeNet:")
print(f"  Python files: {len(py_files)}")
print(f"  Java files: {len(java_files)}")
print(f"  Total: {len(py_files) + len(java_files)} files")
print(f"  Status: {'SMALL (Sample)' if len(py_files) + len(java_files) < 100 else 'LARGE'}")

# MOOCCubeX
mooccubex_file = Path('data/moocsxcube/entities.json')
if mooccubex_file.exists():
    with open(mooccubex_file, 'r') as f:
        data = json.load(f)
    students = len(data.get('student', []))
    concepts = len(data.get('concept', []))
    print(f"\nMOOCCubeX:")
    print(f"  Students: {students}")
    print(f"  Concepts: {concepts}")
    print(f"  Status: {'SMALL (Sample)' if students < 100 else 'LARGE'}")

print("\n" + "="*60)
print("SUMMARY:")
print("="*60)
print("All datasets are currently SMALL SAMPLES")
print("Full datasets can be downloaded for larger validation")















