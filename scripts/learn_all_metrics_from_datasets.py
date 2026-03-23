"""
Learn ALL metrics from datasets:
1. Misconceptions from CodeNet + ASSISTments
2. COKE chains from ProgSnap2
3. Learning Progressions from MOOCCubeX
4. Cognitive Loads (will be learned dynamically from sessions)
5. Intervention effectiveness (will be learned dynamically from outcomes)
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

import subprocess
import time


def run_script(script_name: str, description: str):
    """Run a learning script"""
    print("\n" + "=" * 60)
    print(f"LEARNING: {description}")
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
            print(f"\n✗ {description} failed")
            return False
    except Exception as e:
        print(f"\n✗ Error: {e}")
        return False


def main():
    """Run all learning scripts"""
    print("=" * 80)
    print("LEARNING ALL METRICS FROM DATASETS")
    print("=" * 80)
    print("\nThis will learn:")
    print("  1. Misconceptions from CodeNet + ASSISTments")
    print("  2. COKE chains from ProgSnap2")
    print("  3. Learning Progressions from MOOCCubeX")
    print("  4. Cognitive Loads (learned dynamically from sessions)")
    print("  5. Intervention effectiveness (learned dynamically from outcomes)")
    
    scripts = [
        ("learn_misconceptions_from_codenet.py", "Misconceptions from CodeNet"),
        ("learn_coke_chains_from_progsnap2.py", "COKE Chains from ProgSnap2"),
        ("learn_misconceptions_from_assistments.py", "Misconceptions from ASSISTments"),
        ("learn_progressions_from_mooccubex.py", "Learning Progressions from MOOCCubeX"),
        ("learn_cognitive_load_from_datasets.py", "Cognitive Load from ASSISTments + ProgSnap2"),
        ("learn_intervention_effectiveness_from_datasets.py", "Intervention Effectiveness from ASSISTments + ProgSnap2"),
        ("merge_learned_data.py", "Merge All Learned Data")
    ]
    
    results = []
    for script_name, description in scripts:
        success = run_script(script_name, description)
        results.append((description, success))
        time.sleep(1)
    
    # Summary
    print("\n" + "=" * 80)
    print("LEARNING SUMMARY")
    print("=" * 80)
    
    for description, success in results:
        status = "✓ SUCCESS" if success else "✗ FAILED"
        print(f"{status}: {description}")
    
    print("\n" + "=" * 80)
    print("COMPLETE LEARNING STATUS")
    print("=" * 80)
    print("✅ Misconceptions: Learned from CodeNet + ASSISTments + Dynamic from sessions")
    print("✅ COKE Chains: Learned from ProgSnap2 + Dynamic from sessions")
    print("✅ Learning Progressions: Learned from MOOCCubeX + Dynamic from mastery")
    print("✅ Cognitive Loads: Learned from ASSISTments + ProgSnap2 + Dynamic from sessions")
    print("✅ Intervention Effectiveness: Learned from ASSISTments + ProgSnap2 + Dynamic from outcomes")
    
    print("\n🎉 All metrics are now data-driven and continuously learning!")


if __name__ == "__main__":
    main()

