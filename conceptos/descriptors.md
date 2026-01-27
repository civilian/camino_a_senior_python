# Descriptors

¡Absolutamente! Prepárate para un viaje profundo al corazón del modelo de objetos de Python. No vamos a arañar la superficie; vamos a descender a las catacumbas donde residen los mecanismos que dan a Python su elegancia y poder. Abróchate el cinturón.

***

# El Protocolo del Centinela: Una Guía Senior sobre Descriptores en Python

Bienvenido, colega artesano del código. Has escrito clases, has usado decoradores, y probablemente has tecleado `@property` más veces de las que puedes contar. Sientes que entiendes el modelo de objetos de Python. Pero hay una capa más profunda, un mecanismo subyacente que unifica propiedades, métodos, métodos estáticos y de clase en un solo concepto elegante. Este es el **protocolo de descriptor**.

Dominar los descriptores es como pasar de ser un músico que puede tocar una melodía a ser un compositor que entiende la teoría musical detrás de ella. Te permite no solo usar el lenguaje, sino extenderlo, creando APIs que son a la vez potentes, intuitivas y robustas. Esta guía es tu partitura.

## 1. Introducción Profunda: El Nacimiento de la Unificación

Para entender los descriptores, debemos viajar en el tiempo a los albores del nuevo milenio. Python estaba en una encrucijada.

### Contexto Histórico: El Caos Antes del Cosmos

A finales de los 90 y principios de los 2000, Python tenía una dualidad extraña: "clases clásicas" (old-style) y "tipos" (built-ins como `int`, `list`, `dict`). No se comportaban igual. Intentar heredar de `list` era una aventura llena de peligros y comportamientos inesperados. Esta esquizofrenia era un obstáculo para el crecimiento del lenguaje.

El problema fue abordado por Guido van Rossum y la comunidad de desarrolladores de Python en un esfuerzo monumental que culminó en **Python 2.2** (lanzado en 2001). El objetivo era unificar tipos y clases en una sola jerarquía. Este proyecto, conocido como "new-style classes", necesitaba un mecanismo fundamental para gobernar cómo se accedía a los atributos.

> "El objetivo del proyecto de unificación de tipos/clases es reducir la duplicación de esfuerzo entre los implementadores de tipos y los autores de clases, y aumentar la uniformidad del lenguaje para los usuarios." — **Guido van Rossum**, *PEP 252: Making Types Look More Like Classes* (2001)

### El Problema que Resuelve: La Tiranía del Punto

En casi todos los lenguajes orientados a objetos, el operador punto (`.`) parece simple: `objeto.atributo`. Pero, ¿qué sucede realmente detrás de escena? ¿Cómo funciona `objeto.metodo()`? ¿O `MiClase.metodo_estatico()`?

Antes de los descriptores, la lógica para estos accesos estaba dispersa y codificada en el intérprete de CPython. Era un conjunto de reglas especiales. Las propiedades se implementaban con una función `property()` que se sentía como un añadido mágico. Los métodos eran otro caso especial. No había un principio unificador.

Los descriptores resolvieron este problema al definir un **protocolo común**. Proporcionaron una forma de que un objeto (el descriptor) pudiera "engancharse" al proceso de acceso a atributos de otro objeto (el propietario), interceptando las operaciones de obtención (`get`), establecimiento (`set`) y eliminación (`delete`).

### Evolución: De un Hack a una Piedra Angular

1.  **Python 2.2 (2001):** Nacen los descriptores como parte de las "new-style classes". Son la maquinaria oculta que hace que `@property`, `@staticmethod` y `@classmethod` funcionen. Inicialmente, eran vistos como un detalle de implementación avanzado.
2.  **Python 2.6 / 3.0 (2008):** La comunidad empieza a reconocer su poder para crear APIs más limpias, especialmente en frameworks como Django, donde los campos de modelo (`models.CharField`) son, en esencia, descriptores.
3.  **Python 3.6 (2016):** Se introduce el método `__set_name__` (PEP 487). Este fue un cambio revolucionario. Antes, un descriptor no sabía a qué atributo de la clase propietaria estaba asignado. Esto requería hacks o pasar el nombre del atributo explícitamente. `__set_name__` resolvió este problema de forma elegante, haciendo los descriptores mucho más reutilizables y potentes.

Hoy, los descriptores no son solo una curiosidad. Son el fundamento del modelo de atributos de Python y una herramienta indispensable para cualquier desarrollador senior que construya frameworks, ORMs, o sistemas de validación complejos.

## 2. Fundamentos Teóricos: El Contrato del Acceso

Los descriptores no surgieron de un vacío matemático, sino de principios de diseño de software y de la teoría de lenguajes de programación.

### Base Teórica: Protocolos y Delegación

El concepto clave es el **protocolo**. En lugar de definir una estructura rígida, Python define un contrato: "Si tu objeto tiene un método `__get__`, `__set__` o `__delete__`, entonces es un descriptor y participará en el acceso a atributos de una manera especial".

Esto se alinea con la filosofía de "duck typing" de Python y se inspira en conceptos de lenguajes como Smalltalk, uno de los pioneros de la orientación a objetos.

> "La gran idea de Smalltalk es el 'message passing'. El truco es no preocuparse por lo que son los objetos, sino por los mensajes que pueden recibir." — **Alan Kay**, *Conferencia OOPSLA* (1997)

Un descriptor es la forma en que Python implementa el "message passing" para el operador punto. Cuando escribes `obj.x`, no estás accediendo directamente a un dato. Estás enviando un mensaje "get x" al objeto `obj`. Si `x` es un descriptor, este intercepta el mensaje y decide qué hacer. Es un patrón de **delegación** y **proxy** integrado en el núcleo del lenguaje.

### Principios Subyacentes

*   **Metaprogramación:** Los descriptores son una forma de metaprogramación, es decir, código que manipula otro código. Permiten que un objeto (el descriptor) controle el comportamiento de los atributos de una clase en tiempo de ejecución.
*   **Separación de Responsabilidades (SoC):** Permiten extraer lógicas transversales (como validación, cacheo, logging) de la clase principal y encapsularlas en objetos reutilizables. Una clase `User` no debería preocuparse de si un `email` es una cadena válida; esa es la responsabilidad de un descriptor `ValidatedEmail`.
*   **Don't Repeat Yourself (DRY):** Sin descriptores, si tuvieras múltiples atributos que necesitan la misma lógica de validación, la repetirías. Con un descriptor, defines la lógica una vez y la reutilizas.

## 3. Evolución Histórica Detallada

| Fecha       | Hito                                                               | Figuras Clave        | Contexto Histórico                                                                                             |
| :---------- | :----------------------------------------------------------------- | :------------------- | :------------------------------------------------------------------------------------------------------------- |
| **~2000**   | Discusiones sobre la unificación de tipos y clases en Python.      | Guido van Rossum     | La era post-burbuja de las puntocom. Python compite con Perl y Java por el dominio en el desarrollo web.      |
| **2001**    | **Python 2.2** introduce las "new-style classes" y los descriptores. | Guido van Rossum     | Se publican los PEPs 252 y 253. El mecanismo es poderoso pero considerado un detalle de implementación.        |
| **~2005**   | El framework **Django** es liberado. Su ORM usa descriptores masivamente. | Adrian Holovaty, Simon Willison | Los frameworks web de "full-stack" ganan popularidad. El ORM de Django demuestra el poder de los descriptores. |
| **2008**    | **Python 3.0** es lanzado. Los descriptores se mantienen sin cambios. | Comunidad Python     | Un gran cisma en la comunidad. Las "old-style classes" son eliminadas, haciendo los descriptores universales. |
| **2016**    | **Python 3.6** introduce `__set_name__` a través del PEP 487.        | Martin Teichmann, Larry Hastings | Python está en pleno renacimiento, dominando la ciencia de datos. La mejora de los descriptores los hace más ergonómicos. |

El momento decisivo fue, sin duda, la adopción de los descriptores por parte de frameworks como Django. Demostraron que no eran una curiosidad académica, sino una herramienta de ingeniería de software para construir sistemas mantenibles y a gran escala.

## 4. Implementación Práctica: De la Teoría al Código

Basta de historia. Vamos a ensuciarnos las manos.

### El Protocolo en Código

Un descriptor es cualquier objeto que define al menos uno de estos métodos:

*   `__get__(self, instance, owner)`: Se llama al acceder al atributo.
    *   `self`: La instancia del descriptor.
    *   `instance`: La instancia de la clase a la que se accede (o `None` si se accede desde la clase).
    *   `owner`: La clase propietaria.
*   `__set__(self, instance, value)`: Se llama al asignar un valor al atributo.
*   `__delete__(self, instance)`: Se llama al eliminar el atributo con `del`.

### Ejemplo 1: Antes y Después - Validación de Datos

**El mal camino (repetitivo):**

```python
# antes_descriptores.py
class Product:
    def __init__(self, name: str, price: float, quantity: int):
        self.name = name
        # Validación repetida en el setter
        if price < 0:
            raise ValueError("Price cannot be negative.")
        self._price = price
        if quantity < 0:
            raise ValueError("Quantity cannot be negative.")
        self._quantity = quantity

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if value < 0:
            raise ValueError("Price cannot be negative.")
        self._price = value

    @property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, value):
        if value < 0:
            raise ValueError("Quantity cannot be negative.")
        self._quantity = value

# El código es verboso y viola el principio DRY.
# ¿Qué pasa si queremos añadir un `weight` no negativo? Más código repetido.
```

**El buen camino (usando un descriptor):**

```python
# con_descriptores.py
import weakref

class NonNegative:
    """Un descriptor que asegura que un atributo es un número no negativo."""
    
    def __init__(self):
        # Usamos WeakKeyDictionary para evitar fugas de memoria.
        # Almacena los valores por instancia, no en el descriptor.
        self.data = weakref.WeakKeyDictionary()

    def __get__(self, instance, owner):
        # Si instance es None, se accede desde la clase, devolvemos el descriptor.
        if instance is None:
            return self
        return self.data.get(instance)

    def __set__(self, instance, value):
        if not isinstance(value, (int, float)):
            raise TypeError("Value must be a number.")
        if value < 0:
            raise ValueError("Value cannot be negative.")
        self.data[instance] = value

class Product:
    # La lógica de validación está encapsulada y es reutilizable.
    price = NonNegative()
    quantity = NonNegative()

    def __init__(self, name: str, price: float, quantity: int):
        self.name = name
        self.price = price       # Llama a NonNegative.__set__
        self.quantity = quantity # Llama a NonNegative.__set__

# Código limpio, declarativo y DRY.
p = Product("Laptop", 1200.50, 10)
print(p.price)  # Llama a NonNegative.__get__

try:
    p.quantity = -5
except ValueError as e:
    print(e) # "Value cannot be negative."
```

Este ejemplo revela la magia: el descriptor `NonNegative` no almacena *un* valor, sino que gestiona los valores para *todas* las instancias de `Product` que lo usan. Por eso es crucial almacenar los datos en un diccionario (`self.data`) usando la `instance` como clave.

### Data vs. Non-Data Descriptors: La Batalla por la Precedencia

Este es un concepto **crítico** a nivel senior.

*   **Data Descriptor:** Un descriptor que implementa `__set__` (y/o `__delete__`).
*   **Non-Data Descriptor:** Un descriptor que solo implementa `__get__`.

¿Por qué importa? Por el **orden de búsqueda de atributos**.

Cuando haces `obj.x`, Python busca en este orden:

1.  **Data Descriptors:** ¿Hay un *data descriptor* llamado `x` en la clase de `obj` (o sus superclases)? Si es así, se usa su `__get__`. **Esto tiene la máxima prioridad.**
2.  **Diccionario de Instancia:** ¿Está `x` en `obj.__dict__`? Si es así, se devuelve ese valor.
3.  **Non-Data Descriptors:** ¿Hay un *non-data descriptor* llamado `x` en la clase de `obj`? Si es así, se usa su `__get__`.
4.  Error: `AttributeError`.

**Implicación clave:** Un data descriptor anula el `__dict__` de la instancia. Un non-data descriptor puede ser anulado por una asignación en la instancia.

```python
# data_vs_nondata.py

class NonDataDesc:
    def __get__(self, instance, owner):
        return "Non-data descriptor value"

class DataDesc:
    def __get__(self, instance, owner):
        return "Data descriptor value"
    def __set__(self, instance, value):
        print("Data descriptor __set__ called")

class MyClass:
    non_data = NonDataDesc()
    data = DataDesc()

obj = MyClass()

# --- Non-Data Descriptor ---
print(obj.non_data)  # -> "Non-data descriptor value"
obj.non_data = "instance value" # Esto OCULTA el descriptor
print(obj.non_data)  # -> "instance value" (el __dict__ gana)
print(obj.__dict__)  # -> {'non_data': 'instance value'}

# --- Data Descriptor ---
obj2 = MyClass()
print(obj2.data) # -> "Data descriptor value"
obj2.data = "instance value" # Esto llama a __set__, NO oculta el descriptor
print(obj2.data) # -> "Data descriptor value"
print(obj2.__dict__) # -> {} (el __dict__ no se modifica)
```

Los métodos de instancia son non-data descriptors. Por eso puedes "sobrescribir" un método en una instancia particular, aunque rara vez sea una buena idea.

### Caso de Estudio: ORM de Django Simplificado

Imagina cómo Django define un modelo.

```python
# django_orm_simplified.py

class CharField:
    """Un descriptor simple que simula un CharField de Django."""
    def __init__(self, max_length=255):
        self.max_length = max_length
        self._name = None # Se establecerá por __set_name__

    def __set_name__(self, owner, name):
        # ¡La magia de Python 3.6!
        # El descriptor ahora sabe su propio nombre de atributo.
        self._name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self._name)

    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise TypeError(f"{self._name} must be a string.")
        if len(value) > self.max_length:
            raise ValueError(f"{self._name} exceeds max length of {self.max_length}.")
        instance.__dict__[self._name] = value

class User:
    username = CharField(max_length=50)
    email = CharField(max_length=100)

    def __init__(self, username, email):
        self.username = username
        self.email = email

u = User("alan_turing", "alan@bletchleypark.org")
print(u.username)

try:
    u.email = "a" * 200
except ValueError as e:
    print(e) # "email exceeds max length of 100."
```

Este patrón es la base de los ORMs, sistemas de serialización (como Pydantic o Marshmallow) y mucho más. Es declarativo, reutilizable y potente.

## 5. Nivel Senior - Conceptos Avanzados

Aquí es donde separamos a los profesionales de los aficionados.

### `__set_name__`: El Eslabón Perdido

Como vimos, `__set_name__` (PEP 487) es crucial. Antes, el descriptor no sabía su nombre. La solución era torpe:

```python
# El viejo y feo camino
class OldDescriptor:
    def __init__(self, name):
        self.name = name
    # ...

class MyClass:
    attr = OldDescriptor('attr') # ¡Repetir el nombre es propenso a errores!
```

`__set_name__` es un hook que se llama automáticamente cuando se crea la clase, inyectando el nombre del atributo en el descriptor. Esto permite que los descriptores sean verdaderamente "plug-and-play".

### Trade-offs: Cuándo Usar y Cuándo NO Usar Descriptores

| Ventaja                                    | Desventaja (Trade-off)                                                              | Cuándo Usarlo                                                                                              | Cuándo NO Usarlo                                                                                             |
| :----------------------------------------- | :---------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------- | :----------------------------------------------------------------------------------------------------------- |
| **Reutilización de Lógica (DRY)**          | **Complejidad / Magia** - Puede ocultar lo que realmente está sucediendo.             | Cuando tienes la misma lógica (validación, cacheo, logging) en múltiples atributos o clases.               | Para atributos simples que no necesitan lógica especial. Un `self.x = y` es más claro.                       |
| **APIs Declarativas y Limpias**            | **Rendimiento** - Hay una pequeña sobrecarga por la llamada a métodos extra.          | Para construir frameworks, ORMs, o librerías donde la facilidad de uso del usuario final es primordial.    | En código de bajo nivel y crítico para el rendimiento donde cada ciclo de CPU cuenta (e.g., NumPy internals). |
| **Separación de Responsabilidades (SoC)**  | **Introspección** - Herramientas como linters o IDEs pueden tener dificultades para inferir tipos. | Para encapsular lógica compleja de acceso a datos, manteniendo las clases de negocio limpias.            | Cuando una simple función o un `@property` es suficiente y más legible. No uses un mazo para matar una mosca. |
| **Control Fino sobre el Acceso**           | **Depuración** - Rastrear el flujo de control puede ser más difícil.                  | Para implementar atributos de solo lectura, cacheo de propiedades (lazy evaluation), o proxies a otros recursos. | En scripts simples o aplicaciones pequeñas donde la sobrecarga de diseño no se justifica.                    |

> "Los descriptores son una herramienta poderosa, pero como todas las herramientas poderosas, deben usarse con prudencia." — **Luciano Ramalho**, *Fluent Python* (2015)

### Anti-Patrones Comunes

1.  **El Descriptor Anémico:** Un descriptor que simplemente obtiene y establece un valor en `__dict__` sin añadir ninguna lógica. Es solo una reimplementación más lenta de un atributo normal.
2.  **El Descriptor Monolítico (God Descriptor):** Un descriptor que hace demasiadas cosas: valida, loguea, cachea, notifica... Rompe el Principio de Responsabilidad Única. Es mejor componer descriptores más pequeños.
3.  **Almacenar Estado de Instancia en el Descriptor:** Un error de novato fatal. `self.value = value` dentro de `__set__` hará que todas las instancias compartan el mismo valor. ¡Siempre usa la `instance` como clave para almacenar datos!

    ```python
    class BrokenDescriptor:
        def __set__(self, instance, value):
            self._value = value # ¡MAL! Todas las instancias compartirán este _value

    class CorrectDescriptor:
        def __init__(self):
            self.data = weakref.WeakKeyDictionary()
        def __set__(self, instance, value):
            self.data[instance] = value # ¡BIEN! Cada instancia tiene su propio valor
    ```

### Integración con Metaclases: El Nivel Final

Aquí es donde los conceptos se unen en una sinfonía de metaprogramación. Una metaclase puede inspeccionar una clase en el momento de su creación y aplicar descriptores automáticamente.

Imagina que quieres que todos los atributos en mayúsculas de una clase sean validados como no negativos.

```python
# metaclass_descriptors.py
import weakref

# El mismo descriptor NonNegative de antes
class NonNegative:
    def __init__(self):
        self.data = weakref.WeakKeyDictionary()
    def __set_name__(self, owner, name):
        self.name = name
    def __get__(self, instance, owner):
        if instance is None: return self
        return self.data.get(instance)
    def __set__(self, instance, value):
        if not isinstance(value, (int, float)) or value < 0:
            raise ValueError(f"{self.name} must be non-negative.")
        self.data[instance] = value

class AutoValidateMeta(type):
    def __new__(cls, name, bases, dct):
        # 'dct' es el diccionario de atributos de la clase que se está creando
        for key, value in dct.items():
            if key.isupper():
                # Si un atributo está en mayúsculas, lo reemplazamos
                # con un descriptor NonNegative.
                dct[key] = NonNegative()
        
        return super().__new__(cls, name, bases, dct)

class FinancialRecord(metaclass=AutoValidateMeta):
    # La metaclase transformará estos en descriptores NonNegative
    INCOME = 0
    EXPENSES = 0
    
    def __init__(self, income, expenses):
        self.INCOME = income
        self.EXPENSES = expenses

record = FinancialRecord(50000, 30000)
print(record.INCOME) # 50000

try:
    record.EXPENSES = -100 # Esto fallará gracias a la metaclase y el descriptor
except ValueError as e:
    print(e) # "EXPENSES must be non-negative."
```
Este patrón permite crear DSLs (Lenguajes de Dominio Específico) dentro de Python, que es la marca de un verdadero arquitecto de software.

## 6. Referencias y Citaciones Académicas

Un artesano conoce sus herramientas, pero un maestro conoce su historia y su teoría.

1.  > "Los descriptores son un nuevo mecanismo que permite que los objetos personalicen la búsqueda de atributos... Son la maquinaria detrás de las 'new-style classes' y unifican cómo se acceden a los atributos de un objeto." — **Raymond Hettinger**, *Descriptor HowTo Guide, Python Documentation* (circa 2003). [Enlace](https://docs.python.org/3/howto/descriptor.html)

2.  > "En resumen, el objetivo es proporcionar un modelo de objetos que sea totalmente unificable, de modo que los tipos definidos por el usuario puedan heredar de los tipos incorporados y los tipos incorporados puedan heredar de los tipos definidos por el usuario." — **Guido van Rossum**, *PEP 253: Subtyping Built-in Types* (2001). [Enlace](https://www.python.org/dev/peps/pep-0253/)

3.  > "Los descriptores son una forma de reutilizar la lógica que gestiona el almacenamiento de atributos. En esencia, son clases de atributos reutilizables que pueden gestionar el almacenamiento de los atributos de otras clases." — **David Beazley, Brian K. Jones**, *Python Cookbook, 3rd Edition* (2013).

4.  > "La idea clave detrás de los descriptores es que el lenguaje delega el trabajo de obtener, establecer o eliminar un atributo a un método del propio atributo, si ese método existe." — **Alex Martelli**, *Python in a Nutshell* (2006).

5.  > "Los descriptores son el mecanismo de bajo nivel que impulsa propiedades, métodos, métodos estáticos, métodos de clase y `super()`." — **Luciano Ramalho**, *Fluent Python, 2nd Edition* (2022).

6.  > "La introducción de `__set_name__` en Python 3.6 finalmente abordó la necesidad de que los descriptores conozcan el nombre del atributo al que están asignados en la clase propietaria sin necesidad de hacks o intervención manual." — **Martin Teichmann**, *PEP 487: Simpler customisation of class creation* (2016). [Enlace](https://www.python.org/dev/peps/pep-0487/)

7.  > "La orientación a objetos, para mí, significa solo message passing, polimorfismo local y enlace dinámico (tardío)." — **Alan Kay**, *The Early History of Smalltalk* (1993). Los descriptores son la encarnación de este principio para el acceso a atributos en Python.

8.  > "Un lenguaje de programación es de bajo nivel cuando sus programas requieren atención a lo irrelevante." — **Alan Perlis**, *Epigrams on Programming* (1982). Los descriptores ayudan a Python a ser un lenguaje de más alto nivel al abstraer la lógica de acceso a atributos.

---

Has llegado al final. Si has asimilado estos conceptos, no solo sabes *qué* es un descriptor. Entiendes *por qué* existe, los problemas que resuelve, sus orígenes históricos, sus matices de implementación y los trade-offs que un ingeniero senior debe sopesar.

Ahora, cuando veas un ORM, un sistema de validación, o incluso una simple `@property`, no verás magia. Verás un protocolo elegante y poderoso en acción. Verás el trabajo de los centinelas que guardan las puertas del acceso a los atributos, y sabrás, no solo cómo usarlos, sino cómo comandarlos. Ve y construye sistemas más robustos, expresivos y elegantes. El poder es tuyo.
