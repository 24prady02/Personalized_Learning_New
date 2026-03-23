"""
Process downloaded datasets and prepare for training
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

import pandas as pd
from src.data.processors import (
    CodeNetProcessor, 
    ProgSnap2Processor,
    MOOCCubeXProcessor,
    ASSISTmentsProcessor
)
import yaml


def process_all_datasets():
    """Process all downloaded datasets"""
    
    print("=" * 60)
    print("PROCESSING DATASETS")
    print("=" * 60)
    
    # Load config
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    processed_dir = Path("data/processed")
    processed_dir.mkdir(exist_ok=True)
    
    # Process CodeNet
    print("\n=== Processing CodeNet ===")
    try:
        codenet_processor = CodeNetProcessor("data/codenet", config)
        codenet_df = codenet_processor.process()
        
        if len(codenet_df) > 0:
            output_path = processed_dir / "codenet_processed.csv"
            codenet_df.to_csv(output_path, index=False)
            print(f"✓ Saved {len(codenet_df)} samples to {output_path}")
        else:
            print("⚠ No CodeNet data processed")
    except Exception as e:
        print(f"✗ Error processing CodeNet: {e}")
    
    # Process ProgSnap2
    print("\n=== Processing ProgSnap2 ===")
    try:
        progsnap_processor = ProgSnap2Processor("data/progsnap2", config)
        progsnap_df = progsnap_processor.process()
        
        if len(progsnap_df) > 0:
            output_path = processed_dir / "progsnap2_processed.csv"
            progsnap_df.to_csv(output_path, index=False)
            print(f"✓ Saved {len(progsnap_df)} sessions to {output_path}")
        else:
            print("⚠ No ProgSnap2 data processed")
    except Exception as e:
        print(f"✗ Error processing ProgSnap2: {e}")
    
    # Process ASSISTments
    print("\n=== Processing ASSISTments ===")
    try:
        assistments_processor = ASSISTmentsProcessor("data/assistments", config)
        responses_df, qmatrix_df = assistments_processor.process()
        
        if len(responses_df) > 0:
            responses_path = processed_dir / "assistments_responses.csv"
            qmatrix_path = processed_dir / "assistments_qmatrix.csv"
            
            responses_df.to_csv(responses_path, index=False)
            qmatrix_df.to_csv(qmatrix_path, index=False)
            
            print(f"✓ Saved {len(responses_df)} responses to {responses_path}")
            print(f"✓ Saved Q-matrix with {len(qmatrix_df)} problems to {qmatrix_path}")
        else:
            print("⚠ No ASSISTments data processed")
    except Exception as e:
        print(f"✗ Error processing ASSISTments: {e}")
    
    # Process MOOCCubeX
    print("\n=== Processing MOOCCubeX ===")
    try:
        mooc_processor = MOOCCubeXProcessor("data/moocsxcube", config)
        mooc_df = mooc_processor.process()
        
        if len(mooc_df) > 0:
            output_path = processed_dir / "moocsxcube_processed.csv"
            mooc_df.to_csv(output_path, index=False)
            print(f"✓ Saved {len(mooc_df)} activities to {output_path}")
            
            # Also save knowledge graph
            kg = mooc_processor.build_knowledge_graph()
            import json
            kg_path = processed_dir / "moocsxcube_kg.json"
            with open(kg_path, 'w') as f:
                json.dump(kg, f, indent=2)
            print(f"✓ Saved knowledge graph to {kg_path}")
        else:
            print("⚠ No MOOCCubeX data processed")
    except Exception as e:
        print(f"✗ Error processing MOOCCubeX: {e}")
    
    print("\n" + "=" * 60)
    print("PROCESSING COMPLETE!")
    print("=" * 60)
    print(f"\nProcessed data saved to: {processed_dir.absolute()}")
    print("\nNext step: python train.py")


if __name__ == "__main__":
    process_all_datasets()




















