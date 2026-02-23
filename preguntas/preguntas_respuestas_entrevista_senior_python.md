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
El **SRP** (Single Responsibility Principle) es uno de los cinco principios SOLID: una clase o módulo debe tener **una única razón para cambiar**. Si una clase hace varias cosas, cualquier cambio en uno de esos ámbitos te obliga a tocarla, lo que aumenta el riesgo de regresiones y acopla el diseño a múltiples fuentes de cambio.

En un servicio que lee de Kafka y escribe en PostgreSQL, **no** conviene tener una sola clase que lea mensajes, los transforme y los persista. En su lugar, separa:

- Un componente que **solo** lee mensajes (adaptador o consumer de Kafka): conoce el contrato del topic, deserializa y entrega eventos al siguiente eslabón.
- Un componente que **solo** aplica la lógica de negocio o transformación: recibe eventos de dominio, aplica reglas, validaciones y mapeos, y produce lo que hay que persistir.
- Un componente que **solo** persiste (repositorio o adaptador PostgreSQL): recibe DTOs o entidades y los escribe en la base; conoce el esquema y las transacciones.

Así, un cambio en el contrato de Kafka solo afecta al adaptador; un cambio en reglas de negocio solo al transformador; un cambio en el esquema de la base solo al repositorio. En Python esto se implementa con módulos o clases pequeñas, inyección de dependencias (para poder testear cada parte con mocks) y, si quieres, un orquestador o pipeline que conecte los tres (por ejemplo en un bucle que lee → transforma → persiste). Esta separación también facilita escalar o sustituir una capa (por ejemplo cambiar de Kafka a otra cola) sin reescribir todo el servicio.

### P2. Explica la diferencia entre herencia y composición. ¿Cuándo elegirías composición en un diseño orientado a objetos?

**Respuesta:**  
- **Herencia:** la subclase “es un” tipo de la superclase (por ejemplo `Dog` es un `Animal`). La subclase hereda estado y comportamiento y puede sobrescribir métodos. El problema es el **acoplamiento fuerte**: la subclase depende de la implementación de la base, los cambios en la jerarquía pueden romper subclases, y las jerarquías profundas se vuelven frágiles y difíciles de seguir. Además, en Python la herencia múltiple introduce complejidad (MRO, conflictos de nombres).
- **Composición:** un objeto “tiene” otros objetos (por ejemplo `Car` tiene un `Engine` y una lista de `Wheel`). La reutilización se hace por **delegación**: el objeto delega en sus componentes. Hay menor acoplamiento porque puedes sustituir o mockear componentes sin tocar la jerarquía de clases.

Elegiría **composición** cuando: (1) no hay una relación “es un” clara (por ejemplo un `UserService` no “es un” `EmailSender`, sino que “tiene” o “usa” uno); (2) varias clases comparten comportamiento pero no forman una jerarquía natural (en lugar de herencia múltiple, inyecta el comportamiento como dependencia); (3) quiero poder sustituir o probar partes (inyección de dependencias: paso un `EmailSender` real o un mock). El principio “favor composition over inheritance” del libro *Design Patterns* (GoF) aplica sobre todo en dominios donde los requisitos cambian con el tiempo: la herencia tiende a rigidizar el diseño y a crear jerarquías que luego cuesta modificar. La composición permite cambiar el comportamiento cambiando el objeto inyectado sin tocar la clase que lo usa.

### P3. ¿Qué es la programación funcional en Python? Nombra construcciones del lenguaje y de la stdlib que la soportan.

**Respuesta:**  
La **programación funcional** enfatiza: **funciones puras** (mismo input → mismo output, sin efectos secundarios), **inmutabilidad** (evitar mutar datos), **expresiones** en lugar de sentencias (menos estado intermedio) y **composición de funciones** (encadenar transformaciones en lugar de bucles imperativos). Python no es un lenguaje funcional puro, pero incorpora muchas ideas funcionales.

**Construcciones del lenguaje y stdlib:**

- **Funciones de primera clase:** las funciones son objetos; puedes pasarlas como argumentos, devolverlas y guardarlas en estructuras. Eso permite higher-order functions y estrategias inyectables.
- **Closures** y **higher-order functions:** `map`, `filter`, `functools.reduce` aplican funciones a secuencias; las closures capturan variables del ámbito envolvente (útil para factories y decoradores).
- **`functools`:** `partial` para fijar argumentos; `lru_cache` para memoización; `wraps` para preservar metadatos en decoradores.
- **`itertools`:** `chain`, `groupby`, `islice`, `cycle`, generadores infinitos; permiten pipelines lazy sin materializar listas enormes.
- **Comprehensions** (list, dict, set): expresiones que describen transformaciones y filtros de forma declarativa; suelen ser más legibles que un `for` + `append`.
- **Generadores** y `yield`: flujos **lazy** que producen valores de uno en uno; ahorran memoria y encajan bien con pipelines (itertools + generadores).
- **Inmutabilidad:** tuplas, `frozenset`, y disciplina de no mutar listas/dicts dentro de funciones “puras” para que el código sea más predecible y testeable.

Un senior sabe **cuándo** un estilo funcional mejora la legibilidad (pipelines de datos, transformaciones sobre listas/dicts, lógica sin estado compartido) y **cuándo** un enfoque OOP o imperativo es más claro (cuando hay mucho estado, efectos secundarios o el equipo no está acostumbrado a leer código muy funcional).

### P3b. Explica los cinco principios SOLID con un ejemplo breve de cada uno.

**Respuesta:**  
Los principios **SOLID** (por Robert C. Martin) guían el diseño orientado a objetos para conseguir código mantenible y desacoplado.

- **S (Single Responsibility):** Una clase debe tener **una única razón para cambiar**. Si una clase hace varias cosas (por ejemplo “calcular factura” y “enviar email”), un cambio en el envío de emails te obliga a tocar la misma clase que calcula la factura. Solución: separar en clases o módulos distintos (por ejemplo `FacturaCalculator` y `EmailSender` o un servicio de notificaciones).
- **O (Open/Closed):** Las entidades deben estar **abiertas a extensión** pero **cerradas a modificación**. En lugar de añadir un `if tipo == "X"` cada vez que aparece un nuevo tipo, se usan estrategias, políticas inyectadas o polimorfismo: añades una nueva clase que implementa la interfaz y no modificas el código existente.
- **L (Liskov Substitution):** Las subclases deben poder **sustituir** a la clase base sin romper el contrato que los clientes esperan. Ejemplo clásico: si `Cuadrado` hereda de `Rectángulo` y sobrescribes los setters de ancho/alto para que siempre mantengan el mismo valor, un código que asume “rectángulo con ancho y alto independientes” se rompe al usar un `Cuadrado`. La subclase no debe restringir precondiciones ni relajar postcondiciones de forma que sorprenda al cliente.
- **I (Interface Segregation):** Los clientes no deberían depender de interfaces que no usan. En lugar de una interfaz gigante con muchos métodos, define **varios protocolos o interfaces pequeñas**; cada cliente depende solo de los que necesita. Así evitas clases “gordas” y dependencias innecesarias.
- **D (Dependency Inversion):** Depende de **abstracciones**, no de implementaciones concretas. En lugar de que un servicio instancie directamente `PostgresRepository` o llame a un API concreto, recibe por constructor un `Repository` abstracto (o un protocolo). Así puedes cambiar la base de datos o mockear en tests sin tocar el servicio.

### P3c. ¿Qué es el patrón GRASP “Information Expert” y “Creator”?

**Respuesta:**  
**GRASP** (General Responsibility Assignment Software Patterns) es un conjunto de patrones que guían **a qué clase o objeto asignar** cada responsabilidad en un diseño OOP. No son patrones de código como los GoF, sino criterios para decidir “quién hace qué”.

- **Information Expert:** asigna la responsabilidad al **objeto que tiene la información necesaria** para cumplirla. Así se evita que un objeto pida datos a otros para hacer un cálculo que podría vivir donde ya están esos datos. Ejemplo: el **carrito de compra** es el experto en los ítems y sus precios, así que es natural que **calcule el total**; no hace falta un “Calculator” externo que reciba el carrito y devuelva el total, porque el carrito ya tiene todo lo necesario. Esto reduce acoplamiento y mantiene la cohesión.
- **Creator:** responde a “**quién debe crear** una instancia de la clase B”. Los criterios típicos son: (1) quien **contiene** o **agrega** instancias de B (composición); (2) quien **tiene los datos** necesarios para inicializar B; (3) quien **usa** B muy de cerca. Ejemplo: un **Pedido** crea **LineaPedido** porque el pedido contiene las líneas, las agrega a lo largo de su vida y tiene el contexto (pedido_id, etc.) para inicializarlas. Así la creación queda encapsulada y el cliente no conoce los detalles de construcción de `LineaPedido`.

### P3d. ¿Qué es programación estructurada y cómo se relaciona con “goto considerado perjudicial”?

**Respuesta:**  
La **programación estructurada** es un paradigma que organiza el flujo de control usando solo unas pocas estructuras bien definidas: **secuencia** (una instrucción tras otra), **selección** (if/else, case) y **repetición** (while, for), con un único punto de entrada y salida por bloque. Se evitan los **saltos arbitrarios** (como `goto`) que permiten ir a cualquier línea del programa, porque dificultan la lectura y el razonamiento formal sobre el código.

El artículo de **Dijkstra** “Go To Statement Considered Harmful” (1968) argumentaba que el `goto` hacía el código difícil de seguir, de demostrar correcto y de refactorizar; defendía que cualquier programa podía escribirse solo con secuencia, selección y repetición. Hoy la mayoría de lenguajes no incluyen `goto` (o lo restringen); Python **no tiene** `goto`, así que el flujo es estructurado por defecto.

En la práctica, un senior evita **simular** saltos incontrolados: no usar excepciones para control de flujo normal (solo para errores excepcionales), no abusar de `break`/`continue` anidados que oculten la lógica, y preferir funciones pequeñas y early returns en lugar de ramas muy profundas. La idea sigue siendo la misma: flujo claro y predecible.

---

## 2. Lenguaje Python (core)

### P4. ¿Qué es el GIL (Global Interpreter Lock) y qué implicaciones tiene para concurrencia y paralelismo?

**Respuesta:**  
El **GIL** (Global Interpreter Lock) es un mutex a nivel de intérprete en **CPython** que garantiza que solo un hilo ejecute bytecode Python a la vez. Existe por razones de diseño histórico (gestión de memoria del intérprete, simplificación del código en C) y tiene consecuencias directas en cómo usamos concurrencia y paralelismo en Python.

**Implicaciones prácticas:**

- **Concurrencia I/O-bound (red, disco, esperas):** el GIL **no** suele ser un problema, porque en operaciones de I/O el hilo libera el GIL mientras espera. Por tanto, `threading` puede mejorar el rendimiento cuando hay muchas esperas (muchas peticiones HTTP, lectura/escritura de disco), porque otros hilos pueden ejecutar mientras uno está bloqueado en I/O.
- **Paralelismo CPU-bound (cálculos puros):** varios hilos en el **mismo proceso** no ejecutan código Python en paralelo: en todo momento solo uno “tiene” el GIL. Para aprovechar varios núcleos en tareas CPU-bound hace falta **multiprocessing** (procesos separados, cada uno con su propio GIL) o usar código que libere el GIL (extensiones en C, NumPy, etc.). Los procesos no comparten memoria por defecto, así que la comunicación se hace con colas, pipes o memoria compartida.
- **AsyncIO:** no elimina el GIL, pero permite **muchas tareas** I/O-bound en un **solo hilo** mediante corutinas y un event loop. Así se evita el coste de crear muchos hilos y se evita el contenido del GIL; es muy adecuado para servidores con miles de conexiones (APIs, websockets) cuando el cuello de botella es la espera a red o a otros servicios.

En una entrevista senior se espera que propongas la herramienta adecuada al problema: **threading** para I/O con código que no sea async; **multiprocessing** para CPU-bound; **asyncio** para alto I/O concurrente en un solo proceso. También se valora conocer alternativas como **PyPy** (con un GIL más flexible en algunos escenarios) o arquitecturas con múltiples procesos y colas (workers que consumen tareas en paralelo).

### P5. Diferencia entre `__new__` y `__init__`. ¿Cuándo implementarías `__new__`?

**Respuesta:**  
- **`__init__`:** es el inicializador que todos conocemos. Recibe la instancia ya creada (`self`) y los argumentos; **no retorna nada** (devuelve `None`). Su trabajo es establecer el estado inicial de la instancia (atributos, etc.). Se ejecuta **después** de que la instancia existe. Es lo que se usa en el 99% de las clases.
- **`__new__`:** es el **constructor real** a nivel de objeto: es el que **crea** la instancia y la **devuelve**. Recibe la clase (`cls`) y los argumentos; por defecto llama a `object.__new__(cls)` para obtener la instancia. Se ejecuta **antes** que `__init__`; si `__new__` no devuelve una instancia de la clase, `__init__` no se llama.

Se implementa **`__new__`** en casos concretos: (1) **Singleton:** en `__new__` compruebas si ya existe una instancia (por ejemplo en un atributo de clase) y la devuelves; si no, creas una con `super().__new__(cls)` y la guardas. (2) **Subclases de tipos inmutables** (`str`, `int`, `tuple`): no puedes “inicializar” después de creado el objeto, así que la construcción debe hacerse en `__new__` pasando los valores correctos al constructor de la base. (3) **Factory:** devolver una instancia de **otra** clase según los argumentos (aunque a veces es más claro usar una función factory fuera de la clase). En código normal, `__init__` basta; `__new__` es para estos casos especiales.

### P6. ¿Qué son los descriptors? Pon un ejemplo de uso (por ejemplo, validación o lazy attribute).

**Respuesta:**  
Un **descriptor** es un objeto que implementa al menos **`__get__(self, obj, type=None)`** y opcionalmente **`__set__(self, obj, value)`** y **`__delete__(self, obj)`**, y se declara como **atributo de clase** (no de instancia). Cuando Python accede a ese atributo en una instancia (lectura, asignación o borrado), invoca el método correspondiente del descriptor, pasando la instancia y la clase. Así se controla el acceso a atributos de forma **reutilizable** y declarativa.

**Ejemplos de uso:**  
- **`property`** está implementado como descriptor: `__get__` devuelve el valor calculado o guardado, `__set__` y `__delete__` opcionales permiten atributos read-write o read-only.  
- **Validación:** un descriptor que en `__set__` comprueba que el valor cumple una condición (por ejemplo que sea positivo, que sea un string no vacío) y luego lo guarda en `obj.__dict__[nombre]` o en un almacén propio; si no cumple, lanza. Así la validación está centralizada y se reutiliza en varias clases.  
- **Lazy attribute:** un descriptor que en `__get__` comprueba si el valor ya está calculado (por ejemplo en `obj.__dict__`); si no, lo calcula (llamada costosa, lectura de config, etc.), lo guarda en la instancia y lo devuelve. Las siguientes lecturas usan el valor cacheado.

Los descriptors son la **base** de `@property`, `@classmethod`, `@staticmethod` y de ORMs como SQLAlchemy (las columnas del modelo son descriptores que traducen acceso a atributos en consultas y escrituras a la base).

### P7. Explica el orden de resolución de métodos (MRO) en herencia múltiple. ¿Qué es el “diamond problem”?

**Respuesta:**  
En herencia múltiple, cuando una clase hereda de varias (por ejemplo `class C(A, B)`), hace falta un **orden** definido para decidir de qué clase se toma un método o atributo si está en más de un antecesor. Python usa **C3 linearization** para calcular el **MRO** (Method Resolution Order). Puedes inspeccionarlo con `Clase.mro()` o `Clase.__mro__`. El orden respeta: (1) la jerarquía de cada padre (un padre antes que sus ancestros); (2) el orden de declaración en la lista de bases (si A y B están en conflicto, gana el que aparece primero en `class C(A, B)`); (3) que no haya ciclos (C3 falla si la jerarquía es inconsistente).

El **diamond problem** aparece cuando `A` es padre de `B` y `C`, y una clase `D` hereda de `B` y `C`; entonces `A` está dos veces en la jerarquía. En Python, `A` solo se visita una vez gracias al MRO (por defecto después de `B` y `C`), así que un `super()` en `D` puede llegar a `A` de forma predecible. Un senior sabe leer el MRO y diseñar mixins y herencia múltiple sin sorpresas.

### P8. ¿Qué son los context managers? ¿Cómo implementas uno con clase y con `contextlib`?

**Respuesta:**  
Un **context manager** es un objeto que garantiza lógica de **entrada** (setup) y **salida** (teardown) alrededor de un bloque de código, usando la sentencia `with ...`. Así se asegura que los recursos se liberen aunque haya excepciones o returns (equivalente a try/finally, pero reutilizable y legible).

**Implementación con clase:**  
El protocolo requiere **`__enter__(self)`** y **`__exit__(self, exc_type, exc_val, exc_tb)`**. Al entrar en el `with`, se llama a `__enter__`; su valor de retorno se asigna a la variable del `as` (normalmente devuelves el recurso o `self`). Al salir del bloque (normal o por excepción), se llama a `__exit__` con el tipo, valor y traceback de la excepción (o tres `None` si no hubo). Si `__exit__` devuelve **True**, la excepción se considera “manejada” y no se propaga; si devuelve False o nada, la excepción se propaga. Sirve para archivos, conexiones a BD, locks, transacciones (commit en salida normal, rollback en excepción).

**Implementación con `contextlib.contextmanager`:**  
Decoras un **generador** que tiene exactamente un **`yield`**. El código **antes** del `yield` es el setup (equivalente a `__enter__`); el **después** es el teardown (equivalente a `__exit__`). Si se lanza una excepción dentro del `with`, se inyecta en el generador; puedes usar `try/finally` alrededor del `yield` para garantizar limpieza y luego relanzar si quieres. Es más conciso que una clase cuando la lógica es simple.

### P9. Diferencia entre `iterator` e `iterable`. ¿Cómo harías un iterable perezoso sobre una fuente muy grande?

**Respuesta:**  
- **Iterable:** es cualquier objeto del que puedes obtener un iterator, típicamente implementando **`__iter__`** (que devuelve un iterator). También se considera iterable si tiene **`__getitem__`** con índices secuenciales desde 0 hasta que dé `IndexError`. Ejemplos: list, dict, str, set, range. Se usa en `for x in iterable` y en funciones que consumen secuencias.
- **Iterator:** es un objeto que produce valores **uno a uno**; implementa **`__next__`** (devuelve el siguiente o lanza `StopIteration` al terminar) y **`__iter__`** (suele devolver `self` para que el iterator sea también iterable). Un mismo iterable puede dar varios iterators independientes (cada llamada a `__iter__` puede devolver uno nuevo).

Para una **fuente muy grande** (archivo enorme, API paginada, stream de Kafka), no quieres materializar todo en memoria. El patrón estándar es un **generador** (función con `yield`): es iterable (al llamarla obtienes un generator-iterator) y cada elemento se calcula o lee **solo cuando se pide** (lazy). Así recorres la fuente en una pasada sin cargar todo. Alternativamente, una **clase** con `__iter__` y `__next__` que internamente lea por chunks o páginas y vaya devolviendo elementos; útil cuando la lógica de “siguiente” es más compleja que un simple yield.

### P10. ¿Para qué sirven las type hints y `mypy`? ¿Cómo tiparías un decorador que preserva la firma de la función?

**Respuesta:**  
Las **type hints** (PEP 484) permiten anotar argumentos, retornos y variables con tipos (builtins, `typing`, tipos propios). Sirven para **documentar** el contrato de funciones y clases, y para **análisis estático**: un checker puede detectar errores de tipo sin ejecutar el código. **mypy** es el checker estándar en el ecosistema Python; integrado en CI, reduce bugs de tipo y facilita refactors. Las hints no afectan al runtime por defecto (son solo metadatos), aunque se pueden inspeccionar con `typing.get_type_hints`.

Para un **decorador que preserva la firma** hay dos aspectos: (1) **Runtime:** `functools.wraps(f)` en el decorador para copiar `__name__`, `__doc__`, etc., del decorado. (2) **Tipado:** que el tipo del decorado sea el mismo que el de la función original. Se usa un **TypeVar** acotado a `Callable`: por ejemplo `F = TypeVar('F', bound=Callable[..., Any])` y el decorador se anota como `def decorator(f: F) -> F: ... return f`. Así mypy y los IDEs entienden que el resultado tiene la misma firma que `f`. Para decoradores que **añaden** argumentos (por ejemplo inyectar un request), en Python 3.10+ se usan **ParamSpec** y **Concatenate** para expresar que la función decorada tiene los mismos parámetros que `f` más los extra.

### P11. ¿Qué es la recursión y cuándo puede ser problemática en Python? ¿Qué es la cola de llamadas y el límite de recursión?

**Respuesta:**  
**Recursión** es cuando una función se llama a sí misma: suele haber un **caso base** (condición de parada) y un **caso recursivo** que reduce el problema y se llama de nuevo. Es natural para estructuras recursivas (árboles, listas anidadas) o definiciones matemáticas (factorial, Fibonacci).

En Python puede ser **problemática** por dos razones. (1) **Límite de recursión:** el intérprete limita la profundidad de la pila de llamadas (por defecto ~1000; se ve con `sys.getrecursionlimit()`). Si la recursión es más profunda (por ejemplo un árbol muy profundo o una lista muy larga procesada recursivamente), se lanza **RecursionError**. (2) **Pila de llamadas:** cada llamada guarda estado (variables locales, punto de retorno); recursión muy profunda consume mucha memoria de pila y puede provocar overflow o lentitud.

**Alternativas:** reescribir a **iterativo** (bucle con pila explícita si hace falta, por ejemplo para recorrer un árbol); en muchos algoritmos la versión iterativa es más eficiente y sin límite de profundidad. Python **no** optimiza la recursión de cola (TCO), así que “tail recursion” igualmente consume pila. Aumentar `sys.setrecursionlimit()` solo en casos muy controlados (por ejemplo tests que intencionadamente profundizan); no es una solución general porque el límite del sistema operativo también puede cortar el proceso.

### P12. Diferencia entre list comprehension, generator expression y dict/set comprehension. ¿Cuándo usar cada una?

**Respuesta:**  
- **List comprehension** `[x*2 for x in range(10)]`: construye la **lista completa** en memoria de una vez. Úsala cuando necesites la secuencia entera: acceso por índice, `len()`, iterar varias veces, o pasar la lista a código que espere una lista. Si el rango es muy grande, el consumo de memoria puede ser alto.
- **Generator expression** `(x*2 for x in range(10))`: es **lazy**; no materializa todos los elementos; cada uno se calcula cuando se pide (en un `for`, en `next()`, o al pasarlo a `list()`, `sum()`, etc.). Ahorra memoria en secuencias grandes y encaja bien en **pipelines** (varias transformaciones encadenadas que se consumen en una pasada). No tiene longitud ni índices; una vez consumido, no se puede volver a iterar.
- **Dict comprehension** `{k: v*2 for k, v in d.items()}` y **set comprehension** `{x % 3 for x in nums}`: mismo concepto que la list comprehension pero construyen diccionario o conjunto; también materializan todo en memoria.

**Cuándo usar cada una:** generator cuando el flujo es **una pasada** (procesar, agregar, filtrar sin necesitar la colección entera) o cuando el tamaño puede ser muy grande. List (o dict/set) cuando necesitas **múltiples accesos**, índice, longitud o cuando el tamaño es pequeño y la claridad prima.

### P13. ¿Cómo diseñarías una jerarquía de excepciones personalizadas y cuándo usarías excepciones vs códigos de error?

**Respuesta:**  
**Jerarquía de excepciones:** conviene una **base de dominio** (por ejemplo `AppError` o `ValidationError`) que herede de `Exception`, y excepciones **más específicas** por tipo de fallo (por ejemplo `PaymentDeclinedError`, `InsufficientFundsError` que hereden de `PaymentError`). Así el llamador puede capturar por granularidad: `except InsufficientFundsError` para un tratamiento concreto, `except PaymentError` para cualquier error de pago, o `except AppError` como red de seguridad. Documenta qué excepciones puede lanzar cada función; en código que captura, ordena los `except` de más específica a más general.

**Excepciones vs códigos de error:** usa **excepciones** cuando el fallo es **excepcional** (error de red, datos inválidos que no deberían llegar, errores de configuración) y cuando el llamador puede reaccionar con try/except o dejar propagar. Usa **códigos de error** o un tipo **Result/Either** (por ejemplo `tuple[bool, T]` o un dataclass con `success` y `error`) cuando el “fallo” es **parte del flujo normal** (por ejemplo “recurso no encontrado”, “validación rechazada”) y quieres que esté explícito en la firma y en el tipo de retorno; así el llamador está obligado a manejar el caso. En APIs REST, las excepciones se traducen a códigos HTTP (404, 422, 500) y mensajes en el cuerpo; la jerarquía interna puede mapear a códigos estándar.

### P14. ¿Qué son las clases abstractas (ABC) y las interfaces en Python? Diferencia con typing.Protocol.

**Respuesta:**  
- **Clases abstractas (ABC):** en el módulo **`abc`**, una clase que hereda de **`ABC`** puede declarar métodos **abstractos** con **`@abstractmethod`**. No se puede instanciar hasta que una subclase concreta implemente todos los métodos abstractos. Es **contrato por herencia**: el contrato se expresa explícitamente en la jerarquía; las subclases heredan de la base y el type checker sabe que implementan la interfaz. Útil cuando quieres una base común, posible comportamiento por defecto y que “ser un X” signifique heredar de `X`.
- **typing.Protocol** (PEP 544): **structural subtyping** (“duck typing” con tipos). Un protocolo define métodos (y sus firmas); **cualquier** clase que tenga esos métodos cumple el protocolo, **sin heredar** de él. El type checker (mypy) comprueba que el objeto tenga los métodos necesarios cuando lo usas donde se espera el protocolo. Es más **flexible** que ABC: no acoplas la jerarquía de clases a una interfaz; tipos de librerías externas pueden cumplir tu protocolo sin que hereden de tu código. Muy útil para dependencias inyectadas y para anotar “cualquier cosa que tenga `read()` y `write()`”.

**Resumen:** ABC = contrato por **herencia** (subclase explícita); Protocol = contrato por **estructura** (tener los métodos indicados). Ambos permiten polimorfismo y type checking; elige ABC cuando la jerarquía y la herencia son naturales, y Protocol cuando quieres máxima flexibilidad y menos acoplamiento.

### P15. Nombra al menos cinco magic methods y su propósito. ¿Qué hace `__slots__` y cuándo usarlo?

**Respuesta:**  
**Magic methods** (dunder methods) permiten que tus clases se integren con el lenguaje (operadores, `len()`, `with`, etc.). Algunos ejemplos: **`__init__`** — inicialización de la instancia; **`__str__`** / **`__repr__`** — representación en string (usuario vs depuración); **`__len__`** — `len(obj)`; **`__getitem__`** — acceso por índice/slice, base de la iteración por índice; **`__iter__`** y **`__next__`** — iteración; **`__enter__`** y **`__exit__`** — context manager; **`__call__`** — hacer la instancia “llamable”; **`__eq__`**, **`__lt__`** — comparaciones; **`__add__`** — operador `+`.

**`__slots__`:** es un atributo de clase (tupla o lista de nombres de atributos) que **limita** los atributos de instancia a esos nombres. Por defecto cada instancia tiene un **`__dict__`** que consume memoria; con `__slots__` no se crea `__dict__` (salvo que lo incluyas en slots), así que se **ahorra memoria** cuando tienes muchas instancias (por ejemplo millones de objetos de dominio). Además evita crear atributos por typo (asignar `obj.typo` falla si no está en slots). Limitaciones: no se puede añadir atributos dinámicamente; la herencia con clases que mezclan slots y sin slots puede dar problemas; algunas herramientas asumen `__dict__`. Úsalo cuando el número de instancias sea alto y los atributos estén fijos.

### P16. ¿Cómo funciona la serialización en Python (pickle, json, Pydantic)? ¿Cuándo no usar pickle?

**Respuesta:**  
- **pickle:** convierte objetos Python a un flujo de **bytes** (y viceversa). Soporta una amplia gama de tipos y referencias circulares. **Riesgo de seguridad:** la deserialización ejecuta código implícito en la reconstrucción de objetos; un atacante puede construir un payload que ejecute código arbitrario. Por tanto **solo** debe usarse con datos generados por ti, en procesos o máquinas bajo tu control (por ejemplo cache entre procesos del mismo equipo). **No** usar pickle para datos que vengan de usuarios, de la red o de servicios no confiables.
- **json:** formato de **texto** estándar (strings, números, listas, diccionarios, booleanos, null). Interoperable con cualquier lenguaje y sistema. Limitación: solo tipos básicos; fechas, bytes y tipos custom hay que convertirlos a mano. Idóneo para APIs REST y persistencia portable.
- **Pydantic:** modelos con **tipos** que validan al construir y ofrecen **serialización** a dict o JSON (`.model_dump()`, `.model_dump_json()`). Muy usado para configuración, payloads de API y validación de entrada; combina validación y serialización en una sola capa.

**Resumen:** no usar pickle para comunicación entre servicios ni para cualquier dato que no controles por completo; preferir JSON (o similares) y, cuando convenga, Pydantic para validación y salida tipada.

### P17. Explica el modelo de importación de Python: módulos vs paquetes, `__init__.py`, `import` vs `from ... import`, y qué es `sys.path`.

**Respuesta:**  
- **Módulo:** cualquier archivo **`.py`** que puedas importar; el nombre del módulo es el del archivo (sin `.py`). Contiene código ejecutable; la primera vez que se importa se ejecuta y el resultado se guarda en **`sys.modules`** para no volver a ejecutarlo.
- **Paquete:** un **directorio** que Python trata como un conjunto de módulos. En Python 3.3+, puede ser un “namespace package” (varios directorios con el mismo nombre en `sys.path`) sin `__init__.py`; si tiene **`__init__.py`** (puede estar vacío), es un “regular package” y `__init__.py` se ejecuta al importar el paquete. Los subpaquetes son subdirectorios con su propio `__init__.py`.
- **`import foo`** carga el módulo (o paquete) `foo` y lo deja en el namespace con el nombre `foo`; accedes con `foo.bar`. **`from foo import bar`** carga `foo` y pone solo `bar` en el namespace local; **`from foo import *`** no se recomienda (nombres inesperados, difícil de leer).
- **sys.path:** lista de **directorios** donde el intérprete busca módulos. Incluye el directorio del script que ejecutaste, la variable de entorno **PYTHONPATH** y los directorios de **site-packages** (donde pip instala). El primer nombre que coincida con el módulo pedido gana. Modificar `sys.path` en runtime (por ejemplo añadir la raíz del proyecto) funciona pero es frágil; un senior prefiere estructura de proyecto instalable (`pip install -e .`) y imports absolutos desde el paquete raíz.

### P18. ¿Qué es la metaprogramación en Python? Ejemplos: decoradores que modifican clases, o uso de `type()` para crear clases dinámicamente.

**Respuesta:**  
**Metaprogramación** es código que **genera o modifica** código (o estructuras de programa) en **tiempo de ejecución**. En Python hay varias formas:

- **Decoradores que modifican clases:** un decorador que recibe una clase puede añadir o reemplazar métodos, registrar la clase en un registro, o inyectar atributos. Ejemplo: registradores de rutas en frameworks web que marcan métodos como endpoints.
- **`type(name, bases, dict)`:** con tres argumentos, **crea una nueva clase** dinámicamente: nombre, tupla de bases y diccionario de atributos (métodos, class variables). Es lo que hace internamente `class Nombre(Base): ...`. Útil cuando la clase depende de configuración o de datos que solo existen en runtime.
- **Metaclasses:** la “clase de una clase”. Si defines `class Meta(type)` y usas `metaclass=Meta`, al crear una subclase se invoca `Meta`; sirve para validar que las subclases implementen ciertos métodos, registrar clases, o alterar la creación (por ejemplo ORMs que crean tablas a partir del modelo).
- **Herramientas que generan código:** **dataclasses**, **attrs**, **Pydantic** generan `__init__`, `__repr__`, etc., a partir de anotaciones; es metaprogramación que simplifica boilerplate.

Se usa **con mesura**: cuando herencia, composición o decoradores simples bastan, preferirlos; la metaprogramación puede dificultar la depuración y la lectura si se abusa.

### P19. ¿Cómo implementarías un worker pool con threading y otro con multiprocessing? ¿Cuándo usar cada uno?

**Respuesta:**  
- **Threading:** se usa **`concurrent.futures.ThreadPoolExecutor`** (o el módulo `threading` directamente). Creas un pool con un número fijo de workers (p. ej. 4 o 10) y envías tareas con `executor.submit(fn, *args)` o `executor.map()`. Las tareas son **I/O-bound** (peticiones HTTP, lecturas de BD, disco): mientras un hilo espera, otros pueden ejecutar. Las threads **comparten memoria**, así que hay que tener cuidado con race conditions (locks, estructuras thread-safe). El GIL hace que solo una ejecute bytecode Python a la vez, pero en I/O el GIL se libera, así que el pool puede mejorar el rendimiento.
- **Multiprocessing:** **`concurrent.futures.ProcessPoolExecutor`** o **`multiprocessing.Pool`**. Cada worker es un **proceso** separado con su propio intérprete y memoria; no comparten estado por defecto. La comunicación es por **queues**, **pipes** o **memoria compartida** (Value, Array). Idóneo para tareas **CPU-bound** (cálculos pesados, procesamiento de datos) porque así se usan varios núcleos. Los argumentos y resultados deben ser **serializables** (pickle).

**Cuándo usar cada uno:** si el cuello de botella es **I/O** (red, disco, BD) → threads o, mejor aún, asyncio si tu código es async. Si el cuello de botella es **CPU** → multiprocessing. No uses muchos procesos si el coste de serialización y arranque es alto; en ese caso valora colas externas (Celery, etc.) con workers en procesos.

### P20. ¿Qué son las coroutines y el event loop en asyncio? Diferencia entre `async def` y una función normal que devuelve una coroutine.

**Respuesta:**  
- **Coroutine:** en Python es el objeto que produce una función definida con **`async def`**. Al **llamar** esa función no se ejecuta el cuerpo; se devuelve un **objeto coroutine**. El cuerpo solo se ejecuta cuando esa coroutine se **“awaita”** (con `await coro` o cuando el event loop la programa). `await` cede el control al event loop hasta que el resultado esté disponible (I/O completado, otra coroutine terminada, etc.), sin bloquear el hilo.
- **Event loop:** es el núcleo de asyncio; **ejecuta** las coroutines, programa callbacks y maneja la I/O (sockets, timers). Cuando una coroutine hace `await`, el loop puede ejecutar otras coroutines; cuando el recurso esperado está listo, el loop reanuda la coroutine. Todo esto ocurre en **un solo hilo** (concurrencia cooperativa).
- **Diferencia importante:** una **función normal** que devuelve una coroutine (por ejemplo `def f(): return asyncio.sleep(1)`) **no ejecuta** la coroutine al ser llamada; solo devuelve el objeto. Para ejecutarla hay que hacer `await f()` (dentro de un contexto async) o `loop.run_until_complete(f())`. Con **`async def`** y **`await`** se escribe código concurrente legible sin callbacks explícitos; el flujo parece secuencial pero es no bloqueante.

### P21. ¿Para qué sirven `functools.partial`, `functools.lru_cache` y `functools.wraps`?

**Respuesta:**  
- **`functools.partial`:** crea una **nueva llamable** fijando algunos argumentos (y palabras clave) de una función. Por ejemplo `partial(int, base=2)` devuelve una función que convierte a entero en binario; útil para callbacks que requieren una firma concreta (p. ej. pasar a `map` una función que ya tiene el primer argumento fijado) o para especializar una función genérica sin definir una nueva.
- **`functools.lru_cache`:** decorador que **cachea** en memoria los resultados de la función por conjunto de argumentos (hashables). Usa política **LRU** (Least Recently Used); con `maxsize=None` la cache crece sin límite; con `maxsize=N` se descartan las entradas menos usadas. Ideal para funciones **puras** y costosas (cálculos, llamadas a APIs que no cambian); no usar con argumentos mutables o no hashables sin cuidado. En Python 3.9+ se puede usar también `@cache` para cache sin límite.
- **`functools.wraps`:** decorador que **copia metadatos** de la función decorada al wrapper (`__name__`, `__doc__`, `__module__`, etc.). Sin él, el wrapper tendría el nombre y la documentación del propio wrapper, lo que rompe ayuda, logging y debugging. Es **esencial** usarlo en cualquier decorador que devuelva una función nueva.

### P22. Nombra cinco funciones o generadores de itertools que uses en código real y para qué.

**Respuesta:**  
- **`chain(*iterables)`:** concatena varios iterables en uno solo **sin materializar** listas intermedias; útil para recorrer varios archivos o listas como si fuera una secuencia única.
- **`groupby(iterable, key=None)`:** agrupa elementos consecutivos que comparten la misma **clave** (por defecto el valor). Requiere que el iterable esté **ordenado** por esa clave; si no, los grupos se fragmentan. Útil en pipelines de datos (agrupar líneas por fecha, por id, etc.).
- **`islice(iterable, start, stop[, step])`:** “rebanada” sobre un iterable de forma **lazy** (como `list[start:stop:step]` pero sin cargar todo); ideal para paginación o para tomar los primeros N de un stream.
- **`cycle(iterable)`** y **`repeat(elem[, n])`:** el primero repite el iterable infinitamente; el segundo repite un elemento N veces o infinitas. Sirven para tests (datos cíclicos), padding o patrones repetitivos.
- **`combinations(iterable, r)`** y **`permutations(iterable, r)`:** generan combinaciones o permutaciones **sin cargar** todas en memoria; útiles en algoritmos de combinatoria o generación de casos de test.

Uso típico: **pipelines** de transformaciones sobre streams, parsing de logs o CSV, y generación de datos para tests o benchmarks.

### P23. ¿Qué ofrece el módulo collections (defaultdict, Counter, OrderedDict, namedtuple, deque)? ¿Cuándo usar deque en lugar de list?

**Respuesta:**  
- **defaultdict(factory):** subclase de dict que, cuando se accede a una **clave inexistente**, la crea con el valor devuelto por `factory()` (por ejemplo `list` para listas, `int` para 0). Evita el patrón `if k not in d: d[k] = []; d[k].append(v)`; muy usado para agrupar o acumular por clave.
- **Counter(iterable):** dict especializado en **contar** ocurrencias; `.most_common(n)` da los n más frecuentes; soporta suma y resta entre Counters. Ideal para histogramas, análisis de frecuencias o “top N”.
- **OrderedDict:** dict que mantiene el **orden de inserción**. En Python 3.7+ el `dict` estándar también mantiene orden, así que OrderedDict queda sobre todo para métodos específicos (move_to_end) o compatibilidad.
- **namedtuple:** construye una subclase de tupla con **nombres de campos**; acceso por atributo (`obj.campo`) además de índice; inmutable y ligera. Útil para datos pequeños y legibles (puntos 2D, registros simples). Para más features (defaults, mutabilidad) se suele usar dataclass.
- **deque:** cola **doble**; **append**/ **appendleft** y **pop**/ **popleft** en **O(1)**. **Usar deque** cuando necesites FIFO (cola), LIFO (pila) o ventanas deslizantes (append por un lado, popleft por el otro). Con **list**, insert o pop al **inicio** es O(n) porque hay que desplazar el resto; deque evita eso.

**Resumen:** deque para colas y operaciones por ambos extremos; list para acceso por índice y cuando no importa el coste de insert/pop al inicio.

### P24. ¿Cómo depurar con pdb? Comandos básicos: breakpoint, next, step, continue, list, pp.

**Respuesta:**  
Para detener la ejecución en un punto: insertar **`breakpoint()`** (Python 3.7+; respeta la variable de entorno `PYTHONBREAKPOINT`) o **`import pdb; pdb.set_trace()`**. Al llegar ahí, se abre el prompt de pdb.

**Comandos básicos:**  
- **n** (next): ejecuta la **siguiente línea** en la función actual; no entra en llamadas.  
- **s** (step): **entra** en la próxima llamada (ejecuta paso a paso dentro de la función llamada).  
- **c** (continue): reanuda hasta el **siguiente breakpoint** o hasta el final.  
- **l** (list): muestra **código** alrededor de la línea actual.  
- **pp** (pretty-print): imprime expresiones con formato legible (útil para listas o dicts grandes).  
- **p** (print): evalúa e imprime una expresión.  
- **b** (break): define breakpoints; por ejemplo **b archivo:línea** o **b función**.  
- **q** (quit): sale del debugger y termina el programa.

En desarrollo real se suele usar el **debugger del IDE** (VS Code, PyCharm), que integra pdb o un equivalente y ofrece breakpoints visuales, inspección de variables y ventanas de pila.

### P24b. ¿Cómo escribirías un decorador que acepte argumentos (ej. reintentos o un timeout)?

**Respuesta:**  
Si el decorador debe recibir argumentos, se usan **dos niveles**: una función que recibe los argumentos y devuelve el decorador real, y el decorador que recibe la función. Ejemplo: `def retry(max_attempts):` → `def decorator(f):` → `def wrapper(*args, **kwargs):` … → `return decorator`. Así `@retry(3)` llama a `retry(3)`, que devuelve `decorator`, y el resultado de `decorator(f)` es `wrapper`. Usar `functools.wraps` en el wrapper.

### P24c. ¿Qué es una metaclass y en qué caso la usarías?

**Respuesta:**  
Una **metaclass** es la clase de una clase; su `__new__` o `__init__` se ejecuta cuando se define una clase. Casos: **registro** automático de subclases (plugins); **validación** de que las subclases implementan métodos o atributos; **API** que exige un estilo de definición (ej. ORM que crea tablas a partir de la clase). Usar con moderación; a menudo decoradores o ABC alcanzan. Ejemplo: `type` es la metaclass por defecto; puedes heredar de `type` y sobrescribir `__new__`.

### P25. ¿Cómo estructurarías logging en una aplicación Python (niveles, formateo, handlers, no loguear en producción con DEBUG)?

**Respuesta:**  
- **Estructura:** usar un **logger por módulo** (`logging.getLogger(__name__)`) en lugar de el root directamente; así se puede configurar nivel y handlers por paquete. El root logger se configura una vez al arranque (en `main` o en un módulo `logging_config`).
- **Niveles:** DEBUG (desarrollo, diagnóstico), INFO (flujo normal), WARNING (algo anómalo pero recuperable), ERROR (fallo que requiere atención), CRITICAL (sistema inestable). En **producción** típicamente INFO o WARNING para no llenar discos ni agregadores; DEBUG solo en entornos de staging o con activación bajo demanda.
- **Handlers:** **StreamHandler** (stderr/consola), **FileHandler** (rotación con RotatingFileHandler o TimedRotatingFileHandler), o envío a un servicio (SysLogHandler, HTTP a un agregador como Loki, Datadog). Puedes tener varios handlers en el mismo logger (p. ej. consola + archivo).
- **Formato:** incluir **timestamp**, **nivel**, **nombre del logger** (o módulo) y **mensaje**; en producción suele convenir **JSON** (con formateador JSON) para que los agregadores parseen y filtren por nivel, servicio, etc.
- **Rendimiento:** evitar en hot path construcciones costosas que solo se usan para DEBUG; usar el patrón de **argumentos** (`logger.debug("user %s", user_id)`) para que la interpolación solo ocurra si el nivel está activo, o comprobar `if logger.isEnabledFor(logging.DEBUG):` antes de construir el mensaje.

### P26. ¿Qué es PEP 8 y qué herramientas usas para aplicarlo automáticamente?

**Respuesta:**  
**PEP 8** es la guía de estilo oficial para código Python: indentación (4 espacios), longitud de línea (recomendado 79 o 88), espacios alrededor de operadores y después de comas, convenciones de nombres (snake_case para funciones y variables, CapitalizedWords para clases, etc.), y recomendaciones sobre imports, comentarios y documentación. No es obligatorio pero mejora la consistencia y la legibilidad en equipos.

**Herramientas para aplicarlo automáticamente:**  
- **black:** formateador **opinado** que reescribe el código (indentación, comillas, saltos de línea); tiene poca configuración a propósito para que todo el ecosistema se parezca. Muy usado como estándar de facto.  
- **isort:** ordena y agrupa **imports** (stdlib, third-party, local) y puede eliminar no usados.  
- **ruff:** linter y formateador muy rápido; puede reemplazar flake8, isort y parte de pylint, y tiene un modo formateador compatible con black.  
- **flake8:** lint estático que comprueba estilo (PEP 8) y algunos errores (variables no usadas, sintaxis dudosa).  
- **pylint:** más reglas y advertencias (calidad, complejidad, convenciones); más ruido pero útil para revisar código.

En **CI** se suele ejecutar black (o ruff format) + isort (o ruff) y flake8 o ruff; la configuración y versiones se fijan en **pyproject.toml** o **setup.cfg** para que todo el equipo y CI usen lo mismo.

---

## 3. Arquitectura de software

### P11. ¿Qué es Event Sourcing y cuándo lo recomendarías frente a un modelo CRUD clásico?

**Respuesta:**  
**Event Sourcing** es un patrón en el que en lugar de guardar solo el **estado actual** de una entidad (como en CRUD), se persiste la **secuencia de eventos** (hechos) que llevaron a ese estado. El estado “actual” se obtiene **reconstruyéndolo** aplicando los eventos en orden (replay). Además puedes mantener **múltiples proyecciones** (vistas materializadas) leyendo el mismo stream y derivar nuevos modelos sin modificar el stream; y puedes **reprocesar** el pasado (corregir bugs de proyección, añadir nuevas vistas).

**Cuándo recomendarlo:** cuando hay requisitos fuertes de **auditoría** o compliance (saber qué pasó y cuándo); cuando necesitas “**viajar en el tiempo**” o hacer replay para análisis o correcciones; en dominios donde los **hechos** son la fuente de verdad (finanzas, logística, trazabilidad); o cuando ya usas **CQRS** y quieres que el modelo de lectura sea una proyección del stream, pudiendo cambiar las vistas sin tocar los eventos. **No** lo recomendaría para dominios muy simples (CRUD basta), ni cuando el equipo no tiene experiencia en consistencia eventual, modelado de eventos y operaciones de replay; el coste operativo y de complejidad es alto.

### P12. Diferencia entre CQRS y “una base de datos con lecturas y escrituras”.

**Respuesta:**  
**CQRS** (Command Query Responsibility Segregation) separa explícitamente el **modelo de escritura** del **modelo de lectura**: los **comandos** (escrituras) modifican estado y pueden vivir en un modelo normalizado y consistente; las **consultas** (lecturas) pueden usar modelos desnormalizados, vistas materializadas o incluso otro almacén, optimizados para pantallas y reportes. No obliga a tener dos bases de datos; puede ser el mismo almacén con dos “capas” de modelo (escritura normalizada, lecturas desnormalizadas o cacheadas).

La diferencia con “una base de datos donde se lee y se escribe” es la **intención y el diseño**: en un CRUD clásico sueles tener un único modelo que sirve para todo; en CQRS **aceptas** que el modelo de lectura sea distinto del de escritura: optimizado por caso de uso (pantalla de detalle, listado, dashboard), posiblemente con proyecciones desde un stream de eventos (Event Sourcing). Ventajas: escalar **lectura** y **escritura** por separado (más réplicas de lectura, escritura en un solo sitio); usar **almacenes distintos** (escritura en SQL, lectura en Elasticsearch o en caché); evolución independiente de consultas sin tocar el modelo de escritura. La complejidad añadida (sincronización, consistencia eventual) solo compensa cuando los requisitos de lectura y escritura son realmente distintos.

### P13. ¿Qué es un Message Bus o Event Bus y qué problemas resuelve en un sistema distribuido?

**Respuesta:**  
Un **message bus** o **event bus** es un **intermediario** entre productores y consumidores: los publicadores envían mensajes a un **canal**, **topic** o **cola**, y los suscriptores los reciben **sin conocerse** entre sí (desacoplamiento en tiempo y en espacio). Los productores no llaman directamente a los consumidores; el bus entrega (o encola) los mensajes según suscripciones o colas.

**Problemas que resuelve:** (1) **Desacoplamiento:** añadir o cambiar consumidores sin tocar productores; cada parte depende del contrato del mensaje, no del otro servicio. (2) **Escalabilidad:** puedes añadir más **workers** que consumen de la misma cola (distribución de carga) o más suscriptores a un topic (broadcast). (3) **Resiliencia:** muchos buses persisten mensajes y permiten reintentos y dead-letter; si un consumidor cae, el mensaje no se pierde. (4) **Trazabilidad:** los eventos quedan registrados; útil para auditoría y debugging.

En Python: **Celery** con Redis/RabbitMQ para tareas asíncronas; **Kafka** para event streaming y logs; o un bus interno en memoria para un monolito modular. Un senior sabe **cuándo** un bus aporta valor (múltiples consumidores, procesos asíncronos, límites de contexto entre equipos) y **cuándo** es overkill (flujo síncrono simple entre dos componentes).

### P14. ¿Qué es el patrón MVC y cómo se traduce en Django (MVT)?

**Respuesta:**  
**MVC** (Model-View-Controller): **Model** = datos y lógica de negocio; **View** = presentación (lo que ve el usuario); **Controller** = recibe el input del usuario, actualiza el modelo y decide qué vista mostrar. La idea es separar responsabilidades para que el modelo no dependa de la UI y la vista no contenga lógica de negocio.

En **Django** el patrón se llama **MVT** (Model-View-Template). La correspondencia es: el **Model** es el mismo (ORM, lógica de dominio). La **Template** es la “V” de MVC: el HTML y la presentación. La **View** en Django es en realidad el **Controller**: la función o clase que recibe la petición HTTP, consulta o actualiza el modelo, y devuelve una respuesta (normalmente renderizando una template con un contexto). No hay un componente llamado “Controller”; Django usa el nombre “View” para ese papel. El **enrutado por URL** (urls.py) actúa como front controller que delega en la View correspondiente según la ruta.

### P14b. ¿Qué es Pub/Sub y en qué se diferencia de una cola punto a punto?

**Respuesta:**  
- **Pub/Sub (publish/subscribe):** el publicador envía un mensaje a un **topic** (o canal); **todos** los suscriptores de ese topic reciben una **copia** del mensaje. No hay “dueño” único del mensaje: sirve para **broadcasting** y desacoplamiento (varios sistemas reaccionan al mismo evento). Ejemplo: evento “PedidoCreado” y suscriptores de envío de email, de inventario y de analytics; cada uno procesa el mismo evento.
- **Cola punto a punto:** el mensaje va a una **cola**; **un solo** consumidor (entre los workers que atienden esa cola) lo procesa. Sirve para **distribución de carga** y para garantizar que cada mensaje se procese **una vez** (entre los workers de la cola). Ejemplo: cola de “enviar email”; uno de N workers toma el mensaje y lo procesa.

**Matices:** en **Kafka**, con **consumer groups** cada partición es consumida por un solo miembro del grupo, así que por topic/partición se comporta más como cola; si quieres pub/sub, distintos consumer groups se suscriben al mismo topic. **RabbitMQ** tiene ambos: exchanges **fanout** = pub/sub (el mensaje a todos los bindings); **queues** = punto a punto (compiten por los mensajes de la cola).

### P14c. ¿Cómo descompondrías un monolito en microservicios? Qué criterios usarías para definir límites.

**Respuesta:**  
**Criterios para definir límites:** (1) **Dominio / bounded context (DDD):** agrupar por capacidad de negocio coherente (pedidos, catálogo, envíos); no por capas técnicas (un “servicio de base de datos” no es un buen límite). (2) **Equipo (ley de Conway):** si un equipo puede poseer un servicio de punta a punta, el límite suele ser más estable; evitar servicios que requieran coordinación constante entre muchos equipos. (3) **Escalado:** separar lo que escala de forma distinta (p. ej. generación de informes pesados vs API de consulta). (4) **Tecnología:** permitir stacks distintos solo cuando aporte valor (por ejemplo un servicio de ML en Python y el resto en Java); no fragmentar por tecnología por inercia.

**Pasos de descomposición:** identificar **bounded contexts** y sus APIs (qué exponen y qué consumen); elegir un primer servicio a extraer (bien delimitado y con menos dependencias); aplicar **strangler fig**: poner un proxy o API gateway que delegue al monolito o al nuevo servicio según ruta/capacidad; migrar tráfico de forma gradual; mantener **contratos estables** (versionado de API, eventos con esquemas claros). No intentar extraer todo a la vez; ir por capacidades completas y con tests y monitoreo en cada paso.

### P14d. ¿Qué es DDD (Domain-Driven Design) y qué son el bounded context y el agregado?

**Respuesta:**  
**DDD** es un enfoque para modelar software alrededor del dominio: lenguaje ubicuo, modelo rico (no anémico), colaboración con expertos del dominio. **Bounded context:** límite explícito dentro del cual un modelo (términos, entidades) es consistente; distintos contextos pueden tener entidades con el mismo nombre pero significado distinto. **Agregado:** cluster de entidades que se modifican juntas, con una raíz (aggregate root) que garantiza invariantes; las transacciones no cruzan agregados.

### P14e. ¿Qué es un pipeline ETL y qué consideraciones tendrías para hacerlo robusto (idempotencia, reintentos, monitoreo)?

**Respuesta:**  
Un **pipeline ETL** es un flujo de datos en tres fases: **Extract** (leer desde orígenes: bases de datos, APIs, ficheros), **Transform** (limpieza, normalización, reglas de negocio, agregaciones) y **Load** (escribir en el destino: data warehouse, lago, otra base). Se orquesta con herramientas como **Airflow**, **Prefect** o **Dagster**, que definen DAGs (grafos de tareas) con dependencias y programación.

**Consideraciones para robustez:** (1) **Idempotencia:** re-ejecutar el pipeline (o un paso) no debe duplicar datos ni corromper el destino; usar claves naturales o “upsert” y ventanas de datos reproducibles. (2) **Reintentos:** fallos transitorios (red, timeout) se manejan con reintentos con **backoff** exponencial y un **dead-letter** o alerta si se supera el máximo. (3) **Orden y dependencias:** definir bien las dependencias entre pasos (DAG) para que no se ejecute Load antes de Transform; usar checkpoints o particiones por fecha cuando aplique. (4) **Monitoreo:** métricas de latencia, tasa de fallos, volumen procesado y alertas cuando un paso falle o se retrase. (5) **Versionado:** de esquemas (evolución de tablas) y de reglas de transformación para poder reproducir y auditar. (6) **Tests:** pruebas sobre datos de ejemplo o sintéticos para validar transformaciones y detección de regresiones.

---

## 4. Frameworks MVC / Web

### P15. ¿Cómo diseñarías una API REST escalable y mantenible en FastAPI?

**Respuesta:**  
- **Diseño REST:** recursos como sustantivos en la URL (`/users`, `/orders`), verbos HTTP estándar (GET idempotente y sin efectos, POST para crear, PUT/PATCH para actualizar, DELETE para borrar), **códigos HTTP** correctos (200, 201, 204, 400, 401, 404, 422, 500) y cuerpos en JSON con esquemas documentados. Evitar verbos en la URL y devolver recursos completos o enlaces cuando aplique HATEOAS.
- **Estructura en FastAPI:** **routers por dominio** (`APIRouter` por recurso o módulo) que se incluyen en la app; **modelos Pydantic** para request y response (validación y documentación automática); **inyección de dependencias** para sesión de BD, servicios y autenticación (evitar globals). La **documentación** OpenAPI (Swagger/ReDoc) sale automática.
- **Capas:** rutas solo reciben/validan y llaman a **servicios** (lógica de negocio); servicios usan **repositorios** o clientes para acceso a datos. No poner lógica de negocio en el router.
- **Versionado** (por ejemplo `/v1/users`) y convenciones de nombres consistentes en todo el API.
- **Autenticación y autorización:** OAuth2, JWT o API keys implementados como **dependencias** que extraen y validan el token y exponen el usuario o el scope; uso de `Depends()` en rutas protegidas.
- **Paginación, filtros y orden** en listados (query params: `limit`, `offset` o cursor, `sort`, `filter`) para no devolver colecciones enormes y permitir consumo eficiente.

### P16. Diferencia entre Gunicorn y Uvicorn. ¿Cuándo usar cada uno?

**Respuesta:**  
- **Gunicorn:** es un servidor **WSGI** (Web Server Gateway Interface). Gestiona **múltiples workers** (procesos) y opcionalmente hilos por worker; no ejecuta código async ni ASGI. Ideal para aplicaciones **síncronas**: Django con vistas sync, Flask clásico, cualquier app que use el protocolo WSGI. Muy usado en producción detrás de un proxy (Nginx) por su estabilidad y configuración (timeouts, workers, preload).
- **Uvicorn:** es un servidor **ASGI** (Asynchronous Server Gateway Interface). Soporta **async** (corutinas) y **WebSockets**. Ideal para **FastAPI**, **Starlette**, Django con vistas async. Por defecto corre en un solo proceso; en producción se suele combinar con **Gunicorn** como process manager y Uvicorn como worker class (`gunicorn -k uvicorn.workers.UvicornWorker app:app`) para tener varios procesos ASGI y aprovechar varios núcleos.

**Resumen:** aplicación **síncrona** (Flask, Django sync) → **Gunicorn**. Aplicación **async** (FastAPI, Django async) → **Uvicorn** solo o **Gunicorn + Uvicorn** como worker para múltiples procesos.

### P17. ¿Qué es el ciclo de vida de una petición en Django (desde la petición HTTP hasta la respuesta)?

**Respuesta:**  
1. **WSGI/ASGI:** el servidor (Gunicorn, Uvicorn, etc.) recibe la petición HTTP y la pasa a Django mediante el protocolo WSGI o ASGI.
2. **Middleware (request):** se ejecuta la cadena de middleware en **orden de definición**. Cada uno puede modificar el request, cortocircuitar (devolver respuesta) o llamar a `get_response` para pasar al siguiente. Típicamente aquí se hace autenticación, carga de sesión, CSRF, etc.
3. **URL resolver:** Django compara la ruta con las patrones en `urls.py` y resuelve la **View** (función o clase) y los argumentos capturados (p. ej. `pk`).
4. **View:** se ejecuta la vista con el request y los kwargs; puede usar formularios, modelos, servicios, y devuelve un **HttpResponse** (o subclase: JsonResponse, HttpResponseRedirect, etc.). Si usa **templates**, las renderiza aquí con un contexto. Si está decorada con **`@transaction.atomic`**, la transacción se abre antes y se hace commit/rollback según el resultado.
5. **Middleware (response):** se ejecutan en **orden inverso**; cada middleware puede modificar la respuesta antes de devolverla.
6. **WSGI/ASGI** envía la respuesta al cliente.

Además, durante la view pueden dispararse **signals** (pre_save, post_save, request_finished, etc.) si hay listeners registrados; y las **templates** se renderizan dentro de la view antes de construir la HttpResponse.

### P17b. ¿Cómo implementarías autenticación y autorización en Django (usuarios, permisos, grupos)?

**Respuesta:**  
- **Autenticación:** el modelo **User** (o un perfil extendido con **OneToOne**) representa al usuario. En vistas que reciben credenciales se usa **`authenticate(request, username=..., password=...)`** y, si devuelve un usuario, **`login(request, user)`** para asociar la sesión. Para vistas que requieren usuario logueado: **`@login_required`** (FBV) o **`LoginRequiredMixin`** (CBV); si no está autenticado, redirige al login.
- **Autorización (permisos):** Django tiene permisos por modelo (`add_foo`, `change_foo`, `delete_foo`, `view_foo`) y permisos custom. **`user.has_perm('app.perm_codename')`** o **`@permission_required('app.perm')`** / **`PermissionRequiredMixin`** en la view. Los **grupos** agrupan permisos; asignas usuarios a grupos para no gestionar permisos uno a uno.
- **APIs (DRF):** **TokenAuthentication** (token en header), **JWTAuthentication** (p. ej. djangorestframework-simplejwt), o **SessionAuthentication** para uso desde el navegador. Se configura en `DEFAULT_AUTHENTICATION_CLASSES` y las vistas protegidas con permisos o custom checks.
- **Autorización a nivel de objeto:** el sistema de permisos de Django es por modelo, no por instancia. Para “solo el dueño puede editar este objeto” se usa **django-guardian** (permisos por objeto) o lógica en la view que compruebe que `request.user` es el propietario o tiene relación con el objeto.

### P17c. Diferencia entre Django ORM y SQLAlchemy. ¿Cuándo elegirías cada uno?

**Respuesta:**  
- **Django ORM:** viene **integrado** en Django; API de alto nivel con **QuerySets** (lazy, encadenables, filtros, anotaciones, select_related/prefetch_related), **migraciones** integradas y **admin** automático. Muy orientado a aplicaciones web: modelos declarativos, relaciones FK/M2M, y convenciones “Django”. Ideal cuando todo el stack es Django y los modelos son estándar (CRUD, relaciones típicas).
- **SQLAlchemy:** **independiente** del framework; tiene **Core** (SQL expresivo, conexiones, transacciones) y **ORM** (mapeo objeto-relacional más configurable). Permite consultas raw, múltiples backends, conexiones y pools finos, y optimizaciones avanzadas (bulk, reflección de esquema). Ideal para **FastAPI**, **scripts**, **ETL**, servicios que no usan Django, o cuando necesitas **control fino** y máximo rendimiento en consultas complejas.

**Cuándo elegir:** si el proyecto es **Django** (web o API con Django REST), usa **Django ORM** por consistencia y ecosistema (admin, migraciones, forms). Si el proyecto **no** es Django (FastAPI, Celery workers, ETL, librerías) o necesitas flexibilidad y rendimiento por encima de la integración Django, usa **SQLAlchemy**.

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
