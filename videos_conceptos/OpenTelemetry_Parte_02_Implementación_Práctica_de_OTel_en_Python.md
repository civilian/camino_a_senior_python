La teoría es fascinante, pero ¿cómo se traduce en código real que puedas ejecutar? Es hora de dejar los diagramas y la historia para ensuciarnos las manos. Vamos a construir una aplicación simple en Python y a darle el superpoder de la observabilidad.

# OpenTelemetry

---

### 4. Implementación Práctica en Python

Basta de teoría. Vamos a ensuciarnos las manos. Crearemos una pequeña aplicación Flask que simula tirar un dado y veremos cómo OpenTelemetry nos cuenta su historia.

#### **Configuración del Entorno**

Primero, instala las bibliotecas necesarias. Usaremos un exportador a la consola para ver los resultados directamente, sin necesidad de un backend complejo.

```bash
pip install Flask
pip install opentelemetry-api
pip install opentelemetry-sdk
pip install opentelemetry-instrumentation-flask
pip install opentelemetry-exporter-otlp-proto-http # Opcional, para un backend real
pip install opentelemetry-exporter-otlp-proto-grpc # Opcional, para un backend real
```

#### **Ejemplo de Código: La Tirada de Dados**

```python
# app.py
import time
import random
from flask import Flask

# 1. --- Configuración de OpenTelemetry ---
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.instrumentation.flask import FlaskInstrumentor

# Configura el "Resource" para identificar nuestro servicio
resource = Resource(attributes={
    "service.name": "dice-roller-service"
})

# Configura el "TracerProvider" con el recurso
trace.set_tracer_provider(TracerProvider(resource=resource))

# Usaremos un "ConsoleSpanExporter" para imprimir las trazas en la terminal
# En un entorno real, usarías OTLPSpanExporter para enviar a un backend
exporter = ConsoleSpanExporter()
processor = BatchSpanProcessor(exporter)
trace.get_tracer_provider().add_span_processor(processor)

# Obtiene un "Tracer" para instrumentación manual
tracer = trace.get_tracer(__name__)

# 2. --- Aplicación Flask ---
app = Flask(__name__)

# ¡La magia! Auto-instrumenta Flask para capturar todas las peticiones entrantes.
FlaskInstrumentor().instrument_app(app)

@app.route("/rolldice")
def roll_dice():
    # 3. --- Instrumentación Manual ---
    # Creamos un "span" padre para toda la operación de tirar el dado.
    # El span de Flask (creado por la auto-instrumentación) será su padre.
    with tracer.start_as_current_span("roll_dice_operation") as parent_span:
        
        # Simulamos un trabajo, como llamar a otro servicio o una DB
        delay = random.uniform(0.05, 0.2)
        time.sleep(delay)
        
        # Creamos un "span" hijo para la lógica de negocio específica.
        with tracer.start_as_current_span("calculate_result") as child_span:
            player = "Player1"
            result = random.randint(1, 6)
            
            # 4. --- Enriqueciendo Spans con Atributos y Eventos ---
            # Los atributos son metadatos clave-valor que describen el span.
            parent_span.set_attribute("operation.duration_ms", int(delay * 1000))
            child_span.set_attribute("player.id", player)
            child_span.set_attribute("roll.value", result)
            
            # Los eventos son como logs estructurados adjuntos a un punto en el tiempo dentro del span.
            child_span.add_event("Dice rolled", {"value": result, "player": player})

            if result > 4:
                child_span.set_status(trace.Status(trace.StatusCode.OK, "High roll!"))
            else:
                child_span.set_status(trace.Status(trace.StatusCode.OK, "Low roll."))

            return f"Hello, {player}! You rolled a {result}"

if __name__ == "__main__":
    app.run(debug=True)
```

**Para ejecutarlo:**

1.  Guarda el código como `app.py`.
2.  Ejecuta `opentelemetry-instrument python app.py`. El wrapper `opentelemetry-instrument` es la forma más fácil de aplicar la auto-instrumentación.
3.  Abre tu navegador o usa `curl` para acceder a `http://127.0.0.1:5000/rolldice`.
4.  Observa tu terminal. Verás la traza exportada en formato JSON.

#### **Análisis del Resultado (Salida en la Consola)**

Verás algo como esto (simplificado):

```json
{
  "name": "calculate_result",
  "context": { "trace_id": "0x...", "span_id": "0x...", ... },
  "parent_id": "0x...", // Apunta al span "roll_dice_operation"
  "attributes": { "player.id": "Player1", "roll.value": 5 },
  "events": [{ "name": "Dice rolled", ... }],
  ...
},
{
  "name": "roll_dice_operation",
  "context": { "trace_id": "0x...", "span_id": "0x...", ... },
  "parent_id": "0x...", // Apunta al span de Flask
  ...
},
{
  "name": "GET /rolldice",
  "context": { "trace_id": "0x...", "span_id": "0x...", ... },
  "parent_id": null, // El span raíz
  "attributes": { "http.method": "GET", "http.status_code": 200 },
  ...
}
```

Esta salida, cuando es visualizada en una herramienta como Jaeger, se convierte en una cascada que cuenta una historia clara:
1.  Llegó una petición `GET /rolldice`.
2.  Dentro de ella, se ejecutó la `roll_dice_operation`.
3.  Dentro de esa operación, se `calculate_result`.
Vemos la duración, los atributos y los eventos de cada paso. ¡Hemos pasado de la ceguera a la omnisciencia!

#### **Comparación: Antes vs. Después**

| Antes (Logs desestructurados)                                    | Después (Trazas de OpenTelemetry)                                    |
|------------------------------------------------------------------|----------------------------------------------------------------------|
| `INFO: Request received for /rolldice`                           | Un `Span` raíz `GET /rolldice` con atributos HTTP.                   |
| `DEBUG: Starting dice roll for Player1`                          | Un `Span` hijo `roll_dice_operation` anidado.                        |
| `DEBUG: Dice result is 5`                                        | Un `Span` nieto `calculate_result` con atributos `player.id` y `roll.value`. |
| **Problema:** Correlacionar estos logs es manual y propenso a errores. | **Solución:** La causalidad es explícita. La latencia de cada paso se mide automáticamente. |