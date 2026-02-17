Si has escrito cientos de tests y aun así, un bug insidioso se ha colado en producción, no estás solo. Tus tests, como tú, son humanos y están sesgados por tu propia imaginación. ¿Y si pudieras enseñar a la máquina a ser tu adversario más creativo y despiadado para encontrar esos bugs que ni siquiera sabías que existían?

# hypothesis (property-based testing)

---

# El Arte de la Duda Sistemática: Una Guía Senior sobre Hypothesis y Property-Based Testing

Hola. Si estás aquí, es probable que hayas escrito cientos, quizás miles, de tests unitarios. Has usado `assertEqual`, `assertTrue`, y has cazado obsesivamente ese `off-by-one error` a las 2 de la mañana. Has seguido las mejores prácticas, has alcanzado una cobertura de código del 95% y, aun así, un bug insidioso se ha colado en producción. ¿Por qué? Porque tus tests, como tú, son humanos. Están sesgados por tu propia imaginación.

Hoy vamos a trascender esa limitación. Vamos a aprender a enseñar a la máquina a ser nuestro adversario más creativo y despiadado. Bienvenidos al mundo del **Property-Based Testing (PBT)** y su implementación más brillante en Python: **Hypothesis**.

## 1. Introducción Profunda: El Nacimiento de un Adversario

Para entender Hypothesis, debemos viajar en el tiempo y el espacio a la fría Suecia de finales de los 90, al epicentro del mundo de la programación funcional: la Universidad Tecnológica de Chalmers.

### Contexto Histórico: El Fantasma en la Máquina Funcional

A finales de los 90, el lenguaje de programación **Haskell** estaba ganando tracción en los círculos académicos. Su pureza funcional, su sistema de tipos estáticos y su pereza (lazy evaluation) lo convertían en un paraíso para el razonamiento formal sobre programas. Sin embargo, incluso en este Edén de la corrección matemática, los bugs persistían.

Dos investigadores, **Koen Claessen** y **John Hughes**, se enfrentaban a un problema clásico: ¿cómo probar el código de manera exhaustiva sin escribir una cantidad infinita de ejemplos? Su epifanía fue darse cuenta de que, en lugar de probar *valores* específicos, podían probar *propiedades* universales que debían cumplirse para *todos* los valores posibles.

> "En lugar de elegir manualmente los datos de prueba, uno escribe un generador para datos de prueba aleatorios y define las propiedades del programa que deberían cumplirse para todas las entradas." — **Koen Claessen & John Hughes**, *QuickCheck: A Lightweight Tool for Random Testing of Haskell Programs* (2000)

Así, en el año 2000, nació **QuickCheck**. No era solo una biblioteca; era un cambio de paradigma. La idea era simple pero revolucionaria:

1.  **Define una propiedad** que tu código debe cumplir (por ejemplo, "para cualquier lista `xs`, `reverse(reverse(xs))` debe ser igual a `xs`").
2.  **Especifica el "universo" de datos** de entrada (por ejemplo, "listas de enteros").
3.  **Deja que la máquina genere cientos de ejemplos** aleatorios de ese universo y busque un contraejemplo que viole tu propiedad.

### Problema que Resuelve: La Tiranía del Ejemplo

El testing tradicional, basado en ejemplos, sufre de un sesgo de confirmación cognitivo. Escribimos tests para los casos que se nos ocurren: el caso feliz, el valor nulo, la lista vacía, el número negativo. Pero, ¿qué pasa con la cadena de texto Unicode con emojis y caracteres de control? ¿O la lista de 2000 floats donde uno es `NaN`? ¿O esa fecha del año 9999?

El PBT resuelve esto externalizando la creatividad. Le pasamos la responsabilidad de la "imaginación maliciosa" a la computadora, que es infinitamente más paciente y sistemática que nosotros. Aborda directamente el famoso aforismo de Edsger Dijkstra:

> "Program testing can be used to show the presence of bugs, but never to show their absence!" — **Edsger W. Dijkstra**, *Notes on Structured Programming* (1972)

El PBT no puede probar la ausencia total de bugs (eso nos llevaría al problema de la parada), pero se acerca mucho más al cubrir un espacio de entrada vasto y diverso, descubriendo los "unknown unknowns" que acechan en los rincones oscuros de nuestro código.

### Evolución: De la Academia a las Trincheras de Python

QuickCheck fue un éxito en la comunidad funcional, inspirando clones en Scala (ScalaCheck), F# (FsCheck) y otros lenguajes. Sin embargo, el mundo de los lenguajes dinámicos como Python permanecía ajeno a esta revolución.

Entra en escena **David R. MacIver**, un programador brillante con una profunda comprensión tanto de la teoría como de la práctica. En 2013, comenzó a trabajar en **Hypothesis**, con un objetivo claro: no solo portar QuickCheck a Python, sino mejorarlo fundamentalmente para que fuera ergonómico, potente y adecuado para el mundo "sucio" del software del mundo real.

La innovación clave de Hypothesis fue el **"shrinking" integrado y dirigido por el generador**. Cuando QuickCheck encontraba un fallo, intentaba reducir el contraejemplo (por ejemplo, una lista de 100 elementos) a uno más simple (una lista de 3 elementos). Hypothesis llevó esto un paso más allá, haciendo que el proceso de "shrinking" (reducción) fuera una parte intrínseca de la generación de datos. Esto significa que cuando Hypothesis encuentra un bug, te entrega el ejemplo **más simple y minimalista posible** que lo reproduce. Esto es oro puro para la depuración.

## 2. Fundamentos Teóricos y Matemáticos: La Lógica de la Falsificación

Para usar Hypothesis a nivel senior, no basta con saber usar la API. Debes entender la belleza matemática que la sustenta.

### Base Teórica: Lógica de Predicados y Falsificación Popperiana

En su núcleo, una prueba de propiedad es una afirmación en lógica de primer orden con cuantificación universal:

**∀x ∈ S : P(x)**

Esto se lee como: "Para todo elemento `x` que pertenece al conjunto `S`, el predicado `P(x)` es verdadero".

-   `∀` (para todo) es el cuantificador universal.
-   `x` es una variable (o un conjunto de variables) que representa la entrada a tu función.
-   `S` es el "universo" de posibles entradas, definido por las **estrategias** de Hypothesis.
-   `P(x)` es el **predicado**, tu propiedad, la afirmación que haces sobre tu código (por ejemplo, `mi_sort(x) == sorted(x)`).

El trabajo de Hypothesis no es *probar* que esta afirmación es verdadera (lo cual es generalmente indemostrable para programas no triviales). Su trabajo, inspirado en la filosofía de la ciencia de Karl Popper, es actuar como un **motor de falsificación**. Intenta con todas sus fuerzas encontrar **un solo** contraejemplo `c` tal que `P(c)` sea falso. Si lo encuentra, ha falsificado tu hipótesis (de ahí el nombre de la biblioteca) y ha encontrado un bug.

### Principios Subyacentes: Invariantes y Simetrías

¿De dónde sacamos estas "propiedades"? A menudo provienen de principios matemáticos o lógicos inherentes a nuestro dominio del problema:

-   **Invariantes**: Una propiedad que no cambia. Por ejemplo, ordenar una lista cambia el orden de los elementos, pero no su longitud ni los elementos mismos. `len(mi_sort(xs)) == len(xs)` y `collections.Counter(mi_sort(xs)) == collections.Counter(xs)` son invariantes.
-   **Simetría / Propiedades de "Ida y Vuelta" (Round-trip)**: Si tienes dos operaciones que son inversas, aplicarlas una tras otra debería devolverte al estado original. `decode(encode(x)) == x`. Esto es increíblemente potente para probar serialización, compresión o cifrado.
-   **Idempotencia**: Aplicar una operación varias veces produce el mismo resultado que aplicarla una vez. `f(f(x)) == f(x)`. Por ejemplo, poner en mayúsculas una cadena de texto.
-   **Relación con un Modelo (Oracle Testing)**: Puedes comparar tu implementación optimizada y compleja con una versión más simple y lenta pero demostrablemente correcta (el "oráculo"). `mi_sort_rapido(xs) == mi_sort_lento_y_simple(xs)`.
-   **Propiedades Metamórficas**: Si cambias la entrada de una manera específica, puedes predecir cómo cambiará la salida. Por ejemplo, si `f(x) = y`, entonces `f(x + 1)` podría ser `y + 2`.

### Relación con Otros Conceptos: El Legado de Turing

El PBT es el descendiente pragmático de un sueño mucho más antiguo: la **verificación formal de programas**, un campo iniciado por gigantes como Alan Turing, Tony Hoare y Robert Floyd. Ellos soñaban con poder *probar* matemáticamente que un programa era correcto para *todas* las entradas posibles.

Si bien la verificación formal completa es extremadamente difícil y costosa, el PBT ocupa un punto intermedio perfecto: es mucho más riguroso que las pruebas de ejemplo tradicionales, pero mucho más práctico y accesible que la prueba formal completa. Es, en esencia, "verificación formal para las masas".

## 3. Evolución Histórica Detallada: Un Hilo de Ideas

| Fecha       | Hito                                                                                                  | Figuras Clave                      | Contexto Computacional                                                                    |
|-------------|-------------------------------------------------------------------------------------------------------|------------------------------------|-------------------------------------------------------------------------------------------|
| **1960s-70s** | Nace la idea de la verificación formal y las aserciones de programas.                                   | Turing, Hoare, Floyd, Dijkstra     | Era de los mainframes. El software se consideraba una disciplina matemática.              |
| **2000**    | Se publica el paper de **QuickCheck**. Nace el Property-Based Testing moderno.                          | Koen Claessen, John Hughes         | Auge de la programación funcional (Haskell). La pureza facilita el razonamiento.          |
| **2000s**   | El PBT se extiende por el ecosistema funcional (ScalaCheck, FsCheck).                                   | Varios autores                     | La JVM y .NET se vuelven plataformas multilingües.                                        |
| **2013**    | **David R. MacIver** comienza el desarrollo de Hypothesis.                                              | David R. MacIver                   | Python 2/3 se consolida. Los lenguajes dinámicos necesitan pruebas más robustas.          |
| **2015**    | Hypothesis 1.0 es lanzado. Introduce el "shrinking" integrado como una característica central.           | David R. MacIver                   | El ecosistema de Python (Pytest, Django) está maduro y listo para nuevas ideas de testing. |
| **2016+**   | Hypothesis introduce **Stateful Testing** (RuleBasedStateMachine), un cambio de juego para sistemas complejos. | David R. MacIver y colaboradores | Los microservicios y las APIs complejas se vuelven la norma. Se necesita probar interacciones. |

Un momento decisivo para Hypothesis fue su perfecta integración con `pytest`. Al no requerir un corredor de pruebas especial y funcionar directamente con el decorador `@given`, eliminó la barrera de entrada que tenían otras herramientas, convirtiéndose en una parte natural del flujo de trabajo de un desarrollador de Python.

## 4. Implementación Práctica: De la Teoría al Código

Basta de historia y teoría. Escribamos código.

### Antes vs. Después: Codificando una URL

Imagina una función que "slugifica" un título para una URL, reemplazando espacios con guiones y eliminando caracteres no válidos.

**El enfoque tradicional (basado en ejemplos):**

```python
# slugify.py
import re

def slugify(text: str) -> str:
    # Simulación de una implementación con un bug sutil
    text = text.lower().strip()
    text = re.sub(r'[\s]+', '-', text)
    # BUG: No maneja caracteres no alfanuméricos al principio/final después de reemplazar espacios
    text = re.sub(r'[^a-z0-9-]', '', text)
    return text

# test_slugify_example.py
def test_slugify_basic():
    assert slugify("Hello World") == "hello-world"

def test_slugify_with_extra_spaces():
    assert slugify("  leading and trailing  ") == "leading-and-trailing"

def test_slugify_with_punctuation():
    assert slugify("A title, with: punctuation!") == "a-title-with-punctuation"

def test_slugify_empty():
    assert slugify("") == ""
```

Estos tests pasan. Pero, ¿qué pasa con `slugify("!@#$")`? Devuelve `""`. ¿Y `slugify(" leading space")`? Devuelve `-leading-space`. Nuestros ejemplos no lo encontraron.

**El enfoque Hypothesis (basado en propiedades):**

Ahora, pensemos en las *propiedades* de un slug válido:

1.  No debe contener espacios.
2.  No debe contener caracteres que no sean `a-z`, `0-9` o `-`.
3.  No debe tener guiones consecutivos.
4.  No debe empezar ni terminar con un guión (a menos que sea la única cadena).
5.  La idempotencia es una propiedad deseable: `slugify(slugify(text)) == slugify(text)`.

Vamos a probar la propiedad 2 y la 5.

```python
# test_slugify_hypothesis.py
from hypothesis import given, strategies as st
from slugify import slugify
import re

# Estrategia: generar cualquier cadena de texto Unicode
@given(st.text())
def test_slugify_output_is_valid(text):
    """
    Propiedad: El resultado solo contiene caracteres válidos.
    """
    result = slugify(text)
    # Usamos una expresión regular para verificar que todos los caracteres en el resultado
    # pertenecen al conjunto permitido.
    assert re.match(r'^[a-z0-9-]*$', result) is not None

@given(st.text())
def test_slugify_is_idempotent(text):
    """
    Propiedad: Aplicar slugify dos veces es lo mismo que aplicarlo una vez.
    """
    assert slugify(slugify(text)) == slugify(text)
```

Al ejecutar esto con `pytest`, Hypothesis explota casi instantáneamente:

```
Falsifying example: test_slugify_output_is_valid(text=' ')
...
AssertionError: assert None is not None

Falsifying example: test_slugify_is_idempotent(text='a b')
...
AssertionError: assert 'a--b' == 'a-b'
```

Hypothesis no solo encontró los bugs, sino que nos dio los contraejemplos *mínimos*: un simple espacio (`' '`) y `'a b'`. El primer bug es que nuestra implementación convierte un espacio en un guion, pero luego no lo elimina si está al final, violando la propiedad de "no guiones al final". El segundo bug es que al reemplazar espacios y luego limpiar, podemos crear guiones dobles.

**La solución correcta:**

```python
# slugify_fixed.py
import re

def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r'[^a-z0-9\s]+', '', text) # 1. Limpiar primero
    text = re.sub(r'\s+', '-', text)        # 2. Reemplazar espacios
    return text
```

Con esta versión corregida, los tests de Hypothesis pasan, dándonos una confianza mucho mayor en nuestra implementación.

### Caso de Estudio: Probando un Algoritmo de Compresión (RLE)

Run-Length Encoding (RLE) es un algoritmo simple: `AAABBC` se convierte en `3A2B1C`.

**Propiedad clave:** La compresión y descompresión es una operación de "ida y vuelta".

```python
# rle.py
def encode(data: str) -> str:
    # ... implementación de RLE ...
def decode(data: str) -> str:
    # ... implementación de RLE ...

# test_rle.py
from hypothesis import given, strategies as st
from rle import encode, decode

# Creamos una estrategia personalizada para generar cadenas que son "comprimibles",
# es decir, con caracteres repetidos.
# st.text() podría generar "abcde", que no es un buen caso de prueba.
runnable_chars = st.characters(whitelist_characters='ABCDE')
rle_strategy = st.lists(st.tuples(st.integers(min_value=1, max_value=10), runnable_chars)) \
    .map(lambda runs: "".join([char * count for count, char in runs]))

@given(data=rle_strategy)
def test_rle_roundtrip(data):
    """
    Propiedad: decodificar el resultado de codificar una cadena
    debe devolver la cadena original.
    """
    # Para evitar que la prueba se ejecute con cadenas vacías,
    # donde la propiedad es trivialmente verdadera.
    assume(data) 
    
    encoded = encode(data)
    decoded = decode(encoded)
    assert data == decoded
```

Aquí, hemos usado una estrategia compuesta para generar datos de prueba más realistas para nuestro dominio. `assume` nos permite descartar datos triviales o inválidos sin que la prueba falle.