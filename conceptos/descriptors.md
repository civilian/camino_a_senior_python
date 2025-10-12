# Descriptors

Claro que sí. Prepárate para una inmersión profunda en el mundo de los descriptores de Python. Este no es un tema para principiantes, y dominarlo es una clara señal de madurez como desarrollador de Python, ya que revela el funcionamiento interno del modelo de objetos del lenguaje.

---

# Dominando los Descriptores en Python: Una Guía Profunda para el Programador Senior

## Introducción: ¿Qué problema resuelven los Descriptores?

A un nivel superficial, Python te permite acceder a atributos con la simple notación de punto: `obj.x`. Pero, ¿qué sucede realmente detrás de esa simple operación? ¿Cómo es que `obj.method` se comporta de manera diferente a `obj.data`? ¿Cómo funcionan las `@property`? ¿Cómo los ORMs como Django o SQLAlchemy convierten `user.name` en una consulta a la base de datos?

La respuesta a todas estas preguntas es el **protocolo descriptor**.

Los descriptores son un mecanismo de bajo nivel que te permite "enganchar" y personalizar el comportamiento del acceso a los atributos de un objeto. Son la magia detrás de gran parte de la elegancia y el poder del modelo de objetos de Python.

> "En general, un descriptor es un atributo de objeto con un 'comportamiento de enlace', cuyo acceso al atributo ha sido anulado por métodos en el protocolo de descriptor."
> \- [Python Data Model Documentation](https://docs.python.org/3/reference/datamodel.html#descriptors)

---

## Sección 1: El Protocolo Descriptor - Los Tres Métodos Mágicos

Un objeto es un descriptor si implementa cualquiera de los siguientes métodos especiales (a menudo llamados "métodos de descriptor"):

1.  `__get__(self, instance, owner)`:
    *   **Propósito**: Se llama para obtener el valor de un atributo (lectura). `obj.x`
    *   **`self`**: La instancia del descriptor mismo.
    *   **`instance`**: La instancia a través de la cual se accede al atributo (el `obj`). Puede ser `None` si se accede a través de la clase (`Clase.x`).
    *   **`owner`**: La clase propietaria del descriptor (la `Clase`).

2.  `__set__(self, instance, value)`:
    *   **Propósito**: Se llama para establecer el valor de un atributo (escritura). `obj.x = value`
    *   **`self`**: La instancia del descriptor.
    *   **`instance`**: La instancia cuyo atributo se está estableciendo.
    *   **`value`**: El valor que se va a asignar.

3.  `__delete__(self, instance)`:
    *   **Propósito**: Se llama para eliminar un atributo. `del obj.x`
    *   **`self`**: La instancia del descriptor.
    *   **`instance`**: La instancia cuyo atributo se está eliminando.

### Ejemplo Básico: Un Descriptor de Trazabilidad

Vamos a crear un descriptor simple que solo imprime cuándo se accede a él. Este es el "Hola, Mundo" de los descriptores.

```python
class RevealAccess:
    """Un descriptor que imprime mensajes en get, set y delete."""
    def __init__(self, initval=None, name='var'):
        self.val = initval
        self.name = name

    def __get__(self, instance, owner):
        print(f"Accediendo a '{self.name}' en la instancia {instance}")
        # En un caso real, aquí devolveríamos el valor.
        # Por ahora, solo devolvemos una representación.
        return f"Valor de {self.name}"

    def __set__(self, instance, value):
        print(f"Estableciendo '{self.name}' en la instancia {instance} a {value}")
        # Aquí es donde se almacenaría el valor real.
        self.val = value

    def __delete__(self, instance):
        print(f"Eliminando '{self.name}' de la instancia {instance}")
        del self.val

class MyClass:
    x = RevealAccess(10, 'x')
    y = RevealAccess(5, 'y')

# --- Probando el descriptor ---
m = MyClass()

# Acceso de lectura -> Llama a __get__
print(m.x)
# Salida:
# Accediendo a 'x' en la instancia <__main__.MyClass object at 0x...>
# Valor de x

# Acceso de escritura -> Llama a __set__
m.x = 20
# Salida:
# Estableciendo 'x' en la instancia <__main__.MyClass object at 0x...> a 20

# Acceso de eliminación -> Llama a __delete__
del m.x
# Salida:
# Eliminando 'x' de la instancia <__main__.MyClass object at 0x...>
```

---

## Sección 2: Descriptores de Datos vs. Descriptores de No-Datos

Esta es la distinción más crucial para entender el comportamiento de los descriptores y la precedencia en la búsqueda de atributos.

1.  **Descriptor de Datos (Data Descriptor)**: Un descriptor que implementa `__set__` o `__delete__`. Estos descriptores manejan tanto la lectura como la escritura.

2.  **Descriptor de No-Datos (Non-Data Descriptor)**: Un descriptor que solo implementa `__get__`. Son típicamente para solo lectura, como los métodos.

**¿Por qué es tan importante esta diferencia?** Por la **precedencia**.

> "Los descriptores de datos siempre anulan la redefinición en un diccionario de instancia. En contraste, los descriptores de no-datos pueden ser anulados por las instancias."
> \- [Descriptor How To Guide by Raymond Hettinger](https://docs.python.org/3/howto/descriptor.html#descriptor-protocol)

Esto significa que si tienes un descriptor de datos y un atributo con el mismo nombre en el `__dict__` de una instancia, **el descriptor de datos siempre gana**. Si es un descriptor de no-datos, **el atributo de la instancia gana**.

### Ejemplo de Precedencia

```python
# --- Descriptor de No-Datos (solo __get__) ---
class NonDataDescriptor:
    def __get__(self, instance, owner):
        return "Soy un descriptor de no-datos"

# --- Descriptor de Datos (tiene __set__) ---
class DataDescriptor:
    def __get__(self, instance, owner):
        return "Soy un descriptor de datos"
    def __set__(self, instance, value):
        pass # La implementación no importa, solo su existencia

class Managed:
    non_data = NonDataDescriptor()
    data = DataDescriptor()

# --- Demostración ---
obj = Managed()

# 1. Comportamiento inicial
print(obj.non_data)  # -> 'Soy un descriptor de no-datos'
print(obj.data)      # -> 'Soy un descriptor de datos'

# 2. "Sombreeamos" los descriptores con atributos de instancia
print("\n--- Sombreeando los descriptores ---")
obj.__dict__['non_data'] = 'valor de instancia'
obj.__dict__['data'] = 'valor de instancia'

# 3. Verificamos el resultado
print(obj.non_data)  # -> 'valor de instancia' (El __dict__ de la instancia GANA)
print(obj.data)      # -> 'Soy un descriptor de datos' (El descriptor de datos GANA)
```
Este comportamiento es fundamental. Explica por qué puedes "sombrear" un método (que es un descriptor de no-datos) con un atributo de instancia, pero no puedes hacer lo mismo con una `@property` que tiene un setter (que la convierte en un descriptor de datos).

---

## Sección 3: La Cadena de Búsqueda de Atributos (Attribute Lookup Chain)

Para un programador senior, es vital entender el algoritmo exacto que Python sigue para `obj.x`. Es una secuencia de pasos bien definida:

1.  **¿Es `x` un descriptor de datos en la clase de `obj` o en sus superclases?**
    *   Se busca `x` en `type(obj).__mro__` (el Method Resolution Order).
    *   Si se encuentra un objeto que es un descriptor de datos, se llama a su método `__get__` y se devuelve el resultado. **Fin de la búsqueda.**

2.  **¿Está `x` en el `__dict__` de la instancia `obj`?**
    *   Si `obj.__dict__['x']` existe, se devuelve su valor directamente. **Fin de la búsqueda.**

3.  **¿Es `x` un descriptor de no-datos o un atributo de clase normal?**
    *   Se vuelve a buscar `x` en `type(obj).__mro__`.
    *   Si se encuentra un descriptor de no-datos, se llama a su `__get__` y se devuelve el resultado.
    *   Si se encuentra un atributo de clase normal, se devuelve ese valor.
    *   **Fin de la búsqueda.**

4.  **Lanzar `AttributeError`**.
    *   Si ninguno de los pasos anteriores tuvo éxito, se lanza la excepción.

*Nota: `__getattribute__` puede interceptar este proceso por completo, pero esa es otra capa de complejidad.*

---

## Sección 4: Aplicaciones Prácticas y Casos de Uso (El "Por Qué")

Aquí es donde los descriptores pasan de ser una curiosidad teórica a una herramienta de poder.

### 1. `@property`: Azúcar Sintáctico para Descriptores

La `@property` es, de lejos, el uso más común de los descriptores. Es simplemente una forma más limpia y declarativa de crear un descriptor de datos.

```python
# La forma manual (lo que @property hace por debajo)
class CelsiusManual:
    def __init__(self, temperature=0):
        self._temperature = temperature

    def get_temperature(self):
        print("Obteniendo valor...")
        return self._temperature

    def set_temperature(self, value):
        print("Estableciendo valor...")
        if value < -273.15:
            raise ValueError("La temperatura no puede ser inferior al cero absoluto.")
        self._temperature = value
        
    # property() es una clase que implementa el protocolo descriptor
    temperature = property(get_temperature, set_temperature)

# La forma "Pythonic" con decoradores
class CelsiusPythonic:
    def __init__(self, temperature=0):
        self._temperature = temperature

    @property
    def temperature(self):
        print("Obteniendo valor...")
        return self._temperature

    @temperature.setter
    def temperature(self, value):
        print("Estableciendo valor...")
        if value < -273.15:
            raise ValueError("La temperatura no puede ser inferior al cero absoluto.")
        self._temperature = value

c = CelsiusPythonic()
c.temperature = 30  # Llama al setter
print(c.temperature) # Llama al getter
```

### 2. Validación de Datos y Tipado

Los descriptores son perfectos para crear atributos reutilizables que validan los datos que se les asignan.

```python
class Integer:
    """Un descriptor que solo acepta enteros."""
    def __init__(self, name):
        self.name = name

    def __get__(self, instance, owner):
        # Obtenemos el valor del __dict__ de la instancia
        return instance.__dict__.get(self.name)

    def __set__(self, instance, value):
        if not isinstance(value, int):
            raise TypeError(f"Se esperaba un int para '{self.name}', se obtuvo {type(value).__name__}")
        # Almacenamos el valor en el __dict__ de la instancia
        instance.__dict__[self.name] = value

class Person:
    age = Integer('age')
    salary = Integer('salary')

    def __init__(self, name, age, salary):
        self.name = name
        self.age = age
        self.salary = salary

p = Person("Alice", 30, 50000)
# p.age = "treinta"  # -> Lanza TypeError: Se esperaba un int para 'age'...
```
**Observación importante:** Notarás que el estado (`value`) se almacena en `instance.__dict__` y no en el propio descriptor (`self.value`). Esto es **CRÍTICO**. Los descriptores se instancian una vez por clase, no por objeto. Si almacenaras el estado en el descriptor, todas las instancias de `Person` compartirían la misma edad.

### 3. Atributos "Lazy" o Cacheados

Un caso de uso avanzado es un atributo cuyo valor es costoso de calcular. Un descriptor puede calcularlo solo la primera vez que se accede y luego cachear el resultado.

```python
class LazyProperty:
    def __init__(self, func):
        self.func = func
        self.func_name = func.__name__

    def __get__(self, instance, owner):
        if instance is None:
            return self
        
        # Calcula el valor
        value = self.func(instance)
        
        # Lo almacena en el __dict__ de la instancia para futuros accesos.
        # Esto "sombrea" al descriptor (que es de no-datos), haciendo
        # que los accesos futuros sean instantáneos.
        instance.__dict__[self.func_name] = value
        return value

class DeepThought:
    @LazyProperty
    def meaning_of_life(self):
        """Calcula una respuesta muy, muy costosa."""
        import time
        print("Calculando la respuesta...")
        time.sleep(2)  # Simula un cálculo intensivo
        return 42

d = DeepThought()
print("Primera llamada:")
print(d.meaning_of_life) # Tarda 2 segundos, imprime "Calculando..."

print("\nSegunda llamada:")
print(d.meaning_of_life) # Es instantáneo, no imprime nada
```

### 4. ORMs (Object-Relational Mappers)

En Django, cuando escribes:
`class Post(models.Model): title = models.CharField(max_length=100)`
`models.CharField` es una clase que actúa como un descriptor. Cuando haces `post.title = "Hola"`, el método `__set__` del descriptor `CharField` se encarga de validar la longitud y marcar el objeto como "sucio" para guardarlo en la base de datos. Cuando haces `print(post.title)`, el `__get__` se encarga de recuperar el valor.

### 5. Métodos: ¡Las funciones son descriptores!

Este es el concepto que une todo. En Python, las funciones son objetos y tienen un método `__get__`. Esto las convierte en **descriptores de no-datos**.

Cuando accedes a un método a través de una instancia (`obj.method`), ocurre lo siguiente:
1.  Python encuentra la función `method` en la clase de `obj`.
2.  Detecta que es un descriptor (porque tiene `__get__`).
3.  Llama a `function.__get__(obj, type(obj))`.
4.  El método `__get__` de una función no devuelve la función en sí, sino un nuevo objeto llamado **método enlazado (bound method)**. Este objeto "recuerda" tanto la función original como la instancia (`obj`).
5.  Cuando llamas al método enlazado (`bound_method()`), este invoca la función original, pasando la instancia recordada (`obj`) como el primer argumento (`self`).

¡Es por eso que no tienes que pasar `self` manualmente! El protocolo descriptor se encarga de ello.

> "Las funciones de Python se convierten en métodos enlazados porque todas tienen un método `__get__()` para enlazar métodos a instancias. El `__get__()` de una función devuelve un método enlazado."
> \- [PEP 252 - Making Types Look More Like Classes](https://peps.python.org/pep-0252/)

---

## Sección 5: Consideraciones Avanzadas y "Gotchas"

### `__set_name__` (PEP 487)

En nuestro ejemplo de `Integer`, tuvimos que pasar el nombre del atributo (`'age'`) al constructor. Esto es redundante y propenso a errores. Python 3.6 introdujo una solución elegante.

Si un descriptor define `__set_name__(self, owner, name)`, este método será llamado automáticamente cuando se crea la clase propietaria.

> "Este PEP propone un nuevo método especial, `__set_name__()`, que se llamará en un descriptor cuando se cree la clase propietaria, proporcionando al descriptor una referencia a la clase propietaria y su nombre dentro de esa clase."
> \- [PEP 487 -- Simpler customisation of class creation](https://peps.python.org/pep-0487/)

Refactorizando nuestro validador `Integer`:

```python
class Validated:
    """Un descriptor base que usa __set_name__."""
    def __set_name__(self, owner, name):
        self.private_name = '_' + name

    def __get__(self, instance, owner):
        return getattr(instance, self.private_name)

    def __set__(self, instance, value):
        self.validate(value)
        setattr(instance, self.private_name, value)

    def validate(self, value):
        """Debe ser implementado por las subclases."""
        raise NotImplementedError

class Integer(Validated):
    def validate(self, value):
        if not isinstance(value, int):
            raise TypeError(f"Se esperaba un int, se obtuvo {type(value).__name__}")

class PositiveInteger(Integer):
    def validate(self, value):
        super().validate(value)
        if value <= 0:
            raise ValueError("Se esperaba un entero positivo.")

class Person:
    age = PositiveInteger() # ¡Ya no necesitamos pasar el nombre!
    
    def __init__(self, name, age):
        self.name = name
        self.age = age

p = Person("Bob", 10)
# p.age = -5 # -> Lanza ValueError
```

### Descriptores vs. `__getattr__` y `__getattribute__`

*   **Descriptores**: Para gestionar atributos **específicos** de forma declarativa. Es la herramienta preferida.
*   `__getattr__(self, name)`: Un método de "fallback". Solo se llama si la búsqueda de atributos normal (incluyendo descriptores) **falla**. Útil para proxies o atributos generados dinámicamente.
*   `__getattribute__(self, name)`: Un gancho de bajo nivel que se llama para **cada** acceso a un atributo, sin excepción. Es extremadamente potente pero también peligroso, ya que es fácil crear bucles de recursión infinitos.

El orden de operaciones es: `__getattribute__` -> Descriptores de Datos -> `__dict__` de instancia -> Descriptores de No-Datos -> `__getattr__`.

---

## Conclusión: El Rol del Descriptor en el "Pythonic Way"

Entender los descriptores es entender el núcleo del modelo de objetos de Python. Son la base sobre la que se construyen características fundamentales como `@property`, `@staticmethod`, `@classmethod` y el enlace de métodos.

Para un programador senior, los descriptores no son solo una herramienta, son un cambio de mentalidad:

1.  **Reutilización de Lógica**: Permiten encapsular la lógica de acceso a atributos (validación, cacheo, logging) en clases reutilizables en lugar de repetirla en métodos getter/setter por toda tu base de código.
2.  **APIs Declarativas**: Promueven un estilo de programación más declarativo. En lugar de escribir código imperativo para gestionar un atributo, declaras qué tipo de atributo es (`age = PositiveInteger()`) y dejas que el protocolo descriptor haga el trabajo.
3.  **Claridad y Mantenibilidad**: Un código que usa descriptores de forma efectiva puede ser mucho más limpio y fácil de entender, ya que la lógica de negocio se encuentra en el lugar correcto.

Dominar los descriptores te da el poder de extender el comportamiento de Python de una manera limpia, robusta y, sobre todo, "Pythonic".

---

## Referencias y Lecturas Adicionales

1.  **Documentación Oficial de Python - Data Model**: La fuente canónica. [https://docs.python.org/3/reference/datamodel.html#descriptors](https://docs.python.org/3/reference/datamodel.html#descriptors)
2.  **Descriptor How To Guide by Raymond Hettinger**: La guía más famosa y clara sobre el tema. Una lectura obligatoria. [https://docs.python.org/3/howto/descriptor.html](https://docs.python.org/3/howto/descriptor.html)
3.  **PEP 487 - Simpler customisation of class creation**: Propuesta que introdujo `__set_name__`. [https://peps.python.org/pep-0487/](https://peps.python.org/pep-0487/)
4.  **Libro "Fluent Python" de Luciano Ramalho**: Contiene uno de los capítulos más exhaustivos y bien explicados sobre los descriptores que existen. Es una referencia de nivel senior.
