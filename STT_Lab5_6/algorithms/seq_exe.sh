#!/bin/bash

total_time=0
for i in {1..5}
do
    echo "Running test suite iteration $i..."
    start_time=$(date +%s)
    pytest
    end_time=$(date +%s)
    duration=$((end_time - start_time))
    total_time=$((total_time + duration))
    echo "Iteration $i execution time: $duration seconds"
done

avg_time=$((total_time / 5))
echo "Average execution time (Tseq): $avg_time seconds"
