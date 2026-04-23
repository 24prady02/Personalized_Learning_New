"""
Initialize Nestor Bayesian Profiler in the system
Run this to set up Nestor profiler with synthetic data
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.models.nestor.nestor_bayesian_profiler import NestorBayesianProfiler
import json


def initialize_nestor_profiler(config_path: str = 'config.yaml'):
    """Initialize Nestor profiler and add to system"""
    import yaml
    
    # Load config
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    # Initialize Nestor profiler
    print("=" * 60)
    print("Initializing Nestor Bayesian Profiler")
    print("=" * 60)
    
    profiler = NestorBayesianProfiler(config)
    
    # Test inference
    print("\n🧪 Testing Nestor inference...")
    test_behavioral_data = {
        'exploration_rate': 0.7,
        'persistence': 0.6,
        'organization': 0.8,
        'social_interaction': 0.5,
        'emotional_variability': 0.4
    }
    
    result = profiler.complete_inference(test_behavioral_data)
    
    print("\n✅ Nestor Inference Result:")
    print(f"   Personality: {result['personality']}")
    print(f"   Learning Styles: {result['learning_styles']}")
    print(f"   Top Learning Elements: {result['recommended_elements']}")
    
    print("\n✅ Nestor profiler initialized successfully!")
    print("\nTo use in orchestrator:")
    print("   models['nestor_profiler'] = profiler")
    
    return profiler


if __name__ == '__main__':
    profiler = initialize_nestor_profiler()





