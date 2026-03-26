# Preguntas y Respuestas de Entrevistas Python (2025)

Banco de preguntas con sus respuestas principales para estudio y repaso.

---

## Preguntas Básicas

### P1. ¿Cuál es la diferencia entre listas y tuplas en Python?

**Respuesta:**

- **Listas**
  - Mutables (se pueden modificar después de crearse).
  - Más lentas que las tuplas.
  - Sintaxis: `lista = [10, "Chelsea", 20]`
- **Tuplas**
  - Inmutables (no se pueden modificar después de crearse).
  - Más rápidas que las listas.
  - Sintaxis: `tupla = (10, "Chelsea", 20)`

---

### P2. ¿Cuáles son las características principales de Python?

**Respuesta:**

- **Interpretado** (no requiere compilación previa).
- **Tipado dinámico** (no hay que declarar tipos de variables).
- Soporta **programación orientada a objetos** (clases, herencia, composición).
- **Las funciones y clases son objetos de primera clase**.
- **Rápido de escribir, más lento de ejecutar** (aunque se puede usar extensiones en C como NumPy para velocidad).
- Ampliamente usado en **apps web, automatización, computación científica, big data**, etc.

---

### P3. ¿Qué tipo de lenguaje es Python? ¿De programación o de scripting?

**Respuesta:**

Python es un **lenguaje de programación de propósito general** que también es excelente para **scripting**. Se usa habitualmente en ambos roles.

---

### P4. Python es un lenguaje interpretado. Explica qué significa.

**Respuesta:**

Un **lenguaje interpretado** ejecuta el código línea por línea en tiempo de ejecución, sin producir un binario de código máquina por adelantado. El código fuente de Python se compila a bytecode y luego lo ejecuta la máquina virtual de Python en tiempo de ejecución.

---

### P5. ¿Qué es PEP 8?

**Respuesta:**

**PEP 8** (Python Enhancement Proposal 8) es la **guía de estilo para el código Python**. Define convenciones para:

- Nombres (funciones, variables, clases).
- Indentación, espacios en blanco, longitud de línea.
- Imports, comentarios y más.

Su objetivo es maximizar la legibilidad y consistencia del código.

---

### P6. ¿Cuáles son los beneficios de usar Python?

**Respuesta:**

1. **Fácil de usar y aprender** – sintaxis clara y de alto nivel.
2. **Interpretado** – ejecuta línea por línea, depuración más sencilla.
3. **Tipado dinámico** – no se necesitan declaraciones de tipo explícitas.
4. **Gratuito y de código abierto** – comunidad y ecosistema sólidos.
5. **Extensa librería estándar y paquetes de terceros** (PyPI).
6. **Portable** – corre en muchas plataformas sin cambios.
7. **Estructuras de datos integradas** (listas, dicts, sets).
8. **Más funcionalidad con menos código** – muy productivo.

---

### P7. ¿Qué son los namespaces en Python?

**Respuesta:**

Un **namespace** es un mapeo de nombres a objetos (como un diccionario). Garantiza que los nombres sean únicos y no entren en conflicto.

Tipos de namespaces:

1. **Namespace built-in** – nombres proporcionados por Python (ej. `len`, `print`).
2. **Namespace global** – nombres definidos a nivel de módulo.
3. **Namespaces envolventes** – nombres en funciones que envuelven a otras.
4. **Namespace local** – nombres dentro de una función específica.

---

### P8. ¿Qué son los decoradores en Python?

**Respuesta:**

Los **decoradores** son una forma de modificar o mejorar funciones o métodos **sin cambiar su código**. Un decorador es un callable que recibe una función y devuelve una nueva función.

Patrón básico:

```python
def mi_decorador(func):
    def wrapper(*args, **kwargs):
        # hacer algo antes
        resultado = func(*args, **kwargs)
        # hacer algo después
        return resultado
    return wrapper

@mi_decorador
def mi_funcion():
    ...
```

---

### P9. ¿Qué son las comprensiones de listas y diccionarios?

**Respuesta:**

- **Comprensión de lista** – forma concisa de crear listas:

```python
x = [i for i in range(5)]      # [0, 1, 2, 3, 4]
```

- **Comprensión de diccionario** – forma concisa de crear dicts:

```python
x = {i: i + 2 for i in range(5)}  # {0: 2, 1: 3, 2: 4, 3: 5, 4: 6}
```

Son más legibles y frecuentemente más rápidas que los bucles manuales.

---

### P10. ¿Cuáles son los tipos de datos integrados más comunes en Python?

**Respuesta:**

- **Números** – `int`, `float`, `complex`
- **Cadenas** – `str`
- **Tipos secuencia** – `list`, `tuple`, `range`
- **Mapeados** – `dict`
- **Conjuntos** – `set`, `frozenset`
- **Booleano** – `bool`
- **Tipos binarios** – `bytes`, `bytearray`, `memoryview`

---

### P11. ¿Cuál es la diferencia entre archivos `.py` y `.pyc`?

**Respuesta:**

- `.py` – **código fuente**.
- `.pyc` – **bytecode compilado** (generado automáticamente al importar módulos para acelerar la carga).

Los archivos `.pyc` se generan automáticamente y son usados internamente por Python.

---

### P12. ¿Qué es el slicing en Python?

**Respuesta:**

El **slicing** extrae partes de secuencias (cadenas, listas, tuplas) usando:

```python
secuencia[inicio:fin:paso]
```

- `inicio` – índice de comienzo (incluido).
- `fin` – índice de fin (excluido).
- `paso` – salto; puede ser negativo.

Ejemplo:

```python
lst = [1, 2, 3, 4, 5, 6, 7, 8]
lst[1:5]      # [2, 3, 4, 5]
lst[::-1]     # [8, 7, 6, 5, 4, 3, 2, 1]
```

---

### P13. ¿Qué son las palabras clave (keywords) en Python?

**Respuesta:**

Las **keywords** son palabras reservadas con significado especial (no se pueden usar como identificadores). Ejemplos:

`and, or, not, if, elif, else, for, while, break, as, def, lambda, pass, return, True, False, try, with, assert, class, continue, del, except, finally, from, global, import, in, is, None, nonlocal, raise, yield`

---

### P14. ¿Qué son los literales en Python y qué tipos existen?

**Respuesta:**

Los **literales** representan valores fijos en el código:

- **Literales de cadena** – `"Hola"`, `'Mundo'`, `"""multilínea"""`.
- **Literales numéricos** – enteros, floats, complejos: `10`, `7.9`, `3+4j`.
- **Literales booleanos** – `True`, `False`.
- **Literales de colección**:
  - Listas: `[1, 2, 3]`
  - Tuplas: `(1, 2, 3)`
  - Dicts: `{1: "manzana"}`
  - Sets: `{"A", "B"}`
- **Literal especial** – `None` (representa nulo).

---

### P15. ¿Cuáles son las novedades más destacadas de Python 3.9?

**Respuesta:**

- Operadores de **fusión (`|`) y actualización (`|=`)** para dicts.
- Nuevos métodos de cadena: `removeprefix`, `removesuffix`.
- Mejoras en type hints para colecciones estándar.
- Nuevo parser basado en PEG.
- Nuevos módulos como `zoneinfo`, `graphlib`.
- Diversas optimizaciones y deprecaciones.

---

### P16. ¿Cómo se gestiona la memoria en Python?

**Respuesta:**

- Python gestiona la memoria en un **heap privado**.
- Un **gestor de memoria** integrado se encarga de la asignación.
- Python tiene un **recolector de basura** automático para recuperar memoria no usada (basado en conteo de referencias + GC cíclico).

---

### P17. ¿Qué es un namespace en Python?

**Respuesta:**

Un **namespace** es un mapeo (como un dict) de nombres a objetos, usado para evitar colisiones de nombres. Ejemplos: namespace built-in, global y local.

---

### P18. ¿Qué es `PYTHONPATH`?

**Respuesta:**

`PYTHONPATH` es una **variable de entorno** que especifica directorios adicionales donde el intérprete debe buscar módulos al importar.

---

### P19. ¿Qué son los módulos de Python? Nombra algunos integrados comunes.

**Respuesta:**

Un **módulo** es un archivo `.py` que contiene código Python (funciones, clases, variables).

Módulos integrados comunes:

- `os`, `sys`, `math`, `random`, `datetime`, `json`, etc.

---

### P20. ¿Cuál es la diferencia entre variables locales y globales en Python?

**Respuesta:**

- **Variables globales** – declaradas en el nivel superior de un módulo; accesibles en todo el archivo.
- **Variables locales** – declaradas dentro de una función; accesibles solo dentro de ella.

Ejemplo:

```python
a = 2  # global

def sumar():
    b = 3  # local
    c = a + b
    print(c)  # 5
```

---

### P21. ¿Python distingue entre mayúsculas y minúsculas?

**Respuesta:**

Sí, Python es **case sensitive** (`Variable`, `variable` y `VARIABLE` son tres identificadores distintos).

---

### P22. ¿Qué es la conversión de tipos en Python?

**Respuesta:**

La **conversión de tipos** transforma un tipo de dato en otro:

- `int()`, `float()`, `str()`, `tuple()`, `list()`, `set()`, `dict()`, `complex()`, etc.

Ejemplo:

```python
int("10")      # 10
float("3.14")  # 3.14
str(123)       # "123"
```

---

### P23. ¿Cómo instalar Python en Windows y configurar el PATH?

**Respuesta:**

1. Descargar el instalador desde `python.org`.
2. Ejecutar el instalador y (opcionalmente) marcar **"Add Python to PATH"**.
3. Si no se añade automáticamente:
   - Encontrar la ruta de instalación (ej. `C:\Python39\`).
   - Añadirla a **Variables de Entorno → PATH**.

---

### P24. ¿Es obligatoria la indentación en Python?

**Respuesta:**

Sí. La **indentación es sintácticamente significativa** y define los bloques de código (ej. dentro de `if`, `for`, `def`, etc.). Una indentación incorrecta provoca `IndentationError`.

---

### P25. ¿Cuál es la diferencia entre arrays y listas en Python?

**Respuesta:**

- **Listas**
  - Pueden contener elementos de **distintos tipos**.
  - Integradas, muy flexibles.
- **Arrays** (módulo `array`)
  - Contienen elementos de **un solo tipo** (ej. todos enteros).
  - Más eficientes en memoria para datos numéricos homogéneos grandes.

Ejemplo:

```python
import array as arr

mi_array = arr.array('i', [1, 2, 3, 4])
mi_lista  = [1, "abc", 1.20]
```

---

### P26. ¿Qué son las funciones en Python?

**Respuesta:**

Una **función** es un bloque de código reutilizable definido con `def` y que se ejecuta solo cuando se llama.

Ejemplo:

```python
def nueva_funcion():
    print("Hola, bienvenido")

nueva_funcion()
```

---

### P27. ¿Qué es `__init__`?

**Respuesta:**

`__init__` es el método **constructor** de una clase. Se llama automáticamente al crear una nueva instancia y se usa típicamente para inicializar atributos.

Ejemplo:

```python
class Empleado:
    def __init__(self, nombre, edad, salario):
        self.nombre = nombre
        self.edad = edad
        self.salario = salario
```

---

### P28. ¿Qué es una función lambda?

**Respuesta:**

Una **lambda** es una **función anónima** definida con la palabra clave `lambda`, con una única expresión.

Ejemplo:

```python
sumar = lambda x, y: x + y
sumar(5, 6)  # 11
```

---

### P29. ¿Qué es `self` en Python?

**Respuesta:**

`self` hace referencia a la **instancia** de la clase sobre la que se está llamando el método. Es el primer parámetro de los métodos de instancia por convención (no es una keyword).

---

### P30. ¿Para qué sirven `break`, `continue` y `pass`?

**Respuesta:**

- `break` – sale del bucle más cercano.
- `continue` – salta el resto de la iteración actual y pasa a la siguiente.
- `pass` – no hace nada; se usa como marcador de posición donde el código es sintácticamente necesario.

---

### P31. ¿Qué hace `[::-1]`?

**Respuesta:**

`[::-1]` es un slice que devuelve la secuencia **invertida**.

```python
lst = [1, 2, 3, 4, 5]
lst[::-1]  # [5, 4, 3, 2, 1]
```

---

### P32. ¿Cómo se mezclan aleatoriamente los elementos de una lista en Python?

**Respuesta:**

Usando `random.shuffle`:

```python
from random import shuffle

x = ['Keep', 'The', 'Blue', 'Flag', 'Flying', 'High']
shuffle(x)
```

---

### P33. ¿Qué son los iteradores en Python?

**Respuesta:**

Un **iterador** es un objeto que implementa:

- `__iter__()` – devuelve el objeto iterador en sí.
- `__next__()` – devuelve el siguiente valor o lanza `StopIteration`.

Se usan para recorrer contenedores como listas, tuplas, etc.

---

### P34. ¿Cómo se generan números aleatorios en Python?

**Respuesta:**

Usando el módulo `random`:

```python
import random

random.random()         # float en [0.0, 1.0)
random.randint(1, 10)   # entero entre 1 y 10 inclusive
```

---

### P35. ¿Cuál es la diferencia entre `range` y `xrange`?

**Respuesta (contexto Python 2):**

- `range` devuelve una **lista**.
- `xrange` devuelve un **objeto xrange** que genera valores bajo demanda (como un generador).

En **Python 3**, `range` se comporta como el antiguo `xrange` y `xrange` ya no existe.

---

### P36. ¿Cómo se escriben comentarios en Python?

**Respuesta:**

- Los comentarios de una línea usan `#`.
- La documentación multilínea se hace habitualmente con cadenas entre comillas triples (`""" ... """`) como docstrings.

---

### P37. ¿Qué son el pickling y el unpickling?

**Respuesta:**

- **Pickling** – serializar objetos Python a un flujo de bytes usando el módulo `pickle`.
- **Unpickling** – deserializar el flujo de bytes de vuelta a objetos Python.

Usar solo con **datos de confianza**, ya que deserializar datos arbitrarios puede ejecutar código.

---

### P38. ¿Qué son los generadores en Python?

**Respuesta:**

Los generadores son funciones que usan `yield` para producir una secuencia de valores de forma diferida, devolviendo un iterador.

Ejemplo:

```python
def cuenta_regresiva(n):
    while n > 0:
        yield n
        n -= 1
```

---

### P39. ¿Cómo se capitaliza la primera letra de una cadena?

**Respuesta:**

Usando `str.capitalize()`:

```python
"edureka".capitalize()  # "Edureka"
```

---

### P40. ¿Cómo se convierte una cadena a minúsculas?

**Respuesta:**

Usando `str.lower()`:

```python
"ABCD".lower()  # "abcd"
```

---

### P41. ¿Cómo se comentan múltiples líneas en Python?

**Respuesta:**

Se prefija cada línea con `#`, o en muchos editores se seleccionan las líneas y se usa un atajo de teclado para comentar en bloque. Las cadenas multilínea (`"""..."""`) también pueden servir como documentación pero técnicamente no son comentarios.

---

### P42. ¿Qué son los docstrings en Python?

**Respuesta:**

Los **docstrings** son literales de cadena que aparecen como primera sentencia en un módulo, función, clase o método. Documentan qué hace el objeto y son accesibles mediante `.__doc__` o `help()`.

Ejemplo:

```python
def sumar(a, b):
    """Devuelve la suma de a y b."""
    return a + b
```

---

### P43. ¿Para qué sirven los operadores `is`, `not` e `in`?

**Respuesta:**

- `is` – prueba de identidad (`a is b` comprueba si ambos referencian el mismo objeto).
- `not` – negación lógica (`not True` → `False`).
- `in` – prueba de pertenencia (`x in secuencia`).

---

### P44. ¿Para qué sirven `help()` y `dir()`?

**Respuesta:**

- `help(obj)` – muestra la documentación de un objeto, módulo, función, etc.
- `dir(obj)` – lista atributos y métodos de un objeto (o del ámbito actual si no se pasa argumento).

---

### P45. ¿Por qué al salir de Python no se libera toda la memoria?

**Respuesta:**

- Los objetos con **referencias cíclicas** o referenciados desde namespaces globales pueden no liberarse inmediatamente.
- La memoria asignada por el **runtime de C** (o extensiones) puede no devolverse al SO de inmediato.
- Python depende del **recolector de basura** y del comportamiento del asignador subyacente.

---

### P46. ¿Qué es un diccionario en Python?

**Respuesta:**

Un **diccionario** es una colección de pares clave-valor.

Ejemplo:

```python
persona = {"País": "España", "Capital": "Madrid", "Moneda": "Euro"}
persona["País"]  # "España"
```

---

### P47. ¿Cómo se usan los operadores ternarios en Python?

**Respuesta:**

Python usa una expresión condicional:

```python
resultado = x if condicion else y
```

Ejemplo:

```python
mayor = x if x > y else y
```

---

### P48. ¿Qué significan `*args` y `**kwargs` y para qué se usan?

**Respuesta:**

- `*args` – recoge argumentos **posicionales** extra en una tupla.
- `**kwargs` – recoge argumentos **keyword** extra en un dict.

Se usan cuando:

- No se sabe de antemano cuántos argumentos se pasarán.
- Se quieren reenviar argumentos a otra función.

---

### P49. ¿Qué hace `len()`?

**Respuesta:**

Devuelve la **longitud** de un objeto (número de elementos en una lista, caracteres en una cadena, etc.).

---

### P50. Explica los métodos `split()`, `sub()` y `subn()` del módulo `re`.

**Respuesta:**

- `re.split(patron, cadena)` – divide la cadena usando un patrón regex.
- `re.sub(patron, reemplazo, cadena)` – reemplaza las ocurrencias del patrón (devuelve nueva cadena).
- `re.subn(patron, reemplazo, cadena)` – como `sub` pero también devuelve el número de sustituciones realizadas.

---

### P51. ¿Qué son los índices negativos y para qué se usan?

**Respuesta:**

Los índices negativos hacen referencia a posiciones **desde el final** de la secuencia:

- `-1` – último elemento.
- `-2` – penúltimo, etc.

Son convenientes para acceder o hacer slicing relativo al final.

---

### P52. ¿Qué son los paquetes de Python?

**Respuesta:**

Los **paquetes** son namespaces que contienen múltiples módulos, representados usualmente por un directorio con `__init__.py` (o paquetes de namespace en Python moderno).

---

### P53. ¿Cómo se elimina un archivo en Python?

**Respuesta:**

Usando `os.remove`:

```python
import os
os.remove("archivo.txt")
```

---

### P54. ¿Cuáles son los tipos de variables en la POO de Python?

**Respuesta:**

- **Variables de instancia** – únicas para cada instancia (`self.var`).
- **Variables de clase** – compartidas entre todas las instancias (`Clase.var`).

---

### P55. ¿Qué ventajas ofrecen los arrays de NumPy sobre las listas de Python?

**Respuesta:**

- Más **eficientes** (almacenamiento compacto y homogéneo).
- Soportan **operaciones vectorizadas** (aritmética elemento a elemento, etc.).
- Gran conjunto de rutinas numéricas (álgebra lineal, FFT, estadística).
- Generalmente **mucho más rápidos** que los bucles puros de Python.

---

### P56. ¿Cómo se añaden valores a un array de Python?

**Respuesta:**

Usando el módulo `array`:

```python
import array as arr
a = arr.array('d', [1.1, 2.1, 3.1])

a.append(3.4)
a.extend([4.5, 6.3, 6.8])
a.insert(2, 3.8)
```

---

### P57. ¿Cómo se eliminan valores de un array de Python?

**Respuesta:**

Usando `pop` y `remove`:

```python
import array as arr
a = arr.array('d', [1.1, 2.2, 3.8, 3.1, 3.7, 1.2, 4.6])

a.pop()        # elimina y devuelve el último elemento
a.pop(3)       # elimina y devuelve el elemento en el índice 3
a.remove(1.1)  # elimina la primera ocurrencia del valor 1.1
```

---

### P58. ¿Python soporta POO?

**Respuesta:**

Sí. Python soporta **programación orientada a objetos**: clases, objetos, herencia, polimorfismo, encapsulamiento, etc. También puede usarse en estilos procedural y funcional.

---

### P59. ¿Cuál es la diferencia entre copia profunda y copia superficial?

**Respuesta:**

- **Copia superficial (shallow copy)**
  - Copia el **contenedor externo**, pero no los objetos anidados (comparte referencias).
  - Los cambios en objetos anidados afectan a ambas copias.
- **Copia profunda (deep copy)**
  - Copia el contenedor **y todos los objetos anidados** de forma recursiva.
  - Los cambios en una copia no afectan a la otra.

Se implementan con `copy.copy()` (superficial) y `copy.deepcopy()` (profunda).

---

### P60. ¿Cómo se logra el multithreading en Python?

**Respuesta:**

- Python tiene el módulo `threading` y `concurrent.futures.ThreadPoolExecutor`.
- Pero CPython tiene el **Global Interpreter Lock (GIL)**, por lo que solo un hilo ejecuta bytecode Python a la vez.
- Los hilos son buenos para tareas **I/O-bound**; para tareas **CPU-bound** se debe usar **multiprocessing** o extensiones en código nativo.

---

### P61. ¿Cómo funciona la compilación y el enlazado en Python?

**Respuesta:**

El código Python se compila a **bytecode** (`.pyc`) y lo ejecuta el intérprete. Al extender Python con C/C++:

1. Escribir el archivo fuente de la extensión (ej. `modulo.c`).
2. Añadirlo al build (ej. `Modules/Setup.local`).
3. Recompilar Python o construir el módulo de extensión.

---

### P62. ¿Qué son las librerías de Python? Nombra algunas.

**Respuesta:**

Las librerías de Python son colecciones de módulos que proporcionan funcionalidades específicas:

- **NumPy, Pandas, Matplotlib, SciPy, Scikit-learn, Requests, Flask, Django, TensorFlow**, etc.

---

### P63. ¿Para qué sirve `split`?

**Respuesta:**

`str.split()` divide una cadena en una lista usando un delimitador (por defecto: espacio en blanco).

```python
"hola mundo".split()  # ["hola", "mundo"]
```

---

### P64. ¿Qué son los tipos de datos mutables e inmutables?

**Respuesta:**

- **Mutables** – se pueden modificar en su lugar (ej. `list`, `dict`, `set`, `bytearray`).
- **Inmutables** – no se pueden modificar en su lugar (ej. `str`, `tuple`, `int`, `float`, `bool`, `frozenset`).

---

### P65. ¿Para qué sirve el bloque `try` / `except` en Python?

**Respuesta:**

Se usa para el **manejo de excepciones**:

```python
try:
    # código que puede lanzar una excepción
    ...
except AlgunError:
    # manejar el error
    ...
else:
    # se ejecuta si no hubo excepción
    ...
finally:
    # siempre se ejecuta
    ...
```

---

### P66. ¿Qué es un OrderedDict en Python?

**Respuesta:**

`collections.OrderedDict` preserva el **orden de inserción** al iterar. Desde Python 3.7+, el `dict` integrado también preserva el orden de inserción, pero `OrderedDict` ofrece algunos métodos adicionales.

---

### P67. ¿Cuál es la diferencia entre `return` y `yield`?

**Respuesta:**

- `return` – sale de la función **y devuelve un valor**; la función no puede reanudarse después.
- `yield` – convierte la función en un **generador**; produce un valor y suspende la ejecución, que puede reanudarse más tarde donde se dejó.

---

### P68. ¿Cuál es la diferencia entre `set()` y `frozenset()`?

**Respuesta:**

- `set` – **mutable**; se pueden añadir/eliminar elementos.
- `frozenset` – versión **inmutable** de un set; es hashable y puede usarse como clave de dict o elemento de otro set.

---

### P69. ¿Cuáles son las formas de intercambiar los valores de dos variables?

**Respuesta:**

La forma pythónica:

```python
a, b = b, a
```

---

### P70. ¿Cómo se importan módulos en Python?

**Respuesta:**

```python
import array               # importar módulo completo
import array as arr        # importar con alias
from array import *        # importar todo (no recomendado)
from array import array    # importar nombre específico
```

---

## Preguntas de POO

### P71. Explica la herencia en Python con un ejemplo.

**Respuesta:**

La **herencia** permite que una clase (hija) derive atributos y métodos de otra clase (padre).

Tipos: simple, multinivel, jerárquica, herencia múltiple.

Ejemplo:

```python
class Animal:
    def hablar(self):
        print("Algún sonido")

class Perro(Animal):  # Perro hereda de Animal
    def hablar(self):
        print("Guau")
```

---

### P72. ¿Cómo se crean clases en Python?

**Respuesta:**

Usando la palabra clave `class`:

```python
class Empleado:
    def __init__(self, nombre):
        self.nombre = nombre

e1 = Empleado("Ana")
print(e1.nombre)
```

---

### P73. ¿Qué es el monkey patching en Python?

**Respuesta:**

El **monkey patching** consiste en modificar dinámicamente una clase o módulo **en tiempo de ejecución**.

Ejemplo:

```python
import modulo

def funcion_parche(self):
    print("Función parcheada")

modulo.MiClase.metodo = funcion_parche
obj = modulo.MiClase()
obj.metodo()  # imprime "Función parcheada"
```

---

### P74. ¿Python soporta herencia múltiple?

**Respuesta:**

Sí. Una clase puede heredar de **múltiples clases base**:

```python
class C(A, B):
    ...
```

---

### P75. ¿Qué es el polimorfismo en Python?

**Respuesta:**

El **polimorfismo** permite que objetos de distintas clases sean tratados a través de una interfaz común (mismo nombre de método, distintas implementaciones).

Ejemplo: varias clases implementan un método `hablar()`; el código puede llamar a `obj.hablar()` sin importar la clase concreta.

---

### P76. Define encapsulamiento en Python.

**Respuesta:**

El **encapsulamiento** agrupa datos (atributos) y métodos que operan sobre esos datos dentro de una clase. En Python, los guiones bajos iniciales (`_attr`, `__attr`) señalan uso "protegido" o "privado" por convención.

---

### P77. ¿Cómo se hace abstracción de datos en Python?

**Respuesta:**

Usando **clases base abstractas (ABCs)** e **interfaces** (módulo `abc`), ocultando la implementación interna y exponiendo solo los métodos necesarios.

---

### P78. ¿Python usa especificadores de acceso?

**Respuesta:**

Python no tiene modificadores de acceso estrictos como `public`/`private`; usa **convenciones de nomenclatura**:

- `_nombre` – "protegido" (uso interno).
- `__nombre` – name-mangling para desaconsejar el acceso externo.

---

### P79. ¿Cómo se crea una clase vacía en Python?

**Respuesta:**

Usando `pass`:

```python
class A:
    pass

obj = A()
obj.nombre = "xyz"
```

---

### P80. ¿Qué hace `object()`?

**Respuesta:**

`object` es la **clase base** de todas las clases en Python. `object()` devuelve una nueva instancia sin características especiales.

---

## Preguntas Avanzadas

### P81. ¿Qué es el GIL y cuándo importa?

**Respuesta:**

El **Global Interpreter Lock (GIL)** es un mutex en CPython que permite que solo un hilo ejecute bytecode Python a la vez.

- **No importa** para tareas I/O-bound (el hilo libera el GIL mientras espera).
- **Sí importa** para tareas CPU-bound: usar `multiprocessing` para paralelismo real.

---

### P82. ¿Qué diferencia hay entre `__str__` y `__repr__`?

**Respuesta:**

- `__str__` – representación legible para humanos (usada por `print()`).
- `__repr__` – representación oficial/para depuración; idealmente permite recrear el objeto.

```python
class Punto:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __str__(self):
        return f"Punto({self.x}, {self.y})"

    def __repr__(self):
        return f"Punto(x={self.x}, y={self.y})"
```

---

### P83. ¿Qué son los context managers y para qué se usan?

**Respuesta:**

Un **context manager** gestiona recursos automáticamente (apertura y cierre de archivos, conexiones, locks) usando el protocolo `__enter__` / `__exit__`.

```python
# La forma más común: with
with open("archivo.txt") as f:
    contenido = f.read()
# el archivo se cierra automáticamente, incluso si hay excepción

# Crear uno propio con contextlib
from contextlib import contextmanager

@contextmanager
def temporizador():
    import time
    inicio = time.time()
    yield
    print(f"Tardó {time.time() - inicio:.2f}s")
```

---

### P84. ¿Qué es la metaclase en Python?

**Respuesta:**

Una **metaclase** es la clase de una clase. Controla cómo se crean las clases. `type` es la metaclase por defecto.

```python
class MiMeta(type):
    def __new__(mcs, nombre, bases, namespace):
        # modificar la clase antes de crearla
        return super().__new__(mcs, nombre, bases, namespace)

class MiClase(metaclass=MiMeta):
    pass
```

Se usa para validación automática, registro de clases, inyección de métodos, etc.

---

### P85. ¿Qué son los descriptores en Python?

**Respuesta:**

Un **descriptor** es cualquier objeto que implementa `__get__`, `__set__` o `__delete__`. Son el mecanismo detrás de `property`, `classmethod` y `staticmethod`.

```python
class Validado:
    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, f"_{self.name}", None)

    def __set__(self, obj, value):
        if not isinstance(value, int):
            raise TypeError(f"{self.name} debe ser entero")
        setattr(obj, f"_{self.name}", value)

class Producto:
    precio = Validado()
```

---

### P86. ¿Cuál es la diferencia entre `@staticmethod` y `@classmethod`?

**Respuesta:**

- `@staticmethod` – no recibe ni `self` ni `cls`; es básicamente una función regular agrupada en la clase.
- `@classmethod` – recibe `cls` (la clase) como primer argumento; puede acceder y modificar el estado de la clase.

```python
class Fecha:
    def __init__(self, año, mes, dia):
        self.año, self.mes, self.dia = año, mes, dia

    @classmethod
    def desde_cadena(cls, cadena):
        año, mes, dia = map(int, cadena.split("-"))
        return cls(año, mes, dia)

    @staticmethod
    def es_valida(cadena):
        return len(cadena.split("-")) == 3
```

---

### P87. ¿Qué es `__slots__`?

**Respuesta:**

`__slots__` restringe los atributos que puede tener una instancia, eliminando el `__dict__` por defecto. Reduce el uso de memoria cuando se crean muchas instancias.

```python
class Punto:
    __slots__ = ("x", "y")

    def __init__(self, x, y):
        self.x = x
        self.y = y

# p.z = 1  →  AttributeError
```

---

### P88. ¿Qué es `asyncio` y cuándo usarlo?

**Respuesta:**

`asyncio` es la librería de Python para programación **asíncrona y concurrente** basada en un event loop y coroutines (`async/await`).

Cuándo usarlo: tareas **I/O-bound** (peticiones HTTP, consultas a BD, lectura de archivos en red) donde el programa pasa mucho tiempo esperando respuestas externas.

```python
import asyncio
import aiohttp

async def obtener_datos(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as respuesta:
            return await respuesta.json()

async def main():
    urls = ["https://api.ejemplo.com/1", "https://api.ejemplo.com/2"]
    tareas = [obtener_datos(url) for url in urls]
    resultados = await asyncio.gather(*tareas)
    return resultados

asyncio.run(main())
```

---

### P89. ¿Qué es `functools.wraps` y por qué es importante en decoradores?

**Respuesta:**

`functools.wraps` preserva los metadatos de la función original (nombre, docstring, etc.) cuando se crea un decorador. Sin él, la función decorada pierde su identidad.

```python
from functools import wraps

def mi_decorador(func):
    @wraps(func)  # sin esto, mi_funcion.__name__ sería "wrapper"
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@mi_decorador
def mi_funcion():
    """Mi docstring."""
    pass

print(mi_funcion.__name__)  # "mi_funcion" (correcto)
```

---

### P90. ¿Qué es MRO (Method Resolution Order)?

**Respuesta:**

El **MRO** define el orden en que Python busca métodos en la jerarquía de herencia. Se calcula con el algoritmo **C3 linearization**.

```python
class A:
    def metodo(self): print("A")

class B(A):
    def metodo(self): print("B")

class C(A):
    def metodo(self): print("C")

class D(B, C):
    pass

D().metodo()       # "B" (busca D → B → C → A)
print(D.__mro__)   # (<class 'D'>, <class 'B'>, <class 'C'>, <class 'A'>, <class 'object'>)
```

---

### P91. ¿Qué son los type hints y por qué usarlos?

**Respuesta:**

Los **type hints** (PEP 484) permiten anotar tipos en funciones y variables. No los hace obligatorios en tiempo de ejecución, pero herramientas como `mypy` los validan estáticamente.

```python
def sumar(a: int, b: int) -> int:
    return a + b

from typing import Optional, List

def procesar(items: List[str], limite: Optional[int] = None) -> List[str]:
    return items[:limite]
```

Beneficios: mejor autocompletado en IDEs, detección temprana de errores, documentación implícita.

---

### P92. ¿Cuál es la diferencia entre `is` e `==`?

**Respuesta:**

- `==` – comprueba **igualdad de valor** (llama a `__eq__`).
- `is` – comprueba **identidad** (si ambas variables apuntan al mismo objeto en memoria).

```python
a = [1, 2, 3]
b = [1, 2, 3]

a == b   # True  (mismo valor)
a is b   # False (objetos distintos en memoria)

c = a
a is c   # True  (mismo objeto)
```

Nunca usar `is` para comparar valores; solo para comparar con `None`, `True`, `False`.
