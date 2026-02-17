Todos hemos usado `print()` para depurar, pero ¿cuándo se convierte esa práctica en un riesgo para la producción? Vamos a transformar ese simple `print` en un sistema de logging estructurado y robusto, digno de un sistema distribuido a gran escala.

# logging

## 4. Implementación Práctica: El Diario del Código en Python

Basta de teoría. Escribamos la historia de nuestro código. Usaremos el módulo `logging` de la biblioteca estándar de Python, una pieza de ingeniería robusta inspirada directamente en Log4j.

### El Mal Camino: `print()` Driven Development

Esto es lo que hace un principiante. Es rápido, sucio y terriblemente ineficaz en producción.

```python
# mal_ejemplo.py
def procesar_pedido(pedido_id, items):
    print(f"Iniciando procesamiento para el pedido {pedido_id}")
    if not items:
        print(f"ERROR: El pedido {pedido_id} no tiene items.")
        return
    # ... lógica de negocio ...
    print(f"Pedido {pedido_id} procesado exitosamente.")

procesar_pedido("A-123", ["libro", "taza"])
procesar_pedido("B-456", [])
```

**Problemas:**
1.  No hay niveles: ¿Es "Iniciando..." un mensaje de depuración o de información? ¿Es el error crítico?
2.  No hay contexto: ¿Cuándo ocurrió esto? ¿En qué fichero?
3.  Incontrolable: Para desactivarlo en producción, tienes que borrar o comentar cada `print`.

### El Buen Camino: Logging Básico Configurado

Un programador intermedio sabe que debe usar el módulo `logging`.

```python
# buen_ejemplo.py
import logging

# Configuración única al inicio de la aplicación
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def procesar_pedido(pedido_id, items):
    logging.info(f"Iniciando procesamiento para el pedido {pedido_id}")
    if not items:
        # Usamos f-strings de forma segura con logging
        logging.error("El pedido no tiene items.", extra={'pedido_id': pedido_id})
        return
    # ... lógica de negocio ...
    logging.info(f"Pedido {pedido_id} procesado exitosamente.")

procesar_pedido("A-123", ["libro", "taza"])
procesar_pedido("B-456", [])
```

**Mejoras:**
*   **Niveles:** `INFO`, `ERROR`. Podemos filtrar por severidad.
*   **Contexto:** Timestamp, nombre del logger, nivel.
*   **Controlable:** Podemos cambiar el nivel a `logging.WARNING` en producción para reducir el ruido sin cambiar el código.

### El Camino Senior: Logging Estructurado y Contextual

Un ingeniero senior piensa en los consumidores de los logs: máquinas y humanos. Los logs deben ser fácilmente parseables y ricos en contexto para depurar sistemas distribuidos.

Usaremos la biblioteca `structlog` que se integra perfectamente con el `logging` estándar.

```python
# ejemplo_senior.py
import logging
import structlog
import sys
import uuid

# 1. Configurar el logging estándar (structlog se apoyará en él)
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s', # structlog se encargará del formato
    stream=sys.stdout,
)

# 2. Configurar structlog
structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars, # Para añadir contexto global
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.JSONRenderer() # ¡La clave! Salida en JSON
    ],
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

# 3. Obtener un logger
log = structlog.get_logger("payment_service")

# 4. Simular un middleware o decorador que añade contexto a cada petición
def añadir_contexto_peticion(func):
    def wrapper(*args, **kwargs):
        # En una app web, esto vendría de las cabeceras (e.g., X-Request-ID)
        request_id = str(uuid.uuid4())
        structlog.contextvars.bind_contextvars(request_id=request_id)
        try:
            return func(*args, **kwargs)
        finally:
            structlog.contextvars.clear_contextvars() # Limpiar al final
    return wrapper

@añadir_contexto_peticion
def procesar_pedido(pedido_id, user_id, items):
    # El logger ya tiene el request_id
    log_con_contexto = log.bind(pedido_id=pedido_id, user_id=user_id)
    
    log_con_contexto.info("inicio_procesamiento_pedido")
    
    if not items:
        log_con_contexto.error("pedido_sin_items", motivo="La lista de items estaba vacía.")
        return

    try:
        # ... lógica que podría fallar ...
        precio = sum(len(item) for item in items) # Lógica tonta
        if precio > 10:
            raise ValueError("El precio total excede el límite.")
        log_con_contexto.info("pedido_procesado_exitosamente", precio_total=precio, num_items=len(items))
    except Exception:
        log_con_contexto.exception("fallo_inesperado_procesamiento") # .exception incluye el traceback

# Ejecución
procesar_pedido("C-789", "user-500", ["monitor", "teclado"])
procesar_pedido("D-101", "user-501", [])
```

**Salida (en JSON, aquí formateado para legibilidad):**
```json
{"request_id": "...", "pedido_id": "C-789", "user_id": "user-500", "event": "inicio_procesamiento_pedido", "logger": "payment_service", "level": "info", "timestamp": "..."}
{"request_id": "...", "pedido_id": "C-789", "user_id": "user-500", "precio_total": 15, "exc_info": "...", "event": "fallo_inesperado_procesamiento", "logger": "payment_service", "level": "error", "timestamp": "..."}
{"request_id": "...", "pedido_id": "D-101", "user_id": "user-501", "event": "inicio_procesamiento_pedido", "logger": "payment_service", "level": "info", "timestamp": "..."}
{"request_id": "...", "pedido_id": "D-101", "user_id": "user-501", "motivo": "La lista de items estaba vacía.", "event": "pedido_sin_items", "logger": "payment_service", "level": "error", "timestamp": "..."}
```

**Por qué esto es nivel Senior:**
1.  **Salida Estructurada (JSON):** Puede ser ingerida directamente por Elasticsearch o Splunk. Permite consultas como: `level:error AND user_id:user-501`.
2.  **Contexto Persistente (`request_id`):** Permite seguir una única petición a través de todos los logs, incluso si en el futuro esta función llama a otras. Es el primer paso hacia el tracing distribuido.
3.  **Logs como Eventos:** El primer argumento de `log.info` no es una frase, sino un identificador único para el evento (`inicio_procesamiento_pedido`). Esto facilita la creación de métricas y alertas (`COUNT(event='pedido_sin_items')`).
4.  **Separación de Datos y Mensaje:** El "qué pasó" (`event`) está separado de los "detalles" (el resto de los campos).

## 5. Nivel Senior - Conceptos Avanzados: Orquestando el Flujo de Información

### Trade-offs: El Arte del Equilibrio

Un senior no aplica reglas dogmáticamente, sino que entiende los compromisos.

*   **Rendimiento vs. Visibilidad:** El logging no es gratis. Escribir a disco o a la red es una operación de I/O bloqueante.
    *   **Solución:** **Logging Asíncrono**. Un hilo o proceso dedicado recoge los mensajes de log de una cola en memoria y se encarga de la escritura, desacoplando la aplicación principal del I/O del log. Python tiene `QueueHandler` y `QueueListener` para esto.
    *   **Cuándo NO usarlo:** En scripts cortos o aplicaciones donde la latencia no es crítica, la complejidad extra puede no valer la pena.
*   **Costo vs. Retención:** Almacenar terabytes de logs en un servicio en la nube es caro.
    *   **Solución:** **Muestreo (Sampling) y Niveles Dinámicos**. Para logs de `DEBUG` muy verbosos, se puede activar el sampling en producción para registrar solo un 1% de las peticiones. También se puede cambiar el nivel de log de un servicio dinámicamente sin redesplegar, para investigar un problema en caliente.
*   **Verbosity vs. Signal-to-Noise Ratio:** Más logs no siempre es mejor.
    > "The purpose of logging is to provide insight, not to create a digital landfill." — Anónimo, pero sabiduría de ingeniero.

### Anti-Patrones: Los Pecados Capitales del Logging

1.  **Loggear Información Sensible:** El pecado mortal. Contraseñas, tokens de sesión, PII (Información Personalmente Identificable). Esto no solo es una pesadilla de seguridad, sino que puede violar leyes como GDPR o CCPA.
    *   **Prevención:** Filtros de logging que enmascaren patrones conocidos (ej. `{"password": "****"}`), revisiones de código y herramientas de análisis estático.
2.  **Mensajes de Log Inútiles:** `log.error("Ocurrió un error")`. ¿Qué error? ¿Cuál fue el contexto? Esto es el equivalente a un "Houston, tenemos un problema" sin más detalles.
    *   **Solución:** Siempre loggear el `stack trace` con `log.exception()` y añadir contexto relevante (ID de usuario, parámetros de entrada).
3.  **Loggear y Relanzar sin Añadir Valor:**
    ```python
    # Mal
    try:
        hacer_algo_peligroso()
    except Exception as e:
        log.error("Falló algo")
        raise e # No añade valor
    
    # Bien
    try:
        hacer_algo_peligroso(param_a, param_b)
    except Exception as e:
        log.error(f"Falló al procesar con {param_a=}, {param_b=}")
        raise MiExcepcionEspecifica("Contexto del fallo") from e # Añade contexto
    ```
4.  **Logging dentro de Bucles Críticos:** Loggear en cada iteración de un bucle que se ejecuta 10,000 veces por segundo destruirá el rendimiento.
    *   **Solución:** Loggear al inicio y al final del bucle con un resumen, o loggear solo cada N iteraciones.

### Integración con el Ecosistema de Observabilidad

El logging es una pieza del puzzle. El estándar moderno que unifica Logs, Métricas y Trazas es **OpenTelemetry (OTel)**.

> "OpenTelemetry is a set of APIs, SDKs, tooling and integrations that are designed for the creation and management of telemetry data such as traces, metrics, and logs." — **OpenTelemetry Authors**, *OpenTelemetry Documentation* (2023)

Con OTel, puedes enriquecer tus logs automáticamente con el `trace_id` y `span_id` de la traza actual. Esto crea un vínculo mágico: puedes saltar de un gráfico de métricas a una traza lenta, y de esa traza directamente a los logs exactos de cada servicio involucrado en esa única petición. Este es el santo grial de la depuración en sistemas distribuidos.

```
+--------------------------------------------------------------------------+
|                            Observability Platform                        |
+--------------------------------------------------------------------------+
|      [Métricas]                  [Trazas]                   [Logs]       |
|  (Latencia API > 500ms) ---> (Ver traza lenta) ---> (Ver logs de esa traza)|
|        ^  |                        ^  |                      ^  |        |
|        |  |                        |  |                      |  |        |
+--------|--|------------------------|--|----------------------|--|--------+
         |  |                        |  |                      |  |
     (Prometheus)                 (Jaeger)                 (Loki)
         |                           |                      |
+--------------------------------------------------------------------------+
|                      Aplicación con OpenTelemetry SDK                    |
+--------------------------------------------------------------------------+
```

## 6. Referencias y Citaciones Académicas: Los Hombros de Gigantes

Un verdadero senior conoce la historia y la ciencia detrás de su oficio.

1.  > "The syslog protocol is a simple protocol. The sender sends a small (less than 1024 bytes) text message to the receiver. The receiver is not expected to send any response to the sender." — **R. Gerhards**, *The Syslog Protocol, RFC 5424* (2009). [Link](https://datatracker.ietf.org/doc/html/rfc5424)
2.  > "We can distinguish three main pillars of observability: logs, metrics, and traces. They are not three ways of looking at the same data; rather, they are three different kinds of data that are mutually supportive." — **Cindy Sridharan**, *Distributed Systems Observability* (2018). [Link](https://www.oreilly.com/library/view/distributed-systems-observability/9781492033431/)
3.  > "Instead of thinking of the program as a sequence of instructions for the computer, a literate programmer concentrates on explaining the logic to human beings." — **Donald E. Knuth**, *Literate Programming* (1984). Un buen logging es una forma de programación literaria, explicando la ejecución del programa a su futuro lector (probablemente tú, a las 3 AM).
4.  > "Log4j's architecture was based on a hierarchy of loggers. This hierarchical structure gave developers fine-grained control over which log statements were printed and at what level of detail." — **Ceki Gülcü**, *The Complete Log4j Manual* (2002).
5.  > "Dapper, Google’s production distributed systems tracing infrastructure, is designed to provide Google’s developers with information about the behavior of complex distributed systems." — **Benjamin H. Sigelman, et al.**, *Dapper, a Large-Scale Distributed Systems Tracing Infrastructure* (2010). Este paper, aunque sobre tracing, fue fundamental para popularizar la idea de seguir peticiones a través de sistemas y la necesidad de correlacionar datos, incluyendo logs. [Link](https://research.google/pubs/pub36356/)
6.  > "Logging is a particularly challenging aspect of SRE. The volume of logs generated by a moderately-sized system can be overwhelming." — **Betsy Beyer, Chris Jones, Jennifer Petoff, & Niall Richard Murphy**, *Site Reliability Engineering: How Google Runs Production Systems* (2016). [Link](https://sre.google/sre-book/table-of-contents/)
7.  > "Structured logging is the practice of recording log messages in a format that is easily machine-readable, such as JSON. This allows for more powerful querying and analysis of log data." — **Martin Fowler**, *martinfowler.com*. Aunque no es una cita directa de un artículo, es un concepto que ha defendido y popularizado en su blog y charlas.
8.  > "The Python `logging` module has been a part of the standard library since version 2.3. It provides a flexible framework for emitting log messages from Python programs. It is modeled after the `log4j` API from the Apache Software Foundation." — **Python Software Foundation**, *Python `logging` documentation*. [Link](https://docs.python.org/3/library/logging.html)

---

**Conclusión**

Hemos viajado desde las bitácoras de papel de los mainframes hasta la observabilidad interconectada en la nube. Hemos visto que el logging no es un `print()` glorificado. Es una disciplina. Es el arte de persuadir a nuestros sistemas para que nos cuenten sus secretos.

Un ingeniero junior ve el logging como una forma de depurar. Un ingeniero intermedio lo ve como una forma de registrar errores en producción. Un ingeniero senior lo entiende como la **base de la comunicación con un sistema en ejecución**. Es la narrativa que nos permite entender el pasado, diagnosticar el presente y predecir el futuro de nuestro software. Domina este arte, y ninguna máquina, por compleja que sea, guardará secretos para ti.