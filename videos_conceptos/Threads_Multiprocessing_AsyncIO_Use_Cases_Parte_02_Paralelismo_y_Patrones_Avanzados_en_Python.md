Hemos visto cómo manejar tareas que pasan mucho tiempo esperando, como las peticiones de red. Pero, ¿qué pasa cuando el problema es el opuesto? ¿Cuando la CPU está al 100% y necesitas más potencia de cálculo? Aquí es donde el verdadero paralelismo entra en juego.

# Threads / Multiprocessing / AsyncIO Use Cases

#### Escenario 2: CPU-bound - Procesando Datos

Ahora, imaginemos que cada "tarea" es un cálculo matemático pesado, no una espera de red.

```python
def cpu_bound_task(n):
    print(f"Calculando para {n}...")
    # Un cálculo sin sentido pero intensivo en CPU
    result = sum(i * i for i in range(n))
    print(f"Terminado para {n}")
    return result

numbers = [10_000_000, 10_000_001, 10_000_002]
```

##### El Intento Fallido: `threading` para CPU-bound
Si intentamos usar hilos aquí, nos toparemos con el **Global Interpreter Lock (GIL)**. El GIL es un mutex que protege el acceso a los objetos de Python, evitando que múltiples hilos ejecuten bytecode de Python al mismo tiempo. Solo un hilo puede tener el GIL. Para tareas de I/O, no es un problema porque el GIL se libera durante la espera. Pero para tareas de CPU, los hilos se pelearán por el GIL y la ejecución será, en el mejor de los casos, secuencial, y en el peor, ¡más lenta debido a la sobrecarga de cambio de contexto!

*No mostraré el código porque su rendimiento sería igual o peor que el secuencial, y es un anti-patrón.*

##### El Enfoque Correcto para CPU-bound: `multiprocessing`

Para el verdadero paralelismo en CPython, necesitamos eludir el GIL. `multiprocessing` lo hace creando nuevos procesos. Cada proceso tiene su propio intérprete de Python y su propio espacio de memoria, por lo que el GIL de un proceso no afecta a los demás.

```python
from multiprocessing import Pool
import time

# La misma función cpu_bound_task de antes

start = time.time()
with Pool() as pool:
    pool.map(cpu_bound_task, numbers)

print(f"Multiprocessing: Tomó {time.time() - start:.2f} segundos.")
# Salida esperada: Si tienes 3+ núcleos, tomará aproximadamente el tiempo de UNA sola tarea.
```
**Bien vs. Mal (`multiprocessing`):**
- **Bien:** Minimizar la comunicación entre procesos. La transferencia de datos (serialización/deserialización con `pickle`) es costosa. Pasa solo los datos necesarios.
- **Mal:** Usar `multiprocessing` para tareas muy cortas. La sobrecarga de crear procesos puede ser mayor que el tiempo de ejecución de la tarea en sí.

### 5. Nivel Senior - Conceptos Avanzados

#### La Matriz de Decisión: Trade-offs

| Característica | `threading` | `multiprocessing` | `asyncio` |
| :--- | :--- | :--- | :--- |
| **Ideal para** | I/O-bound (red, disco) | CPU-bound (cálculos, procesamiento de datos) | I/O-bound con muchísimas conexiones (>1000s) |
| **Paralelismo Real (CPython)** | No (limitado por el GIL) | Sí (elude el GIL) | No (un solo hilo/proceso) |
| **Uso de Memoria** | Bajo (hilos comparten memoria) | Alto (cada proceso tiene su propia memoria) | Muy bajo (objetos de tarea ligeros) |
| **Coste de Creación** | Bajo | Alto | Muy bajo |
| **Comunicación** | Fácil (memoria compartida) | Difícil (requiere IPC: `Queues`, `Pipes`) | Fácil (variables compartidas dentro del mismo hilo) |
| **Complejidad de Código** | Moderada (locks, race conditions) | Moderada (IPC, serialización) | Alta (ecosistema `async`, funciones "de colores") |

> "Existen dos tipos de funciones: las que son `async` y las que aún no se han dado cuenta de que lo serán." — Un chiste común en la comunidad de programadores, que refleja el problema de las "funciones de colores" (`async` vs `sync`), donde una función `async` solo puede ser llamada por otra `async`.

#### Anti-Patrones y Cómo Evitarlos

1.  **El Martillo de Oro:** Usar tu herramienta favorita para todo.
    - **Anti-Patrón:** "¡Me encanta `asyncio`! Lo usaré para mi script de procesamiento de imágenes."
    - **Solución Senior:** Reconoce la naturaleza de la tarea. ¿Espera (I/O) o piensa (CPU)? Elige la herramienta que se alinee con la naturaleza del cuello de botella.

2.  **Ignorar el Costo de la Concurrencia:**
    - **Anti-Patrón:** Usar `multiprocessing` para sumar dos números. La sobrecarga de crear procesos, serializar los números, enviarlos, calcular y devolver el resultado será millones de veces más lenta que `a + b`.
    - **Solución Senior:** Mide (profile) tu código. La concurrencia solo vale la pena si el tiempo de la tarea es significativamente mayor que la sobrecarga de la concurrencia.

3.  **Optimización Prematura y Complejidad Accidental:**
    - **Anti-Patrón:** Convertir un script secuencial simple y funcional en un complejo laberinto de `asyncio` o `threading` "por si acaso" necesita ser rápido en el futuro.
    - **Solución Senior:** Escribe código simple y correcto primero. Aplica concurrencia solo cuando sea necesario y esté justificado por mediciones de rendimiento. Como dijo Donald Knuth: "La optimización prematura es la raíz de todo mal".

#### Integración: La Orquesta Sinfónica Completa

Un verdadero senior sabe que estas herramientas no son mutuamente excluyentes. Se pueden combinar.

**Patrón Avanzado:** Usar `asyncio` como el director principal para manejar miles de conexiones de red (I/O-bound), y cuando llega una tarea que requiere un cálculo pesado (CPU-bound), delegarla a un pool de procesos de `multiprocessing`.

```python
import asyncio
from concurrent.futures import ProcessPoolExecutor

def cpu_bound_task_sync(n):
    # Versión síncrona de nuestra tarea CPU-bound
    return sum(i * i for i in range(n))

async def main():
    loop = asyncio.get_running_loop()
    
    # Creamos un pool de procesos
    with ProcessPoolExecutor() as pool:
        # Tarea I/O-bound (simulada con sleep)
        print("Iniciando tarea I/O-bound...")
        await asyncio.sleep(2)
        print("Tarea I/O-bound terminada.")

        # Tarea CPU-bound delegada al pool de procesos
        print("Delegando tarea CPU-bound...")
        # run_in_executor ejecuta una función bloqueante en un hilo/proceso separado
        # sin bloquear el bucle de eventos de asyncio.
        result = await loop.run_in_executor(
            pool, cpu_bound_task_sync, 20_000_000
        )
        print(f"Tarea CPU-bound terminada con resultado: {result}")

asyncio.run(main())
```
Este patrón te da lo mejor de ambos mundos: la escalabilidad de `asyncio` para I/O y la potencia de `multiprocessing` para CPU, todo orquestado elegantemente.

### 6. Referencias y Citaciones Académicas

1.  > "The semaphore is a variable that can take non-negative integer values; when it is created, its value is initialized. Two operations are defined on it, the P- and V-operation." — **Edsger W. Dijkstra**, *Co-operating sequential processes* (1968). [El paper fundamental que introduce los semáforos].
2.  > "The performance enhancement possible with a given improvement is limited by the fraction of the execution time that the improved feature is used." — **Gene M. Amdahl**, *Validity of the single processor approach to achieving large scale computing capabilities* (1967). [El paper original de la Ley de Amdahl].
3.  > "This paper suggests that input and output are basic primitives of programming and that parallel composition of communicating sequential processes is a fundamental program structuring method." — **C. A. R. Hoare**, *Communicating Sequential Processes* (1978). [Una base teórica para la concurrencia basada en mensajes].
4.  > "The GIL is a lock that is used to protect all of Python’s data structures from concurrent access. Effectively, it serializes access to the Python interpreter from multiple threads." — **David Beazley**, *Inside the Python GIL* (2010). [Una charla técnica icónica que desmitifica el GIL]. [Link a la presentación](https://www.dabeaz.com/python/GIL.pdf)
5.  > "Coroutines are a more memory-efficient way to implement concurrent programming than system threads, as there is no context-switching overhead from the OS." — **Python Software Foundation**, *Python Documentation for `asyncio`*. [Documentación oficial]. [Link](https://docs.python.org/3/library/asyncio-task.html)
6.  > "The `multiprocessing` package offers both local and remote concurrency, effectively side-stepping the Global Interpreter Lock by using subprocesses instead of threads." — **Python Software Foundation**, *Python Documentation for `multiprocessing`*. [Documentación oficial]. [Link](https://docs.python.org/3/library/multiprocessing.html)
7.  > "The 'free lunch' is the idea that software performance will continue to improve as a side effect of ongoing processor improvements. The free lunch is over." — **Herb Sutter**, *The Free Lunch Is Over: A Fundamental Turn Toward Concurrency in Software* (2005). [Un artículo seminal que marcó el cambio de la industria hacia el multi-núcleo].
8.  > "Don't get tangled up in race conditions, deadlocks, and other obscure synchronization bugs. Use simple tools to solve simple problems." — **Brett Slatkin**, *Effective Python: 90 Specific Ways to Write Better Python* (2019). [Un libro práctico con excelentes consejos sobre concurrencia].

---

**Conclusión:**

Has viajado desde los albores de la computación hasta las arquitecturas de software más modernas. Ahora entiendes que `threading`, `multiprocessing` y `asyncio` no son solo librerías; son respuestas a diferentes problemas fundamentales que han evolucionado a lo largo de 60 años de historia de la computación.

Un programador intermedio sabe *cómo* usar cada una. Un programador senior sabe *por qué* y *cuándo* usar una sobre las otras. Sabe que la concurrencia no es una bala de plata, sino una herramienta afilada que, mal utilizada, puede causar más problemas de los que resuelve.

La próxima vez que te enfrentes a un problema de rendimiento, no te preguntes "¿Cómo puedo hacer esto más rápido?". Pregúntate: "¿Dónde está esperando mi programa? ¿Está esperando a la red, al disco, o está esperando a la CPU? ¿Cuál es la naturaleza de mi cuello de botella?".

La respuesta a esa pregunta te dirá qué sección de la orquesta dirigir. Y ahora, tienes la partitura. Ve y dirige tu sinfonía.