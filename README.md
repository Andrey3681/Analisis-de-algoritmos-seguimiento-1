# Proyecto: Análisis de Algoritmos Financieros 📈

Este proyecto universitario para la asignatura **Análisis de Algoritmos** implementa un Pipeline de Datos (ETL) y un entorno completo de pruebas y mediciones (Benchmark) para 12 algoritmos de ordenamiento distintos, construidos desde cero en Python puro.

El proyecto recolecta **datos históricos diarios** de 20 activos bursátiles mundiales (Acciones de la BVC y ETFs Globales) utilizando llamadas directas a las APIs públicas de Yahoo Finance, consolidándolos para posteriormente analizar su rendimiento computacional bajo diferentes métodos de ordenamiento matemático y comparativo.

---

## 🎯 Requerimientos y Restricciones Cumplidas
- **Extracción Pura (`Requests`)**: No se emplea `yfinance`, `pandas_datareader` o similares. La comunicación se realiza nativamente mediante HTTP GET Requests.
- **Implementación desde Cero**: Los 12 algoritmos de ordenamiento se construyeron artesanalmente sin hacer uso de los métodos de la librería estándar de Python (`.sort()` o `sorted()`).
- **Reproducibilidad (Sin Datos Estáticos)**: La data se extrae dinámicamente alineando los calendarios de negocio y completando vacíos usando interpolación local de variables financieras.

---

## 📁 Estructura del Directorio (Arquitectura de Software)

```text
Algoritmos de analisis financiero/
│
├── data/                         # 🗄️ Capa de Datos
│   └── dataset_maestro.csv       # Archivo unificado de +26,000 registros generados por el ETL.
│
├── etl/                          # 📡 Módulo de Extracción y Limpieza
│   ├── extractor.py              # Clase HTTP Request con headers falsificados y retries por rate limiting.
│   ├── transformer.py            # Alineación de calendarios festivos (BVC vs WallStreet) vía Pandas.
│   └── loader.py                 # Exportación de las tramas de memoria a disco (CSV).
│
├── sorting/                      # 🧠 Módulo de Modelado y Evaluación
│   ├── models.py                 # Clase 'Record' que sobreescribe métodos mágicos (__lt__, __le__) para fechas y cierres.
│   └── evaluator.py              # Entorno estricto de pruebas de rendimiento (Base matemática: Potencias de 2 - 4096 samples).
│
├── Algoritmos/                   # 📜 Core de Rendimiento (Implementaciones Puras)
│   └── ListaAlgoritmos.py        # Aquí residen los 12 algoritmos: (Tim, Comb, Selection, Tree, Pigeonhole, Bucket, Quick, Heap, Bitonic, Gnome, Binary Insertion, Radix).
│
├── analysis/                     # 📊 Módulo Analítico Visual
│   └── visualizer.py             # Genera la gráfica de barras de tiempos y detecta el 'Top 15 Volumen'.
│
├── docs/                         # 📝 Módulo Teórico
│   └── big_o_analysis.md         # Documentación detallada sobre la complejidad Big-O temporal y espacial de cada algoritmo.
│
├── run_etl.py                    # 🚀 [Punto de Entrada 1] Ejecutar para descargar los datos.
├── main.py                       # 🏎️ [Punto de Entrada 2] Ejecutar para ordenar, medir tiempos y graficar.
└── README.md                     # Documentación general del proyecto (Este archivo).
```

---

## ⚙️ Cómo Ejecutar el Proyecto

### 1. Instalar Dependencias
Asegúrate de contar con Python 3.10+ e instala las librerías permitidas por la especificación:
```bash
pip install pandas numpy requests matplotlib
```

### 2. Ejecutar la Extracción (ETL)
Antes de poder ordenar los datos, debes descargar la información más actualizada a la fecha. En la terminal de tu editor o consola de Windows, desde la carpeta del proyecto ejecuta:
```bash
python run_etl.py
```
> **Nota:** Esto descargará los últimos 5 años de datos de los 20 tickers estipulados y creará el archivo en la carpeta `data/`.

### 3. Ejecutar el Benchmark y Análisis Algorítmico 
Con los datos listos, usa el orquestador principal para evaluar los tiempos de ejecución y procesar el mayor volumen bursátil:
```bash
python main.py
```
> **Nota:** Se tomará una muestra estadísticamente justa y caótica de **4096 registros** (`seed = 42`) para garantizar la operación del `Bitonic Sort` y compilar la gráfica final `sorting_benchmark.png`.
