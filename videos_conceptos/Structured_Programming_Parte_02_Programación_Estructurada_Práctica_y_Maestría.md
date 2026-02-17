Entender la teoría es una cosa, pero ¿cómo se ve la programación estructurada en el código que escribimos hoy? Vamos a comparar dos formas de resolver el mismo problema y ver por qué la claridad no es solo una preferencia, es una necesidad.

# Structured Programming

### 4. Implementación Práctica en Python

Python es un lenguaje inherentemente estructurado. No tiene un `goto` tradicional. Veamos cómo estos principios se manifiestan en el código del día a día.

**Caso de Estudio: Procesamiento de un Archivo de Log**

Imaginemos que tenemos un archivo `app.log` con líneas como:
```
INFO: User logged in
ERROR: Failed to connect to database
WARNING: Disk space is low
INFO: Data processed successfully
```
Queremos contar el número de errores y advertencias.

#### El Mal Camino: Simulación de "Espagueti"

Un programador intermedio podría caer en la trampa de anidar lógicamente de forma confusa, creando un código difícil de seguir, similar en espíritu al `goto`.

```python
# mal_ejemplo.py
# EVITA ESTE ESTILO

def process_logs_unstructured(filepath):
    """
    Procesa logs de una manera difícil de leer y mantener.
    Simula un flujo de control enrevesado con banderas y anidamiento profundo.
    """
    error_count = 0
    warning_count = 0
    file_found = False
    processing_active = False

    try:
        # Simula un "salto" a la sección de procesamiento
        f = open(filepath, 'r')
        file_found = True
        processing_active = True
    except FileNotFoundError:
        print("Error: Archivo no encontrado.")
        # Simula un "salto" al final
        processing_active = False

    if processing_active:
        for line in f:
            line = line.strip()
            if line: # Solo procesar líneas no vacías
                if line.startswith("ERROR"):
                    # Lógica anidada
                    if "database" in line:
                        print(f"Error de base de datos detectado: {line}")
                        error_count += 1
                    else:
                        error_count += 1
                elif line.startswith("WARNING"):
                    warning_count += 1
        f.close()
        
    if file_found:
        print("\n--- Reporte Final ---")
        print(f"Errores encontrados: {error_count}")
        print(f"Advertencias encontradas: {warning_count}")
    else:
        print("No se generó ningún reporte.")

# process_logs_unstructured('app.log')
```
Este código funciona, pero es frágil y confuso. Las banderas `file_found` y `processing_active` son una forma de `goto` glorificado, gestionando el flujo de manera manual y propensa a errores.

#### El Buen Camino: Estructurado y Modular

Un desarrollador senior aplica los principios de **secuencia, selección, iteración y modularidad (funciones)**.

```python
# buen_ejemplo.py
# ESTE ES EL CAMINO

def parse_log_line(line: str) -> tuple[int, int]:
    """
    Analiza una sola línea de log y devuelve el conteo de errores/advertencias.
    Punto de entrada único, punto de salida único. Alta cohesión.
    """
    line = line.strip()
    if line.startswith("ERROR"):
        return (1, 0)  # (error, warning)
    if line.startswith("WARNING"):
        return (0, 1)
    return (0, 0)

def process_log_file(filepath: str) -> dict:
    """
    Lee un archivo de log y procesa cada línea.
    Maneja la apertura y cierre del archivo de forma segura.
    """
    error_count = 0
    warning_count = 0
    try:
        with open(filepath, 'r') as f:
            # Iteración
            for line in f:
                # Secuencia y Modularidad
                errors, warnings = parse_log_line(line)
                error_count += errors
                warning_count += warnings
    except FileNotFoundError:
        print(f"Error: El archivo '{filepath}' no fue encontrado.")
        return None # Salida clara en caso de error

    return {"errors": error_count, "warnings": warning_count}

def generate_report(results: dict):
    """
    Imprime un reporte formateado a partir de los resultados.
    Responsabilidad única.
    """
    if results:
        print("\n--- Reporte Final ---")
        print(f"Errores encontrados: {results['errors']}")
        print(f"Advertencias encontradas: {results['warnings']}")
    else:
        print("No se pudo generar el reporte.")

def main():
    """
    Función principal que orquesta el proceso. Top-Down Design.
    """
    log_file = 'app.log'
    # Secuencia de llamadas a funciones modulares
    log_results = process_log_file(log_file)
    generate_report(log_results)

if __name__ == "__main__":
    # Crear un archivo de log de ejemplo para probar
    with open('app.log', 'w') as f:
        f.write("INFO: User logged in\n")
        f.write("ERROR: Failed to connect to database\n")
        f.write("WARNING: Disk space is low\n")
        f.write("INFO: Data processed successfully\n")
        f.write("ERROR: Timeout\n")

    main()
```

**Análisis de la Versión Senior:**

1.  **Top-Down Design**: El problema se descompone desde lo general (`main`) a lo específico (`parse_log_line`).
2.  **Modularidad**: Cada función tiene una única responsabilidad (SRP). `parse_log_line` solo sabe de líneas, `process_log_file` solo sabe de archivos, `generate_report` solo sabe de imprimir.
3.  **Claridad**: No hay banderas de estado complejas. El flujo es lineal y predecible dentro de cada función. El `try/except` y el `with` son formas estructuradas de manejar errores y recursos.
4.  **Testeabilidad**: `parse_log_line` es una función pura (dada la misma entrada, siempre produce la misma salida), lo que la hace trivial de probar unitariamente.

### 5. Nivel Senior - Conceptos Avanzados

Aquí es donde separamos a los programadores de los arquitectos de software.

**Trade-offs: ¿Cuándo Romper las Reglas?**

Dijkstra era un purista. Knuth, más pragmático. La realidad es que los lenguajes modernos nos dan "saltos estructurados" que son aceptables porque no crean el caos del `GOTO` libre.

*   **`return` temprano en una función**: Es un `goto` al final de la función. Es perfectamente aceptable para validaciones de entrada (guard clauses) porque simplifica la lógica y evita el "código de flecha" (arrowhead code).

    ```python
    # Mal: Anidamiento
    def process_item(item):
        if item is not None:
            if item.is_valid():
                # ... lógica principal ...
    
    # Bien: Guard Clauses
    def process_item(item):
        if item is None:
            return
        if not item.is_valid():
            return
        # ... lógica principal ...
    ```

*   **`break` y `continue` en bucles**: Son `goto` al final o al principio del bucle, respectivamente. Usados con moderación, mejoran la legibilidad al evitar banderas de control de bucle.

*   **Excepciones (`try`/`except`/`raise`)**: Este es el `goto` más poderoso y estructurado de la programación moderna. Transfiere el control a un manejador de errores específico. Su poder es inmenso, pero su abuso conduce a un flujo de control ofuscado. Un senior sabe que las excepciones son para casos *excepcionales*, no para el control de flujo normal.

> "Las excepciones son una forma de `goto` no local. Pueden crear caminos de ejecución ocultos que son difíciles de razonar." — **Atribuido a varias discusiones de diseño de lenguajes**

**Anti-Patrones**

*   **Arrowhead Code**: Anidamiento profundo de `if/else` que forma una flecha visual (`>`). Se soluciona con guard clauses o descomponiendo en funciones.
*   **Funciones Divinas (God Functions)**: Una función de 500 líneas que lo hace todo. Es la antítesis de la modularidad.
*   **Abuso de Banderas de Estado**: Usar variables booleanas para controlar el flujo dentro de una función, como en nuestro `mal_ejemplo.py`. A menudo es una señal de que la función tiene demasiadas responsabilidades.

**Integración con Otros Paradigmas**

*   **OOP**: La programación estructurada es el esqueleto de tus métodos. Un buen método es un buen programa estructurado.
*   **Programación Funcional (FP)**: La FP lleva la idea al extremo. Las funciones puras son la unidad estructurada definitiva: sin estado, sin efectos secundarios, con un punto de entrada y uno de salida. Son perfectamente predecibles.
*   **Programación Concurrente**: Conceptos modernos como **Structured Concurrency** (popularizado por Nathaniel J. Smith) aplican estas ideas a la programación asíncrona. La idea es que un grupo de tareas concurrentes debe tener un único punto de entrada y un único punto de salida, formando un bloque que no puede "filtrar" tareas huérfanas. Es la herencia directa de Dijkstra en el mundo del `async/await`.

### 6. Referencias y Citaciones Académicas

Un senior se apoya en los hombros de gigantes. Aquí están algunos de los documentos y libros que formaron este campo.

1.  > "Our intellectual powers are rather geared to master static relations and that our powers to visualize processes evolving in time are relatively poorly developed. For that reason we should do (as wise programmers aware of our limitations) our utmost to shorten the conceptual gap between the static program and the dynamic process, to make the correspondence between the program (spread out in text space) and the process (spread out in time) as trivial as possible." — **Edsger W. Dijkstra**, *Go To Statement Considered Harmful* (1968)
    [Enlace (ACM)](https://dl.acm.org/doi/10.1145/362929.362947)

2.  > "This paper has the modest aim of showing that any program can be written by using only `do-while` and `if-then-else` statements." — **Corrado Böhm & Giuseppe Jacopini**, *Flow Diagrams, Turing Machines and Languages with Only Two Formation Rules* (1966)
    [Enlace (ACM)](https://dl.acm.org/doi/10.1145/355592.355604)

3.  > "The practice of structured programming... is the systematic use of abstraction to control a mass of detail, and also a means of documentation which aids program design." — **O.-J. Dahl, E. W. Dijkstra, C. A. R. Hoare**, *Structured Programming* (1972)
    [Libro (Amazon)](https://www.amazon.com/Structured-Programming-P-I-C-Classic-Computing/dp/0122005503)

4.  > "I have felt that the GOTO statement has been unjustly maligned... The new morality that I am proposing is that we should be... able to say exactly what is going on in our programs." — **Donald E. Knuth**, *Structured Programming with go to Statements* (1974)
    [Enlace (PDF)](http://www.cs.sjsu.edu/~mak/CS185C/knuth.pdf)

5.  > "The cost of maintaining a piece of software is proportional to the difficulty of understanding it." — **Robert C. Martin**, *Clean Code: A Handbook of Agile Software Craftsmanship* (2008)
    [Libro (Amazon)](https://www.amazon.com/Clean-Code-Handbook-Software-Craftsmanship/dp/0132350882)

6.  > "Good programmers know what to write. Great ones know what to rewrite (and reuse)." — **Eric S. Raymond**, *The Cathedral & the Bazaar* (1999)

7.  > "The software crisis, simply, was the period in the history of computing science in which the demand for new software was much higher than the ability of programmers to deliver it." — **F. P. Brooks, Jr.**, *The Mythical Man-Month* (1975)

8.  > "Structured concurrency: a nursery guarantees that the parent task can’t complete until all the child tasks have completed. [...] This gives us a firm guarantee that there are no “leaked” background tasks." — **Nathaniel J. Smith**, *Notes on structured concurrency, or: Go statement considered harmful* (2018)
    [Enlace (Blog)](https://vorpus.org/blog/notes-on-structured-concurrency-or-go-statement-considered-harmful/)

---

### Conclusión: El Fundamento Silencioso

La programación estructurada ya no es un tema candente. No verás conferencias tituladas "¡El futuro es la programación estructurada!". ¿Por qué? Porque ganó. Ganó tan completamente que se volvió invisible, se convirtió en el cimiento sobre el que se construyó todo lo demás.

Entenderla a este nivel no es un ejercicio académico. Es la diferencia entre un programador que sigue patrones y un ingeniero que toma decisiones de diseño fundamentadas. Cuando descompones un problema en funciones más pequeñas, no lo haces solo porque "es una buena práctica". Lo haces porque estás aplicando los principios de modularidad y punto de entrada/salida único, validados por el teorema de Böhm-Jacopini, para reducir la carga cognitiva y crear sistemas verificables, como lo defendió Dijkstra hace más de 50 años.

Ese, y no otro, es el pensamiento de un desarrollador senior. Ahora, ve y construye con claridad.