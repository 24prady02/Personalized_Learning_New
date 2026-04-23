"""
Evaluate Response Quality and Calculate Accuracy Metrics
Analyzes test outputs and calculates various accuracy metrics
"""

import os
import json
from typing import Dict, List
from datetime import datetime
import re


class ResponseEvaluator:
    """Evaluates response quality and calculates metrics"""
    
    def __init__(self):
        self.metrics = {}
    
    def check_concept_coverage(self, response: str, expected_concepts: List[str]) -> Dict:
        """Check if response covers expected concepts"""
        response_lower = response.lower()
        
        found_concepts = []
        missing_concepts = []
        
        for concept in expected_concepts:
            # Check for concept mentions (with variations)
            concept_variations = [
                concept.lower(),
                concept.replace('_', ' ').lower(),
                concept.replace('_', '-').lower()
            ]
            
            found = any(var in response_lower for var in concept_variations)
            if found:
                found_concepts.append(concept)
            else:
                missing_concepts.append(concept)
        
        coverage = len(found_concepts) / len(expected_concepts) if expected_concepts else 0
        
        return {
            'coverage': coverage,
            'found_concepts': found_concepts,
            'missing_concepts': missing_concepts,
            'total_expected': len(expected_concepts),
            'total_found': len(found_concepts)
        }
    
    def check_error_identification(self, response: str, expected_errors: List[str]) -> Dict:
        """Check if response identifies expected errors"""
        if not expected_errors:
            return {
                'coverage': 1.0,
                'found_errors': [],
                'missing_errors': [],
                'total_expected': 0,
                'total_found': 0
            }
        
        response_lower = response.lower()
        
        found_errors = []
        missing_errors = []
        
        error_keywords = {
            'missing_base_case': ['base case', 'base condition', 'termination'],
            'recursion_error': ['recursion', 'infinite', 'stack overflow'],
            'null_pointer_exception': ['null', 'none', 'empty', 'pointer'],
            'empty_list_handling': ['empty', 'null', 'none', 'check'],
            'initialization_error': ['initialize', 'initial', 'starting value'],
            'off_by_one': ['off by one', 'boundary', 'index'],
            'name_error': ['not defined', 'name error', 'undefined'],
            'scope_issue': ['scope', 'local', 'global', 'parameter'],
            'infinite_loop': ['infinite loop', 'never stops', 'endless'],
            'missing_increment': ['increment', 'decrement', 'update', 'change'],
            'type_error': ['type', 'string', 'integer', 'convert'],
            'implicit_conversion': ['convert', 'type', 'cast'],
            'index_out_of_bounds': ['index', 'out of bounds', 'range'],
            'empty_array': ['empty', 'length', 'size'],
            'syntax_error': ['syntax', 'invalid', 'error'],
            'assignment_in_condition': ['assignment', 'comparison', '==', '='],
            'logical_error': ['logic', 'wrong', 'incorrect'],
            'mutation_during_iteration': ['modify', 'mutate', 'change', 'iteration']
        }
        
        for error in expected_errors:
            keywords = error_keywords.get(error, [error.replace('_', ' ')])
            found = any(keyword in response_lower for keyword in keywords)
            
            if found:
                found_errors.append(error)
            else:
                missing_errors.append(error)
        
        coverage = len(found_errors) / len(expected_errors) if expected_errors else 0
        
        return {
            'coverage': coverage,
            'found_errors': found_errors,
            'missing_errors': missing_errors,
            'total_expected': len(expected_errors),
            'total_found': len(found_errors)
        }
    
    def check_response_quality(self, response: str) -> Dict:
        """Check general response quality metrics"""
        word_count = len(response.split())
        char_count = len(response)
        
        # Check for code examples
        has_code_example = '```' in response or 'def ' in response or 'class ' in response
        
        # Check for explanations
        explanation_indicators = ['because', 'reason', 'why', 'explain', 'means', 'when']
        has_explanation = any(indicator in response.lower() for indicator in explanation_indicators)
        
        # Check for solutions/fixes
        solution_indicators = ['fix', 'solution', 'correct', 'should', 'change', 'modify']
        has_solution = any(indicator in response.lower() for indicator in solution_indicators)
        
        # Check structure (paragraphs, lists)
        has_structure = '\n\n' in response or '\n-' in response or '\n*' in response or '\n1.' in response
        
        return {
            'word_count': word_count,
            'char_count': char_count,
            'has_code_example': has_code_example,
            'has_explanation': has_explanation,
            'has_solution': has_solution,
            'has_structure': has_structure,
            'quality_score': sum([
                has_code_example,
                has_explanation,
                has_solution,
                has_structure,
                word_count > 50,  # Substantial response
                word_count < 1000  # Not too verbose
            ]) / 6.0
        }
    
    def check_emotion_detection_accuracy(self, detected_emotion: str, expected_emotion: str) -> Dict:
        """Check if emotion was detected correctly"""
        emotion_mapping = {
            'confused': ['confused', 'unclear', 'don\'t understand'],
            'frustrated': ['frustrated', 'stuck', 'error', 'fail'],
            'neutral': ['neutral', 'normal', 'okay'],
            'engaged': ['understand', 'got it', 'clear']
        }
        
        # Normalize emotions
        detected_lower = detected_emotion.lower()
        expected_lower = expected_emotion.lower()
        
        # Check if detected emotion matches expected
        exact_match = detected_lower == expected_lower
        
        # Check if detected emotion is in the same category
        detected_category = None
        expected_category = None
        
        for category, keywords in emotion_mapping.items():
            if any(kw in detected_lower for kw in keywords):
                detected_category = category
            if any(kw in expected_lower for kw in keywords):
                expected_category = category
        
        category_match = detected_category == expected_category if detected_category and expected_category else False
        
        return {
            'exact_match': exact_match,
            'category_match': category_match,
            'detected': detected_emotion,
            'expected': expected_emotion,
            'accuracy': 1.0 if exact_match else (0.5 if category_match else 0.0)
        }
    
    def evaluate_scenario(self, result: Dict) -> Dict:
        """Evaluate a single scenario result"""
        scenario_id = result.get('scenario_id')
        output = result.get('output', {})
        expected = result.get('expected', {})
        input_data = result.get('input', {})
        
        response = output.get('response', '')
        analysis = output.get('analysis', {})
        
        # Concept coverage
        concept_coverage = self.check_concept_coverage(
            response,
            expected.get('concepts', [])
        )
        
        # Error identification
        error_coverage = self.check_error_identification(
            response,
            expected.get('errors', [])
        )
        
        # Response quality
        quality_metrics = self.check_response_quality(response)
        
        # Emotion detection
        detected_emotion = analysis.get('emotion', 'neutral')
        expected_emotion = input_data.get('student_state', {}).get('emotion', 'neutral')
        emotion_accuracy = self.check_emotion_detection_accuracy(
            detected_emotion,
            expected_emotion
        )
        
        # Overall score
        overall_score = (
            concept_coverage['coverage'] * 0.4 +
            error_coverage['coverage'] * 0.3 +
            quality_metrics['quality_score'] * 0.2 +
            emotion_accuracy['accuracy'] * 0.1
        )
        
        return {
            'scenario_id': scenario_id,
            'overall_score': overall_score,
            'concept_coverage': concept_coverage,
            'error_coverage': error_coverage,
            'quality_metrics': quality_metrics,
            'emotion_accuracy': emotion_accuracy,
            'response_length': len(response)
        }
    
    def evaluate_all(self, results: List[Dict]) -> Dict:
        """Evaluate all scenario results and calculate aggregate metrics"""
        
        evaluations = []
        for result in results:
            if 'error' not in result:
                eval_result = self.evaluate_scenario(result)
                evaluations.append(eval_result)
        
        if not evaluations:
            return {'error': 'No valid results to evaluate'}
        
        # Aggregate metrics
        total_scenarios = len(evaluations)
        
        avg_overall_score = sum(e['overall_score'] for e in evaluations) / total_scenarios
        avg_concept_coverage = sum(e['concept_coverage']['coverage'] for e in evaluations) / total_scenarios
        avg_error_coverage = sum(e['error_coverage']['coverage'] for e in evaluations) / total_scenarios
        avg_quality_score = sum(e['quality_metrics']['quality_score'] for e in evaluations) / total_scenarios
        avg_emotion_accuracy = sum(e['emotion_accuracy']['accuracy'] for e in evaluations) / total_scenarios
        
        # Count scenarios by score ranges
        excellent = sum(1 for e in evaluations if e['overall_score'] >= 0.8)
        good = sum(1 for e in evaluations if 0.6 <= e['overall_score'] < 0.8)
        fair = sum(1 for e in evaluations if 0.4 <= e['overall_score'] < 0.6)
        poor = sum(1 for e in evaluations if e['overall_score'] < 0.4)
        
        return {
            'timestamp': datetime.now().isoformat(),
            'total_scenarios': total_scenarios,
            'aggregate_metrics': {
                'average_overall_score': avg_overall_score,
                'average_concept_coverage': avg_concept_coverage,
                'average_error_coverage': avg_error_coverage,
                'average_quality_score': avg_quality_score,
                'average_emotion_accuracy': avg_emotion_accuracy
            },
            'score_distribution': {
                'excellent (>=0.8)': excellent,
                'good (0.6-0.8)': good,
                'fair (0.4-0.6)': fair,
                'poor (<0.4)': poor
            },
            'individual_evaluations': evaluations
        }


def load_results(output_dir="test_outputs"):
    """Load all test results from output directory"""
    results = []
    
    summary_file = os.path.join(output_dir, 'all_results_summary.json')
    if os.path.exists(summary_file):
        with open(summary_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            results = data.get('results', [])
    else:
        # Load individual files
        for filename in os.listdir(output_dir):
            if filename.endswith('_output.json'):
                filepath = os.path.join(output_dir, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    results.append(json.load(f))
    
    return results


def print_evaluation_report(evaluation: Dict):
    """Print a formatted evaluation report"""
    print("\n" + "="*80)
    print("📊 EVALUATION REPORT")
    print("="*80)
    
    agg = evaluation.get('aggregate_metrics', {})
    dist = evaluation.get('score_distribution', {})
    
    print(f"\nTotal Scenarios Evaluated: {evaluation.get('total_scenarios', 0)}")
    
    print("\n📈 Aggregate Metrics:")
    print(f"   Overall Score:        {agg.get('average_overall_score', 0):.2%}")
    print(f"   Concept Coverage:     {agg.get('average_concept_coverage', 0):.2%}")
    print(f"   Error Coverage:       {agg.get('average_error_coverage', 0):.2%}")
    print(f"   Quality Score:        {agg.get('average_quality_score', 0):.2%}")
    print(f"   Emotion Accuracy:     {agg.get('average_emotion_accuracy', 0):.2%}")
    
    print("\n📊 Score Distribution:")
    for range_name, count in dist.items():
        print(f"   {range_name}: {count}")
    
    print("\n" + "="*80)


if __name__ == "__main__":
    import sys
    
    output_dir = sys.argv[1] if len(sys.argv) > 1 else "test_outputs"
    
    print("Loading test results...")
    results = load_results(output_dir)
    
    if not results:
        print(f"❌ No results found in {output_dir}")
        print("   Run test_scenarios.py first to generate results")
        sys.exit(1)
    
    print(f"✅ Loaded {len(results)} results")
    
    print("\nEvaluating responses...")
    evaluator = ResponseEvaluator()
    evaluation = evaluator.evaluate_all(results)
    
    # Print report
    print_evaluation_report(evaluation)
    
    # Save evaluation
    eval_file = os.path.join(output_dir, 'evaluation_report.json')
    with open(eval_file, 'w', encoding='utf-8') as f:
        json.dump(evaluation, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Evaluation saved to: {eval_file}")

















