# Presto

¡Absolutamente! Ponte cómodo, sírvete un café (o tu bebida de compilación preferida), porque vamos a embarcarnos en un viaje profundo. No solo aprenderás a usar Presto; aprenderás a *pensar* en Presto. Desmitificaremos su magia para que puedas empuñarla con la precisión de un ingeniero senior.

***

## Presto: El Director de la Orquesta de Datos. Una Guía para el Nivel Senior

### 1. Introducción Profunda: La Necesidad de Velocidad en un Océano de Datos

Para entender Presto, debemos transportarnos a Facebook alrededor de 2012. La empresa se ahogaba en datos, un diluvio de petabytes almacenados en un masivo clúster de Hadoop. Su herramienta para analizar esta montaña de información era **Apache Hive**, que traducía consultas SQL a trabajos de MapReduce. Hive era robusto y escalable, pero tenía la agilidad de un glaciar. Una sola consulta podía tardar desde minutos hasta horas, un ciclo de retroalimentación inaceptable para analistas y científicos de datos que necesitaban explorar datos de forma interactiva.

> "Los analistas de datos, que dependen de SQL para el análisis, se veían frenados por la naturaleza batch de Hadoop/MapReduce. La necesidad de una herramienta que permitiera un análisis de datos interactivo y rápido a escala de petabytes era evidente." — **Martin Traverso, Dain Sundstrom, David Phillips, Eric Hwang**, *Presto: SQL on Everything* (2019)

Este fue el crisol en el que se forjó Presto. Un equipo de cuatro ingenieros visionarios en Facebook —Martin Traverso, Dain Sundstrom, David Phillips y Eric Hwang— se propuso un objetivo audaz: construir un motor de consultas SQL distribuido que pudiera ofrecer respuestas en segundos, no en horas, directamente sobre su data lake en HDFS.

**El problema fundamental que Presto resuelve no es el almacenamiento de datos, sino el acceso federado y de baja latencia a ellos.** Presto desacopla el cómputo del almacenamiento. Es un director de orquesta que no posee ningún instrumento, pero sabe exactamente cómo hacer que la sección de vientos (un clúster de PostgreSQL), las cuerdas (archivos Parquet en S3) y la percusión (una instancia de Kafka) toquen una sinfonía coherente en tiempo real.

**Evolución:**
*   **2012:** Nace el proyecto en Facebook.
*   **2013:** Facebook lo libera como código abierto, causando un gran impacto en el ecosistema Big Data.
*   **2018-2019:** Ocurre un hito crucial: una división en la comunidad. Los creadores originales dejan Facebook y crean un *fork* del proyecto llamado **PrestoSQL**, buscando un modelo de gobierno más abierto. El proyecto original en Facebook continúa como **PrestoDB**.
*   **2020:** Para evitar confusiones, PrestoSQL es renombrado a **Trino**.

Hoy, el ecosistema está dividido, pero Trino (el sucesor espiritual del Presto original) es a menudo considerado el de desarrollo más activo y con un gobierno comunitario más fuerte, respaldado por la empresa Starburst. Esta guía se centrará en los principios que ambos comparten, pero se inclinará hacia Trino por su relevancia actual.

---

### 2. Fundamentos Teóricos y Matemáticos: La Sinfonía de la Computación Distribuida

Presto no es magia, es una brillante aplicación de principios de computación distribuida y optimización de bases de datos que se remontan a décadas atrás.

#### Base Teórica: Arquitectura MPP (Massively Parallel Processing)

El corazón de Presto es una arquitectura de **Procesamiento Masivamente Paralelo (MPP)**, un paradigma que data de los supercomputadores de los años 80 como el Teradata.

**Analogía:** Imagina que tienes que encontrar todas las veces que aparece la palabra "Sócrates" en la Biblioteca de Alejandría.
*   **Enfoque Monolítico (una base de datos tradicional):** Un solo bibliotecario (un único proceso) recorre cada libro, uno por uno. Es lento y no escala.
*   **Enfoque MapReduce (Hive):** El bibliotecario jefe (JobTracker) divide la biblioteca en secciones. Envía a cientos de ayudantes (Mappers) a leer sus secciones y anotar en una tarjeta cada vez que encuentran "Sócrates" y el número de página. Luego, recogen todas las tarjetas, las ordenan (Shuffle/Sort) y otro grupo de ayudantes (Reducers) las suma para obtener el total. Es escalable, pero implica mucha escritura y lectura de tarjetas (I/O a disco).
*   **Enfoque MPP (Presto):** El bibliotecario jefe (Coordinador) le dice a cientos de ayudantes (Workers): "¡Busquen 'Sócrates' en sus secciones asignadas y grítenme los resultados parciales a medida que los encuentren!". Los ayudantes trabajan en paralelo y transmiten los resultados directamente entre ellos o al jefe, sin necesidad de escribir notas intermedias. Es una línea de ensamblaje de datos en memoria.

Esta arquitectura se materializa en dos tipos de nodos:
1.  **Coordinador:** El cerebro de la operación. Recibe la consulta SQL, la analiza, la optimiza creando un plan de ejecución distribuido y coordina a los Workers. No procesa datos por sí mismo.
2.  **Workers:** Los músculos. Ejecutan las tareas asignadas por el Coordinador. Leen los datos de las fuentes, los procesan en memoria y envían los resultados a otros Workers o de vuelta al Coordinador.

```ascii
      [Cliente SQL]
            |
            |  (1. Consulta SQL)
            v
      +-------------+
      | Coordinador | --(3. Asigna Tareas)--> [Worker 1] --(Lee de)--> [Fuente A]
      |   - Parse   |                         [Worker 2] --(Lee de)--> [Fuente B]
      |   - Analyze |                         [Worker 3] --(Lee de)--> [Fuente C]
      |   - Plan    |                           ...
      |   - Schedule|                         [Worker N]
      +-------------+                           ^    |
            ^                                   |    | (4. Intercambio de datos en memoria)
            | (5. Resultados Parciales/Finales) |    v
            +-----------------------------------+
```

#### Principios Subyacentes:

*   **Optimización de Consultas Basada en Costo (CBO):** Presto no ejecuta las consultas a ciegas. Su optimizador, heredero espiritual de las ideas del System R de IBM en los 70, evalúa múltiples planes de ejecución posibles. Considera el "costo" de cada operación (I/O, CPU, red) basándose en estadísticas sobre los datos (tamaño de las tablas, cardinalidad de las columnas, etc.). Elige el plan con el menor costo estimado. Por ejemplo, siempre intentará filtrar los datos lo antes posible (`Predicate Pushdown`) para reducir la cantidad de información que viaja por la red.
*   **Ejecución Pipelined en Memoria:** A diferencia de MapReduce, que materializa los resultados intermedios en disco, Presto transmite los datos entre las etapas de ejecución (llamadas *Stages*) en memoria. Esto reduce drásticamente la latencia, pero también significa que es sensible a la cantidad de RAM disponible.
*   **Extensibilidad a través de Conectores:** Presto en sí no almacena nada. Su poder reside en su API de Conectores (SPI - Service Provider Interface). Un conector es un "driver" que le enseña a Presto cómo hablar con una fuente de datos específica: cómo obtener metadatos, cómo leer los datos en paralelo (en "Splits") y, a veces, cómo delegar operaciones (`Predicate Pushdown`).

> "La arquitectura del conector es clave para la visión de 'SQL en todo'. Permite a Presto federar consultas a través de fuentes de datos heterogéneas, presentando una vista unificada al usuario." — **The Trino Authors**, *Trino: The Definitive Guide* (2021)

---

### 3. Evolución Histórica Detallada: De un Hack de Facebook a un Estándar de la Industria

*   **Contexto (Principios de 2010):** El mundo del Big Data estaba dominado por el ecosistema Hadoop. HDFS era el sistema de archivos de facto y MapReduce el paradigma de procesamiento. Herramientas como Hive y Pig ofrecían abstracciones, pero la latencia era su talón de Aquiles. Mientras tanto, en el mundo académico y comercial, las bases de datos MPP como Vertica y Greenplum demostraban la viabilidad de las consultas analíticas rápidas, pero eran soluciones propietarias y acopladas al almacenamiento.
*   **2012 - La Concepción:** Martin, Dain, David y Eric, frustrados con las limitaciones de Hive, comienzan a diseñar un nuevo motor desde cero. La decisión clave fue adoptar una arquitectura MPP y un modelo de ejecución en memoria, inspirado en los sistemas DWH comerciales, pero construido para la escala y la flexibilidad del ecosistema de código abierto.
*   **2013 - El Lanzamiento:** Facebook libera Presto bajo la licencia Apache 2.0. La comunidad lo adopta rápidamente. Empresas como Netflix, Airbnb y Uber se convierten en grandes contribuyentes, empujando sus límites y añadiendo conectores para sus propias infraestructuras.
*   **Momento Decisivo (2018) - El Fork:** Tras años de desarrollo, surgieron diferencias filosóficas entre los creadores originales y la dirección de Facebook sobre el gobierno del proyecto. Los fundadores querían un modelo más neutral y comunitario, mientras que Facebook mantenía el control. Esto llevó a la decisión de hacer un *fork*. Este evento, aunque dramático, es un hermoso ejemplo del poder del código abierto. Como dijo Eric S. Raymond en *La Catedral y el Bazar*, la capacidad de hacer un *fork* es la máxima garantía de libertad para una comunidad.
*   **2020 - El Renacimiento como Trino:** PrestoSQL se renombra a Trino para establecer una identidad clara y evitar la confusión legal con la marca Presto, ahora gestionada por la Fundación Linux en nombre de Facebook (PrestoDB). Hoy, Trino es el hogar de la comunidad original y la mayoría de los committers activos.

---

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
    print(f"  - Key: {row[0]}, Name: {row[1]}, Comment: '{row[2][:30]}...'")

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
