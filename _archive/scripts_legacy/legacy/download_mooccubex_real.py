"""
Download MOOCCubeX Dataset - Real Data from Official Source
Uses the download script from the repository
"""

import requests
import json
import os
from pathlib import Path
from tqdm import tqdm
import time

def download_file(url, dest_path, desc="Downloading"):
    """Download file with progress"""
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        response = requests.get(url, stream=True, timeout=300)
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

def download_mooccubex_real():
    """Download MOOCCubeX from the official data source"""
    print("\n" + "="*60)
    print("DOWNLOADING MOOCCUBEX REAL DATA")
    print("="*60)
    
    base_url = "https://lfs.aminer.cn/misc/moocdata/data/mooccube2/"
    
    # Files to download based on download_dataset.sh
    files_to_download = [
        # Entities
        "entities/reply.json",
        "entities/video.json",
        "entities/comment.json",
        "entities/course.json",
        "entities/other.json",
        "entities/paper.json",
        "entities/problem.json",
        "entities/school.json",
        "entities/teacher.json",
        "entities/user.json",
        "entities/concept.json",
        # Relations
        "relations/course-school.txt",
        "relations/course-teacher.txt",
        "relations/user-comment.txt",
        "relations/video_id-ccid.txt",
        "relations/comment-reply.txt",
        "relations/concept-other.txt",
        "relations/course-comment.txt",
        "relations/concept-video.txt",
        "relations/exercise-problem.txt",
        "relations/user-reply.txt",
        "relations/concept-comment.txt",
        "relations/concept-paper.txt",
        "relations/concept-problem.txt",
        "relations/concept-reply.json",
        "relations/course-field.json",
        "relations/reply-reply.txt",
        "relations/user-problem.json",
        "relations/user-video.json",
        "relations/user-xiaomu.json",
        # Prerequisites
        "prerequisites/psy.json",
        "prerequisites/cs.json",
        "prerequisites/math.json",
    ]
    
    mooccubex_dir = Path('data/moocsxcube')
    downloaded = 0
    failed = 0
    
    print(f"\nDownloading {len(files_to_download)} files from official source...")
    print("This may take a while depending on file sizes...\n")
    
    for filename in files_to_download:
        url = base_url + filename
        dest = mooccubex_dir / filename
        
        # Skip if already exists and has reasonable size
        if dest.exists() and dest.stat().st_size > 1000:
            print(f"[SKIP] {filename} already exists ({dest.stat().st_size / 1024:.1f} KB)")
            downloaded += 1
            continue
        
        print(f"Downloading {filename}...")
        if download_file(url, dest, filename):
            if dest.exists() and dest.stat().st_size > 100:
                size_mb = dest.stat().st_size / (1024*1024)
                print(f"  [OK] Downloaded ({size_mb:.1f} MB)")
                downloaded += 1
                time.sleep(0.5)  # Be nice to the server
            else:
                print(f"  [ERROR] File too small or empty")
                failed += 1
        else:
            failed += 1
    
    print(f"\n" + "="*60)
    print(f"Download Summary:")
    print(f"  Successfully downloaded: {downloaded}")
    print(f"  Failed: {failed}")
    print("="*60)
    
    return downloaded > 0

def verify_download():
    """Verify downloaded files"""
    print("\n" + "="*60)
    print("VERIFICATION")
    print("="*60)
    
    mooccubex_dir = Path('data/moocsxcube')
    
    # Check entities
    entities_dir = mooccubex_dir / 'entities'
    relations_dir = mooccubex_dir / 'relations'
    prerequisites_dir = mooccubex_dir / 'prerequisites'
    
    total_size = 0
    file_count = 0
    
    for directory in [entities_dir, relations_dir, prerequisites_dir]:
        if directory.exists():
            files = list(directory.glob('*'))
            for f in files:
                if f.is_file():
                    size_mb = f.stat().st_size / (1024*1024)
                    total_size += f.stat().st_size
                    file_count += 1
                    print(f"  {f.relative_to(mooccubex_dir)}: {size_mb:.1f} MB")
    
    print(f"\n  Total files: {file_count}")
    print(f"  Total size: {total_size / (1024*1024):.1f} MB")
    
    if file_count > 0:
        print(f"  Status: [OK] Downloaded")
        return True
    else:
        print(f"  Status: [ERROR] No files found")
        return False

def main():
    print("="*60)
    print("DOWNLOADING MOOCCUBEX REAL DATASET")
    print("="*60)
    print("\nThis will download the actual MOOCCubeX data files")
    print("from the official source: https://lfs.aminer.cn/")
    print("\nNote: Some files may be very large. This may take time.")
    
    success = download_mooccubex_real()
    
    if success:
        verify_download()
        print("\n" + "="*60)
        print("[OK] MOOCCubeX download complete!")
        print("="*60)
    else:
        print("\n[NOTE] Some files failed to download.")
        print("This may be due to:")
        print("  1. Network issues")
        print("  2. Server availability")
        print("  3. File access permissions")
        verify_download()

if __name__ == "__main__":
    main()















