Ya vimos cómo empaquetar una aplicación, pero ¿cómo diseñamos un sistema que otros puedan extender? Los `entry points` son la clave para construir ecosistemas de plugins, y es una de las características más potentes y subestimadas que `setuptools` nos ofrece.

# Setup tools

#### **Caso de Estudio: `entry_points` para un sistema de plugins**

Imagina que `textalyzer` quiere permitir que otros paquetes añadan "analizadores" personalizados. Podemos usar `entry_points` para esto.

En nuestro `pyproject.toml`:

```toml
[project.entry-points."textalyzer.analyzers"]
word_count = "textalyzer.core:word_count_analyzer"
char_count = "textalyzer.core:char_count_analyzer"
```

Ahora, otro paquete, `textalyzer-sentiment`, podría definir su propio `pyproject.toml` para registrar un nuevo analizador:

```toml
# En el pyproject.toml de textalyzer-sentiment
[project.entry-points."textalyzer.analyzers"]
sentiment = "textalyzer_sentiment.analyzer:sentiment_analyzer"
```

La aplicación principal `textalyzer` puede descubrir dinámicamente todos los plugins instalados usando la biblioteca `importlib.metadata` (o `pkg_resources` de `setuptools` en versiones antiguas):

```python
# En textalyzer
import importlib.metadata

def get_analyzers():
    analyzers = {}
    for entry_point in importlib.metadata.entry_points(group="textalyzer.analyzers"):
        analyzers[entry_point.name] = entry_point.load()
    return analyzers

# Esto descubrirá 'word_count', 'char_count' y, si está instalado, 'sentiment'.
```

Este patrón es la base de los ecosistemas de plugins de herramientas masivamente populares como `pytest`, `flake8` y muchas otras. Es una de las características más potentes y subestimadas que `setuptools` popularizó.

---

### 5. Nivel Senior - Conceptos Avanzados

Aquí es donde separamos al artesano del aprendiz.

#### **Trade-offs: `pyproject.toml` vs. `setup.py` dinámico**

| Característica        | `pyproject.toml` (Declarativo)                                 | `setup.py` (Imperativo)                                                               | Decisión Senior                                                                                                                                                                                            |
|-----------------------|----------------------------------------------------------------|---------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Seguridad**         | ✅ **Alta:** No hay ejecución de código arbitrario.            | ❌ **Baja:** El script se ejecuta, abriendo un vector de ataque.                       | Usar siempre `pyproject.toml` a menos que sea absolutamente imposible. La seguridad del build es primordial.                                                                                              |
| **Complejidad**       | ✅ **Baja:** Formato estático, fácil de leer y analizar.        | ⚠️ **Variable:** Puede ser simple o un nido de lógica compleja.                        | La simplicidad declarativa gana a largo plazo. Reduce la carga cognitiva y la superficie de errores.                                                                                                     |
| **Flexibilidad**      | ⚠️ **Limitada:** No se puede tener lógica condicional.          | ✅ **Alta:** Permite cualquier lógica de Python, como compilar extensiones C/C++.      | Para la mayoría de los proyectos Python puros, la flexibilidad no es necesaria. Para extensiones C, la lógica de construcción *aún* se puede encapsular en el backend, manteniendo `pyproject.toml` limpio. |
| **Velocidad de Build**| ✅ **Rápida:** El análisis de metadatos es instantáneo.         | ❌ **Lenta:** Requiere ejecutar un proceso de Python para descubrir las dependencias. | En CI/CD, cada segundo cuenta. El enfoque declarativo es significativamente más rápido para la resolución de dependencias.                                                                                   |

**¿Cuándo podrías *necesitar* un `setup.py` dinámico?**
El caso de uso más común es la construcción de **extensiones C/C++/Rust/Fortran**. Aquí, el `setup.py` (o más bien, la lógica invocada por el backend de `setuptools`) necesita interactuar con compiladores, detectar bibliotecas del sistema, etc. Aun así, la mejor práctica es mantener la *declaración* de metadatos en `pyproject.toml` y `setup.cfg`, y usar `setup.py` solo para la lógica de extensión.

> "La PEP 517 fue diseñada para permitir que las herramientas de construcción compitan en la implementación, pero colaboren en la interfaz." — **Dustin Ingram**, *Mantenedor de PyPI y Director de la PSF*

#### **Anti-patrones: Errores Comunes y Cómo Evitarlos**

1.  **El Anti-patrón:** `sudo python setup.py install`.
    *   **Por qué es malo:** Instala el paquete directamente en el Python del sistema, evitando `pip`. Esto rompe la base de datos de paquetes de `pip`, hace imposible la desinstalación y es un desastre de permisos.
    *   **La Solución Senior:** Usar siempre `pip install .` (para una instalación regular) o `pip install -e .` (para una instalación editable/de desarrollo). `pip` orquestará la construcción a través del backend especificado en `pyproject.toml` y gestionará la instalación correctamente.

2.  **El Anti-patrón:** Poner lógica de aplicación en `setup.py`.
    *   **Por qué es malo:** `setup.py` es para construir el paquete, no para ser ejecutado por el usuario final. He visto `setup.py` que intentan crear archivos de configuración en el home del usuario durante la instalación. Esto es frágil y rompe el principio de que los builds deben ser herméticos.
    *   **La Solución Senior:** La lógica de la aplicación (creación de archivos de config, migraciones de BBDD) debe ocurrir en el primer arranque de la aplicación, no durante la instalación del paquete.

3.  **El Anti-patrón:** Dependencias de build en `install_requires`.
    *   **Por qué es malo:** `install_requires` es para dependencias de *tiempo de ejecución*. Si necesitas `cython` o `numpy` *solo para construir* tu extensión C, pero no para usarla, no debería estar ahí.
    *   **La Solución Senior:** Usa la sección `[build-system]` de `pyproject.toml` para especificar las dependencias de construcción. Esto crea un entorno de construcción aislado y limpio.
        ```toml
        [build-system]
        requires = ["setuptools", "wheel", "cython", "numpy"]
        build-backend = "setuptools.build_meta"
        ```

#### **Integración con el Ecosistema Moderno**

Un desarrollador senior no ve a `setuptools` de forma aislada. Lo ve como una pieza de un rompecabezas más grande:

*   **`setuptools` (Backend):** Define *cómo* se construye el paquete.
*   **`pip` (Frontend):** Orquesta el proceso, resuelve dependencias y realiza la instalación.
*   **`tox` / `nox` (Automatización de Tareas):** Crean entornos virtuales, instalan el paquete en modo editable (`pip install -e .`) y ejecutan tests, linters, etc., en un entorno limpio y reproducible.
*   **`pre-commit` (Ganchos de Git):** Ejecuta herramientas (como `black`, `flake8`) antes de cada commit, asegurando la calidad del código que se empaquetará.
*   **CI/CD (GitHub Actions, GitLab CI):** Automatiza la construcción de `wheels` y `sdist` (distribuciones de fuente) y su publicación en PyPI o en un repositorio privado.

Un flujo de trabajo senior integra todas estas herramientas, usando `setuptools` como el motor de construcción subyacente, pero interactuando con él a través de capas de abstracción de alto nivel.

---

### 6. Referencias y Citaciones Académicas

1.  > "A `wheel` is a ZIP-format archive with a specially formatted filename and the `.whl` extension. It is designed to contain all the files for a PEP 376 compatible installation of a package in a way that is very close to the on-disk format." — **Daniel Holth**, *PEP 427 – The Wheel Binary Package Format 1.0* (2012). [https://www.python.org/dev/peps/pep-0427/](https://www.python.org/dev/peps/pep-0427/)

2.  > "This PEP specifies a new configuration file, `pyproject.toml`, for build system dependencies, as opposed to package dependencies. The new file is also capable of storing any tool-specific configuration for a Python project." — **Brett Cannon, Nathaniel J. Smith**, *PEP 518 – Specifying Minimum Build System Requirements for Python Projects* (2015). [https://www.python.org/dev/peps/pep-0518/](https://www.python.org/dev/peps/pep-0518/)

3.  > "The fundamental problem that this PEP is trying to solve is that there is no single, standard way to specify the project metadata in a tool-agnostic way." — **Brett Cannon, Paul Gaborit, Ofek Zvi, Pradyun Gedam, Tzu-Ping Chung, Stephen J. Turnbull**, *PEP 621 – Storing project metadata in pyproject.toml* (2020). [https://www.python.org/dev/peps/pep-0621/](https://www.python.org/dev/peps/pep-0621/)

4.  > "The `distutils` package provides support for building and installing additional modules into a Python installation. The new modules may be 100%-pure Python, or may be extension modules written in C, or may be collections of Python packages which include modules coded in both Python and C." — **Python Software Foundation**, *distutils — Building and installing Python modules Documentation* (Consultado en 2023). [https://docs.python.org/3/library/distutils.html](https://docs.python.org/3/library/distutils.html)

5.  > "Setuptools is a fully-featured, actively-maintained, and stable library for packaging Python projects. It was for a long time the de-facto standard for Python packaging, and is still a popular choice." — **Python Packaging Authority (PyPA)**, *Setuptools Documentation* (Consultado en 2023). [https://setuptools.pypa.io/](https://setuptools.pypa.io/)

6.  > "Dependency hell is a colloquial term for the frustration of some software users who have installed software packages which have dependencies on specific versions of other software packages." — **Coutts, D., Wallace, C., & Zelfim, A.**, *The Cabal: a framework for packaging Haskell software* (2007). (Aunque sobre Haskell, define el problema universal que `setuptools` ayudó a mitigar en Python).

7.  > "The `entry_points` keyword provides a mechanism for a distribution to advertise components it provides to be discovered and used by other code." — **Python Packaging Authority (PyPA)**, *Setuptools Developer's Guide, Entry Points* (Consultado en 2023). [https://setuptools.pypa.io/en/latest/userguide/entry_point.html](https://setuptools.pypa.io/en/latest/userguide/entry_point.html)

8.  > "Monkey-patching can be useful for bug-fixing or extending a library when you don't have access to the source code. However, it can lead to problems in debugging and conflicts between different patches." — **Martelli, A., Ravenscroft, A., & Ascher, D.**, *Python Cookbook, 3rd Edition* (2013). (Contextualiza la controvertida técnica inicial de `setuptools` sobre `distutils`).

9.  > "The Python Package Index, affectionately known as the Cheese Shop, is a repository of software for the Python programming language." — **Python Software Foundation**, *PyPI History* (parafraseado de la historia oral de la comunidad). [https://pypi.org/](https://pypi.org/)

10. > "Reproducible builds are a set of software development practices that create a verifiable path from human-readable source code to the binary code used by computers." — **Reproducible Builds Project**, *Homepage* (Consultado en 2023). (El movimiento hacia `pyproject.toml` es un paso clave hacia builds más reproducibles en Python). [https://reproducible-builds.org/](https://reproducible-builds.org/)