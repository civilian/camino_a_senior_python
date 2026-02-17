¿Alguna vez te has preguntado por qué algunas consultas de datos tardan una eternidad mientras otras son casi instantáneas? La respuesta no está en la cantidad de datos, sino en la arquitectura del motor que los procesa. Vamos a desentrañar el ingenio detrás de Presto y por qué nació de una necesidad crítica en Facebook.

# Presto

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