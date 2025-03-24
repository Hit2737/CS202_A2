import subprocess
import time
import re
import statistics
import csv
import os

def run_pytest(cmd):
    """
    Runs pytest with the given command list.
    Returns a tuple: (elapsed_time, failure_count, list_of_failed_tests)
    """
    start_time = time.time()
    proc = subprocess.run(cmd, capture_output=True, text=True)
    elapsed = time.time() - start_time
    output = proc.stdout + proc.stderr

    # Extract failure count from lines like "== 0 failed" or "0 failed"
    failure_count = 0
    m = re.search(r"==\s+(\d+)\s+failed", output)
    if m:
        failure_count = int(m.group(1))
    else:
        m = re.search(r"(\d+)\s+failed", output)
        if m:
            failure_count = int(m.group(1))

    # Extract names of failing tests (if printed with the "FAILED" prefix)
    failed_tests = []
    for line in output.splitlines():
        if line.startswith("FAILED"):
            parts = line.split("::")
            if parts:
                test_name = parts[0].replace("FAILED", "").strip()
                failed_tests.append(test_name)
    return elapsed, failure_count, failed_tests

def compute_Tseq(num_runs=5):
    print("\n=== Running Sequential Tests for Timing Measurement ===")
    times = []
    for i in range(num_runs):
        print(f"Timing run {i+1}/{num_runs}")
        elapsed, failures, _ = run_pytest(["pytest", "tests/"])
        if failures != 0:
            print("WARNING: Failures detected in a timing run; expected a stable suite.")
        times.append(elapsed)
        print(f"  Time: {elapsed:.2f} sec")
    Tseq = statistics.mean(times)
    print(f"\nAverage Sequential Execution Time (Tseq) over {num_runs} runs: {Tseq:.2f} sec")
    return Tseq

def run_parallel_tests():
    print("\n=== Running Parallel Test Executions ===")
    n_values = ["1", "auto"]
    parallel_threads_values = ["1", "auto"]
    dist_modes = ["load", "no"]
    
    configurations = []
    for n in n_values:
        for pt in parallel_threads_values:
            for dist in dist_modes:
                name = f"xdist -n {n}, --dist {dist} | run-parallel --parallel-threads {pt}"
                cmd = ["pytest", "-n", n, "--dist", dist, "--parallel-threads", pt, "tests/"]
                configurations.append({"name": name, "cmd": cmd})
    
    repetitions = 3
    results = {}
    
    for config in configurations:
        print(f"\nConfiguration: {config['name']}")
        times = []
        failure_counts = []
        all_failed_tests = []
        for i in range(repetitions):
            print(f"  Parallel run {i+1}/{repetitions}")
            elapsed, failures, failed_tests = run_pytest(config["cmd"])
            times.append(elapsed)
            failure_counts.append(failures)
            all_failed_tests.extend(failed_tests)
            print(f"\tTime: {elapsed:.2f} sec | Failures: {failures}")
        avg_time = statistics.mean(times)
        results[config["name"]] = {
            "Tpar": avg_time,
            "times": times,
            "failure_counts": failure_counts,
            "failing_tests": list(set(all_failed_tests))  # unique test names
        }
        print(f"  => Average Time for '{config['name']}': {avg_time:.2f} sec")
    return results

def write_execution_matrix(Tseq, parallel_results, filename="execution_matrix.csv"):
    print(f"\nWriting execution matrix to '{filename}'...")
    with open(filename, mode='w', newline='') as csvfile:
        fieldnames = ["Configuration", "Avg_Time_sec", "Speedup", "Failure_Counts", "Failing_Tests"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for config, data in parallel_results.items():
            Tpar = data["Tpar"]
            speedup = Tseq / Tpar if Tpar > 0 else "N/A"
            writer.writerow({
                "Configuration": config,
                "Avg_Time_sec": f"{Tpar:.2f}",
                "Speedup": f"{speedup:.2f}" if speedup != "N/A" else "N/A",
                "Failure_Counts": str(data["failure_counts"]),
                "Failing_Tests": ", ".join(data["failing_tests"])
            })
    print("Execution matrix written successfully.")

def call_visualization_script(csv_filename):
    if os.path.exists("visualize.py"):
        print("\nCalling visualization script...")
        subprocess.run(["python", "visualize.py", csv_filename])
    else:
        print("\nVisualization script 'visualize.py' not found. Skipping visualization step.")

def main():
    Tseq = compute_Tseq(num_runs=5)
    parallel_results = run_parallel_tests()
    csv_filename = "execution_matrix.csv"
    write_execution_matrix(Tseq, parallel_results, filename=csv_filename)
    call_visualization_script(csv_filename)

    print("\n=== Final Summary ===")
    print(f"Average Sequential Time (Tseq): {Tseq:.2f} sec")
    for config, data in parallel_results.items():
        speedup = Tseq / data["Tpar"] if data["Tpar"] > 0 else 0
        print(f"{config}: Tpar = {data['Tpar']:.2f} sec | Speedup = {speedup:.2f} | Failure counts per run: {data['failure_counts']}")
        if data["failing_tests"]:
            print(f"  Failing tests: {', '.join(data['failing_tests'])}")
    print("=== End of Summary ===")

if __name__ == "__main__":
    main()
