#!/bin/bash

repos=("django" "matplotlib" "scikit-learn")

for repo in "${repos[@]}"; do
    echo "Processing repository: $repo"
    
    cd "$repo" || { echo "Failed to enter $repo"; continue; }
    
    rm -rf bandit_reports
    mkdir -p bandit_reports

    git log --first-parent --no-merges -n 100 --pretty=format:"%H" --reverse | awk '1; END {print ""}' > commits.txt

    counter=1

    while read commit; do
        [ -z "$commit" ] && continue
        [ ${#commit} -ne 40 ] && continue

        git checkout -f "$commit"

        printf -v seq_num "%03d" $counter

        bandit -r . -f json -x ./tests -o "bandit_reports/bandit_${seq_num}_${commit:0:7}.json"

        ((counter++))
    done < commits.txt

    # Clean up
    cd ..
    
    echo "Completed processing: $repo"
    echo "----------------------------------"
done