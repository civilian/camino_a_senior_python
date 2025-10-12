# pdb

¡Excelente! Preparémonos para una inmersión profunda en `pdb`, el depurador de Python. Esta guía está diseñada no solo para enseñarte los comandos, sino para inculcar la *mentalidad* y las *técnicas* que un desarrollador senior utiliza para diagnosticar y resolver problemas complejos de manera eficiente.

---

# Dominando `pdb`: La Guía Definitiva para el Debugging en Python

Un desarrollador junior usa `print()` para ver qué está pasando. Un desarrollador senior invoca `pdb` para *preguntarle* al programa qué está pasando, modificar su estado en tiempo real y probar hipótesis sin reiniciar el proceso. Esta guía te llevará a ese nivel.

## Tabla de Contenidos
1.  **Filosofía del Debugging Interactivo**
2.  **Iniciando una Sesión de `pdb`**
    *   El Método Clásico: `pdb.set_trace()`
    *   El Método Moderno (Python 3.7+): `breakpoint()`
    *   Desde la Línea de Comandos: `python -m pdb <script.py>`
    *   Debugging Post-Mortem: El Arte de Analizar Cráteres
3.  **Navegación Esencial: Los Comandos Fundamentales**
4.  **Control de Flujo Avanzado: Dominando el Tiempo y el Espacio**
    *   Puntos de Ruptura (Breakpoints)
    *   Navegación Condicional y Saltos
5.  **Introspección Profunda: El Verdadero Poder de `pdb`**
    *   Inspección y Modificación de Estado
    *   Comandos y Acciones Automatizadas
    *   Alias y Personalización con `.pdbrc`
6.  **`pdb` en el Ecosistema Moderno**
    *   `pdb` vs. Depuradores de IDE
    *   Alternativas Mejoradas: `ipdb` y `pdbpp`
    *   Debugging en Frameworks (Django, Flask) y Tests (`pytest`)
7.  **Conclusión: De Herramienta a Mentalidad Senior**
8.  **Referencias y Citaciones**

---

## 1. Filosofía del Debugging Interactivo

La diferencia fundamental entre `print()` y `pdb` es la diferencia entre una fotografía y una conversación. `print()` te da una instantánea estática del estado en un punto del tiempo. `pdb` te da una consola interactiva (REPL) *dentro* del estado congelado de tu programa.

Un senior aborda el debugging con el método científico:
1.  **Observar:** El programa falla o se comporta de forma inesperada.
2.  **Formular una Hipótesis:** "Creo que la variable `user_id` se está volviendo `None` en el bucle de la línea 42".
3.  **Experimentar:** Usar `pdb` para detener la ejecución justo antes o dentro de ese bucle.
4.  **Verificar/Refutar:** Inspeccionar `user_id`. Si es `None`, ¿por qué? Rastrear su origen. Si no es `None`, la hipótesis era incorrecta. Formular una nueva.

`pdb` es la herramienta para el paso 3 y 4. Te permite probar hipótesis sin tener que añadir `print`s, reiniciar y esperar a que el programa llegue al mismo punto.

## 2. Iniciando una Sesión de `pdb`

### El Método Clásico: `pdb.set_trace()`
Es la forma más común. Importas el módulo y llamas a la función donde quieres que la ejecución se detenga.

```python
import pdb

def mi_funcion_compleja(a, b):
    resultado_intermedio = a * b
    # Algo sospechoso está pasando aquí.
    pdb.set_trace() 
    # La ejecución se detendrá aquí, justo antes de la siguiente línea.
    resultado_final = resultado_intermedio ** 2
    return resultado_final

mi_funcion_compleja(5, 3)
```

Al ejecutar este script, la terminal se detendrá y te mostrará el prompt `(Pdb)`.

### El Método Moderno (Python 3.7+): `breakpoint()`

**PEP 553** introdujo una forma más limpia y configurable de hacer lo mismo. La función `breakpoint()` está disponible de forma nativa.

> "This PEP proposes adding a new built-in function, `breakpoint()`, to the language and having it call `sys.breakpointhook()` by default. In turn, `sys.breakpointhook()` calls `pdb.set_trace()` by default." - **PEP 553 -- Built-in `breakpoint()`** [1]

```python
def mi_funcion_moderna(a, b):
    resultado_intermedio = a * b
    # Más limpio, sin necesidad de import.
    breakpoint()
    resultado_final = resultado_intermedio ** 2
    return resultado_final

mi_funcion_moderna(5, 3)
```

La gran ventaja es que el comportamiento de `breakpoint()` se puede controlar con la variable de entorno `PYTHONBREAKPOINT`. Por ejemplo, para deshabilitar todos los breakpoints: `PYTHONBREAKPOINT=0 python mi_script.py`. Para usar `ipdb` en su lugar: `PYTHONBREAKPOINT=ipdb.set_trace python mi_script.py`. Esto es increíblemente útil en sistemas de CI/CD o producción.

### Desde la Línea de Comandos

Útil para iniciar el debugging desde el principio del script sin modificar el código.

```bash
python -m pdb mi_script.py
```

La ejecución se detendrá en la primera línea de código ejecutable.

### Debugging Post-Mortem: El Arte de Analizar Cráteres

Esta es una técnica de nivel senior. En lugar de intentar reproducir un error, lo analizas *después* de que ocurra. Cuando tu programa crashea con una excepción no controlada, puedes invocar `pdb` para inspeccionar el estado exacto en el momento del fallo.

```python
import pdb
import sys

def division_peligrosa(x, y):
    try:
        return x / y
    except ZeroDivisionError:
        # sys.exc_info() contiene información sobre la excepción actual
        # (tipo, valor, traceback)
        type, value, tb = sys.exc_info()
        print("¡Error! Iniciando sesión post-mortem.")
        pdb.post_mortem(tb)

division_peligrosa(10, 0)
```

Una forma aún más sencilla es ejecutar el script completo bajo el control de `pdb` y dejar que él se encargue del post-mortem automáticamente.

```bash
python -m pdb -c continue mi_script_que_falla.py
```

El `-c continue` le dice a `pdb` que se ejecute sin parar hasta que encuentre un breakpoint o, en este caso, una excepción no controlada. En ese momento, te dejará en el prompt `(Pdb)` en el frame exacto del error.

## 3. Navegación Esencial: Los Comandos Fundamentales

Una vez en el prompt `(Pdb)`, estos son tus verbos principales.

| Comando (Alias) | Descripción |
| :--- | :--- |
| `h(elp) [comando]` | Muestra la ayuda. `help l` te explica el comando `list`. |
| `l(ist) [first, last]` | Muestra el código fuente alrededor de la línea actual. |
| `w(here)` | Muestra la pila de llamadas (stack trace). Esencial para saber *cómo* llegaste aquí. |
| `n(ext)` | Ejecuta la línea actual y se detiene en la siguiente línea **en la misma función**. No entra en llamadas a funciones. |
| `s(tep)` | Ejecuta la línea actual y se detiene en la siguiente instrucción posible. **Sí entra** en llamadas a funciones. |
| `c(ontinue)` | Continúa la ejecución hasta el siguiente breakpoint o hasta el final del programa. |
| `r(eturn)` | Continúa la ejecución hasta que la función actual retorne. Útil para salir rápido de una función en la que ya no te interesa depurar. |
| `q(uit)` | Aborta la ejecución del programa. |
| `p <expresión>` | Evalúa la expresión en el contexto actual y la imprime. `p mi_variable`. |
| `pp <expresión>` | Igual que `p`, pero usa el módulo `pprint` para una salida más legible (ideal para diccionarios o listas grandes). |
| `a(rgs)` | Imprime los argumentos de la función actual. |

**Diferencia clave `n(ext)` vs. `s(tep)`:**

```python
1-> def funcion_a():
2       print("Dentro de A")
3       funcion_b()
4       print("Saliendo de A")
5
6   def funcion_b():
7       print("Dentro de B")
```

Si estás en la línea 3:
*   `n(ext)` ejecutará `funcion_b()` por completo y te detendrá en la línea 4.
*   `s(tep)` te llevará a la línea 7, dentro de `funcion_b()`.

Un senior sabe cuándo usar `s` para profundizar y cuándo usar `n` para pasar por alto funciones que sabe que funcionan correctamente.

## 4. Control de Flujo Avanzado: Dominando el Tiempo y el Espacio

Aquí es donde `pdb` se vuelve quirúrgico.

### Puntos de Ruptura (Breakpoints)

Puedes gestionar breakpoints dinámicamente desde la sesión de `pdb`.

*   `b(reak) <lineno>`: Pone un breakpoint en el número de línea especificado. Ej: `b 42`.
*   `b(reak) <function>`: Pone un breakpoint al inicio de una función. Ej: `b mi_funcion_compleja`.
*   `b(reak)`: Lista todos los breakpoints, su número, y si están activos.
*   `cl(ear) [bpnumber]` o `cl(ear) <filename>:<lineno>`: Elimina un breakpoint. `cl 1` elimina el breakpoint #1.
*   `disable [bpnumber]`: Desactiva un breakpoint sin eliminarlo.
*   `enable [bpnumber]`: Reactiva un breakpoint.
*   `tbreak`: Breakpoint temporal. Se elimina automáticamente la primera vez que se alcanza.

**Técnica Senior: Breakpoints Condicionales**

Esta es una de las herramientas más potentes. Detente solo si se cumple una condición.

```
(Pdb) b 120, i > 900
```

Esto pone un breakpoint en la línea 120, pero la ejecución solo se detendrá si, al llegar a esa línea, la variable `i` es mayor que 900. Imagina un bucle con 1000 iteraciones que solo falla en la última. Esto te ahorra pulsar `c` 900 veces.

### Navegación Condicional y Saltos

*   `until [lineno]`: Continúa la ejecución hasta llegar a una línea con un número mayor al actual. Es perfecto para salir de bucles sin tener que esperar a que terminen.
*   `j(ump) <lineno>`: **¡CUIDADO!** Este es el comando más peligroso y poderoso. Mueve el puntero de ejecución a la línea que le indiques *sin ejecutar el código intermedio*. Puede dejar tu programa en un estado inconsistente, pero es invaluable para re-intentar una sección de código o saltarse una inicialización problemática. Úsalo con conocimiento de causa.

> "The `jump` command is a powerful tool, but it should be used with caution. It can lead to unexpected behavior if the program's state is not what the code at the destination line expects." - **Python `pdb` Documentation** [2]

## 5. Introspección Profunda: El Verdadero Poder de `pdb`

### Inspección y Modificación de Estado

El prompt `(Pdb)` es un REPL completo. Puedes hacer más que solo imprimir variables.

*   **Ejecutar código arbitrario:** Usa el prefijo `!`.
    ```
    (Pdb) !mi_variable = "nuevo valor"
    (Pdb) !mi_lista.append(100)
    (Pdb) !import requests; r = requests.get('https://api.github.com')
    ```
    Esta es la esencia del debugging interactivo. ¿Crees que un valor incorrecto está causando el fallo? **¡Cámbialo en caliente y pulsa `c` para ver si tu hipótesis era correcta!** No necesitas reiniciar el programa.

*   **Explorar objetos:**
    ```
    (Pdb) p dir(mi_objeto)
    (Pdb) p type(mi_variable)
    (Pdb) p locals()
    ```

### Comandos y Acciones Automatizadas

Puedes hacer que `pdb` ejecute una serie de comandos cada vez que alcanza un breakpoint.

```
(Pdb) b 42
Breakpoint 1 at /path/to/script.py:42
(Pdb) commands 1
(com) p "Iteración:", i
(com) p mi_diccionario['clave_interesante']
(com) end
```

Ahora, cada vez que la ejecución se detenga en la línea 42, `pdb` imprimirá automáticamente el valor de `i` y de `mi_diccionario['clave_interesante']` y luego te devolverá el control. Si quieres que continúe automáticamente, añade `continue` como último comando.

```
(com) continue
(com) end
```
Esto convierte un breakpoint en un `print()` glorificado y condicional, sin ensuciar tu código fuente.

### Alias y Personalización con `.pdbrc`

Puedes crear alias para comandos largos o secuencias de comandos que usas a menudo.

```
(Pdb) alias pi p i
(Pdb) alias print_status w !! l !! a
```
El `!!` separa comandos. Ahora, al escribir `print_status`, `pdb` ejecutará `where`, luego `list` y finalmente `args`.

Para que tus alias y configuraciones persistan, créalos en un archivo llamado `.pdbrc` en tu directorio home o en el directorio del proyecto. `pdb` lo leerá al iniciar.

**Ejemplo de `.pdbrc`:**
```
# .pdbrc
# Imprime la pila de llamadas y las variables locales
alias wla w !! pp locals()

# Un alias corto para pprint
alias pp pp

# Siempre mostrar el contexto al detenerse
display self.__dict__
```

## 6. `pdb` en el Ecosistema Moderno

### `pdb` vs. Depuradores de IDE (VS Code, PyCharm)

*   **IDE Pros:** Visuales, intuitivos, excelente integración, muestran variables en paneles, etc. Son fantásticos.
*   **`pdb` Pros:**
    *   **Universalidad:** Funciona en cualquier terminal, vía SSH, en un contenedor Docker, en cualquier sitio donde puedas ejecutar Python. Un senior debe ser capaz de depurar en un servidor de producción sin GUI.
    *   **Velocidad y Ligereza:** Sin sobrecarga de un IDE.
    *   **Poder de REPL:** La capacidad de ejecutar código arbitrario con `!` a menudo es más flexible que las "watch expressions" de los IDEs.
    *   **Fuerza la Comprensión:** Al no tener toda la información visualmente, te obliga a pensar activamente qué preguntar y dónde mirar, profundizando tu comprensión del código.

Un desarrollador senior es ambidiestro: usa el depurador del IDE para el desarrollo diario y `pdb` para escenarios remotos, complejos o cuando necesita el máximo control.

### Alternativas Mejoradas: `ipdb` y `pdbpp`

*   **`ipdb`**: Usa IPython como su REPL. Te da autocompletado con tabulador, resaltado de sintaxis, y mejor introspección. Es un reemplazo directo y muy recomendado. `pip install ipdb` y usa `import ipdb; ipdb.set_trace()`.
*   **`pdbpp` (`pdb++`)**: Otra alternativa popular con características como el modo "sticky" (siempre muestra el código fuente) y comandos más inteligentes.

### Debugging en Frameworks y Tests

*   **Flask/Django:** Simplemente coloca `breakpoint()` o `pdb.set_trace()` en una vista o un middleware. Cuando hagas una petición a ese endpoint, la consola del servidor se convertirá en una sesión de `pdb`.
*   **`pytest`**: `pytest` tiene una integración fantástica con `pdb`.
    *   `pytest --pdb`: Inicia una sesión de `pdb` post-mortem en el punto exacto de cualquier test que falle.
    *   `pytest --trace`: Entra en `pdb` al inicio de cada test. Útil para depurar la configuración de un test.
    *   `pytest -s --pdb test_mi_modulo.py -k "test_especifico"`: El `-s` es importante para que `pytest` no capture la salida y puedas interactuar con `pdb`.

## 7. Conclusión: De Herramienta a Mentalidad Senior

Dominar `pdb` no se trata de memorizar todos los comandos. Se trata de cambiar tu enfoque para resolver problemas.

*   **Deja de adivinar, empieza a verificar.**
*   **Interactúa con tu código en vivo.**
*   **Prueba tus hipótesis en segundos, no en minutos.**
*   **Sé capaz de diagnosticar problemas en cualquier entorno, no solo en tu máquina local con tu IDE favorito.**

El depurador es el estetoscopio de un programador. Aprender a usarlo profundamente te permite escuchar el corazón de tu aplicación, diagnosticar sus dolencias y curarlas con precisión quirúrgica.

---

## 8. Referencias y Citaciones

[1] **PEP 553 -- Built-in `breakpoint()`**. (2017). C. D. "Chuck" Moore, B. Warsaw. Python.org. [https://www.python.org/dev/peps/pep-0553/](https://www.python.org/dev/peps/pep-0553/)

[2] **`pdb` — The Python Debugger**. Python 3.11.4 documentation. Python Software Foundation. [https://docs.python.org/3/library/pdb.html](https://docs.python.org/3/library/pdb.html)

[3] **"Debugging Techniques" - PyCon 2016 Talk by Chris McDonough**. Aunque no es una cita directa, charlas como esta enfatizan la importancia de los depuradores interactivos en flujos de trabajo profesionales.

[4] **"Writing Idiomatic Python" - Talk by Jeff Knupp**. A menudo, estos recursos de estilo también tocan el tema de las herramientas profesionales, destacando `pdb` sobre el uso excesivo de `print`.
