"""
Download CSE-KG 2.0 full dataset and set up local access
Two options:
1. Use correct SPARQL endpoint: http://w3id.org/cskg/sparql
2. Download full dataset: http://w3id.org/cskg/downloads/cskg.zip
"""

import requests
from SPARQLWrapper import SPARQLWrapper, JSON
from pathlib import Path
import zipfile
import json
from typing import Dict, List
import time


class CSEKGDownloader:
    """Download CSE-KG 2.0 using multiple methods"""
    
    def __init__(self):
        self.output_dir = Path("data/cse_kg_local")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Try different endpoints
        self.endpoints = [
            "http://w3id.org/cskg/sparql",  # Official endpoint from web search
            "http://cse.ckcest.cn/cskg/sparql",  # Original endpoint
        ]
        
        self.download_url = "http://w3id.org/cskg/downloads/cskg.zip"
    
    def test_endpoint(self, endpoint: str) -> bool:
        """Test if SPARQL endpoint is accessible"""
        print(f"\nTesting endpoint: {endpoint}")
        try:
            sparql = SPARQLWrapper(endpoint)
            sparql.setReturnFormat(JSON)
            query = """
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            SELECT (COUNT(*) as ?count) WHERE {
                ?s ?p ?o .
            }
            LIMIT 1
            """
            sparql.setQuery(query)
            results = sparql.query().convert()
            print(f"  [OK] Endpoint accessible!")
            return True
        except Exception as e:
            print(f"  [ERROR] {e}")
            return False
    
    def find_working_endpoint(self) -> str:
        """Find a working SPARQL endpoint"""
        print("="*80)
        print("FINDING WORKING CSE-KG 2.0 SPARQL ENDPOINT")
        print("="*80)
        
        for endpoint in self.endpoints:
            if self.test_endpoint(endpoint):
                print(f"\n[SUCCESS] Using endpoint: {endpoint}")
                return endpoint
        
        print("\n[WARNING] No SPARQL endpoints accessible")
        return None
    
    def download_full_dataset(self) -> bool:
        """Download full CSE-KG 2.0 dataset"""
        print("\n" + "="*80)
        print("DOWNLOADING FULL CSE-KG 2.0 DATASET")
        print("="*80)
        print(f"URL: {self.download_url}")
        
        zip_path = self.output_dir / "cskg.zip"
        
        try:
            print("Downloading... (this may take a while, dataset is large)")
            response = requests.get(self.download_url, stream=True, timeout=30)
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0
            
            with open(zip_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        if total_size > 0:
                            percent = (downloaded / total_size) * 100
                            print(f"\r  Progress: {percent:.1f}% ({downloaded}/{total_size} bytes)", end='')
            
            print(f"\n[OK] Downloaded to {zip_path}")
            
            # Extract
            print("Extracting...")
            extract_dir = self.output_dir / "extracted"
            extract_dir.mkdir(exist_ok=True)
            
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_dir)
            
            print(f"[OK] Extracted to {extract_dir}")
            
            # Find Turtle files
            ttl_files = list(extract_dir.rglob("*.ttl"))
            print(f"[OK] Found {len(ttl_files)} Turtle files")
            
            return True
            
        except requests.exceptions.RequestException as e:
            print(f"\n[ERROR] Download failed: {e}")
            print("This might be due to:")
            print("  1. Network connectivity issues")
            print("  2. URL might require authentication")
            print("  3. Server might be temporarily unavailable")
            return False
        except Exception as e:
            print(f"\n[ERROR] Extraction failed: {e}")
            return False
    
    def update_config_with_working_endpoint(self, endpoint: str):
        """Update config.yaml with working endpoint"""
        import yaml
        
        config_path = Path("config.yaml")
        if not config_path.exists():
            print("[WARNING] config.yaml not found, skipping update")
            return
        
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        config['cse_kg']['sparql_endpoint'] = endpoint
        
        with open(config_path, 'w') as f:
            yaml.dump(config, f, default_flow_style=False, sort_keys=False)
        
        print(f"\n[OK] Updated config.yaml with endpoint: {endpoint}")
    
    def create_access_guide(self, endpoint: str = None, downloaded: bool = False):
        """Create a guide for accessing CSE-KG 2.0"""
        guide_path = self.output_dir / "ACCESS_GUIDE.md"
        
        with open(guide_path, 'w', encoding='utf-8') as f:
            f.write("# CSE-KG 2.0 Access Guide\n\n")
            
            if endpoint:
                f.write(f"## ✅ Working SPARQL Endpoint\n\n")
                f.write(f"Endpoint: `{endpoint}`\n\n")
                f.write("You can use this endpoint directly in your code:\n\n")
                f.write("```python\n")
                f.write("from SPARQLWrapper import SPARQLWrapper, JSON\n\n")
                f.write(f"sparql = SPARQLWrapper('{endpoint}')\n")
                f.write("sparql.setReturnFormat(JSON)\n")
                f.write("```\n\n")
            
            if downloaded:
                f.write("## ✅ Full Dataset Downloaded\n\n")
                f.write("The full CSE-KG 2.0 dataset has been downloaded to:\n")
                f.write(f"`{self.output_dir / 'extracted'}`\n\n")
                f.write("To use it locally, you can:\n\n")
                f.write("1. **Load into a local SPARQL server** (GraphDB, Blazegraph, Virtuoso):\n")
                f.write("   - Import the Turtle (.ttl) files\n")
                f.write("   - Set up a local SPARQL endpoint\n\n")
                f.write("2. **Use rdflib to load directly**:\n")
                f.write("   ```python\n")
                f.write("   from rdflib import Graph\n")
                f.write("   g = Graph()\n")
                f.write("   g.parse('path/to/cskg.ttl', format='turtle')\n")
                f.write("   ```\n\n")
            
            f.write("## Alternative Access Methods\n\n")
            f.write("1. **Official SPARQL Endpoint**: http://w3id.org/cskg/sparql\n")
            f.write("2. **Download Dataset**: http://w3id.org/cskg/downloads/cskg.zip\n")
            f.write("3. **Local Graph**: Use the local graph built from MOOCCubeX\n\n")
        
        print(f"\n[OK] Access guide saved to {guide_path}")


def main():
    """Main function to set up CSE-KG 2.0 access"""
    downloader = CSEKGDownloader()
    
    # Try to find working endpoint
    endpoint = downloader.find_working_endpoint()
    
    if endpoint:
        # Update config
        downloader.update_config_with_working_endpoint(endpoint)
        downloader.create_access_guide(endpoint=endpoint)
        print("\n" + "="*80)
        print("SUCCESS! CSE-KG 2.0 SPARQL endpoint is accessible")
        print("="*80)
        print(f"\nUsing endpoint: {endpoint}")
        print("\nYou can now use CSE-KG 2.0 in your code!")
        return
    
    # If no endpoint works, try downloading
    print("\n" + "="*80)
    print("ATTEMPTING TO DOWNLOAD FULL DATASET")
    print("="*80)
    
    downloaded = downloader.download_full_dataset()
    
    if downloaded:
        downloader.create_access_guide(downloaded=True)
        print("\n" + "="*80)
        print("SUCCESS! CSE-KG 2.0 dataset downloaded")
        print("="*80)
        print("\nYou can now load it locally using rdflib or a SPARQL server.")
    else:
        print("\n" + "="*80)
        print("FALLBACK: Using local graph from MOOCCubeX")
        print("="*80)
        print("\nSince neither SPARQL endpoint nor download worked,")
        print("the system will use the local graph built from MOOCCubeX data.")
        print("Run: python build_local_cse_kg.py")
        downloader.create_access_guide()


if __name__ == "__main__":
    main()















