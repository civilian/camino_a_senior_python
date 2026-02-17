Entender la teoría es una cosa, pero ¿cómo se ve Presto en acción, uniendo bases de datos dispares con una sola consulta? Ahora es cuando pasamos del 'qué' al 'cómo', escribiendo código real para dirigir nuestra propia orquesta de datos y descubriendo las técnicas que separan a un profesional de un principiante.

# Presto

### 4. Implementación Práctica: Dirigiendo la Orquesta con Python

Usaremos el cliente de Trino para Python (`trino-python-client`), ya que es el proyecto más activo.

`pip install trino`

#### Escenario 1: Consulta Simple (El "Hola Mundo")

Imaginemos que Trino está conectado a un catálogo llamado `tpch` que contiene datos de benchmark.

```python
import trino
from trino.dbapi import connect

# Conexión al coordinador de Trino
# En un entorno real, usarías autenticación (p. ej., Kerberos, LDAP)
conn = connect(
    host="localhost",
    port=8080,
    user="python_user",
    catalog="tpch",  # Catálogo por defecto
    schema="sf1",    # Esquema por defecto
)

cur = conn.cursor()

# Ejecutamos una consulta simple
print("Ejecutando consulta sobre la tabla 'nation'...")
cur.execute("SELECT n_nationkey, n_name, n_comment FROM nation ORDER BY n_name LIMIT 5")

rows = cur.fetchall()

# Imprimimos los resultados
print("Resultados:")
for row in rows:
    print(f"  - Key: {row[0]}, Name: {row[1]}, Comment: '{row[2][:30]}...'" )

cur.close()
conn.close()
```
**Salida esperada:**
```
Ejecutando consulta sobre la tabla 'nation'...
Resultados:
  - Key: 0, Name: ALGERIA, Comment: 'haggle. carefully final deposits...'
  - Key: 1, Name: ARGENTINA, Comment: 'al foxes promise slyly according...'
  - Key: 2, Name: BRAZIL, Comment: 'y alongside of the pending deposits...'
  - Key: 3, Name: CANADA, Comment: 'eas hang ironic, pending requests...'
  - Key: 4, Name: EGYPT, Comment: 'y above the carefully unusual pack...'
```

#### Caso de Estudio: Federación de Datos (El Superpoder de Presto)

Aquí es donde Presto brilla. Imagina que tenemos:
1.  **Catálogo `postgres_db`:** Conectado a una base de datos PostgreSQL que tiene una tabla `employees` con `id`, `name` y `region_id`.
2.  **Catálogo `hive_s3`:** Conectado a un data lake en S3 (usando el conector de Hive) que tiene datos de regiones en formato Parquet en la tabla `regions` con `region_id` y `region_name`.

Nuestra misión: obtener los nombres de los empleados y sus regiones correspondientes.

```python
# ... (conexión similar, pero sin catálogo/esquema por defecto)
conn = connect(host="localhost", port=8080, user="python_user")
cur = conn.cursor()

# Una única consulta SQL que une dos sistemas completamente diferentes
federated_query = """
SELECT
    e.name,
    r.region_name
FROM
    postgres_db.public.employees e
JOIN
    hive_s3.sales_data.regions r
ON
    e.region_id = r.region_id
WHERE
    r.region_name = 'LATAM'
"""

print("Ejecutando consulta federada...")
cur.execute(federated_query)

results = cur.fetchall()

print("\nEmpleados en la región LATAM:")
for name, region in results:
    print(f"  - Empleado: {name}, Región: {region}")

cur.close()
conn.close()
```

**¿Qué sucede tras bambalinas?**
1.  El Coordinador de Trino recibe la consulta.
2.  El planificador se da cuenta de que necesita datos de dos catálogos diferentes.
3.  **Optimización clave:** Ve el `WHERE r.region_name = 'LATAM'`. En lugar de traer *todas* las regiones de S3, le dice al conector de Hive: "Oye, solo dame los datos de la región 'LATAM'". Esto es **Predicate Pushdown**.
4.  Trino obtiene los `region_id` filtrados de S3.
5.  Luego, consulta la tabla `employees` en PostgreSQL, probablemente trayendo solo los empleados cuyos `region_id` coinciden con los que obtuvo de S3.
6.  Finalmente, realiza el `JOIN` en memoria en los workers de Trino y devuelve el resultado.

#### Comparación: Mal vs. Bien

*   **Mal (Consulta "ingenua"):**
    ```sql
    -- Trae tablas enteras y luego filtra. Ineficiente.
    SELECT *
    FROM (SELECT name, region_id FROM postgres_db.public.employees) e
    JOIN (SELECT region_id, region_name FROM hive_s3.sales_data.regions) r
    ON e.region_id = r.region_id
    WHERE r.region_name = 'LATAM';
    ```
    En este caso, aunque el optimizador de Trino es inteligente y probablemente reescriba la consulta, la intención es traer todo a memoria primero.

*   **Bien (Dejar que el optimizador trabaje):**
    ```sql
    -- El filtro se aplica lo más cerca posible de la fuente.
    SELECT
        e.name,
        r.region_name
    FROM
        postgres_db.public.employees e
    JOIN
        hive_s3.sales_data.regions r ON e.region_id = r.region_id
    WHERE
        r.region_name = 'LATAM';
    ```
    Esta forma canónica permite al CBO hacer su trabajo de manera óptima, empujando el predicado `WHERE` hacia la fuente de datos en S3.

---

### 5. Nivel Senior - Conceptos Avanzados: Más Allá de la Consulta

Un ingeniero senior no solo escribe consultas, sino que diseña sistemas y comprende los compromisos.

#### Trade-offs: ¿Cuándo NO usar Presto/Trino?

Presto es un bisturí, no una navaja suiza.

| Característica | Presto / Trino | Apache Spark | Data Warehouse Tradicional (Redshift, BigQuery) |
| :--- | :--- | :--- | :--- |
| **Caso de Uso Principal** | Consultas analíticas interactivas y federadas (OLAP) | ETL a gran escala, Machine Learning, Streaming | Business Intelligence, reportes corporativos (OLAP) |
| **Latencia** | Muy Baja (segundos a minutos) | Media-Alta (minutos a horas) | Baja (segundos a minutos) |
| **Tolerancia a Fallos** | Baja (una consulta falla si un worker muere) | Alta (diseñado para recuperarse de fallos) | Alta (gestionado por el proveedor) |
| **Acoplamiento Cómputo/Storage**| Totalmente desacoplado | Desacoplado | Generalmente acoplado (aunque las versiones modernas se están desacoplando) |
| **Ideal para...** | Exploración de datos, BI de autoservicio, federación. | Transformaciones complejas y de larga duración. | Paneles de control y reportes sobre datos estructurados y limpios. |

**No uses Presto para:**
*   **Cargas de trabajo transaccionales (OLTP):** No tiene índices, transacciones ACID ni la latencia de milisegundos necesaria para una aplicación web. Usa PostgreSQL, MySQL, etc.
*   **ETL muy pesado y de larga duración:** Si una transformación va a durar horas y necesita resiliencia, Spark es una mejor herramienta. La falta de tolerancia a fallos a nivel de consulta en Presto lo hace riesgoso para trabajos muy largos.
*   **Datos muy pequeños:** La sobrecarga de coordinar una consulta distribuida puede hacer que sea más lento que consultar directamente una base de datos local para unos pocos gigabytes de datos.

#### Optimizaciones y Técnicas Avanzadas

1.  **Particionamiento y Bucketing (en la fuente de datos):** La forma en que organizas tus datos en el data lake (p. ej., S3) es CRÍTICA.
    *   **Particionar** por columnas de baja cardinalidad que se usan a menudo en filtros (p. ej., `fecha`, `país`). Si tus datos están en `s3://bucket/data/date=2023-10-27/`, una consulta con `WHERE date = '2023-10-27'` solo leerá ese prefijo, ignorando terabytes de otros datos.
    *   **Bucketing** (o clustering) por columnas de alta cardinalidad (p. ej., `user_id`). Esto organiza los datos dentro de cada partición en archivos separados basados en el hash del valor. Es extremadamente eficaz para acelerar JOINS en esas columnas.

2.  **Elección del Formato de Archivo:** Usa formatos de archivo columnares como **Apache Parquet** u **ORC**.
    > "Los formatos columnares como Parquet permiten a los motores de consulta leer solo las columnas necesarias para una consulta, en lugar de escanear filas enteras. Esta es quizás la optimización más importante para las cargas de trabajo analíticas." — **Wes McKinney**, *Python for Data Analysis* (2017)
    Una consulta `SELECT user_id, last_login FROM events` sobre un archivo Parquet de 100 columnas solo leerá los datos de esas 2 columnas, reduciendo el I/O en un 98%.

3.  **Estadísticas del Optimizador:** El CBO necesita información. Ejecutar `ANALYZE mi_tabla` periódicamente recopila estadísticas (recuento de filas, valores distintos, etc.) que permiten al optimizador tomar decisiones mucho más inteligentes, especialmente sobre el orden de los JOINS y el tipo de distribución (Broadcast vs. Distributed Join).

#### Anti-patrones: El Camino al Desastre

*   **El Martillo de Oro:** Usar Presto para todo (OLTP, ETL, etc.). Conoce tu herramienta y su propósito.
*   **La Consulta Monstruo:** Escribir una única consulta de 500 líneas con docenas de CTEs y JOINS. A menudo es mejor materializar resultados intermedios en una tabla temporal y luego consultar esa tabla. Esto ayuda a la depuración y al rendimiento.
*   **Ignorar la Localidad de los Datos:** Realizar un JOIN masivo entre datos en una región de AWS en EE.UU. y otra en Europa. La latencia de la red matará el rendimiento. Presto funciona mejor cuando el cómputo está cerca del almacenamiento.
*   **`SELECT *` en Tablas Enormes:** El anti-patrón clásico. Solo selecciona las columnas que necesitas. Esto es especialmente importante con formatos columnares.

---

### 6. Referencias y Citaciones Académicas

1.  > "Presto was designed from the ground up for interactive analytic queries against data sources of all sizes, ranging from gigabytes to petabytes." — **Martin Traverso, Dain Sundstrom, David Phillips, Eric Hwang**, *Presto: SQL on Everything* (2019). [Enlace](https://trino.io/Presto_SQL_on_Everything.pdf)
2.  > "A key design point of Presto is to separate compute from storage. This separation allows Presto and the data sources to be scaled independently." — **Martin Traverso, Dain Sundstrom, David Phillips, Eric Hwang**, *Presto: SQL on Everything* (2019).
3.  > "Trino is a community-driven, open source, distributed SQL query engine. You can think of it as a database, but it is not a general-purpose relational database." — **Matt Fuller, Manfred Moser, Martin Traverso**, *Trino: The Definitive Guide* (2021).
4.  > "The predicate pushdown optimization can dramatically reduce the amount of data that needs to be transferred from the storage system to Trino for processing." — **Matt Fuller, Manfred Moser, Martin Traverso**, *Trino: The Definitive Guide* (2021).
5.  > "System R's optimizer was one of the first to use a cost-based approach, which is now the standard for virtually all relational systems." — **P. Griffiths Selinger et al.**, *Access Path Selection in a Relational Database Management System* (1979). (Este es el paper fundamental sobre optimización de consultas que influyó en todos los sistemas posteriores, incluido Presto).
6.  > "Column-stores... offer significant performance improvements for read-mostly, large-data applications." — **Daniel J. Abadi, Samuel R. Madden, Nabil Hachem**, *Column-stores vs. Row-stores: How Different Are They Really?* (2008). [Enlace](http://db.cs.yale.edu/papers/abadi-sigmod08.pdf)
7.  > "MapReduce... has a high latency, mainly because of placing intermediate data in HDFS. For this reason, it is not suitable for interactive data analysis." — **M. Zaharia et al.**, *Resilient Distributed Datasets: A Fault-Tolerant Abstraction for In-Memory Cluster Computing* (2012). (El paper de Spark, que destaca el problema que Presto también resolvió de una manera diferente).
8.  > "The ability to fork a project and for the community to follow the fork is the ultimate guarantee of freedom in open source." — **Eric S. Raymond**, *The Cathedral & the Bazaar* (1999). (Contexto cultural para entender la división PrestoDB/Trino).
9.  > "Netflix’s data warehouse has grown to over 100PB on S3... Presto is our engine of choice to query this data warehouse." — **Netflix Technology Blog**, *Using Presto in our Big Data Platform* (2016). [Enlace](https://netflixtechblog.com/using-presto-in-our-big-data-platform-4c3d44a7173a)
10. > "Conway's law: organizations which design systems are constrained to produce designs which are copies of the communication structures of these organizations." — **Melvin E. Conway**, *How Do Committees Invent?* (1968). (Una lente para ver cómo la arquitectura Coordinador/Worker de Presto refleja una estructura de gestión y ejecución).
11. > "The Babel fish... if you stick it in your ear, you can instantly understand anything said to you in any form of language." — **Douglas Adams**, *The Hitchhiker's Guide to the Galaxy* (1979). (La mejor analogía para la capacidad de federación de Presto).
12. > "Information is the resolution of uncertainty." — **Claude Shannon**, *A Mathematical Theory of Communication* (1948). (El principio fundamental por el cual Presto existe: reducir la incertidumbre (responder preguntas) a partir de la información (datos) de la manera más eficiente posible).

***

Al dominar estos conceptos, dejas de ser un simple usuario de Presto y te conviertes en un arquitecto de datos. Entiendes que cada consulta es una negociación con las leyes de la física —latencia, ancho de banda, capacidad de cómputo— y que tu trabajo es estructurar los datos y las preguntas de tal manera que la sinfonía se ejecute en un tempo vivace, no en un adagio lúgubre. Ahora, ve y dirige tu orquesta.