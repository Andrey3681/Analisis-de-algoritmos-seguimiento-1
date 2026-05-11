import math

def euclidean_distance(ts1, ts2):
    """
    Calcula la distancia Euclidiana entre dos series de tiempo.
    Asume que ambas series tienen la misma longitud.
    """
    if len(ts1) != len(ts2):
        raise ValueError("Las series de tiempo deben tener la misma longitud para la distancia Euclidiana.")
    
    suma_cuadrados = sum((a - b) ** 2 for a, b in zip(ts1, ts2))
    return math.sqrt(suma_cuadrados)

def pearson_correlation(ts1, ts2):
    """
    Calcula la correlación de Pearson entre dos series de tiempo.
    """
    if len(ts1) != len(ts2):
        raise ValueError("Las series de tiempo deben tener la misma longitud para la correlación de Pearson.")
    
    n = len(ts1)
    if n == 0:
        return 0.0

    mean1 = sum(ts1) / n
    mean2 = sum(ts2) / n

    num = sum((a - mean1) * (b - mean2) for a, b in zip(ts1, ts2))
    den1 = sum((a - mean1) ** 2 for a in ts1)
    den2 = sum((b - mean2) ** 2 for b in ts2)

    if den1 == 0 or den2 == 0:
        return 0.0

    return num / math.sqrt(den1 * den2)

def dtw_distance(ts1, ts2):
    """
    Calcula la distancia de Dynamic Time Warping (DTW) entre dos series de tiempo.
    Permite comparar secuencias de diferentes longitudes.
    """
    n, m = len(ts1), len(ts2)
    dtw_matrix = [[float('inf')] * (m + 1) for _ in range(n + 1)]
    dtw_matrix[0][0] = 0

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            cost = abs(ts1[i - 1] - ts2[j - 1])
            dtw_matrix[i][j] = cost + min(
                dtw_matrix[i - 1][j],    # Inserción
                dtw_matrix[i][j - 1],    # Eliminación
                dtw_matrix[i - 1][j - 1] # Coincidencia
            )
            
    return dtw_matrix[n][m]

def cosine_similarity(ts1, ts2):
    """
    Calcula la similitud por coseno entre dos series de tiempo.
    """
    if len(ts1) != len(ts2):
        raise ValueError("Las series de tiempo deben tener la misma longitud para la similitud del coseno.")
    
    dot_product = sum(a * b for a, b in zip(ts1, ts2))
    norm_ts1 = math.sqrt(sum(a ** 2 for a in ts1))
    norm_ts2 = math.sqrt(sum(b ** 2 for b in ts2))
    
    if norm_ts1 == 0 or norm_ts2 == 0:
        return 0.0
        
    return dot_product / (norm_ts1 * norm_ts2)

def get_algorithm_explanations():
    return {
        "Distancia Euclidiana": {
            "matematica": "d(x, y) = sqrt( sum_{i=1}^n (x_i - y_i)^2 )",
            "algoritmica": "1. Verificar que ambas series tengan la misma longitud.\n2. Para cada punto i, calcular la diferencia entre x_i e y_i, y elevar al cuadrado.\n3. Sumar todos estos valores al cuadrado.\n4. Calcular la raíz cuadrada de la suma total.",
            "complejidad": "O(N) donde N es la longitud de las series. Espacio: O(1)."
        },
        "Correlacion de Pearson": {
            "matematica": "r = sum((x_i - mean(x)) * (y_i - mean(y))) / sqrt(sum((x_i - mean(x))^2) * sum((y_i - mean(y))^2))",
            "algoritmica": "1. Calcular la media de ambas series.\n2. Para cada elemento, calcular su diferencia respecto a la media.\n3. Multiplicar las diferencias correspondientes y sumarlas para el numerador.\n4. Para el denominador, calcular la suma de cuadrados de las diferencias para cada serie y multiplicarlas, aplicando raíz cuadrada al resultado final.",
            "complejidad": "O(N) ya que requiere pasadas lineales sobre los datos. Espacio: O(1)."
        },
        "Dynamic Time Warping (DTW)": {
            "matematica": "DTW(i, j) = cost(x_i, y_j) + min(DTW(i-1, j), DTW(i, j-1), DTW(i-1, j-1))",
            "algoritmica": "1. Crear una matriz de tamaño (N+1) x (M+1) inicializada en infinito.\n2. Establecer matriz[0][0] = 0.\n3. Iterar por cada elemento i de la primera serie y j de la segunda.\n4. Calcular el costo (diferencia absoluta) entre x_i e y_j.\n5. El valor de la celda será el costo más el mínimo entre la inserción, eliminación o coincidencia previa.",
            "complejidad": "O(N * M) en tiempo y espacio, donde N y M son las longitudes de las series. Puede optimizarse el espacio a O(min(N, M))."
        },
        "Similitud por Coseno": {
            "matematica": "cos(theta) = sum(x_i * y_i) / (sqrt(sum(x_i^2)) * sqrt(sum(y_i^2)))",
            "algoritmica": "1. Calcular el producto punto multiplicando pares de elementos de ambas series y sumándolos.\n2. Calcular la magnitud (norma L2) de cada serie elevando al cuadrado cada elemento, sumándolos y aplicando raíz cuadrada.\n3. Dividir el producto punto entre la multiplicación de las dos magnitudes.",
            "complejidad": "O(N) en tiempo debido a pasadas lineales. Espacio: O(1)."
        }
    }
