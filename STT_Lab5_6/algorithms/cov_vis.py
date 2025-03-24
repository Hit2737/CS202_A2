import json, os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

with open('testBreport/status.json', 'r') as f:
    data = json.load(f)

os.makedirs('plotsB', exist_ok=True)

records = []
for file_key, file_info in data.get('files', {}).items():
    index = file_info.get('index', {})
    file_path = index.get('file', 'Unknown')
    nums = index.get('nums', {})
    n_statements = nums.get('n_statements', 0)
    n_missing = nums.get('n_missing', 0)
    coverage = ((n_statements - n_missing) / n_statements * 100) if n_statements > 0 else 0
    records.append({
        'file': file_path,
        'n_statements': n_statements,
        'n_missing': n_missing,
        'coverage': coverage
    })

df = pd.DataFrame(records)

plt.figure(figsize=(10, 6))
sns.kdeplot(df['coverage'], fill=True, color='blue')
plt.xlim(0, 100)
plt.title('Density Plot of Code Coverage Percentage')
plt.xlabel('Coverage Percentage (%)')
plt.ylabel('Density')
plt.savefig('plotsB/coverage_density_plot.png')
# plt.show()

plt.figure(figsize=(10, 6))
sns.histplot(df['coverage'], bins=20, kde=True, color='green')
plt.title('Histogram of Code Coverage Percentage')
plt.xlabel('Coverage Percentage (%)')
plt.ylabel('Frequency')
plt.savefig('plotsB/coverage_histogram.png')
# plt.show()