Todos conocemos ese escalofrío al cambiar código antiguo, esperando no romper algo sin darnos cuenta.
Esa "entropía del software" es un problema real, pero tiene solución.
Vamos a ver cómo construir una red de seguridad que nos permita programar y refactorizar sin miedo.

# Unit Testing (unittest, pytest)


---

## La Guía Definitiva del Unit Testing: De Artesano a Maestro

### 1. Introducción Profunda: El Pulso del Software Confiable

Imagina por un momento el programa Apolo. Cientos de miles de líneas de código escritas en un lenguaje ensamblador primitivo, controlando el destino de tres astronautas a 380,000 kilómetros de casa. El software *tenía* que funcionar. No había `git pull` para un hotfix. La confianza en ese código no nació de la esperanza, sino de una disciplina rigurosa de verificación. Aunque el "Unit Testing" formal como lo conocemos hoy no existía, su espíritu sí: la descomposición de un problema masivo en partes verificables.

> "El software del Apolo fue tejido. Literalmente, por costureras en las fábricas de Raytheon. La memoria era 'core rope memory'. Si había un error, tenían que deshacer el tejido y volver a tejerlo. No había margen para el error." — Anécdota de la historia de la computación, a menudo atribuida a Margaret Hamilton y su equipo.

**Contexto Histórico y el Problema que Resuelve**

El concepto moderno de Unit Testing tiene un padre claro: **Kent Beck**. A mediados de la década de 1990, mientras trabajaba en el entorno de programación **Smalltalk**, un lenguaje puramente orientado a objetos que fomentaba la experimentación rápida, Beck desarrolló un framework llamado **SUnit**. Su motivación no era académica, sino profundamente pragmática.

El problema era, y sigue siendo, la **entropía del software**. A medida que un sistema crece, su complejidad aumenta exponencialmente. Un pequeño cambio en una parte del código puede causar fallos catastróficos e inesperados en otra. Este fenómeno, conocido como "regresión", era la pesadilla de los desarrolladores. El ciclo de desarrollo era lento y aterrador: programar durante semanas, luego pasar semanas o meses en una fase de "testing y estabilización" donde los bugs se cazaban como en un safari impredecible.

Kent Beck se preguntó: ¿Y si pudiéramos obtener retroalimentación *instantánea*? ¿Y si pudiéramos construir una red de seguridad que nos permitiera refactorizar y añadir funcionalidades con audacia, sabiendo que no hemos roto nada?

**La solución fue el Unit Testing:** la práctica de escribir código para verificar pequeñas "unidades" aisladas de nuestro código de producción (generalmente una función o un método).

**Evolución: De SUnit a la Pluralidad Moderna**

1.  **SUnit (Smalltalk, ~1994):** El origen. Kent Beck crea el primer framework de la familia "xUnit". Establece el patrón: `setUp`, `tearDown`, tests como métodos, y aserciones para verificar resultados.
2.  **JUnit (Java, 1997):** Kent Beck y **Erich Gamma** (uno de la "Gang of Four" del famoso libro de patrones de diseño) portan SUnit a Java durante un vuelo transatlántico. JUnit se convierte en el estándar de facto y populariza masivamente el Unit Testing en el mundo del desarrollo empresarial. Su estructura de clases y herencia influyó en una generación de frameworks.
3.  **PyUnit / `unittest` (Python, 2001):** Python, necesitando una solución robusta, adopta una versión portada de JUnit, originalmente llamada PyUnit, que se incluye en la librería estándar como el módulo `unittest`. Trajo la potencia y el patrón de JUnit al ecosistema Python.
4.  **La "Rebelión" Pythonica: `pytest` (iniciado como `py.test` por Holger Krekel, ~2004):** A medida que la comunidad de Python maduraba, el estilo verboso y basado en clases de `unittest` (heredado de Java) empezó a sentirse... poco "pythonico". `pytest` surgió como una alternativa que abrazaba la simplicidad de Python: usa funciones normales, aserciones `assert` nativas y un sistema revolucionario de inyección de dependencias llamado *fixtures*. Hoy, es el estándar de facto en la comunidad.

### 2. Fundamentos Teóricos y Matemáticos: La Ciencia de la Confianza

Aunque el Unit Testing parece una simple práctica de ingeniería, sus raíces se hunden en principios más profundos de la computación y la lógica.

**Base Teórica: Verificación Formal vs. Verificación Empírica**

En un mundo ideal, usaríamos la **verificación formal**: pruebas matemáticas para demostrar que nuestro software es correcto para *todas* las entradas posibles. Esto es lo que se hace en sistemas de misión crítica (aviónica, medicina). Sin embargo, es extraordinariamente difícil, costoso y no escala para la mayoría de las aplicaciones comerciales.

El Unit Testing es una forma de **verificación empírica**. Es una aplicación del método científico al código:
1.  **Hipótesis:** "Mi función `sumar(a, b)` devuelve correctamente la suma de `a` y `b`."
2.  **Experimento:** Escribir un test: `assert sumar(2, 3) == 5`.
3.  **Observación:** El test pasa o falla.
4.  **Teoría (provisional):** Si suficientes experimentos (tests) con entradas bien elegidas pasan, ganamos confianza en que nuestra hipótesis es correcta.

> "Program testing can be used to show the presence of bugs, but never to show their absence!" — **Edsger W. Dijkstra**, *Notes on Structured Programming* (1972)

Esta cita icónica de Dijkstra es el corazón filosófico del testing. Nunca podemos probar que un programa es 100% correcto con tests, pero podemos reducir drásticamente la probabilidad de que esté incorrecto.

**Principios Subyacentes**

*   **Modularidad y Ocultación de Información:** El concepto de "unidad" es posible gracias a los principios de diseño de software articulados por **David Parnas** en los 70. Un sistema bien diseñado se compone de módulos con interfaces claras que ocultan su complejidad interna. Solo así podemos testear un "módulo" de forma aislada.
*   **Partición de Equivalencia y Análisis de Valores Límite:** ¿Cómo elegimos qué testear? No podemos probar todos los números. Aquí entran conceptos de la matemática discreta.
    *   **Partición de Equivalencia:** Dividimos las posibles entradas en grupos (particiones) donde el programa se comporta de manera similar. Por ejemplo, para una función que valida la edad de un mayor de edad, las particiones son: `edad < 0` (inválido), `0 <= edad < 18` (menor), `edad >= 18` (mayor). Solo necesitamos un test por partición.
    *   **Análisis de Valores Límite:** Los errores suelen ocurrir en los bordes de estas particiones. Por tanto, testeamos los valores límite: `17`, `18`, `19`, y también `-1`, `0`.

### 3. Evolución Histórica Detallada: Una Narrativa de la Calidad

| Año | Evento Decisivo | Figuras Clave | Contexto Computacional |
| :--- | :--- | :--- | :--- |
| **1947** | Se documenta el primer "bug" real. | Grace Hopper | La computación era mecánica, los "bugs" eran literales (una polilla en un relé del Mark II). |
| **1972** | Dijkstra publica "Notes on Structured Programming". | Edsger Dijkstra | Crisis del software. Los proyectos eran caóticos. Nace la ingeniería de software como disciplina. |
| **1972** | Parnas publica "On the Criteria To Be Used..." | David Parnas | Se establecen las bases teóricas de la modularidad, sin la cual el testing de unidades es imposible. |
| **~1994** | Creación de SUnit para Smalltalk. | Kent Beck | Auge de la Programación Orientada a Objetos. Entornos de desarrollo rápidos y dinámicos. |
| **1997** | Creación de JUnit para Java. | Kent Beck, Erich Gamma | Java está explotando en popularidad. La necesidad de herramientas profesionales es masiva. |
| **1999** | Beck publica "Extreme Programming Explained". | Kent Beck | Se formaliza el Test-Driven Development (TDD), colocando el Unit Testing en el centro del ciclo de desarrollo. |
| **2001** | `unittest` se añade a la librería estándar de Python. | Steve Purcell (autor original de PyUnit) | Python está ganando tracción como un lenguaje de scripting y desarrollo de aplicaciones serio. |
| **~2004** | Nace `pytest`. | Holger Krekel | La comunidad Python busca herramientas más idiomáticas y menos verbosas. El "Zen de Python" influye en el diseño de herramientas. |
| **Hoy** | `pytest` es el rey. | Comunidad Open Source | Ecosistemas maduros de CI/CD, DevOps. El testing automatizado es una expectativa, no un lujo. |

### 4. Implementación Práctica: Del Código a la Confianza

Vamos a modelar una clase simple que gestiona el inventario de una tienda.

```python
# src/inventory.py
class InsufficientStockError(Exception):
    """Excepción para cuando no hay suficiente stock."""
    pass

class Inventory:
    def __init__(self, initial_stock: dict[str, int] | None = None):
        self._stock = initial_stock if initial_stock is not None else {}

    def add_stock(self, item: str, quantity: int):
        if quantity <= 0:
            raise ValueError("La cantidad debe ser positiva.")
        self._stock[item] = self._stock.get(item, 0) + quantity

    def remove_stock(self, item: str, quantity: int):
        if quantity <= 0:
            raise ValueError("La cantidad debe ser positiva.")
        if item not in self._stock or self._stock[item] < quantity:
            raise InsufficientStockError(f"No hay suficiente stock de {item}.")
        self._stock[item] -= quantity

    def get_stock(self, item: str) -> int:
        return self._stock.get(item, 0)
```

#### 4.1. El Estilo Clásico: `unittest`

Este estilo es verboso, estructurado y explícito. Es el descendiente directo de JUnit.

```python
# tests/test_inventory_unittest.py
import unittest
from src.inventory import Inventory, InsufficientStockError

# Heredamos de unittest.TestCase, que nos da las herramientas de aserción.
class TestInventory(unittest.TestCase):

    # El método setUp se ejecuta ANTES de cada test. Ideal para crear objetos frescos.
    def setUp(self):
        print("\n[unittest] Setting up for a new test...")
        self.inventory = Inventory()
        self.inventory.add_stock("manzana", 10)

    # Los métodos de test DEBEN empezar con 'test_'.
    def test_add_stock_successfully(self):
        """Verifica que añadir stock funciona correctamente."""
        self.inventory.add_stock("pera", 5)
        # Usamos los métodos de aserción específicos: assertEqual, assertTrue, etc.
        self.assertEqual(self.inventory.get_stock("pera"), 5)

    def test_remove_stock_successfully(self):
        """Verifica que quitar stock funciona si hay suficiente."""
        self.inventory.remove_stock("manzana", 3)
        self.assertEqual(self.inventory.get_stock("manzana"), 7)

    def test_remove_too_much_stock_raises_error(self):
        """Verifica que se lanza una excepción si se intenta quitar demasiado stock."""
        # El context manager assertRaises verifica que el código dentro del 'with'
        # lanza la excepción esperada.
        with self.assertRaises(InsufficientStockError):
            self.inventory.remove_stock("manzana", 20)

    def test_add_negative_stock_raises_error(self):
        """Verifica que no se puede añadir una cantidad negativa."""
        with self.assertRaises(ValueError):
            self.inventory.add_stock("manzana", -5)
    
    # El método tearDown se ejecuta DESPUÉS de cada test. Ideal para limpieza.
    def tearDown(self):
        print("[unittest] Tearing down the test.")

# Para ejecutarlo desde la línea de comandos
if __name__ == '__main__':
    unittest.main()
```

**Análisis `unittest` (Bien vs. Mal):**
*   **Bien:** Estructura muy clara, parte de la librería estándar (sin dependencias), ideal para quienes vienen de Java/JUnit.
*   **Mal:** Mucho *boilerplate* (código repetitivo como `self.`, herencia, nombres de métodos largos). Las aserciones como `assertEqual(a, b)` son menos legibles que `assert a == b`.

#### 4.2. El Enfoque Moderno y Pythonico: `pytest`

`pytest` elimina el boilerplate y utiliza características nativas de Python, haciéndolo más conciso y legible.

```python
# tests/test_inventory_pytest.py
import pytest
from src.inventory import Inventory, InsufficientStockError

# ¡No hay clases! (Aunque se pueden usar). Son solo funciones.
# La magia de pytest está en las 'fixtures'. Una fixture es una función
# que provee datos o estado a nuestros tests.
@pytest.fixture
def inventory():
    """Fixture que crea una instancia de Inventory con stock inicial."""
    print("\n[pytest] Creating inventory fixture...")
    inv = Inventory()
    inv.add_stock("manzana", 10)
    return inv

# Los tests son funciones normales. El nombre de la fixture se pasa como argumento.
# pytest se encarga de la "inyección de dependencias".
def test_add_stock_successfully(inventory):
    """Verifica que añadir stock funciona correctamente."""
    inventory.add_stock("pera", 5)
    # ¡Usamos el 'assert' nativo de Python! pytest lo "potencia" para dar
    # mensajes de error increíblemente detallados.
    assert inventory.get_stock("pera") == 5

def test_remove_stock_successfully(inventory):
    """Verifica que quitar stock funciona si hay suficiente."""
    inventory.remove_stock("manzana", 3)
    assert inventory.get_stock("manzana") == 7

def test_remove_too_much_stock_raises_error(inventory):
    """Verifica que se lanza una excepción si se intenta quitar demasiado stock."""
    # La sintaxis de pytest para excepciones es más limpia.
    with pytest.raises(InsufficientStockError, match="No hay suficiente stock"):
        inventory.remove_stock("manzana", 20)

def test_add_negative_stock_raises_error(inventory):
    """Verifica que no se puede añadir una cantidad negativa."""
    with pytest.raises(ValueError, match="La cantidad debe ser positiva."):
        inventory.add_stock("manzana", -5)
```

**Análisis `pytest` (Antes vs. Después):**
*   **Antes (`unittest`):** Necesitábamos una clase, `setUp`, `self.inventory`, y `self.assertEqual`.
*   **Después (`pytest`):** Una fixture reutilizable y una función simple con un `assert` claro. El código del test se centra en el *comportamiento* a probar, no en la parafernalia del framework.

### 5. Nivel Senior - Conceptos Avanzados

Aquí es donde separamos a los programadores que *usan* tests de los ingenieros que *diseñan* estrategias de testing.

#### 5.1. Aislamiento y Mocks: Probando en el Vacío

Nuestra clase `Inventory` es simple y no depende de nada. Pero, ¿qué pasa si necesita conectarse a una base de datos o a una API externa para obtener los precios? No queremos que nuestros tests unitarios hagan llamadas de red reales. Serían lentos, frágiles (si la red falla, el test falla) y podrían tener efectos secundarios.

La solución es **aislar la unidad bajo prueba** usando **Mocks**. Un mock es un objeto falso que simula el comportamiento de un objeto real.

```python
# Imaginemos que ahora Inventory necesita un servicio de precios
# from src.pricing import get_price_from_api

class Inventory:
    # ... (código anterior) ...
    def get_total_value(self, item: str) -> float:
        # ¡Dependencia externa! ¡Peligro para el unit test!
        price = get_price_from_api(item) 
        quantity = self.get_stock(item)
        return price * quantity

# tests/test_inventory_advanced.py
from unittest.mock import patch
import pytest
# ...

# Usamos el decorador 'patch' de unittest.mock (que funciona perfecto con pytest)
# para reemplazar 'get_price_from_api' con un objeto Mock durante el test.
@patch('src.inventory.get_price_from_api')
def test_get_total_value(mock_get_price, inventory): # El mock se inyecta como argumento
    """Verifica que el valor total se calcula correctamente usando un precio mockeado."""
    # Configuramos el mock: "Cuando te llamen con 'manzana', devuelve 2.5"
    mock_get_price.return_value = 2.5

    # Ejecutamos el código que queremos probar
    value = inventory.get_total_value("manzana")

    # Verificamos que nuestro código llamó al mock como esperábamos
    mock_get_price.assert_called_once_with("manzana")
    
    # Verificamos el resultado final
    # 10 manzanas (de la fixture) * 2.5 (del mock) = 25.0
    assert value == 25.0
```

#### 5.2. Trade-offs y la Pirámide de Pruebas

No todos los tests son iguales. **Martin Fowler** popularizó la "Pirámide de Pruebas", una heurística para pensar sobre la distribución de nuestros tests.

```
      / \
     / E2E \      <-- Pocos, lentos, costosos (Selenium, Cypress)
    /-------\
   / Service \    <-- Más, prueban servicios completos (API tests)
  /-----------\
 / Unit Tests  \  <-- Muchos, rápidos, baratos, aislados
/---------------\
```

*   **Trade-off:** Los tests unitarios son rápidos y dan feedback preciso, pero no garantizan que el sistema completo funcione. Los tests End-to-End (E2E) lo garantizan, pero son lentos, frágiles y difíciles de depurar.
*   **Decisión Senior:** Un ingeniero senior no busca 100% de cobertura en tests unitarios. Busca la estrategia *correcta*. Testea la lógica de negocio compleja con tests unitarios, las interacciones entre servicios con tests de servicio/integración, y los flujos críticos de usuario con unos pocos tests E2E.

**¿Cuándo NO usar Unit Tests?**
*   Para lógica trivial (getters/setters). El test sería más complejo que el código.
*   Para probar librerías de terceros. Confía en que los desarrolladores de `requests` ya han probado su librería. Tú prueba *tu uso* de ella (usando mocks).
*   Cuando un test de integración es más valioso. A veces, probar la interacción real con una base de datos (en un entorno de prueba) da más confianza que mockearla.

#### 5.3. Anti-Patrones: El Camino al Infierno del Testing

1.  **El Cono de Helado:** El anti-patrón de la pirámide. Muchos tests manuales y E2E, pocos unitarios. El desarrollo es lento y doloroso.
2.  **Tests Frágiles (Brittle Tests):** Tests que se rompen con cambios mínimos en la implementación, aunque el comportamiento externo no haya cambiado. Esto ocurre cuando se testean detalles internos en lugar del contrato público de una función/clase.
3.  **El Burlador Excesivo (The Excessive mocker):** Mockear tanto que el test ya no prueba nada del mundo real. El test pasa, pero la aplicación falla en producción porque las interacciones reales son diferentes a las de los mocks.
4.  **El Test Eremita:** Tests que dependen del orden de ejecución o del estado dejado por otro test. Cada test unitario debe ser completamente independiente. Las fixtures de `pytest` con scope `function` ayudan a garantizar esto.

#### 5.4. Más Allá: Property-Based Testing

Este es el siguiente nivel. En lugar de escribir ejemplos individuales, defines las *propiedades* que tu código debe cumplir, y una librería como **`hypothesis`** genera cientos de ejemplos para intentar romperlas.

```python
# tests/test_advanced_properties.py
from hypothesis import given
import hypothesis.strategies as st

def encode_rle(s: str) -> str:
    # Una implementación simple de Run-Length Encoding, ej: "AAABBC" -> "3A2B1C"
    # ... (podría tener bugs en casos extremos)

def decode_rle(s: str) -> str:
    # ...

# En lugar de pensar en casos: "AA", "", "A", "1A"...
# Pensamos en una propiedad fundamental:
# "Si codifico una cadena y luego la decodifico, debo obtener la original."

@given(st.text()) # 'given' un texto generado por hypothesis...
def test_rle_roundtrip_property(s):
    # La propiedad que debe cumplirse siempre.
    assert decode_rle(encode_rle(s)) == s
```

`hypothesis` buscará inteligentemente los casos más problemáticos: strings vacíos, con emojis, con caracteres de control, muy largos, etc. Es como tener un QA increíblemente creativo y rápido trabajando para ti.

### 6. Referencias y Citaciones Académicas

1.  > "Program testing can be used to show the presence of bugs, but never to show their absence!" — **Edsger W. Dijkstra**, *Notes on Structured Programming* (1972)
    [Enlace (PDF)](https://www.cs.utexas.edu/users/EWD/transcriptions/EWD02xx/EWD249.html)

2.  > "The original JUnit was written on a flight from Zurich to the 1997 OOPSLA in Atlanta. Kent was flying, and I was in the back seat programming." — **Erich Gamma**, en una entrevista sobre la creación de JUnit.

3.  > "On the Criteria To Be Used in Decomposing Systems into Modules" — **David L. Parnas**, *Communications of the ACM* (1972). El paper fundamental que sentó las bases teóricas para la modularidad, un prerrequisito para el unit testing efectivo.
    [Enlace (ACM)](https://dl.acm.org/doi/10.1145/361598.361623)

4.  > "Test-Driven Development is a way of managing fear during programming. The fear of making a mistake. The fear of breaking something that already works." — **Kent Beck**, *Test-Driven Development: By Example* (2002).

5.  > "A fixture is a function that is run by pytest before (and sometimes after) the actual test functions." — **pytest Documentation**, *About fixtures*. La documentación oficial es una fuente canónica excelente.
    [Enlace](https://docs.pytest.org/en/stable/explanation/fixtures.html)

6.  > "The Test Pyramid is a metaphor that tells us to group software tests into buckets of different granularity. It also gives an idea of how many tests we should have in each of these groups." — **Martin Fowler**, *The Practical Test Pyramid* (2018).
    [Enlace](https://martinfowler.com/articles/practical-test-pyramid.html)

7.  > "Mock objects are simulated objects that mimic the behavior of real objects in controlled ways." — **Python `unittest.mock` Documentation**.
    [Enlace](https://docs.python.org/3/library/unittest.mock.html)

8.  > "Hypothesis is a Python library for creating unit tests which are simpler to write and more powerful when run, finding edge cases in your code you wouldn’t have thought to look for." — **Hypothesis Documentation**.
    [Enlace](https://hypothesis.readthedocs.io/en/latest/)

9.  *Refactoring: Improving the Design of Existing Code* — **Martin Fowler, Kent Beck, et al.** (1999). Este libro es clave para entender el "porqué" del testing: para permitir la refactorización segura.

10. *Extreme Programming Explained: Embrace Change* — **Kent Beck** (1999). El libro que introdujo TDD y el testing como una práctica central de desarrollo ágil.

---

Has llegado al final de esta guía, pero al principio de un nuevo entendimiento. El Unit Testing, a nivel senior, no es una tarea tediosa que se hace al final. Es una disciplina de diseño. Es el andamiaje que nos permite construir catedrales de software. Es el diálogo constante con nuestro propio código, preguntándole: "¿Realmente haces lo que dices que haces?". Al dominarlo, no solo escribirás código que funciona hoy, sino que crearás sistemas resilientes, comprensibles y preparados para el futuro. Serás, en efecto, el maestro relojero.