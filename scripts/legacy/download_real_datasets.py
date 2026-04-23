"""
Download Real Datasets - Using Found Links
"""

import requests
import pandas as pd
import json
import gzip
import shutil
from pathlib import Path
from tqdm import tqdm
import subprocess
import sys

def download_google_drive_file(file_id, dest_path):
    """Download file from Google Drive"""
    print(f"Downloading from Google Drive (ID: {file_id})...")
    
    # Google Drive direct download URL
    url = f"https://drive.google.com/uc?export=download&id={file_id}"
    
    session = requests.Session()
    response = session.get(url, stream=True)
    
    # Handle large files that require confirmation
    if 'virus scan warning' in response.text.lower():
        # Extract download link
        confirm_link = response.url
        response = session.get(confirm_link, stream=True)
    
    total_size = int(response.headers.get('content-length', 0))
    
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(dest_path, 'wb') as f, tqdm(
        desc="Downloading",
        total=total_size,
        unit='B',
        unit_scale=True,
        unit_divisor=1024,
    ) as pbar:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
                pbar.update(len(chunk))
    
    return dest_path.exists() and dest_path.stat().st_size > 1000

def download_assistments_from_drive():
    """Download ASSISTments from Google Drive"""
    print("\n" + "="*60)
    print("DOWNLOADING ASSISTMENTS FROM GOOGLE DRIVE")
    print("="*60)
    
    assistments_dir = Path('data/assistments')
    assistments_dir.mkdir(parents=True, exist_ok=True)
    
    output_file = assistments_dir / "2012-2013-data-with-predictions-4-final.csv"
    
    if output_file.exists() and output_file.stat().st_size > 10000000:  # > 10MB
        print(f"[OK] File already exists: {output_file.stat().st_size / (1024*1024):.1f} MB")
        return True
    
    # Google Drive file ID from search results
    file_id = "1cU6Ft4R3hLqA7G1rIGArVfelSZvc6RxY"
    
    print("Attempting to download ASSISTments dataset from Google Drive...")
    print("This may take several minutes (file is ~150 MB)...")
    
    if download_google_drive_file(file_id, output_file):
        print(f"\n[OK] Successfully downloaded!")
        print(f"  File size: {output_file.stat().st_size / (1024*1024):.1f} MB")
        return True
    else:
        print("\n[NOTE] Automatic download failed.")
        print("Please download manually from:")
        print("  https://drive.google.com/file/d/1cU6Ft4R3hLqA7G1rIGArVfelSZvc6RxY/view")
        print(f"  Save to: {output_file.absolute()}")
        return False

def download_progsnap2_alternative():
    """Try alternative methods for ProgSnap2"""
    print("\n" + "="*60)
    print("DOWNLOADING PROGSNAP2")
    print("="*60)
    
    progsnap_dir = Path('data/progsnap2')
    progsnap_dir.mkdir(parents=True, exist_ok=True)
    
    # Try using git clone if git is available
    print("Attempting to clone ProgSnap2 repository...")
    try:
        repo_url = "https://github.com/ProgSnap2/progsnap2-spec.git"
        clone_dir = Path('temp_progsnap2')
        
        if clone_dir.exists():
            shutil.rmtree(clone_dir)
        
        result = subprocess.run(
            ['git', 'clone', '--depth', '1', repo_url, str(clone_dir)],
            capture_output=True,
            text=True,
            timeout=300
        )
        
        if result.returncode == 0:
            # Find MainTable.csv files
            csv_files = list(clone_dir.rglob('MainTable.csv'))
            if csv_files:
                for csv_file in csv_files:
                    dest = progsnap_dir / csv_file.name
                    shutil.copy2(csv_file, dest)
                    print(f"[OK] Copied: {dest.name} ({dest.stat().st_size / (1024*1024):.1f} MB)")
                
                shutil.rmtree(clone_dir)
                return True
        else:
            print(f"Git clone failed: {result.stderr}")
    except FileNotFoundError:
        print("Git not found. Skipping git clone method.")
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n[NOTE] Please download ProgSnap2 manually from:")
    print("  https://github.com/ProgSnap2/progsnap2-spec")
    return False

def download_codenet_alternative():
    """Try alternative methods for CodeNet"""
    print("\n" + "="*60)
    print("DOWNLOADING CODENET")
    print("="*60)
    
    codenet_dir = Path('data/codenet')
    codenet_dir.mkdir(parents=True, exist_ok=True)
    
    # Try cloning repository
    print("Attempting to clone CodeNet repository...")
    try:
        repo_url = "https://github.com/IBM/Project_CodeNet.git"
        clone_dir = Path('temp_codenet')
        
        if clone_dir.exists():
            shutil.rmtree(clone_dir)
        
        # Clone with limited depth to save time
        result = subprocess.run(
            ['git', 'clone', '--depth', '1', '--filter=blob:none', repo_url, str(clone_dir)],
            capture_output=True,
            text=True,
            timeout=600
        )
        
        if result.returncode == 0:
            # Copy metadata
            metadata_file = clone_dir / "metadata" / "problem_list.csv"
            if metadata_file.exists():
                dest = codenet_dir / "problem_list.csv"
                shutil.copy2(metadata_file, dest)
                print(f"[OK] Copied metadata: {dest.name}")
            
            # Note: Full CodeNet is 100GB+, so we'll just get structure
            print("[NOTE] Full CodeNet is 100GB+. Repository cloned for structure.")
            print("  To get full dataset, download from IBM Research directly.")
            
            shutil.rmtree(clone_dir)
            return True
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n[NOTE] CodeNet full dataset (100GB+) requires:")
    print("  1. Visit: https://developer.ibm.com/exchanges/data/all/project-codenet/")
    print("  2. Register and download")
    return False

def download_mooccubex_alternative():
    """Try alternative methods for MOOCCubeX"""
    print("\n" + "="*60)
    print("DOWNLOADING MOOCCUBEX")
    print("="*60)
    
    mooccubex_dir = Path('data/moocsxcube')
    mooccubex_dir.mkdir(parents=True, exist_ok=True)
    
    # Try different repository paths
    repos = [
        "https://github.com/THU-KEG/MOOC-Cube.git",
        "https://github.com/epfl-ml4ed/mooc-cubex.git",
    ]
    
    for repo_url in repos:
        print(f"\nTrying: {repo_url}")
        try:
            clone_dir = Path('temp_mooccubex')
            
            if clone_dir.exists():
                shutil.rmtree(clone_dir)
            
            result = subprocess.run(
                ['git', 'clone', '--depth', '1', repo_url, str(clone_dir)],
                capture_output=True,
                text=True,
                timeout=300
            )
            
            if result.returncode == 0:
                # Find JSON files
                json_files = list(clone_dir.rglob('*.json'))
                for json_file in json_files[:5]:  # Limit to first 5
                    dest = mooccubex_dir / json_file.name
                    shutil.copy2(json_file, dest)
                    print(f"[OK] Copied: {dest.name}")
                
                shutil.rmtree(clone_dir)
                return True
        except Exception as e:
            print(f"  Error: {e}")
            continue
    
    print("\n[NOTE] MOOCCubeX download failed. Try manual download.")
    return False

def main():
    print("="*60)
    print("DOWNLOADING REAL DATASETS FROM SOURCES")
    print("="*60)
    print("\nThis will attempt to download real datasets from:")
    print("  - ASSISTments: Google Drive")
    print("  - ProgSnap2: GitHub repository")
    print("  - CodeNet: GitHub repository")
    print("  - MOOCCubeX: GitHub repository")
    print("\nThis may take 10-30 minutes depending on your connection...\n")
    
    # Download each dataset
    download_assistments_from_drive()
    download_progsnap2_alternative()
    download_codenet_alternative()
    download_mooccubex_alternative()
    
    # Verify
    print("\n" + "="*60)
    print("VERIFICATION")
    print("="*60)
    
    assistments_file = Path('data/assistments/2012-2013-data-with-predictions-4-final.csv')
    if assistments_file.exists() and assistments_file.stat().st_size > 1000000:
        print(f"\nASSISTments: [OK]")
        print(f"  Size: {assistments_file.stat().st_size / (1024*1024):.1f} MB")
    
    progsnap_files = list(Path('data/progsnap2').glob('MainTable*.csv'))
    if progsnap_files:
        for f in progsnap_files:
            print(f"\nProgSnap2: [OK] {f.name}")
            print(f"  Size: {f.stat().st_size / (1024*1024):.1f} MB")
    
    codenet_metadata = Path('data/codenet/problem_list.csv')
    if codenet_metadata.exists():
        print(f"\nCodeNet: [OK] Metadata downloaded")
    
    mooccubex_files = list(Path('data/moocsxcube').glob('*.json'))
    if mooccubex_files:
        print(f"\nMOOCCubeX: [OK] {len(mooccubex_files)} files")
    
    print("\n" + "="*60)
    print("DOWNLOAD COMPLETE!")
    print("="*60)

if __name__ == "__main__":
    main()















