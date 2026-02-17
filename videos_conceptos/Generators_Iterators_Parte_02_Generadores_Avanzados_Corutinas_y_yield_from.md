Ya sabemos que los generadores son excelentes para *producir* datos. Pero, ¿y si te dijera que también pueden *recibir* datos, convirtiéndose en canales de comunicación bidireccionales? Aquí es donde los generadores se transforman en potentes corutinas.

# Generators, Iterators

## 5. Nivel Senior - Conceptos Avanzados

Aquí es donde separamos a los programadores de los arquitectos de software.

### Corutinas: Generadores como Receptores de Datos

La **PEP 342** transformó los generadores de meros productores a canales de comunicación bidireccionales.

- `(yield)`: Ahora puede ser una expresión.
- `generador.send(valor)`: Envía un valor *dentro* del generador, y ese valor se convierte en el resultado de la expresión `yield`.
- `generador.throw(excepcion)`: Lanza una excepción *dentro* del generador, en el punto donde se pausó.
- `generador.close()`: Finaliza el generador, útil para limpieza (ej. cerrar sockets).

**Ejemplo: Un "averager" como corutina**

```python
def averager():
    """Una corutina que calcula una media continua."""
    total = 0.0
    count = 0
    average = None
    while True:
        # yield pausa aquí, esperando un valor enviado por send()
        term = yield average
        if term is None: # Convención para salir
            break
        total += term
        count += 1
        average = total / count

# Uso
coro_avg = averager()
next(coro_avg) # ¡CRÍTICO! Hay que "cebar" la corutina hasta el primer yield.

print(coro_avg.send(10)) # Envía 10, devuelve 10.0
print(coro_avg.send(20)) # Envía 20, devuelve 15.0
print(coro_avg.send(5))  # Envía 5, devuelve 11.66...
try:
    coro_avg.send(None)
except StopIteration:
    print("Corutina finalizada.")
```
Este patrón es la base de la programación asíncrona en Python (`async`/`await` son azúcar sintáctico sobre corutinas basadas en generadores).

### `yield from`: Delegación a Sub-generadores

La **PEP 380** introdujo `yield from` para resolver un problema común: cómo un generador puede "incluir" de forma transparente todos los valores de otro generador.

**Antes (El Mal Camino - Bucle explícito):**
```python
def chain_mal(g1, g2):
    for item in g1:
        yield item
    for item in g2:
        yield item
```

**Después (El Buen Camino - `yield from`):**
```python
def chain_bien(g1, g2):
    yield from g1
    yield from g2
```
No es solo azúcar sintáctico. `yield from` también maneja la comunicación bidireccional (`send`, `throw`, `close`), pasando los mensajes directamente al sub-generador. Es un canal transparente.

**Caso de estudio: Recorrer un árbol**
```python
def traverse_tree(node):
    """Recorre un árbol de nodos en pre-orden usando yield from."""
    if node is not None:
        yield node.value
        # Delega la iteración a los sub-árboles
        yield from traverse_tree(node.left)
        yield from traverse_tree(node.right)
```
Este código es increíblemente expresivo y eficiente para manejar estructuras recursivas de forma perezosa.

### Trade-offs: La Decisión del Senior

| Característica | Lista / Colección en Memoria | Generador / Iterador | Decisión Senior |
| :--- | :--- | :--- | :--- |
| **Uso de Memoria** | `O(n)` - Proporcional al tamaño | `O(1)` - Constante | Para datos masivos o flujos, **generador** es la única opción viable. |
| **Acceso al 1er elemento** | Lento (si la creación es costosa) | Rápido (calcula solo lo necesario) | Si solo necesitas los primeros N elementos de una secuencia larga, **generador**. |
| **Acceso Aleatorio** | `O(1)` - `mi_lista[i]` es instantáneo | No soportado | Si necesitas acceso por índice, saltar, o revertir, necesitas una **lista**. |
| **Re-iteración** | Puedes iterar sobre ella múltiples veces | Se consume tras la primera iteración | Si necesitas pasar por los datos más de una vez, materialízalo en una **lista**. |
| **Componibilidad** | Requiere crear listas intermedias | Excelente, se pueden encadenar | Para pipelines de procesamiento complejos y limpios, los **generadores** son superiores. |

### Anti-Patrones: Errores Comunes a Evitar

1.  **Materialización Prematura**: El error más común.
    ```python
    # ANTI-PATRÓN
    # Carga todo el archivo en una lista, anulando el beneficio del generador.
    lines = list(read_lines_from_huge_file()) 
    for line in lines:
        if "ERROR" in line:
            print(line)
            break
    ```
    **Corrección**: Itera directamente sobre el generador.

2.  **Asumir Re-iterabilidad**:
    ```python
    # ANTI-PATRÓN
    results = my_generator()
    print(f"Max: {max(results)}")
    print(f"Min: {min(results)}") # ¡Error! results ya está consumido.
    ```
    **Corrección**: Si necesitas múltiples pasadas, convierte el generador a una lista: `results = list(my_generator())`, pero sé consciente del coste de memoria.

3.  **Ignorar la Limpieza (`close()`)**: Si un generador maneja recursos externos (sockets, archivos), debe usar un bloque `try...finally` para asegurar que `close()` se llame y los recursos se liberen, incluso si el consumidor del generador se destruye antes de tiempo.

    > "Los generadores proporcionan una forma conveniente de implementar el patrón de iterador. Un generador es simplemente una función que contiene una expresión `yield`." — **David Beazley**, *Python Essential Reference* (2009)

## 6. Referencias y Citaciones Académicas

1.  > "CLU provides a special kind of coroutine, called an iterator, for iterating over the elements of a collection of objects. An iterator is a procedure that yields a sequence of objects." — **Barbara Liskov et al.**, *CLU Reference Manual* (1981) - [PDF Link](http://publications.csail.mit.edu/lcs/pubs/pdf/MIT-LCS-TR-225.pdf)
2.  > "The Iterator pattern is a design pattern in which an iterator is used to traverse a container and access the container's elements. The Iterator pattern decouples algorithms from containers." — **Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides**, *Design Patterns: Elements of Reusable Object-Oriented Software* (1994)
3.  > "This PEP introduces generator functions and the 'yield' statement. The goal is to make it much easier to write iterators." — **Neil Schemenauer, Tim Peters, Magnus Lie Hetland**, *PEP 255: Simple Generators* (2001) - [PEP 255 Link](https://www.python.org/dev/peps/pep-0255/)
4.  > "This PEP proposes some enhancements to Python's generator functions. Specifically, it is proposed to add a `send()` method to generator-iterators, which resumes the generator and 'sends' a value that becomes the result of the current `yield` expression." — **Guido van Rossum, Phillip J. Eby**, *PEP 342: Coroutines via Enhanced Generators* (2005) - [PEP 342 Link](https://www.python.org/dev/peps/pep-0342/)
5.  > "A new expression `yield from <expr>` is proposed. The main use of this new expression is to allow a generator to delegate part of its operations to another generator." — **Thomas Wouters**, *PEP 380: Syntax for Delegating to a Subgenerator* (2009) - [PEP 380 Link](https://www.python.org/dev/peps/pep-0380/)
6.  > "Generators are a simple and powerful tool for creating iterators. They are written like regular functions but use the `yield` statement whenever they want to return data." — **Python Software Foundation**, *Python 3 Documentation, Glossary* - [Docs Link](https://docs.python.org/3/glossary.html#term-generator)
7.  > "Icon's generators are a fundamental control structure, not just a way to produce elements of a sequence. A generator can produce a sequence of values, and backtracking control structures can cause it to resume and produce another value." — **Ralph E. Griswold, Madge T. Griswold**, *The Icon Programming Language* (1996)
8.  > "A coroutine is a computer program component that generalizes subroutines for non-preemptive multitasking, by allowing execution to be suspended and resumed." — **Donald Knuth**, *The Art of Computer Programming, Vol. 1: Fundamental Algorithms* (1968) - Knuth discute el concepto de corutinas mucho antes de su popularización en lenguajes modernos.

---

Dominar los generadores e iteradores es un rito de paso. Es el momento en que un programador deja de pensar en "datos en reposo" y empieza a pensar en "datos en movimiento". Es comprender que la computación más elegante no es la que más hace, sino la que hace exactamente lo que se necesita, en el momento preciso en que se necesita. Es, en esencia, el arte de la pereza elegante y eficiente.