Entender la historia de una herramienta nos revela su propósito. ¿Cómo pasó Numba de ser un experimento a un pilar del ecosistema científico? Y más importante, ¿cómo podemos transformar un código lento en uno ultrarrápido con un simple decorador? Veamos la magia en acción.

# Numba

---

### 3. Evolución Histórica Detallada

#### Timeline de Numba

-   **Principios de 2012:** Comienza el desarrollo en Continuum Analytics. El objetivo es claro: hacer que Python numérico sea rápido sin salir de Python.
-   **Finales de 2012:** Se presenta públicamente en la conferencia PyData. La reacción es de entusiasmo y escepticismo. ¿Otra promesa de velocidad para Python?
-   **2013-2014:** Se solidifica el soporte para NumPy. Numba aprende a entender los arrays de NumPy no como objetos genéricos de Python, sino como bloques contiguos de memoria, la clave para las optimizaciones de bajo nivel.
-   **2014 (Momento Decisivo):** El lanzamiento de `numba.cuda` cambia el juego. De repente, el mismo paradigma de decoradores podía usarse para generar código para arquitecturas masivamente paralelas como las GPUs de NVIDIA. Esto alineó a Numba con la revolución del GPGPU (General-Purpose computing on Graphics Processing Units).
-   **2016 (Cambio de Filosofía):** `nopython=True` se convierte en el estándar. Este fue un acto de madurez. El proyecto declaró que su propósito era el rendimiento sin concesiones. El modo `object` seguía existiendo, pero como una muleta, no como el objetivo.
-   **2017-Adelante:** Se añaden características de paralelismo (`parallel=True`) que pueden vectorizar y paralelizar bucles automáticamente en CPUs multinúcleo, liberando al programador de la gestión manual de hilos y del temido GIL.

#### Figuras Clave

-   **Travis Oliphant:** El visionario. Como padre de NumPy, entendió que el siguiente paso lógico era un compilador que entendiera NumPy a nivel nativo.
-   **Stan Seibert & Siu Kwan Lam:** Los arquitectos y desarrolladores principales. Sus contribuciones técnicas transformaron la visión en un software robusto y funcional. Han sido las caras del proyecto durante años, presentando en conferencias y guiando su desarrollo.

#### Contexto Histórico Computacional

Numba surgió en una "tormenta perfecta":
1.  **La Ley de Moore se ralentizaba:** Ya no se podía confiar en CPUs mononúcleo cada vez más rápidas. El rendimiento futuro dependía del paralelismo (multinúcleo, GPUs).
2.  **El Big Data era una realidad:** Los científicos y analistas se ahogaban en datos, y las herramientas existentes no daban abasto.
3.  **LLVM había madurado:** Proporcionaba una base sólida y de alta calidad sobre la que construir, evitando que el equipo de Numba tuviera que reinventar la rueda de la optimización y la generación de código.
4.  **Python había ganado la guerra de los lenguajes en ciencia de datos:** Era el lugar donde estaban los usuarios, por lo que una solución para Python tendría un impacto masivo.

---

### 4. Implementación Práctica: De la Teoría al Silicio

Basta de historia. Es hora de escribir código y ver los fotones volar.

#### Caso de Estudio 1: La belleza fractal de Mandelbrot

El conjunto de Mandelbrot es un ejemplo canónico de "computación vergonzosamente paralela". Cada píxel se puede calcular de forma independiente, lo que lo hace perfecto para la aceleración.

**El Enfoque "Antes" (Python Puro + NumPy)**

```python
import numpy as np
import time

def mandelbrot_python(m, n, max_iter):
    """Genera el conjunto de Mandelbrot usando Python puro y NumPy."""
    # Crea una matriz de números complejos
    x = np.linspace(-2.0, 1.0, m)
    y = np.linspace(-1.5, 1.5, n)
    c = x[:, np.newaxis] + 1j * y[np.newaxis, :]
    
    # Inicializa la matriz de salida y la z
    z = np.zeros_like(c, dtype=np.complex128)
    output = np.zeros(c.shape, dtype=np.int32)
    
    # El bucle principal
    for i in range(max_iter):
        # Identifica los puntos que no han divergido
        not_diverged = np.abs(z) < 2.0
        # Actualiza la salida para los que divergieron en la iteración anterior
        output[np.logical_and(np.logical_not(not_diverged), output == 0)] = i
        # Actualiza z solo para los puntos que no han divergido
        z[not_diverged] = z[not_diverged]**2 + c[not_diverged]
        
    output[output == 0] = max_iter
    return output

# Medimos el tiempo
start_time = time.time()
mandelbrot_python(1000, 1000, 100)
end_time = time.time()

print(f"Python puro + NumPy: {end_time - start_time:.4f} segundos")
```
Este código es "vectorizado" al estilo NumPy. Evita los bucles `for` explícitos en Python, pero crea muchas matrices intermedias (`not_diverged`, etc.), lo que consume memoria y tiempo.

**El Enfoque "Después" (Numba - El Bien)**

Aquí, escribimos el código como lo haríamos en un lenguaje de bajo nivel: con bucles explícitos. Esto es a menudo anti-pythónico, pero es exactamente lo que Numba quiere.

```python
import numpy as np
import time
from numba import jit

@jit(nopython=True) # El decorador mágico
def mandelbrot_numba(m, n, max_iter):
    """Genera el conjunto de Mandelbrot usando Numba."""
    output = np.zeros((m, n), dtype=np.int32)
    
    # Precalculamos los valores de x e y para evitar hacerlo en el bucle interno
    real_axis = np.linspace(-2.0, 1.0, m)
    imag_axis = np.linspace(-1.5, 1.5, n)
    
    # Bucle explícito sobre cada píxel
    for i in range(m):
        for j in range(n):
            c_real = real_axis[i]
            c_imag = imag_axis[j]
            
            z_real = 0.0
            z_imag = 0.0
            
            for k in range(max_iter):
                # z = z^2 + c
                # (z_r + i*z_i)^2 = z_r^2 - z_i^2 + 2*z_r*z_i*i
                z_real_new = z_real**2 - z_imag**2 + c_real
                z_imag_new = 2 * z_real * z_imag + c_imag
                
                z_real = z_real_new
                z_imag = z_imag_new
                
                # Comprobación de divergencia
                if z_real**2 + z_imag**2 > 4.0:
                    break
            
            output[i, j] = k
    
    return output

# Medimos el tiempo (la primera llamada incluye la compilación)
print("Compilando y ejecutando por primera vez...")
start_time = time.time()
mandelbrot_numba(1000, 1000, 100)
end_time = time.time()
print(f"Numba (primera ejecución): {end_time - start_time:.4f} segundos")

# Medimos el tiempo de una ejecución ya compilada
print("\nEjecutando con la función ya compilada...")
start_time = time.time()
mandelbrot_numba(1000, 1000, 100)
end_time = time.time()
print(f"Numba (segunda ejecución): {end_time - start_time:.4f} segundos")
```
**Resultados Típicos:**
- Python puro + NumPy: ~2.5 segundos
- Numba (primera ejecución): ~0.6 segundos (incluye compilación)
- Numba (segunda ejecución): **~0.05 segundos**

La versión de Numba es **~50 veces más rápida**. ¿Por qué? Porque Numba convirtió esos bucles explícitos, que son veneno para el intérprete de Python, en un bucle de máquina altamente optimizado, sin asignaciones de memoria intermedias y con todas las variables viviendo en registros de la CPU o en la caché.

#### Patrones de Uso

-   **Básico (`@jit`):** Para funciones con bucles numéricos intensivos.
-   **Paralelismo (`@jit(parallel=True)`):** Para bucles que se pueden paralelizar. Se usa con `numba.prange` en lugar de `range`.
-   **Creación de ufuncs (`@vectorize`):** Para crear funciones de NumPy que operan elemento por elemento a la velocidad de C.

```python
from numba import vectorize
import numpy as np

@vectorize(['float64(float64, float64)'])
def add_and_clip(x, y):
    """Suma dos números y los recorta en el rango [0, 1]."""
    res = x + y
    if res > 1.0:
        return 1.0
    if res < 0.0:
        return 0.0
    return res

a = np.linspace(0, 1, 5)
b = np.linspace(-0.5, 0.5, 5)

print(add_and_clip(a, b))
# Output: [0.    0.25  0.5   0.75  1.  ]
```
Esta función `add_and_clip` ahora se comporta como una ufunc de NumPy (como `np.add`), con broadcasting y todas las ventajas, pero con tu lógica personalizada ejecutándose a velocidad nativa.