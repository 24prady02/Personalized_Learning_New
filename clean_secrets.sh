#!/bin/bash
# Comprehensive script to remove all API keys from git history

# Find and replace all Groq API keys (gsk_...) in all text files
find . -type f \( -name "*.py" -o -name "*.yaml" -o -name "*.yml" -o -name "*.md" -o -name "*.txt" -o -name "*.json" \) ! -path "./.git/*" ! -name "clean_secrets.sh" ! -name "remove_secrets.sh" | while read file; do
    if [ -f "$file" ]; then
        # Replace gsk_... patterns with placeholder
        sed -i.bak 's/gsk_[A-Za-z0-9_-]*/YOUR_GROQ_API_KEY_HERE/g' "$file" 2>/dev/null
        # Also replace any hardcoded API key assignments
        sed -i.bak 's/api_key\s*=\s*"gsk_[^"]*"/api_key = os.getenv("GROQ_API_KEY", "")/g' "$file" 2>/dev/null
        sed -i.bak "s/api_key\s*=\s*'gsk_[^']*'/api_key = os.getenv('GROQ_API_KEY', '')/g" "$file" 2>/dev/null
        sed -i.bak 's/groq_api_key\s*=\s*"gsk_[^"]*"/groq_api_key = os.getenv("GROQ_API_KEY", "")/g' "$file" 2>/dev/null
        sed -i.bak "s/groq_api_key\s*=\s*'gsk_[^']*'/groq_api_key = os.getenv('GROQ_API_KEY', '')/g" "$file" 2>/dev/null
        # Remove backup files
        rm -f "$file.bak" 2>/dev/null
    fi
done

