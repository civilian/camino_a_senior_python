# logging

Absolutamente. Abordemos el logging no como una simple tarea de imprimir mensajes, sino como una disciplina de ingeniería fundamental para construir, operar y mantener software robusto a escala. Esta guía está diseñada para llevarte de un entendimiento básico a una mentalidad de nivel Senior.

***

# Guía Profunda de Logging para el Ingeniero de Software Senior

## Introducción: El Vuelo 8501 y la Caja Negra del Software

El 28 de diciembre de 2014, el vuelo 8501 de AirAsia se estrelló, cobrando la vida de 162 personas. La investigación fue posible gracias a la "caja negra" (Flight Data Recorder). Esta caja no prevenía el accidente, pero registraba cada parámetro crítico, cada acción del piloto y cada alerta del sistema, permitiendo a los ingenieros entender *exactamente* qué falló y por qué.

**El logging es la caja negra de tu aplicación.**

Un desarrollador junior ve el logging como una forma de depurar (`print("llegué aquí")`). Un desarrollador senior lo ve como el sistema nervioso central de la aplicación: un flujo de eventos telemetricos que permite la depuración, el monitoreo, la auditoría de seguridad, el análisis de negocio y la respuesta a incidentes.

> "Logging is a cross-cutting concern. A concern that affects the entire application and should be centralized in one place."
> — Martin Fowler

---

## Parte I: Los Fundamentos - Más Allá de `console.log`

### 1. ¿Qué es un Log? La Anatomía de un Evento

Un log no es solo un string. Un log es un **registro inmutable y con marca de tiempo de un evento discreto que ocurrió en el sistema.** Un evento de log bien formado debe responder a las siguientes preguntas:

-   **¿Cuándo ocurrió?** (Timestamp de alta precisión, ej. `2023-10-27T10:00:00.12345Z`)
-   **¿Dónde ocurrió?** (Servicio, nombre de la máquina, función, línea de código)
-   **¿Con qué severidad?** (Nivel de Log: `DEBUG`, `INFO`, `ERROR`)
-   **¿Qué ocurrió?** (El mensaje descriptivo)
-   **¿En qué contexto?** (Datos relevantes: `userID`, `transactionID`, `requestID`)

### 2. Los Niveles de Logging: El Lenguaje Universal (RFC 5424)

Los niveles de log no son arbitrarios. Son un contrato entre tu código y quien lo opera. El estándar de facto, derivado de Syslog ([RFC 5424](https://tools.ietf.org/html/rfc5424)), define las siguientes severidades. Un senior entiende el *público* de cada nivel.

| Nivel      | Público Objetivo          | Propósito y Ejemplo                                                                                                     | ¿Debería estar en Producción? |
| :--------- | :------------------------ | :---------------------------------------------------------------------------------------------------------------------- | :--------------------------- |
| **TRACE**  | Desarrollador (Depuración) | El flujo más granular. "Entrando a la función `calculatePrice` con argumentos `(x, y)`". Útil para seguir la lógica paso a paso. | No (demasiado ruidoso)       |
| **DEBUG**  | Desarrollador (Depuración) | Información de diagnóstico detallada. "Valor de la variable `discount` es 0.15". "Conexión a la base de datos establecida".  | No (generalmente)            |
| **INFO**   | Operaciones / Soporte     | Eventos de alto nivel que marcan el progreso normal de la aplicación. "Usuario `123` ha iniciado sesión". "Orden `ABC` procesada". | **Sí**                       |
| **WARN**   | Operaciones / Soporte     | Un evento inesperado o anómalo que no rompe la funcionalidad actual, pero que podría indicar un problema futuro. "El servicio de pago tardó 3 segundos en responder". "Reintento de conexión a la API #2". | **Sí**                       |
| **ERROR**  | Operaciones / Desarrollador | Un error que impidió que una operación específica se completara, pero la aplicación sigue funcionando. "No se pudo procesar el pago para la orden `ABC` debido a fondos insuficientes". | **Sí (con alertas)**         |
| **FATAL/CRITICAL** | Operaciones / Desarrollador | Un error severo que causa que la aplicación (o un subsistema crítico) se detenga o quede en un estado inoperable. "No se puede conectar a la base de datos principal. La aplicación se va a detener". | **Sí (con alertas críticas)** |

**Principio Senior:** El nivel de log de una aplicación en producción debe ser configurable en tiempo de ejecución sin necesidad de un redespliegue. Esto permite activar `DEBUG` temporalmente para diagnosticar un incidente en vivo.

---

## Parte II: La Práctica de Nivel Senior - El Arte y la Ciencia

Aquí es donde se separa un desarrollador promedio de uno excepcional.

### 1. Structured Logging: La Piedra Angular

El mayor salto de madurez en logging es pasar de logs no estructurados a **logs estructurados**.

-   **No Estructurado (Mal):**
    ```
    INFO: User 12345 checked out with cart 67890 for a total of $99.50.
    ```
    Esto es fácil de leer para un humano, pero es una pesadilla para una máquina. Para encontrar todos los checkouts de más de $50, necesitas usar expresiones regulares complejas y lentas.

-   **Estructurado (Excelente):**
    ```json
    {
      "timestamp": "2023-10-27T10:05:15.345Z",
      "level": "INFO",
      "message": "User checkout successful",
      "service": "payment-api",
      "app_version": "1.2.3",
      "event": {
        "name": "user_checkout",
        "domain": "ecommerce"
      },
      "user": {
        "id": "12345",
        "ip_address": "203.0.113.75"
      },
      "cart": {
        "id": "67890",
        "item_count": 5,
        "total_amount": 99.50,
        "currency": "USD"
      }
    }
    ```
    **¿Por qué es superior?**
    -   **Parseable por Máquinas:** Puedes consultar tus logs como si fueran una base de datos: `level=ERROR AND cart.total_amount > 1000`.
    -   **Consistente:** La estructura obliga a un formato común en todos los servicios.
    -   **Enriquecido:** Permite añadir contexto sin ensuciar el mensaje principal.

Librerías como [Serilog](https://serilog.net/) (.NET), [Winston](https://github.com/winstonjs/winston) (Node.js), o [Logrus](https://github.com/sirupsen/logrus) (Go) son excelentes para esto.

### 2. El Contexto es Rey: IDs de Correlación

En una arquitectura de microservicios, una sola petición de usuario puede viajar a través de 5, 10 o 20 servicios. ¿Cómo sigues el rastro de esa petición?

**Correlation ID (o Trace ID):** Un identificador único que se genera en el borde de tu sistema (ej. API Gateway) y se propaga en las cabeceras (`X-Request-ID`, `traceparent`) de cada llamada subsecuente entre servicios.

**Cada log que escribas DEBE incluir este ID de correlación.**

```json
// Log del Servicio A
{ "level": "INFO", "message": "Received new order", "trace_id": "abc-123-xyz" }

// Log del Servicio B
{ "level": "INFO", "message": "Processing payment", "trace_id": "abc-123-xyz" }

// Log del Servicio C
{ "level": "ERROR", "message": "Inventory not available", "trace_id": "abc-123-xyz" }
```

Ahora, con una simple consulta por `trace_id: "abc-123-xyz"`, puedes reconstruir la historia completa de la petición a través de todo el sistema. Esto es la base del **Distributed Tracing**.

### 3. ¡No Loguees Información Sensible!

Esto no es negociable. Loguear PII (Personally Identifiable Information), contraseñas, tokens de sesión, números de tarjeta de crédito, etc., es una brecha de seguridad masiva y una violación de regulaciones como GDPR o HIPAA.

**Prácticas Senior:**
-   Usa "log scrubbing" o "masking" a nivel de la librería de logging para filtrar automáticamente patrones conocidos (ej. números de tarjeta de crédito).
-   Nunca loguees el cuerpo completo de una petición o respuesta sin antes sanitizarlo.
-   Sé explícito sobre qué se puede loguear. En lugar de `log.debug(userObject)`, haz `log.debug({ userID: userObject.id, username: userObject.username })`.

### 4. El Rendimiento Importa

El logging no es gratis. Escribir a disco o a la red es una operación de I/O lenta.

-   **Logging Asíncrono:** La mayoría de las librerías de logging modernas escriben a un buffer en memoria y un hilo separado se encarga de enviarlo al destino (consola, archivo, red). Esto evita que tu hilo de aplicación se bloquee. Asegúrate de que tu framework lo use.
-   **Sampling:** Para logs de muy alta frecuencia (ej. `TRACE` en un sistema de trading), no puedes loguear el 100% de los eventos. Se usan técnicas de muestreo (ej. loguear 1 de cada 1000 peticiones) para obtener una visión representativa sin sobrecargar el sistema.
-   **Cuidado con la Serialización:** Loguear objetos complejos puede consumir mucho CPU para serializarlos a JSON. Loguea solo los campos necesarios.

---

## Parte III: La Arquitectura de Logging Moderna (The "Stack")

Un senior no solo escribe logs, diseña el sistema que los procesa. El flujo típico es:

**Aplicación -> Agente/Shipper -> Agregador/Backend -> Visualización**

1.  **Aplicación (Generación):** Tu código usa una librería de logging (Log4j, Serilog, Winston) para escribir logs estructurados, generalmente a `stdout`. ¿Por qué `stdout`? Porque se alinea con los principios de [The Twelve-Factor App](https://12factor.net/logs), que trata los logs como un flujo de eventos.

2.  **Agente/Shipper (Recolección y Envío):** Un agente ligero se ejecuta en la misma máquina o contenedor que tu aplicación (ej. [Fluentd](https://www.fluentd.org/), [Vector](https://vector.dev/), [Logstash](https://www.elastic.co/logstash)). Su trabajo es:
    -   Leer los logs de `stdout` (o archivos).
    -   Parsearlos y enriquecerlos (ej. añadir metadata del host o del contenedor).
    -   Enviarlos en batches a un sistema centralizado.

3.  **Agregador/Backend (Almacenamiento e Indexación):** Un sistema distribuido diseñado para ingerir, almacenar e indexar volúmenes masivos de datos de log.
    -   **[Elasticsearch](https://www.elastic.co/elasticsearch/):** El estándar de la industria, parte del stack ELK (Elasticsearch, Logstash, Kibana).
    -   **[Loki](https://grafana.com/oss/loki/):** Un enfoque más ligero de Grafana, inspirado en Prometheus. Indexa solo metadata (labels), no el texto completo del log, haciéndolo más económico.
    -   **[Splunk](https://www.splunk.com/):** Una solución comercial muy potente.

4.  **Visualización y Alerta (Análisis):** La interfaz donde los humanos interactúan con los logs.
    -   **[Kibana](https://www.elastic.co/kibana/):** La 'K' en el stack ELK. Permite buscar, crear dashboards y visualizar datos de Elasticsearch.
    -   **[Grafana](https://grafana.com/):** La 'G' en el stack PLG (Prometheus, Loki, Grafana). Excelente para correlacionar logs con métricas.

---

## Parte IV: Conceptos Avanzados - Observabilidad

El logging es uno de los **Tres Pilares de la Observabilidad**. Un sistema es "observable" si puedes entender su estado interno simplemente observando sus salidas externas.

> "Observability is a property of a system. Monitoring is an activity we do to that system."
> — Charity Majors, Co-founder of Honeycomb.io

Los tres pilares son:

1.  **Logs (Eventos):** Registros detallados de eventos discretos. Responden al **"¿Qué pasó?"**.
2.  **Métricas (Agregados):** Mediciones numéricas a lo largo del tiempo (ej. CPU, latencia, tasa de errores). Responden al **"¿Estamos bien?"** y son ideales para dashboards y alertas de alto nivel.
3.  **Trazas (Traces):** Representan el ciclo de vida de una petición a través de múltiples servicios. Son una colección de "spans" (operaciones) con IDs de correlación. Responden al **"¿Por qué es lento?"** o **"¿Dónde falló?"**.

Un ingeniero senior entiende que estos tres pilares no son independientes. Un buen sistema de observabilidad te permite saltar de uno a otro:

-   Ves un pico en la métrica de latencia en un dashboard (Métrica).
-   Haces clic en el pico para ver las trazas de las peticiones más lentas en ese momento (Traza).
-   Inspeccionas una traza específica y ves que un "span" en el servicio de pagos está tardando mucho.
-   Haces clic en ese "span" para ver los logs detallados de ese servicio con el mismo `trace_id` (Log), y descubres un `WARN` sobre un timeout con un proveedor externo.

Estándares como **[OpenTelemetry](https://opentelemetry.io/)** están unificando la forma en que se generan y colectan logs, métricas y trazas, convirtiéndose en una habilidad crucial para los ingenieros modernos.

---

## Conclusión: De Tarea a Disciplina

El logging, cuando se hace correctamente, es la diferencia entre volar a ciegas y tener una cabina llena de instrumentos. Es una inversión que se paga con creces durante la primera caída del sistema a las 3 AM.

Un desarrollador senior no "añade logs" al final. Diseña la **estrategia de logueo** como parte integral de la arquitectura del software. Piensa en la audiencia, la estructura, el contexto, el rendimiento y el ciclo de vida completo del log.

**No es una tarea; es una disciplina.**

### Lecturas y Citaciones Adicionales

1.  **Libro:** *Site Reliability Engineering: How Google Runs Production Systems* (O'Reilly). El capítulo sobre Monitoreo de Sistemas Distribuidos es fundamental.
2.  **Libro:** *Designing Data-Intensive Applications* por Martin Kleppmann. Explica los fundamentos de los sistemas de procesamiento de datos que sustentan las plataformas de logging.
3.  **Estándar:** [RFC 5424 - The Syslog Protocol](https://tools.ietf.org/html/rfc5424). Para entender los orígenes y la semántica de los niveles de severidad.
4.  **Artículo:** [The Twelve-Factor App - Logs](https://12factor.net/logs). Un manifiesto sobre cómo las aplicaciones modernas deben manejar el logging.
5.  **Blog/Influencer:** [Charity Majors' Blog](https://charity.wtf/). Lectura obligada sobre observabilidad, de una de las voces más influyentes en el campo.
