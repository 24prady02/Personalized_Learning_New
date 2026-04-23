"""
Training script for Personalized Learning System
Multi-task learning with HVSAE, DINA, and Behavioral models
"""

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
import yaml
from pathlib import Path
import argparse
from tqdm import tqdm
try:
    import wandb
    WANDB_AVAILABLE = True
except ImportError:
    WANDB_AVAILABLE = False
from datetime import datetime
from typing import Dict, Tuple, Optional

from src.models.hvsae import HVSAE
from src.models.dina import DINAModel
from src.models.behavioral import BehavioralRNN, BehavioralHMM
from src.models.nestor import NestorBayesianNetwork
from src.data.dataloader import create_dataloaders
from src.data.processors import (
    CodeNetProcessor, 
    ProgSnap2Processor, 
    ASSISTmentsProcessor,
    MOOCCubeXProcessor
)
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split


class Trainer:
    """
    Multi-task trainer for personalized learning system
    """
    
    def __init__(self, config: Dict, models: Dict, dataloaders: Dict):
        self.config = config
        self.models = models
        self.dataloaders = dataloaders
        
        # Device
        self.device = torch.device(config['system']['device'])
        
        # Move models to device
        for name, model in self.models.items():
            if isinstance(model, nn.Module):
                model.to(self.device)
        
        # Optimizers
        self.optimizers = self._create_optimizers()
        
        # Schedulers
        self.schedulers = self._create_schedulers()
        
        # Loss weights
        self.loss_weights = config['training']['loss_weights']
        
        # Training state
        self.epoch = 0
        self.best_val_loss = float('inf')
        
        # Logging
        self.use_wandb = False
        
    def _create_optimizers(self) -> Dict:
        """Create optimizers for each model"""
        lr = self.config['training']['learning_rate']
        weight_decay = self.config['training']['weight_decay']
        
        optimizers = {}
        
        if 'hvsae' in self.models:
            optimizers['hvsae'] = optim.AdamW(
                self.models['hvsae'].parameters(),
                lr=lr,
                weight_decay=weight_decay
            )
        
        if 'dina' in self.models:
            optimizers['dina'] = optim.Adam(
                self.models['dina'].parameters(),
                lr=lr * 0.1  # Slower for DINA
            )
        
        if 'behavioral_rnn' in self.models:
            optimizers['behavioral_rnn'] = optim.AdamW(
                self.models['behavioral_rnn'].parameters(),
                lr=lr,
                weight_decay=weight_decay
            )
        
        return optimizers
    
    def _create_schedulers(self) -> Dict:
        """Create learning rate schedulers (optional — skipped if not configured)."""
        schedulers = {}
        scheduler_config = self.config.get('training', {}).get('scheduler')
        if not scheduler_config:
            return schedulers
        scheduler_type = scheduler_config.get('type', 'step')
        num_epochs = self.config['training'].get('num_epochs',
                     self.config['training'].get('epochs', 10))
        for name, optimizer in self.optimizers.items():
            if scheduler_type == 'cosine':
                schedulers[name] = optim.lr_scheduler.CosineAnnealingLR(
                    optimizer, T_max=num_epochs,
                    eta_min=scheduler_config.get('min_lr', 1e-6),
                )
            elif scheduler_type == 'step':
                schedulers[name] = optim.lr_scheduler.StepLR(
                    optimizer, step_size=10, gamma=0.5,
                )
        return schedulers
    
    def train_epoch(self) -> Dict[str, float]:
        """Train for one epoch"""
        # Check if dataloaders are available
        if 'train' not in self.dataloaders or len(self.dataloaders['train']) == 0:
            print("⚠️  No training data available! Skipping training epoch.")
            return {
                'total': 0.0,
                'reconstruction': 0.0,
                'misconception': 0.0,
                'kl_divergence': 0.0,
                'behavioral': 0.0
            }
        
        # Set models to train mode
        for model in self.models.values():
            if isinstance(model, nn.Module):
                model.train()
        
        total_losses = {
            'total': 0.0,
            'reconstruction': 0.0,
            'misconception': 0.0,
            'kl_divergence': 0.0,
            'behavioral': 0.0
        }
        
        num_batches = 0
        
        # Training loop
        pbar = tqdm(self.dataloaders['train'], desc=f'Epoch {self.epoch}')
        
        for batch in pbar:
            # Move batch to device
            batch = self._to_device(batch)
            
            # === HVSAE Forward ===
            if 'hvsae' in self.models:
                concept_labels = batch.get('concept_label', None)
                # Filter out unlabelled samples (-1)
                if concept_labels is not None:
                    mask = concept_labels >= 0
                    concept_labels = concept_labels[mask] if mask.any() else None
                hvsae_losses = self.models['hvsae'].compute_loss(
                    batch, concept_labels=concept_labels
                )
                
                # Backward
                self.optimizers['hvsae'].zero_grad()
                hvsae_losses['total'].backward()
                
                # Gradient clipping
                nn.utils.clip_grad_norm_(
                    self.models['hvsae'].parameters(),
                    self.config['training']['gradient_clip']
                )
                
                self.optimizers['hvsae'].step()
                
                # Accumulate losses
                for key, value in hvsae_losses.items():
                    if key in total_losses:
                        total_losses[key] += value.item()
            
            # === Behavioral RNN Forward ===
            if 'behavioral_rnn' in self.models:
                # timestamps come in as (B, T, 1); behavioral_rnn expects (B, T)
                ts = batch['timestamps']
                if ts.dim() == 3 and ts.size(-1) == 1:
                    ts = ts.squeeze(-1)
                behavioral_outputs = self.models['behavioral_rnn'](
                    batch['action_sequence'],
                    ts,
                    torch.zeros_like(batch['action_sequence'], dtype=torch.float),
                    batch['sequence_lengths']
                )
                
                # Behavioral losses
                behavioral_targets = {}
                if 'emotion_label' in batch:
                    behavioral_targets['emotion_labels'] = batch['emotion_label']
                
                if behavioral_targets:
                    # Merge outputs with targets for compute_loss
                    loss_batch = {**batch, **behavioral_targets}
                    # squeeze timestamps here too for compute_loss
                    loss_batch['timestamps'] = ts
                    bl = self.models['behavioral_rnn'].compute_loss(loss_batch)
                    # compute_loss may return a scalar tensor or a dict
                    total_loss = bl['total'] if isinstance(bl, dict) else bl

                    # Only backprop if loss is finite and non-zero (emotion mask may be all -1)
                    if total_loss.requires_grad and torch.isfinite(total_loss):
                        self.optimizers['behavioral_rnn'].zero_grad()
                        total_loss.backward()
                        self.optimizers['behavioral_rnn'].step()
                        total_losses['behavioral'] += total_loss.item()
            
            num_batches += 1
            
            # Update progress bar
            pbar.set_postfix({
                'loss': total_losses['total'] / num_batches
            })
        
        # Average losses
        avg_losses = {
            key: value / num_batches 
            for key, value in total_losses.items()
        }
        
        return avg_losses
    
    def validate(self) -> Dict[str, float]:
        """Validate on validation set"""
        # Check if validation dataloader is available
        if 'val' not in self.dataloaders or len(self.dataloaders['val']) == 0:
            print("⚠️  No validation data available! Skipping validation.")
            return {
                'total': 0.0,
                'reconstruction': 0.0,
                'misconception': 0.0,
                'kl_divergence': 0.0
            }
        
        # Set models to eval mode
        for model in self.models.values():
            if isinstance(model, nn.Module):
                model.eval()
        
        total_losses = {
            'total': 0.0,
            'reconstruction': 0.0,
            'misconception': 0.0,
            'kl_divergence': 0.0
        }
        
        num_batches = 0
        
        with torch.no_grad():
            for batch in tqdm(self.dataloaders['val'], desc='Validation'):
                batch = self._to_device(batch)
                
                if 'hvsae' in self.models:
                    # HVSAE.compute_loss signature is (batch, concept_labels=None)
                    concept_labels = batch.get('concept_label', None)
                    if concept_labels is not None:
                        mask = concept_labels >= 0
                        concept_labels = concept_labels[mask] if mask.any() else None
                    hvsae_losses = self.models['hvsae'].compute_loss(
                        batch, concept_labels=concept_labels
                    )

                    for key, value in hvsae_losses.items():
                        if key in total_losses:
                            total_losses[key] += value.item()
                
                num_batches += 1
        
        # Average losses
        avg_losses = {
            key: value / num_batches 
            for key, value in total_losses.items()
        }
        
        return avg_losses
    
    def train(self, num_epochs: Optional[int] = None):
        """Full training loop"""
        if num_epochs is None:
            num_epochs = self.config['training'].get(
                'num_epochs', self.config['training'].get('epochs', 10)
            )
        
        print(f"Starting training for {num_epochs} epochs")
        
        for epoch in range(num_epochs):
            self.epoch = epoch
            
            # Train epoch
            train_losses = self.train_epoch()
            
            # Validate
            val_losses = self.validate()
            
            # Learning rate scheduling
            for scheduler in self.schedulers.values():
                scheduler.step()
            
            # Logging
            print(f"\nEpoch {epoch}")
            print(f"Train Loss: {train_losses['total']:.4f}")
            print(f"Val Loss: {val_losses['total']:.4f}")
            
            if self.use_wandb:
                wandb.log({
                    'train_loss': train_losses['total'],
                    'val_loss': val_losses['total'],
                    'epoch': epoch
                })
            
            # Save checkpoint
            if val_losses['total'] < self.best_val_loss:
                self.best_val_loss = val_losses['total']
                self.save_checkpoint('best')
                print("✓ Saved best model")
            
            # Save periodic checkpoint
            if (epoch + 1) % 10 == 0:
                self.save_checkpoint(f'epoch_{epoch+1}')
    
    def _to_device(self, batch: Dict) -> Dict:
        """Move batch to device"""
        device_batch = {}
        for key, value in batch.items():
            if isinstance(value, torch.Tensor):
                device_batch[key] = value.to(self.device)
            elif isinstance(value, dict):
                device_batch[key] = {
                    k: v.to(self.device) if isinstance(v, torch.Tensor) else v
                    for k, v in value.items()
                }
            else:
                device_batch[key] = value
        return device_batch
    
    def save_checkpoint(self, name: str):
        """Save model checkpoint"""
        checkpoint_dir = Path('checkpoints')
        checkpoint_dir.mkdir(exist_ok=True)
        
        checkpoint = {
            'epoch': self.epoch,
            'config': self.config,
            'best_val_loss': self.best_val_loss
        }
        
        # Save model states
        for model_name, model in self.models.items():
            if isinstance(model, nn.Module):
                checkpoint[f'{model_name}_state'] = model.state_dict()
        
        # Save optimizer states
        for opt_name, optimizer in self.optimizers.items():
            checkpoint[f'{opt_name}_optimizer'] = optimizer.state_dict()
        
        torch.save(checkpoint, checkpoint_dir / f'{name}.pt')
    
    def load_checkpoint(self, path: str):
        """Load model checkpoint"""
        checkpoint = torch.load(path, map_location=self.device)
        
        self.epoch = checkpoint['epoch']
        self.best_val_loss = checkpoint['best_val_loss']
        
        # Load model states
        for model_name, model in self.models.items():
            if isinstance(model, nn.Module) and f'{model_name}_state' in checkpoint:
                model.load_state_dict(checkpoint[f'{model_name}_state'])
        
        print(f"Loaded checkpoint from epoch {self.epoch}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', type=str, default='config.yaml')
    parser.add_argument('--resume', type=str, default=None)
    parser.add_argument('--wandb', action='store_true')
    args = parser.parse_args()
    
    # Load config
    with open(args.config, 'r') as f:
        config = yaml.safe_load(f)
    
    # Initialize wandb
    if args.wandb:
        if WANDB_AVAILABLE:
            wandb.init(project='personalized-learning', config=config)
        else:
            print("⚠️  wandb not installed. Install with: pip install wandb")
            print("   Continuing without wandb logging...")
    
    # Create models
    print("Initializing models...")
    models = {}
    
    # HVSAE (always needed)
    models['hvsae'] = HVSAE(config)
    print("✓ Initialized HVSAE")
    
    # DINA Model (if ASSISTments data available)
    if config['data']['datasets']['assistments']['enabled']:
        try:
            # Determine number of concepts from CSE-KG or use default
            num_concepts = config['dina']['num_concepts']
            models['dina'] = DINAModel(config=config)
            print(f"✓ Initialized DINA with {num_concepts} concepts")
        except Exception as e:
            print(f"⚠️  Could not initialize DINA: {e}")
    
    # Behavioral RNN (if ProgSnap2 data available)
    if config['data']['datasets']['progsnap2']['enabled']:
        try:
            models['behavioral_rnn'] = BehavioralRNN(config)
            print("✓ Initialized Behavioral RNN")
        except Exception as e:
            print(f"⚠️  Could not initialize Behavioral RNN: {e}")
        
        try:
            models['behavioral_hmm'] = BehavioralHMM(config)
            print("✓ Initialized Behavioral HMM")
        except Exception as e:
            print(f"⚠️  Could not initialize Behavioral HMM: {e}")
    
    # Nestor Bayesian Network
    try:
        models['nestor'] = NestorBayesianNetwork(config)
        print("✓ Initialized Nestor Bayesian Network")
    except Exception as e:
        print(f"⚠️  Could not initialize Nestor: {e}")
    
    if len(models) == 0:
        raise ValueError("No models initialized! Check your configuration.")
    
    print(f"\n✓ Initialized {len(models)} models: {list(models.keys())}")
    
    # Load and process datasets
    print("Loading and processing datasets...")
    train_data, val_data, test_data = load_all_datasets(config)
    
    if len(train_data) == 0:
        print("⚠️  WARNING: No training data loaded! Check dataset paths in config.yaml")
        print("   Creating dummy dataloaders for testing...")
        dataloaders = {}
    else:
        print(f"✓ Loaded {len(train_data)} training samples, {len(val_data)} validation samples")
        if test_data is not None:
            print(f"✓ Loaded {len(test_data)} test samples")
        
        # Create dataloaders
        dataloaders = create_dataloaders(config, train_data, val_data, test_data)
        print(f"✓ Created dataloaders: {list(dataloaders.keys())}")
    
    # Create trainer
    trainer = Trainer(config, models, dataloaders)
    trainer.use_wandb = args.wandb
    
    # Resume from checkpoint if specified
    if args.resume:
        trainer.load_checkpoint(args.resume)
    
    # Train
    trainer.train()
    
    print("Training complete!")


def load_all_datasets(config: dict) -> tuple:
    """
    Load and combine all datasets for training
    
    Returns:
        Tuple of (train_data, val_data, test_data) DataFrames
    """
    all_data = []
    
    # 1. Load CodeNet (for code understanding)
    if config['data']['datasets']['codenet']['enabled']:
        try:
            print("  Loading CodeNet...")
            codenet_path = config['data']['datasets']['codenet']['path']
            codenet_processor = CodeNetProcessor(codenet_path, config)
            codenet_df = codenet_processor.process()
            
            if len(codenet_df) > 0:
                # Add required columns for dataloader
                codenet_df['error_message'] = ''  # CodeNet doesn't have error messages
                codenet_df['actions'] = [[]] * len(codenet_df)
                codenet_df['time_deltas'] = [[]] * len(codenet_df)
                codenet_df['student_id'] = codenet_df.get('student_id', range(len(codenet_df)))
                codenet_df['problem_id'] = codenet_df.get('problem_id', range(len(codenet_df)))
                all_data.append(codenet_df)
                print(f"    ✓ Loaded {len(codenet_df)} CodeNet samples")
        except Exception as e:
            print(f"    ⚠️  Error loading CodeNet: {e}")
    
    # 2. Load ProgSnap2 (for behavioral sequences)
    if config['data']['datasets']['progsnap2']['enabled']:
        try:
            print("  Loading ProgSnap2...")
            progsnap_path = config['data']['datasets']['progsnap2']['path']
            progsnap_processor = ProgSnap2Processor(progsnap_path, config)
            progsnap_df = progsnap_processor.process()
            
            if len(progsnap_df) > 0:
                # Convert actions and time_deltas to lists if needed
                if 'actions' in progsnap_df.columns:
                    progsnap_df['actions'] = progsnap_df['actions'].apply(
                        lambda x: x if isinstance(x, list) else eval(x) if isinstance(x, str) else []
                    )
                if 'time_deltas' in progsnap_df.columns:
                    progsnap_df['time_deltas'] = progsnap_df['time_deltas'].apply(
                        lambda x: x if isinstance(x, list) else eval(x) if isinstance(x, str) else []
                    )
                
                # Add code column if missing
                if 'code' not in progsnap_df.columns:
                    progsnap_df['code'] = progsnap_df.get('final_code', '')
                if 'error_message' not in progsnap_df.columns:
                    progsnap_df['error_message'] = ''
                
                all_data.append(progsnap_df)
                print(f"    ✓ Loaded {len(progsnap_df)} ProgSnap2 sessions")
        except Exception as e:
            print(f"    ⚠️  Error loading ProgSnap2: {e}")
    
    # 3. Load ASSISTments (for mastery prediction)
    if config['data']['datasets']['assistments']['enabled']:
        try:
            print("  Loading ASSISTments...")
            assistments_path = config['data']['datasets']['assistments']['path']
            assistments_processor = ASSISTmentsProcessor(assistments_path, config)
            responses_df, q_matrix_df = assistments_processor.process()
            
            if len(responses_df) > 0:
                # Convert ASSISTments format to our format
                responses_df['code'] = ''  # ASSISTments doesn't have code
                responses_df['error_message'] = ''
                responses_df['actions'] = [[]] * len(responses_df)
                responses_df['time_deltas'] = [[]] * len(responses_df)
                responses_df['student_id'] = responses_df['user_id']
                responses_df['problem_id'] = responses_df['problem_id']
                # Add mastery labels (correctness)
                responses_df['is_correct'] = responses_df['correct']
                
                all_data.append(responses_df)
                print(f"    ✓ Loaded {len(responses_df)} ASSISTments responses")
        except Exception as e:
            print(f"    ⚠️  Error loading ASSISTments: {e}")
    
    # Combine all datasets
    if len(all_data) == 0:
        print("  ⚠️  No datasets loaded!")
        return pd.DataFrame(), pd.DataFrame(), None
    
    combined_df = pd.concat(all_data, ignore_index=True)
    print(f"\n  ✓ Combined {len(combined_df)} total samples from {len(all_data)} datasets")
    
    # Split into train/val/test (80/10/10)
    train_df, temp_df = train_test_split(
        combined_df, 
        test_size=0.2, 
        random_state=config.get('system', {}).get('seed', config.get('training', {}).get('seed', 42)),
        shuffle=True
    )
    
    val_df, test_df = train_test_split(
        temp_df,
        test_size=0.5,
        random_state=config.get('system', {}).get('seed', config.get('training', {}).get('seed', 42)),
        shuffle=True
    )
    
    print(f"  ✓ Split: {len(train_df)} train, {len(val_df)} val, {len(test_df)} test")
    
    return train_df, val_df, test_df


if __name__ == '__main__':
    main()






