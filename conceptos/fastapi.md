# FastAPI

¡Excelente! Preparémonos para una inmersión profunda en FastAPI. Este no será solo un tutorial de "cómo hacer X", sino una guía que explora el **"porqué"** detrás de las decisiones de diseño de FastAPI, las tecnologías subyacentes y las mejores prácticas que distinguen a un desarrollador senior.

Un desarrollador senior no solo sabe *usar* una herramienta, sino que entiende *cómo funciona*, sus ventajas, sus limitaciones y cómo encaja en un ecosistema más grande.

---

# Guía Profunda de FastAPI: De Cero a Senior

## Tabla de Contenidos

1.  [**La Filosofía de FastAPI: ¿Por Qué Existe?**](#1-la-filosofía-de-fastapi-por-qué-existe)
    *   Los Tres Pilares: OpenAPI, JSON Schema y OAuth2
    *   Los Dos Gigantes Bajo el Capó: Starlette y Pydantic
2.  [**Conceptos Fundamentales (El Dominio Obligatorio)**](#2-conceptos-fundamentales-el-dominio-obligatorio)
    *   Tipado Moderno de Python (`Type Hints`)
    *   Pydantic: La Columna Vertebral de la Validación
    *   Operaciones de Path y Parámetros
    *   Modelos de Respuesta y Serialización
3.  [**Mecanismos Intermedios (El Salto a la Productividad)**](#3-mecanismos-intermedios-el-salto-a-la-productividad)
    *   Inyección de Dependencias: El Superpoder de FastAPI
    *   Seguridad: Autenticación y Autorización
    *   Middleware: Interceptando Peticiones y Respuestas
    *   Estructura de Proyectos Grandes con `APIRouter`
4.  [**Tópicos Avanzados (El Nivel Senior)**](#4-tópicos-avanzados-el-nivel-senior)
    *   El Mundo Asíncrono: `async`/`await` y el Event Loop
    *   Entendiendo ASGI: El Puente entre el Servidor y tu Código
    *   Pydantic Avanzado: Validadores, Campos Computados y Configuración
    *   WebSockets para Comunicación en Tiempo Real
    *   Tareas en Segundo Plano (`Background Tasks`)
    *   Pruebas (Testing): La Garantía de Calidad
5.  [**Puesta en Producción y Optimización (Mentalidad de Operaciones)**](#5-puesta-en-producción-y-optimización-mentalidad-de-operaciones)
    *   Contenedorización con Docker
    *   Servidores de Producción: Gunicorn + Uvicorn
    *   Optimización de Rendimiento
6.  [**Buenas Prácticas y Filosofía Senior**](#6-buenas-prácticas-y-filosofía-senior)

---

## 1. La Filosofía de FastAPI: ¿Por Qué Existe?

FastAPI no nació en un vacío. Su creador, [Sebastián Ramírez (tiangolo)](https://github.com/tiangolo), lo diseñó para resolver problemas comunes en el desarrollo de APIs con Python, inspirándose en herramientas como Flask, Django Rest Framework, y hasta en lenguajes como Go y frameworks como NestJS.

**El objetivo principal es permitir a los desarrolladores crear APIs robustas, rápidas y bien documentadas con el mínimo esfuerzo posible, utilizando características modernas de Python.**

### Los Tres Pilares: OpenAPI, JSON Schema y OAuth2

FastAPI se basa de forma nativa en estándares abiertos, lo que es una decisión de diseño crucial.

*   **OpenAPI**: Anteriormente conocido como Swagger, es una especificación para describir, producir, consumir y visualizar APIs RESTful. FastAPI utiliza esta especificación para generar documentación interactiva automáticamente (`/docs` y `/redoc`). No es una ocurrencia tardía; el código que escribes *es* la fuente de la especificación.
    > **Citación**: [Especificación OpenAPI 3.1.0](https://spec.openapis.org/oas/v3.1.0)

*   **JSON Schema**: Es un vocabulario que permite anotar y validar documentos JSON. Pydantic, el validador de datos de FastAPI, utiliza JSON Schema para definir las "formas" de los datos que tu API espera y devuelve. Estos esquemas son los que se insertan en la especificación OpenAPI.
    > **Citación**: [Especificación JSON Schema, Draft 2020-12](https://json-schema.org/draft/2020-12/json-schema-core.html)

*   **OAuth2**: Es el framework estándar de la industria para la autorización. FastAPI proporciona herramientas de bajo nivel para integrar diferentes flujos de OAuth2 de manera segura.
    > **Citación**: [RFC 6749 - The OAuth 2.0 Authorization Framework](https://tools.ietf.org/html/rfc6749)

### Los Dos Gigantes Bajo el Capó: Starlette y Pydantic

Un desarrollador senior entiende que un framework es una abstracción sobre otras herramientas. FastAPI es, en esencia, una brillante integración de dos bibliotecas:

*   **Starlette**: Es un microframework/toolkit ASGI (Asynchronous Server Gateway Interface) ligero y de alto rendimiento. Starlette se encarga de todo el trabajo pesado de la web: enrutamiento, middleware, WebSockets, etc. FastAPI extiende Starlette, añadiendo la capa de validación, serialización y documentación.
    > **Citación**: [Documentación de Starlette](https://www.starlette.io/)

*   **Pydantic**: Es una biblioteca de validación de datos y gestión de configuración que utiliza los `type hints` de Python. Es el corazón de la "magia" de FastAPI. Se encarga de:
    1.  **Validación de datos entrantes**: Convierte los datos JSON de una petición en un objeto Python tipado. Si los datos no cumplen con el tipo, genera un error 422 claro y detallado.
    2.  **Serialización de datos salientes**: Convierte tus objetos Python de vuelta a JSON, asegurando que la respuesta cumpla con el modelo definido.
    3.  **Generación de esquemas JSON Schema**: Que luego se usan para la documentación de OpenAPI.
    > **Citación**: [Documentación de Pydantic](https://docs.pydantic.dev/)

---

## 2. Conceptos Fundamentales (El Dominio Obligatorio)

### Tipado Moderno de Python (`Type Hints`)

FastAPI no funcionaría sin los `type hints`. Son la base sobre la que Pydantic construye todo. Un senior en Python no ve los `type hints` como opcionales, sino como una herramienta esencial para la claridad, el mantenimiento y la detección de errores.

> **Citación**: [PEP 484 -- Type Hints](https://www.python.org/dev/peps/pep-0484/)

```python
# main.py
from fastapi import FastAPI

app = FastAPI()

# El type hint `str` le dice a FastAPI que `item_id` debe ser una cadena.
# El type hint `dict` en el retorno es usado para la documentación y autocompletado.
@app.get("/items/{item_id}")
async def read_item(item_id: str) -> dict:
    return {"item_id": item_id}
```

### Pydantic: La Columna Vertebral de la Validación

En lugar de diccionarios planos, definimos la "forma" de nuestros datos con clases que heredan de `pydantic.BaseModel`.

```python
from pydantic import BaseModel, EmailStr
from typing import Optional

class User(BaseModel):
    username: str
    email: EmailStr  # Validación de email incorporada
    full_name: Optional[str] = None # Campo opcional
    age: int > 0 # Pydantic v2 permite validación en la definición

@app.post("/users/")
async def create_user(user: User) -> User:
    # `user` ya no es un dict, es una instancia de la clase User.
    # Los datos han sido validados. Si el email no era válido,
    # el cliente ya habría recibido un error 422.
    return user
```

### Operaciones de Path y Parámetros

FastAPI mapea funciones a rutas (endpoints) usando decoradores (`@app.get`, `@app.post`, etc.). La forma en que defines los parámetros de la función determina cómo FastAPI los obtiene de la petición.

*   **Path Parameters**: Definidos en la ruta con `{}`.
*   **Query Parameters**: Parámetros estándar de la URL (`?key=value`).
*   **Request Body**: Datos enviados en el cuerpo de la petición (usualmente JSON).

```python
from fastapi import FastAPI, Path, Query
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: float

app = FastAPI()

@app.put("/items/{item_id}")
async def update_item(
    # Path Parameter con validación adicional
    item_id: int = Path(..., title="The ID of the item to get", ge=1),
    # Query Parameter opcional
    q: Optional[str] = Query(None, max_length=50),
    # Request Body
    item: Item
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    if item:
        results.update({"item": item})
    return results
```
> **Citación**: [Documentación de FastAPI - Path Parameters](https://fastapi.tiangolo.com/tutorial/path-params/)

### Modelos de Respuesta y Serialización

Así como validas la entrada, debes controlar la salida. El parámetro `response_model` en el decorador de la operación garantiza que la respuesta se ajuste a un modelo Pydantic específico, filtrando datos sensibles y asegurando una estructura consistente.

```python
class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr

class UserOut(BaseModel):
    username: str
    email: EmailStr

# El `response_model` es UserOut, por lo que el campo `password`
# nunca será enviado al cliente, incluso si el objeto `user_in_db` lo contiene.
@app.post("/users/", response_model=UserOut)
async def create_user(user: UserIn):
    # ... lógica para guardar el usuario en la BD ...
    # Supongamos que `user_in_db` es el objeto que recuperamos de la BD
    # y contiene el hash de la contraseña.
    user_in_db = {"username": user.username, "email": user.email, "hashed_password": "..."}
    return user_in_db
```
> **Citación**: [Documentación de FastAPI - Response Model](https://fastapi.tiangolo.com/tutorial/response-model/)

---

## 3. Mecanismos Intermedios (El Salto a la Productividad)

### Inyección de Dependencias: El Superpoder de FastAPI

Este es, posiblemente, el concepto más importante para pasar de un nivel intermedio a senior en FastAPI. La inyección de dependencias (DI) es un patrón de diseño que permite desacoplar componentes.

En FastAPI, se implementa con la función `Depends`. Una "dependencia" es simplemente una función (o una clase invocable) que FastAPI ejecutará antes que tu función de operación de path. El valor que retorne la dependencia será "inyectado" como un parámetro en tu función.

**¿Por qué es tan poderoso?**

*   **Reutilización de Lógica**: Evita repetir código (DRY). Lógica de paginación, obtención del usuario actual, conexión a la base de datos, etc.
*   **Separación de Responsabilidades**: Tu función de operación de path se enfoca en la lógica de negocio, no en cómo obtener una sesión de BD o validar un token.
*   **Facilita las Pruebas (Testing)**: Puedes "sobrescribir" (override) las dependencias durante las pruebas para inyectar mocks o versiones de prueba (ej. una base de datos en memoria).

```python
from fastapi import Depends, FastAPI, HTTPException, status

app = FastAPI()

# Dependencia simple
async def common_parameters(q: Optional[str] = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}

# Dependencia que depende de otra
def get_db_session():
    db = SessionLocal() # Simulación de una sesión de BD
    try:
        yield db # `yield` es clave para dependencias con setup/teardown
    finally:
        db.close()

@app.get("/items/")
# `commons` es el dict retornado por `common_parameters`
async def read_items(commons: dict = Depends(common_parameters)):
    return commons

@app.get("/users/")
# `db` es la sesión de BD inyectada
async def read_users(db: Session = Depends(get_db_session)):
    # ... usar la sesión `db` ...
    return [{"username": "Rick"}, {"username": "Morty"}]
```
> **Citación**: [Documentación de FastAPI - Dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/)

### Seguridad: Autenticación y Autorización

FastAPI no reinventa la rueda. Proporciona un conjunto de herramientas en `fastapi.security` para implementar esquemas de seguridad estándar.

El patrón común es crear una dependencia que:
1.  Extrae el token (o credenciales) de la petición.
2.  Valida el token.
3.  Decodifica el token para obtener la información del usuario.
4.  Retorna el modelo del usuario o lanza una `HTTPException` si algo falla.

```python
from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()

# Esta dependencia solo extrae el token de la cabecera "Authorization: Bearer <token>"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Esta es la dependencia que usarás en tus endpoints protegidos
async def get_current_user(token: str = Depends(oauth2_scheme)):
    # Aquí iría la lógica para validar y decodificar el token JWT
    # y obtener el usuario de la base de datos.
    # Por simplicidad, devolvemos un usuario hardcodeado.
    user = {"username": "johndoe", "email": "johndoe@example.com"}
    return user

@app.get("/users/me")
async def read_users_me(current_user: dict = Depends(get_current_user)):
    return current_user
```
> **Citación**: [Documentación de FastAPI - Security](https://fastapi.tiangolo.com/tutorial/security/first-steps/)

### Middleware

El middleware es código que se ejecuta *antes* de que la petición llegue a tu operación de path y *antes* de que la respuesta sea enviada al cliente. Es ideal para lógica transversal como:
*   Logging de peticiones.
*   Añadir cabeceras (ej. `X-Process-Time`).
*   Manejo de errores a nivel global.
*   CORS (Cross-Origin Resource Sharing).

FastAPI, al estar basado en Starlette, soporta el estándar ASGI para middleware.

```python
import time
from fastapi import FastAPI, Request

app = FastAPI()

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
```
> **Citación**: [Documentación de FastAPI - Middleware](https://fastapi.tiangolo.com/tutorial/middleware/)

### Estructura de Proyectos Grandes con `APIRouter`

Para aplicaciones no triviales, poner todo en un solo archivo `main.py` es insostenible. `APIRouter` funciona como una "mini-aplicación" de FastAPI que puedes incluir en la aplicación principal. Esto te permite organizar tu código por dominios o funcionalidades.

```bash
.
├── app
│   ├── __init__.py
│   ├── main.py
│   └── routers
│       ├── __init__.py
│       ├── items.py
│       └── users.py
```

```python
# app/routers/users.py
from fastapi import APIRouter

router = APIRouter(
    prefix="/users",
    tags=["users"], # Agrupa endpoints en la documentación
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]

# app/main.py
from fastapi import FastAPI
from .routers import items, users

app = FastAPI()

app.include_router(users.router)
app.include_router(items.router)
```
> **Citación**: [Documentación de FastAPI - Bigger Applications](https://fastapi.tiangolo.com/tutorial/bigger-applications/)

---

## 4. Tópicos Avanzados (El Nivel Senior)

### El Mundo Asíncrono: `async`/`await` y el Event Loop

FastAPI es un framework asíncrono. Esto significa que puede manejar múltiples peticiones concurrentemente sin necesidad de múltiples procesos o hilos, gracias al event loop de Python (`asyncio`).

**Regla de Oro Senior**:
*   Usa `async def` para tus operaciones de path si realizan operaciones de E/S (I/O) no bloqueantes (ej. llamadas a una base de datos asíncrona, peticiones HTTP a otras APIs).
*   Usa `def` normal para operaciones que son puramente de CPU (cálculos, procesamiento de datos en memoria). FastAPI es lo suficientemente inteligente como para ejecutar funciones `def` en un pool de hilos externo, evitando que bloqueen el event loop.

**¿Qué pasa con el código bloqueante (ej. una librería de BD síncrona)?**
¡Nunca llames a código bloqueante directamente desde una función `async def`! Bloquearás todo el servidor. La solución es `run_in_executor`:

```python
import time
from fastapi import FastAPI

app = FastAPI()

def blocking_io_call():
    # Simula una operación de E/S bloqueante, como escribir en un archivo
    # o usar una librería de BD síncrona.
    time.sleep(5)
    return "done"

@app.get("/block")
async def run_blocking_task():
    # FastAPI/Starlette manejan esto automáticamente para funciones `def` normales.
    # Si necesitaras hacerlo manualmente dentro de una `async def`:
    # from fastapi.concurrency import run_in_executor
    # result = await run_in_executor(None, blocking_io_call)
    result = blocking_io_call() # FastAPI lo hará por ti si la función es `def`
    return {"message": "Blocking task finished"}
```
> **Citación**: [Documentación de FastAPI - Async](https://fastapi.tiangolo.com/async/)

### Entendiendo ASGI: El Puente entre el Servidor y tu Código

Un desarrollador senior sabe que FastAPI no es un servidor. Es una aplicación ASGI. Necesita un servidor ASGI como **Uvicorn** o **Hypercorn** para ejecutarse.

ASGI (Asynchronous Server Gateway Interface) es el sucesor espiritual de WSGI. Es una especificación que define una interfaz estándar entre servidores web y aplicaciones Python asíncronas. Permite funcionalidades avanzadas como WebSockets y HTTP/2.

> **Citación**: [Especificación ASGI](https://asgi.readthedocs.io/en/latest/)

Cuando ejecutas `uvicorn main:app`, le estás diciendo al servidor Uvicorn que cargue el objeto `app` del archivo `main.py` y lo trate como una aplicación ASGI.

### Pydantic Avanzado: Validadores, Campos Computados y Configuración

Pydantic es mucho más que definir campos.
*   **Validadores**: Puedes crear funciones de validación personalizadas para campos específicos o para todo el modelo.
*   **Campos Computados**: Genera campos dinámicamente a partir de otros.
*   **Gestión de Configuración**: Usa `pydantic-settings` para cargar la configuración desde variables de entorno.

```python
from pydantic import BaseModel, field_validator, computed_field

class User(BaseModel):
    first_name: str
    last_name: str
    age: int

    @field_validator("age")
    @classmethod
    def check_age(cls, v: int) -> int:
        if v < 18:
            raise ValueError("User must be 18 or older")
        return v

    @computed_field
    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"
```
> **Citación**: [Documentación de Pydantic - Validators](https://docs.pydantic.dev/latest/concepts/validators/)

### WebSockets para Comunicación en Tiempo Real

Gracias a Starlette, FastAPI tiene soporte de primera clase para WebSockets, permitiendo comunicación bidireccional persistente.

```python
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message text was: {data}")
    except WebSocketDisconnect:
        print("Client disconnected")
```
> **Citación**: [Documentación de FastAPI - WebSockets](https://fastapi.tiangolo.com/advanced/websockets/)

### Tareas en Segundo Plano (`Background Tasks`)

A veces necesitas ejecutar una operación después de enviar la respuesta al cliente (ej. enviar un email de confirmación). Bloquear la respuesta para esto es una mala experiencia de usuario.

```python
from fastapi import BackgroundTasks, FastAPI

app = FastAPI()

def write_notification(email: str, message=""):
    with open("log.txt", mode="w") as email_file:
        content = f"notification for {email}: {message}"
        email_file.write(content)

@app.post("/send-notification/{email}")
async def send_notification(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(write_notification, email, message="some notification")
    return {"message": "Notification sent in the background"}
```
> **Citación**: [Documentación de FastAPI - Background Tasks](https://fastapi.tiangolo.com/tutorial/background-tasks/)

### Pruebas (Testing): La Garantía de Calidad

FastAPI facilita enormemente las pruebas gracias a su sistema de DI y a `TestClient`. `TestClient` es una envoltura sobre `httpx` que te permite hacer peticiones a tu API directamente en Python, sin necesidad de un servidor en ejecución.

La clave para pruebas avanzadas es `app.dependency_overrides`, que te permite reemplazar dependencias durante las pruebas.

```python
from fastapi.testclient import TestClient
from .main import app, get_db_session # Importa tu app y la dependencia

# Simula una base de datos de prueba
def get_test_db_session():
    # ... lógica para una BD en memoria ...
    pass

# Sobrescribe la dependencia original con la de prueba
app.dependency_overrides[get_db_session] = get_test_db_session

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}
```
> **Citación**: [Documentación de FastAPI - Testing](https://fastapi.tiangolo.com/tutorial/testing/)

---

## 5. Puesta en Producción y Optimización (Mentalidad de Operaciones)

### Contenedorización con Docker

Un senior piensa en el despliegue desde el principio. Docker es el estándar de facto.

```Dockerfile
# Dockerfile
FROM python:3.11

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

# El comando para ejecutar la app en producción
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
```

### Servidores de Producción: Gunicorn + Uvicorn

Aunque Uvicorn puede funcionar solo, en producción es común usar un gestor de procesos como **Gunicorn** para manejar los *worker processes*. Gunicorn se encarga de iniciar, detener y monitorear múltiples procesos de Uvicorn, proporcionando robustez y permitiendo aprovechar múltiples núcleos de CPU.

`gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app`

*   `-w 4`: Inicia 4 procesos worker. Una regla general es `(2 * número de cores de CPU) + 1`.
*   `-k uvicorn.workers.UvicornWorker`: Le dice a Gunicorn que use la clase worker de Uvicorn, que sabe cómo manejar aplicaciones ASGI.

> **Citación**: [Documentación de FastAPI - Deployment](https://fastapi.tiangolo.com/deployment/server-workers/)

### Optimización de Rendimiento

*   **JSON más rápido**: Instala `orjson` y FastAPI lo usará automáticamente para una serialización/deserialización de JSON significativamente más rápida.
    `pip install orjson`
*   **Caching**: Usa dependencias para implementar estrategias de caché (ej. con Redis) para endpoints que no cambian frecuentemente.
*   **Profiling**: Usa herramientas como `py-spy` para encontrar cuellos de botella en tu código.

---

## 6. Buenas Prácticas y Filosofía Senior

1.  **El tipado no es opcional**: Usa `type hints` para todo. Mejora la legibilidad, el autocompletado y la robustez.
2.  **Abusa de la Inyección de Dependencias**: Es la herramienta más potente para escribir código limpio, desacoplado y testeable.
3.  **Separa la lógica de negocio de la capa de API**: Tus operaciones de path deben ser delgadas. Deben recibir la petición, llamar a una función o servicio que contiene la lógica de negocio real, y luego devolver la respuesta. Esto hace que tu lógica sea reutilizable y más fácil de probar.
4.  **Piensa en la estructura del proyecto desde el día uno**: Usa `APIRouter` para organizar tu código por funcionalidades.
5.  **Entiende el asincronismo**: No mezcles código bloqueante y no bloqueante sin saber lo que haces. Entiende el event loop.
6.  **Conoce los límites de la herramienta**: FastAPI es excelente para APIs. No es la mejor herramienta para renderizar HTML del lado del servidor (aunque puede hacerlo con Jinja2) o para tareas de larga duración que requieren un sistema de colas como Celery o RQ.
7.  **La documentación automática es genial, pero no es suficiente**: Usa los parámetros `title`, `description`, `tags` y `summary` en tus operaciones y routers para que la documentación sea realmente útil para los consumidores de tu API.

Convertirse en un desarrollador senior con FastAPI (o cualquier tecnología) es un viaje que va más allá de aprender la sintaxis. Se trata de entender los principios de diseño, el ecosistema y cómo construir software mantenible, escalable y robusto.

Ahora, la clave es practicar: construye proyectos, enfréntate a problemas reales y nunca dejes de profundizar en la documentación oficial. ¡Buena suerte
