Ya hemos visto cómo Hypothesis encuentra bugs que pasaríamos por alto. Ahora, es momento de ir más allá. ¿Cómo pruebas un sistema cuyo comportamiento depende de una secuencia de operaciones, como una API o una base de datos? Vamos a sumergirnos en las características más potentes de Hypothesis para dominar de verdad esta herramienta.

# hypothesis (property-based testing)

## 5. Nivel Senior - Conceptos Avanzados: Dominando la Máquina

Bienvenido al siguiente nivel. Aquí es donde pasas de usar Hypothesis a *pensar* con Hypothesis.

### La Magia del Shrinking: ¿Cómo Funciona?

Cuando un test falla, Hypothesis no se rinde. Inicia un proceso de "shrinking" (reducción) para encontrar el contraejemplo más simple. Conceptualmente, funciona como una especie de **búsqueda binaria sobre la complejidad del dato**.

Imagina que falla con la lista `[10, 20, 0, 50]`. Hypothesis intentará:
-   ¿Falla con `[10, 20]`? (la primera mitad)
-   ¿Falla con `[0, 50]`? (la segunda mitad)
-   ¿Falla con `[0, 0, 0, 0]`? (reduciendo los valores)
-   ¿Falla con `[10, 20, 50]`? (eliminando un elemento)

Repite este proceso recursivamente, explorando el "árbol" de simplificaciones posibles hasta que encuentra un ejemplo que falla y que no puede ser simplificado más. Este proceso es la salsa secreta de Hypothesis y lo que lo hace tan increíblemente útil para la depuración.

### Stateful Testing: Probando Sistemas con Memoria

¿Cómo pruebas un sistema cuyo comportamiento depende de una secuencia de operaciones? ¿Una base de datos, una API RESTful, una caché? La respuesta es el **Stateful Testing** con `RuleBasedStateMachine`.

Esto es, sin duda, la característica más avanzada y potente de Hypothesis.

**Analogía:** Imagina probar una máquina expendedora. No pruebas "insertar moneda" y "seleccionar producto" de forma aislada. Pruebas *secuencias*: insertar moneda, insertar otra moneda, seleccionar producto, recibir cambio.

Con `RuleBasedStateMachine`, defines:
1.  **El estado** del sistema (real y un modelo simplificado).
2.  **Las reglas** (las operaciones que puedes realizar, como `insertar_moneda`).
3.  **Los invariantes** (propiedades que deben ser ciertas *después de cada paso*).

Hypothesis generará secuencias aleatorias de estas reglas y comprobará que los invariantes se mantienen y que el estado del sistema real coincide con tu modelo.

**Ejemplo: Probando una Caché LRU (Least Recently Used)**

```python
from collections import OrderedDict
from hypothesis.stateful import RuleBasedStateMachine, rule, precondition, invariant

class LRUCache:
    # ... implementación de una caché LRU ...

class LRUCacheMachine(RuleBasedStateMachine):
    def __init__(self):
        super().__init__()
        # Modelo: un diccionario ordenado que es simple y correcto.
        self.model = OrderedDict()
        # Sistema bajo prueba
        self.sut = LRUCache(capacity=3)

    @rule(key=st.integers(), value=st.text())
    def set(self, key, value):
        self.sut.set(key, value)
        self.model[key] = value
        if len(self.model) > 3:
            self.model.popitem(last=False) # Simula el desalojo LRU

    @rule(key=st.integers())
    def get(self, key):
        model_result = self.model.get(key, -1)
        sut_result = self.sut.get(key)
        assert model_result == sut_result
        # Si la clave existe, se mueve al final (más reciente)
        if key in self.model:
            self.model.move_to_end(key)

    @invariant()
    def model_and_sut_agree(self):
        # El contenido de la caché y el modelo deben ser consistentes
        # (ignorando el orden por simplicidad aquí, aunque se podría hacer más estricto)
        sut_items = {k: self.sut.get(k) for k in self.model.keys()}
        assert self.model == sut_items

TestLRUCache = LRUCacheMachine.TestCase
```

Este test encontrará bugs sutiles en la lógica de actualización y desalojo de la caché que serían casi imposibles de encontrar con tests de ejemplo.

### Trade-offs: Cuándo NO Usar Hypothesis

Hypothesis es una herramienta poderosa, no una bala de plata.

-   **NO lo uses cuando la propiedad es más compleja que la implementación.** Si para verificar tu función de `sort` necesitas re-implementar `sort` en el test, no ganas nada. (Aquí es donde el Oracle Testing con `sorted()` es útil).
-   **NO lo uses para tests de regresión muy específicos.** Si un bug ocurrió con el input exacto `"legacy_user_#123"`, crea un test de ejemplo para ese caso. Es más rápido y documenta el bug. Hypothesis es para encontrar *clases* de bugs.
-   **Ten cuidado con el rendimiento.** Los tests de PBT son inherentemente más lentos. Pueden no ser adecuados para un ciclo de TDD muy rápido, pero son perfectos para tu suite de CI. Hypothesis tiene perfiles de configuración (`@settings`) para controlar el tiempo de ejecución.
-   **Cuando las propiedades son vagas.** Si estás probando una UI, la propiedad "el botón debe ser azul" no es algo que el PBT pueda manejar bien.

### Anti-Patrones Comunes

-   **La Propiedad Trivial:** `assert mi_funcion(x) is not None`. Esto solo prueba que no crashea, lo cual es útil pero débil. Busca propiedades más fuertes.
-   **Estrategias Demasiado Amplias:** Usar `st.text()` para un número de teléfono. Sé específico. Crea una estrategia que genere números de teléfono válidos. Esto enfoca la búsqueda y produce fallos más relevantes.
-   **Filtrado Excesivo con `assume`:** Si tu test descarta el 99% de los datos generados con `assume`, será extremadamente lento. Es una señal de que tu estrategia de generación es incorrecta. Deberías construir una estrategia que genere *directamente* datos válidos.
-   **Ocultar el Fallo:** No pongas un `try...except` genérico dentro de tu test. Deja que Hypothesis vea la excepción para que pueda encontrar el contraejemplo.

## 6. Referencias y Citaciones Académicas: Sobre Hombros de Gigantes

Un verdadero senior conoce la genealogía de sus herramientas. Aquí están las fuentes primarias y secundarias que sustentan este conocimiento.

1.  > "We have developed a tool that helps the user to formulate and test properties of Haskell programs. The properties are functions of type `a -> Bool`, for some type `a` of testable data. QuickCheck generates a number of random values of type `a` and checks that the property holds for all of them."
    > — **Koen Claessen & John Hughes**, *QuickCheck: A Lightweight Tool for Random Testing of Haskell Programs* (2000). [Enlace](https://www.cs.tufts.edu/~nr/cs257/archive/john-hughes/quick.pdf)

2.  > "The goal of Hypothesis is not just to find bugs that other testing methods would miss, but to do so in a way that is actively pleasant to use and integrates well with your existing work-flows."
    > — **David R. MacIver**, *Documentación Oficial de Hypothesis*. [Enlace](https://hypothesis.readthedocs.io/)

3.  > "Program testing can be used to show the presence of bugs, but never to show their absence!"
    > — **Edsger W. Dijkstra**, *Notes on Structured Programming* (1972). Un texto fundamental sobre el razonamiento de la corrección del software.

4.  > "The problem with example-based testing is the examples. Specifically, the examples you choose... you're likely to pick examples that work."
    > — **David R. MacIver**, *Hypothesis: A new approach to property-based testing* (Charla en PyCon 2016). [Enlace a charla similar](https://www.youtube.com/watch?v=k_hP5A-b2z4)

5.  > "The most powerful notion in the theory of testing is the test oracle, a mechanism that can determine whether the outcome of a test is correct or not."
    > — **Boris Beizer**, *Software Testing Techniques, Second Edition* (1990). El concepto de "Oracle Testing" es un pilar para muchas propiedades.

6.  > "Beware of bugs in the above code; I have only proved it correct, not tried it."
    > — **Donald Knuth**, *Notes on the van Emde Boas construction of priority deques* (1977). Un chiste clásico de programadores que resalta la brecha entre la prueba formal y la realidad, una brecha que el PBT ayuda a cerrar.

7.  > "A metamorphic relation (MR) is a necessary property of the intended functionality of a piece of software, and can be used as a metamorphic oracle for testing."
    > — **T. Y. Chen et al.**, *Metamorphic testing: a new approach for generating next test cases* (1998). La base académica para las pruebas metamórficas, un patrón avanzado de PBT.

8.  > "Falsification, in the sense of Popper, is not just a feature of science, but of all critical reasoning. A property-based test is an exercise in critical reasoning about code."
    > — **Hillel Wayne**, *Practical TLA+: Planning Driven Development* (2018). Aunque sobre TLA+, el libro conecta brillantemente la filosofía de la ciencia con la ingeniería de software moderna.

---

Has llegado al final. Pero esto no es un final, es un comienzo. Ahora no solo sabes *cómo* usar Hypothesis, sino *por qué* funciona, de *dónde* viene y *cuándo* (y cuándo no) desatar su poder.

La próxima vez que escribas una función, no te preguntes solo "¿qué ejemplos debo probar?". Pregúntate: **"¿Qué propiedades definen la corrección de este código?"**. Esa es la pregunta que te distingue como un ingeniero senior. Ahora ve y construye software más robusto, no con esperanza, sino con duda sistemática.