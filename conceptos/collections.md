# collections

Claro. Prepárate para una inmersión profunda en el mundo de las colecciones. Este no es un tutorial para principiantes; es una guía exhaustiva diseñada para cimentar los conceptos, las compensaciones y los patrones de pensamiento que definen a un desarrollador senior.

# Guía Profunda de Colecciones para el Desarrollador Senior

Un desarrollador junior sabe *qué* colección usar (un `List` para una secuencia, un `Map` para pares clave-valor). Un desarrollador senior entiende el *porqué*, el *cómo* funciona internamente y las profundas implicaciones de su elección en el rendimiento, la concurrencia y la mantenibilidad del sistema.

> "I will, in fact, claim that the difference between a bad programmer and a good one is whether he considers his code or his data structures more important. Bad programmers worry about the code. Good programmers worry about data structures and their relationships." — Linus Torvalds

---

## 1. Los Pilares Fundamentales: Más Allá de la Superficie

Antes de sumergirnos en implementaciones específicas, un senior debe dominar los conceptos abstractos que gobiernan todas las colecciones.

### 1.1. Interfaz vs. Implementación: El Contrato Sagrado

Este es, quizás, el principio más importante. Un senior no programa contra `ArrayList` o `HashMap`; programa contra `List` o `Map`.

*   **Interfaz (El "Qué"):** Define un contrato. `List` garantiza que tendrás elementos en una secuencia, que podrás acceder a ellos por un índice y que podrás iterarlos. No dice *cómo* se almacena.
*   **Implementación (El "Cómo"):** Es la materialización de ese contrato. `ArrayList` lo implementa con un array dinámico subyacente. `LinkedList` lo implementa con una lista de nodos doblemente enlazados.

**¿Por qué es crucial?** Permite la flexibilidad y el polimorfismo. Puedes escribir un método que acepte una `List` y funcionará con cualquier implementación. Si mañana descubres que una `LinkedList` es más performante para tu caso de uso, solo cambias la línea de instanciación (`new LinkedList<>()`) sin tocar el resto del código que depende de la interfaz.

> "Program to an interface, not an implementation." — Erich Gamma, Richard Helm, Ralph Johnson, and John Vlissides, "Design Patterns: Elements of Reusable Object-Oriented Software" (The Gang of Four).

### 1.2. Genericidad (Generics/Templates): La Seguridad de Tipos

Las colecciones pre-modernas almacenaban `Object`. Esto era una fuente constante de errores en tiempo de ejecución (`ClassCastException`). Los genéricos resolvieron esto moviendo la verificación de tipos al tiempo de compilación.

Un senior entiende que los genéricos no son solo azúcar sintáctico. Son una herramienta fundamental para:
1.  **Seguridad de Tipos (Type Safety):** El compilador garantiza que solo puedes añadir `String` a una `List<String>`.
2.  **Claridad del Código:** La intención del código es explícita.
3.  **Reutilización:** Creas algoritmos que operan sobre "una colección de T" (`<T>`), sin importar qué es T.

### 1.3. El Patrón Iterador (Iterator Pattern)

El patrón Iterador proporciona una forma de acceder a los elementos de un objeto agregado secuencialmente sin exponer su representación subyacente. Es la base del bucle `for-each`.

Un senior sabe que:
*   **Abstrae el Recorrido:** No te importa si estás recorriendo un array, una lista enlazada o las claves de un árbol. La lógica es `while(iterator.hasNext()) { iterator.next(); }`.
*   **Permite Modificación Segura (a veces):** El método `iterator.remove()` es la única forma segura de modificar una colección mientras se itera sobre ella. Modificar la colección directamente (p. ej., `list.remove()`) durante un bucle `for-each` lanzará una `ConcurrentModificationException` en muchas implementaciones (fail-fast).
*   **Puede ser "Lazy":** Algunos iteradores, especialmente en programación funcional, no cargan todos los elementos en memoria de inmediato.

---

## 2. Anatomía de las Estructuras de Datos Subyacentes

Aquí es donde separamos al senior del resto. No basta con saber que `ArrayList` es rápido para el acceso por índice; hay que saber *por qué* en términos de hardware y ciencia de la computación.

### 2.1. Arrays y Arrays Dinámicos (Base de `ArrayList`, `Vector`, Python `list`)

*   **Cómo Funciona:** Un bloque contiguo de memoria. Para acceder al elemento `i`, la CPU calcula `(dirección_de_inicio) + i * (tamaño_del_elemento)`. Esta es una operación matemática simple y extremadamente rápida.
*   **Complejidad Big O:**
    *   Acceso por índice (`get(i)`): **O(1)**. La joya de la corona.
    *   Añadir al final (`add(value)`): **O(1) amortizado**. Es O(1) la mayoría de las veces, pero cuando el array se llena, se debe crear uno nuevo (normalmente 1.5x o 2x el tamaño), copiar todos los elementos antiguos y luego añadir el nuevo. Esta operación costosa de O(n) se "amortiza" entre las muchas adiciones baratas.
    *   Insertar/Eliminar en medio (`add(i, value)`, `remove(i)`): **O(n)**. Requiere desplazar todos los elementos a la derecha o a la izquierda del índice `i`.
*   **Implicaciones Senior (Cache Locality):**
    *   **Cache-Friendly:** Como los datos son contiguos en memoria, cuando la CPU carga un elemento, es muy probable que los elementos cercanos (que probablemente necesitarás a continuación) ya estén en la caché L1/L2 de la CPU. Esto se llama **localidad espacial de referencia** y es una de las optimizaciones de hardware más importantes. Un `ArrayList` es un sueño para la caché.

> **Citación:** La importancia de la localidad de caché está profundamente documentada en manuales de optimización de CPU como el "Intel® 64 and IA-32 Architectures Optimization Reference Manual".

### 2.2. Listas Enlazadas (Base de `LinkedList`)

*   **Cómo Funciona:** Una cadena de nodos. Cada nodo contiene el dato y uno o dos punteros (al siguiente y/o al anterior). Los nodos pueden estar dispersos por toda la memoria.
*   **Complejidad Big O:**
    *   Acceso por índice (`get(i)`): **O(n)**. Debes empezar desde el principio (o el final, si es doblemente enlazada y `i > n/2`) y seguir los punteros `i` veces.
    *   Añadir/Eliminar al principio/final: **O(1)**. Solo se manipulan los punteros `head` y `tail`.
    *   Insertar/Eliminar en medio (si ya tienes un puntero/iterador al nodo): **O(1)**. Si no, es O(n) para encontrarlo primero.
*   **Implicaciones Senior (Cache Locality):**
    *   **Cache-Unfriendly:** Cada `next()` puede resultar en un **cache miss**, ya que el siguiente nodo puede estar en una ubicación de memoria completamente diferente. Esto hace que iterar sobre una `LinkedList` sea significativamente más lento que sobre un `ArrayList`, incluso si su complejidad Big O es la misma (O(n)).
    *   **Memory Overhead:** Cada nodo requiere memoria extra para los punteros. Una `LinkedList<Long>` puede consumir 3-4 veces más memoria que un `long[]`.

**Veredicto Senior:** Usa `ArrayList` casi siempre. `LinkedList` solo brilla en escenarios muy específicos donde realizas una gran cantidad de inserciones/eliminaciones en los extremos o en el medio de una lista muy grande *y ya tienes un iterador en la posición correcta*.

### 2.3. Tablas Hash (Base de `HashMap`, `HashSet`, Python `dict`, `set`)

Esta es la estructura de datos más importante para un programador de aplicaciones.

*   **Cómo Funciona:** Utiliza un array (llamado "tabla" o "buckets"). Para almacenar un par `(key, value)`:
    1.  Calcula un `hashCode()` para la `key`. Este es un número entero.
    2.  Convierte ese hash en un índice del array, normalmente con `index = hashCode % array.length`.
    3.  Almacena el valor en ese índice.
*   **El Problema: Colisiones:** ¿Qué pasa si dos claves diferentes producen el mismo índice? Esto se llama colisión.
    *   **Solución Común (Separate Chaining):** En lugar de almacenar un solo valor en cada índice del array, se almacena una lista enlazada (o, a partir de Java 8, un árbol balanceado si la lista crece mucho) de todos los valores cuyo hash colisionó en ese índice.
*   **Complejidad Big O:**
    *   Inserción, Búsqueda, Eliminación: **O(1) en promedio**. Si la función de hash es buena y las colisiones son mínimas, estas operaciones son casi instantáneas.
    *   Peor Caso: **O(n)**. Si todas las claves colisionan en el mismo bucket, la tabla hash degenera en una lista enlazada.
*   **Implicaciones Senior (El Contrato `hashCode()` y `equals()`):**
    *   Un `HashMap` solo funciona correctamente si se cumple este contrato:
        1.  Si `a.equals(b)` es `true`, entonces `a.hashCode()` **debe ser** igual a `b.hashCode()`.
        2.  Si `a.hashCode()` es diferente de `b.hashCode()`, entonces `a.equals(b)` **debe ser** `false`.
    *   Un mal `hashCode()` (p. ej., `return 1;`) es desastroso para el rendimiento. Un `hashCode()` que cambia si el objeto muta romperá el `Map` (no podrás encontrar el objeto de nuevo).
    *   Por eso, las claves de un `Map` deben ser inmutables o, al menos, no deben mutar de una manera que afecte a `equals()` o `hashCode()` mientras están en el mapa.

> **Citación:** "The Art of Computer Programming, Vol. 3: Sorting and Searching" de Donald Knuth contiene uno de los análisis más exhaustivos sobre hashing y resolución de colisiones.

### 2.4. Árboles Autobalanceados (Base de `TreeMap`, `TreeSet`)

*   **Cómo Funciona:** Típicamente un Árbol Rojo-Negro. Es un árbol binario de búsqueda que se rebalancea automáticamente tras inserciones y eliminaciones para garantizar que la altura del árbol sea siempre logarítmica con respecto al número de nodos.
*   **Complejidad Big O:**
    *   Inserción, Búsqueda, Eliminación: **O(log n)**. Garantizado.
*   **Implicaciones Senior:**
    *   **Ordenamiento:** La principal ventaja es que siempre mantiene las claves ordenadas. Esto permite operaciones como "encontrar el elemento más pequeño mayor que X", "obtener todas las claves en un rango" o simplemente iterar en orden.
    *   **Requisitos:** Las claves deben ser comparables, ya sea implementando la interfaz `Comparable` o proporcionando un `Comparator` en el constructor.
    *   **Rendimiento:** Aunque O(log n) es muy rápido, es más lento que el O(1) de un `HashMap`. Elige `TreeMap` solo cuando necesites el ordenamiento.

---

## 3. Temas Avanzados: El Territorio del Senior

### 3.1. Concurrencia y Sincronización

En un entorno multihilo, usar colecciones no seguras (`ArrayList`, `HashMap`) puede llevar a corrupción de datos, bucles infinitos y `ConcurrentModificationException`.

*   **Enfoque 1: Wrappers Sincronizados (Legado)**
    *   `Collections.synchronizedList(new ArrayList<>())`
    *   **Cómo funciona:** Envuelve cada método de la colección en un bloque `synchronized(this)`.
    *   **Problema:** Es un cuello de botella. Solo un hilo puede acceder a la colección a la vez para cualquier operación (lectura o escritura). Mal rendimiento bajo alta contención. Además, las operaciones compuestas (como `if (!list.contains(x)) { list.add(x); }`) no son atómicas y requieren bloqueo manual externo.

*   **Enfoque 2: Colecciones Concurrentes (El Camino Moderno)**
    *   `ConcurrentHashMap`, `CopyOnWriteArrayList`, `BlockingQueue`.
    *   **Cómo funcionan:** Utilizan mecanismos de bloqueo más finos y algoritmos sin bloqueo (lock-free) que aprovechan instrucciones a nivel de CPU como Compare-And-Swap (CAS).
    *   **`ConcurrentHashMap`:** No bloquea toda la tabla. Bloquea solo el "segmento" o "bucket" que se está modificando. Permite múltiples lecturas y escrituras simultáneas siempre que no afecten al mismo segmento. Es el estándar de oro para mapas concurrentes.
    *   **`CopyOnWriteArrayList`:** Cualquier modificación (add, set, remove) crea una copia completamente nueva del array subyacente. Las lecturas no requieren bloqueo y son muy rápidas. Ideal para colecciones que se leen mucho más de lo que se modifican (p. ej., listeners de eventos).

> **Citación:** "Java Concurrency in Practice" de Brian Goetz et al. es la biblia sobre este tema. Explica en detalle el funcionamiento interno y los patrones de uso de las colecciones concurrentes.

### 3.2. Inmutabilidad

Una colección inmutable no puede ser modificada después de su creación.

*   **Beneficios:**
    1.  **Seguridad en Hilos (Thread-Safety):** Si no se puede cambiar, es inherentemente seguro para compartir entre hilos sin necesidad de bloqueos.
    2.  **Previsibilidad:** El estado de la colección es fijo, lo que facilita el razonamiento sobre el código.
    3.  **Seguridad:** Evita que código externo modifique una colección interna de una clase.
*   **Implementaciones:**
    *   **Java:** `List.of()`, `Set.of()`, `Map.of()` (desde Java 9).
    *   **Librerías:** Guava de Google (`ImmutableList`, `ImmutableSet`).
    *   **Lenguajes:** Kotlin y Scala tienen una distinción clara entre colecciones mutables e inmutables en su biblioteca estándar.

> **Citación:** "Effective Java, 3rd Edition" de Joshua Bloch, en el "Item 17: Minimize mutability", argumenta convincentemente sobre los beneficios de la inmutabilidad para crear código robusto y simple.

### 3.3. Rendimiento y Uso de Memoria

Un senior piensa más allá del Big O.

*   **Boxing/Unboxing:** En Java, las colecciones de primitivos (`int`, `long`) requieren "envolverlos" en sus objetos correspondientes (`Integer`, `Long`). Esto tiene un coste de memoria (cada `Integer` es un objeto con una cabecera) y de rendimiento (crear estos objetos). Librerías como `Trove` o `Fastutil` ofrecen colecciones especializadas en primitivos para evitar este overhead en aplicaciones de alto rendimiento.
*   **Carga Inicial (Initial Capacity) y Factor de Carga (Load Factor):**
    *   Si sabes que un `ArrayList` o `HashMap` va a contener 10,000 elementos, inicialízalo con esa capacidad (`new ArrayList<>(10000)`). Esto evita múltiples y costosas operaciones de redimensionamiento.
    *   En un `HashMap`, el "factor de carga" (por defecto 0.75) determina cuándo se redimensiona la tabla. Un factor más bajo reduce las colisiones (mejor rendimiento) a costa de más memoria. Un factor más alto ahorra memoria pero aumenta el riesgo de colisiones. Un senior sabe cuándo ajustar estos parámetros.

### 3.4. APIs Funcionales: Streams y LINQ

Las APIs modernas como Java Streams o LINQ en .NET han cambiado la forma en que interactuamos con las colecciones.

*   **Paradigma Declarativo:** Describes *qué* quieres hacer, no *cómo* hacerlo.
    *   Imperativo: `for (User user : users) { if (user.isActive()) { ... } }`
    *   Declarativo: `users.stream().filter(User::isActive).forEach(...)`
*   **Ventajas Senior:**
    *   **Legibilidad:** A menudo, el código es más conciso y expresivo.
    *   **Paralelización:** Cambiar a `users.parallelStream()` puede paralelizar la operación con un esfuerzo mínimo (aunque requiere cuidado para evitar problemas de concurrencia).
    *   **Lazy Evaluation:** Las operaciones intermedias (`filter`, `map`) no se ejecutan hasta que se invoca una operación terminal (`forEach`, `collect`). Esto permite optimizaciones, como el "short-circuiting" (`findFirst`).

---

## 4. La Decisión Final: ¿Qué Colección Usar? (El Proceso Mental de un Senior)

Ante un problema, un senior se hace estas preguntas en orden:

1.  **¿Necesito una colección? ¿O un simple array `T[]` es suficiente?** (Si el tamaño es fijo y el rendimiento es ultra-crítico).
2.  **¿Necesito una relación clave-valor?**
    *   **Sí:** Voy a usar un `Map`.
        *   **¿Necesito que las claves estén ordenadas?**
            *   **Sí:** `TreeMap`. Soy consciente de que será O(log n).
            *   **No:** `HashMap`. Es mi opción por defecto por su rendimiento O(1).
        *   **¿Necesito mantener el orden de inserción?**
            *   **Sí:** `LinkedHashMap`.
        *   **¿Será accedido por múltiples hilos?**
            *   **Sí:** `ConcurrentHashMap`. Sin dudarlo.
3.  **No, solo necesito almacenar elementos.**
    *   **¿Necesito garantizar que no haya duplicados?**
        *   **Sí:** Voy a usar un `Set`.
            *   (Las mismas sub-preguntas que para `Map`: `HashSet` por defecto, `TreeSet` para orden, `LinkedHashSet` para orden de inserción).
    *   **No, los duplicados están bien.** Voy a usar una `List`.
        *   **¿Cuál será la operación predominante?**
            *   **Acceso por índice e iteración:** `ArrayList`. Esta es la respuesta el 99% de las veces. Pienso en la localidad de caché.
            *   **Muchas inserciones/eliminaciones en los extremos de la lista:** `LinkedList` podría ser una opción, o mejor aún, una `ArrayDeque`.
        *   **¿Será accedido por múltiples hilos?**
            *   **Lecturas masivas, escrituras raras:** `CopyOnWriteArrayList`.
            *   **Lecturas y escrituras frecuentes:** Probablemente necesite un enfoque diferente, quizás usando colas o bloqueos explícitos, ya que no hay un equivalente a `ConcurrentHashMap` para `List`.
4.  **¿Necesito un comportamiento de Cola (FIFO) o Pila (LIFO)?**
    *   **Sí:** `ArrayDeque` es casi siempre la mejor implementación para `Queue` y `Stack`. Es más eficiente que la antigua clase `Stack` y que `LinkedList`.
    *   **¿Necesito una cola bloqueante para un escenario productor-consumidor?**
        *   **Sí:** `BlockingQueue` (p. ej., `ArrayBlockingQueue`, `LinkedBlockingQueue`).

Esta guía te proporciona el conocimiento y, más importante, el *marco mental* para tratar las colecciones como lo haría un desarrollador senior. No se trata de memorizar complejidades, sino de entender las compensaciones fundamentales entre memoria, velocidad, concurrencia y simplicidad.
