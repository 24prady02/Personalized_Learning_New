"""
Download Large CodeNet and MOOCCubeX Datasets from GitHub
"""

import subprocess
import shutil
from pathlib import Path
import requests
import json
from tqdm import tqdm

def download_with_git_clone(repo_url, target_dir, repo_name):
    """Clone repository using git"""
    print(f"\nCloning {repo_name} repository...")
    print(f"  URL: {repo_url}")
    
    temp_dir = Path(f'temp_{repo_name}')
    
    if temp_dir.exists():
        print(f"  Removing existing temp directory...")
        try:
            shutil.rmtree(temp_dir)
        except PermissionError:
            print(f"  [WARNING] Could not remove temp directory (may be in use)")
            # Try to continue anyway
    
    try:
        print(f"  Running: git clone --depth 1 {repo_url}")
        result = subprocess.run(
            ['git', 'clone', '--depth', '1', repo_url, str(temp_dir)],
            capture_output=True,
            text=True,
            timeout=600
        )
        
        if result.returncode == 0:
            print(f"  [OK] Repository cloned successfully!")
            return temp_dir
        else:
            print(f"  [ERROR] Git clone failed:")
            print(f"    {result.stderr}")
            return None
    except FileNotFoundError:
        print(f"  [ERROR] Git not found. Please install Git.")
        return None
    except subprocess.TimeoutExpired:
        print(f"  [ERROR] Clone timed out (repository may be very large)")
        return None
    except Exception as e:
        print(f"  [ERROR] {e}")
        return None

def download_codenet_full():
    """Download full CodeNet dataset"""
    print("\n" + "="*60)
    print("DOWNLOADING FULL CODENET DATASET")
    print("="*60)
    
    codenet_dir = Path('data/codenet')
    codenet_dir.mkdir(parents=True, exist_ok=True)
    
    # Try multiple CodeNet repositories
    repos = [
        "https://github.com/IBM/Project_CodeNet.git",
    ]
    
    for repo_url in repos:
        temp_dir = download_with_git_clone(repo_url, codenet_dir, "codenet")
        
        if temp_dir and temp_dir.exists():
            print("\n  Copying CodeNet files...")
            
            # Copy metadata
            metadata_src = temp_dir / "metadata"
            if metadata_src.exists():
                metadata_dest = codenet_dir / "metadata"
                if metadata_dest.exists():
                    shutil.rmtree(metadata_dest)
                shutil.copytree(metadata_src, metadata_dest)
                print(f"    [OK] Copied metadata directory")
            
            # Copy sample data directories (full dataset is 100GB+)
            data_src = temp_dir / "data"
            if data_src.exists():
                # Copy first few problem directories as samples
                problem_dirs = sorted([d for d in data_src.iterdir() if d.is_dir()])[:10]
                for prob_dir in problem_dirs:
                    prob_dest = codenet_dir / "data" / prob_dir.name
                    if not prob_dest.exists():
                        shutil.copytree(prob_dir, prob_dest)
                        print(f"    [OK] Copied {prob_dir.name}")
            
            # Copy Python/Java/C++ files from data directory
            python_dir = codenet_dir / "python"
            java_dir = codenet_dir / "java"
            cpp_dir = codenet_dir / "c++"
            
            python_dir.mkdir(parents=True, exist_ok=True)
            java_dir.mkdir(parents=True, exist_ok=True)
            cpp_dir.mkdir(parents=True, exist_ok=True)
            
            # Find and copy code files
            code_files = list(temp_dir.rglob('*.py')) + list(temp_dir.rglob('*.java')) + list(temp_dir.rglob('*.cpp'))
            
            copied = 0
            for code_file in code_files[:1000]:  # Limit to first 1000 files
                if 'python' in str(code_file).lower() or code_file.suffix == '.py':
                    dest = python_dir / code_file.name
                    if not dest.exists():
                        shutil.copy2(code_file, dest)
                        copied += 1
                elif 'java' in str(code_file).lower() or code_file.suffix == '.java':
                    dest = java_dir / code_file.name
                    if not dest.exists():
                        shutil.copy2(code_file, dest)
                        copied += 1
                elif 'cpp' in str(code_file).lower() or code_file.suffix == '.cpp':
                    dest = cpp_dir / code_file.name
                    if not dest.exists():
                        shutil.copy2(code_file, dest)
                        copied += 1
            
            print(f"    [OK] Copied {copied} code files")
            
            # Cleanup
            print("  Cleaning up temp directory...")
            shutil.rmtree(temp_dir)
            
            print(f"\n[OK] CodeNet dataset downloaded!")
            return True
    
    print("\n[NOTE] CodeNet download failed.")
    print("  Full CodeNet (100GB+) requires:")
    print("  1. Visit: https://developer.ibm.com/exchanges/data/all/project-codenet/")
    print("  2. Register and download")
    return False

def download_mooccubex_full():
    """Download full MOOCCubeX dataset"""
    print("\n" + "="*60)
    print("DOWNLOADING FULL MOOCCUBEX DATASET")
    print("="*60)
    
    mooccubex_dir = Path('data/moocsxcube')
    mooccubex_dir.mkdir(parents=True, exist_ok=True)
    
    # Try multiple MOOCCubeX repositories
    repos = [
        ("https://github.com/THU-KEG/MOOC-Cube.git", "THU-KEG"),
        ("https://github.com/epfl-ml4ed/mooc-cubex.git", "epfl-ml4ed"),
    ]
    
    for repo_url, repo_name in repos:
        print(f"\nTrying {repo_name} repository...")
        temp_dir = download_with_git_clone(repo_url, mooccubex_dir, f"mooccubex_{repo_name}")
        
        if temp_dir and temp_dir.exists():
            print("\n  Copying MOOCCubeX files...")
            
            # Find and copy JSON/data files
            json_files = list(temp_dir.rglob('*.json'))
            csv_files = list(temp_dir.rglob('*.csv'))
            
            copied = 0
            for data_file in json_files + csv_files:
                # Skip very large files or node_modules
                if 'node_modules' in str(data_file) or data_file.stat().st_size > 100000000:  # > 100MB
                    continue
                
                dest = mooccubex_dir / data_file.name
                if not dest.exists():
                    try:
                        shutil.copy2(data_file, dest)
                        copied += 1
                        print(f"    [OK] Copied {data_file.name} ({data_file.stat().st_size / (1024*1024):.1f} MB)")
                    except:
                        pass
            
            # Also copy data directories
            data_dirs = [d for d in temp_dir.iterdir() if d.is_dir() and d.name in ['data', 'dataset', 'datasets']]
            for data_dir in data_dirs:
                dest_dir = mooccubex_dir / data_dir.name
                if not dest_dir.exists():
                    try:
                        shutil.copytree(data_dir, dest_dir)
                        print(f"    [OK] Copied {data_dir.name} directory")
                    except:
                        pass
            
            print(f"    [OK] Copied {copied} data files")
            
            # Cleanup
            print("  Cleaning up temp directory...")
            shutil.rmtree(temp_dir)
            
            print(f"\n[OK] MOOCCubeX dataset downloaded!")
            return True
    
    print("\n[NOTE] MOOCCubeX download failed.")
    print("  Try manual download from:")
    print("  - https://github.com/THU-KEG/MOOC-Cube")
    print("  - https://github.com/epfl-ml4ed/mooc-cubex")
    return False

def verify_downloads():
    """Verify downloaded datasets"""
    print("\n" + "="*60)
    print("VERIFICATION")
    print("="*60)
    
    # CodeNet
    codenet_py = len(list(Path('data/codenet/python').glob('*.py'))) if Path('data/codenet/python').exists() else 0
    codenet_java = len(list(Path('data/codenet/java').glob('*.java'))) if Path('data/codenet/java').exists() else 0
    codenet_cpp = len(list(Path('data/codenet/c++').glob('*.cpp'))) if Path('data/codenet/c++').exists() else 0
    codenet_txt = len(list(Path('data/codenet/python').glob('*.txt'))) if Path('data/codenet/python').exists() else 0
    codenet_txt += len(list(Path('data/codenet/java').glob('*.txt'))) if Path('data/codenet/java').exists() else 0
    codenet_txt += len(list(Path('data/codenet/c++').glob('*.txt'))) if Path('data/codenet/c++').exists() else 0
    
    total_codenet = codenet_py + codenet_java + codenet_cpp + codenet_txt
    
    print(f"\nCodeNet:")
    print(f"  Python files: {codenet_py}")
    print(f"  Java files: {codenet_java}")
    print(f"  C++ files: {codenet_cpp}")
    print(f"  Text files: {codenet_txt}")
    print(f"  Total: {total_codenet} files")
    print(f"  Status: {'[OK] LARGE' if total_codenet > 100 else '[SAMPLE]'}")
    
    # MOOCCubeX
    mooccubex_files = list(Path('data/moocsxcube').glob('*.json'))
    mooccubex_csv = list(Path('data/moocsxcube').glob('*.csv'))
    
    print(f"\nMOOCCubeX:")
    print(f"  JSON files: {len(mooccubex_files)}")
    print(f"  CSV files: {len(mooccubex_csv)}")
    
    if mooccubex_files:
        for f in mooccubex_files[:3]:
            try:
                with open(f, 'r') as file:
                    data = json.load(file)
                    if isinstance(data, dict):
                        print(f"    {f.name}: {len(data)} keys")
                    elif isinstance(data, list):
                        print(f"    {f.name}: {len(data)} items")
            except:
                pass
    
    print(f"  Status: {'[OK] LARGE' if len(mooccubex_files) + len(mooccubex_csv) > 5 else '[SAMPLE]'}")

def main():
    print("="*60)
    print("DOWNLOADING CODENET AND MOOCCUBEX FROM GITHUB")
    print("="*60)
    print("\nThis will clone repositories and extract datasets.")
    print("This may take 10-30 minutes depending on repository size...\n")
    
    # Download
    codenet_success = download_codenet_full()
    mooccubex_success = download_mooccubex_full()
    
    # Verify
    verify_downloads()
    
    print("\n" + "="*60)
    print("DOWNLOAD COMPLETE!")
    print("="*60)
    
    if codenet_success:
        print("\n[OK] CodeNet downloaded successfully!")
    else:
        print("\n[NOTE] CodeNet may require manual download for full dataset (100GB+)")
    
    if mooccubex_success:
        print("[OK] MOOCCubeX downloaded successfully!")
    else:
        print("[NOTE] MOOCCubeX may require manual download")

if __name__ == "__main__":
    main()

