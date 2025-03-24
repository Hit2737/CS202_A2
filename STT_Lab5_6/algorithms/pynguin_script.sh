#!/bin/bash

MODULE_DIR="algorithms/$1"
OUTPUT_DIR="testsB"

mkdir -p $OUTPUT_DIR

find $MODULE_DIR -type f -name "*.py" | while read -r file; do
    module_path=$(dirname "$file")
    module_name=$(basename "$file" .py)
    
    echo "Running Pynguin for module $module_name"
    pynguin --project-path="$module_path" --module-name="$module_name" --output-path="$OUTPUT_DIR" --export-strategy=PY_TEST
done