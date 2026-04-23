"""
Download full CSE-KG 2.0 dataset from ZIP file and set it up for use
"""

import requests
from pathlib import Path
import zipfile
import json
from collections import defaultdict
import networkx as nx
import pickle
from rdflib import Graph, Namespace
from rdflib.namespace import RDF, RDFS
import time

class CSEKGZipDownloader:
    """Download and process full CSE-KG 2.0 dataset from ZIP"""
    
    def __init__(self):
        self.download_url = "http://w3id.org/cskg/downloads/cskg.zip"
        self.output_dir = Path("data/cse_kg_full")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.zip_path = self.output_dir / "cskg.zip"
        self.extract_dir = self.output_dir / "extracted"
        
        self.concepts = {}
        self.relations = []
        self.graph = nx.DiGraph()
        self.concept_keywords = defaultdict(set)
    
    def download_zip(self):
        """Download the full CSE-KG 2.0 dataset ZIP"""
        print("="*80)
        print("DOWNLOADING FULL CSE-KG 2.0 DATASET")
        print("="*80)
        print(f"URL: {self.download_url}")
        print(f"Destination: {self.zip_path}")
        
        if self.zip_path.exists():
            file_size = self.zip_path.stat().st_size / (1024*1024)
            print(f"\n[INFO] ZIP file already exists: {self.zip_path}")
            print(f"  Size: {file_size:.1f} MB")
            
            # Check if download is complete (expected ~3129 MB)
            if file_size > 3100:  # Close to expected size
                print("  [INFO] File appears to be complete (>3100 MB)")
                return True
            else:
                print("  [INFO] File seems incomplete, will resume/redownload")
        
        try:
            print("\nDownloading... (this may take a while, dataset is large)")
            response = requests.get(self.download_url, stream=True, timeout=60)
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0
            chunk_size = 8192
            
            with open(self.zip_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=chunk_size):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        if total_size > 0:
                            percent = (downloaded / total_size) * 100
                            mb_downloaded = downloaded / (1024*1024)
                            mb_total = total_size / (1024*1024)
                            print(f"\r  Progress: {percent:.1f}% ({mb_downloaded:.1f}/{mb_total:.1f} MB)", end='', flush=True)
            
            print(f"\n\n[SUCCESS] Downloaded to {self.zip_path}")
            print(f"  Size: {self.zip_path.stat().st_size / (1024*1024):.1f} MB")
            return True
            
        except requests.exceptions.RequestException as e:
            print(f"\n[ERROR] Download failed: {e}")
            print("\nPossible reasons:")
            print("  1. Network connectivity issues")
            print("  2. URL might require authentication")
            print("  3. Server might be temporarily unavailable")
            print("  4. URL might have changed")
            return False
        except Exception as e:
            print(f"\n[ERROR] Unexpected error: {e}")
            return False
    
    def extract_zip(self):
        """Extract the ZIP file"""
        if not self.zip_path.exists():
            print("[ERROR] ZIP file not found. Download it first.")
            return False
        
        print(f"\n{'='*80}")
        print("EXTRACTING CSE-KG 2.0 DATASET")
        print("="*80)
        
        try:
            self.extract_dir.mkdir(exist_ok=True)
            
            print(f"Extracting to: {self.extract_dir}")
            with zipfile.ZipFile(self.zip_path, 'r') as zip_ref:
                file_list = zip_ref.namelist()
                print(f"  Found {len(file_list)} files in ZIP")
                
                # Extract all files
                zip_ref.extractall(self.extract_dir)
            
            print(f"[SUCCESS] Extracted to {self.extract_dir}")
            
            # List extracted files
            ttl_files = list(self.extract_dir.rglob("*.ttl"))
            print(f"  Found {len(ttl_files)} Turtle (.ttl) files")
            
            if ttl_files:
                print("\n  Sample files:")
                for f in ttl_files[:5]:
                    size_mb = f.stat().st_size / (1024*1024)
                    print(f"    - {f.name} ({size_mb:.2f} MB)")
            
            return True
            
        except zipfile.BadZipFile:
            print("[ERROR] ZIP file is corrupted or invalid")
            return False
        except Exception as e:
            print(f"[ERROR] Extraction failed: {e}")
            return False
    
    def load_from_turtle(self, limit_files=None):
        """Load CSE-KG data from Turtle files using rdflib"""
        print(f"\n{'='*80}")
        print("LOADING CSE-KG 2.0 FROM TURTLE FILES")
        print("="*80)
        
        ttl_files = list(self.extract_dir.rglob("*.ttl"))
        if not ttl_files:
            print("[ERROR] No Turtle files found in extracted directory")
            return False
        
        if limit_files:
            ttl_files = ttl_files[:limit_files]
            print(f"  Processing first {len(ttl_files)} files (for testing)")
        else:
            print(f"  Processing {len(ttl_files)} files")
        
        # Initialize RDF graph
        rdf_graph = Graph()
        
        # Load all Turtle files
        print("\nLoading Turtle files...")
        for i, ttl_file in enumerate(ttl_files, 1):
            try:
                print(f"  [{i}/{len(ttl_files)}] Loading {ttl_file.name}...", end='', flush=True)
                rdf_graph.parse(str(ttl_file), format='turtle')
                print(" [OK]")
            except Exception as e:
                print(f" [ERROR: {e}]")
                continue
        
        print(f"\n  Loaded {len(rdf_graph)} triples from RDF graph")
        
        # Extract concepts and relations
        print("\nExtracting concepts and relations...")
        self._extract_from_rdf_graph(rdf_graph)
        
        return True
    
    def _extract_from_rdf_graph(self, rdf_graph):
        """Extract concepts and relations from RDF graph"""
        cskg_ns = Namespace("https://w3id.org/cskg/resource/")
        cskg_ont = Namespace("https://w3id.org/cskg/ontology#")
        
        # Extract all subjects that are concepts/methods/tasks
        concepts_found = set()
        
        # Get all entities (subjects)
        for subject, predicate, obj in rdf_graph:
            if isinstance(subject, Namespace) or str(subject).startswith("https://w3id.org/cskg/"):
                concepts_found.add(subject)
        
        print(f"  Found {len(concepts_found)} entities")
        
        # Extract concept information
        for entity in list(concepts_found)[:1000]:  # Limit for performance
            entity_str = str(entity)
            entity_id = entity_str.replace("https://w3id.org/cskg/resource/", "").replace("cskg:", "")
            
            # Get labels
            labels = list(rdf_graph.objects(entity, RDFS.label))
            label = str(labels[0]) if labels else entity_id
            
            # Get descriptions
            comments = list(rdf_graph.objects(entity, RDFS.comment))
            description = str(comments[0]) if comments else ""
            
            # Get type
            types = list(rdf_graph.objects(entity, RDF.type))
            entity_type = str(types[0]).split('/')[-1] if types else "Concept"
            
            self.concepts[entity_id] = {
                'id': entity_id,
                'uri': entity_str,
                'label': label,
                'description': description,
                'type': entity_type
            }
            
            # Add to graph
            self.graph.add_node(entity_id, **self.concepts[entity_id])
            
            # Build keyword index
            if label:
                keywords = self._extract_keywords(label)
                for keyword in keywords:
                    self.concept_keywords[keyword].add(entity_id)
        
        # Extract relations
        print("  Extracting relationships...")
        relation_count = 0
        for subject, predicate, obj in rdf_graph:
            if (isinstance(subject, Namespace) or str(subject).startswith("https://w3id.org/cskg/")) and \
               (isinstance(obj, Namespace) or str(obj).startswith("https://w3id.org/cskg/")):
                
                source_id = str(subject).replace("https://w3id.org/cskg/resource/", "").replace("cskg:", "")
                target_id = str(obj).replace("https://w3id.org/cskg/resource/", "").replace("cskg:", "")
                relation_type = str(predicate).split('/')[-1].split('#')[-1]
                
                if source_id in self.concepts and target_id in self.concepts:
                    self.relations.append({
                        'source': source_id,
                        'target': target_id,
                        'relation': relation_type
                    })
                    self.graph.add_edge(source_id, target_id, relation=relation_type)
                    relation_count += 1
                    
                    if relation_count >= 5000:  # Limit for performance
                        break
        
        print(f"  Extracted {len(self.concepts)} concepts and {len(self.relations)} relations")
    
    def _extract_keywords(self, text: str):
        """Extract keywords from text"""
        import re
        words = re.sub(r'[^\w\s]', ' ', text.lower()).split()
        keywords = {w for w in words if len(w) > 2 and w not in ['the', 'and', 'for', 'are', 'with']}
        return keywords
    
    def save_processed_data(self):
        """Save processed data for easy use"""
        print(f"\n{'='*80}")
        print("SAVING PROCESSED CSE-KG 2.0 DATA")
        print("="*80)
        
        # Save concepts
        concepts_file = self.output_dir / "concepts.json"
        with open(concepts_file, 'w', encoding='utf-8') as f:
            json.dump(self.concepts, f, indent=2, ensure_ascii=False)
        print(f"  Saved {len(self.concepts)} concepts to {concepts_file}")
        
        # Save relations
        relations_file = self.output_dir / "relations.json"
        with open(relations_file, 'w', encoding='utf-8') as f:
            json.dump(self.relations, f, indent=2, ensure_ascii=False)
        print(f"  Saved {len(self.relations)} relations to {relations_file}")
        
        # Save graph
        graph_file = self.output_dir / "graph.pkl"
        with open(graph_file, 'wb') as f:
            pickle.dump(self.graph, f)
        print(f"  Saved graph ({len(self.graph.nodes())} nodes, {len(self.graph.edges())} edges) to {graph_file}")
        
        # Save keyword index
        keyword_index = {
            keyword: list(concept_ids) 
            for keyword, concept_ids in self.concept_keywords.items()
        }
        keyword_file = self.output_dir / "keyword_index.json"
        with open(keyword_file, 'w', encoding='utf-8') as f:
            json.dump(keyword_index, f, indent=2, ensure_ascii=False)
        print(f"  Saved {len(keyword_index)} keyword mappings to {keyword_file}")
        
        # Save summary
        summary = {
            'source': 'CSE-KG 2.0 Full Dataset (ZIP)',
            'download_url': self.download_url,
            'download_date': time.strftime('%Y-%m-%d %H:%M:%S'),
            'num_concepts': len(self.concepts),
            'num_relations': len(self.relations),
            'num_nodes': len(self.graph.nodes()),
            'num_edges': len(self.graph.edges()),
            'num_keywords': len(keyword_index),
            'location': str(self.output_dir.absolute())
        }
        summary_file = self.output_dir / "summary.json"
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        print(f"  Saved summary to {summary_file}")
        
        print(f"\n{'='*80}")
        print("CSE-KG 2.0 FULL DATASET READY!")
        print("="*80)
        print(f"Location: {self.output_dir.absolute()}")
        print(f"Concepts: {len(self.concepts)}")
        print(f"Relations: {len(self.relations)}")
        print(f"Graph: {len(self.graph.nodes())} nodes, {len(self.graph.edges())} edges")
    
    def download_and_process(self, limit_files=None):
        """Main method: download, extract, and process"""
        # Download
        if not self.download_zip():
            return False
        
        # Extract
        if not self.extract_zip():
            return False
        
        # Load from Turtle files
        if not self.load_from_turtle(limit_files=limit_files):
            return False
        
        # Save processed data
        self.save_processed_data()
        
        return True


if __name__ == "__main__":
    downloader = CSEKGZipDownloader()
    
    # For testing, limit to first 5 files. Remove limit_files for full dataset
    print("\n[INFO] Starting download and processing...")
    print("[INFO] For full dataset, this may take a while.")
    print("[INFO] For testing, limiting to first 5 Turtle files.\n")
    
    downloader.download_and_process(limit_files=5)  # Remove this parameter for full dataset

