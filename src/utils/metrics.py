"""
Evaluation metrics for the personalized learning system
"""

import torch
import numpy as np
from typing import Dict, List
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, roc_auc_score


class MetricsCalculator:
    """
    Calculate evaluation metrics for different tasks
    """
    
    @staticmethod
    def misconception_metrics(predictions: torch.Tensor, 
                             targets: torch.Tensor) -> Dict[str, float]:
        """
        Metrics for misconception classification (multi-label)
        
        Args:
            predictions: [batch, num_misconceptions] - probabilities
            targets: [batch, num_misconceptions] - binary labels
            
        Returns:
            Dictionary with metrics
        """
        # Convert to numpy
        preds_np = (predictions > 0.5).cpu().numpy()
        targets_np = targets.cpu().numpy()
        
        # Accuracy
        accuracy = accuracy_score(targets_np.flatten(), preds_np.flatten())
        
        # Precision, Recall, F1
        precision, recall, f1, _ = precision_recall_fscore_support(
            targets_np, preds_np, average='weighted', zero_division=0
        )
        
        # AUC
        try:
            auc = roc_auc_score(targets_np, predictions.cpu().numpy(), average='weighted')
        except:
            auc = 0.0
        
        return {
            'accuracy': float(accuracy),
            'precision': float(precision),
            'recall': float(recall),
            'f1': float(f1),
            'auc': float(auc)
        }
    
    @staticmethod
    def mastery_metrics(predictions: torch.Tensor,
                       targets: torch.Tensor) -> Dict[str, float]:
        """
        Metrics for mastery prediction (regression)
        
        Args:
            predictions: [batch, num_concepts] - mastery probabilities
            targets: [batch, num_concepts] - true mastery
            
        Returns:
            Dictionary with metrics
        """
        # MSE
        mse = torch.mean((predictions - targets) ** 2).item()
        
        # MAE
        mae = torch.mean(torch.abs(predictions - targets)).item()
        
        # RMSE
        rmse = np.sqrt(mse)
        
        # Correlation
        preds_np = predictions.cpu().numpy().flatten()
        targets_np = targets.cpu().numpy().flatten()
        
        if len(preds_np) > 1:
            correlation = np.corrcoef(preds_np, targets_np)[0, 1]
        else:
            correlation = 0.0
        
        return {
            'mse': float(mse),
            'mae': float(mae),
            'rmse': float(rmse),
            'correlation': float(correlation)
        }
    
    @staticmethod
    def emotion_metrics(predictions: torch.Tensor,
                       targets: torch.Tensor) -> Dict[str, float]:
        """
        Metrics for emotional state classification
        
        Args:
            predictions: [batch, num_emotions] - logits or probabilities
            targets: [batch] - class indices
            
        Returns:
            Dictionary with metrics
        """
        # Get predicted classes
        pred_classes = torch.argmax(predictions, dim=-1)
        
        # Convert to numpy
        preds_np = pred_classes.cpu().numpy()
        targets_np = targets.cpu().numpy()
        
        # Accuracy
        accuracy = accuracy_score(targets_np, preds_np)
        
        # Precision, Recall, F1
        precision, recall, f1, _ = precision_recall_fscore_support(
            targets_np, preds_np, average='macro', zero_division=0
        )
        
        return {
            'accuracy': float(accuracy),
            'precision': float(precision),
            'recall': float(recall),
            'f1': float(f1)
        }
    
    @staticmethod
    def intervention_metrics(recommended: List[str],
                           successful: List[str]) -> Dict[str, float]:
        """
        Metrics for intervention recommendation
        
        Args:
            recommended: List of recommended intervention types
            successful: List of successful intervention types
            
        Returns:
            Dictionary with metrics
        """
        # Success rate
        if not recommended:
            return {'success_rate': 0.0, 'match_rate': 0.0}
        
        matches = sum(1 for r in recommended if r in successful)
        success_rate = matches / len(recommended)
        
        # Match rate (how many successful were recommended)
        if successful:
            match_rate = matches / len(successful)
        else:
            match_rate = 0.0
        
        return {
            'success_rate': float(success_rate),
            'match_rate': float(match_rate)
        }




















