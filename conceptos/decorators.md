# Decorators

Claro que sí. Prepárate para una inmersión profunda en el mundo de los decoradores de Python. Este no es un tutorial básico; es una guía completa diseñada para llevar tu comprensión desde los fundamentos hasta el nivel de un desarrollador Senior, cubriendo no solo el "cómo" sino, más importante, el "porqué" y el "cuándo".

***

# Dominando los Decoradores en Python: De Cero a Senior

Un decorador, en su esencia, es "azúcar sintáctico" para una idea mucho más fundamental en Python: las **funciones de orden superior (Higher-Order Functions)**. Entender esto es el primer paso para dominarlos.

> **Citación Clave:** El **PEP 318**, que introdujo formalmente los decoradores en Python 2.4, los describe como: *"una forma de transformar una función o método... La motivación principal es simplificar la sintaxis para aplicar estas transformaciones de una manera que sea legible y mantenible."* - [PEP 318 -- Decorators for Functions and Methods](https://peps.python.org/pep-0318/)

## 1. Los Pilares Fundamentales (Prerrequisitos)

Para ser un experto en decoradores, primero debes dominar los conceptos sobre los que se construyen. Un Senior no solo usa la sintaxis `@`, entiende la maquinaria que hay debajo.

### 1.1. Las Funciones como Objetos de Primera Clase (First-Class Objects)

En Python, las funciones no son solo bloques de código; son objetos como cualquier otro (enteros, strings, listas). Esto significa que puedes:
1.  Asignarlas a una variable.
2.  Pasarlas como argumento a otra función.
3.  Retornarlas desde otra función.

```python
def saludar(nombre):
    return f"Hola, {nombre}"

# 1. Asignar a una variable
mi_saludo = saludar
print(mi_saludo("Mundo"))  # Salida: Hola, Mundo

# 2. Pasar como argumento
def ejecutar_funcion(func, argumento):
    print(func(argumento))

ejecutar_funcion(saludar, "Pythonista") # Salida: Hola, Pythonista
```

### 1.2. Funciones de Orden Superior (Higher-Order Functions)

Una función que toma otra función como argumento, o que retorna una función, se llama Función de Orden Superior. El ejemplo `ejecutar_funcion` de arriba es una. Los decoradores son una aplicación de este concepto.

### 1.3. Clausuras (Closures)

Este es el concepto más crucial y a menudo el menos entendido. **Una clausura ocurre cuando una función anidada recuerda y tiene acceso al ámbito (scope) de la función que la contiene, incluso después de que la función contenedora haya terminado su ejecución.**

```python
def fabrica_de_multiplicadores(n):
    """Función exterior (fábrica)"""
    def multiplicador(x):
        """Función anidada (clausura)"""
        # 'n' no está definido aquí, pero es "recordado" del ámbito de la fábrica.
        return x * n
    return multiplicador

# Creamos dos instancias de la clausura, cada una "recordando" un 'n' diferente.
por_tres = fabrica_de_multiplicadores(3)
por_cinco = fabrica_de_multiplicadores(5)

print(por_tres(10))   # Salida: 30
print(por_cinco(10))  # Salida: 50
print(por_tres(por_cinco(2))) # Salida: 30 (3 * (5 * 2))
```
La función `multiplicador` es una clausura. "Recuerda" el valor de `n` de su entorno de creación. Los decoradores dependen fundamentalmente de las clausuras para funcionar.

## 2. Anatomía de un Decorador: Paso a Paso

Un decorador es simplemente una función que toma otra función como argumento, le añade alguna funcionalidad y retorna otra función, todo sin modificar el código de la función original.

### 2.1. La Forma Manual (Sin Azúcar Sintáctico)

```python
def mi_decorador(func):
    def wrapper():
        print("Algo sucede antes de llamar a la función.")
        func()
        print("Algo sucede después de llamar a la función.")
    return wrapper

def di_hola():
    print("¡Hola!")

# Así se aplicaría un decorador manualmente
di_hola_decorado = mi_decorador(di_hola)
di_hola_decorado()
```

### 2.2. La Forma "Pythonica" con `@`

La sintaxis `@` es solo una forma más limpia y legible de hacer exactamente lo mismo que arriba.

```python
@mi_decorador
def di_adios():
    print("¡Adiós!")

di_adios()
```
Esta pieza de código es 100% equivalente a: `di_adios = mi_decorador(di_adios)`.

### 2.3. Decoradores para Funciones con Argumentos

Nuestro decorador anterior fallaría si la función decorada aceptara argumentos. Para hacerlo genérico, usamos `*args` y `**kwargs`.

```python
def decorador_universal(func):
    def wrapper(*args, **kwargs):
        print(f"Llamando a la función '{func.__name__}' con argumentos {args} y {kwargs}")
        resultado = func(*args, **kwargs) # Pasamos los argumentos y capturamos el resultado
        print(f"La función '{func.__name__}' retornó: {resultado}")
        return resultado
    return wrapper

@decorador_universal
def suma(a, b, mensaje="Resultado:"):
    print(mensaje)
    return a + b

suma(10, 5, mensaje="Total:")
```

### 2.4. El Problema de los Metadatos y `functools.wraps`

Hay un problema sutil pero importante. Al decorar una función, estamos reemplazándola con la función `wrapper`. Esto significa que perdemos los metadatos de la función original, como su nombre (`__name__`) y su docstring (`__doc__`).

```python
print(suma.__name__) # Salida: wrapper (¡Incorrecto!)
print(suma.__doc__)  # Salida: None (¡Perdimos la documentación!)
```

Un desarrollador Senior **siempre** soluciona esto usando `@functools.wraps`. Este es un decorador que decora nuestro `wrapper` y copia los metadatos de la función original a la función `wrapper`.

> **Citación Clave:** La documentación oficial de Python para `functools.wraps` dice: *"This is a convenience function for invoking `update_wrapper()` as a function decorator when defining a wrapper function. It is equivalent to `partial(update_wrapper, wrapped=wrapped, assigned=assigned, updated=updated)`."* - [Python `functools` Documentation](https://docs.python.org/3/library/functools.html#functools.wraps)

```python
import functools
import time

def decorador_senior(func):
    @functools.wraps(func) # <-- La pieza clave
    def wrapper(*args, **kwargs):
        """Este es el docstring del wrapper, pero será reemplazado."""
        # ... lógica del decorador ...
        return func(*args, **kwargs)
    return wrapper

@decorador_senior
def resta(a, b):
    """Esta función resta dos números."""
    return a - b

print(resta.__name__) # Salida: resta (¡Correcto!)
print(resta.__doc__)  # Salida: Esta función resta dos números. (¡Correcto!)
```
**Regla de oro:** Si escribes un decorador, usa `@functools.wraps`. Es una marca de calidad y profesionalismo.

## 3. Decoradores Avanzados

### 3.1. Decoradores con Argumentos (Fábricas de Decoradores)

¿Y si queremos que nuestro decorador acepte argumentos? Por ejemplo, `@repetir(n=3)`. Para esto, necesitamos un nivel extra de anidación: una función que *crea* y *retorna* un decorador.

```python
def repetir(n):
    """Esto es una fábrica de decoradores."""
    def decorador(func):
        """Este es el decorador real."""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            """Este es el wrapper."""
            for _ in range(n):
                resultado = func(*args, **kwargs)
            return resultado
        return wrapper
    return decorador

@repetir(n=3)
def saluda(nombre):
    print(f"Hola, {nombre}")

saluda("Senior Dev")
# Salida:
# Hola, Senior Dev
# Hola, Senior Dev
# Hola, Senior Dev
```
El flujo es:
1.  `repetir(n=3)` es llamado.
2.  Retorna la función `decorador`.
3.  Python usa este `decorador` retornado para decorar `saluda`, es decir, `saluda = decorador(saluda)`.

### 3.2. Decoradores de Clases (Class-based Decorators)

A veces, un decorador necesita mantener un estado. Por ejemplo, contar cuántas veces se ha llamado a una función. Aunque se puede lograr con clausuras y variables `nonlocal`, una clase puede ser más limpia y explícita.

Para que una clase actúe como decorador, debe implementar el método `__call__`.

```python
class ContadorDeLlamadas:
    def __init__(self, func):
        functools.update_wrapper(self, func) # Preserva metadatos
        self.func = func
        self.num_llamadas = 0

    def __call__(self, *args, **kwargs):
        self.num_llamadas += 1
        print(f"Llamada número {self.num_llamadas} a {self.func.__name__}")
        return self.func(*args, **kwargs)

@ContadorDeLlamadas
def decir_whee():
    print("Whee!")

decir_whee() # Llamada número 1 a decir_whee
decir_whee() # Llamada número 2 a decir_whee
```
Aquí, `decir_whee` se convierte en una *instancia* de la clase `ContadorDeLlamadas`.

### 3.3. Decoradores de Clases (Decorating Classes)

También es posible decorar clases enteras. Esto fue formalizado en el **PEP 3129**. Un decorador de clase toma una clase como argumento y retorna una clase (posiblemente modificada).

> **Citación Clave:** *"This PEP proposes a syntax for "class decorators", equivalent to the existing syntax for function decorators."* - [PEP 3129 -- Class Decorators](https://peps.python.org/pep-3129/)

Un uso común es para implementar el patrón Singleton o para añadir métodos a una clase dinámicamente.

```python
def añadir_repr(cls):
    """Decorador de clase para añadir un __repr__ útil."""
    def __repr__(self):
        params = ', '.join(f'{k}={v!r}' for k, v in self.__dict__.items())
        return f'{type(self).__name__}({params})'
    
    cls.__repr__ = __repr__
    return cls

@añadir_repr
class MiClase:
    def __init__(self, x, y):
        self.x = x
        self.y = y

instancia = MiClase(10, "test")
print(instancia) # Salida: MiClase(x=10, y='test')
```

## 4. Casos de Uso del Mundo Real (Nivel Senior)

Aquí es donde se demuestra la maestría: aplicando el patrón de decorador para resolver problemas reales de forma elegante.

*   **Logging:** Envolver funciones críticas para registrar sus llamadas, argumentos y resultados.
*   **Medición de Rendimiento (Timing):** Calcular cuánto tarda una función en ejecutarse.
*   **Caching/Memoización:** Almacenar los resultados de funciones costosas. Python lo incluye en su librería estándar con `@functools.lru_cache`.
*   **Autenticación y Autorización:** En frameworks web como Flask o Django, decoradores como `@login_required` o `@permission_required` verifican si un usuario puede ejecutar una vista.
*   **Validación de Datos:** Verificar que los argumentos de una función cumplen ciertos criterios (tipos, rangos, etc.) antes de ejecutarla.
*   **Manejo de Contexto (DB Connections):** Un decorador puede abrir una conexión a la base de datos, ejecutar la función dentro de un bloque `try...finally`, y asegurarse de que la conexión se cierre siempre.
*   **Registro de APIs/Plugins:** Un decorador puede registrar una función en un "despachador" central, permitiendo arquitecturas de plugins.

```python
# Ejemplo: Caching con la librería estándar
import functools

@functools.lru_cache(maxsize=None) # Least Recently Used Cache
def fibonacci(n):
    """Calcula el n-ésimo número de Fibonacci (muy ineficiente sin caché)."""
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# La primera llamada a fibonacci(35) será lenta.
print(fibonacci(35))

# Las siguientes llamadas (con los mismos argumentos) serán instantáneas
# porque los resultados están cacheados.
print(fibonacci(35))
```

## 5. Anti-Patrones y Consideraciones (La Sabiduría del Senior)

Un Senior no solo sabe cómo usar una herramienta, sino también cuándo **no** usarla.

1.  **Abuso de Decoradores (Decorator Chaining Hell):** Apilar demasiados decoradores (`@d1 @d2 @d3 @d4`) puede hacer el código difícil de leer y depurar. El orden importa: se aplican de abajo hacia arriba.
2.  **Magia Oculta:** Un decorador puede cambiar drásticamente el comportamiento de una función de una manera no obvia. El código debe ser explícito. Si un decorador modifica los argumentos o el valor de retorno de forma inesperada, puede ser un signo de mal diseño.
3.  **Rendimiento:** Cada capa de decoración añade una llamada de función extra. Para código en un bucle muy crítico (hot loop), este overhead podría ser relevante, aunque en el 99% de los casos no lo es.
4.  **Alternativas:** A veces, un simple Gestor de Contexto (`with` statement) o una función de orden superior llamada explícitamente es más claro que un decorador.

> **Citación de la Comunidad:** **Luciano Ramalho** en su libro **"Fluent Python"** dedica un capítulo entero a los decoradores y las clausuras, enfatizando que entender las clausuras es la clave para entender los decoradores. Argumenta que los decoradores son una de las características más potentes de Python para la metaprogramación.

> **Citación de la Comunidad:** **Raymond Hettinger**, un desarrollador del core de Python y un educador reconocido, a menudo explica los decoradores en sus charlas como una forma de separar las preocupaciones (separation of concerns). La lógica de negocio principal permanece en la función, mientras que las preocupaciones transversales (logging, caching, auth) se encapsulan en los decoradores.

## 6. Conclusión: El Decorador como Herramienta de Composición

Al final del día, los decoradores son una herramienta de **composición**. Te permiten construir funcionalidades complejas a partir de piezas más simples y reutilizables. En lugar de herencia o de modificar el código existente, "decoras" el comportamiento existente con nuevas capas.

Dominar los decoradores significa:
-   Entender a la perfección las funciones como objetos, las funciones de orden superior y, sobre todo, las **clausuras**.
-   Saber usar `*args`, `**kwargs` y `@functools.wraps` por defecto.
-   Ser capaz de crear decoradores con y sin argumentos, y decoradores basados en clases cuando el estado es necesario.
-   Reconocer los patrones comunes donde los decoradores brillan (caching, auth, logging).
-   Tener el juicio para decidir cuándo un decorador es la solución correcta y cuándo es una complicación innecesaria.

Esta comprensión profunda es lo que separa a un programador intermedio de un desarrollador Senior. No se trata solo de la sintaxis, sino de la arquitectura del pensamiento.
