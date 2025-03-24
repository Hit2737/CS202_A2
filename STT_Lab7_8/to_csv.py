import json
import csv
import os
from glob import glob
import argparse

def process_bandit_report(filepath):
    with open(filepath, 'r') as f:
        data = json.load(f)
    
    results = data.get("results", [])
    conf_high = sum(1 for issue in results if issue.get("issue_confidence", "").upper() == "HIGH")
    conf_med = sum(1 for issue in results if issue.get("issue_confidence", "").upper() == "MEDIUM")
    conf_low = sum(1 for issue in results if issue.get("issue_confidence", "").upper() == "LOW")
    
    # Count severity levels.
    sev_high = sum(1 for issue in results if issue.get("issue_severity", "").upper() == "HIGH")
    sev_med = sum(1 for issue in results if issue.get("issue_severity", "").upper() == "MEDIUM")
    sev_low = sum(1 for issue in results if issue.get("issue_severity", "").upper() == "LOW")
    
    # Collect unique CWE IDs.
    cwe_set = set()
    for issue in results:
        cwe_info = issue.get("issue_cwe")
        if cwe_info and "id" in cwe_info:
            cwe_set.add(f"CWE-{cwe_info['id']}")
    unique_cwes = ", ".join(sorted(cwe_set))
    
    # Extract commit hash from the filename.
    # Assuming filename pattern: bandit_NUM_COMMIT.json (e.g., bandit_100_136a1e8.json)
    filename = os.path.basename(filepath)
    parts = filename.split('_')
    commit = parts[2].split('.')[0] if len(parts) >= 3 else ""
    
    return {
        "commit": commit,
        "conf_high": conf_high,
        "conf_medium": conf_med,
        "conf_low": conf_low,
        "sev_high": sev_high,
        "sev_medium": sev_med,
        "sev_low": sev_low,
        "unique_cwes": unique_cwes,
    }

def main():
    parser = argparse.ArgumentParser(description="Process Bandit JSON reports and aggregate results into a CSV file.")
    parser.add_argument("directory", help="Directory where the 'bandit_reports' folder is located.")
    args = parser.parse_args()

    report_dir = os.path.join(args.directory, "bandit_reports")
    json_files = sorted(glob(os.path.join(report_dir, "*.json")))
    if not json_files:
        print(f"No JSON report files found in the '{report_dir}' directory.")
        return
    
    output_file = os.path.join("./", f"{args.directory}_bandit_report.csv")
    
    with open(output_file, "w", newline="") as csvfile:
        fieldnames = [
            "commit",
            "conf_high",
            "conf_medium",
            "conf_low",
            "sev_high",
            "sev_medium",
            "sev_low",
            "unique_cwes"
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for jf in json_files:
            row = process_bandit_report(jf)
            writer.writerow(row)
            print(f"Processed {os.path.basename(jf)}")
            
    print(f"Aggregated CSV report generated as '{output_file}'.")

if __name__ == "__main__":
    main()
