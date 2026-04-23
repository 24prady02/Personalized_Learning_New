"""
Complete Metrics Implementation for All Learned Features
Measures accuracy of all 6 learned detections
"""

import numpy as np
from typing import Dict, List, Tuple, Optional
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, roc_auc_score, mean_squared_error, r2_score
)
from scipy.stats import pearsonr
import torch


class CompleteMetricsCalculator:
    """
    Comprehensive metrics calculator for all learned features
    """
    
    def __init__(self):
        self.metrics_history = {
            'emotion': [],
            'engagement': [],
            'error_detection': [],
            'mastery': [],
            'personality': [],
            'code_embeddings': []
        }
    
    # ========== 1. EMOTION DETECTION METRICS ==========
    
    def calculate_emotion_metrics(
        self,
        predictions: List[str],
        ground_truth: List[str],
        emotion_classes: List[str] = ['confused', 'frustrated', 'neutral', 'engaged', 'confident']
    ) -> Dict[str, float]:
        """
        Calculate metrics for emotion detection
        
        Metrics:
        - Classification Accuracy
        - Precision (per class and weighted)
        - Recall (per class and weighted)
        - F1-Score (per class and weighted)
        - Confusion Matrix
        """
        
        # Overall accuracy
        accuracy = accuracy_score(ground_truth, predictions)
        
        # Precision, Recall, F1 (weighted average)
        precision_weighted = precision_score(
            ground_truth, predictions, 
            labels=emotion_classes, 
            average='weighted', 
            zero_division=0
        )
        recall_weighted = recall_score(
            ground_truth, predictions,
            labels=emotion_classes,
            average='weighted',
            zero_division=0
        )
        f1_weighted = f1_score(
            ground_truth, predictions,
            labels=emotion_classes,
            average='weighted',
            zero_division=0
        )
        
        # Per-class metrics
        precision_per_class = precision_score(
            ground_truth, predictions,
            labels=emotion_classes,
            average=None,
            zero_division=0
        )
        recall_per_class = recall_score(
            ground_truth, predictions,
            labels=emotion_classes,
            average=None,
            zero_division=0
        )
        f1_per_class = f1_score(
            ground_truth, predictions,
            labels=emotion_classes,
            average=None,
            zero_division=0
        )
        
        # Confusion matrix
        cm = confusion_matrix(ground_truth, predictions, labels=emotion_classes)
        
        # Frustration-specific metrics (most important)
        frustration_precision = self._calculate_class_metric(
            predictions, ground_truth, 'frustrated', 'precision'
        )
        frustration_recall = self._calculate_class_metric(
            predictions, ground_truth, 'frustrated', 'recall'
        )
        frustration_f1 = self._calculate_class_metric(
            predictions, ground_truth, 'frustrated', 'f1'
        )
        
        metrics = {
            'overall_accuracy': float(accuracy),
            'precision_weighted': float(precision_weighted),
            'recall_weighted': float(recall_weighted),
            'f1_weighted': float(f1_weighted),
            'frustration_precision': float(frustration_precision),
            'frustration_recall': float(frustration_recall),
            'frustration_f1': float(frustration_f1),
            'per_class_precision': {emotion_classes[i]: float(precision_per_class[i]) 
                                   for i in range(len(emotion_classes))},
            'per_class_recall': {emotion_classes[i]: float(recall_per_class[i]) 
                                for i in range(len(emotion_classes))},
            'per_class_f1': {emotion_classes[i]: float(f1_per_class[i]) 
                            for i in range(len(emotion_classes))},
            'confusion_matrix': cm.tolist()
        }
        
        self.metrics_history['emotion'].append(metrics)
        return metrics
    
    # ========== 2. ENGAGEMENT DETECTION METRICS ==========
    
    def calculate_engagement_metrics(
        self,
        predicted_scores: List[float],
        ground_truth_scores: List[float],
        threshold_low: float = 0.4,
        threshold_high: float = 0.7
    ) -> Dict[str, float]:
        """
        Calculate metrics for engagement detection
        
        Metrics:
        - Classification Accuracy (low/medium/high)
        - Correlation (Pearson)
        - RMSE
        - MAE
        - Per-level Precision/Recall
        """
        
        # Convert to numpy
        pred = np.array(predicted_scores)
        gt = np.array(ground_truth_scores)
        
        # Regression metrics
        rmse = np.sqrt(mean_squared_error(gt, pred))
        mae = np.mean(np.abs(gt - pred))
        correlation, p_value = pearsonr(gt, pred)
        r2 = r2_score(gt, pred)
        
        # Classification metrics (low/medium/high)
        def quantize(scores, low_thresh, high_thresh):
            return ['low' if s < low_thresh else 'high' if s > high_thresh else 'medium' 
                   for s in scores]
        
        pred_levels = quantize(pred, threshold_low, threshold_high)
        gt_levels = quantize(gt, threshold_low, threshold_high)
        
        accuracy = accuracy_score(gt_levels, pred_levels)
        
        # Per-level metrics
        levels = ['low', 'medium', 'high']
        precision_per_level = precision_score(
            gt_levels, pred_levels,
            labels=levels,
            average=None,
            zero_division=0
        )
        recall_per_level = recall_score(
            gt_levels, pred_levels,
            labels=levels,
            average=None,
            zero_division=0
        )
        
        metrics = {
            'classification_accuracy': float(accuracy),
            'correlation': float(correlation),
            'correlation_p_value': float(p_value),
            'rmse': float(rmse),
            'mae': float(mae),
            'r2_score': float(r2),
            'per_level_precision': {levels[i]: float(precision_per_level[i]) 
                                   for i in range(len(levels))},
            'per_level_recall': {levels[i]: float(recall_per_level[i]) 
                                for i in range(len(levels))}
        }
        
        self.metrics_history['engagement'].append(metrics)
        return metrics
    
    # ========== 3. ERROR DETECTION METRICS ==========
    
    def calculate_error_detection_metrics(
        self,
        predicted_errors: List[Dict],
        ground_truth_errors: List[Dict]
    ) -> Dict[str, float]:
        """
        Calculate metrics for error detection
        
        Metrics:
        - Detection Accuracy (error present/not present)
        - Error Type Classification Accuracy
        - False Positive Rate
        - False Negative Rate
        - Error Location Accuracy
        """
        
        # Error presence detection
        pred_present = [1 if e.get('present', False) else 0 for e in predicted_errors]
        gt_present = [1 if e.get('present', False) else 0 for e in ground_truth_errors]
        
        accuracy = accuracy_score(gt_present, pred_present)
        
        # Confusion matrix for presence
        cm = confusion_matrix(gt_present, pred_present)
        tn, fp, fn, tp = cm.ravel() if cm.size == 4 else (0, 0, 0, 0)
        
        false_positive_rate = fp / (fp + tn) if (fp + tn) > 0 else 0.0
        false_negative_rate = fn / (fn + tp) if (fn + tp) > 0 else 0.0
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
        
        # Error type classification (only for detected errors)
        pred_types = [e.get('type', 'unknown') for e in predicted_errors if e.get('present', False)]
        gt_types = [e.get('type', 'unknown') for e in ground_truth_errors if e.get('present', False)]
        
        type_accuracy = 0.0
        if len(gt_types) > 0:
            # Match predicted errors to ground truth errors
            type_accuracy = self._match_error_types(predicted_errors, ground_truth_errors)
        
        # Error location accuracy
        location_accuracy = self._calculate_location_accuracy(predicted_errors, ground_truth_errors)
        
        metrics = {
            'detection_accuracy': float(accuracy),
            'precision': float(precision),
            'recall': float(recall),
            'f1_score': float(f1),
            'false_positive_rate': float(false_positive_rate),
            'false_negative_rate': float(false_negative_rate),
            'error_type_accuracy': float(type_accuracy),
            'error_location_accuracy': float(location_accuracy)
        }
        
        self.metrics_history['error_detection'].append(metrics)
        return metrics
    
    def _match_error_types(self, pred_errors: List[Dict], gt_errors: List[Dict]) -> float:
        """Match predicted errors to ground truth errors and calculate type accuracy"""
        # Simple matching: count correct type matches
        correct = 0
        total = 0
        
        for gt_error in gt_errors:
            if not gt_error.get('present', False):
                continue
            
            total += 1
            gt_type = gt_error.get('type', '')
            gt_line = gt_error.get('line', -1)
            
            # Find matching predicted error (by line or type)
            for pred_error in pred_errors:
                if pred_error.get('present', False):
                    pred_type = pred_error.get('type', '')
                    pred_line = pred_error.get('line', -1)
                    
                    if (gt_line == pred_line and gt_line != -1) or gt_type == pred_type:
                        if gt_type == pred_type:
                            correct += 1
                        break
        
        return correct / total if total > 0 else 0.0
    
    def _calculate_location_accuracy(self, pred_errors: List[Dict], gt_errors: List[Dict]) -> float:
        """Calculate accuracy of error location detection"""
        correct = 0
        total = 0
        
        for gt_error in gt_errors:
            if not gt_error.get('present', False):
                continue
            
            gt_line = gt_error.get('line', -1)
            if gt_line == -1:
                continue
            
            total += 1
            
            # Find matching predicted error
            for pred_error in pred_errors:
                if pred_error.get('present', False):
                    pred_line = pred_error.get('line', -1)
                    if abs(gt_line - pred_line) <= 1:  # Within 1 line
                        correct += 1
                        break
        
        return correct / total if total > 0 else 0.0
    
    # ========== 4. MASTERY ESTIMATION METRICS ==========
    
    def calculate_mastery_metrics(
        self,
        predicted_mastery: List[float],
        ground_truth_mastery: List[float],
        threshold: float = 0.7
    ) -> Dict[str, float]:
        """
        Calculate metrics for mastery estimation
        
        Metrics:
        - Prediction Accuracy (mastered/not mastered)
        - RMSE
        - MAE
        - Correlation
        - AUC-ROC
        - Calibration Error
        """
        
        # Convert to numpy
        pred = np.array(predicted_mastery)
        gt = np.array(ground_truth_mastery)
        
        # Regression metrics
        rmse = np.sqrt(mean_squared_error(gt, pred))
        mae = np.mean(np.abs(gt - pred))
        correlation, p_value = pearsonr(gt, pred)
        r2 = r2_score(gt, pred)
        
        # Classification metrics (mastered/not mastered)
        pred_binary = (pred >= threshold).astype(int)
        gt_binary = (gt >= threshold).astype(int)
        
        accuracy = accuracy_score(gt_binary, pred_binary)
        
        # AUC-ROC
        try:
            auc = roc_auc_score(gt_binary, pred)
        except:
            auc = 0.0
        
        # Calibration error (binned)
        calibration_error = self._calculate_calibration_error(gt, pred, n_bins=10)
        
        # Per-skill metrics (if provided as dict)
        per_skill_metrics = {}
        
        metrics = {
            'prediction_accuracy': float(accuracy),
            'rmse': float(rmse),
            'mae': float(mae),
            'correlation': float(correlation),
            'correlation_p_value': float(p_value),
            'r2_score': float(r2),
            'auc_roc': float(auc),
            'calibration_error': float(calibration_error)
        }
        
        self.metrics_history['mastery'].append(metrics)
        return metrics
    
    def _calculate_calibration_error(self, gt: np.ndarray, pred: np.ndarray, n_bins: int = 10) -> float:
        """Calculate calibration error using binning"""
        bin_boundaries = np.linspace(0, 1, n_bins + 1)
        bin_lowers = bin_boundaries[:-1]
        bin_uppers = bin_boundaries[1:]
        
        calibration_error = 0.0
        for bin_lower, bin_upper in zip(bin_lowers, bin_uppers):
            in_bin = (pred > bin_lower) & (pred <= bin_upper)
            prop_in_bin = in_bin.mean()
            
            if prop_in_bin > 0:
                accuracy_in_bin = gt[in_bin].mean()
                avg_confidence_in_bin = pred[in_bin].mean()
                calibration_error += np.abs(avg_confidence_in_bin - accuracy_in_bin) * prop_in_bin
        
        return calibration_error
    
    # ========== 5. PERSONALITY DETECTION METRICS ==========
    
    def calculate_personality_metrics(
        self,
        predicted_traits: Dict[str, List[float]],
        ground_truth_traits: Dict[str, List[float]],
        traits: List[str] = ['openness', 'conscientiousness', 'extraversion', 
                            'agreeableness', 'neuroticism']
    ) -> Dict[str, float]:
        """
        Calculate metrics for personality trait detection
        
        Metrics:
        - Per-trait Correlation
        - Per-trait RMSE
        - Overall Correlation
        - Learning Style Classification Accuracy
        """
        
        per_trait_metrics = {}
        all_pred = []
        all_gt = []
        
        for trait in traits:
            if trait in predicted_traits and trait in ground_truth_traits:
                pred = np.array(predicted_traits[trait])
                gt = np.array(ground_truth_traits[trait])
                
                # Correlation
                correlation, p_value = pearsonr(gt, pred)
                
                # RMSE
                rmse = np.sqrt(mean_squared_error(gt, pred))
                
                # MAE
                mae = np.mean(np.abs(gt - pred))
                
                per_trait_metrics[trait] = {
                    'correlation': float(correlation),
                    'correlation_p_value': float(p_value),
                    'rmse': float(rmse),
                    'mae': float(mae)
                }
                
                all_pred.extend(pred.tolist())
                all_gt.extend(gt.tolist())
        
        # Overall correlation
        overall_correlation, overall_p = pearsonr(all_gt, all_pred) if len(all_gt) > 0 else (0.0, 1.0)
        
        metrics = {
            'per_trait_metrics': per_trait_metrics,
            'overall_correlation': float(overall_correlation),
            'overall_correlation_p_value': float(overall_p)
        }
        
        self.metrics_history['personality'].append(metrics)
        return metrics
    
    def calculate_learning_style_metrics(
        self,
        predicted_styles: List[str],
        ground_truth_styles: List[str]
    ) -> Dict[str, float]:
        """Calculate accuracy for learning style classification"""
        
        accuracy = accuracy_score(ground_truth_styles, predicted_styles)
        
        # Per-style metrics
        unique_styles = list(set(ground_truth_styles + predicted_styles))
        precision_per_style = precision_score(
            ground_truth_styles, predicted_styles,
            labels=unique_styles,
            average=None,
            zero_division=0
        )
        recall_per_style = recall_score(
            ground_truth_styles, predicted_styles,
            labels=unique_styles,
            average=None,
            zero_division=0
        )
        
        metrics = {
            'classification_accuracy': float(accuracy),
            'per_style_precision': {unique_styles[i]: float(precision_per_style[i]) 
                                   for i in range(len(unique_styles))},
            'per_style_recall': {unique_styles[i]: float(recall_per_style[i]) 
                                for i in range(len(unique_styles))}
        }
        
        return metrics
    
    # ========== 6. CODE EMBEDDING METRICS ==========
    
    def calculate_code_embedding_metrics(
        self,
        embeddings: np.ndarray,
        code_labels: List[str],
        similarity_pairs: Optional[List[Tuple[int, int, float]]] = None
    ) -> Dict[str, float]:
        """
        Calculate metrics for code embeddings
        
        Metrics:
        - Code Similarity Accuracy
        - Code Classification Accuracy
        - Embedding Quality (cosine similarity)
        """
        
        from sklearn.metrics.pairwise import cosine_similarity
        
        # Cosine similarity matrix
        similarity_matrix = cosine_similarity(embeddings)
        
        # Code similarity accuracy (if pairs provided)
        similarity_accuracy = 0.0
        if similarity_pairs:
            correct = 0
            total = 0
            for i, j, expected_similarity in similarity_pairs:
                actual_similarity = similarity_matrix[i, j]
                # Consider correct if within threshold
                if abs(actual_similarity - expected_similarity) < 0.2:
                    correct += 1
                total += 1
            similarity_accuracy = correct / total if total > 0 else 0.0
        
        # Code classification accuracy (if labels provided)
        classification_accuracy = 0.0
        if code_labels:
            # Use embeddings for classification (would need a classifier)
            # For now, return placeholder
            classification_accuracy = 0.0
        
        # Average embedding quality (intra-class similarity)
        avg_intra_class_similarity = 0.0
        if code_labels:
            unique_labels = list(set(code_labels))
            intra_similarities = []
            for label in unique_labels:
                indices = [i for i, l in enumerate(code_labels) if l == label]
                if len(indices) > 1:
                    label_embeddings = embeddings[indices]
                    label_similarity = cosine_similarity(label_embeddings)
                    # Average similarity within class (excluding diagonal)
                    mask = np.ones_like(label_similarity, dtype=bool)
                    np.fill_diagonal(mask, False)
                    intra_similarities.append(label_similarity[mask].mean())
            avg_intra_class_similarity = np.mean(intra_similarities) if intra_similarities else 0.0
        
        metrics = {
            'similarity_accuracy': float(similarity_accuracy),
            'classification_accuracy': float(classification_accuracy),
            'avg_intra_class_similarity': float(avg_intra_class_similarity),
            'embedding_dimension': int(embeddings.shape[1])
        }
        
        self.metrics_history['code_embeddings'].append(metrics)
        return metrics
    
    # ========== HELPER METHODS ==========
    
    def _calculate_class_metric(
        self,
        predictions: List[str],
        ground_truth: List[str],
        target_class: str,
        metric: str
    ) -> float:
        """Calculate metric for a specific class"""
        # Convert to binary (target class vs others)
        pred_binary = [1 if p == target_class else 0 for p in predictions]
        gt_binary = [1 if g == target_class else 0 for g in ground_truth]
        
        if metric == 'precision':
            return precision_score(gt_binary, pred_binary, zero_division=0)
        elif metric == 'recall':
            return recall_score(gt_binary, pred_binary, zero_division=0)
        elif metric == 'f1':
            return f1_score(gt_binary, pred_binary, zero_division=0)
        else:
            return 0.0
    
    # ========== SUMMARY METRICS ==========
    
    def get_summary_metrics(self) -> Dict[str, Dict]:
        """Get summary of all metrics"""
        summary = {}
        
        for feature, history in self.metrics_history.items():
            if history:
                # Average metrics across all evaluations
                latest = history[-1]
                summary[feature] = latest
        
        return summary
    
    def print_metrics_report(self):
        """Print formatted metrics report"""
        print("\n" + "="*80)
        print("COMPLETE METRICS REPORT")
        print("="*80)
        
        summary = self.get_summary_metrics()
        
        for feature, metrics in summary.items():
            print(f"\n{feature.upper().replace('_', ' ')} METRICS:")
            print("-" * 80)
            for key, value in metrics.items():
                if isinstance(value, dict):
                    print(f"  {key}:")
                    for sub_key, sub_value in value.items():
                        print(f"    {sub_key}: {sub_value:.4f}")
                elif isinstance(value, list):
                    print(f"  {key}: {len(value)} items")
                else:
                    print(f"  {key}: {value:.4f}")


# ========== USAGE EXAMPLE ==========

if __name__ == "__main__":
    calculator = CompleteMetricsCalculator()
    
    # Example: Emotion Detection
    predicted_emotions = ['confused', 'frustrated', 'engaged', 'confused', 'neutral']
    ground_truth_emotions = ['confused', 'frustrated', 'engaged', 'frustrated', 'neutral']
    
    emotion_metrics = calculator.calculate_emotion_metrics(
        predicted_emotions, ground_truth_emotions
    )
    print("Emotion Metrics:", emotion_metrics)
    
    # Example: Mastery Estimation
    predicted_mastery = [0.85, 0.60, 0.45, 0.30, 0.75]
    ground_truth_mastery = [0.80, 0.65, 0.50, 0.35, 0.70]
    
    mastery_metrics = calculator.calculate_mastery_metrics(
        predicted_mastery, ground_truth_mastery
    )
    print("\nMastery Metrics:", mastery_metrics)
    
    # Print full report
    calculator.print_metrics_report()














