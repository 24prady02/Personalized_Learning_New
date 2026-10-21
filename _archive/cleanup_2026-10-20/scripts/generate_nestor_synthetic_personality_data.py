"""
Generate synthetic personality data for Nestor Bayesian Network training
Based on the Nestor paper: ECSEE 2025

Generates data for:
- Big Five Inventory (BFI) Personalities (P1-P5)
- Felder-Silverman Learning Style Dimensions (D1-D4)
- LISTK Learning Strategies (T1-T4)
- Learning Elements (L) with 9 states
"""

import numpy as np
import pandas as pd
from typing import Dict, List
import json
from pathlib import Path


class NestorSyntheticDataGenerator:
    """
    Generate synthetic personality data based on Nestor framework
    
    Structure:
    - BFI Personalities (root nodes) → Learning Styles
    - BFI Personalities (root nodes) → Learning Strategies
    - All → Learning Elements
    """
    
    def __init__(self, n_samples: int = 1000, seed: int = 42):
        """
        Args:
            n_samples: Number of synthetic samples to generate
            seed: Random seed for reproducibility
        """
        self.n_samples = n_samples
        np.random.seed(seed)
        
        # BFI Personality traits (5 dimensions)
        self.personality_traits = [
            'openness', 'conscientiousness', 'extraversion', 
            'agreeableness', 'neuroticism'
        ]
        
        # Felder-Silverman Learning Style Dimensions (4 dimensions)
        self.learning_style_dimensions = [
            'visual_verbal',      # D1: Visual vs Verbal
            'sensing_intuitive',  # D2: Sensing vs Intuitive
            'active_reflective',  # D3: Active vs Reflective
            'sequential_global'   # D4: Sequential vs Global
        ]
        
        # LISTK Learning Strategies (4 strategies)
        self.learning_strategies = [
            'deep_processing',    # T1: Deep processing
            'elaboration',        # T2: Elaboration
            'organization',        # T3: Organization
            'metacognition'       # T4: Metacognition
        ]
        
        # Learning Elements (9 states from Staufer et al. 2024)
        self.learning_elements = [
            'BO',   # Book/Text
            'LG',   # Learning Game
            'MS',   # Multimedia Simulation
            'SU',   # Summary
            'EX',   # Exercise
            'QU',   # Quiz
            'VAM',  # Video Animation
            'TAM',  # Text Animation
            'AAM'   # Audio Animation
        ]
    
    def generate_personality_scores(self) -> np.ndarray:
        """
        Generate BFI personality scores (root nodes)
        Returns: [n_samples, 5] array of personality scores (0-1 scale)
        """
        # Use beta distribution to create realistic personality distributions
        # Beta(2, 2) gives bell-shaped distribution centered at 0.5
        personalities = np.zeros((self.n_samples, 5))
        
        for i in range(5):
            # Vary the distribution for each trait
            alpha = np.random.uniform(1.5, 3.0)
            beta = np.random.uniform(1.5, 3.0)
            personalities[:, i] = np.random.beta(alpha, beta, self.n_samples)
        
        return personalities
    
    def personality_to_learning_style(self, personalities: np.ndarray) -> np.ndarray:
        """
        Generate learning style dimensions based on personalities
        P(Personalities) → P(Learning Styles | Personalities)
        
        Based on research: Personalities influence learning styles
        """
        learning_styles = np.zeros((self.n_samples, 4))
        
        # D1: Visual vs Verbal (influenced by Openness)
        # High openness → more visual, creative
        openness = personalities[:, 0]
        learning_styles[:, 0] = np.clip(
            openness * 0.6 + np.random.normal(0, 0.15, self.n_samples),
            0, 1
        )
        
        # D2: Sensing vs Intuitive (influenced by Openness + Conscientiousness)
        # High openness + low conscientiousness → intuitive
        openness = personalities[:, 0]
        conscientiousness = personalities[:, 1]
        learning_styles[:, 1] = np.clip(
            (openness * 0.4 - conscientiousness * 0.2) + 
            np.random.normal(0, 0.2, self.n_samples) + 0.5,
            0, 1
        )
        
        # D3: Active vs Reflective (influenced by Extraversion)
        # High extraversion → active
        extraversion = personalities[:, 2]
        learning_styles[:, 2] = np.clip(
            extraversion * 0.7 + np.random.normal(0, 0.15, self.n_samples),
            0, 1
        )
        
        # D4: Sequential vs Global (influenced by Conscientiousness)
        # High conscientiousness → sequential
        conscientiousness = personalities[:, 1]
        learning_styles[:, 3] = np.clip(
            conscientiousness * 0.6 + np.random.normal(0, 0.2, self.n_samples),
            0, 1
        )
        
        return learning_styles
    
    def personality_to_learning_strategy(self, personalities: np.ndarray) -> np.ndarray:
        """
        Generate learning strategies based on personalities
        P(Personalities) → P(Learning Strategies | Personalities)
        """
        strategies = np.zeros((self.n_samples, 4))
        
        # T1: Deep Processing (influenced by Openness + Conscientiousness)
        openness = personalities[:, 0]
        conscientiousness = personalities[:, 1]
        strategies[:, 0] = np.clip(
            (openness * 0.4 + conscientiousness * 0.4) + 
            np.random.normal(0, 0.15, self.n_samples),
            0, 1
        )
        
        # T2: Elaboration (influenced by Openness)
        strategies[:, 1] = np.clip(
            openness * 0.5 + np.random.normal(0, 0.2, self.n_samples),
            0, 1
        )
        
        # T3: Organization (influenced by Conscientiousness)
        conscientiousness = personalities[:, 1]
        strategies[:, 2] = np.clip(
            conscientiousness * 0.7 + np.random.normal(0, 0.15, self.n_samples),
            0, 1
        )
        
        # T4: Metacognition (influenced by Conscientiousness + Openness)
        openness = personalities[:, 0]
        conscientiousness = personalities[:, 1]
        strategies[:, 3] = np.clip(
            (openness * 0.3 + conscientiousness * 0.5) + 
            np.random.normal(0, 0.15, self.n_samples),
            0, 1
        )
        
        return strategies
    
    def all_to_learning_elements(self, personalities: np.ndarray,
                                 learning_styles: np.ndarray,
                                 strategies: np.ndarray) -> np.ndarray:
        """
        Generate learning element preferences based on all characteristics
        P(Personalities, Learning Styles, Strategies) → P(Learning Elements)
        """
        # Combine all features
        all_features = np.hstack([personalities, learning_styles, strategies])
        n_features = all_features.shape[1]
        
        # Create preference scores for each learning element
        element_scores = np.zeros((self.n_samples, len(self.learning_elements)))
        
        # Define weights for each learning element based on characteristics
        # These are based on research correlations
        weights = {
            'BO': [0.1, 0.3, 0.0, 0.0, 0.0, 0.2, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],  # Text: high conscientiousness
            'LG': [0.2, 0.1, 0.3, 0.0, 0.0, 0.0, 0.4, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],  # Game: high extraversion, active
            'MS': [0.3, 0.1, 0.2, 0.0, 0.0, 0.4, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],  # Simulation: high openness, visual
            'SU': [0.1, 0.4, 0.0, 0.0, 0.0, 0.0, 0.0, 0.3, 0.0, 0.0, 0.0, 0.0, 0.0],  # Summary: high conscientiousness, organization
            'EX': [0.1, 0.2, 0.2, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],  # Exercise: active, elaboration
            'QU': [0.1, 0.3, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.4, 0.0, 0.0, 0.0, 0.0],  # Quiz: conscientiousness, metacognition
            'VAM': [0.4, 0.1, 0.1, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],  # Video: high openness, visual
            'TAM': [0.2, 0.2, 0.0, 0.0, 0.0, 0.3, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],  # Text Animation: moderate
            'AAM': [0.3, 0.1, 0.2, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]   # Audio: openness
        }
        
        for i, element in enumerate(self.learning_elements):
            w = np.array(weights[element])
            # Compute weighted sum
            scores = np.dot(all_features, w[:n_features])
            # Add noise
            scores += np.random.normal(0, 0.1, self.n_samples)
            element_scores[:, i] = np.clip(scores, 0, 1)
        
        # Convert to discrete choices (select top preference)
        element_choices = np.argmax(element_scores, axis=1)
        
        return element_choices
    
    def generate_dataset(self) -> pd.DataFrame:
        """
        Generate complete synthetic dataset
        """
        # 1. Generate personalities (root nodes)
        personalities = self.generate_personality_scores()
        
        # 2. Generate learning styles (conditioned on personalities)
        learning_styles = self.personality_to_learning_style(personalities)
        
        # 3. Generate learning strategies (conditioned on personalities)
        strategies = self.personality_to_learning_strategy(personalities)
        
        # 4. Generate learning elements (conditioned on all)
        learning_elements = self.all_to_learning_elements(
            personalities, learning_styles, strategies
        )
        
        # Create DataFrame
        data = {}
        
        # Add personalities
        for i, trait in enumerate(self.personality_traits):
            data[f'P{i+1}_{trait}'] = personalities[:, i]
        
        # Add learning styles (discretize: 0-0.5 = first option, 0.5-1 = second option)
        for i, dim in enumerate(self.learning_style_dimensions):
            data[f'D{i+1}_{dim}'] = (learning_styles[:, i] > 0.5).astype(int)
        
        # Add learning strategies (discretize)
        for i, strategy in enumerate(self.learning_strategies):
            data[f'T{i+1}_{strategy}'] = (strategies[:, i] > 0.5).astype(int)
        
        # Add learning elements
        data['L_learning_element'] = [self.learning_elements[int(e)] for e in learning_elements]
        
        df = pd.DataFrame(data)
        
        return df
    
    def save_dataset(self, df: pd.DataFrame, output_dir: Path = Path('data/nestor')):
        """
        Save dataset to files
        """
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Save as CSV
        csv_path = output_dir / 'nestor_synthetic_personality_data.csv'
        df.to_csv(csv_path, index=False)
        print(f"✅ Saved CSV to {csv_path}")
        
        # Save as JSON (for easier loading)
        json_path = output_dir / 'nestor_synthetic_personality_data.json'
        df.to_json(json_path, orient='records', indent=2)
        print(f"✅ Saved JSON to {json_path}")
        
        # Save metadata
        metadata = {
            'n_samples': self.n_samples,
            'personality_traits': self.personality_traits,
            'learning_style_dimensions': self.learning_style_dimensions,
            'learning_strategies': self.learning_strategies,
            'learning_elements': self.learning_elements,
            'description': 'Synthetic personality data for Nestor Bayesian Network training'
        }
        metadata_path = output_dir / 'nestor_metadata.json'
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        print(f"✅ Saved metadata to {metadata_path}")
        
        return csv_path, json_path, metadata_path


def main():
    """Generate synthetic Nestor personality data"""
    print("=" * 60)
    print("Nestor Synthetic Personality Data Generator")
    print("Based on: ECSEE 2025 Paper")
    print("=" * 60)
    
    # Generate different sizes (as in the paper)
    sizes = [50, 100, 500, 1000, 5000, 10000]
    
    for size in sizes:
        print(f"\n📊 Generating {size} samples...")
        generator = NestorSyntheticDataGenerator(n_samples=size, seed=42)
        df = generator.generate_dataset()
        
        # Save
        output_dir = Path(f'data/nestor/synthetic_{size}')
        csv_path, json_path, metadata_path = generator.save_dataset(df, output_dir)
        
        print(f"   Generated {len(df)} samples")
        print(f"   Columns: {list(df.columns)}")
        print(f"   Learning element distribution:")
        print(df['L_learning_element'].value_counts().to_dict())


if __name__ == '__main__':
    main()





