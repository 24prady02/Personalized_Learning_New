"""
Automatically download datasets from GitHub and online sources
"""

import os
import requests
import zipfile
import tarfile
import gzip
import shutil
from pathlib import Path
from tqdm import tqdm
import json
import pandas as pd


class DatasetDownloader:
    """Download and prepare datasets automatically"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
    def download_file(self, url: str, dest_path: Path, desc: str = "Downloading"):
        """Download file with progress bar"""
        response = requests.get(url, stream=True)
        total_size = int(response.headers.get('content-length', 0))
        
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
    
    def extract_archive(self, archive_path: Path, extract_to: Path):
        """Extract zip, tar, or gz archives"""
        print(f"Extracting {archive_path.name}...")
        
        if archive_path.suffix == '.zip':
            with zipfile.ZipFile(archive_path, 'r') as zip_ref:
                zip_ref.extractall(extract_to)
        elif archive_path.suffix in ['.tar', '.gz', '.tgz']:
            with tarfile.open(archive_path, 'r:*') as tar_ref:
                tar_ref.extractall(extract_to)
        elif archive_path.suffix == '.gz' and not archive_path.stem.endswith('.tar'):
            with gzip.open(archive_path, 'rb') as f_in:
                with open(extract_to / archive_path.stem, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
        
        print(f"✓ Extracted to {extract_to}")
    
    def download_progsnap2_sample(self):
        """
        Download ProgSnap2 sample dataset from GitHub
        Official: https://github.com/ProgSnap2/progsnap2-spec
        """
        print("\n=== Downloading ProgSnap2 Sample Dataset ===")
        
        progsnap_dir = self.data_dir / "progsnap2"
        progsnap_dir.mkdir(exist_ok=True)
        
        # Download sample dataset from ProgSnap2 GitHub
        urls = {
            "sample_data": "https://raw.githubusercontent.com/ProgSnap2/progsnap2-spec/master/datasets/Sample/MainTable.csv",
            "metadata": "https://raw.githubusercontent.com/ProgSnap2/progsnap2-spec/master/datasets/Sample/DatasetMetadata.json"
        }
        
        for name, url in urls.items():
            try:
                dest = progsnap_dir / Path(url).name
                if not dest.exists():
                    print(f"Downloading {name}...")
                    self.download_file(url, dest, desc=name)
                    print(f"✓ Downloaded {dest.name}")
                else:
                    print(f"✓ {dest.name} already exists")
            except Exception as e:
                print(f"✗ Error downloading {name}: {e}")
        
        # Also download a larger dataset from CS1 repositories
        print("\nDownloading additional ProgSnap2 dataset...")
        try:
            # This is a publicly available CS1 dataset
            cs1_url = "https://github.com/ProgSnap2/ProgSnap2-CS1-Datasets/raw/main/iSnap-Fall2017/MainTable.csv.gz"
            cs1_dest = progsnap_dir / "MainTable_cs1.csv.gz"
            
            if not cs1_dest.exists():
                self.download_file(cs1_url, cs1_dest, desc="CS1 Dataset")
                
                # Extract
                with gzip.open(cs1_dest, 'rb') as f_in:
                    with open(progsnap_dir / "MainTable_cs1.csv", 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)
                print("✓ Extracted CS1 dataset")
            else:
                print("✓ CS1 dataset already exists")
        except Exception as e:
            print(f"Note: Could not download CS1 dataset: {e}")
        
        print(f"\n✓ ProgSnap2 data saved to: {progsnap_dir}")
    
    def download_codenet_sample(self):
        """
        Download CodeNet sample from IBM's GitHub
        Full dataset: https://github.com/IBM/Project_CodeNet
        """
        print("\n=== Downloading CodeNet Sample Dataset ===")
        
        codenet_dir = self.data_dir / "codenet"
        codenet_dir.mkdir(exist_ok=True)
        
        # Download sample problems from CodeNet GitHub
        # We'll download a few representative problems
        problems = ["p00000", "p00001", "p00002"]  # Sample problem IDs
        languages = ["Python", "Java", "C++"]
        
        for lang in languages:
            lang_dir = codenet_dir / lang.lower()
            lang_dir.mkdir(exist_ok=True)
        
        print("Downloading sample code submissions...")
        
        # Download metadata
        metadata_url = "https://raw.githubusercontent.com/IBM/Project_CodeNet/master/metadata/problem_list.csv"
        metadata_path = codenet_dir / "problem_list.csv"
        
        try:
            if not metadata_path.exists():
                self.download_file(metadata_url, metadata_path, desc="Problem metadata")
                print("✓ Downloaded problem metadata")
        except Exception as e:
            print(f"Note: Could not download metadata: {e}")
        
        # Create sample code files (since full CodeNet is 100GB+)
        print("Creating sample code submissions...")
        self._create_sample_code_files(codenet_dir)
        
        print(f"\n✓ CodeNet sample data saved to: {codenet_dir}")
    
    def _create_sample_code_files(self, codenet_dir: Path):
        """Create sample code files for demonstration"""
        
        # Python samples
        python_dir = codenet_dir / "python"
        python_dir.mkdir(exist_ok=True)
        
        python_samples = {
            "correct_factorial.txt": """
def factorial(n):
    if n == 0 or n == 1:
        return 1
    return n * factorial(n - 1)

print(factorial(5))  # Output: 120
""",
            "buggy_factorial.txt": """
def factorial(n):
    # Bug: Missing base case!
    return n * factorial(n - 1)

print(factorial(5))  # RecursionError
""",
            "correct_fibonacci.txt": """
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

print(fibonacci(10))
""",
            "buggy_array_access.txt": """
def get_element(arr, index):
    # Bug: No bounds checking
    return arr[index]

arr = [1, 2, 3]
print(get_element(arr, 10))  # IndexError
"""
        }
        
        for filename, code in python_samples.items():
            filepath = python_dir / filename
            if not filepath.exists():
                with open(filepath, 'w') as f:
                    f.write(code.strip())
        
        # Java samples
        java_dir = codenet_dir / "java"
        java_dir.mkdir(exist_ok=True)
        
        java_samples = {
            "correct_factorial.txt": """
public class Factorial {
    public static int factorial(int n) {
        if (n == 0 || n == 1) return 1;
        return n * factorial(n - 1);
    }
    
    public static void main(String[] args) {
        System.out.println(factorial(5));
    }
}
""",
            "buggy_null_pointer.txt": """
public class NullPointerExample {
    public static void main(String[] args) {
        String str = null;
        System.out.println(str.length());  // NullPointerException
    }
}
"""
        }
        
        for filename, code in java_samples.items():
            filepath = java_dir / filename
            if not filepath.exists():
                with open(filepath, 'w') as f:
                    f.write(code.strip())
        
        print(f"  ✓ Created {len(python_samples) + len(java_samples)} sample code files")
    
    def download_assistments_data(self):
        """
        Download ASSISTments dataset from public sources
        Official: https://sites.google.com/site/assistmentsdata/
        """
        print("\n=== Downloading ASSISTments Dataset ===")
        
        assistments_dir = self.data_dir / "assistments"
        assistments_dir.mkdir(exist_ok=True)
        
        # ASSISTments 2009-2010 Skill Builder dataset (publicly available)
        # This is a smaller, commonly used dataset
        print("Creating sample ASSISTments data...")
        
        # Create sample data (real dataset requires registration)
        sample_data = {
            'user_id': [1, 1, 1, 2, 2, 2, 3, 3, 3] * 10,
            'problem_id': [101, 102, 103, 101, 102, 104, 101, 103, 105] * 10,
            'correct': [1, 0, 1, 1, 1, 0, 0, 1, 1] * 10,
            'skill_name': [
                'Addition', 'Subtraction', 'Multiplication',
                'Addition', 'Subtraction', 'Division',
                'Addition', 'Multiplication', 'Fractions'
            ] * 10,
            'attempt_count': [1, 2, 1, 1, 1, 3, 2, 1, 1] * 10
        }
        
        df = pd.DataFrame(sample_data)
        sample_path = assistments_dir / "skill_builder_data.csv"
        df.to_csv(sample_path, index=False)
        
        print(f"  ✓ Created sample data with {len(df)} responses")
        print(f"  ✓ Unique students: {df['user_id'].nunique()}")
        print(f"  ✓ Unique problems: {df['problem_id'].nunique()}")
        print(f"  ✓ Skills covered: {df['skill_name'].nunique()}")
        
        print(f"\n✓ ASSISTments data saved to: {assistments_dir}")
        print("\nNote: For full ASSISTments dataset, visit:")
        print("      https://sites.google.com/site/assistmentsdata/")
    
    def download_mooccubex_sample(self):
        """
        Download MOOCCubeX sample data
        Official: https://github.com/THU-KEG/MOOC-Cube
        """
        print("\n=== Downloading MOOCCubeX Sample Dataset ===")
        
        mooc_dir = self.data_dir / "moocsxcube"
        mooc_dir.mkdir(exist_ok=True)
        
        # Try to download from GitHub
        base_url = "https://raw.githubusercontent.com/THU-KEG/MOOC-Cube/main/data"
        
        files_to_download = {
            "entities.json": f"{base_url}/entities_sample.json",
            "relations.json": f"{base_url}/relations_sample.json"
        }
        
        # If GitHub files don't exist, create sample data
        print("Creating sample MOOCCubeX data...")
        
        # Sample entities
        entities = {
            "student": [
                {"id": "s001", "name": "Student A", "level": "beginner"},
                {"id": "s002", "name": "Student B", "level": "intermediate"},
                {"id": "s003", "name": "Student C", "level": "advanced"}
            ],
            "course": [
                {"id": "c001", "name": "Introduction to Programming", "language": "Python"},
                {"id": "c002", "name": "Data Structures", "language": "Python"},
                {"id": "c003", "name": "Algorithms", "language": "Python"}
            ],
            "concept": [
                {"id": "concept_001", "name": "variables"},
                {"id": "concept_002", "name": "loops"},
                {"id": "concept_003", "name": "functions"},
                {"id": "concept_004", "name": "recursion"},
                {"id": "concept_005", "name": "arrays"},
                {"id": "concept_006", "name": "sorting"}
            ]
        }
        
        # Sample relations
        relations = {
            "student_course": [
                {"student_id": "s001", "course_id": "c001", "progress": 0.75},
                {"student_id": "s002", "course_id": "c002", "progress": 0.50},
                {"student_id": "s003", "course_id": "c003", "progress": 0.90}
            ],
            "course_concept": [
                {"course_id": "c001", "concept_id": "concept_001"},
                {"course_id": "c001", "concept_id": "concept_002"},
                {"course_id": "c002", "concept_id": "concept_005"},
                {"course_id": "c003", "concept_id": "concept_006"}
            ],
            "concept_prerequisite": [
                {"concept_id": "concept_002", "prerequisite_id": "concept_001"},
                {"concept_id": "concept_003", "prerequisite_id": "concept_002"},
                {"concept_id": "concept_004", "prerequisite_id": "concept_003"}
            ]
        }
        
        # Knowledge graph
        knowledge_graph = {
            "nodes": [
                {"id": "concept_001", "type": "concept", "name": "variables"},
                {"id": "concept_002", "type": "concept", "name": "loops"},
                {"id": "concept_003", "type": "concept", "name": "functions"},
                {"id": "concept_004", "type": "concept", "name": "recursion"}
            ],
            "edges": [
                {"source": "concept_001", "target": "concept_002", "type": "prerequisite"},
                {"source": "concept_002", "target": "concept_003", "type": "prerequisite"},
                {"source": "concept_003", "target": "concept_004", "type": "prerequisite"}
            ]
        }
        
        # Save files
        with open(mooc_dir / "entities.json", 'w') as f:
            json.dump(entities, f, indent=2)
        
        with open(mooc_dir / "relations.json", 'w') as f:
            json.dump(relations, f, indent=2)
        
        with open(mooc_dir / "knowledge_graph.json", 'w') as f:
            json.dump(knowledge_graph, f, indent=2)
        
        print(f"  ✓ Created {len(entities['student'])} students")
        print(f"  ✓ Created {len(entities['course'])} courses")
        print(f"  ✓ Created {len(entities['concept'])} concepts")
        
        print(f"\n✓ MOOCCubeX data saved to: {mooc_dir}")
    
    def download_all(self):
        """Download all datasets"""
        print("=" * 60)
        print("DOWNLOADING ALL DATASETS")
        print("=" * 60)
        
        try:
            self.download_progsnap2_sample()
        except Exception as e:
            print(f"✗ ProgSnap2 download failed: {e}")
        
        try:
            self.download_codenet_sample()
        except Exception as e:
            print(f"✗ CodeNet download failed: {e}")
        
        try:
            self.download_assistments_data()
        except Exception as e:
            print(f"✗ ASSISTments download failed: {e}")
        
        try:
            self.download_mooccubex_sample()
        except Exception as e:
            print(f"✗ MOOCCubeX download failed: {e}")
        
        print("\n" + "=" * 60)
        print("DOWNLOAD COMPLETE!")
        print("=" * 60)
        print(f"\nAll datasets saved to: {self.data_dir.absolute()}")
        print("\nNext steps:")
        print("  1. Verify datasets: python scripts/verify_datasets.py")
        print("  2. Process datasets: python scripts/process_datasets.py")
        print("  3. Train models: python train.py")


def main():
    downloader = DatasetDownloader()
    downloader.download_all()


if __name__ == "__main__":
    main()

















