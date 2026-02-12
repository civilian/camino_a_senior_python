Escribir un DAG es solo el comienzo. Para dominar Airflow de verdad, necesitas pensar como un arquitecto. ¿Cuándo NO deberías usarlo? ¿Cómo lo escalas sin que todo explote? Es hora de ver los secretos que separan a un junior de un senior.

# Apache Airflow

## 5. Nivel Senior - Conceptos Avanzados: Dominando la Orquesta

Aquí es donde separamos a los seniors de los juniors. No se trata solo de escribir DAGs, sino de diseñar, operar y optimizar un sistema Airflow a escala.

### Trade-offs: Cuándo Usar y Cuándo NO Usar Airflow

> "No hay soluciones, solo trade-offs." — **Thomas Sowell**, *A Conflict of Visions* (1987)

Un ingeniero senior sabe que ninguna herramienta es una bala de plata.

**Use Airflow cuando:**
*   Sus flujos de trabajo son principalmente por lotes (batch).
*   Sus flujos de trabajo son complejos, con múltiples dependencias.
*   Quiere tratar sus pipelines como código (CI/CD, testing, versionado).
*   El ecosistema de proveedores (integraciones con Snowflake, Databricks, GCP, AWS, etc.) es valioso para usted.
*   La observabilidad y la capacidad de reejecutar tareas granularmente son críticas.

**NO use Airflow (o úselo con cuidado) cuando:**
*   Necesita procesamiento en tiempo real o streaming. Airflow es un orquestador de lotes, no un motor de streaming como Flink o Spark Streaming.
*   Necesita latencias de segundos. El Scheduler de Airflow tiene una sobrecarga y no está diseñado para tareas de muy baja latencia.
*   Sus tareas mueven grandes volúmenes de datos entre ellas. Airflow orquesta; no procesa. Usar XComs para pasar un DataFrame de 1GB es un anti-patrón terrible. Los datos deben residir en un sistema de almacenamiento externo (S3, GCS, HDFS) y las tareas deben pasarse punteros (ej: la ruta del archivo).
*   Su equipo no está cómodo con Python.

### Arquitectura de Airflow 2.x: Los Instrumentos de la Orquesta

Para escalar y solucionar problemas, debes conocer los componentes:

*   **Web Server**: La interfaz de usuario. Sirve la UI y habilita la API REST. Es stateless.
*   **Scheduler**: El cerebro. Monitoriza los DAGs, evalúa las dependencias y envía las tareas listas para ejecutar al Executor. En 2.x, puedes ejecutar múltiples schedulers en modo activo-activo para alta disponibilidad.
*   **Metadata Database**: El corazón. Generalmente PostgreSQL o MySQL. Almacena el estado de todos los DAGs, Tareas, Conexiones, etc. Es el único componente con estado y debe ser tratado con el máximo cuidado (backups, réplicas).
*   **Executor**: El músculo. Es el mecanismo que realmente ejecuta las tareas. La elección del executor es una de las decisiones arquitectónicas más importantes.

| Executor              | Descripción                                                                 | Caso de Uso Ideal                               | Complejidad |
| --------------------- | --------------------------------------------------------------------------- | ----------------------------------------------- | ----------- |
| **LocalExecutor**     | Ejecuta tareas en procesos paralelos en la misma máquina que el Scheduler.  | Desarrollo local, despliegues pequeños.         | Baja        |
| **CeleryExecutor**    | Distribuye tareas a un clúster de workers de Celery (usando RabbitMQ/Redis). | Cargas de trabajo grandes y distribuidas.       | Media       |
| **KubernetesExecutor**| Lanza un Pod de Kubernetes para cada tarea.                                 | Entornos nativos de la nube, aislamiento de dependencias. | Alta        |

Un error común es empezar con `LocalExecutor` y no planificar la migración. Un senior anticipa el crecimiento y elige `Celery` o `Kubernetes` desde el principio si la escala es un requisito.

### Anti-Patrones y Cómo Evitarlos

1.  **El Anti-Patrón del "Dios DAG"**: Un único DAG masivo que hace todo.
    *   **Por qué es malo**: Difícil de mantener, un fallo en una parte puede detener todo, difícil de depurar.
    *   **Solución**: Dividir en DAGs más pequeños y lógicos. Usar `TriggerDagRunOperator` para encadenar DAGs si es necesario. Aplicar el Principio de Responsabilidad Única a los DAGs.

2.  **Procesamiento Pesado en el Top-Level del Código del DAG**:
    *   **Por qué es malo**: El Scheduler de Airflow ejecuta el código de nivel superior de cada archivo DAG cada pocos segundos para "parsearlo". Si haces llamadas a APIs, consultas a BBDD o cualquier operación pesada aquí, estrangularás tu Scheduler.
    *   **Solución**: Toda la lógica pesada debe estar DENTRO de un operador (ej: en la función de un `PythonOperator`). El top-level solo debe contener la estructura del DAG.

3.  **Abuso de XComs**:
    *   **Por qué es malo**: XComs se almacenan en la base de datos de metadatos. Pasar grandes cantidades de datos (más de unos pocos KB) ralentizará toda tu instancia de Airflow.
    *   **Solución**: Pasar punteros a los datos (ej: `s3://my-bucket/data/{{ ds }}.parquet`). La API TaskFlow en Airflow 2.x puede configurarse para usar un backend de XComs externo (como S3) para mitigar esto, pero el principio sigue siendo el mismo.

4.  **Uso de `datetime.now()`**:
    *   **Por qué es malo**: Un DAG debe ser determinista. `datetime.now()` no lo es. Si tu DAG se reejecuta mañana (backfill), usará la fecha de mañana, no la fecha de la ejecución original.
    *   **Solución**: Usar siempre las variables de plantilla de Airflow como `{{ ds }}`, `{{ data_interval_start }}`, etc. Estas son fijas para cada `DagRun`.

### Optimizaciones y Escalabilidad

*   **Pools**: Limita el paralelismo para sistemas externos. Si tu API solo soporta 5 llamadas concurrentes, crea un pool con 5 "slots" y asigna las tareas correspondientes a ese pool.
*   **Afinación del Scheduler**: Ajusta parámetros como `scheduler.parsing_processes` o `scheduler.min_file_process_interval` en `airflow.cfg` para optimizar el rendimiento en instancias con muchos DAGs.
*   **Proveedores (Providers)**: En lugar de usar `BashOperator` para todo, usa los proveedores oficiales (`apache-airflow-providers-snowflake`, `apache-airflow-providers-google`, etc.). Delegan la ejecución al sistema externo, reduciendo la carga en tus workers y aprovechando la computación nativa de la plataforma de destino.
*   **Dynamic DAGs**: Si tienes 50 fuentes de datos que necesitan el mismo pipeline, no copies y pegues 50 DAGs. Escribe un script Python que genere los 50 objetos DAG dinámicamente. Esto es "Workflows-as-Code" en su máxima expresión.

## 6. Referencias y Citaciones Académicas: La Biblioteca del Maestro

Un verdadero experto conoce las fuentes primarias y se apoya en el conocimiento establecido.

1.  > "We are announcing that we are open sourcing Airflow, a workflow management platform that we’ve developed and have been using for more than a year. Airflow allows us to easily build and run complex data pipelines, making sure that each task is executed in the right order and that each task gets the required resources." — **Maxime Beauchemin**, *"Airflow: a workflow management platform"* (Airbnb Engineering & Data Science Blog, 2015). [Link](https://medium.com/airbnb-engineering/airflow-a-workflow-management-platform-46318b977d86)

2.  > "The Airflow scheduler monitors all tasks and all DAGs, and triggers the task instances whose dependencies have been met. Behind the scenes, it monitors and stays in sync with a folder for all DAG objects it may contain, and periodically (every minute or so) inspects active tasks to see whether they can be triggered." — **Apache Airflow Documentation**, *"Scheduler"*. [Link](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/scheduler.html)

3.  > "Idempotence is the property of certain operations in mathematics and computer science whereby they can be applied multiple times without changing the result beyond the initial application." — **Eric S. Raymond**, *The Jargon File*. (Una definición clásica de la cultura hacker).

4.  > "Data orchestration is the process of taking all the different systems, services, and data and combining them into a single, cohesive, and unified pipeline that can be executed, either on a schedule or on demand." — **Joe Reis, Matt Housley**, *Fundamentals of Data Engineering* (2022). (Coloca a Airflow en el contexto moderno de la ingeniería de datos).

5.  > "A directed graph is acyclic if it has no directed cycles; i.e., if there is no path that starts and ends at the same vertex. Every finite DAG has a topological ordering, a sequence of the vertices such that every edge is directed from an earlier to a later vertex in the sequence." — **Thomas H. Cormen et al.**, *Introduction to Algorithms, 3rd Edition* (2009). (El fundamento teórico de los DAGs desde el libro de texto de algoritmos por excelencia).

6.  > "With the Highly Available Scheduler, you can run multiple schedulers. This provides two benefits: The scheduler is no longer a single point of failure. If a scheduler node goes down, the other schedulers can take over its work." — **Apache Airflow Improvement Proposals (AIP-15)**, *"Scheduler High Availability"*. (Documentación de diseño que justifica un cambio arquitectónico clave).

7.  > "The TaskFlow API, introduced in Airflow 2.0, provides a new way of authoring DAGs that is more in line with traditional Python scripting." — **Astronomer.io Guides**, *"Introduction to the TaskFlow API"*. [Link](https://www.astronomer.io/guides/taskflow-api) (Referencia a una mejora de usabilidad clave en Airflow 2.0 de la principal empresa comercial detrás de Airflow).

8.  > "Conway's law: Organizations which design systems are constrained to produce designs which are copies of the communication structures of these organizations." — **Melvin E. Conway**, *How Do Committees Invent?* (1968). (Una cita profunda para un senior: la forma en que estructuras tus equipos de datos a menudo se reflejará en cómo estructuras tus DAGs. Equipos aislados crean DAGs aislados y frágiles. Equipos colaborativos crean pipelines de datos cohesivos).

---

Al llegar al final de esta guía, ya no deberías ver a Airflow como una simple herramienta, sino como una plataforma para aplicar principios de ingeniería de software a la ingeniería de datos. Entiendes su *porqué* histórico, su *qué* teórico y su *cómo* práctico y avanzado. Ahora puedes justificar por qué eliges un `KubernetesExecutor` sobre Celery, por qué insistes en que las tareas sean idempotentes y por qué un DAG bien diseñado es una forma de arte. Estás listo para dirigir la orquesta.