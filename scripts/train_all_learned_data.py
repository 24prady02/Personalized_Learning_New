"""
Main script to train all learned data from datasets
Runs all learning scripts in sequence
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

import subprocess
import time


def run_script(script_name: str, description: str):
    """Run a learning script"""
    print("\n" + "=" * 60)
    print(f"STEP: {description}")
    print("=" * 60)
    
    script_path = Path(__file__).parent / script_name
    
    if not script_path.exists():
        print(f"⚠ Script not found: {script_path}")
        return False
    
    try:
        result = subprocess.run(
            [sys.executable, str(script_path)],
            capture_output=False,
            text=True
        )
        
        if result.returncode == 0:
            print(f"\n✓ {description} completed successfully")
            return True
        else:
            print(f"\n✗ {description} failed with return code {result.returncode}")
            return False
    except Exception as e:
        print(f"\n✗ Error running {description}: {e}")
        return False


def main():
    """Run all learning scripts"""
    print("=" * 60)
    print("TRAINING ALL LEARNED DATA FROM DATASETS")
    print("=" * 60)
    print("\nThis will:")
    print("  1. Extract misconceptions from CodeNet buggy code")
    print("  2. Learn COKE chains from ProgSnap2 action sequences")
    print("  3. Learn misconceptions from ASSISTments wrong answers")
    print("  4. Merge all learned data into unified format")
    print("\nThis replaces hardcoded logic with data-driven learning!")
    
    input("\nPress Enter to continue...")
    
    scripts = [
        ("learn_misconceptions_from_codenet.py", "Extract Misconceptions from CodeNet"),
        ("learn_coke_chains_from_progsnap2.py", "Learn COKE Chains from ProgSnap2"),
        ("learn_misconceptions_from_assistments.py", "Learn Misconceptions from ASSISTments"),
        ("merge_learned_data.py", "Merge All Learned Data")
    ]
    
    results = []
    for script_name, description in scripts:
        success = run_script(script_name, description)
        results.append((description, success))
        time.sleep(1)  # Brief pause between scripts
    
    # Summary
    print("\n" + "=" * 60)
    print("TRAINING SUMMARY")
    print("=" * 60)
    
    for description, success in results:
        status = "✓ SUCCESS" if success else "✗ FAILED"
        print(f"{status}: {description}")
    
    all_success = all(success for _, success in results)
    
    if all_success:
        print("\n" + "=" * 60)
        print("🎉 ALL TRAINING COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        print("\nThe system will now use learned data instead of hardcoded values:")
        print("  - Misconceptions learned from CodeNet and ASSISTments")
        print("  - COKE chains learned from ProgSnap2")
        print("\nNext steps:")
        print("  1. Restart your application to load the new learned data")
        print("  2. The system will automatically use learned data if available")
        print("  3. Hardcoded defaults will only be used as fallback")
    else:
        print("\n" + "=" * 60)
        print("⚠ SOME TRAINING FAILED")
        print("=" * 60)
        print("\nCheck the errors above and fix issues before continuing.")
        print("The system will use hardcoded defaults until training succeeds.")


if __name__ == "__main__":
    main()





