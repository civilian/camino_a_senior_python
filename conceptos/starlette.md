# Starlette

¡Absolutamente! Ponte cómodo, toma tu bebida preferida y prepárate para un viaje profundo al corazón de la web asíncrona de Python. No solo aprenderemos a usar Starlette; desentrañaremos su filosofía, su historia y su lugar en el panteón de las herramientas de desarrollo web.

---

## La Guía Definitiva de Starlette: De Aprendiz a Arquitecto Asíncrono

### **Prólogo: La Sinfonía Inacabada de la Concurrencia Web**

Imagina una orquesta donde cada músico debe esperar a que el anterior termine su solo antes de tocar su propia nota. Sería una melodía lenta, tediosa y terriblemente ineficiente. Durante años, así funcionó gran parte de la web en Python, regida por el paradigma síncrono de WSGI. Cada petición era un músico solista que acaparaba la atención del director (el proceso del servidor).

Pero entonces, una nueva forma de composición musical emergió, inspirada no en la secuencia, sino en la superposición de armonías: la programación asíncrona. Starlette no es solo un instrumento en esta nueva orquesta; es la partitura misma, el conjunto de reglas y herramientas que permite a los desarrolladores componer sinfonías web complejas, rápidas y concurrentes. Esta guía es tu curso de maestría en esa composición.

---

### 1. Introducción Profunda: El Nacimiento de una Estrella

#### **Contexto Histórico: Un Gigante sobre Hombros de Gigantes**

Starlette fue creado por **Tom Christie**, un nombre que resuena con reverencia en la comunidad de Python. Christie es también el autor de `Django REST Framework`, una de las bibliotecas más exitosas y queridas del ecosistema Django. Su experiencia construyendo APIs a gran escala le dio una perspectiva única sobre las limitaciones del mundo síncrono.

Starlette surgió oficialmente alrededor de 2018. No nació en el vacío. Fue la culminación de un cambio tectónico en Python: la estandarización y maduración de `asyncio` (introducido en Python 3.4 y mejorado con la sintaxis `async`/`await` en Python 3.5). El mundo de Python estaba listo para la asincronía, pero carecía de las herramientas web fundamentales para aprovecharla de manera elegante y estandarizada.

#### **El Problema que Resuelve: La Tiranía del "Espera y Verás"**

El problema fundamental que Starlette aborda es el **bloqueo de E/S (Entrada/Salida)**. En un servidor web tradicional (WSGI), cuando una petición necesita, por ejemplo, consultar una base de datos, leer un archivo o llamar a otra API, el proceso del servidor se detiene y espera. Está "bloqueado". Durante esa espera, que pueden ser milisegundos o segundos, ese proceso no puede hacer nada más. Para manejar múltiples usuarios, la solución era lanzar más procesos o hilos, lo cual es costoso en términos de memoria y gestión.

Este es el famoso **problema C10k**: cómo manejar diez mil conexiones concurrentes en un solo servidor. La programación asíncrona, popularizada por entornos como Node.js, ofrece una solución: cuando una tarea espera por E/S, en lugar de bloquearse, cede el control al "bucle de eventos" (event loop), que inmediatamente pone a trabajar al procesador en otra tarea que sí esté lista.

Starlette fue diseñado para ser el cimiento de este nuevo mundo. Proporciona las herramientas esenciales para construir servicios web sobre el estándar **ASGI (Asynchronous Server Gateway Interface)**, la contraparte asíncrona de WSGI.

#### **Evolución: De Toolkit a Ecosistema**

- **Concepción (2018):** Starlette nace como un *toolkit* ASGI ligero. La palabra "toolkit" es clave. No es un framework monolítico como Django. Es una colección de componentes reutilizables (enrutamiento, middleware, respuestas, etc.) que puedes ensamblar a tu gusto.
- **Adopción y Fundación de FastAPI (2018):** Casi inmediatamente, Sebastián Ramírez utilizó Starlette como la base para crear **FastAPI**. Este fue un hito crucial. FastAPI añadió un sistema de inyección de dependencias, validación de datos con Pydantic y generación automática de documentación OpenAPI, demostrando la increíble potencia de Starlette como base.
- **Madurez y Estabilidad (2019-Actualidad):** Starlette ha seguido evolucionando, pero su núcleo se ha mantenido estable y robusto. Las mejoras se han centrado en el rendimiento, el cumplimiento de los estándares ASGI y la adición de funcionalidades clave como soporte para WebSockets, streaming de respuestas y tareas en segundo plano. Hoy, Starlette no es solo una biblioteca; es el corazón de un vasto ecosistema de herramientas web asíncronas en Python.

---

### 2. Fundamentos Teóricos y Computacionales

#### **Base Teórica: El Protocolo ASGI**

Para entender Starlette, primero debes entender ASGI. Es su ADN. WSGI (PEP 333) definió una interfaz simple: una función `callable` que toma un diccionario `environ` y una función `start_response`. Simple, síncrono, efectivo.

ASGI (Asynchronous Server Gateway Interface) es una bestia diferente, diseñada para la concurrencia. Su especificación define una aplicación asíncrona como un `callable` que acepta tres argumentos: `scope`, `receive`, y `send`.

> "ASGI consists of two components: a protocol server... and an application. The server is responsible for managing sockets and translating incoming and outgoing byte streams into a series of events and receiving event messages back from the application." — **Andrew Godwin et al.**, *ASGI Specification* (2019)

Vamos a visualizarlo como una conversación telefónica:

1.  **`scope` (diccionario):** Es el "identificador de llamada". Contiene toda la información estática sobre la conexión entrante: el tipo de conexión (`http`, `websocket`), la ruta, las cabeceras, la información del cliente, etc. Esta información no cambia durante la vida de la petición.
2.  **`receive` (awaitable):** Es tu "oído". Es una función asíncrona que esperas (`await`) para recibir eventos del cliente. En una petición HTTP, normalmente solo lo llamas una vez para obtener el cuerpo de la petición. En un WebSocket, lo llamarías en un bucle para recibir mensajes.
3.  **`send` (awaitable):** Es tu "boca". Es una función asíncrona que usas para enviar eventos de vuelta al cliente. Envías el inicio de la respuesta (código de estado, cabeceras) y luego el cuerpo, posiblemente en varios trozos.

**Analogía del Chef Asíncrono:**
Imagina un chef en una cocina (el bucle de eventos).
- **Síncrono (WSGI):** El chef recibe un pedido, va al almacén a por ingredientes, corta las verduras, cocina el plato, lo emplata y lo sirve. No empieza el siguiente pedido hasta que el primero está completamente terminado. Si el almacén está lejos (E/S de red), toda la cocina se detiene.
- **Asíncrono (ASGI):** El chef recibe un pedido y pone el agua a hervir (inicia una operación de E/S). Mientras el agua hierve, en lugar de mirar la olla, toma otro pedido y empieza a cortar verduras para ese. Cuando el agua hierve (la operación de E/S se completa), una alarma suena (el bucle de eventos le notifica). El chef pausa momentáneamente el corte, echa la pasta al agua y vuelve a cortar las verduras del segundo pedido. Es un solo chef, pero maneja múltiples platos "concurrentemente" al no esperar durante los tiempos muertos.

Starlette es el conjunto de cuchillos, ollas y sartenes de alta calidad para este chef asíncrono.

#### **Principios Subyacentes**

- **Composabilidad:** Starlette está diseñado como un conjunto de componentes que se pueden unir. Una aplicación Starlette es, en esencia, una composición de rutas, middleware y manejadores de eventos.
- **Minimalismo:** Proporciona solo lo esencial para construir servicios web. No hay ORM, ni sistema de autenticación complejo, ni panel de administración. Esto le da una flexibilidad y un rendimiento inmensos.
- **Estándares Primero:** Se adhiere estrictamente a la especificación ASGI. Cualquier componente de Starlette puede ser usado con cualquier servidor ASGI (Uvicorn, Daphne, Hypercorn) y cualquier otro middleware ASGI.

---

### 3. Evolución Histórica Detallada

| Fecha       | Evento Clave                                                              | Figura(s) Clave(s)        | Contexto Histórico en Computación                                                                                              |
| :---------- | :------------------------------------------------------------------------ | :------------------------ | :----------------------------------------------------------------------------------------------------------------------------- |
| **2003**    | **PEP 333 - WSGI v1.0:** Se estandariza la interfaz síncrona para web en Python. | Phillip J. Eby            | El mundo web estaba dominado por CGI. Apache y `mod_python` eran la norma. Python necesitaba una forma unificada de hablar con los servidores. |
| **2008**    | **Lanzamiento de Node.js:** Populariza masivamente el modelo de E/S asíncrona no bloqueante con un bucle de eventos en el backend. | Ryan Dahl                 | El "problema C10k" se vuelve un tema central. Las aplicaciones en tiempo real (chat, notificaciones) empiezan a despegar.        |
| **2012**    | **PEP 3156 - `asyncio`:** Se introduce el módulo `asyncio` en la librería estándar de Python, aunque con una sintaxis compleja (`yield from`). | Guido van Rossum          | Python busca una respuesta nativa al modelo de Node.js y otros lenguajes como Go. La concurrencia se vuelve una prioridad.      |
| **2015**    | **PEP 492 - `async`/`await`:** Python 3.5 introduce una sintaxis mucho más limpia y legible para la programación asíncrona. | Yury Selivanov            | Este es el momento "eureka" para la asincronía en Python. Hace que el código asíncrono sea casi tan legible como el síncrono. |
| **2016**    | **Django Channels:** Andrew Godwin introduce un proyecto para llevar WebSockets y otros protocolos de larga duración a Django, creando la primera versión de lo que se convertiría en ASGI. | Andrew Godwin             | Django, el gigante síncrono, se da cuenta de que necesita una historia para el tiempo real. WSGI no es suficiente.                 |
| **~2018**   | **Nacimiento de Starlette:** Tom Christie crea un toolkit ASGI puro, ligero y de alto rendimiento, aprendiendo de sus experiencias con DRF. | Tom Christie              | El ecosistema `asyncio` está maduro. Hacen falta herramientas de alto nivel. Uvicorn, un servidor ASGI ultrarrápido, también emerge. |
| **2018-Hoy**| **Explosión del Ecosistema:** Starlette se convierte en la base de FastAPI, y juntos impulsan una adopción masiva de la web asíncrona en Python. | Sebastián Ramírez, T. Christie | La necesidad de APIs de alto rendimiento, microservicios y la facilidad de uso de FastAPI/Starlette crean la tormenta perfecta. |

---

### 4. Implementación Práctica: Del "Hola Mundo" a la Arquitectura Real

#### **Ejemplo Básico: La Anatomía de una App Starlette**

Instalemos lo necesario:
`pip install starlette uvicorn`

```python
# main.py
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
import uvicorn

# Un "endpoint" es simplemente una función asíncrona
# que recibe un objeto `request`.
async def homepage(request):
    """
    Un endpoint simple que devuelve un JSON.
    """
    return JSONResponse({'hello': 'world'})

async def user_info(request):
    """
    Un endpoint que extrae un parámetro de la ruta.
    """
    username = request.path_params['username']
    return JSONResponse({'user': username, 'message': f'Hello, {username}!'})

# Las rutas se definen como una lista de objetos Route.
# Cada Route mapea una ruta URL a un endpoint.
routes = [
    Route("/", endpoint=homepage),
    Route("/users/{username}", endpoint=user_info),
]

# La aplicación Starlette se instancia con sus rutas.
app = Starlette(debug=True, routes=routes)

# Esto es solo para ejecutarlo directamente con `python main.py`
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

Para ejecutarlo, guarda el archivo como `main.py` y corre en tu terminal: `uvicorn main:app --reload`.

Este simple ejemplo ya muestra la filosofía de Starlette: componentes explícitos y desacoplados (rutas, aplicación, endpoints).

#### **Patrones de Uso: "Mal vs. Bien"**

El pecado capital en el mundo asíncrono es **bloquear el bucle de eventos**.

**MAL ❌: El Bloqueador de Mundos**

```python
import time
from starlette.responses import PlainTextResponse

async def slow_operation(request):
    # ¡TERRIBLE! time.sleep() es síncrono y bloqueante.
    # Mientras esto se ejecuta, el servidor no puede responder
    # a NINGUNA otra petición. El chef se quedó mirando la olla.
    time.sleep(5) 
    return PlainTextResponse("I'm finally done.")
```

**BIEN ✅: El Cooperador Concurrente**

```python
import asyncio
from starlette.responses import PlainTextResponse

async def slow_non_blocking_operation(request):
    # ¡CORRECTO! asyncio.sleep() es asíncrono.
    # Cede el control al bucle de eventos, permitiendo
    # que otras tareas se ejecuten durante la "espera".
    # El chef pone un temporizador y se va a hacer otras cosas.
    await asyncio.sleep(5)
    return PlainTextResponse("I'm done, and I didn't stop the world.")
```

> "The golden rule of async programming is to never, ever, ever call a blocking function from within an async function." — **Luciano Ramalho**, *Fluent Python* (2015)

#### **Caso de Estudio: API que Consulta un Servicio Externo**

Imagina una API que necesita obtener datos del clima de un servicio externo. Esta es una operación de E/S de red, el caso de uso perfecto para `async`.

```python
# requirements: pip install starlette uvicorn httpx
import httpx
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
import uvicorn

# Usamos httpx, un cliente HTTP asíncrono.
# Usar `requests` aquí sería un anti-patrón (es bloqueante).
async_client = httpx.AsyncClient()

async def get_weather(request):
    city = request.path_params['city']
    # URL de una API de clima pública (ejemplo)
    url = f"https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&current_weather=true"
    
    try:
        # `await` en la llamada de red. El bucle de eventos
        # puede trabajar en otras cosas mientras esperamos la respuesta.
        response = await async_client.get(url)
        response.raise_for_status() # Lanza excepción si hay error HTTP
        data = response.json()
        
        return JSONResponse({
            'city': city,
            'temperature': data['current_weather']['temperature'],
            'unit': 'celsius'
        })
    except httpx.HTTPStatusError as e:
        return JSONResponse({'error': f'API error: {e.response.status_code}'}, status_code=502)
    except Exception as e:
        return JSONResponse({'error': str(e)}, status_code=500)

routes = [
    Route("/weather/{city}", endpoint=get_weather)
]

app = Starlette(debug=True, routes=routes)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

Este ejemplo demuestra cómo la asincronía permite que nuestro servicio sea altamente concurrente. Podría estar manejando cientos de peticiones de clima simultáneamente, ya que la mayor parte del tiempo se pasa esperando respuestas de la red, no ocupando la CPU.

---

### 5. Nivel Senior - Conceptos Avanzados

Aquí es donde separamos a los programadores de los arquitectos. Un senior no solo usa la herramienta, sino que entiende sus límites, sus costos y cómo integrarla en un sistema complejo.

#### **Middleware: La Cebolla ASGI**

El middleware en ASGI es una hermosa implementación del patrón decorador. Cada middleware es una capa de una cebolla que envuelve a la aplicación. Una petición entra, atraviesa cada capa (que puede modificar la petición o realizar acciones), llega al núcleo (tu endpoint), y la respuesta vuelve a salir atravesando las capas en orden inverso.

```python
# middleware.py
import time
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

class TimingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Código ejecutado ANTES del endpoint
        start_time = time.time()
        
        # Llama a la siguiente capa de la cebolla (o al endpoint)
        response = await call_next(request)
        
        # Código ejecutado DESPUÉS del endpoint
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        print(f"Request to {request.url.path} took {process_time:.4f}s")
        
        return response

# En tu main.py, lo añadirías así:
from starlette.middleware import Middleware
from middleware import TimingMiddleware

middleware = [
    Middleware(TimingMiddleware)
]

app = Starlette(routes=routes, middleware=middleware)
```
**Trade-off:** Cada capa de middleware añade una pequeña latencia. Un exceso de middleware puede impactar el rendimiento. Úsalo para preocupaciones transversales (logging, autenticación, compresión), no para lógica de negocio.

#### **Tareas en Segundo Plano (Background Tasks)**

A veces, necesitas hacer algo después de enviar la respuesta al cliente, como enviar un email de confirmación. Bloquear la respuesta para esto es una mala experiencia de usuario.

```python
from starlette.background import BackgroundTask
from starlette.responses import JSONResponse
import asyncio

async def send_confirmation_email(email: str):
    # Simula el envío de un email
    print(f"Sending confirmation email to {email}...")
    await asyncio.sleep(3) # Operación de E/S (ej. conectar a un servidor SMTP)
    print("Email sent!")

async def register_user(request):
    data = await request.json()
    email = data['email']
    
    # Lógica de registro de usuario aquí...
    user_id = 123 
    
    # Creamos la tarea, pero NO la ejecutamos aún.
    task = BackgroundTask(send_confirmation_email, email=email)
    
    # La pasamos a la respuesta. Starlette la ejecutará
    # DESPUÉS de que la respuesta haya sido enviada.
    return JSONResponse(
        {'user_id': user_id, 'status': 'registered'},
        background=task
    )
```

**Trade-off y Anti-patrón:** Las `BackgroundTasks` son para operaciones cortas y no críticas. No hay reintentos garantizados si el servidor se cae. Para tareas robustas, críticas y de larga duración, **debes usar un sistema de colas dedicado como Celery o RQ**. Usar `BackgroundTask` para procesar un video de 20 minutos es un anti-patrón que puede agotar los recursos del servidor.

#### **Cuándo NO usar Starlette (y el Ecosistema ASGI)**

1.  **Cargas de Trabajo Pesadas en CPU:** Si tu aplicación realiza principalmente cálculos matemáticos intensivos, criptografía o procesamiento de imágenes, el modelo asíncrono no ofrece beneficios significativos. El Global Interpreter Lock (GIL) de Python significa que solo un hilo puede ejecutar bytecode de Python a la vez. Para esto, es mejor un modelo multiproceso (ej. Gunicorn con múltiples workers síncronos) o descargar el trabajo a otros lenguajes (Rust, C++).
    *   **Solución Híbrida:** Puedes ejecutar una operación bloqueante de CPU en un pool de hilos separado usando `run_in_executor` para no bloquear el bucle de eventos principal.
        ```python
        import asyncio
        
        def cpu_bound_task():
            # Simula un cálculo pesado
            sum(i*i for i in range(10**7))

        async def my_endpoint(request):
            loop = asyncio.get_running_loop()
            # Ejecuta la función bloqueante en otro hilo
            await loop.run_in_executor(None, cpu_bound_task)
            return JSONResponse({'status': 'done'})
        ```

2.  **Equipos sin Experiencia en `asyncio`:** La programación asíncrona tiene una curva de aprendizaje. Errores como mezclar código bloqueante y no bloqueante pueden ser sutiles y difíciles de depurar. Un equipo que conoce bien Django o Flask podría ser más productivo con esas herramientas que luchando con los conceptos de `asyncio`.

3.  **Proyectos que Necesitan "Pilas Incluidas":** Si necesitas un ORM, un panel de administración, un sistema de migración de base de datos, y un framework de autenticación completo desde el primer día, un framework monolítico como **Django** es una opción mucho más rápida y robusta. Starlette te da la libertad de elegir cada componente, pero también la responsabilidad de hacerlo.

#### **Tabla Comparativa de Trade-offs**

| Característica        | Starlette                                   | FastAPI                                     | Flask                                     | Django                                      |
| :-------------------- | :------------------------------------------ | :------------------------------------------ | :---------------------------------------- | :------------------------------------------ |
| **Paradigma**         | ASGI (Async-first)                          | ASGI (Async-first, sobre Starlette)         | WSGI (Síncrono, con soporte ASGI)         | WSGI (Síncrono, con soporte ASGI)           |
| **Filosofía**         | Toolkit minimalista, composable             | "Pilas incluidas" para APIs, rápido de codificar | Micro-framework, extensible               | "Pilas incluidas" para webs completas       |
| **Rendimiento (E/S)** | Muy Alto                                    | Muy Alto                                    | Moderado (en modo WSGI)                   | Moderado (en modo WSGI)                     |
| **Curva de Aprendizaje** | Moderada (requiere entender ASGI/asyncio) | Baja (abstrae mucho de asyncio)             | Baja                                      | Moderada (por su tamaño)                    |
| **Ideal para**        | Microservicios, APIs de alto rendimiento, WebSockets, como base para otros frameworks. | APIs de datos, servicios que requieren validación y documentación automática. | Proyectos pequeños, prototipos, aplicaciones web tradicionales. | Aplicaciones grandes, CMS, proyectos con admin panel, ORM complejo. |

---

### 6. Referencias y Citaciones Académicas

Para alcanzar el nivel de maestría, uno debe consultar las fuentes originales y los textos canónicos.

1.  > "An ASGI application is a single asynchronous callable that takes scope, receive, and send arguments."
    > — **Andrew Godwin et al.**, *ASGI Specification* (2019). [https://asgi.readthedocs.io/en/latest/introduction.html](https://asgi.readthedocs.io/en/latest/introduction.html)

2.  > "Starlette is a lightweight ASGI framework/toolkit, which is ideal for building high performance asyncio services."
    > — **Tom Christie**, *Starlette Official Documentation*. [https://www.starlette.io/](https://www.starlette.io/)

3.  > "The purpose of this PEP is to propose a provisional API for asynchronous I/O in Python 3, including a pluggable event loop, and abstractions for transports and protocols."
    > — **Guido van Rossum**, *PEP 3156 -- Asynchronous I/O Support aka "asyncio"* (2012). [https://peps.python.org/pep-3156/](https://peps.python.org/pep-3156/)

4.  > "This PEP proposes making `async` and `await` proper keywords. They will be used to define coroutines."
    > — **Yury Selivanov**, *PEP 492 -- Coroutines with async and await syntax* (2015). [https://peps.python.org/pep-0492/](https://peps.python.org/pep-0492/)

5.  > "The problem is that a traditional web server creates one thread (or process) per connection. This is a fine model for a small number of connections, but it breaks down around a few thousand connections."
    > — **Dan Kegel**, *The C10k problem* (1999, updated). [http://www.kegel.com/c10k.html](http://www.kegel.com/c10k.html)

6.  > "This document specifies a proposed standard interface between web servers and Python web applications or frameworks, to promote web application portability across a variety of web servers."
    > — **Phillip J. Eby**, *PEP 333 -- Python Web Server Gateway Interface v1.0* (2003). [https://peps.python.org/pep-0333/](https://peps.python.org/pep-0333/)

7.  > "FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints. The key features are... Fast: Very high performance, on par with NodeJS and Go (thanks to Starlette and Pydantic)."
    > — **Sebastián Ramírez**, *FastAPI Official Documentation*. [https://fastapi.tiangolo.com/](https://fastapi.tiangolo.com/)

8.  > "Don’t block the event loop. This is the most important performance guideline for any asyncio application."
    > — **Yury Selivanov & Elvis Pranskevichus**, *uvloop: Blazing fast Python networking* (PyCon 2016).

9.  > "Concurrency is about dealing with lots of things at once. Parallelism is about doing lots of things at once."
    > — **Rob Pike**, *Concurrency is not Parallelism* (2012). [https://go.dev/blog/waza-talk](https://go.dev/blog/waza-talk) (Esta distinción es fundamental para entender por qué `asyncio` es concurrente pero no necesariamente paralelo en CPython).

10. > "The Global Interpreter Lock... is a mutex that protects access to Python objects, preventing multiple threads from executing Python bytecodes at the same time."
    > — **Python Software Foundation**, *Python Wiki on the GIL*. [https://wiki.python.org/moin/GlobalInterpreterLock](https://wiki.python.org/moin/GlobalInterpreterLock)

---

### Conclusión: El Arquitecto Asíncrono

Has viajado desde los orígenes síncronos de la web en Python hasta el corazón del bucle de eventos de `asyncio`. Ahora entiendes que Starlette no es solo una herramienta, sino una filosofía. Es la elección consciente de la composición sobre la herencia, de la flexibilidad sobre la rigidez, y del rendimiento concurrente sobre la simplicidad síncrona.

Un desarrollador senior que domina Starlette no solo escribe código `async`. Diseña sistemas que respiran al ritmo de la E/S, que escalan no por fuerza bruta, sino por inteligencia en la gestión de recursos. Entiende los trade-offs, sabe cuándo la simplicidad de Flask es preferible, cuándo la robustez de Django es necesaria, y cuándo la velocidad y el control de Starlette son la única respuesta.

La orquesta asíncrona te espera. Con Starlette como tu partitura, estás listo para dirigir.
