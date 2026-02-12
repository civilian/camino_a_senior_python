La teoría es fascinante, pero ¿cómo se ve un flujo de trabajo de Oozie en el mundo real? Vamos a dejar de lado los diagramas y a construir, paso a paso, un pipeline de datos funcional, desde el script generador hasta su ejecución en el clúster.

# Apache Oozie

---

### 4. Implementación Práctica: Del Concepto al Clúster

Basta de teoría. Vamos a ensuciarnos las manos. Un error común es pensar que se debe escribir el XML a mano. Un ingeniero senior sabe que debe generar estos artefactos mediante scripts para mantener la cordura y la reproducibilidad.

Usaremos Python para generar un flujo de trabajo simple:
1.  Un script de **Pig** para limpiar datos de entrada.
2.  Una consulta de **Hive** para agregar los datos limpios.

#### **Estructura de Archivos en HDFS**

Antes de ejecutar, necesitamos esta estructura en HDFS:

```
/user/senior_dev/oozie_project/
├── workflow.xml
├── job.properties
├── lib/
│   └── pig/
│       └── clean_data.pig
│   └── hive/
│       └── aggregate_data.hql
└── input-data/
    └── raw.txt
```

#### **Paso 1: El Script de Python Generador**

Este script creará los archivos `workflow.xml` y `job.properties`.

```python
# generator.py
import os

# --- Definición del Flujo de Trabajo (La Lógica) ---
WORKFLOW_XML_TEMPLATE = """
<workflow-app name="Simple-ETL-Workflow" xmlns="uri:oozie:workflow:0.5">
    <start to="clean_data_pig"/>

    <action name="clean_data_pig">
        <pig>
            <job-tracker>{jobTracker}</job-tracker>
            <name-node>{nameNode}</name-node>
            <script>${{nameNode}}/user/senior_dev/oozie_project/lib/pig/clean_data.pig</script>
            <param>INPUT=${{inputDir}}</param>
            <param>OUTPUT=${{cleanOutputDir}}</param>
        </pig>
        <ok to="aggregate_data_hive"/>
        <error to="fail"/>
    </action>

    <action name="aggregate_data_hive">
        <hive xmlns="uri:oozie:hive-action:0.5">
            <job-tracker>{jobTracker}</job-tracker>
            <name-node>{nameNode}</name-node>
            <script>${{nameNode}}/user/senior_dev/oozie_project/lib/hive/aggregate_data.hql</script>
            <param>INPUT_TABLE_PATH=${{cleanOutputDir}}</param>
            <param>OUTPUT_TABLE_PATH=${{finalOutputDir}}</param>
        </hive>
        <ok to="end"/>
        <error to="fail"/>
    </action>

    <kill name="fail">
        <message>Workflow fallido, mensaje de error: [${{wf:errorMessage(wf:lastErrorNode())}}]</message>
    </kill>

    <end name="end"/>
</workflow-app>
"""

JOB_PROPERTIES_TEMPLATE = """
nameNode=hdfs://localhost:9000
jobTracker=localhost:8032
queueName=default
oozie.use.system.libpath=true
oozie.wf.application.path=${{nameNode}}/user/senior_dev/oozie_project

# Parámetros de la aplicación
inputDir=${{nameNode}}/user/senior_dev/oozie_project/input-data
cleanOutputDir=${{nameNode}}/user/senior_dev/oozie_project/cleaned-data
finalOutputDir=${{nameNode}}/user/senior_dev/oozie_project/final-output
"""

def generate_oozie_files():
    """Genera los archivos de configuración de Oozie."""
    
    # Llenar las plantillas con valores (en un caso real, podrían venir de un config)
    # Aquí, los placeholders como {jobTracker} son para claridad. Oozie los resolverá
    # desde job.properties.
    workflow_content = WORKFLOW_XML_TEMPLATE.format(
        jobTracker="${jobTracker}",
        nameNode="${nameNode}"
    )
    
    with open("workflow.xml", "w") as f:
        f.write(workflow_content)
        print("workflow.xml generado.")

    with open("job.properties", "w") as f:
        f.write(JOB_PROPERTIES_TEMPLATE)
        print("job.properties generado.")

if __name__ == "__main__":
    generate_oozie_files()
```

#### **Paso 2: Los Scripts de Pig y Hive**

**`clean_data.pig`**:
```pig
-- Carga los datos crudos
raw_logs = LOAD '$INPUT' USING PigStorage(',') AS (user_id:chararray, event:chararray, timestamp:long);
-- Filtra eventos nulos
filtered_logs = FILTER raw_logs BY event IS NOT NULL;
-- Almacena los datos limpios
STORE filtered_logs INTO '$OUTPUT' USING PigStorage(',');
```

**`aggregate_data.hql`**:
```hql
-- Crea una tabla externa sobre los datos limpios de Pig
CREATE EXTERNAL TABLE IF NOT EXISTS cleaned_logs (
    user_id STRING,
    event STRING,
    timestamp BIGINT
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
LOCATION '${INPUT_TABLE_PATH}';

-- Crea la tabla final
CREATE EXTERNAL TABLE IF NOT EXISTS event_counts (
    event STRING,
    total INT
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
LOCATION '${OUTPUT_TABLE_PATH}';

-- Agrega los datos y los inserta en la tabla final
INSERT OVERWRITE TABLE event_counts
SELECT event, COUNT(1) as total
FROM cleaned_logs
GROUP BY event;
```

#### **Paso 3: Despliegue y Ejecución**

1.  **Generar los archivos:** `python generator.py`
2.  **Subir todo a HDFS:**
    ```bash
    hdfs dfs -mkdir -p /user/senior_dev/oozie_project/lib/{pig,hive}
    hdfs dfs -put workflow.xml job.properties /user/senior_dev/oozie_project/
    hdfs dfs -put lib/pig/clean_data.pig /user/senior_dev/oozie_project/lib/pig/
    hdfs dfs -put lib/hive/aggregate_data.hql /user/senior_dev/oozie_project/lib/hive/
    # ...y también los datos de entrada
    ```
3.  **Ejecutar el trabajo:**
    ```bash
    oozie job -config job.properties -run
    ```

#### **Comparaciones: "Antes vs Después" y "Mal vs Bien"**

*   **Antes (Script de Shell frágil):**
    ```bash
    pig -f clean_data.pig && hive -f aggregate_data.hql
    # ¿Qué pasa si pig falla? ¿Y si el clúster está ocupado? ¿Cómo reintento?
    # No hay estado, no hay visibilidad.
    ```
*   **Después (Oozie):**
    Un flujo de trabajo robusto, monitorizable, con reintentos configurables y manejo de errores explícito. El servidor de Oozie mantiene el estado en una base de datos, por lo que incluso si el servidor se reinicia, el flujo de trabajo puede reanudarse.

*   **Mal Patrón (Monolito):**
    Un `workflow.xml` de 2000 líneas que hace todo. Es imposible de depurar, reutilizar o entender.
*   **Buen Patrón (Modular con Sub-workflows):**
    Un flujo de trabajo principal que orquesta `sub-workflows` más pequeños y reutilizables (ej. un sub-workflow para "Ingesta", otro para "Limpieza").
    ```xml
    <action name="run_ingestion_logic">
        <sub-workflow>
            <app-path>${ingestionWorkflowPath}</app-path>
            <propagate-configuration/>
        </sub-workflow>
        <ok to="next_step"/>
        <error to="fail"/>
    </action>
    ```