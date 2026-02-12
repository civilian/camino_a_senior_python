Entender la teoría de los DAGs es una cosa, pero ¿cómo se traduce eso en código que realmente funciona? Pasemos del 'qué' al 'cómo', transformando un frágil script de cron en un pipeline de Airflow elegante y robusto. Veremos cómo definir dependencias, manejar bifurcaciones y pasar información entre tareas.

# Apache Airflow

## 3. Evolución Histórica Detallada: Gigantes sobre Hombros de Gigantes

Airflow no surgió en el vacío. Es la culminación de una larga historia de intentos de domar la complejidad de la computación.

*   **Años 70**: Nace `cron` en los Laboratorios Bell de Unix. Es simple, robusto y revolucionario para su época. Es el abuelo de la automatización de tareas, pero ingenuo ante las dependencias.
*   **Años 90 - 2000**: Surgen herramientas de ETL comerciales como Informatica y DataStage. Ofrecen interfaces gráficas para construir flujos de trabajo, pero son cajas negras, caras y no se integran bien con el ecosistema de código.
*   **Principios de 2010**: La era del Big Data. Hadoop explota en popularidad, y con él, la necesidad de orquestar complejos trabajos de MapReduce. Nace **Apache Oozie**. Es potente pero notoriamente difícil de usar, con definiciones de flujo de trabajo en XML farragosos.
*   **2014**: Maxime Beauchemin, frustrado con las alternativas, aplica el mantra "software is eating the world" a la orquestación. Si todo es código, ¿por qué no los flujos de trabajo? Nace Airflow, con Python como su *lingua franca*. Esta decisión fue genial: Python ya era el lenguaje dominante en la ciencia de datos, lo que facilitó enormemente la adopción.

**Figuras Clave**:
*   **Maxime Beauchemin**: El creador. Su visión de "workflows-as-code" es el ADN de Airflow.
*   **Ash Berlin-Taylor**: Una de las figuras más importantes en la comunidad post-Airbnb, liderando el proyecto hacia la versión 2.0 y más allá. Es el actual PMC Chair de Airflow.

**Momento Decisivo**: El lanzamiento de **Airflow 2.0**. Antes de esto, el Scheduler era un único punto de fallo (SPOF). Si se caía, no se programaban nuevas tareas. La comunidad, en un esfuerzo hercúleo, lo rediseñó para ser altamente disponible, un cambio que elevó a Airflow de una herramienta potente a una plataforma de nivel empresarial.

## 4. Implementación Práctica: De la Teoría al Taller

Hablemos de código. Aquí es donde la goma se encuentra con el camino.

### Antes y Después: De Cron a un DAG

**El "Antes" (el infierno de cron y bash):**
Imagina un `crontab` así:
```bash
# crontab -e
0 1 * * * /usr/bin/bash /home/user/scripts/fetch_data.sh && /usr/bin/bash /home/user/scripts/process_data.sh && /usr/bin/bash /home/user/scripts/generate_report.sh
```
¿Qué pasa si `process_data.sh` falla? El informe no se genera. ¿Cómo lo reejecutas solo a él? ¿Cómo sabes que falló sin revisar logs manualmente? Es frágil.

**El "Después" (la elegancia de Airflow):**
```python
# dags/report_dag.py
from __future__ import annotations

import pendulum

from airflow.models.dag import DAG
from airflow.operators.bash import BashOperator

with DAG(
    dag_id="daily_report_generator",
    start_date=pendulum.datetime(2023, 1, 1, tz="UTC"),
    schedule_interval="0 1 * * *",
    catchup=False,
    doc_md="""
    ### Daily Report Generator
    
    Este DAG obtiene datos, los procesa y genera un informe diario.
    Es un ejemplo de un flujo de trabajo básico pero robusto.
    """,
    tags=["example", "reporting"],
) as dag:
    # Tarea 1: Obtener los datos.
    # Usamos BashOperator para ejecutar un script de shell, igual que en cron.
    fetch_data = BashOperator(
        task_id="fetch_data",
        bash_command="/home/user/scripts/fetch_data.sh --date {{ ds }}",
        doc_md="Obtiene los datos brutos de la fuente para una fecha específica."
    )

    # Tarea 2: Procesar los datos.
    # La tarea es idempotente: si se ejecuta de nuevo para la misma fecha, sobrescribe el resultado.
    process_data = BashOperator(
        task_id="process_data",
        bash_command="/home/user/scripts/process_data.sh --input /data/raw/{{ ds }} --output /data/processed/{{ ds }}",
    )

    # Tarea 3: Generar el informe.
    generate_report = BashOperator(
        task_id="generate_report",
        bash_command="/home/user/scripts/generate_report.sh --input /data/processed/{{ ds }} --output /reports/{{ ds }}.pdf",
    )

    # Definir las dependencias. Esto es el "Grafo Dirigido".
    # Se lee como: fetch_data debe completarse antes de que process_data comience,
    # y process_data debe completarse antes de que generate_report comience.
    fetch_data >> process_data >> generate_report
```
**¿Por qué es infinitamente mejor?**
1.  **Legibilidad**: Las dependencias son explícitas (`>>`).
2.  **Parametrización**: Usamos plantillas Jinja (`{{ ds }}`) para pasar la fecha de ejecución a los scripts, haciendo las tareas reutilizables e idempotentes.
3.  **Observabilidad**: Verás este DAG en la UI, con el estado de cada tarea (éxito, fallo, en ejecución).
4.  **Robustez**: Si `process_data` falla, Airflow lo reintentará según la configuración. Puedes borrar el estado de esa tarea y reejecutarla sin afectar a `fetch_data`.

### Caso de Estudio: Un Pipeline ELT con Bifurcación

Imagina que extraemos datos de usuarios. Si encontramos nuevos usuarios, queremos enriquecer sus perfiles y enviarles un email de bienvenida. Si no hay nuevos usuarios, no hacemos nada.

```python
# dags/user_onboarding_dag.py
from __future__ import annotations

import pendulum

from airflow.models.dag import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.email import EmailOperator
from airflow.utils.trigger_rule import TriggerRule

# --- Funciones de Python (lógica de negocio) ---
# En un proyecto real, estarían en módulos separados e importados.

def _extract_new_users(**kwargs):
    """
    Simula la extracción de nuevos usuarios.
    Devuelve una lista de IDs de usuario. Pasa esta lista a la siguiente tarea vía XCom.
    """
    print("Extrayendo nuevos usuarios...")
    # Lógica para conectar a la BBDD y obtener usuarios desde la última ejecución.
    new_user_ids = [101, 205, 312] # Simulación
    if new_user_ids:
        ti = kwargs["ti"]
        ti.xcom_push(key="new_user_ids", value=new_user_ids)
        return "enrich_user_profiles" # Nombre de la task_id a la que bifurcar
    else:
        return "no_new_users_detected" # Nombre de la otra task_id

def _enrich_profiles(**kwargs):
    """
    Toma los IDs de usuario de XCom y enriquece sus perfiles.
    """
    ti = kwargs["ti"]
    user_ids = ti.xcom_pull(key="new_user_ids", task_ids="extract_new_users")
    print(f"Enriqueciendo perfiles para los usuarios: {user_ids}")
    # Lógica para llamar a APIs externas, etc.
    
def _send_welcome_emails(**kwargs):
    """
    Envía emails de bienvenida.
    """
    ti = kwargs["ti"]
    user_ids = ti.xcom_pull(key="new_user_ids", task_ids="extract_new_users")
    print(f"Enviando emails de bienvenida a {len(user_ids)} usuarios.")

# --- Definición del DAG ---

with DAG(
    dag_id="user_onboarding_pipeline",
    start_date=pendulum.datetime(2023, 1, 1, tz="UTC"),
    schedule_interval="@daily",
    catchup=False,
    tags=["onboarding", "elt"],
) as dag:
    
    extract_new_users = BranchPythonOperator(
        task_id="extract_new_users",
        python_callable=_extract_new_users,
    )

    enrich_user_profiles = PythonOperator(
        task_id="enrich_user_profiles",
        python_callable=_enrich_profiles,
    )

    send_welcome_emails = PythonOperator(
        task_id="send_welcome_emails",
        python_callable=_send_welcome_emails,
    )
    
    # Una tarea "dummy" para marcar el final de la rama "sin usuarios"
    no_new_users_detected = PythonOperator(
        task_id="no_new_users_detected",
        python_callable=lambda: print("No se encontraron nuevos usuarios. Finalizando."),
    )

    # Una tarea final que se ejecuta sin importar qué rama se tomó.
    # Nota el trigger_rule: se ejecuta si al menos uno de sus padres tuvo éxito.
    pipeline_complete = EmailOperator(
        task_id="pipeline_complete_notification",
        to="data_team@example.com",
        subject="User Onboarding Pipeline Completed for {{ ds }}",
        html_content="<h3>Pipeline Finished</h3><p>The user onboarding pipeline has finished its daily run.</p>",
        trigger_rule=TriggerRule.ONE_SUCCESS,
    )

    # Definición de dependencias
    extract_new_users >> [enrich_user_profiles, no_new_users_detected]
    enrich_user_profiles >> send_welcome_emails
    [send_welcome_emails, no_new_users_detected] >> pipeline_complete

```
Este DAG muestra patrones avanzados:
*   **`BranchPythonOperator`**: Permite que el flujo del DAG tome diferentes caminos basándose en el resultado de una función.
*   **XComs (Cross-communications)**: `xcom_push` y `xcom_pull` permiten a las tareas pasarse pequeñas cantidades de metadatos.
*   **`TriggerRule`**: Controla la lógica de ejecución de una tarea en función del estado de sus predecesores. `TriggerRule.ONE_SUCCESS` es crucial para unir las ramas de una bifurcación.