"""
Validate sizes of all downloaded datasets
"""

import os
from pathlib import Path
import json
import pandas as pd
import gzip

def format_size(size_bytes):
    """Format size in human readable format"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} PB"

def check_assistments():
    """Check ASSISTments dataset"""
    print("\n" + "="*60)
    print("ASSISTMENTS DATASET")
    print("="*60)
    
    assistments_dir = Path('data/assistments')
    skill_builder = assistments_dir / 'skill_builder_data.csv'
    
    if skill_builder.exists():
        size = skill_builder.stat().st_size
        print(f"File: skill_builder_data.csv")
        print(f"Size: {format_size(size)}")
        
        try:
            df = pd.read_csv(skill_builder, nrows=0)
            print(f"Columns: {len(df.columns)}")
            
            # Count rows (approximate)
            with open(skill_builder, 'r', encoding='utf-8') as f:
                row_count = sum(1 for _ in f) - 1  # Subtract header
            print(f"Rows: {row_count:,}")
            
            if size > 100 * 1024 * 1024:  # > 100 MB
                print("Status: [OK] LARGE DATASET")
                return True, size, row_count
            else:
                print("Status: [WARNING] Small dataset")
                return False, size, row_count
        except Exception as e:
            print(f"Error reading file: {e}")
            return False, size, 0
    else:
        print("Status: [ERROR] File not found")
        return False, 0, 0

def check_progsnap2():
    """Check ProgSnap2 dataset"""
    print("\n" + "="*60)
    print("PROGSNAP2 DATASET")
    print("="*60)
    
    progsnap_dir = Path('data/progsnap2')
    
    main_table = progsnap_dir / 'MainTable_cs1.csv'
    code_state = progsnap_dir / 'CodeStates.csv'
    
    total_size = 0
    total_rows = 0
    files_found = 0
    
    for file_path in [main_table, code_state]:
        if file_path.exists():
            size = file_path.stat().st_size
            total_size += size
            files_found += 1
            print(f"\nFile: {file_path.name}")
            print(f"Size: {format_size(size)}")
            
            try:
                if file_path.suffix == '.gz':
                    with gzip.open(file_path, 'rt', encoding='utf-8') as f:
                        row_count = sum(1 for _ in f) - 1
                else:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        row_count = sum(1 for _ in f) - 1
                total_rows += row_count
                print(f"Rows: {row_count:,}")
            except Exception as e:
                print(f"Error counting rows: {e}")
    
    # Check for other files
    other_files = list(progsnap_dir.glob('*.csv')) + list(progsnap_dir.glob('*.json'))
    for f in other_files:
        if f.name not in ['MainTable_cs1.csv', 'CodeStates.csv']:
            size = f.stat().st_size
            total_size += size
            files_found += 1
            print(f"\nFile: {f.name}")
            print(f"Size: {format_size(size)}")
    
    print(f"\nTotal files: {files_found}")
    print(f"Total size: {format_size(total_size)}")
    
    if total_size > 50 * 1024 * 1024:  # > 50 MB
        print("Status: [OK] LARGE DATASET")
        return True, total_size, total_rows
    else:
        print("Status: [WARNING] Small dataset")
        return False, total_size, total_rows

def check_codenet():
    """Check CodeNet dataset"""
    print("\n" + "="*60)
    print("CODENET DATASET")
    print("="*60)
    
    codenet_dir = Path('data/codenet')
    
    total_size = 0
    file_count = 0
    code_files = 0
    
    # Check for code files
    for ext in ['.py', '.java', '.cpp', '.c', '.txt']:
        files = list(codenet_dir.rglob(f'*{ext}'))
        for f in files:
            if f.is_file():
                size = f.stat().st_size
                total_size += size
                file_count += 1
                if ext in ['.py', '.java', '.cpp', '.c']:
                    code_files += 1
    
    # Check CSV files
    csv_files = list(codenet_dir.glob('*.csv'))
    for f in csv_files:
        size = f.stat().st_size
        total_size += size
        file_count += 1
    
    print(f"Total files: {file_count}")
    print(f"Code files: {code_files}")
    print(f"Total size: {format_size(total_size)}")
    
    if file_count > 100:  # > 100 files
        print("Status: [OK] LARGE DATASET")
        return True, total_size, file_count
    else:
        print("Status: [WARNING] Small dataset")
        return False, total_size, file_count

def check_mooccubex():
    """Check MOOCCubeX dataset"""
    print("\n" + "="*60)
    print("MOOCCUBEX DATASET")
    print("="*60)
    
    mooccubex_dir = Path('data/moocsxcube')
    
    total_size = 0
    file_count = 0
    
    # Check entities
    entities_dir = mooccubex_dir / 'entities'
    if entities_dir.exists():
        entity_files = list(entities_dir.glob('*.json'))
        for f in entity_files:
            size = f.stat().st_size
            total_size += size
            file_count += 1
            print(f"  {f.name}: {format_size(size)}")
    
    # Check relations
    relations_dir = mooccubex_dir / 'relations'
    if relations_dir.exists():
        relation_files = list(relations_dir.glob('*'))
        for f in relation_files:
            if f.is_file():
                size = f.stat().st_size
                total_size += size
                file_count += 1
                print(f"  {f.name}: {format_size(size)}")
    
    # Check other JSON files
    other_files = list(mooccubex_dir.glob('*.json'))
    for f in other_files:
        if f.name not in ['entities.json', 'entities.json.backup']:
            size = f.stat().st_size
            total_size += size
            file_count += 1
    
    print(f"\nTotal files: {file_count}")
    print(f"Total size: {format_size(total_size)}")
    
    if total_size > 1 * 1024 * 1024 * 1024:  # > 1 GB
        print("Status: [OK] LARGE DATASET")
        return True, total_size, file_count
    else:
        print("Status: [WARNING] Small dataset")
        return False, total_size, file_count

def main():
    print("="*60)
    print("DATASET SIZE VALIDATION")
    print("="*60)
    
    results = {}
    
    # Check all datasets
    results['ASSISTments'] = check_assistments()
    results['ProgSnap2'] = check_progsnap2()
    results['CodeNet'] = check_codenet()
    results['MOOCCubeX'] = check_mooccubex()
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    
    total_size = 0
    all_large = True
    
    for dataset_name, (is_large, size, count) in results.items():
        status = "[OK] LARGE" if is_large else "[WARNING] SMALL"
        total_size += size
        if not is_large:
            all_large = False
        print(f"{dataset_name:15} | {status:15} | {format_size(size):>12} | {count:>12,} items")
    
    print("-" * 60)
    print(f"{'TOTAL':15} | {'':15} | {format_size(total_size):>12} | {'':>12}")
    
    print("\n" + "="*60)
    if all_large:
        print("[OK] ALL DATASETS ARE AT FULL/LARGE SIZE")
    else:
        print("[WARNING] SOME DATASETS ARE STILL SMALL")
    print("="*60)

if __name__ == "__main__":
    main()















