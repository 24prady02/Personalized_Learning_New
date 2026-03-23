"""
Download Real Datasets from GitHub and Public Sources
"""

import requests
import pandas as pd
import json
import gzip
import shutil
from pathlib import Path
from tqdm import tqdm
import os

def download_file(url, dest_path, desc="Downloading"):
    """Download file with progress bar"""
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        response = requests.get(url, stream=True, timeout=60)
        response.raise_for_status()
        total_size = int(response.headers.get('content-length', 0))
        
        with open(dest_path, 'wb') as f, tqdm(
            desc=desc,
            total=total_size,
            unit='B',
            unit_scale=True,
            unit_divisor=1024,
        ) as pbar:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    pbar.update(len(chunk))
        return True
    except Exception as e:
        print(f"  Error: {e}")
        return False

def download_progsnap2_from_github():
    """Download ProgSnap2 from GitHub"""
    print("\n" + "="*60)
    print("DOWNLOADING PROGSNAP2 FROM GITHUB")
    print("="*60)
    
    progsnap_dir = Path('data/progsnap2')
    progsnap_dir.mkdir(parents=True, exist_ok=True)
    
    # Try multiple GitHub sources
    urls = [
        # Official ProgSnap2 spec repository
        "https://raw.githubusercontent.com/ProgSnap2/progsnap2-spec/master/datasets/Sample/MainTable.csv",
        # Alternative: CS1 datasets
        "https://github.com/ProgSnap2/ProgSnap2-CS1-Datasets/raw/main/iSnap-Fall2017/MainTable.csv",
        # Try other repositories
        "https://raw.githubusercontent.com/kevinlondon/ProgSnap2/master/datasets/sample/MainTable.csv",
    ]
    
    for url in urls:
        print(f"\nTrying: {url}")
        dest = progsnap_dir / "MainTable.csv"
        
        if download_file(url, dest, "ProgSnap2"):
            if dest.exists() and dest.stat().st_size > 1000:
                print(f"[OK] Downloaded: {dest.stat().st_size / (1024*1024):.1f} MB")
                return True
    
    print("\n[NOTE] Direct download failed. Try manual download from:")
    print("  https://github.com/ProgSnap2/progsnap2-spec")
    return False

def download_codenet_from_github():
    """Download CodeNet samples from GitHub"""
    print("\n" + "="*60)
    print("DOWNLOADING CODENET FROM GITHUB")
    print("="*60)
    
    codenet_dir = Path('data/codenet')
    python_dir = codenet_dir / "python"
    java_dir = codenet_dir / "java"
    cpp_dir = codenet_dir / "c++"
    
    python_dir.mkdir(parents=True, exist_ok=True)
    java_dir.mkdir(parents=True, exist_ok=True)
    cpp_dir.mkdir(parents=True, exist_ok=True)
    
    # Download problem list
    metadata_url = "https://raw.githubusercontent.com/IBM/Project_CodeNet/master/metadata/problem_list.csv"
    metadata_path = codenet_dir / "problem_list.csv"
    
    print("Downloading problem metadata...")
    download_file(metadata_url, metadata_path, "Problem List")
    
    # Try to download sample code files from GitHub
    base_url = "https://raw.githubusercontent.com/IBM/Project_CodeNet/master/data"
    
    # Download a few sample problems
    sample_problems = ["p00000", "p00001", "p00002", "p00003", "p00004"]
    languages = ["Python", "Java", "C++"]
    
    downloaded = 0
    for problem in sample_problems:
        for lang in languages:
            lang_lower = lang.lower().replace("++", "pp")
            # Try different file paths
            urls = [
                f"{base_url}/{problem}/{lang_lower}/solutions/{problem}.{lang_lower}",
                f"{base_url}/{problem}/{lang}/solutions/{problem}.{lang_lower}",
            ]
            
            for url in urls:
                if lang == "Python":
                    dest = python_dir / f"{problem}.py"
                elif lang == "Java":
                    dest = java_dir / f"{problem}.java"
                else:
                    dest = cpp_dir / f"{problem}.cpp"
                
                if download_file(url, dest, f"{problem}_{lang}"):
                    downloaded += 1
                    break
    
    print(f"\n[OK] Downloaded {downloaded} code files from GitHub")
    return downloaded > 0

def download_assistments_alternative():
    """Try to find ASSISTments dataset from alternative sources"""
    print("\n" + "="*60)
    print("SEARCHING FOR ASSISTMENTS DATASET")
    print("="*60)
    
    assistments_dir = Path('data/assistments')
    assistments_dir.mkdir(parents=True, exist_ok=True)
    
    # Try Kaggle API if available
    try:
        import kaggle
        print("Kaggle API found, searching for ASSISTments dataset...")
        # Would need kaggle.json credentials
        print("  Note: Requires Kaggle API credentials")
    except:
        print("Kaggle API not available")
    
    # Try direct links
    urls = [
        # These would need to be actual working links
        "https://www.kaggle.com/datasets/nicapotato/wisdm-dataset/download",
    ]
    
    print("\n[NOTE] ASSISTments requires manual download:")
    print("  1. Visit: https://sites.google.com/site/assistmentsdata/")
    print("  2. Download: 2012-2013-data-with-predictions-4-final.csv")
    print(f"  3. Save to: {assistments_dir.absolute()}")
    
    return False

def download_mooccubex_from_github():
    """Download MOOCCubeX from GitHub"""
    print("\n" + "="*60)
    print("DOWNLOADING MOOCCUBEX FROM GITHUB")
    print("="*60)
    
    mooccubex_dir = Path('data/moocsxcube')
    mooccubex_dir.mkdir(parents=True, exist_ok=True)
    
    # Try GitHub repositories
    urls = [
        "https://raw.githubusercontent.com/THU-KEG/MOOC-Cube/master/data/entities.json",
        "https://github.com/THU-KEG/MOOC-Cube/raw/master/data/knowledge_graph.json",
    ]
    
    downloaded = 0
    for url in urls:
        filename = url.split('/')[-1]
        dest = mooccubex_dir / filename
        
        if download_file(url, dest, filename):
            downloaded += 1
    
    print(f"\n[OK] Downloaded {downloaded} MOOCCubeX files")
    return downloaded > 0

def main():
    print("="*60)
    print("DOWNLOADING REAL DATASETS FROM GITHUB")
    print("="*60)
    
    # Download from GitHub
    download_progsnap2_from_github()
    download_codenet_from_github()
    download_mooccubex_from_github()
    download_assistments_alternative()
    
    print("\n" + "="*60)
    print("DOWNLOAD COMPLETE")
    print("="*60)
    print("\nNote: Some datasets may require manual download.")
    print("Check the output above for instructions.")

if __name__ == "__main__":
    main()















