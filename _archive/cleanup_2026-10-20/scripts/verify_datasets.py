"""
Verify downloaded datasets are correctly formatted
"""

import pandas as pd
import json
from pathlib import Path


def verify_progsnap2(data_dir: Path):
    """Verify ProgSnap2 dataset"""
    print("\n=== Verifying ProgSnap2 ===")
    progsnap_dir = data_dir / "progsnap2"
    
    if not progsnap_dir.exists():
        print("✗ ProgSnap2 directory not found")
        return False
    
    # Check for MainTable.csv
    main_table = progsnap_dir / "MainTable.csv"
    if main_table.exists():
        df = pd.read_csv(main_table)
        print(f"✓ MainTable.csv found: {len(df)} rows")
        print(f"  Columns: {list(df.columns)}")
        return True
    else:
        print("✗ MainTable.csv not found")
        return False


def verify_codenet(data_dir: Path):
    """Verify CodeNet dataset"""
    print("\n=== Verifying CodeNet ===")
    codenet_dir = data_dir / "codenet"
    
    if not codenet_dir.exists():
        print("✗ CodeNet directory not found")
        return False
    
    languages = ["python", "java", "cpp"]
    total_files = 0
    
    for lang in languages:
        lang_dir = codenet_dir / lang
        if lang_dir.exists():
            files = list(lang_dir.glob("*.txt"))
            print(f"✓ {lang}: {len(files)} code files")
            total_files += len(files)
        else:
            print(f"✗ {lang} directory not found")
    
    return total_files > 0


def verify_assistments(data_dir: Path):
    """Verify ASSISTments dataset"""
    print("\n=== Verifying ASSISTments ===")
    assistments_dir = data_dir / "assistments"
    
    if not assistments_dir.exists():
        print("✗ ASSISTments directory not found")
        return False
    
    skill_builder = assistments_dir / "skill_builder_data.csv"
    if skill_builder.exists():
        df = pd.read_csv(skill_builder)
        print(f"✓ skill_builder_data.csv found: {len(df)} responses")
        print(f"  Students: {df['user_id'].nunique()}")
        print(f"  Problems: {df['problem_id'].nunique()}")
        print(f"  Skills: {df['skill_name'].nunique()}")
        return True
    else:
        print("✗ skill_builder_data.csv not found")
        return False


def verify_mooccubex(data_dir: Path):
    """Verify MOOCCubeX dataset"""
    print("\n=== Verifying MOOCCubeX ===")
    mooc_dir = data_dir / "moocsxcube"
    
    if not mooc_dir.exists():
        print("✗ MOOCCubeX directory not found")
        return False
    
    files = ["entities.json", "relations.json", "knowledge_graph.json"]
    all_exist = True
    
    for file in files:
        filepath = mooc_dir / file
        if filepath.exists():
            with open(filepath, 'r') as f:
                data = json.load(f)
            print(f"✓ {file} found")
            if file == "entities.json":
                print(f"  Students: {len(data.get('student', []))}")
                print(f"  Courses: {len(data.get('course', []))}")
                print(f"  Concepts: {len(data.get('concept', []))}")
        else:
            print(f"✗ {file} not found")
            all_exist = False
    
    return all_exist


def main():
    data_dir = Path("data")
    
    print("=" * 60)
    print("VERIFYING DATASETS")
    print("=" * 60)
    
    results = {
        "ProgSnap2": verify_progsnap2(data_dir),
        "CodeNet": verify_codenet(data_dir),
        "ASSISTments": verify_assistments(data_dir),
        "MOOCCubeX": verify_mooccubex(data_dir)
    }
    
    print("\n" + "=" * 60)
    print("VERIFICATION SUMMARY")
    print("=" * 60)
    
    for dataset, status in results.items():
        status_str = "✓ PASS" if status else "✗ FAIL"
        print(f"{dataset:20s}: {status_str}")
    
    all_pass = all(results.values())
    
    if all_pass:
        print("\n✓ All datasets verified successfully!")
        print("\nReady to process and train!")
    else:
        print("\n⚠ Some datasets failed verification")
        print("Run: python scripts/download_datasets.py")


if __name__ == "__main__":
    main()




















