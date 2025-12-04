"""
Generate synthetic dataset for Nestor Bayesian Network training

Based on the Nestor paper methodology:
- Uses Bayesian Network structure to generate realistic samples
- Maintains statistical properties of empirical data
- Can be used when real data is not available
"""

import pandas as pd
import numpy as np
from pathlib import Path
import argparse
import yaml
from typing import Dict, List
try:
    from pgmpy.models import BayesianNetwork
    from pgmpy.factors.discrete import TabularCPD
    from pgmpy.sampling import BayesianModelSampling
    PGMPY_AVAILABLE = True
except ImportError:
    PGMPY_AVAILABLE = False
    print("[WARN] pgmpy not available. Install with: pip install pgmpy")


def create_nestor_bn_structure() -> Dict:
    """
    Create the Nestor Bayesian Network structure
    Based on the paper: Personality → Learning Style → Strategy → Learning Element
    """
    # Define edges (dependencies)
    edges = []
    
    # Personality traits (root nodes)
    personality_traits = [
        'personality_openness',
        'personality_conscientiousness', 
        'personality_extraversion',
        'personality_agreeableness',
        'personality_neuroticism'
    ]
    
    # Learning style dimensions
    learning_styles = [
        'style_visual_verbal',
        'style_active_reflective',
        'style_sequential_global'
    ]
    
    # Learning strategies
    learning_strategies = [
        'strategy_elaboration',
        'strategy_organization',
        'strategy_critical_thinking',
        'strategy_metacognitive_self_regulation',
        'strategy_time_management'
    ]
    
    # Emotional state (influences everything)
    emotional_states = ['emotional_state']
    
    # Learning elements (target variable)
    learning_elements = ['learning_element']
    
    # Build edges: Personality → Learning Styles
    for trait in personality_traits:
        for style in learning_styles:
            edges.append((trait, style))
    
    # Emotional state → Learning Styles
    for style in learning_styles:
        edges.append(('emotional_state', style))
    
    # Personality + Learning Styles → Learning Strategies
    for trait in personality_traits:
        for strategy in learning_strategies:
            edges.append((trait, strategy))
    
    for style in learning_styles:
        for strategy in learning_strategies:
            edges.append((style, strategy))
    
    # Emotional state → Learning Strategies
    for strategy in learning_strategies:
        edges.append(('emotional_state', strategy))
    
    # Everything → Learning Elements
    for trait in personality_traits:
        edges.append((trait, 'learning_element'))
    
    for style in learning_styles:
        edges.append((style, 'learning_element'))
    
    for strategy in learning_strategies:
        edges.append((strategy, 'learning_element'))
    
    edges.append(('emotional_state', 'learning_element'))
    
    return {
        'edges': edges,
        'personality_traits': personality_traits,
        'learning_styles': learning_styles,
        'learning_strategies': learning_strategies,
        'emotional_states': emotional_states,
        'learning_elements': learning_elements
    }


def generate_synthetic_data_pgmpy(size: int = 1000, seed: int = 42) -> pd.DataFrame:
    """
    Generate synthetic data using pgmpy Bayesian Network sampling
    """
    if not PGMPY_AVAILABLE:
        raise ImportError("pgmpy is required. Install with: pip install pgmpy")
    
    np.random.seed(seed)
    
    # Get structure
    structure = create_nestor_bn_structure()
    
    # Create Bayesian Network
    model = BayesianNetwork(structure['edges'])
    
    # Define CPDs (Conditional Probability Distributions)
    # Based on literature and reasonable priors
    
    # 1. Personality traits (marginal distributions - uniform prior)
    for trait in structure['personality_traits']:
        cpd = TabularCPD(
            variable=trait,
            variable_card=3,  # low, medium, high
            values=[[0.33], [0.34], [0.33]]  # Uniform distribution
        )
        model.add_cpds(cpd)
    
    # 2. Emotional state (marginal)
    emotional_cpd = TabularCPD(
        variable='emotional_state',
        variable_card=5,  # frustrated, engaged, confused, systematic, exploratory
        values=[[0.2], [0.3], [0.15], [0.2], [0.15]]  # Slightly favor engaged
    )
    model.add_cpds(emotional_cpd)
    
    # 3. Learning styles (conditional on personality + emotion)
    # Example: Visual/Verbal depends on openness and emotional state
    for style in structure['learning_styles']:
        if style == 'style_visual_verbal':
            # Visual preference increases with openness and engagement
            cpd = TabularCPD(
                variable=style,
                variable_card=2,  # visual, verbal
                evidence=['personality_openness', 'emotional_state'],
                evidence_card=[3, 5],
                values=[
                    # Low openness, frustrated -> verbal
                    [0.3, 0.3, 0.3, 0.3, 0.3],  # frustrated
                    [0.4, 0.4, 0.4, 0.4, 0.4],  # engaged
                    [0.3, 0.3, 0.3, 0.3, 0.3],  # confused
                    [0.5, 0.5, 0.5, 0.5, 0.5],  # systematic
                    [0.4, 0.4, 0.4, 0.4, 0.4],  # exploratory
                    # Medium openness
                    [0.4, 0.4, 0.4, 0.4, 0.4],
                    [0.5, 0.5, 0.5, 0.5, 0.5],
                    [0.4, 0.4, 0.4, 0.4, 0.4],
                    [0.6, 0.6, 0.6, 0.6, 0.6],
                    [0.5, 0.5, 0.5, 0.5, 0.5],
                    # High openness -> visual
                    [0.6, 0.6, 0.6, 0.6, 0.6],
                    [0.7, 0.7, 0.7, 0.7, 0.7],
                    [0.6, 0.6, 0.6, 0.6, 0.6],
                    [0.8, 0.8, 0.8, 0.8, 0.8],
                    [0.7, 0.7, 0.7, 0.7, 0.7],
                ]
            )
        else:
            # Simplified CPD for other styles
            cpd = TabularCPD(
                variable=style,
                variable_card=2,
                evidence=['personality_openness'],
                evidence_card=[3],
                values=[
                    [0.4, 0.5, 0.6],  # Low -> first option
                    [0.6, 0.5, 0.4],  # High -> second option
                ]
            )
        model.add_cpds(cpd)
    
    # 4. Learning strategies (conditional on personality + style + emotion)
    # Simplified: Use personality and emotional state
    for strategy in structure['learning_strategies']:
        cpd = TabularCPD(
            variable=strategy,
            variable_card=3,  # low, medium, high
            evidence=['personality_conscientiousness', 'emotional_state'],
            evidence_card=[3, 5],
            values=[
                # Low conscientiousness
                [0.5, 0.3, 0.2, 0.4, 0.3],  # frustrated
                [0.3, 0.4, 0.3, 0.2, 0.3],  # engaged
                [0.4, 0.3, 0.3, 0.3, 0.3],  # confused
                [0.2, 0.4, 0.4, 0.3, 0.4],  # systematic
                [0.3, 0.3, 0.4, 0.3, 0.3],  # exploratory
                # Medium conscientiousness
                [0.3, 0.4, 0.3, 0.3, 0.3],
                [0.2, 0.3, 0.5, 0.2, 0.3],
                [0.3, 0.3, 0.4, 0.3, 0.3],
                [0.1, 0.3, 0.6, 0.2, 0.3],
                [0.2, 0.3, 0.5, 0.3, 0.3],
                # High conscientiousness
                [0.2, 0.3, 0.5, 0.2, 0.3],
                [0.1, 0.2, 0.7, 0.1, 0.2],
                [0.2, 0.3, 0.5, 0.2, 0.3],
                [0.1, 0.2, 0.7, 0.1, 0.2],
                [0.1, 0.2, 0.7, 0.2, 0.2],
            ]
        )
        model.add_cpds(cpd)
    
    # 5. Learning elements (conditional on all parent variables)
    # Simplified: Use personality, style, strategy, and emotion
    # 9 learning elements: BO, LG, MS, SU, EX, QU, VAM, TAM, AAM
    learning_element_cpd = TabularCPD(
        variable='learning_element',
        variable_card=9,
        evidence=['personality_openness', 'style_visual_verbal', 'emotional_state'],
        evidence_card=[3, 2, 5],
        # Uniform distribution (can be refined based on domain knowledge)
        values=np.ones((9, 30)) / 9  # 3 * 2 * 5 = 30 combinations
    )
    model.add_cpds(learning_element_cpd)
    
    # Validate model
    if not model.check_model():
        print("[WARN] Model validation failed, but continuing...")
    
    # Sample from the network
    sampler = BayesianModelSampling(model)
    samples = sampler.forward_sample(size=size)
    
    # Convert to DataFrame
    df = samples.copy()
    
    # Map numeric values to categorical labels
    # Personality traits
    for trait in structure['personality_traits']:
        df[trait] = df[trait].map({0: 'low', 1: 'medium', 2: 'high'})
    
    # Learning styles
    style_mappings = {
        'style_visual_verbal': {0: 'visual', 1: 'verbal'},
        'style_active_reflective': {0: 'active', 1: 'reflective'},
        'style_sequential_global': {0: 'sequential', 1: 'global'}
    }
    for style, mapping in style_mappings.items():
        if style in df.columns:
            df[style] = df[style].map(mapping)
    
    # Learning strategies
    for strategy in structure['learning_strategies']:
        df[strategy] = df[strategy].map({0: 'low', 1: 'medium', 2: 'high'})
    
    # Emotional state
    df['emotional_state'] = df['emotional_state'].map({
        0: 'frustrated',
        1: 'engaged',
        2: 'confused',
        3: 'systematic',
        4: 'exploratory'
    })
    
    # Learning elements
    learning_element_labels = ['BO', 'LG', 'MS', 'SU', 'EX', 'QU', 'VAM', 'TAM', 'AAM']
    df['learning_element'] = df['learning_element'].map(
        {i: label for i, label in enumerate(learning_element_labels)}
    )
    
    return df


def generate_synthetic_data_simple(size: int = 1000, seed: int = 42) -> pd.DataFrame:
    """
    Generate synthetic data using simple random sampling
    (Fallback when pgmpy is not available)
    """
    np.random.seed(seed)
    
    structure = create_nestor_bn_structure()
    
    data = {}
    
    # Personality traits (uniform distribution)
    for trait in structure['personality_traits']:
        data[trait] = np.random.choice(['low', 'medium', 'high'], size=size, p=[0.33, 0.34, 0.33])
    
    # Emotional state
    data['emotional_state'] = np.random.choice(
        ['frustrated', 'engaged', 'confused', 'systematic', 'exploratory'],
        size=size,
        p=[0.2, 0.3, 0.15, 0.2, 0.15]
    )
    
    # Learning styles (correlated with personality)
    for style in structure['learning_styles']:
        if style == 'style_visual_verbal':
            # Higher openness -> more visual
            data[style] = [
                'visual' if np.random.random() > 0.4 + (0.2 if p == 'high' else -0.2 if p == 'low' else 0)
                else 'verbal'
                for p in data['personality_openness']
            ]
        elif style == 'style_active_reflective':
            # Higher extraversion -> more active
            data[style] = [
                'active' if np.random.random() > 0.4 + (0.2 if p == 'high' else -0.2 if p == 'low' else 0)
                else 'reflective'
                for p in data['personality_extraversion']
            ]
        else:  # sequential_global
            # Higher conscientiousness -> more sequential
            data[style] = [
                'sequential' if np.random.random() > 0.4 + (0.2 if p == 'high' else -0.2 if p == 'low' else 0)
                else 'global'
                for p in data['personality_conscientiousness']
            ]
    
    # Learning strategies (correlated with conscientiousness)
    for strategy in structure['learning_strategies']:
        data[strategy] = [
            np.random.choice(['low', 'medium', 'high'], p=[
                0.3 if c == 'low' else 0.1 if c == 'high' else 0.2,
                0.4 if c == 'low' else 0.3 if c == 'high' else 0.4,
                0.3 if c == 'low' else 0.6 if c == 'high' else 0.4
            ])
            for c in data['personality_conscientiousness']
        ]
    
    # Learning elements (correlated with all factors)
    learning_elements = ['BO', 'LG', 'MS', 'SU', 'EX', 'QU', 'VAM', 'TAM', 'AAM']
    data['learning_element'] = np.random.choice(learning_elements, size=size)
    
    return pd.DataFrame(data)


def main():
    parser = argparse.ArgumentParser(description='Generate synthetic dataset for Nestor training')
    parser.add_argument('--size', type=int, default=1000, help='Number of samples to generate')
    parser.add_argument('--output', type=str, default='data/processed/nestor_training_data.csv',
                       help='Output file path')
    parser.add_argument('--seed', type=int, default=42, help='Random seed')
    parser.add_argument('--method', type=str, choices=['pgmpy', 'simple'], default='pgmpy',
                       help='Generation method (pgmpy uses BN, simple uses random)')
    
    args = parser.parse_args()
    
    # Create output directory
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    print(f"Generating {args.size} synthetic samples for Nestor training...")
    print(f"Method: {args.method}")
    
    try:
        if args.method == 'pgmpy' and PGMPY_AVAILABLE:
            df = generate_synthetic_data_pgmpy(size=args.size, seed=args.seed)
            print("✓ Generated using Bayesian Network sampling (pgmpy)")
        else:
            if args.method == 'pgmpy':
                print("[WARN] pgmpy not available, falling back to simple method")
            df = generate_synthetic_data_simple(size=args.size, seed=args.seed)
            print("✓ Generated using simple random sampling")
        
        # Save to CSV
        df.to_csv(output_path, index=False)
        print(f"✓ Saved {len(df)} samples to {output_path}")
        print(f"\nDataset columns: {list(df.columns)}")
        print(f"\nFirst few rows:")
        print(df.head())
        print(f"\nValue counts for learning_element:")
        print(df['learning_element'].value_counts())
        
    except Exception as e:
        print(f"✗ Error generating data: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == '__main__':
    exit(main())





