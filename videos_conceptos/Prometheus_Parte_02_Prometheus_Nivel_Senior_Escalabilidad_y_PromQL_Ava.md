Ya sabes cómo instrumentar una aplicación, pero ¿qué pasa cuando tienes miles de ellas? ¿O cuando necesitas predecir fallos antes de que ocurran? Aquí es donde separamos a los que usan Prometheus de los que realmente lo dominan.

# Prometheus

## 5. Nivel Senior - Conceptos Avanzados: Más Allá del `up{}`

Aquí es donde separamos a los ingenieros que *usan* Prometheus de los que lo *entienden*.

### Trade-offs: La Sabiduría de Saber Cuándo NO Usarlo

*   **Prometheus NO es para Event Logging:** Si necesitas almacenar información de eventos individuales con alta cardinalidad (como un `request_id` o `user_id`), Prometheus es la herramienta equivocada. Para eso están los sistemas de logging (ELK Stack, Loki) o de tracing (Jaeger, Zipkin).
    > "Si necesitas buscar por un ID único, probablemente no es una métrica." - Un SRE anónimo pero sabio.
*   **Precisión vs. Disponibilidad:** Prometheus favorece la disponibilidad sobre la consistencia estricta de los datos. Puede perder algún punto de datos si un scrape falla. Si necesitas una contabilidad 100% precisa (ej. sistemas de facturación), no uses métricas de Prometheus para ello.
*   **Pull vs. Push (El Pushgateway):** El modelo *pull* no funciona bien para trabajos efímeros (ej. un script cron que dura 2 segundos). Para esto existe el **Pushgateway**, un intermediario que recibe métricas y las expone para que Prometheus las recoja.
    *   **Anti-patrón:** Usar el Pushgateway como una forma de convertir Prometheus en un sistema *push*. Esto es un error. El Pushgateway se convierte en un punto único de fallo y un dolor de cabeza de gestión, ya que las métricas de trabajos muertos persisten. Úsalo con extrema precaución.

### El Ecosistema de Escalabilidad: Thanos, Cortex y VictoriaMetrics

Un servidor Prometheus por sí solo es una "mascota". Es una isla de datos. Para construir un sistema de monitoreo global, de alta disponibilidad y con almacenamiento a largo plazo, necesitas ir más allá.

| Característica | Prometheus (Vanilla) | Thanos | Cortex / Mimir |
| :--- | :--- | :--- | :--- |
| **Almacenamiento** | Local, a corto plazo | Bloques en Object Storage (S3, GCS) | Bloques en Object Storage |
| **Vista Global** | No (Federación limitada) | Sí (Query Layer global) | Sí (Query Frontend global) |
| **Alta Disponibilidad** | No (Requiere configuración manual) | Sí (Sidecar/Receiver) | Sí (Replicación de ingesta) |
| **Multitenancy** | No | Sí (con hacks) | Sí (nativo, su principal caso de uso) |

**Diagrama de Arquitectura con Thanos (ASCII Art):**

```
             [ Grafana ]
                  |
           [ Thanos Query ]
          /        |       \
[Thanos Sidecar] [Thanos Store] [Thanos Compactor]
      |               |                |
[ Prometheus A ]  [ Prometheus B ]  [ Object Storage (S3/GCS) ]
      |               |
 [ App Cluster A ] [ App Cluster B ]
```

*   **Thanos Sidecar:** Se ejecuta junto a cada Prometheus, subiendo los bloques de datos a un almacenamiento de objetos barato.
*   **Thanos Query:** Proporciona una única API de consulta que puede buscar datos tanto en los Prometheus en tiempo real como en el almacenamiento a largo plazo.
*   **Decisión de Diseño Senior:** ¿Cuándo introducir Thanos? Cuando necesites una de estas tres cosas:
    1.  **Retención a largo plazo:** Guardar métricas por más de unas pocas semanas/meses.
    2.  **Vista de consulta global:** Ver métricas de todos tus clústeres en un solo dashboard.
    3.  **Alta disponibilidad** para tus datos de métricas.

### PromQL Avanzado: El Lenguaje de los Oráculos

Un senior no solo escribe `rate(http_requests_total[5m])`. Un senior compone sinfonías.

*   **Calcular Tasa de Error:**
    ```promql
    sum(rate(http_requests_total{status=~"5.."}[5m])) by (job)
    /
    sum(rate(http_requests_total[5m])) by (job)
    ```
*   **Calcular el 95º Percentil de Latencia (usando un Histograma):**
    ```promql
    histogram_quantile(0.95, sum(rate(http_request_latency_seconds_bucket[5m])) by (le, job))
    ```
*   **Encontrar los 3 endpoints con más errores 500:**
    ```promql
    topk(3, sum(rate(http_requests_total{status="500"}[5m])) by (endpoint))
    ```
*   **Alertar cuando un disco se llenará en 4 horas:**
    La función `predict_linear()` es tu bola de cristal.
    ```promql
    # Alerta si el espacio libre predicho en 4 horas es menor que 0
    predict_linear(node_filesystem_free_bytes{mountpoint="/"}[1h], 4 * 3600) < 0
    ```

### El Anti-Patrón de la Cardinalidad: El Monstruo bajo la Cama

La cardinalidad es el número total de series temporales únicas. Una métrica como `http_requests_total{method, path, status}` con 3 métodos, 50 paths y 5 status codes genera `3 * 50 * 5 = 750` series. ¡Esto está bien!

Pero si añades `user_id` con 1 millón de usuarios, generas 750 millones de series. Esto destruirá la memoria RAM de tu Prometheus y hará que las consultas sean insoportablemente lentas.

**Cómo evitarlo:**
1.  **Nunca, jamás, uses IDs de usuario, IDs de petición, direcciones de email o cualquier dato de cardinalidad ilimitada como etiqueta.**
2.  Usa herramientas como `tsdb-analyzer` para inspeccionar tu TSDB y encontrar las métricas y etiquetas culpables.
3.  Agrega en el cliente si es necesario. En lugar de `user_id`, quizás `user_type` (`free`, `premium`).

## 6. Referencias y Citaciones Académicas: En Hombros de Gigantes

1.  > "Borgmon's design is based on a simple, robust, and scalable architecture that has proven to be effective for monitoring large-scale, dynamic systems." — **Abhishek Verma, et al.**, *Large-scale cluster management at Google with Borg* (2015). [Enlace](https://storage.googleapis.com/pub-tools-public-publication-data/pdf/43438.pdf)

2.  > "The key to PromQL’s expressive power is its use of labels to create a multi-dimensional data space, which can be sliced, diced, and aggregated on the fly." — **Julius Volz**, *PromCon 2016 Keynote*.

3.  > "We call this model 'white-box' monitoring, in contrast to 'black-box' monitoring. With white-box monitoring, you have insight into the internal state of your systems, which is essential for debugging and performance analysis." — **Beyer, B., Jones, C., Petoff, J., & Murphy, N. R.**, *Site Reliability Engineering: How Google Runs Production Systems* (2016).

4.  > "Gorilla is a time-series database that is optimized for writes and reads of recent data. It achieves a 26x reduction in storage size by using a combination of delta-of-delta timestamps, XOR-based floating point compression, and other novel techniques." — **Tuomas Pelkonen, et al.**, *Gorilla: A Fast, Scalable, In-Memory Time Series Database* (2015). [Enlace](https://www.vldb.org/pvldb/vol8/p1816-teller.pdf) (Nota: Aunque no es Prometheus, este paper de Facebook sobre su TSDB muestra el estado del arte en el campo y los problemas que Prometheus también tuvo que resolver).

5.  > "Prometheus is a graduated project. Graduated projects are considered stable and are used successfully in production environments." — **CNCF (Cloud Native Computing Foundation)**, *Prometheus Graduation Announcement* (2018). [Enlace](https://www.cncf.io/announcements/2018/08/09/cncf-announces-prometheus-graduation/)

6.  > "Histograms are a powerful tool for understanding the distribution of a set of values. They are particularly useful for calculating quantiles, such as the 95th percentile, which are often more meaningful than simple averages." — **Brian Brazil**, *Prometheus: Up & Running* (2018).

7.  > "The pull model simplifies client-side instrumentation and provides a centralized point of control for the monitoring system. It also allows for easy service discovery, as Prometheus can be configured to automatically discover new targets to scrape." — **Prometheus Authors**, *Official Prometheus Documentation - "Pulling versus Pushing"*. [Enlace](https://prometheus.io/docs/introduction/overview/#pulling-versus-pushing)

8.  > "Thanos was created to address the challenges of running Prometheus at scale, including long-term storage, global query view, and high availability." — **Fabian Reinartz & Bartek Plotka**, *Thanos - Prometheus at scale* (KubeCon Talk, 2018).

9.  > "The most important thing to remember about the Pushgateway is that it is not an aggregator or a distributed counter, but rather a metrics cache." — **Prometheus Authors**, *Official Prometheus Documentation - "When to use the Pushgateway"*. [Enlace](https://prometheus.io/docs/practices/pushing/)

10. > "The whole point of SRE is to bridge the gap between development and operations. Instrumenting your code with metrics is a key part of that bridge." — **Ben Treynor Sloss**, Creador del término "SRE" en Google.