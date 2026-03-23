#!/bin/bash
# Remove all Groq API keys from files

find . -type f \( -name "*.py" -o -name "*.yaml" -o -name "*.yml" \) ! -path "./.git/*" ! -name "remove_all_secrets.sh" ! -name "clean_secrets.sh" ! -name "remove_secrets.sh" | while read file; do
    if [ -f "$file" ]; then
        # Replace gsk_... patterns
        sed -i.bak 's/gsk_[A-Za-z0-9_-]*/YOUR_GROQ_API_KEY_HERE/g' "$file" 2>/dev/null
        # Replace hardcoded API key assignments with environment variable
        sed -i.bak 's/api_key = "gsk_[^"]*"/api_key = os.getenv("GROQ_API_KEY", "")/g' "$file" 2>/dev/null
        sed -i.bak "s/api_key = 'gsk_[^']*'/api_key = os.getenv('GROQ_API_KEY', '')/g" "$file" 2>/dev/null
        # Remove backup files
        rm -f "$file.bak" 2>/dev/null
    fi
done

