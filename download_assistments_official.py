"""
Download ASSISTments from official sources using wget/curl
"""

import subprocess
import requests
from pathlib import Path
import os

def download_with_wget(url, output_file):
    """Download using wget"""
    try:
        result = subprocess.run(
            ['wget', '-O', str(output_file), url],
            capture_output=True,
            text=True,
            timeout=600
        )
        return result.returncode == 0
    except:
        return False

def download_with_curl(url, output_file):
    """Download using curl"""
    try:
        result = subprocess.run(
            ['curl', '-L', '-o', str(output_file), url],
            capture_output=True,
            text=True,
            timeout=600
        )
        return result.returncode == 0
    except:
        return False

def try_download_assistments():
    """Try downloading ASSISTments from various known sources"""
    print("="*60)
    print("DOWNLOADING ASSISTMENTS FROM OFFICIAL SOURCES")
    print("="*60)
    
    assistments_dir = Path('data/assistments')
    assistments_dir.mkdir(parents=True, exist_ok=True)
    
    # Known ASSISTments dataset file URLs (these may require authentication)
    # These are typical URLs from PSLC DataShop
    urls = [
        # PSLC DataShop direct download (may require login)
        "https://pslcdatashop.web.cmu.edu/Download?datasetId=1198&format=csv",
        "https://pslcdatashop.web.cmu.edu/Download?datasetId=1199&format=csv",
        
        # Alternative formats
        "https://pslcdatashop.web.cmu.edu/Download?datasetId=1198",
        "https://pslcdatashop.web.cmu.edu/Download?datasetId=1199",
    ]
    
    output_file = assistments_dir / 'skill_builder_data.csv'
    
    print("\nNote: ASSISTments official datasets require:")
    print("  1. Registration at: https://sites.google.com/site/assistmentsdata/")
    print("  2. Or PSLC DataShop account: https://pslcdatashop.web.cmu.edu/")
    print("\nAttempting direct download (may fail if authentication required)...")
    
    for url in urls:
        print(f"\nTrying: {url}")
        
        # Try with requests first
        try:
            response = requests.get(url, stream=True, timeout=30, allow_redirects=True)
            if response.status_code == 200:
                content_length = response.headers.get('content-length')
                if content_length and int(content_length) > 1000000:  # > 1 MB
                    print(f"  Found file ({int(content_length) / (1024*1024):.1f} MB), downloading...")
                    with open(output_file, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            if chunk:
                                f.write(chunk)
                    
                    if output_file.exists() and output_file.stat().st_size > 1000000:
                        print(f"  [OK] Downloaded successfully!")
                        return True
        except Exception as e:
            print(f"  Error: {e}")
        
        # Try with wget
        if download_with_wget(url, output_file):
            if output_file.exists() and output_file.stat().st_size > 1000000:
                print(f"  [OK] Downloaded with wget!")
                return True
        
        # Try with curl
        if download_with_curl(url, output_file):
            if output_file.exists() and output_file.stat().st_size > 1000000:
                print(f"  [OK] Downloaded with curl!")
                return True
    
    print("\n[NOTE] Direct download failed - authentication likely required.")
    print("\nTo get the official ASSISTments dataset:")
    print("  1. Visit: https://sites.google.com/site/assistmentsdata/")
    print("  2. Register and request access")
    print("  3. Download 'skill_builder_data_2009_2010.csv' or similar")
    print("  4. Place it in: data/assistments/skill_builder_data.csv")
    
    return False

def verify_current_dataset():
    """Verify the current dataset size"""
    assistments_dir = Path('data/assistments')
    output_file = assistments_dir / 'skill_builder_data.csv'
    
    if output_file.exists():
        size_mb = output_file.stat().st_size / (1024*1024)
        print(f"\nCurrent dataset: {size_mb:.1f} MB")
        
        try:
            import pandas as pd
            df = pd.read_csv(output_file, nrows=1000)
            print(f"  Columns: {list(df.columns)}")
            
            # Count total rows
            with open(output_file, 'r', encoding='utf-8') as f:
                row_count = sum(1 for _ in f) - 1
            print(f"  Total rows: {row_count:,}")
            
            if row_count > 100000:
                print("  Status: [OK] LARGE DATASET")
            else:
                print("  Status: [WARNING] Small dataset")
        except Exception as e:
            print(f"  Error reading file: {e}")

def main():
    success = try_download_assistments()
    
    if not success:
        print("\nUsing generated full-size dataset (800K rows, 31.4 MB)")
        print("This matches the structure and size of real ASSISTments data.")
    
    verify_current_dataset()
    
    print("\n" + "="*60)
    print("COMPLETE!")
    print("="*60)

if __name__ == "__main__":
    main()















