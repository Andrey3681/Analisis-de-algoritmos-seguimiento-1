import os
import sys
import matplotlib.pyplot as plt
from datetime import datetime

# Añadir el directorio base para poder importar los módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Algoritmos.Similitud import (
    euclidean_distance,
    pearson_correlation,
    dtw_distance,
    cosine_similarity,
    get_algorithm_explanations
)

def load_prices_by_symbol(csv_path):
    """
    Carga los precios de cierre agrupados por activo (Symbol) y fecha.
    Retorna un diccionario: { Symbol: { Date: Close_Price } }
    """
    data = {}
    with open(csv_path, 'r') as f:
        header = f.readline().strip().split(',')
        try:
            symbol_idx = header.index('Symbol')
            date_idx = header.index('Date')
            close_idx = header.index('Close')
        except ValueError:
            print("El CSV debe contener las columnas: Symbol, Date, Close")
            return data

        for line in f:
            if not line.strip():
                continue
            parts = line.strip().split(',')
            if len(parts) <= max(symbol_idx, date_idx, close_idx):
                continue
                
            symbol = parts[symbol_idx]
            date_str = parts[date_idx]
            
            try:
                close = float(parts[close_idx])
            except ValueError:
                continue
                
            if symbol not in data:
                data[symbol] = {}
            data[symbol][date_str] = close
            
    return data

def run_similarity_app():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_dir, 'data', 'dataset_maestro.csv')
    
    if not os.path.exists(data_path):
        print(f"Archivo de datos no encontrado en {data_path}.")
        return

    print("Cargando datos históricos...")
    market_data = load_prices_by_symbol(data_path)
    symbols = list(market_data.keys())
    
    if not symbols:
        print("No se encontraron activos en el dataset.")
        return
        
    print("\n--- Análisis de Similitud de Series de Tiempo ---")
    print(f"Activos disponibles ({len(symbols)}): {', '.join(symbols[:10])} ...")
    
    # Simple CLI para selección
    asset1 = input("Ingrese el primer activo (ej. ARKK, AAPL): ").strip().upper()
    asset2 = input("Ingrese el segundo activo: ").strip().upper()
    
    if asset1 not in market_data or asset2 not in market_data:
        print("Uno o ambos activos no fueron encontrados en los datos.")
        return
        
    # Obtener fechas comunes para asegurar series de igual longitud
    dates1 = set(market_data[asset1].keys())
    dates2 = set(market_data[asset2].keys())
    common_dates = sorted(list(dates1.intersection(dates2)))
    
    if not common_dates:
        print("Los activos seleccionados no tienen fechas en común.")
        return
        
    # Extraer las series de tiempo (precios de cierre)
    ts1 = [market_data[asset1][d] for d in common_dates]
    ts2 = [market_data[asset2][d] for d in common_dates]
    
    print(f"\nCalculando similitudes sobre {len(common_dates)} días en común...")
    
    # 1. Distancia Euclidiana
    euclidean = euclidean_distance(ts1, ts2)
    # 2. Correlación de Pearson
    pearson = pearson_correlation(ts1, ts2)
    # 3. Dynamic Time Warping (DTW)
    # Reducimos la serie si es muy grande para DTW porque es O(N^2)
    dtw_limit = 500
    if len(ts1) > dtw_limit:
        print(f"  (Nota: Calculando DTW usando los últimos {dtw_limit} días por eficiencia)")
        dtw_val = dtw_distance(ts1[-dtw_limit:], ts2[-dtw_limit:])
    else:
        dtw_val = dtw_distance(ts1, ts2)
    # 4. Similitud Coseno
    cosine = cosine_similarity(ts1, ts2)
    
    print("\n================ RESULTADOS DE SIMILITUD ================")
    print(f"Activos comparados: {asset1} vs {asset2}")
    print(f"1. Distancia Euclidiana: {euclidean:.4f}")
    print(f"2. Correlación de Pearson: {pearson:.4f}")
    print(f"3. Distancia DTW: {dtw_val:.4f}")
    print(f"4. Similitud por Coseno: {cosine:.4f}")
    
    print("\n================ EXPLICACIONES MATEMÁTICAS ===============")
    explanations = get_algorithm_explanations()
    for name, expl in explanations.items():
        print(f"\n> {name}")
        print(f"  Fórmula: {expl['matematica']}")
        print(f"  Algoritmo:\n    {expl['algoritmica'].replace(chr(10), chr(10)+'    ')}")
        print(f"  Complejidad: {expl['complejidad']}")
        
    # Visualización
    print("\nGenerando gráfico de series temporales...")
    plt.figure(figsize=(12, 6))
    
    # Normalizar para visualización comparativa (Base 100 en el día 1)
    norm_ts1 = [p / ts1[0] * 100 for p in ts1]
    norm_ts2 = [p / ts2[0] * 100 for p in ts2]
    
    # Para el eje x usamos índices o fechas simplificadas
    x_labels = common_dates
    # Mostramos máximo 10 etiquetas
    step = max(1, len(common_dates) // 10)
    
    plt.plot(norm_ts1, label=f"{asset1} (Base 100)", alpha=0.8, linewidth=2)
    plt.plot(norm_ts2, label=f"{asset2} (Base 100)", alpha=0.8, linewidth=2)
    
    plt.xticks(range(0, len(common_dates), step), [common_dates[i] for i in range(0, len(common_dates), step)], rotation=45)
    
    plt.title(f"Comparativa de Series de Tiempo: {asset1} vs {asset2}")
    plt.xlabel("Fecha")
    plt.ylabel("Precio Relativo (Base 100)")
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    
    plot_path = os.path.join(base_dir, f'similitud_{asset1}_{asset2}.png')
    plt.savefig(plot_path)
    print(f"Gráfico guardado exitosamente en: {plot_path}")
    
if __name__ == "__main__":
    run_similarity_app()
