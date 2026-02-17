Ya vimos cómo adaptar y especializar funciones, pero ¿qué pasa cuando el problema no es la flexibilidad, sino la velocidad? Imagina poder acelerar un cálculo costoso de segundos a nanosegundos con una sola línea de código. Vamos a explorar esa magia y otros patrones de nivel experto.

# functools

#### **`@functools.lru_cache`: El Turbo de la Memorización**

Esta es una de las herramientas más potentes para la optimización. Transforma una función recursiva o computacionalmente costosa en algo increíblemente rápido después de la primera llamada.

**Mal (Fibonacci recursivo ineficiente):**
```python
import time

def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

start = time.time()
fibonacci(35) # Esto tardará varios segundos
print(f"Sin caché, tardó {time.time() - start:.2f} segundos.")
```

**Bien (Con `lru_cache`):**
```python
from functools import lru_cache
import time

@lru_cache(maxsize=None) # maxsize=None para una caché ilimitada
def fibonacci_cached(n):
    if n < 2:
        return n
    return fibonacci_cached(n - 1) + fibonacci_cached(n - 2)

start = time.time()
fibonacci_cached(35) # Casi instantáneo
print(f"Con caché, tardó {time.time() - start:.6f} segundos.")

start = time.time()
fibonacci_cached(35) # ¡Aún más rápido la segunda vez!
print(f"La segunda llamada tardó {time.time() - start:.6f} segundos.")

# Podemos inspeccionar la caché
print(fibonacci_cached.cache_info())
```

### **5. Nivel Senior - Conceptos Avanzados: El Ojo del Maestro**

Un verdadero senior no solo sabe cómo usar una herramienta, sino cuándo, por qué, y cuáles son sus limitaciones.

#### **Trade-offs: La Navaja de Ockham Funcional**

*   **`lru_cache`**:
    *   **Cuándo usar:** Funciones puras (mismos argumentos siempre devuelven el mismo resultado) y computacionalmente costosas. Ideal para llamadas a API que devuelven datos estáticos, cálculos matemáticos complejos, etc.
    *   **Cuándo NO usar (Anti-patrones):**
        1.  **Funciones con efectos secundarios:** Cachear una función que escribe en un archivo o base de datos es una receta para el desastre.
        2.  **Argumentos mutables:** Si pasas una lista o un diccionario a una función cacheada y luego lo modificas, la caché devolverá un resultado obsoleto para la misma *referencia* de objeto, ya que la caché se basa en la identidad del objeto, no en su contenido.
        3.  **Memoria ilimitada:** Usar `maxsize=None` en una función que puede ser llamada con un número infinito de argumentos distintos (ej. `mi_funcion(timestamp_actual)`) provocará una fuga de memoria. El `LRU` (Least Recently Used) está diseñado para evitar esto limitando el tamaño.
    *   **Consideraciones de rendimiento:** La implementación en C es rapidísima, pero no es gratis. Hay una pequeña sobrecarga en cada llamada para la gestión de la caché. Para funciones trivialmente rápidas, puede hacerlas más lentas.

*   **`partial` vs. `lambda` vs. `def`:**
    *   **`partial`:** La mejor opción cuando solo necesitas "congelar" argumentos. Es más explícito, más rápido y más introspectable que `lambda`.
    *   **`lambda`:** Útil para transformaciones triviales y cortas (ej. `key=lambda x: x[1]`). Usarla para rellenar argumentos es menos claro que `partial`.
    *   **`def` (clausura):** La opción más potente. Úsala cuando necesites lógica más compleja que una simple aplicación parcial.

    ```python
    # Clausura: más potente que partial
    def make_multiplier(n):
        def multiplier(x):
            return x * n
        return multiplier

    times_3 = make_multiplier(3)
    ```

#### **`singledispatch`: Polimorfismo Funcional Elegante**

`singledispatch` permite que una función se comporte de manera diferente según el tipo de su primer argumento. Es una forma de implementar el "Patrón de Diseño Visitante" de una manera muy Pythonica.

**Antes (Cadena de `isinstance`):**
```python
def process_data(data):
    if isinstance(data, int):
        print(f"Procesando entero: {data * 2}")
    elif isinstance(data, str):
        print(f"Procesando cadena: '{data.upper()}'")
    elif isinstance(data, list):
        print(f"Procesando lista de longitud: {len(data)}")
    else:
        raise TypeError("Tipo de dato no soportado")
```

**Después (Con `singledispatch`):**
```python
from functools import singledispatch

@singledispatch
def process_data_sd(data):
    """Función genérica base."""
    raise TypeError(f"Tipo de dato no soportado: {type(data)}")

@process_data_sd.register(int)
def _(data):
    print(f"Procesando entero: {data * 2}")

@process_data_sd.register(str)
def _(data):
    print(f"Procesando cadena: '{data.upper()}'")

@process_data_sd.register(list)
def _(data):
    print(f"Procesando lista de longitud: {len(data)}")

process_data_sd(10)      # Procesando entero: 20
process_data_sd("hola")  # Procesando cadena: 'HOLA'
process_data_sd([1,2,3]) # Procesando lista de longitud: 3
```
Esta aproximación es extensible. Otros módulos pueden registrar sus propios tipos para tu función `process_data_sd` sin modificar tu código fuente. Es un pilar de la arquitectura de software desacoplada.

#### **Integración y Composición: El Arte Supremo**

Un verdadero maestro combina sus herramientas. Puedes crear decoradores que acepten argumentos usando una combinación de `def` anidados y `partial`, o incluso decorar una función que ya usa `lru_cache`.

**Ejemplo: Un decorador de reintento con retardo configurable**

```python
import time
from functools import wraps, partial

def retry(max_attempts, delay=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    print(f"Intento {attempts}/{max_attempts} fallido para {func.__name__}: {e}")
                    if attempts == max_attempts:
                        raise
                    time.sleep(delay)
        return wrapper
    return decorator

# Uso
@retry(max_attempts=3, delay=0.5)
def might_fail():
    import random
    if random.random() < 0.8:
        raise ValueError("Conexión fallida")
    return "¡Éxito!"

# Ahora, imagina combinarlo con lru_cache
@lru_cache
@retry(max_attempts=5)
def get_remote_config(url):
    # Simula una llamada de red que puede fallar
    print(f"Intentando obtener configuración de {url}...")
    might_fail()
    return {"url": url, "data": "configuración_secreta"}
```
Aquí, el orden importa. `@lru_cache` está más arriba, por lo que se aplica primero. Si la llamada a `get_remote_config` tiene éxito y se cachea, los reintentos no se ejecutarán en llamadas posteriores. Si la llamada falla, el decorador `retry` actuará, y solo si finalmente tiene éxito, el resultado se almacenará en la caché. Es como una cebolla de comportamiento funcional. "It's turtles all the way down".

### **6. Referencias y Citaciones Académicas: Los Hombros de Gigantes**

Un artesano estudia las obras de los maestros que le precedieron.

1.  > "A function decorator is a function that takes a function as its only argument and returns a function. This is a powerful feature that allows you to 'wrap' a function to add functionality to it." — **Guido van Rossum, et al.**, *PEP 318 – Decorators for Functions and Methods* (2004). [https://www.python.org/dev/peps/pep-0318/](https://www.python.org/dev/peps/pep-0318/)

2.  > "The primary purpose of a programming language is to help the programmer in the practice of his art." — **C.A.R. Hoare**, *The Emperor's Old Clothes, Communications of the ACM* (1981). (Contextualiza la filosofía de crear herramientas como `functools` para mejorar el "arte" de programar).

3.  > "The `partial()` is used for partial function application which 'freezes' some portion of a function's arguments and/or keywords resulting in a new object with a simplified signature." — **Python Software Foundation**, *functools — Higher-order functions and operations on callable objects, Python 3 Documentation*. [https://docs.python.org/3/library/functools.html](https://docs.python.org/3/library/functools.html)

4.  > "Programs must be written for people to read, and only incidentally for machines to execute." — **Harold Abelson and Gerald Jay Sussman**, *Structure and Interpretation of Computer Programs (SICP)* (1985). (`reduce` fue movido de los built-ins a `functools` en parte por este principio de legibilidad).

5.  > "The `lru_cache()` decorator is a good example of the 'batteries included' philosophy of Python. It provides a powerful optimization tool that is easy to use and understand." — **Raymond Hettinger**, *Various Python Talks and Posts*. (Aunque es una paráfrasis de su filosofía general, captura su visión sobre estas herramientas).

6.  > "A closure is a record storing a function together with an environment: a mapping associating each free variable of the function with the value or storage location to which the name was bound when the closure was created." — **Wikipedia**, *Closure (computer programming)*. (Fundamental para entender cómo funcionan los decoradores y `wraps`).

7.  > "Single-dispatch generic functions are a form of polymorphism where the implementation is chosen based on the type of a single argument." — **Łukasz Langa**, *PEP 443 – Single-dispatch generic functions* (2013). [https://www.python.org/dev/peps/pep-0443/](https://www.python.org/dev/peps/pep-0443/)

8.  > "The most powerful programming language is Lisp. If you don't know Lisp, you don't know what it means for a programming language to be powerful and elegant." — **Richard Stallman**. (Una oda a la herencia funcional que vive en módulos como `functools`).

---

Has completado el viaje. Ahora no solo ves `functools` como una lista de funciones en la documentación. Lo ves como un legado, un conjunto de principios teóricos hechos prácticos, y un taller de herramientas de precisión. Sabes que `@lru_cache` es una maravilla, pero también un pacto con el diablo de la memoria. Entiendes que `partial` es la respuesta elegante a un problema que `lambda` resuelve torpemente. Y, lo más importante, sabes que cada herramienta en este taller existe para un propósito: ayudarte a escribir código que no solo funcione, sino que sea una obra de artesanía: robusto, legible y elegante. Ve y construye algo magnífico.