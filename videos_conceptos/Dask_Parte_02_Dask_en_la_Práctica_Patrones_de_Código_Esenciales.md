Entender la teoría de los grafos de tareas es una cosa, pero ¿cómo se traduce eso en código que realmente funciona? Ahora vamos a pasar de los conceptos a la práctica, explorando los patrones de código que te permitirán paralelizar tus flujos de trabajo de NumPy, Pandas y mucho más.

# Dask

### **3. Evolución Histórica Detallada: Una Revolución Silenciosa**

*   **~2014 (Concepción):** El ecosistema PyData es maduro pero limitado por la memoria. La frustración es palpable en la comunidad. En Continuum Analytics, Matthew Rocklin y otros comienzan a experimentar con la idea de "NumPy bloqueado" (`dask.array`). La idea es simple: dividir un gran array en muchos arrays de NumPy más pequeños (chunks) y coordinar las operaciones sobre ellos.
*   **2015 (Nacimiento):** Se lanza Dask. Inicialmente, se centra en el paralelismo de un solo nodo, utilizando hilos y procesos para aprovechar todos los núcleos de una CPU moderna. El `dask.dataframe` emerge, aplicando la misma idea a los DataFrames de Pandas.
*   **2016 (El Salto a Distribuido):** Este es el momento decisivo. El lanzamiento de `dask.distributed` cambia las reglas del juego. Dask pasa de ser una herramienta para una sola máquina a un framework de computación distribuida. Ahora, el mismo grafo de tareas puede ser ejecutado en un clúster de cientos de máquinas. Esto lo posiciona como una alternativa real y "pythónica" a Spark.
*   **Contexto Histórico:** En ese momento, la conversación sobre "Big Data" estaba dominada por el ecosistema Hadoop/JVM. Spark había ganado una tracción inmensa por ser más rápido y fácil de usar que MapReduce. Dask no intentó una confrontación directa, sino que ofreció una "rampa de acceso" para los millones de programadores de Python que no querían abandonar su ecosistema. Fue una jugada brillante.
*   **Figuras Clave:**
    *   **Matthew Rocklin:** El creador y visionario principal.
    *   **Jim Crist, Martin Durant, Tom Augspurger:** Contribuidores clave en las primeras etapas que ayudaron a construir y solidificar el proyecto.
    *   **La comunidad PyData:** Dask no existiría sin la base sólida de NumPy y Pandas, ni sin la comunidad que lo adoptó, probó y contribuyó a su crecimiento.

---

### **4. Implementación Práctica: Del Concepto al Código**

Hablemos en el lenguaje que mejor conocemos: el código.

#### **Patrón 1: El "Big Array" - Dask Array**

**Antes (El Muro de la Memoria):**
```python
import numpy as np

# Esto fallará con un MemoryError en la mayoría de las máquinas
# (8 bytes/float * 50000 * 50000 = 20 GB)
try:
    large_array = np.ones((50000, 50000))
    result = large_array.mean()
except MemoryError as e:
    print(f"¡Crash! {e}")
```

**Después (El Poder de los Chunks):**
```python
import dask.array as da

# Dask no carga nada en memoria todavía. Solo define la estructura.
# 'chunks' define el tamaño de los bloques de NumPy subyacentes.
large_array = da.ones((50000, 50000), chunks=(5000, 5000))

# La sintaxis es casi idéntica a NumPy
result_graph = large_array.mean()

# Visualicemos el plan (el grafo) antes de ejecutar
# En un notebook, esto mostraría una imagen del DAG
print(result_graph) 

# ¡Ejecutamos! Dask procesará chunk por chunk.
final_value = result_graph.compute()
print(f"El resultado es: {final_value}")
```
**¿Por qué funciona?** Dask nunca intenta crear el array de 20 GB. Carga un chunk de 5000x5000 (200 MB), calcula su suma y su tamaño, lo descarga, y pasa al siguiente. Al final, combina los resultados parciales.

#### **Patrón 2: El "Big DataFrame" - Dask DataFrame**

**Caso de Estudio: Análisis de logs de un año**
Imagina que tienes 365 archivos CSV, uno por cada día del año, cada uno con varios GB.

**Mal (Iterativo y Lento):**
```python
import pandas as pd
import glob

# Lento, secuencial y puede agotar la memoria si los resultados intermedios son grandes
all_files = glob.glob('logs/*.csv')
results = []
for f in all_files:
    df = pd.read_csv(f)
    # Una operación de ejemplo
    results.append(df[df.error_level == 'CRITICAL'].value.mean())

final_mean = pd.Series(results).mean()
```

**Bien (Paralelo y Eficiente con Dask):**
```python
import dask.dataframe as dd

# Dask lee los metadatos, pero no los datos. Crea un plan.
# npartitions define el nivel de paralelismo.
ddf = dd.read_csv('logs/*.csv')

# La sintaxis es idéntica a Pandas. Esto construye un grafo.
critical_errors = ddf[ddf.error_level == 'CRITICAL'].value.mean()

# La computación se ejecuta en paralelo en todos los núcleos.
final_mean = critical_errors.compute()
print(f"La media de los valores críticos es: {final_mean}")
```
**¿Por qué es mejor?** Dask lee y procesa múltiples archivos CSV en paralelo. Cada partición del Dask DataFrame es un DataFrame de Pandas. La operación de filtrado y la media se aplican en paralelo a cada partición, y los resultados se agregan al final.

#### **Patrón 3: Paralelismo Arbitrario - Dask Delayed**

Este es el nivel más fundamental y flexible. `dask.delayed` puede paralelizare CUALQUIER código Python envolviendo las llamadas a funciones.

**Antes (Secuencial y Aburrido):**
```python
import time

def process_data(x):
    time.sleep(1) # Simula un trabajo costoso
    return x * 2

def summarize_results(data_list):
    time.sleep(1)
    return sum(data_list)

data = [1, 2, 3, 4, 5, 6, 7, 8]
processed = []
for d in data:
    processed.append(process_data(d))

total = summarize_results(processed)
# Tiempo total: ~8 segundos (para procesar) + 1 segundo (para sumar) = ~9 segundos
```

**Después (Paralelo y Mágico):**
```python
import dask
import time

# Mismas funciones, sin cambios
def process_data(x):
    time.sleep(1)
    return x * 2

def summarize_results(data_list):
    time.sleep(1)
    return sum(data_list)

# Envolvemos las llamadas a funciones con dask.delayed
lazy_processed = []
for d in data:
    lazy_processed.append(dask.delayed(process_data)(d))

# La llamada a summarize también es perezosa
lazy_total = dask.delayed(summarize_results)(lazy_processed)

# Visualicemos el grafo
lazy_total.visualize() # Muestra un hermoso grafo de tareas en paralelo

# ¡Ejecutamos todo el grafo!
total = lazy_total.compute()
# Tiempo total: ~1 segundo (si tienes 8+ núcleos) + 1 segundo = ~2 segundos
```
**¿Por qué es tan potente?** `dask.delayed` te permite construir DAGs personalizados para cualquier flujo de trabajo, no solo para arrays o dataframes. Es la navaja suiza del paralelismo en Python.