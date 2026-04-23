"""
Download MOOCCubeX Dataset from GitHub
"""

import requests
import json
import subprocess
import shutil
from pathlib import Path
from tqdm import tqdm

def download_file(url, dest_path, desc="Downloading"):
    """Download file with progress"""
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

def download_mooccubex_from_github():
    """Download MOOCCubeX from GitHub"""
    print("\n" + "="*60)
    print("DOWNLOADING MOOCCUBEX FROM GITHUB")
    print("="*60)
    
    mooccubex_dir = Path('data/moocsxcube')
    mooccubex_dir.mkdir(parents=True, exist_ok=True)
    
    # Try different repository paths and file locations
    base_urls = [
        "https://raw.githubusercontent.com/THU-KEG/MOOC-Cube/master/data/",
        "https://raw.githubusercontent.com/THU-KEG/MOOC-Cube/main/data/",
        "https://raw.githubusercontent.com/epfl-ml4ed/mooc-cubex/main/data/",
    ]
    
    files_to_download = [
        "entities.json",
        "knowledge_graph.json",
        "relations.json",
        "student_course.json",
        "course_concept.json",
    ]
    
    downloaded = 0
    for base_url in base_urls:
        print(f"\nTrying base URL: {base_url}")
        for filename in files_to_download:
            url = base_url + filename
            dest = mooccubex_dir / filename
            
            if dest.exists() and dest.stat().st_size > 1000:
                print(f"  [SKIP] {filename} already exists")
                continue
            
            print(f"  Downloading {filename}...")
            if download_file(url, dest, filename):
                if dest.exists() and dest.stat().st_size > 1000:
                    print(f"    [OK] Downloaded ({dest.stat().st_size / 1024:.1f} KB)")
                    downloaded += 1
                    break  # Found working URL, continue with other files
    
    # Try cloning repository if direct downloads fail
    if downloaded == 0:
        print("\nTrying to clone repository...")
        repos = [
            "https://github.com/THU-KEG/MOOC-Cube.git",
            "https://github.com/THU-KEG/MOOC-CubeX.git",
        ]
        
        for repo_url in repos:
            print(f"\nTrying: {repo_url}")
            temp_dir = Path('temp_mooccubex')
            
            if temp_dir.exists():
                try:
                    shutil.rmtree(temp_dir)
                except:
                    pass
            
            try:
                result = subprocess.run(
                    ['git', 'clone', '--depth', '1', repo_url, str(temp_dir)],
                    capture_output=True,
                    text=True,
                    timeout=300
                )
                
                if result.returncode == 0 and temp_dir.exists():
                    # Find JSON files
                    json_files = list(temp_dir.rglob('*.json'))
                    for json_file in json_files:
                        if json_file.stat().st_size < 100000000:  # < 100MB
                            dest = mooccubex_dir / json_file.name
                            if not dest.exists():
                                shutil.copy2(json_file, dest)
                                print(f"  [OK] Copied {json_file.name}")
                                downloaded += 1
                    
                    # Cleanup
                    try:
                        shutil.rmtree(temp_dir)
                    except:
                        pass
                    
                    if downloaded > 0:
                        break
            except Exception as e:
                print(f"  Error: {e}")
                continue
    
    if downloaded > 0:
        print(f"\n[OK] Downloaded {downloaded} MOOCCubeX files!")
        return True
    else:
        print("\n[NOTE] MOOCCubeX download failed.")
        print("  The repository may require different access or the files are in a different location.")
        print("  Current files in data/moocsxcube/:")
        existing = list(mooccubex_dir.glob('*.json'))
        for f in existing:
            print(f"    - {f.name} ({f.stat().st_size / 1024:.1f} KB)")
        return False

def verify_mooccubex():
    """Verify MOOCCubeX download"""
    print("\n" + "="*60)
    print("MOOCCUBEX VERIFICATION")
    print("="*60)
    
    mooccubex_dir = Path('data/moocsxcube')
    json_files = list(mooccubex_dir.glob('*.json'))
    
    if json_files:
        print(f"\n[OK] Found {len(json_files)} JSON files:")
        total_size = 0
        for f in json_files:
            size_kb = f.stat().st_size / 1024
            total_size += f.stat().st_size
            print(f"  {f.name}: {size_kb:.1f} KB")
            
            # Try to load and show structure
            try:
                with open(f, 'r') as file:
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
    else:
        print("\n[ERROR] No MOOCCubeX files found")

def main():
    print("="*60)
    print("DOWNLOADING MOOCCUBEX DATASET")
    print("="*60)
    
    download_mooccubex_from_github()
    verify_mooccubex()
    
    print("\n" + "="*60)
    print("DOWNLOAD COMPLETE!")
    print("="*60)

if __name__ == "__main__":
    main()















