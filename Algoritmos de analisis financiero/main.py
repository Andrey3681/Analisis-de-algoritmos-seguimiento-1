import os
import sys

# Ensure modules resolve correctly when executed natively
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sorting.evaluator import load_data, evaluate_algorithms
from analysis.visualizer import plot_benchmark_results, get_top_15_volume_days

def run_project():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_dir, 'data', 'dataset_maestro.csv')
    
    if not os.path.exists(data_path):
        print(f"Data file not found at {data_path}. Please run run_etl.py first.")
        return
        
    print("Loading dataset maestro...")
    records = load_data(data_path)
    print(f"Loaded {len(records)} records successfully.")
    
    # Solve additional request: identify top 15 highest volume days
    get_top_15_volume_days(records)
    
    print("\nStarting Sorting Benchmark (Sample Size = 4096)")
    print("Please wait, O(N^2) algorithms will take some time to run...\n")
    
    results = evaluate_algorithms(records, sample_size=4096)
    
    chart_path = os.path.join(base_dir, 'sorting_benchmark.png')
    plot_benchmark_results(results, chart_path)

if __name__ == "__main__":
    run_project()
