import random
import time
from ListaAlgoritmos import tim_sort

def main():
    print("Iniciando pruebas de Algoritmos...")
    
    # Prueba 1: Lista pequeña
    lista_pequena = [5, 2, 9, 1, 5, 6, 8, 3, 7, 4]
    print(f"\nPrueba 1 - Lista original: {lista_pequena}")
    # Pasamos una copia para no modificar la original en caso de que queramos reusarla
    resultado_pequeno = tim_sort(lista_pequena.copy())
    print(f"Prueba 1 - Lista ordenada: {resultado_pequeno}")
    
    # Prueba 2: Lista con elementos repetidos
    lista_repetidos = [3, 3, 1, 2, 4, 3, 1, 5, 2]
    print(f"\nPrueba 2 - Lista con repetidos: {lista_repetidos}")
    resultado_repetidos = tim_sort(lista_repetidos.copy())
    print(f"Prueba 2 - Lista ordenada: {resultado_repetidos}")
    
    # Prueba 3: Lista ya ordenada
    lista_ordenada = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    print(f"\nPrueba 3 - Lista ya ordenada: {lista_ordenada}")
    resultado_ordenada = tim_sort(lista_ordenada.copy())
    print(f"Prueba 3 - Lista ordenada: {resultado_ordenada}")
    
    # Prueba 4: Lista aleatoria grande para medir tiempo
    tamano = 10000
    lista_grande = [random.randint(1, 1000) for _ in range(tamano)]
    print(f"\nPrueba 4 - Lista grande ({tamano} elementos)")
    
    inicio_tiempo = time.time()
    resultado_grande = tim_sort(lista_grande.copy())
    fin_tiempo = time.time()
    
    tiempo_transcurrido = fin_tiempo - inicio_tiempo
    print(f"Prueba 4 - Primeros 20 elementos ordenados: {resultado_grande[:20]}...")
    print(f"Tiempo de ejecución para {tamano} elementos: {tiempo_transcurrido:.4f} segundos")
    
    # Verificar que realmente esté ordenada
    es_ordenada = all(resultado_grande[i] <= resultado_grande[i+1] for i in range(len(resultado_grande)-1))
    print(f"¿La lista grande está correctamente ordenada?: {'Sí' if es_ordenada else 'No'}")

if __name__ == "__main__":
    main()
