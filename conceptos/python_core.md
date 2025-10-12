# Python Core

¡Excelente objetivo! Convertirse en un programador senior en Python no se trata solo de conocer más librerías, sino de entender el *porqué* y el *cómo* del lenguaje en su nivel más fundamental. Un senior domina los mecanismos internos, los patrones de diseño y las compensaciones (trade-offs) de cada decisión.

Aquí tienes una guía profunda sobre Python Core, diseñada para llevarte de un nivel intermedio a uno avanzado/senior.

---

# Guía Profunda de Python Core para el Desarrollador Senior

Ser un programador senior en Python va más allá de la sintaxis. Implica un profundo entendimiento del modelo de datos, la gestión de memoria, la concurrencia y el ecosistema que rodea al lenguaje. Esta guía se enfoca en esos pilares.

> "Python is a language for consenting adults." — Guido van Rossum

Esta cita es clave. Python te da el poder de hacer cosas complejas y "peligrosas" (como modificar clases en tiempo de ejecución), confiando en que sabes lo que haces. Un senior entiende y respeta este poder.

## Tabla de Contenidos
1.  [El Modelo de Datos de Python: El Corazón de lo "Pythónico"](#1-el-modelo-de-datos-de-python-el-corazón-de-lo-pythónico)
2.  [Funciones como Objetos de Primera Clase: Decoradores y Closures](#2-funciones-como-objetos-de-primera-clase-decoradores-y-closures)
3.  [Iteradores, Generadores y el Protocolo de Iteración](#3-iteradores-generadores-y-el-protocolo-de-iteración)
4.  [Gestión de Contexto y la Sentencia `with`](#4-gestión-de-contexto-y-la-sentencia-with)
5.  [Metaprogramación: Clases Dinámicas y Metaclases](#5-metaprogramación-clases-dinámicas-y-metaclases)
6.  [Concurrencia y Paralelismo: El GIL y Cómo Superarlo](#6-concurrencia-y-paralelismo-el-gil-y-cómo-superarlo)
7.  [CPython Internals: Un Vistazo Bajo el Capó](#7-cpython-internals-un-vistazo-bajo-el-capó)
8.  [Ecosistema y Herramientas del Programador Senior](#8-ecosistema-y-herramientas-del-programador-senior)
9.  [Recursos Imprescindibles](#9-recursos-imprescindibles)

---

### 1. El Modelo de Datos de Python: El Corazón de lo "Pythónico"

Un senior no ve Python como un conjunto de comandos, sino como un framework consistente. El modelo de datos es la API que te permite hacer que tus propios objetos se comporten como los nativos.

**Concepto Clave:** Los métodos especiales (special methods), también conocidos como "dunder methods" (por *double underscore*), son la clave. Cuando haces `len(mi_objeto)`, Python no busca un método `mi_objeto.len()`. En su lugar, invoca `mi_objeto.__len__()`.

> **Citación:** La documentación oficial de Python lo describe así: "El modelo de datos de Python [...] es una descripción de Python como un framework. Formaliza las interfaces de los bloques de construcción del lenguaje mismo" [^1].

**Ejemplo Práctico:** Creemos una baraja de cartas que se comporte como una secuencia.

```python
import collections

Card = collections.namedtuple('Card', ['rank', 'suit'])

class FrenchDeck:
    ranks = [str(n) for n in range(2, 11)] + list('JQKA')
    suits = 'spades diamonds clubs hearts'.split()

    def __init__(self):
        self._cards = [Card(rank, suit) for suit in self.suits
                                        for rank in self.ranks]

    # Al implementar __len__, podemos usar la función len()
    def __len__(self):
        return len(self._cards)

    # Al implementar __getitem__, obtenemos indexación, slicing,
    # y la capacidad de iterar sobre el objeto.
    def __getitem__(self, position):
        return self._cards[position]

deck = FrenchDeck()

# Gracias a __len__
print(f"Tamaño de la baraja: {len(deck)}")

# Gracias a __getitem__
print(f"Primera carta: {deck[0]}")
print(f"Última carta: {deck[-1]}")

# ¡Incluso podemos obtener una carta al azar!
from random import choice
print(f"Carta al azar: {choice(deck)}")

# Y slicing
print(f"Primeras 3 cartas: {deck[:3]}")

# Y la iteración funciona "gratis"
for card in deck:
    # ... (hará print de las 52 cartas)
    pass
```

**Nivel Senior:** Entender esto significa que sabes que para que tu objeto sea "ordenable", debes implementar `__lt__`, `__eq__`, etc. (o usar `functools.total_ordering`). Para que funcione con el operador `+`, implementas `__add__`. No estás limitado por el lenguaje; lo extiendes.

> **Lectura Obligada:** El libro "Fluent Python" de Luciano Ramalho dedica sus primeros capítulos a este concepto, considerándolo la característica más importante del lenguaje [^2].

### 2. Funciones como Objetos de Primera Clase: Decoradores y Closures

En Python, las funciones son objetos como cualquier otro. Puedes asignarlas a variables, pasarlas como argumentos y devolverlas desde otras funciones.

**Concepto Clave:**
*   **Higher-Order Functions:** Funciones que toman otras funciones como argumentos o las devuelven. `map()`, `filter()`, `sorted(key=...)` son ejemplos.
*   **Closures:** Una función que recuerda el entorno en el que fue creada. Específicamente, recuerda las variables de un ámbito superior incluso después de que ese ámbito haya dejado de existir.
*   **Decoradores:** Azúcar sintáctico para una higher-order function que toma una función y devuelve otra (generalmente extendiendo la original). `@my_decorator` es equivalente a `my_func = my_decorator(my_func)`.

> **Citación:** La propuesta original de los decoradores, PEP 318, los describe como una forma de transformar una función o método [^3].

**Ejemplo Práctico (Decorador con Closure):**

```python
import time
import functools

def timer(func):
    """Un decorador que imprime el tiempo de ejecución de una función."""
    @functools.wraps(func)  # Preserva el nombre y docstring de la función original
    def wrapper_timer(*args, **kwargs):
        start_time = time.perf_counter()
        value = func(*args, **kwargs) # Llama a la función original
        end_time = time.perf_counter()
        run_time = end_time - start_time
        print(f"Terminó {func.__name__!r} en {run_time:.4f} segundos")
        return value
    return wrapper_timer

@timer
def waste_some_time(num_times):
    """Una función que simplemente pierde el tiempo."""
    for _ in range(num_times):
        sum([i**2 for i in range(1000)])

waste_some_time(1)
waste_some_time(100)

print(waste_some_time.__name__) # Imprime 'waste_some_time' gracias a @functools.wraps
```

**Nivel Senior:** Entender los closures es crucial para entender por qué los decoradores con estado funcionan. Saber usar `functools.wraps` es una señal de profesionalismo para no romper la introspección. Además, un senior sabe crear decoradores que aceptan argumentos, lo que implica una capa extra de anidación de funciones.

### 3. Iteradores, Generadores y el Protocolo de Iteración

La eficiencia en el manejo de datos es una marca de un desarrollador senior. Los generadores son la herramienta principal para esto.

**Concepto Clave:**
*   **Iterable:** Cualquier objeto del que se puede obtener un iterador. Implementa `__iter__()`. Listas, tuplas, strings son iterables.
*   **Iterador:** Un objeto que produce el siguiente valor de una secuencia. Implementa `__next__()` (que lanza `StopIteration` al final) y `__iter__()` (que se devuelve a sí mismo).
*   **Generador:** Una forma sencilla de crear iteradores. Es una función que usa la palabra clave `yield`. Cuando `yield` es llamado, la función se "pausa" y devuelve un valor. Su estado se guarda para la próxima llamada a `next()`.

> **Citación:** PEP 255 introdujo los generadores simples, describiéndolos como una forma de "simplificar la creación de iteradores" [^4].

**Ejemplo Práctico:**

```python
# Malo: Ineficiente en memoria para archivos grandes
def csv_reader_list(filename):
    lines = []
    with open(filename) as f:
        for line in f:
            lines.append(line)
    return lines

# Bueno: Eficiente en memoria, procesa línea por línea
def csv_reader_generator(filename):
    with open(filename) as f:
        for line in f:
            yield line # Pausa y entrega la línea, sin almacenar todo en memoria

# Aún más Pythónico: Generator Expression
# (similar a una list comprehension, pero con paréntesis)
log_lines = (line for line in open('access.log'))
# 'log_lines' es un generador, no consume memoria hasta que se itera sobre él.
# Por ejemplo, para encontrar la primera línea con un error:
first_error = next((line for line in log_lines if 'ERROR' in line), None)
```

**Nivel Senior:** Sabes cuándo usar una list comprehension (si necesitas todos los datos en memoria para accesos múltiples) vs. un generator expression (para procesar grandes volúmenes de datos de forma secuencial y con bajo consumo de memoria). Entiendes el poder de `yield from` para encadenar generadores.

### 4. Gestión de Contexto y la Sentencia `with`

Un código robusto gestiona los recursos correctamente (archivos, conexiones de red, locks). La sentencia `with` es la forma idiomática de hacerlo.

**Concepto Clave:** El protocolo de gestión de contexto se basa en dos métodos:
*   `__enter__(self)`: Se ejecuta al entrar en el bloque `with`. Su valor de retorno se asigna a la variable después de `as` (si existe).
*   `__exit__(self, exc_type, exc_value, traceback)`: Se ejecuta al salir del bloque, ya sea de forma normal o por una excepción. Si hubo una excepción, los argumentos contendrán la información. Si devuelve `True`, la excepción se suprime.

> **Citación:** PEP 343 introdujo la sentencia `with`, justificándola como una forma de "factorizar el código de `try/finally`" para la gestión de recursos [^5].

**Ejemplo Práctico:**

```python
# Forma tradicional (verbosa y fácil de olvidar el 'finally')
f = open('my_file.txt', 'w')
try:
    f.write('hello')
finally:
    f.close()

# Forma Pythónica con 'with'
with open('my_file.txt', 'w') as f:
    f.write('hello')
# f.close() se llama automáticamente al salir del bloque, incluso si hay un error.

# Creando tu propio context manager con el decorador @contextmanager
from contextlib import contextmanager
import time

@contextmanager
def timer_context():
    """Un context manager para medir el tiempo de un bloque de código."""
    start_time = time.perf_counter()
    try:
        yield # El control se cede al bloque 'with' aquí
    finally:
        end_time = time.perf_counter()
        run_time = end_time - start_time
        print(f"El bloque tardó {run_time:.4f} segundos")

with timer_context():
    # Código que queremos medir
    time.sleep(0.5)
```

**Nivel Senior:** No solo usas `with` para archivos, sino que lo reconoces como un patrón para cualquier par de acciones `setup/teardown`. Lo usas para transacciones de base de datos, locks de concurrencia, etc. Sabes crear tus propios context managers usando clases o, más comúnmente, el decorador `contextlib.contextmanager`.

### 5. Metaprogramación: Clases Dinámicas y Metaclases

La metaprogramación es escribir código que manipula código. Es un tema avanzado, pero entenderlo te da un poder inmenso.

**Concepto Clave:**
*   En Python, las clases son objetos. Son instancias de su *metaclase*.
*   La metaclase por defecto es `type`.
*   `type` no solo te da el tipo de un objeto (`type(5)`), sino que también puede crear clases dinámicamente: `MyClass = type('MyClass', (BaseClass,), {'attr': 100})`.
*   Una **metaclase** es una clase cuya instancia es una clase. Te permite interceptar la creación de una clase para modificarla.

**¿Cuándo se usa?**
*   **ORMs (Object-Relational Mappers):** Como los de Django o SQLAlchemy. Definen un modelo como una clase simple, y la metaclase la convierte en un mapeo a una tabla de base de datos, añadiendo campos y métodos automáticamente.
*   **APIs / Registros:** Para registrar automáticamente clases en un sistema (e.g., plugins, serializadores).

**Ejemplo Práctico (Metaclase simple para registro de plugins):**

```python
# Un registro global para nuestros plugins
PLUGIN_REGISTRY = {}

class PluginMeta(type):
    def __new__(cls, name, bases, attrs):
        # Crea la nueva clase como lo haría 'type' normalmente
        new_class = super().__new__(cls, name, bases, attrs)
        
        # Si la clase tiene un atributo 'plugin_name', la registramos
        if 'plugin_name' in attrs:
            PLUGIN_REGISTRY[attrs['plugin_name']] = new_class
            
        return new_class

# Todas las clases que usen PluginMeta como su metaclase pasarán por el __new__ anterior
class BasePlugin(metaclass=PluginMeta):
    pass

# Este plugin se registrará automáticamente
class MyAwesomePlugin(BasePlugin):
    plugin_name = 'awesome'
    def execute(self):
        print("Executing awesome plugin!")

# Este no se registrará porque no tiene 'plugin_name'
class AnotherClass(BasePlugin):
    pass

print(PLUGIN_REGISTRY)
# >> {'awesome': <class '__main__.MyAwesomePlugin'>}

# Podemos instanciarlo desde el registro
plugin_instance = PLUGIN_REGISTRY['awesome']()
plugin_instance.execute()
```

**Nivel Senior:** Sabes que el 99% de las veces no necesitas una metaclase. A menudo, un decorador de clase o una función de fábrica es una solución más simple. Pero entiendes cuándo una metaclase es la herramienta correcta y cómo funciona el proceso de creación de clases (`__new__` vs `__init__` en metaclases).

### 6. Concurrencia y Paralelismo: El GIL y Cómo Superarlo

Este es un tema crítico para aplicaciones de alto rendimiento.

**Concepto Clave: El GIL (Global Interpreter Lock)**
El GIL es un mutex que protege el acceso a los objetos de Python, impidiendo que múltiples hilos ejecuten bytecode de Python *al mismo tiempo* dentro del mismo proceso.

> **Citación:** David Beazley, un experto en concurrencia en Python, explica que el GIL "simplifica la implementación de CPython y facilita la escritura de extensiones en C" [^6].

**Implicaciones:**
*   **`threading`:** Es ideal para tareas **I/O-bound** (limitadas por entrada/salida, como peticiones de red, acceso a disco). Mientras un hilo espera por la red, el GIL se libera y otro hilo puede ejecutar código Python. No ofrece paralelismo real para código CPU-bound.
*   **`multiprocessing`:** Es la solución para tareas **CPU-bound** (limitadas por el procesador, como cálculos matemáticos intensos). Crea procesos separados, cada uno con su propio intérprete de Python y su propio GIL. La comunicación entre procesos (IPC) tiene un coste (overhead).
*   **`asyncio`:** Es un framework para escribir código concurrente de un solo hilo usando corrutinas (event loop). Es perfecto para un número masivo de conexiones I/O (e.g., un servidor web con miles de clientes). Es **concurrencia cooperativa**, no preemptiva.

**Nivel Senior:**
*   Diagnosticas correctamente si un problema es I/O-bound o CPU-bound.
*   Eliges la herramienta adecuada: `threading` para I/O simple, `asyncio` para I/O a gran escala, `multiprocessing` para CPU.
*   Entiendes los peligros de las condiciones de carrera (race conditions) y usas primitivas de sincronización (`Lock`, `Queue`, `Semaphore`) cuando es necesario.
*   Conoces `concurrent.futures` como una abstracción de alto nivel sobre `threading` y `multiprocessing`.

```python
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests

URLS = ['http://www.google.com', 'http://www.python.org', 'http://www.facebook.com']

# Usando ThreadPoolExecutor para tareas I/O-bound
def fetch(url):
    try:
        response = requests.get(url, timeout=5)
        return url, len(response.content)
    except requests.RequestException as e:
        return url, str(e)

with ThreadPoolExecutor(max_workers=3) as executor:
    futures = [executor.submit(fetch, url) for url in URLS]
    for future in as_completed(futures):
        url, result = future.result()
        print(f"URL: {url}, Resultado: {result}")
```

### 7. CPython Internals: Un Vistazo Bajo el Capó

Un senior no trata al intérprete como una caja negra.

**Concepto Clave:**
*   **De Código a Ejecución:** Tu código `.py` se compila a **bytecode**. Este bytecode es lo que ejecuta la Máquina Virtual de Python (PVM). Puedes inspeccionar el bytecode con el módulo `dis`.
*   **Gestión de Memoria:** CPython usa principalmente el **conteo de referencias (reference counting)**. Cada objeto tiene un contador. Cuando llega a cero, el objeto se libera.
*   **Garbage Collector (GC):** El conteo de referencias no puede manejar **ciclos de referencias** (e.g., `a.ref = b` y `b.ref = a`). Para esto, Python tiene un colector de basura generacional que periódicamente busca y rompe estos ciclos. Puedes interactuar con él a través del módulo `gc`.
*   **Implementación de Tipos de Datos:** Entender por qué un `dict` tiene búsquedas O(1) (es una tabla hash) o por qué añadir a un `list` es O(1) amortizado (es un array dinámico que se redimensiona) te ayuda a escribir código más eficiente.

> **Citación:** Raymond Hettinger, un core developer de Python, tiene charlas famosas donde explica cómo están implementadas las estructuras de datos de Python para ser "super-poderosas" [^7].

**Ejemplo Práctico (Inspeccionando Bytecode):**

```python
import dis

def add(a, b):
    return a + b

dis.dis(add)
```
Salida:
```
  4           0 LOAD_FAST                0 (a)
              2 LOAD_FAST                1 (b)
              4 BINARY_ADD
              6 RETURN_VALUE
```
Esto te muestra exactamente las instrucciones que la PVM ejecuta. `BINARY_ADD` es la operación que llama a `a.__add__(b)`.

**Nivel Senior:** Sabes usar el `dis` module para entender cuellos de botella. Entiendes las implicaciones de la gestión de memoria (e.g., por qué crear y destruir muchos objetos pequeños en un bucle puede ser lento). Sabes que el rendimiento de tus estructuras de datos no es magia.

### 8. Ecosistema y Herramientas del Programador Senior

El conocimiento del lenguaje debe ir acompañado de un dominio de las herramientas profesionales.

*   **Testing:** Dominio de `pytest`. No solo escribes tests, sino que usas fixtures, mocks (`unittest.mock`), y parametrización para escribir tests limpios y mantenibles.
*   **Typing (Tipado Estático):** Uso extensivo de type hints (PEP 484). Usas `mypy` en tu CI/CD para detectar errores antes de que lleguen a producción. Esto es crucial para la mantenibilidad de grandes bases de código.
*   **Packaging:** Entiendes `pyproject.toml` (PEP 518) y herramientas modernas como `Poetry` o `PDM` para gestionar dependencias, construir y publicar paquetes.
*   **Linting y Formateo:** El código no solo debe funcionar, debe ser legible. Usas `black` para un formato consistente, `isort` para los imports, y `flake8` o `ruff` para detectar errores de estilo y lógicos.
*   **Profiling:** Cuando el rendimiento es un problema, no adivinas. Usas `cProfile` para encontrar cuellos de botella y herramientas como `line_profiler` o `memory-profiler` para un análisis más detallado.

### 9. Recursos Imprescindibles

*   **Libros:**
    *   **"Fluent Python, 2nd Edition"** - Luciano Ramalho. Es la biblia sobre cómo usar Python de forma idiomática y profunda.
    *   **"Python Cookbook, 3rd Edition"** - David Beazley & Brian K. Jones. Recetas prácticas para problemas avanzados.
*   **Charlas (Talks):**
    *   Cualquier charla de **Raymond Hettinger**. Búscalo en YouTube. Especialmente "Transforming Code into Beautiful, Idiomatic Python" y "Python's Class Development Toolkit".
    *   Cualquier charla de **David Beazley**. Especialmente sus tutoriales sobre generadores y concurrencia.
*   **Documentación:**
    *   La **documentación oficial de Python**. Un senior la consulta constantemente.
    *   Los **Python Enhancement Proposals (PEPs)**. Leer los PEPs clave (como los citados aquí) te da el contexto histórico y técnico de las características del lenguaje.

---

Convertirse en senior es un viaje continuo. Implica curiosidad, práctica deliberada y la humildad de saber que siempre hay más por aprender. ¡Buena suerte en tu camino!

---

### Referencias

[^1]: The Python Language Reference, "[3. Data model](https://docs.python.org/3/reference/datamodel.html)".
[^2]: Ramalho, L. (2022). *Fluent Python: Clear, Concise, and Effective Programming* (2nd ed.). O'Reilly Media.
[^3]: van Rossum, G., & Warsaw, B. (2003). "[PEP 318 -- Decorators for Functions and Methods](https://peps.python.org/pep-0318/)".
[^4]: van Rossum, G. (2001). "[PEP 255 -- Simple Generators](https://peps.python.org/pep-0255/)".
[^5]: van Rossum, G., & Ewing, P. (2005). "[PEP 343 -- The "with" Statement](https://peps.python.org/pep-0343/)".
[^6]: Beazley, D. (2010). "[Understanding the Python GIL](http://www.dabeaz.com/python/UnderstandingGIL.pdf)" (Slides de PyCon 2010).
[^7]: Hettinger, R. (2013). "[Modern Python Dictionaries, A confluence of great ideas](https://www.youtube.com/watch?v=p33CVV29OG8)" (PyCon 2017 Talk).
