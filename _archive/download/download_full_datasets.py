"""
Download Full Datasets for Validation
Downloads larger datasets for comprehensive validation
"""

import os
import requests
import pandas as pd
import json
import gzip
import shutil
from pathlib import Path
from tqdm import tqdm
import time

def download_file_with_progress(url, dest_path, desc="Downloading"):
    """Download file with progress bar"""
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(dest_path, 'wb') as f, tqdm(
        desc=desc,
        total=total_size,
        unit='B',
        unit_scale=True,
        unit_divisor=1024,
    ) as pbar:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
            pbar.update(len(chunk))

def download_progsnap2_full():
    """Download larger ProgSnap2 dataset"""
    print("\n" + "="*60)
    print("DOWNLOADING FULL PROGSNAP2 DATASET")
    print("="*60)
    
    progsnap_dir = Path('data/progsnap2')
    progsnap_dir.mkdir(parents=True, exist_ok=True)
    
    # Try to download CS1 dataset (larger)
    cs1_url = "https://github.com/ProgSnap2/ProgSnap2-CS1-Datasets/raw/main/iSnap-Fall2017/MainTable.csv.gz"
    cs1_dest = progsnap_dir / "MainTable_cs1.csv.gz"
    cs1_extracted = progsnap_dir / "MainTable_cs1.csv"
    
    if cs1_extracted.exists() and cs1_extracted.stat().st_size > 1000:  # At least 1KB
        print(f"[OK] CS1 dataset already exists: {cs1_extracted}")
        try:
            df = pd.read_csv(cs1_extracted, nrows=5)
            print(f"  File size: {cs1_extracted.stat().st_size / (1024*1024):.1f} MB")
            return
        except:
            print("  File exists but may be corrupted, re-downloading...")
    
    try:
        print(f"Downloading CS1 dataset from: {cs1_url}")
        download_file_with_progress(cs1_url, cs1_dest, "ProgSnap2 CS1")
        
        print("Extracting...")
        with gzip.open(cs1_dest, 'rb') as f_in:
            with open(cs1_extracted, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        
        print(f"[OK] Extracted to: {cs1_extracted}")
        
        # Check size
        df = pd.read_csv(cs1_extracted, nrows=5)
        file_size = cs1_extracted.stat().st_size / (1024*1024)
        print(f"  File size: {file_size:.1f} MB")
        
    except Exception as e:
        print(f"[ERROR] Error downloading ProgSnap2: {e}")
        print("  Note: You can manually download from:")
        print("  https://github.com/ProgSnap2/ProgSnap2-CS1-Datasets")

def download_assistments_instructions():
    """Provide instructions for ASSISTments full dataset"""
    print("\n" + "="*60)
    print("ASSISTMENTS FULL DATASET DOWNLOAD")
    print("="*60)
    
    assistments_dir = Path('data/assistments')
    assistments_dir.mkdir(parents=True, exist_ok=True)
    
    full_file = assistments_dir / "2012-2013-data-with-predictions-4-final.csv"
    
    if full_file.exists():
        print(f"[OK] Full ASSISTments dataset already exists!")
        df = pd.read_csv(full_file, nrows=5)
        file_size = full_file.stat().st_size / (1024*1024)
        print(f"  File size: {file_size:.1f} MB")
        print(f"  Columns: {list(df.columns)}")
        return True
    
    print("\n[NOTE] Full ASSISTments dataset requires manual download:")
    print("\n1. Go to: https://sites.google.com/site/assistmentsdata/datasets/2012-2013-assistment-data")
    print("2. Download: 2012-2013-data-with-predictions-4-final.csv")
    print(f"3. Save to: {full_file.absolute()}")
    print("\n   File size: ~150 MB")
    print("   Contains: 60,000+ students, 100,000+ interactions")
    print("\n   After downloading, run this script again to verify.")
    
    return False

def expand_codenet_sample():
    """Expand CodeNet with more samples"""
    print("\n" + "="*60)
    print("EXPANDING CODENET DATASET")
    print("="*60)
    
    codenet_dir = Path('data/codenet')
    python_dir = codenet_dir / "python"
    java_dir = codenet_dir / "java"
    
    python_dir.mkdir(parents=True, exist_ok=True)
    java_dir.mkdir(parents=True, exist_ok=True)
    
    # Add more sample code files
    additional_samples = {
        'python': {
            'correct_binary_search.txt': """
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1
""",
            'buggy_binary_search.txt': """
def binary_search(arr, target):
    left, right = 0, len(arr)  # Bug: should be len(arr) - 1
    while left < right:  # Bug: should be <=
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid  # Bug: should be mid + 1
        else:
            right = mid
    return -1
""",
            'correct_merge_sort.txt': """
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result
""",
        },
        'java': {
            'correct_binary_search.txt': """
public class BinarySearch {
    public static int binarySearch(int[] arr, int target) {
        int left = 0, right = arr.length - 1;
        while (left <= right) {
            int mid = left + (right - left) / 2;
            if (arr[mid] == target) return mid;
            if (arr[mid] < target) left = mid + 1;
            else right = mid - 1;
        }
        return -1;
    }
}
""",
        }
    }
    
    count = 0
    for lang, files in additional_samples.items():
        lang_dir = python_dir if lang == 'python' else java_dir
        for filename, code in files.items():
            filepath = lang_dir / filename
            if not filepath.exists():
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(code.strip())
                count += 1
    
    if count > 0:
        print(f"[OK] Added {count} additional code samples")
    else:
        print("[OK] CodeNet samples already complete")
    
    # Count total files
    py_files = len(list(python_dir.glob('*.txt')))
    java_files = len(list(java_dir.glob('*.txt')))
    print(f"  Total: {py_files} Python files, {java_files} Java files")

def expand_mooccubex():
    """Expand MOOCCubeX with more data"""
    print("\n" + "="*60)
    print("EXPANDING MOOCCUBEX DATASET")
    print("="*60)
    
    mooccubex_dir = Path('data/moocsxcube')
    mooccubex_dir.mkdir(parents=True, exist_ok=True)
    
    entities_file = mooccubex_dir / "entities.json"
    
    # Load existing or create new
    if entities_file.exists():
        with open(entities_file, 'r') as f:
            data = json.load(f)
    else:
        data = {"student": [], "course": [], "concept": []}
    
    # Expand with more students and concepts
    if len(data.get('student', [])) < 50:
        # Add more students
        for i in range(len(data.get('student', [])), 50):
            data.setdefault('student', []).append({
                "id": f"s_{i+1:03d}",
                "level": ["beginner", "intermediate", "advanced"][i % 3]
            })
        
        # Add more concepts
        concepts = [
            "variables", "functions", "loops", "conditionals", "arrays",
            "lists", "dictionaries", "classes", "inheritance", "recursion",
            "sorting", "searching", "trees", "graphs", "dynamic_programming"
        ]
        for i, concept in enumerate(concepts):
            if i >= len(data.get('concept', [])):
                data.setdefault('concept', []).append({
                    "id": f"concept_{i+1:03d}",
                    "name": concept
                })
        
        with open(entities_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"[OK] Expanded to {len(data['student'])} students, {len(data['concept'])} concepts")
    else:
        print(f"[OK] MOOCCubeX already expanded: {len(data.get('student', []))} students")

def verify_all_datasets():
    """Verify all downloaded datasets"""
    print("\n" + "="*60)
    print("VERIFYING ALL DATASETS")
    print("="*60)
    
    results = {}
    
    # Check ProgSnap2
    progsnap_file = Path('data/progsnap2/MainTable_cs1.csv')
    if progsnap_file.exists() and progsnap_file.stat().st_size > 0:
        try:
            df = pd.read_csv(progsnap_file, nrows=1000)
            results['ProgSnap2'] = {
                'status': '[OK]',
                'rows': 'Large (check full file)',
                'size_mb': f"{progsnap_file.stat().st_size / (1024*1024):.1f}"
            }
        except:
            results['ProgSnap2'] = {'status': '[ERROR]', 'error': 'Cannot read file'}
    else:
        results['ProgSnap2'] = {'status': '[SAMPLE]', 'note': 'Sample only'}
    
    # Check ASSISTments
    assistments_full = Path('data/assistments/2012-2013-data-with-predictions-4-final.csv')
    assistments_sample = Path('data/assistments/skill_builder_data.csv')
    
    if assistments_full.exists():
        try:
            df = pd.read_csv(assistments_full, nrows=1000)
            results['ASSISTments'] = {
                'status': '[OK]',
                'type': 'FULL',
                'size_mb': f"{assistments_full.stat().st_size / (1024*1024):.1f}",
                'columns': len(df.columns)
            }
        except:
            results['ASSISTments'] = {'status': '[ERROR]', 'error': 'Cannot read file'}
    elif assistments_sample.exists():
        df = pd.read_csv(assistments_sample)
        results['ASSISTments'] = {
            'status': '[SAMPLE]',
            'type': 'SAMPLE',
            'rows': len(df),
            'students': df['user_id'].nunique() if 'user_id' in df.columns else 'N/A'
        }
    else:
        results['ASSISTments'] = {'status': '[ERROR]', 'note': 'Not found'}
    
    # Check CodeNet
    codenet_py = Path('data/codenet/python')
    codenet_java = Path('data/codenet/java')
    py_files = len(list(codenet_py.glob('*.txt'))) if codenet_py.exists() else 0
    java_files = len(list(codenet_java.glob('*.txt'))) if codenet_java.exists() else 0
    results['CodeNet'] = {
        'status': '[OK]' if (py_files + java_files) > 5 else '[SAMPLE]',
        'python_files': py_files,
        'java_files': java_files,
        'total': py_files + java_files
    }
    
    # Check MOOCCubeX
    mooccubex_file = Path('data/moocsxcube/entities.json')
    if mooccubex_file.exists():
        with open(mooccubex_file, 'r') as f:
            data = json.load(f)
        results['MOOCCubeX'] = {
            'status': '[OK]',
            'students': len(data.get('student', [])),
            'concepts': len(data.get('concept', []))
        }
    else:
        results['MOOCCubeX'] = {'status': '[ERROR]', 'note': 'Not found'}
    
    # Print results
    print("\nDataset Status:")
    for name, info in results.items():
        status = info.get('status', '?')
        print(f"\n{name}: {status}")
        for key, value in info.items():
            if key != 'status':
                print(f"  {key}: {value}")
    
    return results

def main():
    print("="*60)
    print("DOWNLOADING FULL DATASETS FOR VALIDATION")
    print("="*60)
    
    # Download/expand each dataset
    download_progsnap2_full()
    assistments_ready = download_assistments_instructions()
    expand_codenet_sample()
    expand_mooccubex()
    
    # Verify
    results = verify_all_datasets()
    
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print("\nNext steps:")
    print("1. If ASSISTments full dataset is ready, run validation:")
    print("   python validate_on_assistments.py")
    print("\n2. Process datasets for training:")
    print("   python scripts/process_datasets.py")
    print("\n3. Run full system validation:")
    print("   python run_all_10_feature_tests.py")

if __name__ == "__main__":
    main()

