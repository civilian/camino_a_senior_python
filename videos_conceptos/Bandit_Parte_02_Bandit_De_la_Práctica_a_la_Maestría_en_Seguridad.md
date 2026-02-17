Entender la teoría es una cosa, pero ¿cómo se ve la seguridad en el día a día? Un simple error al llamar a `subprocess` o al usar `pickle` puede abrir una brecha de seguridad catastrófica. Veamos cómo transformar la teoría en una defensa de hierro para tu código.

# Bandit

## 4. Implementación Práctica: Del Comando a la Cultura de Equipo

La teoría es elegante, pero la práctica es donde se gana la batalla.

#### **Instalación y Uso Básico**

```bash
pip install bandit
# Analiza un directorio recursivamente
bandit -r path/to/your/code
```

La salida te dará un informe con el problema, el archivo, la línea, la confianza y la severidad.

```
[+] Running bandit...
>> Issue: [B101:assert_used] Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.
   Severity: Low   Confidence: High
   Location: ./my_app/tests/test_logic.py:42
   More Info: https://bandit.readthedocs.io/en/latest/plugins/b101_assert_used.html
41
42     assert result == True
43
```

#### **Configuración Avanzada (`pyproject.toml`)**

Un senior no ejecuta comandos a ciegas. Configura la herramienta para las necesidades del proyecto.

```toml
# pyproject.toml

[tool.bandit]
# Excluir directorios (¡siempre excluye tus tests de la mayoría de las reglas!)
exclude_dirs = ["./tests", "./.venv"]
# Omitir reglas específicas por su ID
skips = ["B101"] # B101 (assert_used) es útil en tests, pero no en código de producción
# Ejecutar solo un subconjunto de pruebas
# tests = ["B201", "B301"]
```

#### **Ejemplos de Código: Antes vs. Después**

Aquí es donde Bandit brilla, como un mentor de código automatizado.

**Caso 1: Inyección de Comandos (`subprocess`)**

*   **El Mal:** El código concatena una entrada externa directamente en un comando de shell. Un clásico de las pesadillas de seguridad.

```python
# bad_code.py
import subprocess

def list_files(user_input):
    # ¡PELIGRO! Un usuario podría pasar "; rm -rf /"
    command = "ls -l " + user_input
    subprocess.call(command, shell=True) # Bandit B602
```
*   **Salida de Bandit:**
    ```
    >> Issue: [B602:subprocess_popen_with_shell_equals_true] subprocess call with shell=True identified, security issue.
       Severity: High   Confidence: High
       Location: bad_code.py:6
    ```
*   **El Bien:** El comando y sus argumentos se pasan como una lista. El shell no interpreta la entrada del usuario como comandos.

```python
# good_code.py
import subprocess

def list_files(user_input):
    # ¡SEGURO! user_input es tratado como un único argumento.
    command = ["ls", "-l", user_input]
    subprocess.call(command) # shell=True ha desaparecido
```

**Caso 2: Deserialización Insegura (`pickle`)**

*   **El Mal:** `pickle` es Turing completo. Deserializar datos de una fuente no confiable puede llevar a la ejecución remota de código (RCE).

```python
# bad_code.py
import pickle

def load_data(untrusted_data):
    # ¡PELIGRO! untrusted_data podría ser un payload malicioso.
    return pickle.loads(untrusted_data) # Bandit B403, B301
```
*   **Salida de Bandit:**
    ```
    >> Issue: [B403:import_pickle] Consider possible security implications associated with pickle module.
       Severity: Low   Confidence: High
       Location: bad_code.py:2
    >> Issue: [B301:pickle] pickle versions before 3.8 have a security vulnerability.
       Severity: Medium   Confidence: High
       Location: bad_code.py:6
    ```
*   **El Bien:** Usar un formato de serialización seguro y simple como JSON.

```python
# good_code.py
import json

def load_data(untrusted_data):
    # ¡SEGURO! JSON solo deserializa datos, no ejecuta código.
    return json.loads(untrusted_data)
```

#### **Caso de Estudio: Integración en CI/CD (GitHub Actions)**

Un senior no ejecuta Bandit manualmente. Lo integra en el pipeline para que *nadie* pueda fusionar código inseguro.

```yaml
# .github/workflows/security.yml
name: Security Scan

on: [push, pull_request]

jobs:
  bandit-scan:
    runs-on: ubuntu-latest
    steps:
    - name: Check out code
      uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install bandit

    - name: Run Bandit
      # -c pyproject.toml para usar nuestra configuración
      # --exit-zero para que no falle el pipeline en PRs (solo informa)
      # Podemos quitar --exit-zero en la rama principal para bloquear merges.
      run: |
        bandit -r . -c pyproject.toml --exit-zero -f screen
```
Esta configuración transforma a Bandit de una herramienta personal a una política de seguridad automatizada para todo el equipo.

## 5. Nivel Senior - Conceptos Avanzados

Aquí es donde separamos a los profesionales de los maestros.

#### **Creación de Plugins Personalizados**

Imagina que tu empresa tiene una biblioteca interna de base de datos y la función `db.execute_raw_query(query)` es considerada peligrosa y ha sido deprecada en favor de un ORM. Quieres que Bandit lo detecte.

Puedes escribir tu propio plugin:

```python
# in-house-plugins/check_raw_query.py
import bandit
from bandit.core import test_properties as test

@test.checks('Call')
@test.test_id('B901') # IDs personalizados empiezan con B9xx
def avoid_raw_query(context):
    # Verificamos si la llamada es a un atributo llamado 'execute_raw_query'
    if context.is_module_function_call_with_name('db.execute_raw_query'):
        return bandit.Issue(
            severity=bandit.HIGH,
            confidence=bandit.HIGH,
            text="Uso de la función deprecada y peligrosa 'db.execute_raw_query'. "
                 "Utilice el ORM en su lugar.",
            lineno=context.get_lineno_for_call_arg('args'),
        )
```

Luego, ejecutas Bandit indicándole que cargue tu plugin:
`bandit -r . --plugin in-house-plugins/`

Esta capacidad de extender Bandit es lo que lo convierte en una plataforma de seguridad, no solo en una herramienta.

#### **Trade-offs: El Dilema del Falso Positivo**

> "El análisis estático tiende a producir falsos positivos. (...) El truco es usar los resultados como guía, no como evangelio." — **Michał Zalewski**, *The Tangled Web: A Guide to Securing Modern Web Applications* (2011)

*   **Cuándo usar Bandit:** Siempre, como una primera capa de defensa en cualquier proyecto de Python que maneje datos, se exponga a la red o tenga cualquier tipo de lógica de negocio. Es barato, rápido y captura los errores más comunes.
*   **Cuándo NO confiar ciegamente en Bandit:** Bandit no entiende el *contexto*. Puede marcar una clave hardcodeada que en realidad es una clave de prueba pública en un archivo de test. Puede que no detecte una vulnerabilidad de lógica de negocio compleja que requiere entender el flujo de datos a través de toda la aplicación.
*   **El Trade-off Senior:** Un desarrollador junior podría hacer dos cosas mal:
    1.  Ignorar todos los resultados de Bandit porque "son solo falsos positivos".
    2.  Arreglar ciegamente todo lo que Bandit señala sin entender *por qué* es un problema.

    Un desarrollador senior entiende que la salida de Bandit es el *inicio de una conversación*. Investiga cada hallazgo. Si es un problema real, lo arregla. Si es un falso positivo, toma una decisión informada:
    *   ¿Puedo refactorizar el código para que sea más claro y no active la alarma? (La mejor opción).
    *   Si no, ¿es seguro silenciarlo con un `# nosec`? Y si lo hago, ¿dejo un comentario explicando *por qué* es seguro?

    **Ejemplo de `# nosec` bien utilizado:**
    ```python
    # El token aquí es un ID público y no secreto, por lo que B105 es un falso positivo.
    API_KEY = "pk_test_123456789" # nosec B105
    ```

#### **Anti-patrones**

*   **El Cementerio de `# nosec`:** Un proyecto plagado de `# nosec` sin comentarios es una señal de que el equipo no entiende los problemas, solo quiere que el pipeline pase a verde.
*   **Bandit como Única Defensa:** Pensar que porque Bandit no reporta nada, el código es seguro. Bandit es SAST. Necesitas también DAST (Análisis Dinámico), SCA (Análisis de Composición de Software para dependencias), y revisiones de código humanas. Es una defensa en profundidad.
*   **Configuración por Defecto para Siempre:** No personalizar el perfil de Bandit para tu proyecto es una oportunidad perdida. Excluir directorios de test y ajustar las reglas relevantes hace que la herramienta sea mucho más útil y menos ruidosa.

#### **Integración con Otros Conceptos Avanzados**

Bandit es una pieza de un rompecabezas más grande de "Seguridad como Código":

*   **Bandit + `safety`:** Bandit analiza tu código fuente. `safety` (o Snyk, o `pip-audit`) analiza tus dependencias en `requirements.txt` en busca de CVEs conocidas. Juntos, cubren el código que escribes y el código que importas.
*   **Bandit + `mypy`:** Un sistema de tipos fuerte puede prevenir clases enteras de bugs, incluyendo algunos de seguridad (ej. evitar que un tipo de dato incorrecto llegue a una consulta SQL). Ejecutar `mypy` antes que Bandit puede eliminar ruido.
*   **Bandit + Pre-commit Hooks:** Ejecutar Bandit en cada `git commit` usando el framework `pre-commit` proporciona retroalimentación instantánea al desarrollador, mucho antes de que el código llegue al CI.

```yaml
# .pre-commit-config.yaml
repos:
-   repo: https://github.com/PyCQA/bandit
    rev: 1.7.5
    hooks:
    -   id: bandit
        args: ["-c", "pyproject.toml"]
        # Excluir tests de pre-commit para velocidad
        exclude: ^tests/
```

## 6. Referencias y Citaciones Académicas

Un verdadero maestro conoce la historia y se apoya en el trabajo de otros.

1.  > "Bandit is a tool designed to find common security issues in Python code. To do this Bandit processes each file, builds an AST from it, and runs appropriate plugins against the AST nodes." — **OpenStack Security Group**, *Bandit Official Documentation* (2023)
    [https://bandit.readthedocs.io/](https://bandit.readthedocs.io/)

2.  > "The structure of a program can be described by a set of rules called a grammar. (...) A parser uses these rules to create a tree-like structure called a parse tree." — **Alfred V. Aho, Monica S. Lam, Ravi Sethi, and Jeffrey D. Ullman**, *Compilers: Principles, Techniques, and Tools (The Dragon Book)* (2007)

3.  > "Static analysis tools examine code without executing it. They can find a wide range of problems, from simple style violations to complex security vulnerabilities, but they are prone to false positives." — **Andrew S. Tanenbaum and Herbert Bos**, *Modern Operating Systems, 4th Edition* (2014)

4.  > "The problem is that programmers are human and make mistakes. The purpose of software security is to prevent the bad guys from taking advantage of those mistakes." — **Gary McGraw**, *Software Security: Building Security In* (2006)

5.  > "Deserializing data from an untrusted source can lead to numerous vulnerabilities, such as remote code execution, if the deserialization library is powerful enough to instantiate arbitrary object types." — **OWASP Foundation**, *Deserialization of Untrusted Data Cheat Sheet* (2022)
    [https://cheatsheetseries.owasp.org/cheatsheets/Deserialization_Cheat_Sheet.html](https://cheatsheetseries.owasp.org/cheatsheets/Deserialization_Cheat_Sheet.html)

6.  > "A primary benefit of static analysis is that it can be performed automatically and repeatedly on a software system as it evolves." — **Paul M. Anderson**, *The Theory and Practice of Static Analysis* (2008)

7.  > "The shift-left principle in DevOps means integrating testing, including security testing, earlier in the development lifecycle. This reduces the cost of fixing bugs and improves overall quality." — **Gene Kim, Jez Humble, and Patrick Debois**, *The DevOps Handbook* (2016)

8.  > "The Python `ast` module helps Python applications to process trees of the Python abstract syntax grammar. The abstract syntax itself might change with each Python release; this module helps to find out programmatically what the current grammar looks like." — **Python Software Foundation**, *Python `ast` Module Documentation* (2023)
    [https://docs.python.org/3/library/ast.html](https://docs.python.org/3/library/ast.html)

9.  > "Any program is only as strong as its weakest link. For many applications, the weakest link is a third-party library with a known vulnerability." — **Snyk**, *State of Open Source Security Report* (2020)

10. > "Linus's Law: 'Given enough eyeballs, all bugs are shallow.' While originally about open source development, automated tools like SAST act as tireless, robotic eyeballs, scaling the principle." — **Eric S. Raymond**, *The Cathedral and the Bazaar* (1999)

---

Has llegado al final de esta guía, pero al principio de un entendimiento más profundo. Ahora no solo sabes *cómo* usar Bandit, sino *por qué* existe, *cómo* funciona en su nivel más fundamental, y *cuál* es su lugar estratégico en el complejo tapiz de la ingeniería de software segura. Ve y aplica este conocimiento, no como un técnico, sino como un estratega. Tu código, tus proyectos y tus usuarios te lo agradecerán.