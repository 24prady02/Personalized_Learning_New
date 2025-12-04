"""
Quick start script - Download everything and set up the system
"""

import subprocess
import sys


def run_command(cmd, desc):
    """Run command and show progress"""
    print(f"\n{'='*60}")
    print(f"{desc}")
    print(f"{'='*60}\n")
    
    try:
        result = subprocess.run(cmd, shell=True, check=True, text=True)
        print(f"\n✓ {desc} completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n✗ {desc} failed: {e}")
        return False


def main():
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║  PERSONALIZED LEARNING SYSTEM - QUICK START              ║
    ║  Automated Setup & Dataset Download                      ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    
    steps = [
        ("python scripts/download_models.py", "Step 1/5: Downloading Pre-trained Models"),
        ("python scripts/download_datasets.py", "Step 2/5: Downloading Datasets"),
        ("python scripts/init_knowledge_graph.py", "Step 3/5: Initializing CSE-KG Connection"),
        ("python scripts/verify_datasets.py", "Step 4/5: Verifying Datasets"),
        ("python scripts/process_datasets.py", "Step 5/5: Processing Datasets")
    ]
    
    success = []
    
    for cmd, desc in steps:
        result = run_command(cmd, desc)
        success.append(result)
    
    print(f"\n{'='*60}")
    print("QUICK START SUMMARY")
    print(f"{'='*60}\n")
    
    for i, (cmd, desc) in enumerate(steps, 1):
        status = "✓ PASS" if success[i-1] else "✗ FAIL"
        print(f"  {status}  {desc}")
    
    if all(success):
        print(f"\n{'='*60}")
        print("🎉 SYSTEM READY!")
        print(f"{'='*60}\n")
        print("Next steps:")
        print("  1. Start API server: python api/server.py")
        print("  2. Try examples: python example_usage.py")
        print("  3. Train models: python train.py")
        print("\nFor full documentation, see README.md")
    else:
        print(f"\n{'='*60}")
        print("⚠ SETUP INCOMPLETE")
        print(f"{'='*60}\n")
        print("Some steps failed. Please check errors above.")
        print("You can run individual scripts manually:")
        for cmd, _ in steps:
            print(f"  {cmd}")


if __name__ == "__main__":
    main()

















