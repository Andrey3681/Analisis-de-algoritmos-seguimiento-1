from typing import List, Any
import sys
sys.setrecursionlimit(20000)

MIN_MERGE = 32

# Calcula la logitud minima en el que se divide el arreglo para ordenarlo
def calcularMinRun(tamañoArreglo: int) -> int:
    reciduo = 0
    while tamañoArreglo >= MIN_MERGE:
        reciduo |= tamañoArreglo & 1
        tamañoArreglo >>= 1
    return tamañoArreglo + reciduo

# Ordena el arreglo desde 'left' hasta 'right' usando Insertion Sort. (menor a mayor)
def OrdenarArregloLtoR(arreglo: List[Any], left: int, right: int) -> None:
    for i in range(left + 1, right + 1):
        temp = arreglo[i]
        j = i - 1
        while j >= left and arreglo[j] > temp:
            arreglo[j + 1] = arreglo[j]
            j -= 1
        arreglo[j + 1] = temp


def _merge(arreglo: List[Any], l: int, m: int, r: int) -> None:
    """Combina dos subarrays ordenados."""
    len1, len2 = m - l + 1, r - m
    left, right = [], []
    for i in range(0, len1):
        left.append(arreglo[l + i])
    for i in range(0, len2):
        right.append(arreglo[m + 1 + i])

    i, j, k = 0, 0, l

    while i < len1 and j < len2:
        if left[i] <= right[j]:
            arreglo[k] = left[i]
            i += 1
        else:
            arreglo[k] = right[j]
            j += 1
        k += 1

    while i < len1:
        arreglo[k] = left[i]
        k += 1
        i += 1

    while j < len2:
        arreglo[k] = right[j]
        k += 1
        j += 1

# 1. Tim Sort
def tim_sort(arreglo: List[Any]) -> List[Any]:
    """
    Método de ordenamiento TimSort.
    Ordena el arreglo in-place y lo devuelve.
    """
    if not arreglo:
        return arreglo
    
    n = len(arreglo)
    min_run = calcularMinRun(n)

    # Ordenar subarrays individuales de tamaño min_run
    for start in range(0, n, min_run):
        end = min(start + min_run - 1, n - 1)
        OrdenarArregloLtoR(arreglo, start, end)

    # Combinar los subarrays ordenados
    size = min_run
    while size < n:
        for left in range(0, n, 2 * size):
            mid = min(n - 1, left + size - 1)
            right = min((left + 2 * size - 1), (n - 1))
            if mid < right:
                _merge(arreglo, left, mid, right)
        size *= 2
        
    return arreglo


# 2. Comb Sort
def comb_sort(arreglo: List[Any]) -> List[Any]:
    n = len(arreglo)
    gap = n
    shrink = 1.3
    sorted_flag = False

    while gap > 1 or not sorted_flag:
        gap = max(1, int(gap / shrink))
        sorted_flag = True
        for i in range(n - gap):
            if arreglo[i] > arreglo[i + gap]:
                arreglo[i], arreglo[i + gap] = arreglo[i + gap], arreglo[i]
                sorted_flag = False
    return arreglo


# 3. Selection Sort
def selection_sort(arreglo: List[Any]) -> List[Any]:
    n = len(arreglo)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arreglo[j] < arreglo[min_idx]:
                min_idx = j
        arreglo[i], arreglo[min_idx] = arreglo[min_idx], arreglo[i]
    return arreglo


# 4. Tree Sort
class TreeNode:
    def __init__(self, key):
        self.left = None
        self.right = None
        self.val = key

def insert_tree_iterative(root, key):
    if root is None:
        return TreeNode(key)
    curr = root
    while True:
        if key < curr.val:
            if curr.left is None:
                curr.left = TreeNode(key)
                break
            else:
                curr = curr.left
        else:
            if curr.right is None:
                curr.right = TreeNode(key)
                break
            else:
                curr = curr.right
    return root

def store_sorted_iterative(root, arreglo):
    stack = []
    curr = root
    i = 0
    while stack or curr:
        if curr:
            stack.append(curr)
            curr = curr.left
        else:
            curr = stack.pop()
            arreglo[i] = curr.val
            i += 1
            curr = curr.right

def tree_sort(arreglo: List[Any]) -> List[Any]:
    if not arreglo:
        return arreglo
    root = None
    for item in arreglo:
        root = insert_tree_iterative(root, item)
    store_sorted_iterative(root, arreglo)
    return arreglo


# 5. Pigeonhole Sort
def pigeonhole_sort(arreglo: List[Any], key=lambda x: x) -> List[Any]:
    if not arreglo: return arreglo
    min_val = key(arreglo[0])
    max_val = key(arreglo[0])
    for item in arreglo:
        val = key(item)
        if val < min_val: min_val = val
        if val > max_val: max_val = val
        
    size = max_val - min_val + 1
    holes = [[] for _ in range(size)]
    
    for item in arreglo:
        holes[key(item) - min_val].append(item)
        
    i = 0
    for hole in holes:
        for item in hole:
            arreglo[i] = item
            i += 1
    return arreglo


# 6. Bucket Sort
def bucket_sort(arreglo: List[Any], key=lambda x: x) -> List[Any]:
    if not arreglo: return arreglo
    
    min_val = key(arreglo[0])
    max_val = key(arreglo[0])
    for item in arreglo:
        val = key(item)
        if val < min_val: min_val = val
        if val > max_val: max_val = val
        
    bucket_count = min(len(arreglo), 1000)
    buckets = [[] for _ in range(bucket_count)]
    
    range_val = max_val - min_val
    if range_val == 0:
        return arreglo
        
    for item in arreglo:
        idx = int(((key(item) - min_val) / range_val) * (bucket_count - 1))
        buckets[idx].append(item)
        
    i = 0
    for bucket in buckets:
        OrdenarArregloLtoR(bucket, 0, len(bucket)-1)
        for item in bucket:
            arreglo[i] = item
            i += 1
    return arreglo


# 7. Quick Sort
def partition(arreglo: List[Any], low: int, high: int) -> int:
    pivot = arreglo[high]
    i = low - 1
    for j in range(low, high):
        if arreglo[j] <= pivot:
            i = i + 1
            arreglo[i], arreglo[j] = arreglo[j], arreglo[i]
    arreglo[i + 1], arreglo[high] = arreglo[high], arreglo[i + 1]
    return i + 1

def quick_sort(arreglo: List[Any]) -> List[Any]:
    size = len(arreglo)
    if size <= 1: return arreglo
    stack = [0] * (size + 1)
    top = -1
    top += 1
    stack[top] = 0
    top += 1
    stack[top] = size - 1

    while top >= 0:
        high = stack[top]
        top -= 1
        low = stack[top]
        top -= 1

        if low < high:
            pi = partition(arreglo, low, high)
            
            if pi - 1 > low:
                top += 1
                stack[top] = low
                top += 1
                stack[top] = pi - 1

            if pi + 1 < high:
                top += 1
                stack[top] = pi + 1
                top += 1
                stack[top] = high
    return arreglo


# 8. Heap Sort
def heapify_iterative(arreglo: List[Any], n: int, i: int):
    while True:
        largest = i
        l = 2 * i + 1
        r = 2 * i + 2
        
        if l < n and arreglo[l] > arreglo[largest]:
            largest = l
        if r < n and arreglo[r] > arreglo[largest]:
            largest = r
            
        if largest != i:
            arreglo[i], arreglo[largest] = arreglo[largest], arreglo[i]
            i = largest
        else:
            break

def heap_sort(arreglo: List[Any]) -> List[Any]:
    n = len(arreglo)
    for i in range(n // 2 - 1, -1, -1):
        heapify_iterative(arreglo, n, i)
    for i in range(n - 1, 0, -1):
        arreglo[i], arreglo[0] = arreglo[0], arreglo[i]
        heapify_iterative(arreglo, i, 0)
    return arreglo


# 9. Bitonic Sort
def _bitonic_merge(arreglo: List[Any], low: int, cnt: int, d: int):
    if cnt > 1:
        k = cnt // 2
        for i in range(low, low + k):
            if (d == 1 and arreglo[i] > arreglo[i + k]) or (d == 0 and arreglo[i] < arreglo[i + k]):
                arreglo[i], arreglo[i + k] = arreglo[i + k], arreglo[i]
        _bitonic_merge(arreglo, low, k, d)
        _bitonic_merge(arreglo, low + k, k, d)

def _bitonic_sort_rec(arreglo: List[Any], low: int, cnt: int, d: int):
    if cnt > 1:
        k = cnt // 2
        _bitonic_sort_rec(arreglo, low, k, 1) # Ascending
        _bitonic_sort_rec(arreglo, low + k, k, 0) # Descending
        _bitonic_merge(arreglo, low, cnt, d)

def bitonic_sort(arreglo: List[Any]) -> List[Any]:
    """ NOTE: cnt must be a power of 2 to work perfectly. """
    if arreglo:
        _bitonic_sort_rec(arreglo, 0, len(arreglo), 1)
    return arreglo


# 10. Gnome Sort
def gnome_sort(arreglo: List[Any]) -> List[Any]:
    n = len(arreglo)
    index = 0
    while index < n:
        if index == 0:
            index = index + 1
        if arreglo[index] >= arreglo[index - 1]:
            index = index + 1
        else:
            arreglo[index], arreglo[index - 1] = arreglo[index - 1], arreglo[index]
            index = index - 1
    return arreglo


# 11. Binary Insertion Sort
def binary_search_insertion(arreglo, val, start, end):
    if start == end:
        if arreglo[start] > val:
            return start
        else:
            return start + 1
    if start > end:
        return start
    mid = (start + end) // 2
    if arreglo[mid] < val:
        return binary_search_insertion(arreglo, val, mid + 1, end)
    elif arreglo[mid] > val:
        return binary_search_insertion(arreglo, val, start, mid - 1)
    else:
        return mid

def binary_insertion_sort(arreglo: List[Any]) -> List[Any]:
    for i in range(1, len(arreglo)):
        val = arreglo[i]
        j = binary_search_insertion(arreglo, val, 0, i - 1)
        for k in range(i, j, -1):
            arreglo[k] = arreglo[k - 1]
        arreglo[j] = val
    return arreglo


# 12. Radix Sort
def counting_sort_for_radix(arreglo: List[Any], exp1: int, key=lambda x: x):
    n = len(arreglo)
    output = [None] * n
    count = [0] * 10
    
    for i in range(n):
        index = key(arreglo[i]) // exp1
        count[index % 10] += 1
        
    for i in range(1, 10):
        count[i] += count[i - 1]
        
    i = n - 1
    while i >= 0:
        index = key(arreglo[i]) // exp1
        output[count[index % 10] - 1] = arreglo[i]
        count[index % 10] -= 1
        i -= 1
        
    for i in range(n):
        arreglo[i] = output[i]

def radix_sort(arreglo: List[Any], key=lambda x: x) -> List[Any]:
    if not arreglo: return arreglo
    
    # We find the min to handle any offsets if necessary.
    # Standard Radix assumes positive integers.
    max_val = key(max(arreglo, key=key))
    
    exp = 1
    while max_val // exp > 0:
        counting_sort_for_radix(arreglo, exp, key)
        exp *= 10
    return arreglo
