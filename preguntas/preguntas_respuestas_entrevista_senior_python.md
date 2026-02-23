# Preguntas y Respuestas para Entrevista Senior Python

Este documento agrupa **más de 100 preguntas** típicas de entrevistas para perfil **Senior Python**, alineadas con los temas de [habilidades_python.md](../habilidades_python.md). Incluye preguntas que suelen hacerse en procesos reales y cubre en profundidad los temas de la carpeta `preguntas/`.

**Contenido aproximado:** Paradigmas (SOLID, GRASP, OOP, FP) · Python core (GIL, descriptors, MRO, decoradores, generadores, asyncio, threading, logging, pdb, itertools, collections, type hints) · Arquitectura (MVC, CQRS, Event Sourcing, DDD, microservicios, ETL, Pub/Sub) · Frameworks web (Django, Flask, FastAPI, Falcon, Starlette, WebSockets) · Datos (ACID, CAP, PostgreSQL, MongoDB, Elasticsearch, DynamoDB, Redis, MVCC, sharding) · Análisis (pandas, SQLAlchemy, Airflow, Prefect, Pydantic) · APIs (REST, GraphQL, gRPC, rate limiting, Nginx) · Event driven (Celery, Kafka, RabbitMQ) · Rendimiento (Numba, Greenlet, memory) · Seguridad (OAuth, JWT, Bandit, hashing) · Testing (pytest, mocks, coverage, Locust, TDD, hypothesis, tox) · CI/CD (Jenkins, poetry, PyPI, serverless) · Extras (Prometheus, Sentry, OpenTelemetry, Docker, K8s, Helm, Terraform, NumPy, LangChain, ruff, hatch, Streamlit, etc.).

**Banco ampliado:** Para un listado de **más de 10.000 preguntas** (sin respuestas desarrolladas) generadas a partir de todos los temas de [habilidades_python.md](../habilidades_python.md), ver [banco_10000_preguntas.md](banco_10000_preguntas.md). Se puede regenerar con `python preguntas/generar_banco_preguntas.py`.

---

## Índice por bloques

1. [Paradigmas de programación](#1-paradigmas-de-programación)
2. [Lenguaje Python (core)](#2-lenguaje-python-core)
3. [Arquitectura de software](#3-arquitectura-de-software)
4. [Frameworks web](#4-frameworks-mvc--web)
5. [Acceso a datos y persistencia](#5-acceso-a-datos--persistencia)
6. [Análisis y procesamiento de datos](#6-análisis-y-procesamiento-de-datos)
7. [Servidores, APIs y protocolos](#7-servidores-apis-y-protocolos)
8. [Event driven, rendimiento, seguridad](#8-event-driven-rendimiento-seguridad)
9. [Testing, CI/CD y DevOps](#9-testing-cicd-y-devops)
10. [Extras (observabilidad, ML, tipado, etc.)](#10-extras-relevantes)

---

## 1. Paradigmas de programación

### P1. ¿Qué es el principio de responsabilidad única (SRP) y cómo lo aplicarías en un servicio que lee de Kafka y escribe en PostgreSQL?

**Respuesta:**  
El **SRP** (Single Responsibility Principle) dice que una clase o módulo debe tener una única razón para cambiar. En ese servicio, en lugar de una clase que lea de Kafka, transforme y escriba en PostgreSQL, conviene separar:

- Un componente que **solo** lee mensajes (adaptador Kafka).
- Un componente que **solo** aplica la lógica de negocio/transformación.
- Un componente que **solo** persiste (repositorio o adaptador PostgreSQL).

Así, un cambio en el contrato de Kafka, en la lógica de negocio o en el esquema de la base son cambios en componentes distintos. En Python esto se traduce en módulos/clases pequeñas, inyección de dependencias y posible uso de un bus o orquestador que conecte los tres.

### P2. Explica la diferencia entre herencia y composición. ¿Cuándo elegirías composición en un diseño orientado a objetos?

**Respuesta:**  
- **Herencia:** la subclase “es un” tipo de la superclase (ej. `Dog` es un `Animal`). Acoplamiento fuerte y riesgo de jerarquías profundas y frágiles.
- **Composición:** un objeto “tiene” otros objetos (ej. `Engine` dentro de `Car`). Favorece reutilización por delegación y menor acoplamiento.

Elegiría **composición** cuando: no hay una relación “es un” clara, cuando varias clases comparten comportamiento pero no una jerarquía natural (evitar herencia múltiple), o cuando quiero poder sustituir o probar partes (inyección de dependencias). El principio “favor composition over inheritance” (GoF) aplica sobre todo en dominios donde los requisitos cambian y la herencia rigidiza el diseño.

### P3. ¿Qué es la programación funcional en Python? Nombra construcciones del lenguaje y de la stdlib que la soportan.

**Respuesta:**  
Programación funcional enfatiza funciones puras, inmutabilidad, expresiones en lugar de sentencias y composición de funciones. En Python:

- **Funciones de primera clase** y paso como argumentos.
- **Closures** y **higher-order functions** (`map`, `filter`, `functools.reduce`).
- **`functools`:** `partial`, `lru_cache`, `wraps`.
- **`itertools`:** `chain`, `groupby`, `islice`, generadores infinitos.
- **Comprehensions** (list, dict, set) como expresiones.
- **Generadores** y `yield` para flujos lazy.
- **Inmutabilidad** mediante tuplas, `frozenset`, y evitar mutar en funciones “puras”.

Un senior sabe cuándo un estilo funcional mejora la legibilidad (pipelines, transformaciones de datos) y cuándo un enfoque OOP o imperativo es más claro.

### P3b. Explica los cinco principios SOLID con un ejemplo breve de cada uno.

**Respuesta:**  
- **S (SRP):** Una clase, una razón para cambiar. Ej.: separar “enviar email” de “calcular factura”.  
- **O (Open/Closed):** Abierto a extensión, cerrado a modificación. Ej.: estrategias (inyección de políticas) en lugar de if/else.  
- **L (Liskov):** Las subclases deben poder sustituir a la base sin romper el contrato. Ej.: no hacer que un “Cuadrado” herede de “Rectángulo” si cambia la semántica de setter.  
- **I (Interface Segregation):** Interfaces pequeñas y específicas; el cliente no depende de lo que no usa. Ej.: varios protocolos en lugar de una interfaz gigante.  
- **D (Dependency Inversion):** Depender de abstracciones, no de concretos. Ej.: inyectar un `Repository` abstracto en lugar de instanciar `PostgresRepository` dentro del servicio.

### P3c. ¿Qué es el patrón GRASP “Information Expert” y “Creator”?

**Respuesta:**  
**GRASP** (General Responsibility Assignment Software Patterns) guía a quién asignar responsabilidades.  
- **Information Expert:** asignar la responsabilidad al que tiene la información necesaria (ej. el `Carrito` calcula el total porque tiene los ítems).  
- **Creator:** quién debe crear una instancia de B: quien contiene o agrega instancias de B, quien tiene los datos para inicializar B, o quien usa B muy de cerca. Ej.: `Pedido` crea `LineaPedido` porque las contiene.

### P3d. ¿Qué es programación estructurada y cómo se relaciona con “goto considerado perjudicial”?

**Respuesta:**  
Programación estructurada: flujo de control con secuencia, selección (if/else) y repetición (while/for), sin saltos arbitrarios (goto). El artículo de Dijkstra “Go To Statement Considered Harmful” argumentaba que el goto hacía el código difícil de seguir y de demostrar correcto. En Python no existe goto; el flujo es estructurado por defecto; un senior evita “estructuras” que lo simulen (excepciones para control de flujo, breaks anidados excesivos).

---

## 2. Lenguaje Python (core)

### P4. ¿Qué es el GIL (Global Interpreter Lock) y qué implicaciones tiene para concurrencia y paralelismo?

**Respuesta:**  
El **GIL** es un mutex del intérprete CPython que permite que solo un hilo ejecute bytecode Python a la vez. **Implicaciones:**

- **Concurrencia I/O-bound:** no suele ser problema; los hilos liberan el GIL en operaciones de I/O, así que threading puede mejorar rendimiento en redes o disco.
- **Paralelismo CPU-bound:** varios hilos en un mismo proceso no ejecutan código Python en paralelo; para usar varios núcleos hace falta **multiprocessing** (procesos separados) o integrar código que suelte el GIL (C extensions, NumPy, etc.).
- **AsyncIO** no elimina el GIL pero permite muchas tareas I/O-bound en un solo hilo, evitando el coste de hilos y el contenido del GIL.

En una entrevista senior se espera que propongas: threading para I/O, multiprocessing para CPU, asyncio para alto I/O concurrente, y que conozcas alternativas como PyPy (GIL más flexible) o múltiples procesos + colas.

### P5. Diferencia entre `__new__` y `__init__`. ¿Cuándo implementarías `__new__`?

**Respuesta:**  
- **`__init__`:** inicializa la instancia ya creada; recibe `self` y argumentos; no retorna nada; es lo habitual.
- **`__new__`:** es el constructor “real”; crea y devuelve la instancia (por defecto `object.__new__(cls)`); recibe la clase y argumentos; se ejecuta antes que `__init__`.

Se implementa **`__new__`** cuando: creas un **singleton** (devolver la misma instancia), subclasificas tipos inmutables (`str`, `int`, `tuple`) y debes construir el objeto antes de “inicializarlo”, o cuando quieres devolver una instancia de **otra clase** (factory). Ejemplo típico: patrón singleton con `__new__` que guarda la instancia en un atributo de clase.

### P6. ¿Qué son los descriptors? Pon un ejemplo de uso (por ejemplo, validación o lazy attribute).

**Respuesta:**  
Un **descriptor** es un objeto que define `__get__`, y opcionalmente `__set__` y `__delete__`, y se declara como atributo de clase. Así se controla el acceso a atributos (get/set/delete) de forma reutilizable.

Ejemplos: **`property`** es un descriptor; **validación** (ej. que un atributo sea positivo) se puede hacer con un descriptor que en `__set__` valide y asigne; **lazy attribute** se implementa con un descriptor que en `__get__` calcula el valor la primera vez, lo guarda en el instance dict y lo devuelve después. Los descriptors son la base de `@property`, `@classmethod`, `@staticmethod` y de ORMs (por ejemplo atributos de columnas en SQLAlchemy).

### P7. Explica el orden de resolución de métodos (MRO) en herencia múltiple. ¿Qué es el “diamond problem”?

**Respuesta:**  
Python usa **C3 linearization** para el MRO. Se puede ver con `Clase.mro()` o `Clase.__mro__`. El orden respeta: la jerarquía de cada padre y que una clase aparezca antes que sus ancestros; si hay conflicto, el orden de declaración en la lista de bases manda.

El **diamond problem** aparece cuando `A` es padre de `B` y `C`, y una clase `D` hereda de `B` y `C`; entonces `A` está dos veces en la jerarquía. En Python, `A` solo se visita una vez gracias al MRO (por defecto después de `B` y `C`), así que un `super()` en `D` puede llegar a `A` de forma predecible. Un senior sabe leer el MRO y diseñar mixins y herencia múltiple sin sorpresas.

### P8. ¿Qué son los context managers? ¿Cómo implementas uno con clase y con `contextlib`?

**Respuesta:**  
Un **context manager** garantiza lógica de entrada y salida (setup/teardown) alrededor de un bloque, típicamente con `with ...`. Se implementa con `__enter__` y `__exit__`.

- **Con clase:**  
  `__enter__` devuelve el recurso (o `self`); `__exit__(self, exc_type, exc_val, exc_tb)` recibe la excepción si la hay; si devuelve `True`, la excepción se “traga”; si no, se propaga. Sirve para recursos (archivos, conexiones, locks).

- **Con `contextlib.contextmanager`:**  
  Un generador con un solo `yield`: el código antes del `yield` es el “enter”, el después es el “exit”. Si hay excepción, se relanza después del `yield` y puedes usar `try/finally` para limpiar.

Ejemplo: abrir conexión en `__enter__`, cerrar o hacer rollback en `__exit__`.

### P9. Diferencia entre `iterator` e `iterable`. ¿Cómo harías un iterable perezoso sobre una fuente muy grande?

**Respuesta:**  
- **Iterable:** tiene `__iter__` (y opcionalmente `__getitem__` secuencial); devuelve un iterator. Ej.: list, dict, str.
- **Iterator:** tiene `__iter__` (devuelve `self`) y `__next__`; produce valores uno a uno y lanza `StopIteration` al acabar.

Para una fuente muy grande, el patrón estándar es un **generador** (`yield`): es iterable (devuelve un generator-iterator) y solo calcula el siguiente elemento cuando se pide. Así no cargas todo en memoria. Alternativamente, una clase con `__iter__` y `__next__` que lea por chunks (archivos, APIs paginadas, Kafka) y vaya devolviendo elementos.

### P10. ¿Para qué sirven las type hints y `mypy`? ¿Cómo tiparías un decorador que preserva la firma de la función?

**Respuesta:**  
Las **type hints** (PEP 484) documentan tipos y permiten análisis estático. **mypy** es el checker estándar; reduce bugs de tipo sin ejecutar el código.

Para un **decorador que preserva la firma** se usa `functools.wraps` (preservar nombre y docstring) y **typing** para que el tipo refleje la función original:  
`from typing import TypeVar, Callable; F = TypeVar('F', bound=Callable[..., Any])`  
y el decorador se anota como `def decorator(f: F) -> F: ... return f` (o con `ParamSpec` y `Concatenate` en Python 3.10+ para decoradores que añaden argumentos). Así las herramientas ven que el decorado tiene la misma firma que `f`.

### P11. ¿Qué es la recursión y cuándo puede ser problemática en Python? ¿Qué es la cola de llamadas y el límite de recursión?

**Respuesta:**  
Recursión: una función se llama a sí misma (caso base + caso recursivo). En Python el **límite** por defecto es ~1000 (`sys.getrecursionlimit()`); superarlo lanza `RecursionError`. La **pila de llamadas** guarda el estado de cada invocación; recursión muy profunda consume mucha memoria. Alternativas: iteración con bucle, recursión de cola (Python no la optimiza, pero se puede reescribir a iterativo), o aumentar el límite solo si es seguro (no recomendado como solución general).

### P12. Diferencia entre list comprehension, generator expression y dict/set comprehension. ¿Cuándo usar cada una?

**Respuesta:**  
- **List comprehension** `[x*2 for x in range(10)]`: construye la lista completa en memoria; uso cuando necesitas la lista entera o múltiples accesos.  
- **Generator expression** `(x*2 for x in range(10))`: es lazy; produce un elemento cada vez; ahorra memoria en secuencias grandes o pipelines.  
- **Dict/set comprehension** `{k: v*2 for k,v in d.items()}`, `{x%3 for x in nums}`: mismo concepto para diccionarios y conjuntos.  
Usar generator cuando el flujo es “una pasada” o el tamaño es grande; list cuando necesitas índice, longitud o iterar varias veces.

### P13. ¿Cómo diseñarías una jerarquía de excepciones personalizadas y cuándo usarías excepciones vs códigos de error?

**Respuesta:**  
Heredar de `Exception` (o de una base de dominio, ej. `ValidationError`); excepciones específicas por tipo de fallo (ej. `PaymentDeclinedError`, `InsufficientFundsError`); capturar de más específica a más general. Usar **excepciones** para flujos excepcionales y cuando el llamador puede decidir (try/except); usar **códigos de error** o `Result` cuando los fallos son parte del flujo normal (ej. “no encontrado”) y quieres que sea explícito en la firma (typing). En APIs REST, excepciones se traducen a códigos HTTP y mensajes.

### P14. ¿Qué son las clases abstractas (ABC) y las interfaces en Python? Diferencia con typing.Protocol.

**Respuesta:**  
- **ABC (abc.ABC, @abstractmethod):** clases base que no se pueden instanciar; las subclases deben implementar los métodos abstractos; se usa para definir contratos en OOP.  
- **typing.Protocol** (PEP 544): “structural subtyping”; una clase cumple el protocolo si tiene los métodos indicados, sin herencia explícita; útil para duck typing con type checkers.  
ABC = contrato por herencia; Protocol = contrato por estructura (más flexible, no requiere herencia).

### P15. Nombra al menos cinco magic methods y su propósito. ¿Qué hace `__slots__` y cuándo usarlo?

**Respuesta:**  
Ejemplos: `__init__`, `__str__`/`__repr__`, `__len__`, `__getitem__`, `__iter__`/`__next__`, `__enter__`/`__exit__`, `__call__`, `__eq__`, `__add__`.  
**`__slots__`:** limita los atributos de instancia a los nombres listados; ahorra memoria (no hay `__dict__`) y evita crear atributos por error. Se usa cuando tienes muchas instancias y memoria importa (ej. objetos de dominio en listas grandes). No usar con herencia múltiple que mezcle clases con y sin slots.

### P16. ¿Cómo funciona la serialización en Python (pickle, json, Pydantic)? ¿Cuándo no usar pickle?

**Respuesta:**  
- **pickle:** serializa objetos Python a bytes; solo seguro entre procesos/maquinas bajo tu control; no usar para datos que vienen de usuarios o de la red (riesgo de deserialización arbitraria).  
- **json:** texto estándar; interoperable; solo tipos básicos; para APIs y persistencia portable.  
- **Pydantic:** validación y serialización a dict/json con tipos; ideal para configuración y APIs.  
No usar pickle para comunicación entre servicios ni para datos no confiables.

### P17. Explica el modelo de importación de Python: módulos vs paquetes, `__init__.py`, `import` vs `from ... import`, y qué es `sys.path`.

**Respuesta:**  
- **Módulo:** un archivo `.py`; **paquete:** directorio con (en Python 3.3+) `__init__.py` opcional que puede estar vacío; los paquetes pueden ser “namespace packages” sin `__init__.py`.  
- `import foo` carga el módulo y lo deja en `foo`; `from foo import bar` carga el módulo y pone `bar` en el namespace local.  
- **sys.path:** lista de directorios donde se buscan módulos; incluye el directorio del script, PYTHONPATH y site-packages. Un senior evita modificar sys.path en runtime; usa estructura de proyecto y pip instalable.

### P18. ¿Qué es la metaprogramación en Python? Ejemplos: decoradores que modifican clases, o uso de `type()` para crear clases dinámicamente.

**Respuesta:**  
Metaprogramación: código que genera o modifica código (o estructuras) en tiempo de ejecución. Ejemplos: **decoradores** que añaden métodos o atributos a clases; **`type(name, bases, dict)`** para crear una clase dinámicamente; **metaclasses** (clase cuya instancia es una clase) para validar subclases o registrar recursos; **dataclasses**, **attrs** o **Pydantic** que generan `__init__` y otros métodos. Se usa con mesura; cuando las abstracciones estándar (herencia, composición, decoradores simples) bastan, preferirlas.

### P19. ¿Cómo implementarías un worker pool con threading y otro con multiprocessing? ¿Cuándo usar cada uno?

**Respuesta:**  
- **Threading:** `concurrent.futures.ThreadPoolExecutor`; tareas I/O-bound (HTTP, DB, disco); compartir memoria (cuidado con race conditions y GIL).  
- **Multiprocessing:** `concurrent.futures.ProcessPoolExecutor` o `multiprocessing.Pool`; tareas CPU-bound; cada proceso tiene su propio intérprete y memoria; comunicación por queues o valores compartidos.  
Elegir según cuello de botella: I/O → threads (o asyncio); CPU → processes.

### P20. ¿Qué son las coroutines y el event loop en asyncio? Diferencia entre `async def` y una función normal que devuelve una coroutine.

**Respuesta:**  
**Coroutine:** función definida con `async def`; al llamarla devuelve un objeto coroutine (no ejecuta el cuerpo hasta que se “await”). **Event loop:** ejecuta coroutines, programa callbacks y maneja I/O; `await` cede el control al loop hasta que el resultado está listo. Una función normal que devuelve una coroutine no la ejecuta; hay que hacer `await f()` o `loop.run_until_complete(f())`. Con `async def` y `await` se escribe código concurrente sin callbacks explícitos.

### P21. ¿Para qué sirven `functools.partial`, `functools.lru_cache` y `functools.wraps`?

**Respuesta:**  
- **partial:** fija argumentos de una función y devuelve una nueva llamable; ej. `partial(int, base=2)` para parsear binario.  
- **lru_cache:** cache en memoria por argumentos (LRU); ideal para funciones puras costosas; se puede acotar con `maxsize`.  
- **wraps:** decorador que copia `__name__`, `__doc__`, etc. del decorado al wrapper; esencial en decoradores para no perder metadatos.

### P22. Nombra cinco funciones o generadores de itertools que uses en código real y para qué.

**Respuesta:**  
- **chain:** concatenar iterables sin materializar listas.  
- **groupby:** agrupar por clave (requiere datos ordenados por esa clave).  
- **islice:** “rebanada” sobre un iterable (como slice pero lazy).  
- **cycle / repeat:** iterables infinitos para tests o padding.  
- **combinations / permutations:** combinatoria sin cargar todo en memoria.  
Uso típico: pipelines de datos, parsing, generación de casos de test.

### P23. ¿Qué ofrece el módulo collections (defaultdict, Counter, OrderedDict, namedtuple, deque)? ¿Cuándo usar deque en lugar de list?

**Respuesta:**  
- **defaultdict:** dict que asigna un valor por defecto a claves nuevas.  
- **Counter:** conteo de elementos (histograma).  
- **OrderedDict:** orden de inserción (en 3.7+ dict también mantiene orden).  
- **namedtuple:** tupla con nombres de campos (legible y ligera).  
- **deque:** cola doble; append/pop por ambos extremos en O(1); **usar deque** para FIFO/LIFO o ventanas deslizantes; list tiene O(n) para insert/pop al inicio.

### P24. ¿Cómo depurar con pdb? Comandos básicos: breakpoint, next, step, continue, list, pp.

**Respuesta:**  
Insertar `breakpoint()` (o `import pdb; pdb.set_trace()`). Comandos: **n** (next): siguiente línea en la función actual; **s** (step): entrar en la llamada; **c** (continue): seguir hasta el siguiente breakpoint; **l** (list): ver código alrededor; **pp**: pretty-print de variables. También **b archivo:línea** para breakpoints, **p var** para imprimir. En entornos modernos se usa el debugger del IDE (VS Code, PyCharm) que suele integrar pdb.

### P24b. ¿Cómo escribirías un decorador que acepte argumentos (ej. reintentos o un timeout)?

**Respuesta:**  
Si el decorador debe recibir argumentos, se usan **dos niveles**: una función que recibe los argumentos y devuelve el decorador real, y el decorador que recibe la función. Ejemplo: `def retry(max_attempts):` → `def decorator(f):` → `def wrapper(*args, **kwargs):` … → `return decorator`. Así `@retry(3)` llama a `retry(3)`, que devuelve `decorator`, y el resultado de `decorator(f)` es `wrapper`. Usar `functools.wraps` en el wrapper.

### P24c. ¿Qué es una metaclass y en qué caso la usarías?

**Respuesta:**  
Una **metaclass** es la clase de una clase; su `__new__` o `__init__` se ejecuta cuando se define una clase. Casos: **registro** automático de subclases (plugins); **validación** de que las subclases implementan métodos o atributos; **API** que exige un estilo de definición (ej. ORM que crea tablas a partir de la clase). Usar con moderación; a menudo decoradores o ABC alcanzan. Ejemplo: `type` es la metaclass por defecto; puedes heredar de `type` y sobrescribir `__new__`.

### P25. ¿Cómo estructurarías logging en una aplicación Python (niveles, formateo, handlers, no loguear en producción con DEBUG)?

**Respuesta:**  
Configurar el **root logger** o loggers por módulo; **niveles** DEBUG, INFO, WARNING, ERROR, CRITICAL; en producción normalmente INFO o WARNING. **Handlers:** StreamHandler (consola), FileHandler (archivo), o envío a un servicio (SysLog, HTTP). **Formato:** incluir timestamp, nivel, nombre del logger y mensaje; en producción JSON para ingest en agregadores. No dejar `logging.debug()` con formato costoso en hot path; usar `if logger.isEnabledFor(logging.DEBUG):` o mensajes con % y argumentos (el mensaje solo se forma si el nivel está activo).

### P26. ¿Qué es PEP 8 y qué herramientas usas para aplicarlo automáticamente?

**Respuesta:**  
**PEP 8** es la guía de estilo para código Python (indentación, longitud de línea, espacios, nombres, etc.). Herramientas: **black** (formateador opinado, poco configurable); **isort** (orden de imports); **flake8** (lint estático, incluye estilo y algunos errores); **pylint** (más reglas y advertencias). En CI se suele ejecutar black + isort (o ruff) y flake8; el proyecto puede fijar versiones y configuración en `pyproject.toml` o `setup.cfg`.

---

## 3. Arquitectura de software

### P11. ¿Qué es Event Sourcing y cuándo lo recomendarías frente a un modelo CRUD clásico?

**Respuesta:**  
**Event Sourcing** persiste el estado como secuencia de eventos (hechos) en lugar de solo el estado actual. El estado se reconstruye aplicando los eventos en orden; se pueden tener múltiples “proyecciones” (vistas) y reprocesar el pasado.

Lo recomendaría cuando: hay requisitos de auditoría o compliance, necesidad de “viajar en el tiempo” o replay, dominios donde los hechos son la verdad (finanzas, logística), o cuando CQRS encaja y quieres leer modelos optimizados sin tocar el stream de eventos. No lo recomendaría para dominios muy simples o equipos sin experiencia en consistencia eventual y modelado de eventos.

### P12. Diferencia entre CQRS y “una base de datos con lecturas y escrituras”.

**Respuesta:**  
**CQRS** (Command Query Responsibility Segregation) separa el modelo de escritura del de lectura: **comandos** modifican estado (escritura) y **consultas** solo leen. No implica dos bases de datos; puede ser el mismo almacén con modelos distintos (por ejemplo escritura normalizada y lecturas desnormalizadas o cacheadas).

La diferencia con “una DB con lecturas y escrituras” es la **intención**: en CQRS los modelos de lectura pueden estar optimizados para pantallas o reportes (vistas materializadas, proyecciones desde eventos), y el modelo de escritura para reglas de negocio y consistencia. Permite escalar lectura y escritura por separado y usar almacenes distintos (ej. escritura en SQL, lectura en Elasticsearch).

### P13. ¿Qué es un Message Bus o Event Bus y qué problemas resuelve en un sistema distribuido?

**Respuesta:**  
Un **message/event bus** es un intermediario que desacopla productores y consumidores: los publicadores envían mensajes a un canal o topic y los suscriptores los reciben sin conocerse. Resuelve: **desacoplamiento** (cambiar consumidores sin tocar productores), **escalabilidad** (añadir workers que consumen de la cola), **resiliencia** (mensajes persistidos y reintentos), y **trazabilidad** (auditoría de eventos).

En Python, ejemplos: Celery con Redis/RabbitMQ, Kafka para event streaming, o un bus interno en memoria para un monolito modular. Un senior sabe cuándo un bus añade valor (múltiples consumidores, procesos asíncronos, límites de contexto) y cuándo es overkill (flujo síncrono simple).

### P14. ¿Qué es el patrón MVC y cómo se traduce en Django (MVT)?

**Respuesta:**  
**MVC:** Model (datos y lógica de negocio), View (presentación / qué ve el usuario), Controller (recibe input, actualiza modelo, elige vista). En **Django (MVT):** el “Model” es igual; la **Template** es la vista (HTML); la **View** en Django es en realidad el controlador (función o clase que maneja la petición, usa el modelo y devuelve la template con contexto). El “missing” es el controller explícito; Django lo llama View. La URL routing hace de front controller que delega en la View apropiada.

### P14b. ¿Qué es Pub/Sub y en qué se diferencia de una cola punto a punto?

**Respuesta:**  
**Pub/Sub:** un mensaje lo reciben **todos** los suscriptores del topic; desacoplamiento y broadcasting. **Cola punto a punto:** cada mensaje lo consume **un solo** consumidor (entre los workers de la cola); distribución de carga y garantía de procesamiento único. Kafka con consumer groups es más parecido a cola por partición; RabbitMQ tiene ambos modelos (exchanges fanout = pub/sub, queues = punto a punto).

### P14c. ¿Cómo descompondrías un monolito en microservicios? Qué criterios usarías para definir límites.

**Respuesta:**  
Criterios típicos: **dominio** (bounded context en DDD); **equipo** (Conway: un equipo por servicio); **escalado** (separar lo que escala distinto); **tecnología** (permitir stacks distintos si hace falta). Pasos: identificar contextos y APIs; extraer un servicio (strangler fig: proxy que delega); mantener contratos estables (API versioning, eventos). No partir por capas técnicas (un “servicio de DB”); partir por capacidad de negocio.

### P14d. ¿Qué es DDD (Domain-Driven Design) y qué son el bounded context y el agregado?

**Respuesta:**  
**DDD** es un enfoque para modelar software alrededor del dominio: lenguaje ubicuo, modelo rico (no anémico), colaboración con expertos del dominio. **Bounded context:** límite explícito dentro del cual un modelo (términos, entidades) es consistente; distintos contextos pueden tener entidades con el mismo nombre pero significado distinto. **Agregado:** cluster de entidades que se modifican juntas, con una raíz (aggregate root) que garantiza invariantes; las transacciones no cruzan agregados.

### P14e. ¿Qué es un pipeline ETL y qué consideraciones tendrías para hacerlo robusto (idempotencia, reintentos, monitoreo)?

**Respuesta:**  
**ETL:** Extract (origen), Transform (limpieza, reglas), Load (destino). Robustez: **idempotencia** (re-ejecutar no duplica ni corrompe); **reintentos** con backoff y dead-letter; **orden** y dependencias entre pasos (Airflow DAGs, Prefect); **monitoreo** (latencia, fallos, volumen); **versionado** de esquemas y datos; **tests** sobre datos de ejemplo o sintéticos.

---

## 4. Frameworks MVC / Web

### P15. ¿Cómo diseñarías una API REST escalable y mantenible en FastAPI?

**Respuesta:**  
- **Rutas por recurso**, verbos HTTP estándar (GET, POST, PUT/PATCH, DELETE), códigos HTTP correctos y cuerpos en JSON.
- **FastAPI:** routers por dominio (`APIRouter`), modelos Pydantic para request/response, inyección de dependencias para DB y servicios, y documentación automática (OpenAPI).
- **Capas:** rutas → servicios (lógica) → repositorios (acceso a datos); no poner lógica de negocio en el router.
- **Versionado** (ej. `/v1/...`) y convenciones de nombres consistentes.
- **Autenticación/autorización** con OAuth2, JWT o API keys vía dependencias.
- **Paginación, filtros y orden** en listados para no devolver recursos enormes.

### P16. Diferencia entre Gunicorn y Uvicorn. ¿Cuándo usar cada uno?

**Respuesta:**  
- **Gunicorn:** servidor WSGI; multiproceso (y opcionalmente multihilo); ideal para aplicaciones **síncronas** (Django, Flask clásico). No ejecuta ASGI.
- **Uvicorn:** servidor ASGI; soporta **async** y WebSockets; ideal para FastAPI, Starlette, Django async. Suele usarse con workers (p. ej. Gunicorn con worker class uvicorn para tener varios procesos ASGI).

Resumen: app síncrona (Flask/Django sync) → Gunicorn; app async (FastAPI, Django async) → Uvicorn, o Gunicorn + Uvicorn como worker.

### P17. ¿Qué es el ciclo de vida de una petición en Django (desde la petición HTTP hasta la respuesta)?

**Respuesta:**  
1. **WSGI/ASGI** recibe la petición.  
2. **Middleware** (request): se ejecutan en orden (auth, sesión, etc.).  
3. **URL resolver** mapea la ruta a una View.  
4. **View** (función o clase): puede usar formularios, modelos, servicios; devuelve un `HttpResponse` (o subclase).  
5. **Middleware** (response): se ejecutan en orden inverso.  
6. **WSGI/ASGI** envía la respuesta al cliente.

Además: **signals** (pre_save, post_save, etc.) si se usan; **transacciones** si la view está decorada con `@transaction.atomic`; **templates** renderizadas dentro de la view.

### P17b. ¿Cómo implementarías autenticación y autorización en Django (usuarios, permisos, grupos)?

**Respuesta:**  
Modelo **User** (o extendido con OneToOne); **authenticate()** y **login()** en la view; **@login_required** o **LoginRequiredMixin**; **User.has_perm()**, **@permission_required** o **PermissionRequiredMixin**; **grupos** para conjuntos de permisos; para APIs: tokens (DRF TokenAuthentication), JWT (djangorestframework-simplejwt) o sesiones. Autorización a nivel de objeto: **django-guardian** o lógica en la view que compruebe el objeto.

### P17c. Diferencia entre Django ORM y SQLAlchemy. ¿Cuándo elegirías cada uno?

**Respuesta:**  
- **Django ORM:** integrado en Django; API de alto nivel (querysets, migraciones, admin); ideal para aplicaciones web Django y modelos estándar.  
- **SQLAlchemy:** independiente del framework; más flexible (Core vs ORM); consultas raw, conexiones, múltiples backends; ideal para servicios que no usan Django, ETL, o cuando necesitas control fino y rendimiento.  
Elegir Django ORM con Django; SQLAlchemy para FastAPI, scripts, o proyectos que no son web Django.

### P17d. ¿Qué es el patrón “application factory” en Flask y para qué sirve?

**Respuesta:**  
En lugar de crear la app globalmente (`app = Flask(__name__)`), una **función** (ej. `create_app()`) crea la instancia de Flask, carga config, registra blueprints, inicializa extensiones (DB, login) y devuelve la app. Ventajas: **tests** con distintas configuraciones; **múltiples instancias**; **configuración tardía**. Es la forma recomendada de estructurar aplicaciones Flask medianas/grandes.

### P17e. ¿Cómo manejarías dependencias asíncronas en FastAPI (sesión de DB, cliente HTTP) para no bloquear el event loop?

**Respuesta:**  
Usar **clientes y drivers async**: por ejemplo `asyncpg` o `databases` para PostgreSQL, `httpx.AsyncClient` para HTTP. Crear la sesión/cliente en un **lifespan** o **dependency** y cerrarla al terminar; inyectar con `Depends()`. No llamar a código **síncrono bloqueante** (requests, psycopg2) dentro de rutas async sin ejecutarlo en un thread pool (`run_in_executor`) para no bloquear el loop.

### P17f. ¿Qué ventajas tiene Falcon frente a Flask o FastAPI para APIs de alto rendimiento?

**Respuesta:**  
Falcon está pensado para **APIs REST puras**: mínimo overhead, sin capas de templates ni sesiones por defecto; diseño “resource + responder” muy explícito; buen rendimiento en benchmarks. Ventajas: ligero, predecible, fácil de optimizar. Se elige cuando la API es el producto (no una web con formularios) y el equipo prioriza rendimiento y simplicidad sobre ecosistema (plugins, admin, ORM integrado).

### P17g. ¿Qué son los middlewares en Starlette/FastAPI y en qué orden se ejecutan?

**Respuesta:**  
Los **middlewares** envuelven la aplicación: reciben request y llaman al siguiente en la cadena (o a la app); pueden modificar request/response o cortocircuitar. En Starlette/FastAPI se añaden con `app.add_middleware(MiddlewareClass, ...)`. El **orden** importa: el primero añadido es el más externo (se ejecuta primero en request y último en response); típicamente CORS, luego auth, luego logging.

### P17h. ¿Cómo implementarías un WebSocket en FastAPI o en Django Channels?

**Respuesta:**  
- **FastAPI:** endpoint que recibe `WebSocket`; `await websocket.accept()`; luego `await websocket.receive_text()` / `send_text()` en un bucle; manejar desconexión y excepciones.  
- **Django Channels:** ASGI app con protocolo `websocket`; consumers que reciben `receive` y envían `send`; canal layer (Redis) para comunicar entre instancias. En ambos: considerar timeouts, heartbeat y límites de mensajes.

---

## 5. Acceso a datos y persistencia

### P18. Explica ACID y por qué es importante en transacciones.

**Respuesta:**  
- **Atomicity:** la transacción se ejecuta por completo o no se ejecuta (rollback).  
- **Consistency:** la transacción lleva la base de un estado válido a otro (restricciones, triggers).  
- **Isolation:** las transacciones concurrentes no se “ven” a medias; se evitan lecturas sucias y actualizaciones perdidas.  
- **Durability:** una vez confirmada (commit), los cambios sobreviven a fallos (persistidos en disco).

Es importante para operaciones que no pueden quedar a medias (p. ej. transferencias, reservas) y para mantener integridad ante concurrencia y fallos.

### P19. ¿Qué es el teorema CAP? ¿Cómo afecta a la elección de una base de datos distribuida?

**Respuesta:**  
**CAP:** en un sistema distribuido ante partición de red solo se pueden garantizar dos de tres: **C**onsistency (todos ven los mismos datos), **A**vailability (toda petición recibe respuesta), **P**artition tolerance (el sistema sigue aunque haya partición).

En la práctica, P es asumida (redes fallan), así que se elige entre **CP** (consistencia fuerte, posible indisponibilidad) o **AP** (disponibilidad con consistencia eventual). Bases CP: muchos sistemas SQL distribuidos; AP: muchas NoSQL (Cassandra, DynamoDB en ciertos modos). La elección depende de si el dominio tolera datos eventualmente consistentes o no.

### P20. ¿Cómo implementarías reintentos y política de backoff al conectar con PostgreSQL desde Python?

**Respuesta:**  
- Usar un cliente que soporte reintentos o implementar un wrapper que capture excepciones de conexión (ej. `psycopg2.OperationalError`).  
- **Backoff exponencial:** esperar 1s, 2s, 4s, … (con jitter opcional) entre reintentos para no saturar el servidor.  
- Librerías: `tenacity` (decoradores para reintentos y backoff), o `backoff`.  
- Límite de reintentos y timeout global para no bloquear indefinidamente.  
- Opcional: circuit breaker si la base está caída mucho tiempo (evitar llamadas inútiles).

### P21. Diferencia entre Redis como cache y como message broker (por ejemplo con Celery).

**Respuesta:**  
- **Como cache:** almacén clave-valor en memoria; TTL; reduce carga en DB; patrones cache-aside, write-through, etc. Uso típico: sesiones, resultados de consultas costosas.  
- **Como message broker:** cola de tareas; Celery usa Redis (o RabbitMQ) para enviar mensajes a workers; los workers consumen tareas en background. Redis es más simple y rápido pero menos robusto que RabbitMQ para colas (sin garantías de entrega tan estrictas; posibilidad de pérdida en fallos). Para colas críticas suele preferirse RabbitMQ o Kafka.

### P21b. ¿Qué es MVCC y cómo ayuda en PostgreSQL con concurrencia?

**Respuesta:**  
**MVCC** (Multiversion Concurrency Control): cada transacción ve una “instantánea” coherente de los datos; las escrituras crean nuevas versiones de filas en lugar de sobrescribir; las lecturas no bloquean escrituras y viceversa. Reduce locks y permite alta concurrencia; el coste es espacio (versiones antiguas) y vacuum para reclamar. En PostgreSQL es la base del modelo de transacciones y niveles de aislamiento.

### P21c. ¿Qué es un índice compuesto y cuándo lo usarías? ¿Qué es un índice parcial?

**Respuesta:**  
**Índice compuesto:** varias columnas en un solo índice; el orden de columnas importa (la primera define la partición lógica). Útil cuando las consultas filtran/ordenan por esas columnas (ej. `(user_id, created_at)`). **Índice parcial:** índice solo sobre filas que cumplen una condición (WHERE); ahorra espacio y mejora rendimiento cuando la condición reduce mucho el conjunto (ej. índice solo donde `deleted_at IS NULL`).

### P21d. ¿Qué es sharding y qué desafíos introduce (consultas cross-shard, rebalanceo, transacciones)?

**Respuesta:**  
**Sharding:** particionar datos en varios nodos por una clave (ej. user_id); cada nodo tiene un subconjunto. Desafíos: **consultas cross-shard** (agregaciones globales requieren federar); **rebalanceo** al añadir nodos (mover datos sin downtime); **transacciones** que abarcan varios shards (2PC o saga). Se usa cuando un solo nodo no aguanta volumen o escrituras; el diseño del esquema y la clave de sharding son críticos.

### P21e. Diferencia entre vista y vista materializada. ¿Cuándo usar una materializada?

**Respuesta:**  
**Vista:** consulta guardada; cada acceso ejecuta la query (o el optimizador la integra). **Vista materializada:** resultado persistido como tabla; se actualiza con REFRESH (completo o incremental). Usar materializada cuando la query es costosa y los datos pueden ser “casi en tiempo real” (refresco periódico); típico en reportes y dashboards. En PostgreSQL: `CREATE MATERIALIZED VIEW ... AS SELECT ...`.

### P21f. ¿Cómo modelarías datos en MongoDB para una aplicación de alta lectura (embebidos vs referencias)?

**Respuesta:**  
- **Documentos embebidos:** cuando la relación es 1-a-pocos y siempre se accede junta (ej. direcciones en un usuario); evita joins y round-trips.  
- **Referencias:** cuando hay muchos o se accede por separado; el cliente hace la segunda query o se usa lookup/aggregation.  
Para alta lectura: favorecer desnormalización y embebidos donde tenga sentido; evitar documentos gigantes (límite 16MB); índices en campos por los que se filtra o ordena.

### P21g. ¿Qué es eventual consistency y cómo afecta al diseño de una aplicación?

**Respuesta:**  
**Eventual consistency:** en un sistema distribuido, tras dejar de haber escrituras, todas las réplicas acaban mostrando el mismo valor; pero en un instante dado pueden verse valores distintos. Afecta al diseño: **leer después de escribir** puede no mostrar el último valor (leer tu propio write requiere garantías del almacén o patrones como “read-your-writes”); **UI** debe manejar retrasos (mensajes “actualizando…”, reintentos); **operaciones** que dependen de “valor más reciente” pueden requerir consistencia fuerte en un quorum o líder.

### P21h. ¿Cuándo usarías Elasticsearch en lugar de (o junto a) una base SQL?

**Respuesta:**  
**Elasticsearch** para: búsqueda full-text (relevancia, stemming, fuzzy); agregaciones analíticas sobre logs o eventos; escalado horizontal de búsquedas. Se usa **junto a** SQL cuando la fuente de verdad es la base relacional y Elasticsearch es una vista indexada para búsqueda y analytics; se mantiene sincronizado con cambios (CDC, colas, o jobs). No sustituir SQL para transacciones ACID y consultas relacionales complejas.

### P21i. ¿Qué es el modelo de datos de DynamoDB (partition key, sort key, GSI, LSI) y cómo diseñarías una tabla para consultas por usuario y por fecha?

**Respuesta:**  
**Partition key** (PK): identifica la partición; **sort key** (SK): orden dentro de la partición; acceso eficiente por PK o PK+SK. **GSI:** índice con PK/SK distintos (otra vista de los mismos datos). **LSI:** mismo PK, SK alternativo. Para “por usuario” y “por fecha”: PK = user_id, SK = timestamp permite “todos los ítems de un usuario” ordenados; para consultas globales por fecha haría falta un GSI con PK = fecha (ej. día) y SK = user_id o ítem_id.

---

## 6. Análisis y procesamiento de datos

### P22. ¿Cuándo usarías pandas y cuándo Dask o Spark para procesar datos?

**Respuesta:**  
- **pandas:** datos que caben en memoria en una máquina; exploración, transformaciones, análisis ad-hoc; API rica y expresiva.  
- **Dask:** mismo estilo que pandas pero paralelizado en un clúster o múltiples núcleos; datos que no caben en RAM de una sola máquina pero sí en un clúster; API similar a pandas.  
- **Spark (PySpark):** datos muy grandes, varios nodos; ecosistema Hadoop; necesidad de ML distribuido (MLlib), streaming o integración con Kafka; más overhead que Dask para conjuntos medianos.

Regla práctica: si cabe en RAM y es un solo nodo → pandas; si no cabe o quieres paralelismo → Dask o Spark según tamaño y ecosistema.

### P23. ¿Qué es idempotencia en un pipeline de datos (por ejemplo en Airflow)? ¿Por qué importa?

**Respuesta:**  
**Idempotencia:** ejecutar la misma tarea varias veces produce el mismo resultado que ejecutarla una vez. En pipelines: si un job falla a mitad y se re-ejecuta, no debe duplicar datos ni dejar estados inconsistentes.

Importa para: **reintentos** seguros, **reprocesamiento** de ventanas de tiempo, y **consistencia** sin efectos secundarios dobles. Se logra con: claves únicas y “upsert”, ventanas de tiempo bien definidas (partition by date), y operaciones que sean deterministas (misma entrada → misma salida).

### P23b. ¿Cómo evitarías fugas de memoria al procesar DataFrames muy grandes con pandas?

**Respuesta:**  
Leer por chunks (`chunksize` en `read_csv`), procesar y escribir cada chunk; no cargar todo en memoria. Usar tipos eficientes (`category`, tipos numéricos más pequeños). Liberar con `del df; gc.collect()` si ya no se usa. Para conjuntos que no caben en RAM, valorar **Dask** o **PySpark** en lugar de pandas puro.

### P23c. ¿Qué es SQLAlchemy y cuál es la diferencia entre el Core y el ORM?

**Respuesta:**  
**SQLAlchemy** es un toolkit para SQL en Python. **Core:** capa de bajo nivel (engine, connection, texto SQL, tablas/metadatos); para consultas raw y control total. **ORM:** capa sobre Core; mapeo clase-tabla, sesiones, queries por objetos. Se puede mezclar: ORM para CRUD estándar y Core para consultas complejas o bulk. Migraciones con Alembic.

### P23d. ¿Cómo orquestarías un DAG en Airflow y qué buenas prácticas aplicarías (idempotencia, retries, XCom)?

**Respuesta:**  
Definir **DAG** con schedule, default_args (retries, backoff); **tasks** como operadores (PythonOperator, PostgresOperator, etc.); dependencias con `>>` y `<<`. Buenas prácticas: tareas **idempotentes**; **retries** con exponential backoff; evitar pasar datos grandes por **XCom** (usar almacén externo o pasar referencias); usar **Variables/Connections** para config sensible; agrupar tareas relacionadas y no hacer DAGs gigantes.

### P23e. ¿Para qué sirve Pydantic en un proyecto Python (validación, configuración, serialización)?

**Respuesta:**  
**Pydantic** valida datos en tiempo de construcción del modelo (tipos, validators personalizados); serializa a dict/JSON; útil para **configuración** (env, archivos) con validación temprana; **APIs** (request/response en FastAPI); **datos de negocio** inmutables y tipados. Evita datos mal formados en el resto del código y documenta el contrato.

### P23f. ¿Cuándo usarías Prefect en lugar de Airflow?

**Respuesta:**  
**Prefect** es más “Python-native”: flujos definidos en código Python (no DAGs en archivos estáticos); mejor experiencia para desarrolladores; orquestación más ligera. Elegir **Prefect** para equipos que prefieren código y despliegue simple; **Airflow** para ecosistema maduro, UI rica y muchos operadores predefinidos o cuando ya está estandarizado en la empresa.

---

## 7. Servidores, APIs y protocolos

### P24. Diferencia entre REST y GraphQL. ¿Cuándo elegirías GraphQL?

**Respuesta:**  
- **REST:** recursos identificados por URLs; el cliente usa verbos HTTP y varias rutas para obtener lo que necesita; a veces over-fetching o under-fetching.  
- **GraphQL:** un endpoint; el cliente envía una query declarando exactamente qué campos quiere; el servidor devuelve solo eso; evita over-fetching y permite agrupar datos de varias “entidades” en una sola petición.

Elegiría **GraphQL** cuando: muchos clientes (móvil, web, partners) con necesidades de datos distintas; necesidad de reducir round-trips y control fino del payload; APIs públicas o muy flexibles. Elegiría **REST** cuando el modelo es simple, hay caché HTTP estándar y el equipo estándar es REST.

### P25. ¿Qué es idempotencia en HTTP? ¿Qué métodos deben ser idempotentes?

**Respuesta:**  
Un método es **idempotente** si ejecutarlo una o varias veces tiene el mismo efecto (sobre el estado del servidor). **GET, PUT, DELETE** deben ser idempotentes; **POST** no (crear recurso varias veces suele crear varios recursos). Esto permite reintentos seguros y caché; los proxies y clientes pueden asumir que repetir GET/PUT/DELETE no cambia el resultado de forma impredecible.

### P26. ¿Cómo diseñarías autenticación para una API (API keys, JWT, OAuth2)?

**Respuesta:**  
- **API keys:** simple; un token por cliente; adecuado para server-to-server o integraciones controladas; se validan en cada request (header o query).  
- **JWT:** stateless; el token lleva claims (user_id, roles, exp); el servidor valida firma y exp; adecuado para SPA y móviles; cuidado con almacenamiento (httpOnly cookie o almacenamiento seguro) y con no poner datos sensibles.  
- **OAuth2:** delegación de autorización; flujos (authorization code, client credentials, etc.); adecuado cuando el usuario autoriza a terceros (login with Google, acceso a recursos de otro servicio).  
En muchos sistemas: OAuth2 para “login” y emisión de tokens, JWT como access token, y API keys para máquina a máquina.

### P26b. ¿Qué es gRPC y cuándo lo elegirías frente a REST?

**Respuesta:**  
**gRPC** usa HTTP/2 y **Protocol Buffers**: contratos fuertemente tipados, serialización binaria eficiente, soporte para streaming (cliente, servidor, bidireccional). Elegir gRPC para: comunicación **servicio a servicio** en microservicios, bajo latencia y alto throughput, streaming o APIs muy estructuradas. REST sigue siendo mejor para APIs públicas (navegador, integraciones heterogéneas) y cuando la herramienting (caché HTTP, proxies) es importante.

### P26c. ¿Cómo implementarías rate limiting en una API (por IP, por usuario, por clave)?

**Respuesta:**  
Algoritmos típicos: **ventana fija** (N requests por ventana; riesgo de picos al borde); **sliding window** o **token bucket** (más justo). Implementación: middleware que comprueba un contador en **Redis** (clave por IP o user_id), incrementa y compara con límite; si se excede, devolver 429. Por clave API: mismo esquema con el API key como parte de la clave. Librerías: slowapi (FastAPI), flask-limiter.

### P26d. ¿Qué son los códigos de estado HTTP que usarías en una API REST (2xx, 4xx, 5xx) y ejemplos concretos?

**Respuesta:**  
- **2xx:** 200 OK (éxito genérico), 201 Created (recurso creado, Location header), 204 No Content (éxito sin cuerpo).  
- **4xx:** 400 Bad Request (validación), 401 Unauthorized (no autenticado), 403 Forbidden (sin permiso), 404 Not Found, 409 Conflict (ej. duplicado), 422 Unprocessable Entity (semántica inválida), 429 Too Many Requests.  
- **5xx:** 500 Internal Server Error (fallo inesperado), 502 Bad Gateway (upstream caído), 503 Service Unavailable (sobrecarga o mantenimiento).

### P26e. ¿Cómo colocarías Nginx delante de una aplicación Python (reverse proxy, SSL, balanceo)?

**Respuesta:**  
**Reverse proxy:** `proxy_pass` al upstream (Gunicorn/Uvicorn en un puerto); `proxy_set_header Host`, `X-Real-IP`, `X-Forwarded-For/Proto` para que la app vea el cliente real. **SSL:** terminar TLS en Nginx (certificado en `ssl_certificate`); proxy al backend por HTTP interno. **Balanceo:** bloque `upstream` con varios `server`; algoritmo (round_robin, least_conn); health checks si el backend lo soporta. Nginx puede además servir estáticos y comprimir respuestas.

### P26f. Diferencia entre HTTP/1.1 y HTTP/2 (multiplexing, headers compression, server push).

**Respuesta:**  
**HTTP/1.1:** una request-response por conexión (o pipelining poco usado); varias conexiones para paralelismo. **HTTP/2:** multiplexing (muchos streams en una sola conexión TCP); compresión de cabeceras (HPACK); frames binarios; server push (servidor envía recursos antes de que el cliente los pida). Beneficios: menos latencia y mejor uso de la conexión; para APIs muchas veces el impacto es menor que en web con muchos recursos.

---

## 8. Event driven, rendimiento, seguridad

### P27. ¿Cómo garantizas que un mensaje en Kafka no se pierda entre productor y consumidor?

**Respuesta:**  
- **Productor:** `acks=all` (o `-1`) para que el líder y réplicas confirmen; reintentos; `idempotence=true` para evitar duplicados por reintentos.  
- **Broker:** réplicas (replication factor > 1) y `min.insync.replicas` adecuado.  
- **Consumidor:** commit del offset **después** de procesar y persistir; procesamiento idempotente por si hay replay; consumer groups para escalar y no perder particiones.

Un senior puede explicar el flujo de confirmación, replicación y commit de offsets.

### P28. ¿Qué es el GIL y cómo afecta al uso de threads vs multiprocessing en Python?

**Respuesta:**  
(Variante de P4.) El GIL hace que solo un hilo ejecute bytecode Python a la vez. Threads sirven para I/O-bound; para CPU-bound hace falta multiprocessing o código que libere el GIL (C extensions). AsyncIO permite muchas tareas I/O en un solo hilo sin el coste de muchos threads.

### P29. ¿Qué vulnerabilidades típicas debes tener en cuenta en una API web (Python)?

**Respuesta:**  
- **Inyección:** SQL (usar ORM/consultas parametrizadas), comandos, templates (no renderizar input crudo).  
- **XSS:** escapar salida en HTML; Content-Security-Policy; en APIs que devuelven JSON, evitar que el cliente inyecte HTML sin sanitizar.  
- **CSRF:** tokens en formularios; SameSite cookies; en APIs stateless con JWT, cuidado con cookies y origen de peticiones.  
- **Autenticación:** contraseñas hasheadas (bcrypt, argon2); no enviar secrets en URLs; JWT con exp y almacenamiento seguro.  
- **Rate limiting** y validación de entrada (Pydantic, validación estricta).  
- **Dependencias:** escaneo (safety, pip-audit) y actualización.

### P30. ¿Qué es Bandit y cómo lo integrarías en CI?

**Respuesta:**  
**Bandit** es un linter de seguridad para Python: detecta patrones inseguros (ej. uso de `eval`, deserialización insegura, contraseñas hardcodeadas). Se ejecuta con `bandit -r src/` y se integra en CI fallando el pipeline si hay hallazgos de severidad alta (o según política). Se puede configurar con `.bandit` o en el comando (excluir falsos positivos, niveles).

### P30b. ¿Cómo configurarías Celery para tareas críticas (broker, resultados, reintentos, colas prioritarias)?

**Respuesta:**  
**Broker:** RabbitMQ preferible para garantías; Redis aceptable si se asume cierto riesgo. **Resultados:** backend (Redis/DB) si necesitas resultado; si no, desactivar. **Reintentos:** `autoretry_for`, `retry_backoff`, `max_retries`; tareas idempotentes. **Colas:** varias colas (default, high_priority); workers dedicados por cola; envío con `queue='high'`. **Monitoreo:** Flower o métricas (latencia, fallos).

### P30c. ¿Qué es RabbitMQ y cómo se compara con Kafka para colas de mensajes?

**Respuesta:**  
**RabbitMQ:** broker de mensajes tradicional; colas, exchanges, bindings; push a consumidores; mensajes se borran al ack. **Kafka:** log distribuido; mensajes persistidos por partición; pull por el consumidor; retención por tiempo/tamaño; replay. RabbitMQ para colas de tareas (Celery), trabajo distribuido, routing flexible. Kafka para event streaming, alto throughput, múltiples consumidores con replay, y retención larga.

### P30d. ¿Qué es Numba y cuándo lo usarías para acelerar código Python?

**Respuesta:**  
**Numba** compila funciones Python (con tipos numéricos y bucles) a código máquina vía JIT; se usa con el decorador `@njit`. Efectivo en bucles numéricos puros y operaciones sobre arrays (compatible con NumPy). No sirve para código con objetos Python arbitrarios o que llama a librerías no soportadas. Se usa cuando el cuello de botella es numérico y no se quiere reescribir en C/Cython.

### P30e. ¿Qué son Greenlet y Eventlet y cómo se relacionan con la concurrencia?

**Respuesta:**  
**Greenlet:** corutinas a nivel de biblioteca (no del lenguaje); se cede el control explícitamente. **Eventlet:** librería que usa greenlets y hace “patch” de la stdlib (sockets, etc.) para que las operaciones de I/O no bloqueen el greenlet; estilo “threads” pero con greenlets. Permite código que “parece” síncrono y escala en I/O. Menos estándar que asyncio; asyncio es la opción recomendada en código nuevo para I/O concurrente.

### P30f. ¿Cómo investigarías una fuga de memoria en una aplicación Python (herramientas, pasos)?

**Respuesta:**  
**memory_profiler** (línea a línea) o **tracemalloc** (stdlib) para ver qué crece; **objgraph** para ver referencias a objetos que no se liberan; **gc.get_objects()** para inspeccionar. Pasos: reproducir la fuga (carga o tiempo); tomar referencias de memoria antes/después; identificar tipos que crecen; buscar referencias globales, caches sin límite, callbacks que retienen objetos. Revisar ciclos que el GC no pueda romper si hay referencias cruzadas con C extensions.

### P30g. ¿Qué es OAuth 2.0 y qué flujos usarías para una SPA, para una app móvil y para servicio a servicio?

**Respuesta:**  
**OAuth 2.0** delega autorización entre cliente, usuario y servidor de recursos. **SPA:** Authorization Code + PKCE (sin client secret; el código se canjea por tokens). **App móvil:** mismo flujo con PKCE; refresh token en almacenamiento seguro. **Servicio a servicio:** Client Credentials (el cliente es la aplicación; no hay usuario). No usar Implicit o Resource Owner Password en clientes públicos.

### P30h. ¿Cómo almacenarías y validarías JWT (access token, refresh token, rotación)?

**Respuesta:**  
**Access token:** corta duración (minutos); el cliente lo envía en cada request (header o cookie httpOnly); el servidor valida firma y exp. **Refresh token:** larga duración; se usa solo para obtener un nuevo access token; almacenar de forma segura (httpOnly, no en localStorage si hay riesgo XSS). **Rotación:** al usar el refresh token, emitir uno nuevo e invalidar el anterior (refresh token rotation) para limitar daño si se filtra.

### P30i. ¿Qué librerías y prácticas usarías para hashear contraseñas y para secretos en código?

**Respuesta:**  
**Contraseñas:** hashear con **bcrypt** o **argon2** (no MD5/SHA sin salt); salt por contraseña; nunca guardar en claro. **Secretos en código:** no hardcodear; usar variables de entorno, archivos fuera del repo, o **Secrets Manager** (AWS Secrets Manager, Vault); en desarrollo, `.env` con valores de ejemplo y el real en local (no commitear). **Dependency scanning:** `pip-audit` o `safety` para CVEs en dependencias.

---

## 9. Testing, CI/CD y DevOps

### P31. Diferencia entre unittest y pytest. ¿Cuándo usarías fixtures y parametrización?

**Respuesta:**  
- **unittest:** estilo xUnit, heredar de `TestCase`, `assertEqual`, `setUp`/`tearDown`; parte de la stdlib.  
- **pytest:** assertions con expresiones (no solo `assertEqual`), descubrimiento de tests por nombre, **fixtures** para setup/teardown reutilizable e inyección, **parametrize** para un test con muchos casos, plugins (coverage, mutpy, etc.).

Usaría **fixtures** para DB de prueba, clientes HTTP, mocks compartidos; **parametrización** para probar la misma lógica con muchos inputs/salidas (ej. validadores, formateadores).

### P32. ¿Qué es un mock y cuándo mockearías una dependencia externa en un test?

**Respuesta:**  
Un **mock** (o stub/fake) sustituye un objeto real por uno controlado que devuelve respuestas predefinidas y permite verificar llamadas. Se mockea una dependencia externa (API, DB, cola) para: **aislar** la unidad bajo test, **evitar** efectos secundarios (no llamar a APIs reales), **controlar** errores y casos límite, y **acelerar** tests. No conviene abusar: si mockeas todo, no estás probando integración; para flujos críticos conviene algún test de integración con dependencias reales o contenedores.

### P33. ¿Cómo estructurarías un pipeline CI/CD para una aplicación Python (tests, lint, build, deploy)?

**Respuesta:**  
- **CI:** en cada push/PR: instalar deps (`pip install -r requirements.txt`), lint (flake8/black/isort), type check (mypy), tests (pytest con coverage), seguridad (bandit, safety). Si algo falla, el pipeline no pasa.  
- **Build:** empaquetar (wheel/sdist con build o poetry) y publicar a artefactos o PyPI interno; opcional imagen Docker.  
- **CD:** despliegue a staging con aprobación manual o automática; luego producción con aprobación o canary; usar variables de entorno y secrets para config; rollback definido (versión anterior o revert commit).

Herramientas típicas: GitHub Actions, GitLab CI, Jenkins; contenedores con Docker; entornos con venv/poetry en CI.

### P33b. ¿Qué es code coverage y qué umbrales razonables fijarías? ¿Qué no mide el coverage?

**Respuesta:**  
**Coverage** mide qué líneas (o ramas) se ejecutan en los tests. Umbral típico: 80–90% para código crítico; 100% no siempre es rentable. **No mide:** corrección (puedes tener tests que pasen y código mal); casos no cubiertos (combinaciones de entrada); calidad de aserciones. Combinar con revisión de código y tests de integración; coverage como indicador, no como meta absoluta.

### P33c. ¿Cómo harías load testing de una API Python (herramientas, métricas, objetivos)?

**Respuesta:**  
**Herramientas:** Locust (Python, scripts en código), k6, JMeter. Definir **escenarios** (mix de endpoints, usuarios concurrentes, rampa). **Métricas:** RPS, latencia (p50, p95, p99), tasa de error; objetivo ej. “p95 < 200 ms bajo X RPS”. Ejecutar contra staging; identificar cuellos de botella (DB, red, CPU). No solo “aguanta 1000 usuarios”; definir carga realista y SLOs.

### P33d. ¿Qué es TDD y qué ventajas y limitaciones ves?

**Respuesta:**  
**TDD:** escribir el test que falla primero, luego el código mínimo para que pase, luego refactorizar. Ventajas: diseño orientado a uso, tests desde el inicio, refactor seguro. Limitaciones: no sustituye diseño de alto nivel; puede generar tests acoplados a implementación; en dominios muy inciertos a veces explorar antes. Un senior lo usa cuando encaja en el flujo del equipo y el problema; no dogmático.

### P33e. Diferencia entre venv, virtualenv, pipenv y poetry para entornos y dependencias.

**Respuesta:**  
- **venv:** stdlib (3.3+); crea entorno aislado; `pip` para deps.  
- **virtualenv:** similar, más opciones; histórico.  
- **pipenv:** une entorno + Pipfile (deps y dev); lock file; un comando para instalar y activar.  
- **poetry:** gestión de proyecto y deps con `pyproject.toml`; lock file; publicación a PyPI; muy usado en proyectos nuevos.  
Elegir: venv + pip para simplicidad; poetry para proyectos con muchas deps y publicación.

### P33f. ¿Cómo empaquetarías una librería Python para publicarla en PyPI (wheel, sdist, twine)?

**Respuesta:**  
Configurar `pyproject.toml` (build-system, metadata, dependencias). **Construir:** `python -m build` genera **sdist** (código fuente) y **wheel** (distribución binaria por plataforma). **Publicar:** `twine upload dist/*` a PyPI (o a un índice privado). Buenas prácticas: versionado semántico, no subir secretos, usar 2FA en PyPI; opcionalmente GitHub Actions para publicar en tag.

### P33g. ¿Qué es Jenkins y cómo lo usarías para un pipeline Python (build, test, deploy)?

**Respuesta:**  
**Jenkins** es un servidor de CI/CD; jobs definidos por pipelines (scripted o declarative). Para Python: etapa de **build** (checkout, `pip install -r requirements.txt` o poetry); etapa de **test** (pytest, coverage, lint, mypy); etapa de **deploy** (ej. construir imagen Docker, push a registry, desplegar a K8s o a un servidor). Credenciales en Jenkins; artefactos y reportes (coverage, JUnit) para historial. Alternativas modernas: GitHub Actions, GitLab CI.

### P33h. ¿Cómo desplegarías una app Python en AWS Lambda (serverless) y qué limitaciones tendrías?

**Respuesta:**  
Empaquetar código y deps en un zip (o imagen); configurar handler (ej. `module.function`); tiempo máximo y memoria; triggers (API Gateway, eventos, cron). **Limitaciones:** tiempo de ejecución (15 min max); cold start (primera invocación); tamaño del paquete; no estado persistente en el proceso. Adecuado para APIs de bajo tráfico, eventos, cron; no para conexiones largas (WebSockets con limitaciones) o procesos muy largos.

---

## 10. Extras relevantes

### P34. ¿Qué es el patrón Circuit Breaker y cuándo lo usarías?

**Respuesta:**  
El **Circuit Breaker** evita llamar repetidamente a un servicio que está fallando: después de N fallos pasa a estado “open” y no llama (o devuelve fallback); tras un tiempo prueba de nuevo (“half-open”); si funciona, vuelve a “closed”. Se usa para: llamadas a APIs externas, microservicios, DB; así se evita saturar un servicio caído y se da una respuesta degradada o en caché. Librerías: `pybreaker`, o implementación con estado y contadores.

### P35. ¿Cómo definirías observabilidad en un servicio Python (logs, métricas, trazas)?

**Respuesta:**  
- **Logs:** estructurados (JSON) con nivel, timestamp, contexto (request_id, user_id); no loguear datos sensibles; usar `logging` o structlog; enviar a un agregador (ELK, Loki, CloudWatch).  
- **Métricas:** contadores, histogramas (latencia, throughput); exportar en formato Prometheus o StatsD; dashboards en Grafana.  
- **Trazas:** correlación de requests entre servicios (OpenTelemetry, Jaeger); un trace_id por request y span por operación.  
Objetivo: poder diagnosticar errores y rendimiento en producción (dónde, cuándo y por qué).

### P36. ¿Qué ventajas tiene usar type hints y mypy en un proyecto grande?

**Respuesta:**  
Documentación viva, detección de errores antes de ejecutar, mejor autocompletado y refactors más seguros. En proyectos grandes: contratos claros entre módulos, menos bugs de tipos, onboarding más rápido. mypy se integra en CI; se puede ir adoptando de forma gradual (archivos sin tipos con `# type: ignore` o módulos excluidos al principio).

### P37. ¿Qué es dependency injection y cómo la aplicarías en un proyecto FastAPI o Flask?

**Respuesta:**  
**Dependency injection (DI):** las dependencias (DB, clientes externos, config) se pasan desde fuera (constructor, parámetros o contenedor) en lugar de crearlas dentro del código. Ventajas: testeabilidad (inyectar mocks), flexibilidad (cambiar implementaciones) y menor acoplamiento.

En **FastAPI:** `Depends()` define dependencias (p. ej. sesión de DB, usuario actual); el framework las resuelve y las inyecta en la ruta. En **Flask:** se puede usar un contenedor (e.g. `flask-injector`) o pasar dependencias por `g` o argumentos desde un factory que configure la app.

### P37b. ¿Cómo expondrías métricas de una app Python para Prometheus?

**Respuesta:**  
Usar **client_prometheus** (o `prometheus_client`): definir contadores, gauges, histogramas; registrar latencias y contadores de requests; exponer endpoint `/metrics` (formato texto). En Flask/FastAPI un middleware puede medir duración por ruta y contar por código de estado. Prometheus hace scrape del endpoint; Grafana para dashboards. Buenas prácticas: etiquetas estables y no cardinalidad explosiva.

### P37c. ¿Qué es Sentry y cómo lo integrarías para capturar excepciones en producción?

**Respuesta:**  
**Sentry** es un servicio de monitoreo de errores: captura excepciones, stack traces, contexto (usuario, tags, breadcrumbs). Integración: instalar `sentry-sdk`, inicializar con DSN en el arranque de la app; en frameworks (Flask, Django, FastAPI) hay integraciones que capturan automáticamente. Configurar sampling si el volumen es alto; no enviar datos sensibles (PII); usar releases y entornos para filtrar.

### P37d. ¿Qué es OpenTelemetry y cómo lo usarías para trazas distribuidas?

**Respuesta:**  
**OpenTelemetry** es un estándar para métricas, trazas y logs. Para **trazas:** instrumentar el código (manual o auto-instrumentación para HTTP, DB); cada operación es un span; los spans se enlazan con trace_id y span_id para seguir una request entre servicios. Exportar a Jaeger, Zipkin o backend en la nube. En Python: `opentelemetry-api`, `opentelemetry-sdk` e instrumentadores para requests, SQLAlchemy, etc.

### P37e. ¿Cómo construirías una imagen Docker para una aplicación Python (multi-stage, tamaño, no root)?

**Respuesta:**  
**Multi-stage:** etapa de build (instalar deps, compilar si hay C extensions); etapa final solo con el artefacto y runtime; reduce tamaño. **Base:** imagen slim (python:3.12-slim); no usar root en el contenedor (USER no privilegiado). **Deps:** copiar requirements primero, `pip install`, luego código (mejor uso de caché de capas). No incluir tests ni herramientas de desarrollo en la imagen final. .dockerignore para no copiar venv ni __pycache__.

### P37f. ¿Qué es Kubernetes y qué recursos usarías para desplegar una API Python (Deployment, Service, Ingress)?

**Respuesta:**  
**Kubernetes** orquesta contenedores: **Deployment** define la app (imagen, réplicas, health checks, recursos); **Service** expone los pods (ClusterIP, LoadBalancer); **Ingress** para HTTP(S) y routing externo. ConfigMap/Secret para configuración. HPA para escalar por CPU o métricas. Un senior conoce los objetos básicos y cómo depurar (logs, describe, exec).

### P37g. ¿Qué es Helm y para qué lo usarías?

**Respuesta:**  
**Helm** es un gestor de paquetes para K8s: empaqueta manifiestos en **charts** con plantillas (Go templating) y valores configurables; permite instalar/actualizar/desinstalar una “release”. Se usa para desplegar aplicaciones complejas (varios recursos) con valores por entorno (staging, prod); charts públicos (nginx, postgres) o propios. `helm install`, `helm upgrade`, `helm values`.

### P37h. ¿Qué es Terraform y cómo lo usarías para infraestructura que aloja una app Python?

**Respuesta:**  
**Terraform** es IaC (infraestructura como código): define recursos (VPC, instancias, DB, buckets) en HCL; plan y apply para crear/actualizar. Para una app Python: definir instancias o ECS/EKS, balanceador, base de datos, DNS; state remoto (S3, etc.); módulos para reutilizar. Separar entornos (workspaces o directorios); no guardar secretos en tf; usar data sources y variables para configurar.

### P37i. ¿Cuándo usarías NumPy en lugar de listas de Python para cálculos numéricos?

**Respuesta:**  
**NumPy** ofrece arrays homogéneos en memoria contigua y operaciones vectorizadas (implementadas en C); órdenes de magnitud más rápido que bucles en Python para operaciones sobre arrays. Usar NumPy para: álgebra lineal, estadística, procesamiento de señales, cualquier cálculo repetitivo sobre grandes conjuntos numéricos. Listas para secuencias heterogéneas y cuando el tamaño es pequeño y la legibilidad prima.

### P37j. ¿Qué es hypothesis (property-based testing) y un ejemplo de uso en Python?

**Respuesta:**  
**Hypothesis** genera datos de prueba automáticamente según estrategias (integers, strings, listas, objetos); el test se ejecuta muchas veces con distintos inputs. **Property-based:** en lugar de “para este input la salida es X”, afirmas una propiedad (“para cualquier lista, ordenar no pierde elementos”). Ejemplo: `@given(st.lists(st.integers()))` y comprobar que el resultado está ordenado y tiene los mismos elementos. Muy útil para invariantes y encontrar corner cases.

### P37k. ¿Qué es tox y para qué lo usarías?

**Respuesta:**  
**tox** automatiza la ejecución de tests en **múltiples entornos**: distintas versiones de Python (3.9, 3.10, 3.11), distintas dependencias o variables de entorno. Define entornos en `tox.ini`; `tox` crea entornos virtuales, instala deps y ejecuta los comandos (pytest, lint). Sirve para asegurar compatibilidad con varias versiones de Python y configuraciones antes de hacer release.

### P37l. ¿Cómo programarías tareas recurrentes en Python (APScheduler vs Celery Beat)?

**Respuesta:**  
- **APScheduler:** en proceso o en background; flexible (cron, interval); adecuado para tareas ligeras en la misma máquina (limpieza, reportes pequeños).  
- **Celery Beat:** scheduler para Celery; las tareas se encolan y las ejecutan workers; adecuado cuando las tareas son pesadas, necesitan cola y workers distribuidos. Elegir APScheduler para apps simples; Celery Beat cuando ya usas Celery y quieres jobs programados distribuidos.

### P37m. ¿Qué es Jinja2 y cuándo lo usarías frente a generar HTML/strings en código?

**Respuesta:**  
**Jinja2** es un motor de plantillas: variables `{{ var }}`, bloques `{% for %}`, herencia de plantillas, filtros y tests. Se usa para generar HTML (Django-like), emails, configs (Ansible, Salt). Frente a concatenar strings: separación de lógica y presentación, escaping por defecto (anti-XSS), reutilización (includes, herencia), y mantenibilidad. Para APIs que solo devuelven JSON no suele hacer falta.

### P37n. ¿Cómo harías scraping robusto con Scrapy (pipelines, throttling, manejo de errores)?

**Respuesta:**  
**Scrapy:** spiders que definen start_urls y parsean; **pipelines** para limpiar, validar y guardar ítems; **middlewares** para retries, user-agent rotativo, proxies. **Throttling:** DOWNLOAD_DELAY, AUTOTHROTTLE; respetar robots.txt y términos de uso. **Errores:** retry en 5xx, ignorar o reintentar según código; logging y estadísticas. No sobrecargar el sitio; considerar caché y deduplicación de URLs.

### P37o. ¿Qué es Faker y para qué lo usarías en tests o desarrollo?

**Respuesta:**  
**Faker** genera datos sintéticos realistas: nombres, emails, direcciones, fechas, texto, etc.; por locale. Uso: **tests** (datos variados sin fixtures enormes); **desarrollo** (llenar DB con datos de prueba); **demos** y documentación. No usar en producción para datos reales; en tests permite property-based style con datos “creíbles” y evita colisiones o valores mágicos.

### P37p. ¿Qué es LangChain (o concepto de cadenas con LLMs) y qué problemas aborda?

**Respuesta:**  
**LangChain** (y similares) es un framework para aplicaciones que usan LLMs: encadenar prompts, herramientas (tools), memoria y fuentes de datos. Aborda: **orquestación** de llamadas a modelos; **RAG** (retrieval-augmented generation) con vectores y contexto; **agents** que deciden qué herramienta llamar; **parsing** de salidas. En una entrevista senior se valora conocer el patrón (prompt + context + tools) más que solo la librería.

### P37q. ¿Qué es ruff y por qué se está adoptando en lugar de flake8 + isort + black?

**Respuesta:**  
**Ruff** es un linter y formateador en **Rust**: muy rápido; reemplaza flake8, isort, y parte de pycodestyle/pylint en un solo binario; puede formatear (compatible con black). Se adopta por **velocidad** (CI más rápida) y **unificación** de herramientas (una config, un comando). Migración gradual: activar reglas por grupos; puede coexistir con black un tiempo.

### P37r. ¿Qué es hatch en el ecosistema Python y para qué se usa?

**Respuesta:**  
**Hatch** es una herramienta moderna de gestión de proyectos Python: entornos, builds, publicación. Gestiona `pyproject.toml`, crea entornos aislados, construye wheels/sdist (sustituto de setuptools/build en el flujo), publica en PyPI. Competidor de poetry en “todo en uno”; más ligero en filosofía. Se usa para crear, construir y publicar paquetes Python de forma estándar (PEP 517/518).

### P37s. ¿Qué es ZeroMQ y cuándo lo usarías frente a HTTP o a Kafka?

**Respuesta:**  
**ZeroMQ** es una librería de mensajería que ofrece sockets de alto nivel (pub/sub, push/pull, request/reply) sin broker (o con broker ligero). Baja latencia; en proceso, entre procesos o entre máquinas. Usar cuando: comunicación **baja latencia** entre servicios, patrones **pub/sub** o **worker** sin desplegar Kafka/RabbitMQ, o integración en el mismo host. HTTP para APIs estándar; Kafka para persistencia, replay y ecosistema de streaming.

### P37t. ¿Qué es Streamlit y qué tipo de aplicaciones permite construir?

**Respuesta:**  
**Streamlit** permite construir **dashboards e interfaces** en Python con poco código: widgets (sliders, selects), gráficos (con Plotly, etc.), y re-ejecución del script al interactuar. Ideal para: prototipos de ML, herramientas internas, visualización de datos. No sustituye a una web app completa (estado limitado, no multi-usuario avanzado); sí para demos y herramientas de datos.

### P37u. ¿Cómo automatizarías pruebas E2E en un frontend web con Selenium desde Python?

**Respuesta:**  
**Selenium** con el driver de Python: elegir driver (Chrome, Firefox) o usar **webdriver-manager** para gestionar binarios; navegar a URLs, localizar elementos (by id, CSS, XPath), clicar y rellenar; assertions sobre texto o estado. Buenas prácticas: **esperas explícitas** (WebDriverWait) en lugar de sleeps; **Page Object** para mantener selectores y acciones en clases; ejecutar en headless en CI; capturas en fallos para depuración. Alternativas: Playwright (Python) para APIs más modernas.

### P37v. ¿Para qué usarías ReportLab en un proyecto Python y qué alternativas conoces?

**Respuesta:**  
**ReportLab** sirve para **generar PDFs** programáticamente: documentos, informes, facturas, formularios. API de bajo nivel (canvas) y de alto nivel (SimpleDocTemplate, flowables). Se usa cuando el PDF debe generarse en el servidor con datos dinámicos. Alternativas: **WeasyPrint** (HTML/CSS a PDF), **Jinja2 + WeasyPrint** para reportes basados en plantillas; **FPDF**, **fpdf2**; para solo rellenar plantillas PDF existentes, **PyPDF2** o **pdfrw**.

---

## Notas finales

- **Cantidad:** este documento incluye más de 100 preguntas con respuestas, cubriendo todos los bloques de habilidades_python.md (paradigmas, lenguaje Python, arquitectura, frameworks, datos, análisis, APIs, event driven, rendimiento, seguridad, testing, CI/CD, DevOps y extras).
- **Carpeta `preguntas/`:** si añades más archivos (por tema, empresa o tipo de entrevista), puedes referenciarlos desde aquí o unificarlos en un índice.
- **Preparación:** conviene practicar respuestas en voz alta y ejemplos de código cortos para preguntas de implementación (descriptor, context manager, decorador, generador, etc.).
- **Temas de habilidades_python.md:** la lista está cubierta de forma amplia; para profundizar en un tema concreto puedes añadir más preguntas con la misma estructura: pregunta clara + respuesta concisa con ejemplos cuando ayude.
