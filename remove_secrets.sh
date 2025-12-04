#!/bin/bash
# Script to remove API keys from git history

files=(
  "generate_complete_response_with_metrics.py"
  "test_all_knowledge_graphs_integration.py"
  "regenerate_all_conversations_with_groq.py"
  "FINAL_SYSTEM_WITH_BKT.py"
  "complete_system_with_nestor.py"
  "process_advanced_question.py"
  "run_feature_test_results_2.py"
  "run_personalization_tests.py"
)

for file in "${files[@]}"; do
  if [ -f "$file" ]; then
    # Replace Groq API keys (gsk_...) with placeholder
    sed -i.bak 's/gsk_[A-Za-z0-9_-]*/YOUR_GROQ_API_KEY_HERE/g' "$file"
    rm -f "$file.bak" 2>/dev/null
  fi
done


