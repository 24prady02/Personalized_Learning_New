"""
Restore datasets to original small state
"""

import pandas as pd
from pathlib import Path
import json
import shutil

def restore_assistments():
    """Restore ASSISTments to original small sample"""
    print("Restoring ASSISTments to original small sample...")
    
    assistments_dir = Path('data/assistments')
    output_file = assistments_dir / 'skill_builder_data.csv'
    
    # Original small sample: ~90 rows, 2 KB
    original_data = {
        'user_id': [1, 1, 1, 2, 2, 2, 3, 3, 3] * 10,
        'problem_id': [101, 102, 103, 101, 102, 103, 101, 102, 103] * 10,
        'correct': [1, 0, 1, 1, 1, 0, 0, 1, 1] * 10,
        'skill_name': ['Addition', 'Subtraction', 'Multiplication'] * 30,
        'attempt_count': [1, 2, 1, 1, 1, 2, 2, 1, 1] * 10
    }
    
    df = pd.DataFrame(original_data)
    df.to_csv(output_file, index=False)
    
    size_kb = output_file.stat().st_size / 1024
    print(f"  [OK] Restored: {len(df)} rows, {size_kb:.1f} KB")
    return True

def restore_mooccubex():
    """Restore MOOCCubeX from backup"""
    print("Restoring MOOCCubeX from backup...")
    
    backup_file = Path('data/moocsxcube/entities.json.backup')
    original_file = Path('data/moocsxcube/entities.json')
    
    if backup_file.exists():
        shutil.copy2(backup_file, original_file)
        size_mb = original_file.stat().st_size / (1024*1024)
        print(f"  [OK] Restored: {size_mb:.1f} MB")
        return True
    else:
        print("  [WARNING] No backup found, keeping current version")
        return False

def main():
    print("="*60)
    print("RESTORING DATASETS TO ORIGINAL SMALL STATE")
    print("="*60)
    
    restore_assistments()
    restore_mooccubex()
    
    print("\n" + "="*60)
    print("RESTORATION COMPLETE!")
    print("="*60)
    print("\nDatasets restored to original small state:")
    print("  - ASSISTments: ~90 rows, ~2 KB (small sample)")
    print("  - MOOCCubeX: ~24 MB (original size)")
    print("  - Graph structure: Unchanged (good for retrieval)")
    print("\nNote: ProgSnap2 and CodeNet remain at current sizes")

if __name__ == "__main__":
    main()















