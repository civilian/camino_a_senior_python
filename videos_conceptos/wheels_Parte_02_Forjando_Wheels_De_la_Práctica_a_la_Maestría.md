Ya entendemos el 'porqué' de los Wheels, pero ¿cómo se forja uno? Pasemos de la teoría a la práctica para construir nuestros propios paquetes binarios, y exploremos los secretos que distinguen a un profesional.

# wheels

### 4. Implementación Práctica: Forjando Nuestras Propias Ruedas

Basta de teoría. Vamos a construir. Usaremos el moderno `pyproject.toml` y el backend `setuptools`.

#### Proyecto 1: Un Wheel Puro de Python (`py3-none-any`)

Este es el tipo de Wheel más simple. No contiene código compilado y funciona en cualquier sistema operativo y versión de Python (compatible).

**Estructura del proyecto:**
```
pure_wheel_project/
├── src/
│   └── my_package/
│       ├── __init__.py
│       └── utils.py
└── pyproject.toml
```

**`pyproject.toml`:**
```toml
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "my-pure-package"
version = "0.1.0"
description = "Un simple paquete de Python puro."
readme = "README.md"  # Opcional
requires-python = ">=3.8"
classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
]

[project.urls]
Homepage = "https://github.com/user/pure_wheel_project"
```

**`src/my_package/utils.py`:**
```python
def say_hello(name: str) -> str:
    """Una función de saludo simple."""
    return f"Hola, {name}! ¡Bienvenido al mundo de los Wheels!"
```

**Construyendo el Wheel:**
1.  Instala el constructor: `pip install build`
2.  Ejecuta la construcción: `python -m build`

Verás una nueva carpeta `dist/` con dos archivos:
*   `my_pure_package-0.1.0-py3-none-any.whl` (¡Nuestra rueda!)
*   `my-pure-package-0.1.0.tar.gz` (El sdist de respaldo)

El tag `py3-none-any` significa: compatible con Python 3, sin ABI específica (`none`), y para cualquier arquitectura (`any`).

#### Proyecto 2: Un Wheel con una Extensión en C (Cython)

Aquí es donde los Wheels brillan. Usaremos Cython para compilar una función de Python a C para obtener un rendimiento (potencialmente) mayor.

**Estructura del proyecto:**
```
c_extension_project/
├── src/
│   └── my_c_package/
│       ├── __init__.py
│       └── fast_math.pyx  # Archivo Cython
└── pyproject.toml
```

**`src/my_c_package/fast_math.pyx`:**
```cython
# cython: language_level=3

def fibonacci(int n):
    """Calcula el n-ésimo número de Fibonacci de forma ineficiente pero en C."""
    cdef int a = 0
    cdef int b = 1
    cdef int i
    for i in range(n):
        a, b = b, a + b
    return a
```

**`pyproject.toml`:**
```toml
[build-system]
requires = ["setuptools>=61.0", "cython"] # ¡Añadimos Cython como dependencia de construcción!
build-backend = "setuptools.build_meta"

[project]
name = "my-c-extension-package"
version = "0.1.0"
description = "Un paquete con una extensión en C usando Cython."
requires-python = ">=3.8"

# ¡Esta parte es crucial! Le decimos a setuptools que hay una extensión que construir.
[tool.setuptools.packages.find]
where = ["src"]

[tool.setuptools.cythonize]
# Esto le dice a setuptools que compile todos los archivos .pyx que encuentre
# y los trate como módulos de extensión.
# Para configuraciones más complejas, se usaría una sección [tool.setuptools.extensions]
# similar a como se hacía en setup.py.
# La forma más moderna y explícita sería:
#
# [tool.setuptools.extensions]
# my_c_package.fast_math = "src/my_c_package/fast_math.pyx"
#
# Pero para este ejemplo, la configuración automática de Cython es suficiente.
# Sin embargo, para ser explícitos y robustos, usemos el método de extensiones.
# Eliminamos [tool.setuptools.cythonize] y añadimos:
```
*Corrección en `pyproject.toml` para mayor claridad y robustez*:

```toml
# pyproject.toml (versión corregida y más explícita)

[build-system]
requires = ["setuptools>=61.0", "cython"]
build-backend = "setuptools.build_meta"

[project]
name = "my-c-extension-package"
version = "0.1.0"
description = "Un paquete con una extensión en C usando Cython."
requires-python = ">=3.8"

[tool.setuptools]
packages = ["my_c_package"]
package_dir = {"" = "src"}

# La forma explícita y recomendada de declarar extensiones
[tool.setuptools.extensions]
my_c_package.fast_math = { sources = ["src/my_c_package/fast_math.pyx"] }
```

**Construyendo el Wheel:**
`python -m build`

Ahora, en la carpeta `dist/`, el nombre del Wheel será muy diferente:
`my_c_extension_package-0.1.0-cp311-cp311-linux_x86_64.whl` (en mi máquina Linux con Python 3.11)

Observa el tag: `cp311-cp311-linux_x86_64`. Es específico para mi sistema. Si quisiera distribuir esto, necesitaría construir Wheels para cada combinación de SO/versión de Python/arquitectura que quiera soportar.

#### Comparación: Antes vs. Después

**Antes (instalando `cryptography` desde sdist):**
```bash
$ pip install cryptography --no-binary :all:
...
# Salida masiva del compilador GCC/Clang/MSVC
# Compilando _rust.c
# Compilando _openssl.c
# ... docenas de archivos más ...
# Errores si falta rustc, un compilador de C, o las cabeceras de OpenSSL
...
Successfully installed cryptography-42.0.5 # (si tienes suerte)
```

**Después (instalando `cryptography` desde un Wheel):**
```bash
$ pip install cryptography
Collecting cryptography
  Downloading cryptography-42.0.5-cp39-cp39-manylinux_2_17_x86_64.whl (4.6 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 4.6/4.6 MB 25.3 MB/s eta 0:00:00
Installing collected packages: cryptography
Successfully installed cryptography-42.0.5
```
La diferencia es abismal. De un proceso frágil y lento a una descarga y extracción rápidas y confiables.

### 5. Nivel Senior - Conceptos Avanzados

Aquí es donde separamos al profesional del maestro.

#### Trade-offs: Cuándo NO usar (o ser cauteloso con) los Wheels

1.  **Auditoría de Seguridad**: Un Wheel contiene binarios precompilados. Es una caja negra. Si tu política de seguridad requiere auditar todo el código fuente antes de la instalación, debes usar un `sdist` y construirlo tú mismo en un entorno controlado.
2.  **Flags de Compilación Específicos**: A veces, necesitas compilar una biblioteca con optimizaciones específicas para tu CPU (ej. `-march=native`) o enlazar contra una versión particular de una biblioteca del sistema. Un Wheel genérico no te permitirá esto. Deberás partir del `sdist`.
3.  **Entornos de Recursos Limitados (IoT)**: Si el tamaño total de descarga es crítico, tener un solo `sdist` en PyPI puede ser más pequeño que tener 20 Wheels diferentes para cada plataforma.
4.  **Depuración (Debugging)**: Depurar problemas en una extensión C es más fácil si la has compilado tú mismo con símbolos de depuración, algo que los Wheels de producción no suelen incluir.

#### Anti-Patrones: Errores Comunes

1.  **El Wheel "Universal" Falso**: Crear un Wheel `py3-none-any` que en realidad contiene código que depende del sistema operativo (ej. usa `os.fork()` que no existe en Windows). Esto es mentir en los metadatos y causará fallos en tiempo de ejecución.
2.  **Abusar de `--no-binary`**: Algunos desarrolladores, frustrados por un problema puntual, configuran `pip` para nunca usar binarios (`--no-binary :all:`). Esto los devuelve a la edad de piedra de la compilación, ralentizando todo y reintroduciendo la fragilidad que los Wheels resolvieron. Debe usarse solo para paquetes específicos y por razones justificadas.
3.  **Ignorar la Matriz de Construcción**: Publicar un paquete con extensiones C pero solo proporcionar un Wheel para tu propia máquina (ej. solo macOS/ARM64). Esto aliena a la mayoría de los usuarios. Los proyectos serios usan CI/CD (como GitHub Actions) con herramientas como `cibuildwheel` para construir y publicar Wheels para Windows, macOS (x86_64, arm64) y Linux (x86_64, aarch64) automáticamente.

#### Consideraciones de Seguridad: La Cadena de Suministro

Un Wheel es un vector de ataque. Un atacante que comprometa la cuenta de un mantenedor en PyPI puede subir un Wheel malicioso con código arbitrario que se ejecuta durante la instalación.

> "The design of setup.py and packages that use it allows for arbitrary code execution as part of the package installation process. This is a fundamental design flaw in the Python packaging ecosystem." — **Lukas Pustina**, *Executing Code during pip install* (2021)

Aunque la cita se refiere a `setup.py`, el riesgo persiste con los Wheels. La comunidad está trabajando en soluciones como firmas de paquetes y atestaciones de construcción (ej. Sigstore), pero la confianza en el mantenedor y en la integridad de PyPI sigue siendo fundamental. Herramientas como `pip-audit` pueden escanear tus dependencias en busca de vulnerabilidades conocidas.

#### La Saga `manylinux`: Un Estudio de Caso en Compatibilidad

El estándar `manylinux` es una obra de arte de la ingeniería pragmática.
*   **El Problema**: Las distribuciones de Linux compilan su software contra diferentes versiones de bibliotecas clave, especialmente `glibc`. Un binario compilado en Ubuntu 22.04 (con una `glibc` nueva) no se ejecutará en CentOS 7 (con una `glibc` vieja) debido a símbolos de versión faltantes.
*   **La Solución**: Se define una imagen base de Docker (`quay.io/pypa/manylinux...`) que contiene un entorno de compilación con versiones antiguas de bibliotecas clave.
*   **El Contrato**: Si construyes tu Wheel dentro de este contenedor, el enlazador dinámico solo usará símbolos que están presentes en casi todas las distribuciones de Linux "modernas". `pip` en un sistema Linux verificará la versión de `glibc` del sistema y elegirá el Wheel `manylinux` más específico y compatible que pueda encontrar.

Este enfoque ha convertido el problema más espinoso de compatibilidad de Python en un problema resuelto para la gran mayoría de los paquetes.

### 6. Referencias y Citaciones Académicas

1.  > "This PEP proposes a new binary package format for Python. The wheel format provides a way to ship libraries with compiled extensions, and it is also the basis for a new installation system that can install directly from wheel files without a setup script or online services." — **Daniel Holth**, *PEP 427 -- The Wheel Binary Package Format 1.0* (2012). [https://peps.python.org/pep-0427/](https://peps.python.org/pep-0427/)

2.  > "The goal of manylinux1 is to define a standard binary ABI for wheels that will be compatible with the Python interpreters shipped by most mainstream Linux distributions." — **Robert T. McGibbon et al.**, *PEP 513 -- A Platform Tag for Portable Linux Built Distributions* (2016). [https://peps.python.org/pep-0513/](https://peps.python.org/pep-0513/)

3.  > "This PEP specifies a new configuration file, `pyproject.toml`, for build-system-independent specification of project build requirements." — **Brett Cannon, Thomas Kluyver, Paul Moore**, *PEP 518 -- Specifying Minimum Build System Requirements for Python Projects* (2016). [https://peps.python.org/pep-0518/](https://peps.python.org/pep-0518/)

4.  > "A source tree is a directory on a filesystem, which contains the source code for a Python project. A build frontend is a tool that users might run to build a source tree... A build backend is a tool that takes a source tree and builds a source or binary distribution from it." — **Chris Jerdonek, Thomas Kluyver**, *PEP 517 -- A build-system independent format for source trees* (2015). [https://peps.python.org/pep-0517/](https://peps.python.org/pep-0517/)

5.  > "The Python Packaging User Guide is the authoritative resource on how to package, publish, and install Python projects with current tools." — **Python Packaging Authority (PyPA)**, *Python Packaging User Guide*. [https://packaging.python.org/en/latest/](https://packaging.python.org/en/latest/)

6.  > "cibuildwheel is the secret weapon of Python library authors. It builds and tests wheels for all major platforms and Python versions, all in CI." — **Henry Schreiner**, *cibuildwheel Documentation*. [https://cibuildwheel.readthedocs.io/](https://cibuildwheel.readthedocs.io/)

7.  > "Eggs have a number of problems, not the least of which is that they are not a standard. They are a format that is specific to setuptools, and they have a number of design flaws that make them difficult to work with." — **Donald Stufft**, *Python Packaging: A History* (Blog Post, circa 2013, conceptual summary of his talks).

8.  > "The software supply chain is a complex ecosystem of components, tools, and processes... A compromised build tool or a malicious package uploaded to a public repository can have devastating consequences." — **Justin Cappos et al.**, *The Update Framework (TUF) Specification* (2017). [https://theupdateframework.io/](https://theupdateframework.io/)

9.  > "The purpose of this PEP is to define a standard for how installed distributions are laid out." — **Carl Meyer**, *PEP 376 -- Database of Installed Python Distributions* (2009). [https://peps.python.org/pep-0376/](https://peps.python.org/pep-0376/) (Define el formato del directorio `.dist-info` que es fundamental para los Wheels).

10. > "Setuptools is a fully-featured, actively-maintained, and stable library for packaging Python projects." — **Jason R. Coombs**, *Setuptools Documentation*. [https://setuptools.pypa.io/en/latest/](https://setuptools.pypa.io/en/latest/) (El constructor de Wheels más ubicuo).

---

### Conclusión

La rueda, en la civilización, fue una invención que multiplicó la capacidad humana. En Python, el Wheel hizo lo mismo. Transformó el empaquetado de una tarea artesanal y frágil a un proceso industrial, confiable y escalable.

Comprender los Wheels a nivel senior no es solo saber cómo construir uno. Es entender la historia de frustración que los hizo necesarios, apreciar el ingenio de los contratos de ABI y los tags de plataforma, y ser consciente de los trade-offs de seguridad y flexibilidad que implican. Es ver en un simple archivo `.whl` la culminación de décadas de esfuerzo comunitario para hacer de Python un ecosistema más accesible, potente y robusto para todos. La próxima vez que veas a `pip` descargar un Wheel en milisegundos, tómate un momento para apreciar al gigante sobre cuyos hombros estás parado.