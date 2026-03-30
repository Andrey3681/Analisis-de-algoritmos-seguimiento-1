# Análisis de Complejidad Big-O de los Algoritmos de Ordenamiento

Este documento detalla la complejidad temporal y espacial de los 12 algoritmos de ordenamiento implementados desde cero en el proyecto para ordenar los registros financieros (por Fecha y Precio de Cierre).

## 1. Algoritmos Comparativos (Basados en intercambios y comparaciones)

### TimSort
- **Mejor Caso:** $O(N)$ (Si el arreglo ya está ordenado).
- **Caso Promedio y Peor Caso:** $O(N \log N)$
- **Espacio:** $O(N)$

### Comb Sort (Variación de Bubble Sort)
- **Mejor Caso:** $O(N)$
- **Caso Promedio:** $O(N \log N)$
- **Peor Caso:** $O(N^2)$
- **Espacio:** $O(1)$

### Selection Sort
- **Todos los casos:** $O(N^2)$ (Siempre escanea la parte desordenada completa para buscar el mínimo).
- **Espacio:** $O(1)$

### Tree Sort
- **Mejor y Caso Promedio:** $O(N \log N)$ (Si el árbol binario se distribuye bien).
- **Peor Caso:** $O(N^2)$ (Si los datos ya están ordenados y el árbol degenera en lista).
- **Espacio:** $O(N)$

### QuickSort
- **Mejor y Promedio:** $O(N \log N)$
- **Peor Caso:** $O(N^2)$ (Ocurre raramente con buena elección de pivote, como un balance pobre prolongado).
- **Espacio:** $O(\log N)$ a $O(N)$ dependiendo de las llamadas recursivas, en nuestra versión iterativa la pila artificial.

### HeapSort
- **Todos los casos:** $O(N \log N)$
- **Espacio:** $O(1)$ (Implementación in-place sin recursión).

### Bitonic Sort
- **Todos los casos:** $O(N \log^2 N)$
- **Espacio:** $O(\log N)$ para la pila iterativa o llamadas empiladas. 
- *Nota:* Su enfoque natural y dependiente de potencias de 2 es muy amigable con ejecución en hardware paralelo (CUDA/GPU).

### Gnome Sort
- **Mejor Caso:** $O(N)$ (Si ya está ordenado).
- **Peor y Promedio:** $O(N^2)$ (Enormes retrocesos sobre cada desordenamiento local).
- **Espacio:** $O(1)$

### Binary Insertion Sort 
- **Mejor Caso:** Búsquedas $O(N \log N)$ pero con desplazamiento escaso.
- **Peor y Promedio:** $O(N^2)$ (A pesar de la optimización con la búsqueda binaria, reordenar e insertar elementos desplazando el array subyacente cuesta iteraciones extras).
- **Espacio:** $O(1)$

## 2. Algoritmos No Comparativos (Criterio Integer)

### Pigeonhole Sort
- **Complejidad Temporal:** $O(N + R)$ donde $R$ es el rango de valores (Max - Min).
- **Espacio:** $O(N + R)$
- *Nota:* Excelente desempeño en nuestro proyecto ya que se mapearon las fechas como `20240322` con varianza controlable por los límites temporales.

### Bucket Sort
- **Mejor y Promedio:** $O(N + k)$ donde $k$ es el número de buckets.
- **Peor Caso:** $O(N^2)$ (Si todos los elementos tienen valores tan similares que caen en un mismo bucket y usamos Insertion Sort ahí).
- **Espacio:** $O(N + k)$

### Radix Sort
- **Complejidad Temporal:** $O(d \cdot (N + b))$ donde $d$ son los dígitos por barrer, y $b$ la base elegida (10 en nuestro caso).
- **Espacio:** $O(N + b)$
- *Nota:* Implementamos una llave unificada base 10 permitiendo agrupar temporalidad y precios decimalmente alineados con pasadas sucesivas para garantizar estabilidad.
