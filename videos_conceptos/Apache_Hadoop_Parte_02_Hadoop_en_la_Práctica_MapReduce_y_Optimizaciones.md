La teoría es fascinante, pero ¿cómo se ve realmente el código que procesa petabytes de datos? Pasemos de los conceptos a la consola. Veremos cómo un par de simples scripts de Python pueden orquestar un ejército de máquinas para resolver un problema masivo, y cómo optimizar ese proceso para que no tarde una eternidad.

# Apache Hadoop

### 4. Implementación Práctica

Hablemos de código. Aunque hoy en día es más común usar PySpark, entender el paradigma original de MapReduce es fundamental. Usaremos **Hadoop Streaming**, una utilidad que permite usar cualquier ejecutable (como un script de Python) como mapper o reducer, comunicándose a través de `stdin` y `stdout`.

**Caso de Estudio: El Clásico "Word Count"**

Imagina que tienes terabytes de texto (libros, logs, tweets) y quieres contar la frecuencia de cada palabra.

#### El Mapper: `mapper.py`

El mapper lee el texto línea por línea, lo limpia, y emite pares `(palabra, 1)` por cada palabra que encuentra.

```python
#!/usr/bin/env python
import sys
import re

def main():
    """
    Lee líneas de stdin, las divide en palabras y emite pares (palabra, 1) a stdout.
    """
    # Regex para encontrar palabras (secuencias de caracteres alfanuméricos)
    word_regex = re.compile(r'\b\w+\b')

    for line in sys.stdin:
        # 1. Limpieza básica: quitar espacios en blanco y convertir a minúsculas
        line = line.strip().lower()
        
        # 2. Encontrar todas las palabras en la línea
        words = word_regex.findall(line)
        
        # 3. Emitir un par clave-valor para cada palabra
        #    El formato es: clave <tab> valor
        for word in words:
            print(f'{word}\t1')

if __name__ == "__main__":
    main()
```
**Explicación del "Por qué":**
*   `sys.stdin`: Hadoop Streaming redirigirá los bloques de datos de HDFS a la entrada estándar de este script. El script no necesita saber nada sobre HDFS. Es una hermosa abstracción.
*   `print(f'{word}\t1')`: La salida estándar es la forma de comunicarse con el framework de Hadoop. El tabulador (`\t`) es el delimitador por defecto entre la clave y el valor. Cada `print` es una "emisión".
*   **Idempotencia:** Este mapper es idempotente. Si se ejecuta dos veces sobre el mismo dato, producirá la misma salida. Esto es crucial para la tolerancia a fallos.

#### El Reducer: `reducer.py`

Hadoop garantiza que todos los valores para una misma clave llegarán al mismo reducer, y además, llegarán juntos y ordenados. El reducer solo tiene que iterar y agregar.

```python
#!/usr/bin/env python
import sys

def main():
    """
    Lee pares (clave, valor) ordenados de stdin y suma los valores para cada clave.
    Emite el resultado (palabra, recuento_total) a stdout.
    """
    current_word = None
    current_count = 0
    
    for line in sys.stdin:
        line = line.strip()
        
        # 1. Parsear la entrada (clave y valor)
        try:
            word, count = line.split('\t', 1)
            count = int(count)
        except ValueError:
            # Ignorar líneas malformadas
            continue
            
        # 2. La magia del reducer: aprovechar la entrada ordenada
        #    Si la palabra es la misma que la anterior, acumulamos el contador.
        if current_word == word:
            current_count += count
        else:
            # Si encontramos una nueva palabra, emitimos el resultado de la anterior.
            if current_word:
                print(f'{current_word}\t{current_count}')
            
            # Y reiniciamos los contadores para la nueva palabra.
            current_word = word
            current_count = count
            
    # 3. No olvidar emitir la última palabra
    if current_word:
        print(f'{current_word}\t{current_count}')

if __name__ == "__main__":
    main()
```
**Explicación del "Por qué":**
*   **El "Shuffle and Sort"**: Entre el Map y el Reduce, Hadoop realiza una fase mágica y costosa llamada "Shuffle and Sort". Agrupa todas las salidas de los mappers por clave y las ordena. Por eso el reducer puede asumir que verá `(gato, 1)`, `(gato, 1)`, `(gato, 1)`... todo junto, antes de ver `(perro, 1)`. El código del reducer depende críticamente de esta garantía.
*   **Lógica de cambio de clave:** El `if current_word == word:` es el patrón central de casi todos los reducers. Es simple, eficiente en memoria (solo necesita mantener el estado de una clave a la vez) y explota la garantía de ordenación de Hadoop.

#### Ejecución en un Cluster (Sintaxis conceptual)

```bash
# 1. Asegurarse de que los scripts son ejecutables
chmod +x mapper.py reducer.py

# 2. Poner los datos de entrada en HDFS
hdfs dfs -put libros_texto /user/miusuario/input

# 3. Ejecutar el trabajo de Hadoop Streaming
hadoop jar /path/to/hadoop-streaming.jar \
    -files mapper.py,reducer.py \
    -mapper mapper.py \
    -reducer reducer.py \
    -input /user/miusuario/input \
    -output /user/miusuario/wordcount_output

# 4. Ver los resultados
hdfs dfs -cat /user/miusuario/wordcount_output/part-00000
```

#### Comparación: "Antes vs Después"

| Enfoque                                    | Problema con Datos Masivos                                                                                             | Solución Hadoop                                                                                                        |
|--------------------------------------------|------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------|
| **Script en una sola máquina**             | El script tarda días en ejecutarse. Si la máquina falla a mitad de camino, hay que empezar de cero. El disco no es suficiente. | El trabajo se divide en miles de tareas paralelas. Si un nodo falla, YARN reasigna su trabajo a otro. El tiempo se reduce a minutos/horas. |
| **Base de Datos Relacional** (`GROUP BY`)  | Ingestar terabytes de texto no estructurado es lento y costoso. La consulta `GROUP BY` puede bloquear la base de datos.    | HDFS almacena los datos en su formato nativo. El procesamiento por lotes no interfiere con sistemas transaccionales. |

---

### 5. Nivel Senior - Conceptos Avanzados

Aquí es donde separamos a los que usan Hadoop de los que lo entienden de verdad.

#### Optimizaciones y Técnicas Avanzadas

*   **Combiners:** Un "mini-reducer" que se ejecuta en el mismo nodo que el mapper. Su objetivo es reducir la cantidad de datos que se envían por la red durante la fase de Shuffle, que es la más costosa. En nuestro Word Count, un Combiner podría sumar los `1`s de un mismo documento *antes* de enviarlos. El Combiner es una optimización, por lo que debe producir el mismo tipo de salida que el mapper.
    *   **ASCII Diagram:**
        ```
        Mapper 1 Output: (the, 1), (quick, 1), (brown, 1), (fox, 1), (the, 1)
             |
             V
        Combiner on Node 1: (the, 2), (quick, 1), (brown, 1), (fox, 1)  <-- MENOS DATOS A ENVIAR
             |
             V
        --- NETWORK (SHUFFLE) ---
             |
             V
        Reducer
        ```
*   **Partitioners:** Controlan a qué reducer se envía un par clave-valor. Por defecto, es un hash de la clave (`hash(key) % num_reducers`). Un Partitioner personalizado permite agrupaciones más inteligentes. Por ejemplo, podrías querer que todas las palabras que empiezan por "a" vayan a un reducer, las de "b" a otro, etc.
*   **Speculative Execution:** Hadoop monitoriza las tareas. Si una tarea es anormalmente lenta (quizás por un disco defectuoso en ese nodo), Hadoop puede lanzar una copia "especulativa" de la misma tarea en otro nodo. La primera que termine "gana", y la otra se cancela. Es una forma de mitigar el problema de los "stragglers" (rezagados).
    > "La ejecución especulativa no reduce el trabajo total realizado; de hecho, lo aumenta. El objetivo es reducir el tiempo de respuesta del trabajo." — **Tom White**, *Hadoop: The Definitive Guide* (2015)
*   **Compresión de Datos:** El I/O (lectura de disco y transferencia de red) es casi siempre el cuello de botella. Comprimir los datos en HDFS (con formatos como Snappy o LZO, que son "splittables") y la salida intermedia de los mappers puede acelerar drásticamente los trabajos. Es un trade-off clásico: CPU (para comprimir/descomprimir) vs. I/O.

#### Trade-offs: Cuándo Usar y Cuándo NO Usar Hadoop

Esta es la pregunta más importante para un senior. Hadoop no es una bala de plata.

| Característica        | Cuándo USAR Hadoop (MapReduce/HDFS)                                                              | Cuándo NO USAR Hadoop (y qué usar en su lugar)                                                                |
|-----------------------|--------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------|
| **Latencia**          | **Procesamiento por lotes (Batch) de alto rendimiento.** Análisis que pueden tardar minutos u horas. | **Baja latencia / Consultas interactivas.** Necesitas respuestas en segundos. (Usa: Spark, Presto, Druid, ClickHouse). |
| **Volumen de Datos**  | **Terabytes y Petabytes.** Cuando los datos no caben en una sola máquina.                          | **Gigabytes o menos.** La sobrecarga de Hadoop es excesiva ("Hadoverkill"). (Usa: Pandas, Dask, una base de datos PostgreSQL/MySQL). |
| **Acceso a Datos**    | **Lecturas secuenciales de grandes archivos.** Análisis de todo el conjunto de datos.              | **Búsquedas aleatorias y actualizaciones puntuales.** Necesitas modificar un solo registro. (Usa: HBase, Cassandra, una RDBMS). |
| **Estructura de Datos** | **Datos no estructurados o semi-estructurados** (logs, texto, JSON, imágenes).                    | **Datos altamente estructurados con transacciones ACID.** (Usa: PostgreSQL, Oracle, MySQL).                     |

La broma interna es que si tu "Big Data" cabe en la RAM de tu portátil, probablemente no necesites Hadoop.