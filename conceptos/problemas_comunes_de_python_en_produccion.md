# Problemas Comunes de Python en Producción

Colección de errores frecuentes que separan un sistema que "funciona en local" de uno que aguanta en producción.

---

## 1. Imports cíclicos

**El problema:** El módulo A importa B y B importa A. Python empieza a ejecutar A, llega al import de B, empieza a ejecutar B, llega al import de A... y en ese punto A aún no está completamente cargado. Resultado: `ImportError` o atributos que aparecen como `None`.

```python
# módulo a.py
from b import funcion_b

def funcion_a():
    return "a"
```

```python
# módulo b.py
from a import funcion_a  # ImportError: cannot import name 'funcion_a'

def funcion_b():
    return funcion_a()
```

**Soluciones:**

```python
# Opción 1: import tardío (dentro de la función)
def funcion_b():
    from a import funcion_a
    return funcion_a()

# Opción 2: extraer la dependencia compartida a un tercer módulo (lo más limpio)
# shared.py → contiene lo que ambos necesitan

# Opción 3: importar el módulo en vez del símbolo
import a

def funcion_b():
    return a.funcion_a()
```

---

## 2. Olvidar instalar dependencias en Docker

**El problema:** La app funciona local pero el contenedor falla con `ModuleNotFoundError`.

**Causas frecuentes:**

```dockerfile
# MAL: requirements.txt desactualizado → librería nueva no está
COPY requirements.txt .
RUN pip install -r requirements.txt

# MAL: imagen base diferente a local (Python 3.11 vs 3.12, slim vs full)
FROM python:3.11-slim
```

**Buenas prácticas:**

```dockerfile
FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["gunicorn", "app:app"]
```

```bash
# Regenerar requirements antes de cada build
pip freeze > requirements.txt

# O con pip-tools (con hashes para reproducibilidad exacta)
pip-compile pyproject.toml
```

**Tip:** Correr los tests *dentro* del contenedor en CI/CD, no fuera. Así el entorno de test es idéntico al de producción.

---

## 3. Demasiados workers de Gunicorn para los cores disponibles

**El problema:** Configurar `--workers 16` en una máquina con 1 vCPU. El OS hace context switching constante entre procesos, la latencia sube y el consumo de RAM se multiplica.

```bash
# MAL en una instancia con 1 vCPU
gunicorn app:app --workers 16

# BIEN: fórmula recomendada = (2 * cores) + 1
# En 1 vCPU → 3 workers
gunicorn app:app --workers 3

# Para apps async (FastAPI):
gunicorn app:app --workers 3 --worker-class uvicorn.workers.UvicornWorker

# Para Django/Flask con mucha espera de I/O:
gunicorn app:app --workers 3 --worker-class gevent --worker-connections 1000
```

Cada worker es un proceso separado con su propia copia de la memoria (50-150 MB típicamente). Más workers no siempre = más throughput.

---

## 4. Usar threading para tareas CPU-bound (el GIL)

**El problema:** El GIL solo permite que un thread ejecute bytecode Python a la vez. Usar threads para cómputo puro no genera paralelismo real.

```python
# Esto NO va más rápido con threads si la tarea es CPU-bound
import threading

threads = [threading.Thread(target=calcular_chunk, args=(chunk,)) for chunk in chunks]
# Resultado: igual o más lento que secuencial
```

```python
# BIEN: multiprocessing para CPU, threading/asyncio para I/O
from multiprocessing import Pool

with Pool(processes=4) as pool:
    resultados = pool.map(calcular_chunk, chunks)
```

---

## 5. No poner timeouts en llamadas de red

**El problema:** Un worker queda bloqueado indefinidamente esperando una API externa o la base de datos. Con suficientes requests lentos, todos los workers quedan ocupados y el servicio deja de responder.

```python
# MAL
response = requests.get("https://api.externa.com/datos")

# BIEN
response = requests.get("https://api.externa.com/datos", timeout=(3, 10))
# (connect_timeout, read_timeout)
```

```python
# En SQLAlchemy
engine = create_engine(
    DATABASE_URL,
    pool_timeout=30,
    connect_args={"connect_timeout": 5}
)
```

---

## 6. Bloquear el event loop en asyncio

**El problema:** Llamar a una función bloqueante dentro de una coroutine congela toda la aplicación. Ninguna otra coroutine puede ejecutarse mientras dura el bloqueo.

```python
async def endpoint():
    time.sleep(5)        # MAL: bloquea el event loop
    await asyncio.sleep(5)  # BIEN: cede el control
```

```python
# Para código bloqueante que no se puede cambiar:
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor()

async def endpoint():
    loop = asyncio.get_event_loop()
    resultado = await loop.run_in_executor(executor, funcion_bloqueante, arg)
    return resultado
```

---

## 7. Argumentos mutables por defecto

**El problema:** Los objetos mutables como valor por defecto se crean una sola vez al definir la función y se comparten entre todas las llamadas.

```python
# MAL
def agregar(item, lista=[]):
    lista.append(item)
    return lista

agregar("a")  # ["a"]
agregar("b")  # ["a", "b"] ← sorpresa: "b" se acumula sobre la llamada anterior
```

```python
# BIEN
def agregar(item, lista=None):
    if lista is None:
        lista = []
    lista.append(item)
    return lista
```

---

## 8. Variables de entorno que no existen en producción

**El problema:** `os.environ["DATABASE_URL"]` funciona local porque tienes un `.env` cargado. En producción la variable no está → `KeyError` al arrancar, o peor, falla silenciosamente más tarde.

```python
# MAL: falla con KeyError
DB_URL = os.environ["DATABASE_URL"]

# MAL: usa None sin avisar
DB_URL = os.environ.get("DATABASE_URL")

# BIEN: falla rápido con mensaje claro
DB_URL = os.environ.get("DATABASE_URL")
if not DB_URL:
    raise EnvironmentError("DATABASE_URL no está configurada")

# MEJOR: pydantic-settings valida todas las variables al arrancar
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    redis_url: str
    secret_key: str

settings = Settings()  # lanza ValidationError si falta alguna
```

---

## 9. Cachés sin límite de tamaño

**El problema:** Un dict usado como caché manual acumula entradas indefinidamente. La memoria del proceso crece hasta que el sistema lo mata.

```python
# MAL
_cache = {}

def get_usuario(user_id):
    if user_id not in _cache:
        _cache[user_id] = db.query(user_id)
    return _cache[user_id]
```

```python
# BIEN: lru_cache con maxsize
from functools import lru_cache

@lru_cache(maxsize=1000)
def get_usuario(user_id):
    return db.query(user_id)

# O cachetools para TTL y más control
from cachetools import TTLCache
cache = TTLCache(maxsize=1000, ttl=300)
```

---

## 10. Problema N+1 con ORMs

**El problema:** Se consulta una lista de objetos y luego se accede a una relación en un bucle. Cada iteración genera una consulta adicional a la base de datos.

```python
# MAL: 1 query para los posts + 1 query por cada post para el autor = N+1
posts = Post.objects.all()
for post in posts:
    print(post.autor.nombre)  # cada acceso dispara un SELECT
```

```python
# BIEN: traer los autores en la misma query
posts = Post.objects.select_related("autor").all()  # Django ORM
# SQLAlchemy:
posts = session.query(Post).options(joinedload(Post.autor)).all()
```

En producción con miles de registros, esto puede convertir una respuesta de 50ms en 5 segundos.

---

## 11. Usar `print()` en vez de `logging`

**El problema:** `print()` va a stdout sin timestamps, sin niveles, sin contexto. En producción no se puede filtrar, agregar ni correlacionar con otras herramientas.

```python
# MAL
print(f"Procesando pedido {order_id}")
print(f"Error al conectar: {e}")
```

```python
# BIEN
import logging

logger = logging.getLogger(__name__)

logger.info("Procesando pedido", extra={"order_id": order_id})
logger.error("Error al conectar", exc_info=True)
```

```python
# En producción, configurar logging estructurado (JSON) para que las herramientas
# como Datadog, CloudWatch o ELK puedan indexarlo
import structlog

logger = structlog.get_logger()
logger.info("pedido procesado", order_id=order_id, user_id=user_id, duration_ms=45)
```

---

## 12. `except Exception: pass` (tragar errores)

**El problema:** Se captura una excepción y no se hace nada con ella. El error desaparece silenciosamente y el sistema continúa en un estado inconsistente.

```python
# MAL: el error se traga, nadie sabe que pasó
try:
    enviar_email(usuario)
except Exception:
    pass

# MAL: se loguea pero se pierde el stack trace
except Exception as e:
    print(f"Error: {e}")

# BIEN
except Exception:
    logger.exception("Error enviando email a %s", usuario.email)
    raise  # o manejar explícitamente
```

---

## 13. No cerrar conexiones / agotamiento del pool

**El problema:** Se abren conexiones a la base de datos, Redis o servicios externos sin cerrarlas. El pool de conexiones se agota y los requests empiezan a fallar o a esperar indefinidamente.

```python
# MAL: la conexión no se cierra si hay una excepción
conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()
cursor.execute("SELECT ...")
# Si algo falla aquí, conn nunca se cierra

# BIEN: context manager garantiza el cierre
with psycopg2.connect(DATABASE_URL) as conn:
    with conn.cursor() as cursor:
        cursor.execute("SELECT ...")
```

```python
# En SQLAlchemy, usar scoped sessions o el patrón de sesión por request
# No hacer `session = Session()` global sin gestionar su ciclo de vida
```

---

## 14. Datetimes sin timezone (naive vs aware)

**El problema:** Mezclar datetimes con y sin timezone genera comparaciones incorrectas, bugs de ordenación y problemas al guardar en bases de datos.

```python
from datetime import datetime, timezone

# MAL: datetime naive (sin timezone), asume la del sistema
ahora = datetime.now()

# BIEN: siempre UTC, siempre aware
ahora = datetime.now(timezone.utc)

# Con pendulum para manejo más ergonómico
import pendulum
ahora = pendulum.now("UTC")
en_madrid = ahora.in_timezone("Europe/Madrid")
```

---

## 15. Usar `float` para dinero

**El problema:** Los floats tienen errores de representación en binario. Pequeñas diferencias se acumulan y los cálculos financieros producen resultados incorrectos.

```python
# MAL
precio = 0.1 + 0.2
print(precio)  # 0.30000000000000004

# BIEN
from decimal import Decimal

precio = Decimal("0.1") + Decimal("0.2")
print(precio)  # 0.3
```

---

## 16. DEBUG=True en producción (Django/Flask)

**El problema:** Con `DEBUG=True`, cualquier excepción muestra el stack trace completo, las variables locales y la configuración de la app en el navegador. Es un riesgo de seguridad grave.

```python
# settings.py - MAL
DEBUG = True  # nunca en producción

# BIEN
import os
DEBUG = os.environ.get("DEBUG", "false").lower() == "true"
# En producción, la variable de entorno no está definida o es "false"
```

---

## 17. Tareas pesadas bloqueando el proceso principal

**El problema:** Enviar un email, generar un PDF o llamar a una API lenta directamente en el handler de un request HTTP. El usuario espera todo ese tiempo y el worker queda ocupado.

```python
# MAL: el usuario espera mientras se procesa todo
@app.post("/pedido")
def crear_pedido(datos):
    pedido = db.crear_pedido(datos)
    enviar_email_confirmacion(pedido)   # puede tardar 2 segundos
    generar_factura_pdf(pedido)         # puede tardar 3 segundos
    return {"id": pedido.id}

# BIEN: responder inmediatamente y procesar en background (Celery, RQ, etc.)
@app.post("/pedido")
def crear_pedido(datos):
    pedido = db.crear_pedido(datos)
    enviar_email_confirmacion.delay(pedido.id)  # Celery task
    generar_factura_pdf.delay(pedido.id)
    return {"id": pedido.id}
```

---

## 18. Dependencias sin versiones fijas

**El problema:** `pip install requests` sin fijar versión. Una actualización de la librería rompe la app en producción aunque funcionara en local.

```
# MAL (requirements.txt)
requests
django
celery

# BIEN: versiones fijas
requests==2.32.3
django==5.0.6
celery==5.4.0

# MEJOR: pip-tools o poetry para gestionar versiones transitivas también
```

---

## 19. No manejar SIGTERM (graceful shutdown)

**El problema:** Kubernetes o el sistema operativo envían SIGTERM para detener el proceso. Si la app no lo maneja, se mata en medio de una request, una transacción o un job de Celery.

```python
import signal
import sys

def manejador_sigterm(signum, frame):
    logger.info("Recibido SIGTERM, cerrando limpiamente...")
    # cerrar conexiones, terminar tasks en curso, flush de logs
    sys.exit(0)

signal.signal(signal.SIGTERM, manejador_sigterm)
```

```bash
# En Gunicorn, configurar un timeout de graceful shutdown
gunicorn app:app --graceful-timeout 30
```

---

## 20. Cargar datasets enteros en RAM con Pandas

**El problema:** `pd.read_csv("archivo_enorme.csv")` carga todo en memoria. En producción con archivos grandes, el proceso consume gigas de RAM y puede ser matado por el OOM killer.

```python
# MAL: carga 10 GB en RAM
df = pd.read_csv("transacciones.csv")

# BIEN: procesar en chunks
for chunk in pd.read_csv("transacciones.csv", chunksize=10_000):
    procesar(chunk)

# O usar Dask para procesar en paralelo sin cargar todo
import dask.dataframe as dd
df = dd.read_csv("transacciones.csv")
resultado = df.groupby("categoria").monto.sum().compute()
```

---

## 21. Usar `random` para tokens de seguridad

**El problema:** `random` no es criptográficamente seguro. Sus valores son predecibles si se conoce el estado del generador. No usar para tokens, contraseñas ni identificadores de sesión.

```python
import random
import string

# MAL: predecible
token = "".join(random.choices(string.ascii_letters, k=32))

# BIEN: criptográficamente seguro
import secrets
token = secrets.token_hex(32)
token_url = secrets.token_urlsafe(32)
```

---

## 22. Olvidar `if __name__ == "__main__"` con multiprocessing

**El problema:** En Windows y macOS (spawn), al crear procesos con `multiprocessing`, el módulo principal se reimporta. Si el código de creación de procesos está en el nivel del módulo (sin el guard), se lanza un bucle infinito de procesos.

```python
# MAL: en Mac/Windows, esto crea procesos recursivamente hasta crashear
from multiprocessing import Pool

pool = Pool(4)
pool.map(calcular, datos)

# BIEN
from multiprocessing import Pool

def calcular(x):
    return x ** 2

if __name__ == "__main__":
    with Pool(4) as pool:
        resultados = pool.map(calcular, range(100))
```

---

## 23. Diferencias de case sensitivity entre local y producción

**El problema:** El filesystem de macOS es case-insensitive por defecto. `from Modulo import X` funciona local aunque el archivo se llame `modulo.py`. En Linux (producción) falla con `ModuleNotFoundError`.

```python
# Funciona en Mac, falla en Linux si el archivo es `utils.py`
from Utils import helper
from utils import helper  # correcto
```

También aplica a archivos de templates, assets estáticos y cualquier path construido manualmente.

---

## 24. Pool de conexiones mal dimensionado

**El problema:** Con 10 workers de Gunicorn y un pool de 5 conexiones por worker, la app intenta abrir hasta 50 conexiones a la base de datos. PostgreSQL por defecto acepta 100. Con varios servicios, el límite se alcanza fácilmente.

```python
# Ver cuántas conexiones activas hay en PostgreSQL
# SELECT count(*) FROM pg_stat_activity;

# BIEN: dimensionar el pool teniendo en cuenta workers * conexiones_por_worker
engine = create_engine(
    DATABASE_URL,
    pool_size=5,        # conexiones mantenidas abiertas
    max_overflow=2,     # conexiones extra permitidas momentáneamente
    pool_timeout=30,
)

# Alternativa: PgBouncer como proxy de conexiones frente a PostgreSQL
```

---

## 25. Race conditions con operaciones no atómicas

**El problema:** Leer un valor, modificarlo y guardarlo son tres pasos separados. Con concurrencia, dos procesos pueden leer el mismo valor, modificarlo por separado y el segundo sobrescribir al primero.

```python
# MAL: read-modify-write no es atómico
saldo = db.get_saldo(user_id)      # proceso A y B leen 100
saldo += 50
db.set_saldo(user_id, saldo)       # A escribe 150, B escribe 150 (en vez de 200)

# BIEN: operación atómica en la base de datos
db.execute("UPDATE cuentas SET saldo = saldo + 50 WHERE user_id = %s", [user_id])

# O con Redis para contadores distribuidos
redis.incr(f"saldo:{user_id}", 50)

# O usando SELECT FOR UPDATE para bloquear la fila
with db.transaction():
    saldo = db.execute("SELECT saldo FROM cuentas WHERE id = %s FOR UPDATE", [user_id])
    db.execute("UPDATE cuentas SET saldo = %s WHERE id = %s", [saldo + 50, user_id])
```
