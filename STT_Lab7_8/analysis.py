import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from collections import Counter

bandit_csv = 'django_bandit_report.csv'
matplotlib_csv = 'matplotlib_bandit_report.csv'
scikit_learn_csv = 'scikit-learn_bandit_report.csv'

# Read the CSV files into DataFrames
bandit_df = pd.read_csv(bandit_csv)
matplotlib_df = pd.read_csv(matplotlib_csv)
scikit_learn_df = pd.read_csv(scikit_learn_csv)

bandit_df['repo'] = 'django'
matplotlib_df['repo'] = 'matplotlib'
scikit_learn_df['repo'] = 'scikit-learn'

combined_df = pd.concat([bandit_df, matplotlib_df, scikit_learn_df], ignore_index=True)

cwe_counter = Counter()

for cwe_str in combined_df['unique_cwes'].dropna():
    cwe_list = [cwe.strip() for cwe in cwe_str.split(',') if cwe.strip()]
    cwe_counter.update(cwe_list)

cwe_df = pd.DataFrame.from_dict(cwe_counter, orient='index', columns=['Frequency'])
cwe_df = cwe_df.sort_values(by='Frequency', ascending=False).reset_index()
cwe_df.rename(columns={'index': 'CWE'}, inplace=True)

# Plot the frequency bar graph
plt.figure(figsize=(12, 8))
sns.barplot(x='CWE', y='Frequency', data=cwe_df, palette='viridis', hue='CWE', legend=False)
plt.xlabel("CWE")
plt.ylabel("Frequency")
plt.title("Overall Frequency of Unique CWEs Across Repositories")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig("overall_cwe_frequency.png")

repos = combined_df['repo'].unique()

for repo in repos:
    repo_df = combined_df[combined_df['repo'] == repo].reset_index(drop=True)
    repo_df['commit_index'] = repo_df.index + 1

    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    fig.suptitle(f"Severity Trends Over Commits for {repo.capitalize()}", fontsize=16)

    axes[0].plot(repo_df['commit_index'], repo_df['sev_high'], linestyle='-', color='r')
    axes[0].set_title("High Severity")
    axes[0].set_xlabel("Commit Number")
    axes[0].set_ylabel("Vulnerability Count")

    axes[1].plot(repo_df['commit_index'], repo_df['sev_medium'], linestyle='-', color='orange')
    axes[1].set_title("Medium Severity")
    axes[1].set_xlabel("Commit Number")

    axes[2].plot(repo_df['commit_index'], repo_df['sev_low'], linestyle='-', color='g')
    axes[2].set_title("Low Severity")
    axes[2].set_xlabel("Commit Number")

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.savefig(f"{repo}_severity_trends.png")
    # plt.show()

for repo in repos:
    repo_df = combined_df[combined_df['repo'] == repo].reset_index(drop=True)
    repo_df['commit_index'] = repo_df.index + 1

    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    fig.suptitle(f"Confidence Trends Over Commits for {repo.capitalize()}", fontsize=16)

    axes[0].plot(repo_df['commit_index'], repo_df['conf_high'], linestyle='-', color='r')
    axes[0].set_title("High Confidence")
    axes[0].set_xlabel("Commit Number")
    axes[0].set_ylabel("Vulnerability Count")

    axes[1].plot(repo_df['commit_index'], repo_df['conf_medium'], linestyle='-', color='orange')
    axes[1].set_title("Medium Confidence")
    axes[1].set_xlabel("Commit Number")

    axes[2].plot(repo_df['commit_index'], repo_df['conf_low'], linestyle='-', color='g')
    axes[2].set_title("Low Confidence")
    axes[2].set_xlabel("Commit Number")

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.savefig(f"{repo}_confidence_trends.png")
    # plt.show()