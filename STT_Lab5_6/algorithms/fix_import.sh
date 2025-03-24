#!/bin/bash

# Directory containing the Python files
DIRECTORY="testsB"

find "$DIRECTORY" -name "*.py" | while read -r file; do
    # Update the import statements
    sed -i 's/import \(.*\) as module_/from algorithms.tree import \1 as module_/' "$file"
    
    # Change filename
    dir=$(dirname "$file")
    filename=$(basename "$file" .py)
    mv "$file" "$dir/${filename}_B.py"
done