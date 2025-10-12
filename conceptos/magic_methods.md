# Magic Methods

Claro que sí. Prepárate para una inmersión profunda en el corazón de Python. Entender los métodos mágicos no es solo aprender una lista de funciones; es comprender la filosofía de diseño del lenguaje. Esto es lo que separa a un programador que *usa* Python de uno que lo *habla* con fluidez.

---

# Dominando los Métodos Mágicos en Python: Una Guía Profunda para el Desarrollador Senior

## ¿Qué son los Métodos Mágicos?

Los "Métodos Mágicos" (o "Métodos Especiales") son el mecanismo que permite que tus propios objetos se integren con el comportamiento fundamental del lenguaje Python. Se reconocen por sus nombres, que empiezan y terminan con doble guion bajo (por ejemplo, `__init__`, `__len__`). En la comunidad, se les conoce como **"dunder methods"** (de "double underscore").

No son "mágicos" en el sentido de que hagan algo misterioso. Son "mágicos" porque raramente los llamas directamente. En su lugar, el intérprete de Python los invoca por ti en respuesta a ciertas sintaxis u operaciones. Por ejemplo, cuando escribes `len(mi_objeto)`, Python en realidad está buscando y llamando a `mi_objeto.__len__()`.

La base de todo esto es el **Modelo de Datos de Python** (Python Data Model).

> **Citación Clave:** "El Modelo de Datos de Python es una descripción de la API que puedes usar para hacer que tus propios objetos se comporten como los tipos incorporados." — *Luciano Ramalho, "Fluent Python"*

Entender este modelo es el paso más crucial para pasar de un nivel intermedio a senior en Python. Te permite escribir código que es idiomático, expresivo y eficiente, aprovechando al máximo las características del lenguaje.

## Categorías Fundamentales de Métodos Mágicos

Agruparemos los métodos por la funcionalidad que implementan. Esto refleja la idea de **protocolos**: un objeto es un "contenedor" no porque herede de una clase `Container`, sino porque implementa los métodos del protocolo de contenedor (`__len__`, `__getitem__`, etc.).

### 1. Creación, Inicialización y Destrucción de Objetos

Estos métodos controlan el ciclo de vida de un objeto.

-   `__new__(cls, *args, **kwargs)`
    -   **Propósito:** Es el primer método llamado en la creación de una instancia. Es el verdadero **constructor**. Su trabajo es crear y devolver una nueva instancia de la clase (`cls`).
    -   **Cuándo se usa:** Rara vez. Es útil para subclases de tipos inmutables (como `str`, `int`, `tuple`) o para implementar patrones de diseño como Singleton o Metaclases.
    -   **Nota de Senior:** `__new__` es un método de clase estático (aunque no necesites decorarlo con `@staticmethod`). El primer argumento que recibe es la propia clase, no la instancia.

-   `__init__(self, *args, **kwargs)`
    -   **Propósito:** Es el **inicializador**. Su trabajo es configurar el estado de una instancia *ya creada* por `__new__`. No devuelve nada.
    -   **Cuándo se usa:** Casi siempre. Es donde asignas los atributos iniciales al objeto (`self.atributo = valor`).

-   `__del__(self)`
    -   **Propósito:** Es el **finalizador** o **destructor**. Se llama justo antes de que el objeto sea destruido por el recolector de basura (Garbage Collector).
    -   **Cuándo se usa:** Con mucha precaución. No hay garantía de *cuándo* o *si* se llamará (por ejemplo, si el programa termina abruptamente). Es frágil y propenso a errores. Para la gestión de recursos (archivos, conexiones de red), siempre prefiere los **Context Managers** (`with` statement).
    -   **Nota de Senior:** Evita `__del__` a menos que sea absolutamente necesario para liberar recursos externos que Python no gestiona.

```python
class ControlledLifecycle:
    def __new__(cls, *args, **kwargs):
        print("1. Creando la instancia con __new__")
        instance = super().__new__(cls)
        return instance

    def __init__(self, value):
        print("2. Inicializando la instancia con __init__")
        self.value = value

    def __del__(self):
        # ¡Cuidado con este método!
        print(f"3. Destruyendo la instancia con valor: {self.value}")

# El flujo es: __new__ -> __init__
obj = ControlledLifecycle(10) 
# La llamada a __del__ es indeterminada, pero ocurrirá cuando 'obj' salga del alcance.
```

### 2. Representación de Objetos

¿Cómo se "ve" tu objeto? Estos métodos definen su representación en texto.

-   `__str__(self)`
    -   **Propósito:** Devuelve una representación "informal" o "amigable para el usuario" del objeto. Es lo que se invoca con `str(obj)` y `print(obj)`.
    -   **Objetivo:** Ser legible.

-   `__repr__(self)`
    -   **Propósito:** Devuelve una representación "oficial" o "inequívoca" del objeto. Es lo que se invoca en la consola interactiva cuando escribes el nombre del objeto y presionas Enter.
    -   **Objetivo:** Ser informativo y, si es posible, ser un fragmento de código Python válido que pueda recrear el objeto. `eval(repr(obj)) == obj` es el ideal.
    -   **Nota de Senior:** Si solo puedes implementar uno, implementa `__repr__`. Si `__str__` no está definido, Python usará `__repr__` en su lugar. Un buen `__repr__` es una de las herramientas de depuración más potentes que existen.

> **Citación (PEP 3140):** "Para cualquier objeto, `repr(x)` debe devolver una cadena que, cuando se pasa a `eval()`, produce un objeto con el mismo valor." (Aunque esto no siempre es práctico, es el principio rector).

```python
import datetime

class Evento:
    def __init__(self, nombre, fecha):
        self.nombre = nombre
        self.fecha = fecha

    def __str__(self):
        # Para el usuario final
        return f"Evento '{self.nombre}' el {self.fecha.strftime('%d-%m-%Y')}"

    def __repr__(self):
        # Para el desarrollador, inequívoco
        return f"Evento(nombre='{self.nombre}', fecha=datetime.date({self.fecha.year}, {self.fecha.month}, {self.fecha.day}))"

hoy = datetime.date.today()
evento = Evento("Lanzamiento Python 4.0", hoy)

print(str(evento))  # Llama a __str__ -> Evento 'Lanzamiento Python 4.0' el 24-05-2024
print(repr(evento)) # Llama a __repr__ -> Evento(nombre='Lanzamiento Python 4.0', fecha=datetime.date(2024, 5, 24))
```

### 3. Emulación de Tipos Numéricos y Operadores

Esto permite que tus objetos usen operadores como `+`, `-`, `*`, `==`, `<`.

-   **Operadores Binarios:** `__add__`, `__sub__`, `__mul__`, `__truediv__`, `__floordiv__`, `__mod__`, `__pow__`.
-   **Operadores de Comparación:** `__eq__` (==), `__ne__` (!=), `__lt__` (<), `__le__` (<=), `__gt__` (>), `__ge__` (>=).
-   **Operadores Reflejados (Right-hand):** `__radd__`, `__rsub__`, etc. Se llaman cuando tu objeto está a la *derecha* de la operación y el objeto de la izquierda no sabe cómo manejarla. Ejemplo: `3 + mi_objeto` llamará a `mi_objeto.__radd__(3)`.
-   **Operadores de Asignación Aumentada (In-place):** `__iadd__`, `__isub__`, etc. Para operadores como `+=`, `-=`. Si es posible, deben modificar el objeto en el lugar (`self`) y devolverlo.

**Nota de Senior:** En los operadores de comparación y binarios, si no puedes realizar la operación con el otro tipo, debes devolver el singleton `NotImplemented`. Python entonces intentará la operación reflejada en el otro operando.

```python
import functools

@functools.total_ordering # ¡Un decorador muy útil!
class Vector2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Vector2D({self.x}, {self.y})"

    def __add__(self, other):
        if isinstance(other, Vector2D):
            return Vector2D(self.x + other.x, self.y + other.y)
        return NotImplemented

    def __mul__(self, scalar):
        if isinstance(scalar, (int, float)):
            return Vector2D(self.x * scalar, self.y * scalar)
        return NotImplemented
    
    # La versión reflejada para '3 * v1'
    def __rmul__(self, scalar):
        return self.__mul__(scalar)

    def __eq__(self, other):
        if not isinstance(other, Vector2D):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    # Solo necesitamos __eq__ y uno de los otros (__lt__, __gt__, etc.)
    # y @total_ordering hará el resto.
    def __lt__(self, other):
        if not isinstance(other, Vector2D):
            return NotImplemented
        return (self.x**2 + self.y**2) < (other.x**2 + other.y**2)

v1 = Vector2D(2, 3)
v2 = Vector2D(5, 1)

print(v1 + v2)  # Llama a v1.__add__(v2) -> Vector2D(7, 4)
print(v1 * 3)   # Llama a v1.__mul__(3) -> Vector2D(6, 9)
print(3 * v1)   # Llama a v1.__rmul__(3) -> Vector2D(6, 9)
print(v1 > v2)  # Inferido por @total_ordering a partir de __lt__ y __eq__ -> False
```

### 4. Emulación de Contenedores

Haz que tus objetos se comporten como listas, diccionarios o conjuntos.

-   `__len__(self)`: Implementa `len(obj)`. Debe devolver un entero.
-   `__getitem__(self, key)`: Implementa el acceso por índice o clave: `obj[key]`.
-   `__setitem__(self, key, value)`: Implementa la asignación por índice o clave: `obj[key] = value`.
-   `__delitem__(self, key)`: Implementa la eliminación por índice o clave: `del obj[key]`.
-   `__iter__(self)`: Devuelve un iterador para el contenedor. Es la base de los bucles `for`.
-   `__contains__(self, item)`: Implementa el operador `in`. `item in obj`. Si no se define, Python itera sobre el objeto para buscar el elemento.

**Nota de Senior:** Implementar `__getitem__` hace que un objeto sea iterable automáticamente (aunque es más eficiente implementar también `__iter__`). Esta es la esencia del "Duck Typing".

> **Citación (Alex Martelli):** "No compruebes si es un pato, comprueba si grazna (`__quack__`), etc. Es más preciso decir 'Comprueba si tiene los métodos que necesitas'." Esto se conoce como EAFP (Easier to Ask for Forgiveness than Permission) vs LBYL (Look Before You Leap).

```python
class Baraja:
    palos = 'picas diamantes corazones tréboles'.split()
    valores = [str(n) for n in range(2, 11)] + list('JQKA')

    def __init__(self):
        self._cartas = [f'{valor} de {palo}' for palo in self.palos for valor in self.valores]

    def __len__(self):
        return len(self._cartas)

    def __getitem__(self, position):
        return self._cartas[position]

mazo = Baraja()
print(f"La baraja tiene {len(mazo)} cartas.") # Llama a __len__
print(f"La primera carta es: {mazo[0]}")     # Llama a __getitem__
print(f"La última carta es: {mazo[-1]}")    # Llama a __getitem__

# ¡Es iterable gracias a __getitem__!
for carta in mazo[:5]:
    print(carta)

# ¡Y también soporta 'in' de forma optimizada si implementamos __contains__!
print('As de picas' in mazo) # True
```

### 5. Gestión de Atributos

Controla el acceso, la asignación y la eliminación de atributos. Son herramientas muy potentes, pero también peligrosas si se usan incorrectamente.

-   `__getattr__(self, name)`
    -   Se llama **solo** cuando se intenta acceder a un atributo que **no existe** en la instancia.
    -   Ideal para proxies, APIs dinámicas o para evitar `AttributeError`.

-   `__getattribute__(self, name)`
    -   Se llama **siempre** que se intenta acceder a un atributo, exista o no.
    -   **Peligro:** Es muy fácil crear una recursión infinita. Por ejemplo, `self.name` dentro de `__getattribute__` volverá a llamar a `__getattribute__`. Debes usar `super().__getattribute__(name)` para acceder a los atributos.
    -   **Nota de Senior:** Usa `__getattr__` a menos que necesites interceptar *todos* los accesos a atributos, lo cual es raro y complejo.

-   `__setattr__(self, name, value)`
    -   Se llama siempre que se intenta asignar un valor a un atributo (`obj.name = value`).
    -   También es propenso a la recursión infinita. Usa `super().__setattr__(name, value)`.

-   `__delattr__(self, name)`
    -   Se llama siempre que se usa `del obj.name`.

```python
class LoggerProxy:
    def __init__(self, target):
        # Usamos super() para evitar la recursión infinita en __setattr__
        super().__setattr__('_target', target)

    def __getattribute__(self, name):
        target = super().__getattribute__('_target')
        print(f"Accediendo al atributo '{name}'")
        return getattr(target, name)

    def __setattr__(self, name, value):
        target = super().__getattribute__('_target')
        print(f"Asignando '{value}' al atributo '{name}'")
        setattr(target, name, value)

class MiClase:
    def __init__(self):
        self.a = 1
        self.b = 2

obj = MiClase()
proxy = LoggerProxy(obj)

proxy.a # Imprime "Accediendo al atributo 'a'"
proxy.c = 10 # Imprime "Asignando '10' al atributo 'c'"
```

### 6. Context Managers (`with` statement)

Permiten una gestión de recursos limpia y segura (archivos, locks, conexiones a bases de datos).

-   `__enter__(self)`
    -   Se llama al entrar en el bloque `with`. El valor que devuelve se asigna a la variable después de `as` (si existe).
-   `__exit__(self, exc_type, exc_value, traceback)`
    -   Se llama al salir del bloque `with`, ya sea de forma normal o por una excepción.
    -   Si no hubo excepción, los tres últimos argumentos son `None`.
    -   Si hubo una excepción, contienen la información de la misma. Si `__exit__` devuelve `True`, la excepción se suprime. Si devuelve `False` o `None`, la excepción se propaga.

> **Citación (PEP 343):** "Esta PEP añade una nueva declaración 'with' para simplificar la implementación del patrón `try/finally` para la gestión de recursos."

```python
import time

class Temporizador:
    def __enter__(self):
        self.inicio = time.perf_counter()
        return self # Devolvemos el objeto para poder interactuar con él

    def __exit__(self, exc_type, exc_value, traceback):
        self.fin = time.perf_counter()
        duracion = self.fin - self.inicio
        print(f"El bloque tardó {duracion:.4f} segundos.")
        # No suprimimos excepciones, devolvemos None implícitamente

with Temporizador():
    # Código cuyo tiempo queremos medir
    time.sleep(1)
```

### 7. Tipos Invocables (Callables)

-   `__call__(self, *args, **kwargs)`
    -   Permite que una instancia de tu clase sea "llamada" como si fuera una función.

```python
class Acumulador:
    def __init__(self):
        self._contador = 0

    def __call__(self, valor):
        self._contador += valor
        print(f"Contador actual: {self._contador}")
        return self._contador

acum = Acumulador()
acum(5)  # Llama a acum.__call__(5) -> Contador actual: 5
acum(10) # Llama a acum.__call__(10) -> Contador actual: 15
```

### 8. Métodos Asíncronos (Avanzado)

Para la programación con `async`/`await`.

-   `__await__(self)`: Permite que un objeto sea usado en una expresión `await`. Debe devolver un iterador.
-   `__aenter__(self)`, `__aexit__(self, ...)`: Versiones asíncronas de los context managers, para usar con `async with`.
-   `__aiter__(self)`, `__anext__(self)`: Versiones asíncronas para iteradores, para usar con `async for`.

## Conclusión: De la Sintaxis a la Filosofía

Un desarrollador senior no solo memoriza los nombres de los métodos mágicos. Entiende que son los puntos de enganche (hooks) que le permiten enseñar a Python a hablar el lenguaje de su dominio de problema.

-   **Piensa en Protocolos, no en Herencia:** ¿Quieres que tu objeto sea "ordenable"? No necesitas heredar de `Ordenable`, solo implementa `__lt__` y `__eq__`. Esta es la esencia del "Pythonic way".
-   **Escribe APIs Fluidas:** Al implementar `__add__` para un objeto `Vector`, permites que el usuario escriba `v1 + v2` en lugar de `v1.sumar(v2)`. El primer caso es más legible, intuitivo y se integra con el resto del ecosistema (por ejemplo, `sum([v1, v2, v3])` funcionará si `__add__` está bien implementado).
-   **La Depuración es Clave:** Un `__repr__` bien implementado te ahorrará horas de depuración. Es una de las marcas de un programador experimentado.

Al dominar el Modelo de Datos de Python, dejas de ser un simple usuario del lenguaje y te conviertes en un arquitecto capaz de extenderlo para crear código elegante, expresivo y robusto.

### Referencias y Lecturas Adicionales

1.  **Documentación Oficial de Python: The Data Model:** La fuente canónica. [https://docs.python.org/3/reference/datamodel.html](https://docs.python.org/3/reference/datamodel.html)
2.  **"Fluent Python" por Luciano Ramalho:** Considerado por muchos como la biblia sobre este tema. Los primeros 10 capítulos son una clase magistral sobre el modelo de datos.
3.  **"A Guide to Python's Magic Methods" por Rafe Kettler:** Un excelente tutorial online que cubre muchos de los métodos.
4.  **PEP 8 -- Style Guide for Python Code:** Aunque no trata directamente sobre métodos mágicos, seguirlo es una señal de senioridad. [https://www.python.org/dev/peps/pep-0008/](https://www.python.org/dev/peps/pep-0008/)
