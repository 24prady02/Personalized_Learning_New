"""
Merge all learned data from different datasets
Combines misconceptions and COKE chains into unified format
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

import json
from collections import defaultdict
from typing import Dict, List


class LearnedDataMerger:
    """Merge learned data from multiple sources"""
    
    def __init__(self, data_dir: str = "data/pedagogical_kg"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
    
    def load_learned_misconceptions(self) -> List[Dict]:
        """Load all learned misconception files"""
        misconception_files = [
            self.data_dir / "misconceptions_learned.json",
            self.data_dir / "misconceptions_assistments_learned.json"
        ]
        
        all_misconceptions = []
        for file_path in misconception_files:
            if file_path.exists():
                print(f"Loading {file_path.name}...")
                with open(file_path, 'r', encoding='utf-8') as f:
                    misconceptions = json.load(f)
                    all_misconceptions.extend(misconceptions)
                    print(f"  ✓ Loaded {len(misconceptions)} misconceptions")
            else:
                print(f"  ⚠ {file_path.name} not found")
        
        return all_misconceptions
    
    def load_learned_coke_chains(self) -> List[Dict]:
        """Load learned COKE chains"""
        chains_file = self.data_dir / "coke_chains_learned.json"
        
        if chains_file.exists():
            print(f"Loading {chains_file.name}...")
            with open(chains_file, 'r', encoding='utf-8') as f:
                chains = json.load(f)
                print(f"  ✓ Loaded {len(chains)} cognitive chains")
                return chains
        else:
            print(f"  ⚠ {chains_file.name} not found")
            return []
    
    def merge_misconceptions(self, misconceptions: List[Dict]) -> List[Dict]:
        """Merge misconceptions by concept, combining evidence"""
        print("\n" + "=" * 60)
        print("MERGING MISCONCEPTIONS")
        print("=" * 60)
        
        # Group by concept
        concept_misconceptions = defaultdict(list)
        for mc in misconceptions:
            concept = mc.get("concept", "unknown")
            concept_misconceptions[concept].append(mc)
        
        merged = []
        for concept, mc_list in concept_misconceptions.items():
            if len(mc_list) == 1:
                # Single source, use as-is
                merged.append(mc_list[0])
            else:
                # Multiple sources, merge
                merged_mc = self._merge_misconception_list(mc_list)
                merged.append(merged_mc)
                print(f"\n✓ Merged {len(mc_list)} misconceptions for concept: {concept}")
                print(f"  Total evidence: {merged_mc.get('evidence_count', 0)}")
        
        return merged
    
    def _merge_misconception_list(self, mc_list: List[Dict]) -> Dict:
        """Merge multiple misconceptions for the same concept"""
        # Use the first one as base
        merged = mc_list[0].copy()
        
        # Combine evidence
        total_evidence = sum(mc.get("evidence_count", 0) for mc in mc_list)
        merged["evidence_count"] = total_evidence
        
        # Combine sources
        sources = [mc.get("source", "unknown") for mc in mc_list]
        merged["source"] = ", ".join(set(sources))
        
        # Combine indicators
        all_indicators = []
        for mc in mc_list:
            all_indicators.extend(mc.get("common_indicators", []))
        merged["common_indicators"] = list(set(all_indicators))
        
        # Use highest severity
        severity_order = {"high": 3, "medium": 2, "low": 1}
        max_severity = max(mc_list, key=lambda x: severity_order.get(x.get("severity", "low"), 0))
        merged["severity"] = max_severity.get("severity", "medium")
        
        # Average frequency
        frequencies = [mc.get("frequency", 0.0) for mc in mc_list]
        merged["frequency"] = sum(frequencies) / len(frequencies)
        
        # Combine correction strategies
        strategies = [mc.get("correction_strategy", "") for mc in mc_list if mc.get("correction_strategy")]
        if strategies:
            merged["correction_strategy"] = " | ".join(set(strategies))
        
        # Update ID to indicate merged
        merged["id"] = f"mc_merged_{merged.get('concept', 'unknown').lower().replace(' ', '_')}"
        
        return merged
    
    def save_merged_data(self, misconceptions: List[Dict], coke_chains: List[Dict]):
        """Save merged data in format compatible with builders"""
        print("\n" + "=" * 60)
        print("SAVING MERGED DATA")
        print("=" * 60)
        
        # Save misconceptions (compatible with PedagogicalKGBuilder)
        misconceptions_file = self.data_dir / "misconceptions.json"
        with open(misconceptions_file, 'w', encoding='utf-8') as f:
            json.dump(misconceptions, f, indent=2, ensure_ascii=False)
        print(f"✓ Saved {len(misconceptions)} misconceptions to {misconceptions_file}")
        
        # Save COKE chains (compatible with COKECognitiveGraph)
        coke_chains_file = self.data_dir / "coke_chains.json"
        with open(coke_chains_file, 'w', encoding='utf-8') as f:
            json.dump(coke_chains, f, indent=2, ensure_ascii=False)
        print(f"✓ Saved {len(coke_chains)} COKE chains to {coke_chains_file}")
        
        return misconceptions_file, coke_chains_file


def main():
    """Main function"""
    merger = LearnedDataMerger()
    
    # Load learned data
    misconceptions = merger.load_learned_misconceptions()
    coke_chains = merger.load_learned_coke_chains()
    
    if not misconceptions and not coke_chains:
        print("\n⚠ No learned data found. Run learning scripts first:")
        print("  1. python scripts/learn_misconceptions_from_codenet.py")
        print("  2. python scripts/learn_coke_chains_from_progsnap2.py")
        print("  3. python scripts/learn_misconceptions_from_assistments.py")
        return
    
    # Merge misconceptions
    if misconceptions:
        merged_misconceptions = merger.merge_misconceptions(misconceptions)
    else:
        merged_misconceptions = []
    
    # Save merged data
    misconceptions_file, coke_chains_file = merger.save_merged_data(
        merged_misconceptions, coke_chains
    )
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Total misconceptions: {len(merged_misconceptions)}")
    print(f"Total COKE chains: {len(coke_chains)}")
    print(f"\n✓ Merged data saved:")
    print(f"  - {misconceptions_file}")
    print(f"  - {coke_chains_file}")
    print("\n✓ System will now use learned data instead of hardcoded values!")


if __name__ == "__main__":
    main()





