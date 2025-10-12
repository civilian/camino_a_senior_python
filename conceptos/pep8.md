# PEP8

¡Excelente! Has pedido una inmersión profunda en PEP 8, y eso es exactamente lo que obtendrás. Un desarrollador senior no solo *conoce* las reglas de PEP 8, sino que entiende *por qué* existen, cuándo aplicarlas y, lo que es más importante, cuándo romperlas con justificación.

Este documento está diseñado para ser tu guía definitiva.

---

# Guía Profunda de PEP 8: De Cero a Senior

## Tabla de Contenidos
1.  [¿Qué es PEP 8 y por qué es crucial para un Senior?](#1-qué-es-pep-8-y-por-qué-es-crucial-para-un-senior)
2.  [La Filosofía Subyacente: El Zen de Python](#2-la-filosofía-subyacente-el-zen-de-python)
3.  [Las Reglas Fundamentales (El "Qué")](#3-las-reglas-fundamentales-el-qué)
    *   [3.1 Layout del Código](#31-layout-del-código)
    *   [3.2 Convenciones de Nomenclatura (Naming Conventions)](#32-convenciones-de-nomenclatura-naming-conventions)
    *   [3.3 Comentarios y Docstrings](#33-comentarios-y-docstrings)
    *   [3.4 Espacios en Blanco en Expresiones y Sentencias](#34-espacios-en-blanco-en-expresiones-y-sentencias)
    *   [3.5 Importaciones (Imports)](#35-importaciones-imports)
    *   [3.6 Recomendaciones de Programación](#36-recomendaciones-de-programación)
4.  [El Salto a Senior: Cuándo Ignorar PEP 8 (El "Porqué" y el "Cuándo")](#4-el-salto-a-senior-cuándo-ignorar-pep-8-el-porqué-y-el-cuándo)
5.  [Herramientas del Oficio: Automatización de PEP 8](#5-herramientas-del-oficio-automatización-de-pep-8)
6.  [Conclusión: PEP 8 como Lenguaje Común](#6-conclusión-pep-8-como-lenguaje-común)

---

## 1. ¿Qué es PEP 8 y por qué es crucial para un Senior?

**PEP** significa **P**ython **E**nhancement **P**roposal. Son documentos que proponen nuevas características, procesos o entornos para Python. **PEP 8**, escrito en 2001 por Guido van Rossum, Barry Warsaw y Nick Coghlan, es la guía de estilo oficial para el código Python.

Un desarrollador junior ve PEP 8 como un conjunto de reglas a memorizar. Un desarrollador senior lo ve como un **contrato social** para la colaboración. Su propósito principal no es la estética, sino la **legibilidad**.

> > "Readability counts."
> > — The Zen of Python, PEP 20

El código se lee muchas más veces de las que se escribe. Un código que sigue PEP 8 es predecible. Reduce la carga cognitiva de tus compañeros de equipo (y de tu "yo" futuro), permitiéndoles centrarse en la lógica del programa en lugar de descifrar tu estilo de escritura idiosincrásico.

**Para un senior, dominar PEP 8 significa:**
*   **Escribir código profesional y mantenible.**
*   **Facilitar la colaboración y las revisiones de código (Code Reviews).**
*   **Demostrar disciplina y atención al detalle.**
*   **Entender el "espíritu" de la comunidad Python.**

---

## 2. La Filosofía Subyacente: El Zen de Python

Antes de las reglas, está la filosofía. PEP 8 es la manifestación práctica del **Zen de Python (PEP 20)**. Ejecuta `import this` en tu intérprete de Python.

```python
import this
```

Verás principios como:
*   *Beautiful is better than ugly.* (Bello es mejor que feo.)
*   *Explicit is better than implicit.* (Explícito es mejor que implícito.)
*   *Simple is better than complex.* (Simple es mejor que complejo.)
*   *Readability counts.* (La legibilidad cuenta.)

PEP 8 es la guía para hacer que tu código sea "bello", "explícito" y "legible".

---

## 3. Las Reglas Fundamentales (El "Qué")

Aquí desglosamos las secciones más importantes de PEP 8, con citas directas y el razonamiento de un senior.

### 3.1 Layout del Código

#### 3.1.1 Indentación

La regla más sagrada de Python.

> > "Use 4 spaces per indentation level."

*   **¿Por qué?** Los espacios son consistentes en todos los editores y sistemas, mientras que los tabuladores pueden tener anchos variables (2, 4, 8 espacios), rompiendo la alineación visual.
*   **Nivel Senior:** Nunca mezcles tabuladores y espacios. Las versiones modernas de Python lanzarán un `TabError`. Configura tu editor para que la tecla `Tab` inserte 4 espacios.

#### 3.1.2 Longitud de Línea

> > "Limit all lines to a maximum of 79 characters."
> > "For flowing long blocks of text with fewer structural restrictions (docstrings or comments), the line length should be limited to 72 characters."

*   **¿Por qué?** Facilita la visualización de múltiples archivos uno al lado del otro y evita el "line wrapping" (salto de línea automático del editor) que puede ser confuso. El límite de 72 para texto ayuda a que no se desborde en terminales estándar.
*   **Nivel Senior:** Aunque los monitores modernos son anchos, esta regla sigue siendo valiosa para revisiones de código en herramientas como GitHub/GitLab y para mantener la densidad de información bajo control. Si una línea es demasiado larga, probablemente esté haciendo demasiadas cosas. Es una señal para refactorizar.

**¿Cómo romper líneas largas?** La forma preferida es usando los paréntesis, corchetes o llaves de Python.

```python
# ✅ Bien: Ruptura implícita dentro de paréntesis
def my_function(
        param_1, param_2,
        param_3, param_4):
    return param_1 + param_2 + param_3 + param_4

# ✅ Bien: También se puede alinear con el paréntesis de apertura
my_list = [
    1, 2, 3,
    4, 5, 6,
]

# ❌ Mal: Usar la barra invertida (\) es posible, pero menos preferido
print('Esto es una línea muy larga que necesita ser rota ' \
      'usando una barra invertida.')
```

#### 3.1.3 Líneas en Blanco

Usa las líneas en blanco para separar bloques lógicos de código, como si fueran párrafos en un texto.
*   **Dos líneas en blanco** para separar funciones de alto nivel y definiciones de clases.
*   **Una línea en blanco** para separar métodos dentro de una clase o bloques lógicos más pequeños dentro de una función.

```python
class MyClass:
    def first_method(self):
        # Bloque lógico 1
        print("Hello")
        a = 1 + 2

        # Bloque lógico 2 (separado por una línea en blanco)
        print("World")
        b = 3 + 4

    def second_method(self):
        ...


# Dos líneas en blanco antes de la siguiente definición
def another_function():
    ...
```

### 3.2 Convenciones de Nomenclatura (Naming Conventions)

La elección de nombres es una de las cosas más difíciles y más importantes en programación.

> > "The naming conventions of Python's library are a bit of a mess, so we'll never get this completely consistent -- nevertheless, here are the currently recommended naming standards."

| Tipo | Convención | Ejemplo |
| :--- | :--- | :--- |
| Módulos | `short_lowercase` | `my_module.py` |
| Paquetes | `short_lowercase` | `my_package` |
| Clases | `CapWords` (o `PascalCase`) | `MyClass`, `ModelView` |
| Funciones | `lowercase_with_underscores` | `my_function()` |
| Variables | `lowercase_with_underscores` | `my_variable` |
| Constantes | `ALL_CAPS_WITH_UNDERSCORES` | `MAX_OVERFLOW`, `PI` |

#### Nombres con Guiones Bajos (Underscores)

Esto es crucial y separa a los que entienden la encapsulación en Python de los que no.

*   `_single_leading_underscore`: **Uso interno**. Es una convención para indicar que una variable o método no debe ser accedido desde fuera de la clase/módulo. No es forzado por el intérprete (excepto en `from module import *`).
    ```python
    class MyClass:
        def _internal_method(self):
            # No deberías llamar a esto desde fuera
            pass
    ```
*   `__double_leading_underscore`: **Name Mangling**. El intérprete de Python renombra el atributo para evitar colisiones de nombres en subclases. Si tienes un atributo `__my_var` en `MyClass`, se convierte en `_MyClass__my_var`.
    ```python
    class MyClass:
        def __init__(self):
            self.__mangled = "I am mangled"

    # >>> obj = MyClass()
    # >>> obj.__mangled  # AttributeError
    # >>> obj._MyClass__mangled  # 'I am mangled'
    ```
*   `__double_leading_and_trailing_underscore__`: **Métodos "mágicos" o "dunder"**. Nombres reservados por Python para operaciones especiales. Nunca crees tus propios nombres `__like_this__`; solo úsalos como está documentado (ej. `__init__`, `__str__`, `__add__`).

### 3.3 Comentarios y Docstrings

Los comentarios explican el *porqué* (la intención), no el *qué* (la implementación).

> > "Comments that contradict the code are worse than no comments. Always make a priority of keeping the comments up-to-date when the code changes!"

#### 3.3.1 Block Comments

Se aplican a un bloque de código que les sigue. Deben estar indentados al mismo nivel.

```python
# Este bucle itera sobre los resultados para encontrar un valor específico.
# Se eligió este enfoque por su simplicidad, a pesar de ser O(n).
for item in results:
    if item.is_valid():
        ...
```

#### 3.3.2 Inline Comments

Úsalos con moderación.

> > "An inline comment is a comment on the same line as a statement. Inline comments should be separated by at least two spaces from the statement."

```python
x = x + 1  # Compensar el offset
```

#### 3.3.3 Docstrings

**¡Esto es fundamental!** Todas las funciones, módulos, clases y métodos públicos deben tener un docstring. PEP 257 es el PEP específico para convenciones de docstrings.

> > "The docstring is a phrase ending in a period. It prescribes the function or method's effect as a command ("Do this", "Return that"), not as a description; e.g. don't write "Returns the square of x.""

```python
def calculate_area(radius):
    """Calculate the area of a circle given its radius.

    Args:
        radius (float): The radius of the circle. Must be a non-negative number.

    Returns:
        float: The area of the circle.

    Raises:
        ValueError: If the radius is negative.
    """
    if radius < 0:
        raise ValueError("Radius cannot be negative.")
    return 3.14159 * radius ** 2
```

### 3.4 Espacios en Blanco en Expresiones y Sentencias

La regla general es usar espacios alrededor de la mayoría de los operadores, pero no abusar de ellos.

#### 3.4.1 Sí usar espacios:

*   Alrededor de operadores binarios: `=`, `+=`, `==`, `<`, `+`, `-`, `*`, `/`, `in`, `is`, etc.
*   Después de comas `,`, punto y coma `;` o dos puntos `:`.

```python
# ✅ Bien
x = 1
y = 2
if x > 5 and y is not None:
    print(x, y)
my_list[1:3]

# ❌ Mal
x=1
y =2
if x>5 and y is not None:
    print(x,y)
my_list[1 : 3]
```

#### 3.4.2 No usar espacios:

*   Inmediatamente dentro de paréntesis, corchetes o llaves.
*   Inmediatamente antes de una coma.
*   Alrededor del `=` en argumentos de palabra clave o valores por defecto.

```python
# ✅ Bien
my_function(arg1, arg2=True)
my_dict = {'key': 'value'}
my_list = [1, 2, 3]

# ❌ Mal
my_function( arg1, arg2 = True )
my_dict = { 'key' : 'value' }
my_list = [ 1, 2, 3 ]
```

### 3.5 Importaciones (Imports)

> > "Imports should usually be on separate lines."

```python
# ✅ Bien
import os
import sys

# ❌ Mal
import os, sys
```

> > "Imports are always put at the top of the file, just after any module comments and docstrings, and before module globals and constants."

El orden de los imports debe ser:
1.  **Librerías estándar** (ej. `sys`, `os`, `math`).
2.  **Librerías de terceros** (ej. `numpy`, `requests`, `django`).
3.  **Librerías de tu propia aplicación** (imports locales).

Separa cada grupo con una línea en blanco.

```python
"""Este es el docstring del módulo."""

import os
from subprocess import Popen

import numpy as np
import requests

from my_project.core import utils
from my_project.models import User
```

### 3.6 Recomendaciones de Programación

PEP 8 también ofrece consejos que van más allá del estilo.

*   **Comparaciones con singletons como `None`:** Usa `is` o `is not`, no `==` o `!=`. `is` comprueba la identidad del objeto, que es lo que quieres con un singleton.

    ```python
    # ✅ Bien
    if my_var is not None:
        ...

    # ❌ Mal
    if my_var != None:
        ...
    ```

*   **Comprobaciones de booleanos:** No compares directamente con `True` o `False`.

    ```python
    # ✅ Bien
    if my_list:  # Aprovecha la "truthiness" de los objetos
        ...
    if not is_validated:
        ...

    # ❌ Mal
    if len(my_list) > 0:
        ...
    if is_validated == False:
        ...
    ```

*   **Uso de `startswith()` y `endswith()`:** En lugar de hacer slicing de strings.

    ```python
    # ✅ Bien
    if filename.endswith('.py'):
        ...

    # ❌ Mal
    if filename[-3:] == '.py':
        ...
    ```

---

## 4. El Salto a Senior: Cuándo Ignorar PEP 8 (El "Porqué" y el "Cuándo")

Esta es la sección más importante. Un desarrollador senior sabe que las guías de estilo son eso: guías, no leyes inmutables.

La propia PEP 8 lo dice:

> > "But most importantly: know when to be inconsistent -- sometimes the style guide just doesn't apply. When in doubt, use your best judgment. Look at other examples and decide what looks best. And don't hesitate to ask!"

Y la cita clave:

> > "A foolish consistency is the hobgoblin of little minds."

**Principales razones para ignorar una regla de PEP 8:**

1.  **Para mantener la consistencia con el código circundante.** Si te unes a un proyecto que no sigue PEP 8, es a menudo mejor seguir el estilo existente que introducir una mezcla de estilos. El código consistente es más fácil de leer que el código que es "formalmente correcto" pero inconsistente.

2.  **Cuando seguir la regla empeora la legibilidad.** A veces, romper la regla de los 79 caracteres hace que una expresión larga sea mucho más clara que romperla en múltiples líneas de forma artificial. Esto es común en expresiones regulares o URLs largas.

3.  **Compatibilidad con versiones antiguas de Python.** El código debe ser compatible con versiones que no soportan ciertas características más nuevas.

4.  **Cuando el código fue generado automáticamente.** No tiene sentido reformatear el output de una herramienta si se va a regenerar después.

**El proceso mental de un senior:**
"Ok, esta línea tiene 85 caracteres. La regla dice 79. ¿Puedo romperla de forma limpia? Si la rompo, ¿la lógica se vuelve más difícil de seguir? Si la respuesta es sí, entonces la dejo como está y quizás añado un comentario `# noqa` para que las herramientas automáticas la ignoren, explicando por qué."

---

## 5. Herramientas del Oficio: Automatización de PEP 8

Un senior no pierde tiempo formateando código manualmente. Usa herramientas para automatizar el proceso y centrarse en la lógica.

*   **Linters (Analizadores estáticos):** Revisan tu código en busca de errores y violaciones de estilo sin ejecutarlo.
    *   `flake8`: Combina `pycodestyle` (el checker de PEP 8), `pyflakes` (detector de errores) y `mccabe` (complejidad ciclomática). Es el estándar de facto.
    *   `pylint`: Mucho más exhaustivo y configurable. Puede ser ruidoso al principio, pero es extremadamente potente.

*   **Formatters (Formateadores automáticos):** Reescriben tu código para que cumpla con un estilo determinado. Esto elimina los debates sobre estilo en el equipo.
    *   `black`: "The Uncompromising Code Formatter". Es muy dogmático. No tiene apenas configuración. Lo formateas con `black` y listo. Elimina todas las discusiones de estilo. Muy popular en equipos modernos.
    *   `autopep8`: Formatea el código para que cumpla específicamente con PEP 8. Es menos dogmático que `black`.
    *   `isort`: Una herramienta especializada que ordena tus imports automáticamente según las reglas de PEP 8.

**Flujo de trabajo de un senior:**
1.  Configura estas herramientas en su editor (VS Code, PyCharm, etc.) para que se ejecuten al guardar el archivo.
2.  Configura un "pre-commit hook" para que `flake8` y `black` se ejecuten antes de cada `git commit`. Esto asegura que ningún código que no cumpla con el estilo llegue al repositorio.
3.  El equipo acuerda las reglas (ej. en un archivo `pyproject.toml` o `.flake8`) y deja que las herramientas hagan el trabajo sucio.

---

## 6. Conclusión: PEP 8 como Lenguaje Común

Dominar PEP 8 no es sobre ser pedante con los espacios en blanco. Es sobre **comunicación, profesionalismo y respeto** por tus compañeros.

*   **Es comunicación:** Hablas un dialecto de Python que todos en la comunidad entienden.
*   **Es profesionalismo:** Demuestra que te preocupas por la calidad y la mantenibilidad a largo plazo de tu trabajo.
*   **Es respeto:** Haces que la vida de la siguiente persona que tenga que leer tu código (que podrías ser tú mismo dentro de 6 meses) sea mucho más fácil.

Al internalizar no solo las reglas de PEP 8, sino su espíritu, dejas de pensar en ellas y simplemente escribes código limpio y legible de forma natural. Ese es un verdadero rasgo de un desarrollador de Python senior.
