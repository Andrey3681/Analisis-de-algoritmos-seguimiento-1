import matplotlib.pyplot as plt

def plot_benchmark_results(results_dict, output_path="sorting_benchmark.png"):
    """
    Plots a horizontally oriented bar chart sorting by best performing algorithms.
    """
    sorted_items = sorted(results_dict.items(), key=lambda x: x[1])
    algos = [item[0] for item in sorted_items]
    times = [item[1] for item in sorted_items]
    
    plt.figure(figsize=(12, 8))
    bars = plt.barh(algos, times, color='skyblue')
    plt.xlabel('Time (Seconds)')
    plt.title('Sorting Algorithms Performance Comparison (Lower is Better)')
    plt.gca().invert_yaxis()  # Put fastest algorithm on top
    
    # Add text labels on the bars
    for bar in bars:
        width = bar.get_width()
        plt.text(width + max(times)*0.01, bar.get_y() + bar.get_height()/2, 
                 f'{width:.4f}s', va='center')
                 
    plt.tight_layout()
    plt.savefig(output_path)
    print(f"\nBenchmark chart generated and saved to {output_path}")

def get_top_15_volume_days(records):
    """
    Finds the top 15 highest volume records using our custom QuickSort implementation.
    Wraps the Record class temporarily to alter the < and <= logic for descending sort.
    """
    from Algoritmos.ListaAlgoritmos import quick_sort
    
    class VolumeWrapper:
        def __init__(self, record):
            self.r = record
        def __lt__(self, other):
            return self.r.volume > other.r.volume
        def __le__(self, other):
            return self.r.volume >= other.r.volume
            
    wrapped = [VolumeWrapper(r) for r in records]
    quick_sort(wrapped)
    
    top_15 = [w.r for w in wrapped[:15]]
    print("\nTop 15 días con mayor volumen de negociación:")
    print("-" * 60)
    for i, r in enumerate(top_15, 1):
        print(f"{i:2d}. {r.date_str} | {r.symbol:6s} | Volumen: {r.volume:,}")
    return top_15
