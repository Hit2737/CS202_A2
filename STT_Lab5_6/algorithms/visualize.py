import sys
import pandas as pd
import matplotlib.pyplot as plt

def visualize(csv_filename):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_filename)
    
    # Convert the Speedup column to numeric (if possible)
    df["Speedup"] = pd.to_numeric(df["Speedup"], errors='coerce')
    
    # Create a bar plot for speedup ratios
    plt.figure(figsize=(10, 6))
    plt.bar(df["Configuration"], df["Speedup"], color='skyblue')
    plt.xlabel("Test Configuration")
    plt.ylabel("Speedup (Tseq / Tpar)")
    plt.title("Speedup Ratios for Parallel Test Configurations")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    
    # Save the plot as an image and display it
    plt.savefig("speedup_plot.png")
    # plt.show()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python visualize.py <csv_filename>")
        sys.exit(1)
    
    csv_filename = sys.argv[1]
    visualize(csv_filename)
