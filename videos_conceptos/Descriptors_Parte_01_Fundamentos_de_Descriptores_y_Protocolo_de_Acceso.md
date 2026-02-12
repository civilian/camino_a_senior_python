¿Alguna vez te has preguntado qué sucede realmente cuando escribes `objeto.atributo`? No es tan simple como parece. Hay un poderoso mecanismo, un guardián silencioso, que controla cada acceso, y dominarlo es la clave para desbloquear el verdadero poder de Python.

# Descriptors

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