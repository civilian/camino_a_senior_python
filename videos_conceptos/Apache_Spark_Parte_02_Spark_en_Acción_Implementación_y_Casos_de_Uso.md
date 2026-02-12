Hemos visto la elegante teoría detrás de Spark, pero ¿cómo se traduce eso en código que resuelve problemas reales? Pasemos del 'porqué' al 'cómo' y construyamos un pipeline de datos desde cero, viendo las buenas prácticas y los errores a evitar.

# Apache Spark

---

### 3. **Evolución Histórica Detallada: Una Carrera Hacia la Velocidad de la Luz**

| Año | Hito Clave | Contexto Computacional | Figuras Clave |
| :-- | :--- | :--- | :--- |
| **2004** | Google publica el paper de MapReduce. | El Big Data es un problema de nicho para gigantes de la web. Nace el ecosistema Hadoop. | Jeffrey Dean, Sanjay Ghemawat |
| **2009** | **Nace Spark** en el AMPLab de Berkeley. | Hadoop domina, pero su lentitud para cargas de trabajo iterativas es un dolor de cabeza creciente. | **Matei Zaharia** |
| **2012** | Publicación del paper fundamental de los RDDs. | El Machine Learning a escala empieza a ser una necesidad empresarial, no solo académica. | Matei Zaharia et al. |
| **2013** | Spark se une a la Incubadora de Apache. | La comunidad de código abierto busca alternativas más rápidas y flexibles a MapReduce. | |
| **2014** | **Spark 1.0**: Spark SQL, Streaming, MLlib. | El concepto de "Lambda Architecture" (sistemas separados para batch y streaming) es popular. Spark promete unificarlo. | |
| **2015** | **Nace Databricks**, la empresa detrás de Spark. | La comercialización y el soporte empresarial se vuelven cruciales para la adopción masiva. | Fundadores del AMPLab |
| **2016** | **Spark 2.0**: API de DataFrame/Dataset, Catalyst, Tungsten. | La optimización de compiladores y la gestión manual de memoria se aplican al Big Data. Es un cambio de juego. | **Michael Armbrust** (Catalyst) |
| **2020** | **Spark 3.0**: Adaptive Query Execution (AQE), mejoras en Python. | La optimización en tiempo de ejecución se vuelve la nueva frontera. La ciencia de datos en Python es el rey. | |

El momento decisivo fue, sin duda, la transición de la API de RDD a la de DataFrame en Spark 2.0. Fue un movimiento audaz. La comunidad amaba la flexibilidad de los RDDs, pero el equipo de Spark sabía que para alcanzar el siguiente nivel de rendimiento, necesitaban una abstracción más estructurada. Al imponer un esquema, le dieron al motor la información que necesitaba para optimizar las consultas de una manera que era imposible con el código opaco de los RDDs. Fue un trade-off de flexibilidad por un rendimiento y una simplicidad asombrosos.

---

### 4. **Implementación Práctica: De la Teoría al Teclado**

Hablemos en Python (PySpark), el lenguaje de facto para la ciencia de datos con Spark.

#### **Ejemplo Funcional: Análisis de Logs de Servidor Web**

Imaginemos que tenemos un archivo de log con el formato `ip_address, timestamp, request, status_code`. Queremos encontrar las 10 páginas más visitadas que devolvieron un error 404.

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, split, count

# 1. Crear una SparkSession - El punto de entrada a toda la funcionalidad de Spark
spark = SparkSession.builder \
    .appName("AnalisisLogsWeb") \
    .master("local[*]") # Usar todos los cores locales
    .getOrCreate()

# 2. Cargar los datos (Spark infiere el esquema si es simple)
# En un entorno real, leerías de HDFS, S3, etc.
# Creamos un DataFrame de ejemplo para que sea reproducible
log_data = [
    ("192.168.1.1", "2023-10-27T10:00:00Z", "GET /home HTTP/1.1", 200),
    ("192.168.1.2", "2023-10-27T10:01:00Z", "GET /products/123 HTTP/1.1", 200),
    ("192.168.1.1", "2023-10-27T10:02:00Z", "GET /about-us HTTP/1.1", 200),
    ("192.168.1.3", "2023-10-27T10:03:00Z", "GET /non-existent-page HTTP/1.1", 404),
    ("192.168.1.2", "2023-10-27T10:04:00Z", "GET /another-bad-link HTTP/1.1", 404),
    ("192.168.1.1", "2023-10-27T10:05:00Z", "GET /non-existent-page HTTP/1.1", 404),
]
columns = ["ip", "timestamp", "request", "status"]
logs_df = spark.createDataFrame(log_data, columns)

# 3. Transformaciones (Lazy) - Construyendo el DAG
#    Aquí es donde defines la "receta"
print("--- Definiendo las transformaciones ---")

# Filtrar solo los errores 404
errors_404_df = logs_df.filter(col("status") == 404)

# Extraer la página solicitada del string de la petición
# split() devuelve un array, y accedemos al segundo elemento
page_df = errors_404_df.withColumn(
    "page",
    split(col("request"), " ")[1]
)

# Agrupar por página y contar las ocurrencias
page_counts_df = page_df.groupBy("page").agg(count("*").alias("error_count"))

# Ordenar por el conteo en orden descendente
top_10_errors_df = page_counts_df.orderBy(col("error_count").desc()).limit(10)

# 4. Acción - ¡Ejecutar el trabajo!
#    Nada de lo anterior se ha ejecutado hasta esta línea.
#    .show() es una acción que muestra los resultados en la consola.
print("--- Ejecutando la acción (.show()) ---")
top_10_errors_df.show()

# Puedes ver el plan de ejecución que Spark ha optimizado
print("--- Plan de Ejecución Físico ---")
top_10_errors_df.explain()

# 5. Detener la sesión de Spark
spark.stop()
```

#### **Comparaciones: "Mal vs. Bien"**

**Mal (Estilo RDD, propenso a errores y lento):**

```python
# NO HACER ESTO PARA ANÁLISIS ESTRUCTURADO
logs_rdd = spark.sparkContext.textFile("logs.txt")
errors_404_rdd = logs_rdd \
    .filter(lambda line: line.split(",")[3] == "404") \
    .map(lambda line: (line.split(",")[2].split(" ")[1], 1)) \
    .reduceByKey(lambda a, b: a + b) \
    .sortBy(lambda x: x[1], ascending=False) \
    .take(10) # take() es una acción

# ¿Por qué es malo?
# 1. Opaco para Spark: Spark ve el código Python como una "caja negra". No puede optimizar el orden de las operaciones.
# 2. Frágil: Un cambio en el formato del log rompe el código con errores de índice.
# 3. Verboso: Es más difícil de leer y mantener.
```

**Bien (Estilo DataFrame/Spark SQL, optimizado y robusto):**

```python
# SÍ HACER ESTO
# (El código del ejemplo funcional anterior)
# ¿Por qué es bueno?
# 1. Expresivo y Declarativo: Dices "qué" quieres, no "cómo" hacerlo.
# 2. Optimización por Catalyst: Spark entiende la estructura y puede reordenar filtros, proyecciones (selects) y optimizar joins.
# 3. Robusto: Accedes a los datos por nombre de columna (col("status")), no por índice.
```

#### **Caso de Estudio: Detección de Fraude en Transacciones**

Una empresa financiera necesita identificar patrones de fraude en tiempo real. Usan Spark Structured Streaming para leer transacciones de Kafka.

1.  **Ingesta**: Un DataFrame de streaming se conecta a un topic de Kafka.
2.  **Enriquecimiento**: Hacen un `join` del stream de transacciones con un DataFrame estático de perfiles de usuario para añadir información contextual (ej. país del usuario).
3.  **Agregación en Ventana**: Usan una ventana de tiempo deslizante (`window()`) para calcular agregados por usuario, como "número de transacciones en los últimos 5 minutos" o "suma de importes desde países de alto riesgo en la última hora".
4.  **Detección**: Aplican una regla o un modelo de MLlib para marcar transacciones como sospechosas si los agregados superan ciertos umbrales.
5.  **Salida**: Las alertas de fraude se escriben en otro topic de Kafka o en una base de datos para acción inmediata.

Este caso de uso es perfecto para Spark porque combina streaming, joins y agregaciones complejas en un solo motor coherente.