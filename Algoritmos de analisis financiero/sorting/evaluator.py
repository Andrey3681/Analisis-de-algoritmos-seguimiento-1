import csv
import random
import time
import copy
from typing import List

from sorting.models import Record
from Algoritmos.ListaAlgoritmos import (
    tim_sort, comb_sort, selection_sort, tree_sort,
    pigeonhole_sort, bucket_sort, quick_sort, heap_sort,
    bitonic_sort, gnome_sort, binary_insertion_sort, radix_sort
)

def unified_int_key(record: Record) -> int:
    """ Maps date and close price to a large integer keeping ordinality. """
    return record.date_int * 10000000 + record.close_int

def load_data(filepath: str) -> List[Record]:
    records = []
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            records.append(Record(
                symbol=row['Symbol'],
                date_str=row['Date'],
                open_p=row['Open'],
                high=row['High'],
                low=row['Low'],
                close_p=row['Close'],
                volume=row['Volume']
            ))
    return records

def evaluate_algorithms(records: List[Record], sample_size: int = 4096):
    """
    Evaluates algorithmic performance.
    Sample size is explicitly a power of 2 (4096) to satisfy Bitonic Sort's strict logic
    while keeping O(N^2) sorts within a manageable execution timeframe.
    """
    random.seed(42)  # For reproducibility
    sample = random.sample(records, min(sample_size, len(records)))
    
    results = {}
    
    print(f"Benchmarking with array size: {len(sample)}")

    # Array of algorithms strictly following the assignment list
    # Mapping algorithm name to the function and any specific kwargs needed
    algos = [
        ("TimSort", tim_sort, {}),
        ("Comb Sort", comb_sort, {}),
        ("Selection Sort", selection_sort, {}),
        ("Tree Sort", tree_sort, {}),
        ("Pigeonhole Sort", pigeonhole_sort, {'key': lambda x: x.date_int}), # Range must be small
        ("Bucket Sort", bucket_sort, {'key': unified_int_key}),
        ("QuickSort", quick_sort, {}),
        ("HeapSort", heap_sort, {}),
        ("Bitonic Sort", bitonic_sort, {}),
        ("Gnome Sort", gnome_sort, {}),
        ("Binary Insertion Sort", binary_insertion_sort, {}),
        ("RadixSort", radix_sort, {'key': unified_int_key})
    ]
    
    for name, func, kwargs in algos:
        arr = copy.deepcopy(sample)
        t0 = time.perf_counter()
        func(arr, **kwargs) if kwargs else func(arr)
        t1 = time.perf_counter()
        elapsed = t1 - t0
        results[name] = elapsed
        print(f"[{name}] > {elapsed:.4f}s")
        
    return results
