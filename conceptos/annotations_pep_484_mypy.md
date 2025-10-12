# Annotations (PEP 484, mypy)

¡Excelente! Has pedido una inmersión profunda en el sistema de tipado de Python, un tema fundamental que distingue a un programador intermedio de uno senior. Un desarrollador senior no solo sabe *cómo* usar las anotaciones, sino *por qué*, *cuándo*, y cómo integrarlas en un proyecto a gran escala para maximizar sus beneficios.

Aquí tienes una guía exhaustiva en formato Markdown, desde los fundamentos hasta los conceptos más avanzados y la filosofía detrás de ellos, con las citaciones solicitadas.

---

# Guía Maestra de Anotaciones de Tipo en Python (PEP 484 y más allá)

## Introducción: La Revolución Silenciosa del Tipado Gradual

Python es, y siempre será, un lenguaje de tipado dinámico. Esto significa que no necesitas declarar el tipo de una variable al crearla.

```python
# Tipado dinámico en acción
mi_variable = 10         # Es un int
mi_variable = "hola"   # Ahora es un str, ¡no hay problema!
```

Sin embargo, en proyectos grandes, esta flexibilidad puede llevar a errores difíciles de rastrear y a un código menos legible. Para solucionar esto, Python introdujo las **anotaciones de tipo** (Type Hints) de forma oficial en **PEP 484** ([Citation: PEP 484 -- Type Hints](https://www.python.org/dev/peps/pep-0484/)).

**Punto Clave Senior:** Las anotaciones de tipo son **opcionales** y **no son forzadas por el intérprete de Python en tiempo de ejecución**. Son metadatos. Su poder se desata con herramientas de análisis estático como **Mypy**, Pyright (Pylance en VSCode), o Pyre. Este concepto se llama **Tipado Gradual** (Gradual Typing): puedes introducir tipos poco a poco en una base de código existente.

> "Python will remain a dynamically typed language, and the authors have no desire to ever make type hints mandatory, even by convention." - **PEP 484**

---

## 1. Fundamentos (El Nivel de Entrada)

### 1.1. Sintaxis Básica

La sintaxis es simple: `variable: tipo`. Para funciones: `def funcion(param: tipo) -> tipo_retorno:`.

- **Variables (PEP 526):** Introducido formalmente en [PEP 526 -- Syntax for Variable Annotations](https://www.python.org/dev/peps/pep-0526/).

```python
edad: int = 25
nombre: str = "Guido"
es_valido: bool = True
pi: float = 3.14159

# Mypy lo aprueba
# mypy mi_script.py -> Success: no issues found in 1 source file
```

Si intentas asignar un tipo incorrecto, Mypy te lo advertirá:

```python
edad: int = "veinticinco" # Error!

# Mypy: error: Incompatible types in assignment (expression has type "str", variable has type "int")
```

### 1.2. Tipos Primitivos y Colecciones

El módulo `typing` es tu mejor amigo.

```python
from typing import List, Set, Dict, Tuple

# Lista de enteros
numeros: List[int] = [1, 2, 3]

# Conjunto de strings
nombres: Set[str] = {"Alice", "Bob"}

# Diccionario con claves string y valores float
precios: Dict[str, float] = {"manzana": 1.5, "banana": 0.75}

# Tupla de tamaño y tipos fijos
coordenada: Tuple[int, int, str] = (10, 20, "origen")

# Tupla de tamaño variable con tipos homogéneos
puntos: Tuple[int, ...] = (1, 2, 3, 4)
```

### 1.3. `Any`, `None` y `Optional`

- `Any`: Es el "comodín". Una variable anotada con `Any` puede ser de cualquier tipo. Es una escotilla de escape, pero úsala con moderación. Un código senior minimiza el uso de `Any`.
- `None`: El tipo del objeto `None`.
- `Optional[T]`: Indica que una variable puede ser de tipo `T` o `None`. Es un atajo para `Union[T, None]`.

```python
from typing import Any, Optional

def procesar_datos(datos: Any) -> None:
    # Mypy no se quejará de casi nada que hagas con 'datos'
    # ¡Esto reduce la seguridad!
    print(datos.upper()) # Podría fallar en tiempo de ejecución si datos no es str

def buscar_usuario(user_id: int) -> Optional[str]:
    if user_id == 1:
        return "Admin"
    return None # Válido

# Mypy te forzará a comprobar el None
nombre_usuario = buscar_usuario(1)
if nombre_usuario is not None:
    print(nombre_usuario.upper()) # Seguro
```

---

## 2. Conceptos Intermedios (Construyendo Robustez)

### 2.1. `Union` y Type Aliases

- `Union[T1, T2, ...]`: La variable puede ser de cualquiera de los tipos listados.
- **Type Aliases**: Para no repetir anotaciones complejas, puedes crear alias.

```python
from typing import List, Union

# Un ID puede ser int o str
ID = Union[int, str]
Vector = List[float]

def imprimir_id(user_id: ID) -> None:
    print(f"ID de usuario: {user_id}")

def escalar_vector(v: Vector, s: float) -> Vector:
    return [x * s for x in v]

imprimir_id(101)       # Válido
imprimir_id("abc-123") # Válido
# imprimir_id(None)    # Mypy: error: Argument 1 to "imprimir_id" has incompatible type "None"; expected "Union[int, str]"
```

### 2.2. `Callable`

Para anotar funciones o cualquier objeto que se pueda llamar (como un objeto con `__call__`).

La sintaxis es `Callable[[Arg1Type, Arg2Type], ReturnType]`.

```python
from typing import Callable

def ejecutar_operacion(a: int, b: int, operacion: Callable[[int, int], int]) -> int:
    return operacion(a, b)

def sumar(x: int, y: int) -> int:
    return x + y

resultado = ejecutar_operacion(5, 3, sumar) # Válido
print(resultado) # 8
```

### 2.3. Genéricos con `TypeVar`

Este es un concepto **CRUCIAL** para un desarrollador senior. Permite crear funciones y clases que funcionan con múltiples tipos de manera segura.

```python
from typing import TypeVar, List

# T es una variable de tipo. Puede ser cualquier tipo.
T = TypeVar('T')

def obtener_primer_elemento(items: List[T]) -> T:
    return items[0]

# Mypy infiere el tipo de T en cada llamada
primer_numero = obtener_primer_elemento([1, 2, 3])   # Mypy infiere T=int, primer_numero es int
primer_nombre = obtener_primer_elemento(["a", "b"]) # Mypy infiere T=str, primer_nombre es str
```

Puedes restringir un `TypeVar`:

```python
# NumberT solo puede ser int o float
NumberT = TypeVar('NumberT', bound=int|float) # Sintaxis moderna (Python 3.10+)
# Antigua sintaxis: NumberT = TypeVar('NumberT', bound=Union[int, float])

def suma_numerica(a: NumberT, b: NumberT) -> NumberT:
    # Mypy sabe que a y b soportan la operación '+'
    return a + b
```

### 2.4. Tipado de Clases y Métodos

- `self` y `cls` no se anotan explícitamente en la mayoría de los casos. Mypy los infiere.
- Para referenciar la propia clase dentro de sus anotaciones (forward reference), usa un string.

```python
class Nodo:
    def __init__(self, valor: int, siguiente: 'Optional[Nodo]' = None):
        self.valor = valor
        self.siguiente = siguiente

    def __repr__(self) -> str:
        return f"Nodo({self.valor})"
```

A partir de Python 3.7, con `from __future__ import annotations` (o por defecto en Python 3.10+), ya no necesitas los strings para las referencias futuras. Esto se describe en **PEP 563** ([Citation: PEP 563 -- Postponed Evaluation of Annotations](https://www.python.org/dev/peps/pep-0563/)).

---

## 3. Tópicos Avanzados (El Nivel Senior)

Aquí es donde demuestras maestría.

### 3.1. `Protocol` y Duck Typing Estático (PEP 544)

Este es quizás el concepto más "pythónico" y potente. En lugar de heredar de una clase base abstracta, un `Protocol` define una "forma" (un conjunto de métodos y atributos). Cualquier clase que tenga esa forma, cumple con el protocolo, sin necesidad de herencia explícita. Es Duck Typing para el analizador estático.

[Citation: PEP 544 -- Protocols: Structural subtyping (static duck typing)](https://www.python.org/dev/peps/pep-0544/)

```python
from typing import Protocol, Iterable

class SoportaCierre(Protocol):
    def close(self) -> None:
        ... # El cuerpo del método no importa

# Esta clase NO hereda de SoportaCierre
class RecursoArchivo:
    def close(self) -> None:
        print("Cerrando archivo")

# Esta tampoco
class ConexionRed:
    def close(self) -> None:
        print("Cerrando conexión")

def cerrar_recursos(recursos: Iterable[SoportaCierre]) -> None:
    for recurso in recursos:
        recurso.close() # Mypy sabe que .close() existe

cerrar_recursos([RecursoArchivo(), ConexionRed()]) # ¡Válido!
```

### 3.2. `TypedDict` (PEP 589)

Para anotar diccionarios que tienen un conjunto fijo de claves de tipo string y valores de tipos específicos. Ideal para payloads de API, JSON, etc.

[Citation: PEP 589 -- TypedDict: Type Hints for Dictionaries with a Fixed Set of Keys](https://www.python.org/dev/peps/pep-0589/)

```python
from typing import TypedDict

class Usuario(TypedDict):
    nombre: str
    id: int
    activo: bool

def procesar_usuario(usuario: Usuario) -> None:
    if usuario["activo"]:
        print(f"Usuario {usuario['nombre'].upper()} está activo.")

# Mypy verifica la estructura
procesar_usuario({"nombre": "Alice", "id": 1, "activo": True}) # Válido
# procesar_usuario({"nombre": "Bob", "id": "dos"}) # Mypy: error: Incompatible type for "id"
```

### 3.3. `Literal` (PEP 586)

Cuando una variable solo puede tomar un conjunto específico de valores literales.

[Citation: PEP 586 -- Literal Types](https://www.python.org/dev/peps/pep-0586/)

```python
from typing import Literal

Modo = Literal["r", "w", "a", "r+"]

def abrir_archivo(path: str, modo: Modo) -> None:
    print(f"Abriendo {path} en modo {modo}")

abrir_archivo("log.txt", "w") # Válido
# abrir_archivo("log.txt", "x") # Mypy: error: Argument 2 to "abrir_archivo" has incompatible type "str"; expected "Literal['r', 'w', 'a', 'r+']"
```

### 3.4. `Final` y `ClassVar`

- `Final` (PEP 591): Indica que una variable o atributo no debe ser reasignado.
- `ClassVar`: Indica que una variable es una variable de clase, no de instancia.

[Citation: PEP 591 -- Adding a final qualifier to typing](https://www.python.org/dev/peps/pep-0591/)

```python
from typing import final, Final, ClassVar

VERSION: Final[str] = "1.2.3"
# VERSION = "1.2.4" # Mypy: error: Cannot assign to final name "VERSION"

class Config:
    _instancia: ClassVar[Optional['Config']] = None
    timeout: int

    def __init__(self, timeout: int):
        self.timeout = timeout

@final
class VentanaPrincipal: # Nadie puede heredar de esta clase
    pass
```

### 3.5. Sobrecarga de Funciones con `@overload`

Para funciones que pueden aceptar diferentes combinaciones de tipos de argumentos y retornar diferentes tipos en consecuencia.

```python
from typing import overload, Union

@overload
def obtener_valor(key: str) -> str: ...

@overload
def obtener_valor(key: int) -> int: ...

def obtener_valor(key: Union[str, int]) -> Union[str, int]:
    if isinstance(key, str):
        return "valor_string"
    else:
        return 123

# Mypy entiende los retornos específicos
resultado_str: str = obtener_valor("mi_llave")
resultado_int: int = obtener_valor(42)
# resultado_malo: str = obtener_valor(42) # Mypy: error: Incompatible types in assignment
```

---

## 4. El Ecosistema y las Mejores Prácticas (Mentalidad Senior)

Saber la sintaxis es solo la mitad de la batalla. Un senior integra el tipado en el flujo de trabajo del equipo.

### 4.1. Configuración de Mypy (`mypy.ini`)

Un proyecto serio necesita un fichero `mypy.ini` para asegurar consistencia. Un punto de partida estricto es fundamental.

```ini
[mypy]
# Nivel de Estrictez
strict = true

# Opciones adicionales recomendadas
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
check_untyped_defs = true
no_implicit_optional = true

# Para bibliotecas sin tipos
[mypy-requests.*]
ignore_missing_imports = true
```

> **Filosofía Senior:** Empieza con `strict = true` en código nuevo. Para código existente, activa las reglas gradualmente para no abrumarte. `disallow_untyped_defs` es una de las reglas más importantes: fuerza a que todas tus funciones estén anotadas.

### 4.2. Stubs (`.pyi`) y `typeshed`

¿Qué pasa con las bibliotecas que no tienen anotaciones?
1.  **Stubs:** Son ficheros (`.pyi`) que contienen solo las signaturas de las funciones y clases con sus tipos, pero sin la implementación.
2.  **Typeshed:** Es un repositorio centralizado de stubs para la librería estándar y muchas bibliotecas de terceros populares. Mypy lo usa por defecto. ([Citation: Typeshed GitHub](https://github.com/python/typeshed))
3.  Si una biblioteca no está en `typeshed`, a menudo puedes instalar un paquete de stubs por separado (ej: `pip install types-requests`).

### 4.3. Integración en el Flujo de Trabajo (CI/CD)

Un senior no confía en que cada desarrollador ejecute Mypy manualmente.
- **Hooks de pre-commit:** Usa `pre-commit` para ejecutar Mypy en los ficheros modificados antes de que se puedan subir al repositorio.
- **Integración Continua (CI):** Añade un paso en tu pipeline (GitHub Actions, GitLab CI, etc.) que ejecute `mypy .` sobre todo el proyecto. Si Mypy falla, el build falla.

### 4.4. Anotaciones en Tiempo de Ejecución

Aunque el propósito principal es el análisis estático, las anotaciones son accesibles en tiempo de ejecución a través del atributo `__annotations__` y la función `typing.get_type_hints()`.

Librerías como **Pydantic** y **FastAPI** llevan esto a otro nivel, usando las anotaciones para hacer validación de datos, serialización y generación de documentación de APIs de forma automática. Este es un uso avanzado y extremadamente poderoso de la infraestructura de tipado.

```python
# Ejemplo con Pydantic (requiere `pip install pydantic`)
from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str = 'John Doe'

# Pydantic usa las anotaciones para validar y coaccionar tipos en tiempo de ejecución
user_data = {"id": 123, "name": "Alice"}
user_obj = User(**user_data)
print(user_obj.name) # "Alice"

invalid_data = {"id": "not-an-int"}
try:
    User(**invalid_data)
except ValueError as e:
    print(e) # Pydantic levanta un error de validación claro
```

---

## Conclusión: La Filosofía del Tipado en Python

Convertirse en un experto en el sistema de tipado de Python no se trata de memorizar cada tipo del módulo `typing`. Se trata de entender la filosofía:

1.  **Claridad sobre Concisión:** Las anotaciones hacen el código más verboso, pero inmensamente más claro. Declaran la *intención* del programador.
2.  **Documentación Viva:** Las anotaciones son la forma más fiable de documentación. A diferencia de los docstrings, no se vuelven obsoletas porque son verificadas por Mypy.
3.  **Refactorización Segura:** El tipado estático es la mejor red de seguridad al refactorizar código. El type checker te dirá inmediatamente si has roto un contrato en otra parte del sistema.
4.  **Herramientas Potenciadas:** Los IDEs como VSCode y PyCharm usan las anotaciones para ofrecer autocompletado de calidad superior, detección de errores en tiempo real y navegación de código inteligente.
5.  **Contratos de Código:** Las anotaciones definen los "contratos" entre funciones y módulos. Esto es fundamental para construir sistemas grandes y mantenibles.

Dominar estos conceptos y, más importante, aplicarlos con pragmatismo y consistencia, es una de las habilidades clave que te llevarán a un nivel de programación senior en el ecosistema de Python moderno.
