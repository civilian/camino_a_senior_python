Escribir tests básicos es un gran primer paso, pero ¿qué sucede cuando nuestro código depende de una base de datos o una API externa? Ahí es donde separamos a los programadores que usan tests de los ingenieros que diseñan estrategias de testing robustas. Exploremos cómo aislar nuestro código y pensar más allá de los tests simples.

# Unit Testing (unittest, pytest)

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
/--------------- \
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