"""
Download MOOCCubeX Dataset - Correct Method
"""

import requests
import json
import subprocess
import shutil
from pathlib import Path
from tqdm import tqdm
import os

def download_file(url, dest_path, desc="Downloading"):
    """Download file with progress"""
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        response = requests.get(url, stream=True, timeout=120)
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

def clone_mooccubex_repo():
    """Clone MOOCCubeX repository using git"""
    print("\n" + "="*60)
    print("DOWNLOADING MOOCCUBEX FROM GITHUB")
    print("="*60)
    
    mooccubex_dir = Path('data/moocsxcube')
    mooccubex_dir.mkdir(parents=True, exist_ok=True)
    
    # Try the correct repository name
    repo_url = "https://github.com/THU-KEG/MOOCCubeX.git"
    temp_dir = Path('temp_mooccubex')
    
    # Remove temp directory if exists
    if temp_dir.exists():
        print("Removing existing temp directory...")
        try:
            shutil.rmtree(temp_dir)
        except:
            # Force remove on Windows
            os.system(f'rmdir /s /q {temp_dir}' if os.name == 'nt' else f'rm -rf {temp_dir}')
    
    print(f"\nCloning repository: {repo_url}")
    print("This may take a few minutes...")
    
    try:
        result = subprocess.run(
            ['git', 'clone', '--depth', '1', repo_url, str(temp_dir)],
            capture_output=True,
            text=True,
            timeout=600
        )
        
        if result.returncode == 0:
            print("[OK] Repository cloned successfully!")
            
            # Find and copy data files
            print("\nSearching for data files...")
            
            # Look for JSON files
            json_files = list(temp_dir.rglob('*.json'))
            csv_files = list(temp_dir.rglob('*.csv'))
            
            print(f"  Found {len(json_files)} JSON files, {len(csv_files)} CSV files")
            
            copied = 0
            for data_file in json_files + csv_files:
                # Skip node_modules and very large files
                if 'node_modules' in str(data_file) or data_file.stat().st_size > 500000000:  # > 500MB
                    continue
                
                # Copy to mooccubex directory
                dest = mooccubex_dir / data_file.name
                if not dest.exists() or dest.stat().st_size < data_file.stat().st_size:
                    try:
                        shutil.copy2(data_file, dest)
                        size_mb = dest.stat().st_size / (1024*1024)
                        print(f"  [OK] Copied {data_file.name} ({size_mb:.1f} MB)")
                        copied += 1
                    except Exception as e:
                        print(f"  [ERROR] Could not copy {data_file.name}: {e}")
            
            # Also copy data directories
            data_dirs = [d for d in temp_dir.iterdir() if d.is_dir() and d.name.lower() in ['data', 'dataset', 'datasets', 'raw']]
            for data_dir in data_dirs:
                dest_dir = mooccubex_dir / data_dir.name
                if not dest_dir.exists():
                    try:
                        shutil.copytree(data_dir, dest_dir)
                        print(f"  [OK] Copied {data_dir.name} directory")
                    except Exception as e:
                        print(f"  [ERROR] Could not copy {data_dir.name}: {e}")
            
            # Cleanup
            print("\nCleaning up temp directory...")
            try:
                shutil.rmtree(temp_dir)
            except:
                os.system(f'rmdir /s /q {temp_dir}' if os.name == 'nt' else f'rm -rf {temp_dir}')
            
            if copied > 0:
                print(f"\n[OK] Successfully downloaded {copied} MOOCCubeX files!")
                return True
            else:
                print("\n[WARNING] Repository cloned but no data files found")
                return False
        else:
            print(f"[ERROR] Git clone failed:")
            print(f"  {result.stderr}")
            return False
            
    except FileNotFoundError:
        print("[ERROR] Git not found. Please install Git to download from GitHub.")
        return False
    except subprocess.TimeoutExpired:
        print("[ERROR] Clone timed out. Repository may be very large.")
        return False
    except Exception as e:
        print(f"[ERROR] {e}")
        return False

def verify_download():
    """Verify MOOCCubeX download"""
    print("\n" + "="*60)
    print("VERIFICATION")
    print("="*60)
    
    mooccubex_dir = Path('data/moocsxcube')
    
    json_files = list(mooccubex_dir.glob('*.json'))
    csv_files = list(mooccubex_dir.glob('*.csv'))
    
    if json_files or csv_files:
        print(f"\n[OK] MOOCCubeX files found:")
        total_size = 0
        
        for f in json_files + csv_files:
            size_mb = f.stat().st_size / (1024*1024)
            total_size += f.stat().st_size
            print(f"  {f.name}: {size_mb:.1f} MB")
            
            # Try to show structure for JSON files
            if f.suffix == '.json':
                try:
                    with open(f, 'r', encoding='utf-8') as file:
                        data = json.load(file)
                        if isinstance(data, dict):
                            print(f"    Keys: {list(data.keys())[:5]}")
                            for key in list(data.keys())[:3]:
                                if isinstance(data[key], list):
                                    print(f"    {key}: {len(data[key])} items")
                        elif isinstance(data, list):
                            print(f"    Items: {len(data)}")
                except:
                    pass
        
        print(f"\n  Total size: {total_size / (1024*1024):.1f} MB")
        print(f"  Status: [OK] Downloaded")
        return True
    else:
        print("\n[ERROR] No MOOCCubeX files found in data/moocsxcube/")
        return False

def main():
    print("="*60)
    print("DOWNLOADING MOOCCUBEX DATASET")
    print("="*60)
    print("\nAttempting to download from GitHub repository...")
    
    success = clone_mooccubex_repo()
    
    if success:
        verify_download()
    else:
        print("\n[NOTE] Download failed. MOOCCubeX may require:")
        print("  1. Manual download from: https://github.com/THU-KEG/MOOCCubeX")
        print("  2. Or the repository structure may have changed")
        verify_download()  # Check what we have

if __name__ == "__main__":
    main()















