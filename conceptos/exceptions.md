# Exceptions

¡Excelente! Preparémonos para una inmersión profunda en el manejo de excepciones. Este no es solo un tema de sintaxis (`try/catch`), es un pilar fundamental del diseño de software robusto y mantenible. Un manejo de excepciones de nivel senior distingue a un programador que simplemente escribe código que funciona, de un ingeniero que construye sistemas resilientes.

Aquí tienes una guía exhaustiva en formato Markdown.

---

# Guía Profunda sobre Excepciones: De Novato a Senior

## 1. Introducción: Más Allá de los Códigos de Error

Antes de las excepciones, el manejo de errores se basaba principalmente en códigos de retorno. Una función devolvía `0` si todo iba bien, `-1` si había un error de fichero, `-2` si la red fallaba, etc.

```c
// Estilo antiguo con códigos de error
int resultado = haz_algo_critico();
if (resultado == -1) {
    // Manejar error de fichero
} else if (resultado == -2) {
    // Manejar error de red
}
```

Este enfoque tiene problemas graves:
*   **Código Ofuscado:** La lógica de negocio se mezcla constantemente con la comprobación de errores.
*   **Frágil:** ¿Qué pasa si el programador olvida comprobar un código de retorno? El error se propaga silenciosamente, llevando a un estado corrupto.
*   **Pérdida de Contexto:** Un simple `-1` no te dice *qué* fichero falló, en *qué* línea de código, ni la secuencia de llamadas que llevó al error.

Las excepciones resuelven esto separando el "camino feliz" (happy path) del código de manejo de errores, y preservando el contexto completo del fallo.

> **Citación:** "De hecho, una de las ventajas más importantes de las excepciones es que separan los detalles del manejo de errores del código principal de un programa." - *Thinking in Java*, Bruce Eckel.

## 2. Anatomía de una Excepción

Una excepción no es solo un mensaje de error. Es un objeto rico en información que contiene, como mínimo:

1.  **Tipo de Excepción:** La clase de la excepción (ej. `FileNotFoundException`, `NullPointerException`, `IllegalArgumentException`). Esto permite manejar diferentes errores de forma distinta.
2.  **Mensaje:** Una cadena de texto descriptiva del error.
3.  **Stack Trace (Traza de Pila):** La "joya de la corona". Es una instantánea de la pila de llamadas en el momento del error. Te dice exactamente la secuencia de métodos que se llamaron para llegar al punto del fallo, incluyendo ficheros y números de línea. Es la herramienta de depuración más valiosa.
4.  **Excepción Interna (Inner Exception / Cause):** Una excepción puede "envolver" a otra. Esto es crucial para no perder la causa raíz de un problema, como veremos en los patrones de diseño.

## 3. El Flujo de Control: `try`, `catch`, `finally`, `throw`

Esta es la mecánica básica, pero con matices importantes.

*   `try`: Encierra el código que *podría* lanzar una excepción.
*   `throw` (o `raise` en Python): Crea y lanza una instancia de un objeto de excepción. En este punto, el flujo normal del programa se detiene.
*   **El Desenrollado de Pila (Stack Unwinding):** El runtime busca hacia atrás en la pila de llamadas un bloque `catch` que pueda manejar ese tipo de excepción.
*   `catch`: Si se encuentra un manejador compatible, el desenrollado de pila se detiene y el código dentro del `catch` se ejecuta.
*   `finally`: Este bloque se ejecuta **siempre**, sin importar si se lanzó una excepción, si se capturó o si el `try` terminó con éxito. Su propósito principal es la **liberación de recursos** (cerrar ficheros, conexiones de red, transacciones de BD).

```java
// Ejemplo canónico
Connection conn = null;
try {
    conn = database.getConnection();
    // ... hacer algo con la conexión
} catch (SQLException e) {
    // Manejar el error específico de SQL
    log.error("Error de base de datos", e);
    throw new InfrastructureException("No se pudo completar la operación de BD", e); // Envolver la excepción
} catch (Exception e) {
    // Un catch-all genérico (usar con cuidado)
    log.error("Error inesperado", e);
} finally {
    if (conn != null) {
        try {
            conn.close(); // Liberar el recurso
        } catch (SQLException e) {
            log.warn("No se pudo cerrar la conexión", e);
        }
    }
}
```

**Mejora Moderna: `try-with-resources` (Java) o `using` (C#)**

El bloque `finally` para cerrar recursos es tan común y propenso a errores (¿qué pasa si `close()` también lanza una excepción?) que los lenguajes modernos introdujeron una sintaxis más limpia.

```java
// Mucho más limpio y seguro
try (Connection conn = database.getConnection();
     Statement stmt = conn.createStatement()) {
    // ... hacer algo con conn y stmt
} catch (SQLException e) {
    log.error("Error de base de datos", e);
    throw new InfrastructureException("No se pudo completar la operación de BD", e);
}
```

## 4. Tipos de Excepciones: La Gran Controversia

Este es un tema de debate que define la filosofía de un lenguaje.

### a) Checked vs. Unchecked Exceptions (Principalmente en Java)

*   **Checked Exceptions (Excepciones Verificadas):** Heredan de `java.lang.Exception` (pero no de `RuntimeException`). Son condiciones de error "previsibles" y recuperables de las que un cliente de una API debería saber. El compilador de Java te **obliga** a manejarlas, ya sea con un `try-catch` o declarando que tu método las relanza con `throws`. Ejemplos: `IOException`, `SQLException`.
    *   **Filosofía:** Forzar al programador a pensar en los fallos. Si llamas a un método que puede fallar al leer un fichero, *debes* manejar esa posibilidad.
    *   **Crítica:** Conduce a un código verboso y puede violar la encapsulación. Si una capa de bajo nivel lanza una `SQLException`, ¿debería la capa de UI saber sobre SQL? No. Esto lleva a bloques `catch` vacíos o a relanzar excepciones que no tienen sentido en un contexto superior.

*   **Unchecked Exceptions (Excepciones No Verificadas):** Heredan de `java.lang.RuntimeException`. Son errores que indican un **fallo de programación (bug)** o un problema irrecuperable en el entorno. El compilador no te obliga a manejarlas. Ejemplos: `NullPointerException`, `IllegalArgumentException`, `ArrayIndexOutOfBoundsException`.
    *   **Filosofía:** Estos errores no deberían ocurrir en un programa correcto. Si ocurren, indican que hay un bug que debe ser corregido, no manejado en tiempo de ejecución. Atrapar un `NullPointerException` suele ser un mal "parche" para un problema de lógica subyacente.

> **Citación:** Joshua Bloch en su libro *Effective Java*, dedica un capítulo entero a este tema. Su recomendación general es: "Usa excepciones verificadas para condiciones de las cuales el llamador puede recuperarse razonablemente. Usa excepciones en tiempo de ejecución para indicar errores de programación." (Item 70, 3rd Edition).

La mayoría de los lenguajes modernos (C#, Python, Kotlin, Scala, Go con su `panic/recover`) han optado por **no usar excepciones verificadas**, favoreciendo la flexibilidad y un código menos verboso.

## 5. Principios y Buenas Prácticas (Nivel Senior)

Aquí es donde se demuestra la maestría.

### 1. **NO uses excepciones para el control de flujo normal.**
Lanzar y capturar una excepción es una operación computacionalmente **costosa** porque requiere capturar y construir toda la traza de pila.

```java
// ANTI-PATRÓN
try {
    for (int i = 0; ; i++) {
        System.out.println(miArray[i]);
    }
} catch (ArrayIndexOutOfBoundsException e) {
    // Bucle terminado, continuar...
}

// CORRECTO
for (int i = 0; i < miArray.length; i++) {
    System.out.println(miArray[i]);
}
```

> **Citación:** "No uses excepciones para el control de flujo... Son para el manejo de errores." - *Clean Code: A Handbook of Agile Software Craftsmanship*, Robert C. Martin.

### 2. **Lanza excepciones específicas, no genéricas.**
No hagas `throw new Exception("Error")`. Crea tus propias clases de excepción semánticas.

```java
// MAL
public User findUser(String id) {
    if (id == null) throw new Exception("ID es nulo");
    // ...
}

// BIEN
public class UserNotFoundException extends RuntimeException {
    public UserNotFoundException(String userId) {
        super("No se encontró el usuario con ID: " + userId);
    }
}

public User findUser(String id) {
    if (id == null) throw new IllegalArgumentException("ID no puede ser nulo");
    User user = userRepository.findById(id);
    if (user == null) throw new UserNotFoundException(id);
    return user;
}
```
Esto permite a los llamadores capturar selectivamente los errores que les interesan.

### 3. **NO "tragues" excepciones (Empty Catch Block).**
Este es uno de los peores anti-patrones. Oculta un problema, dejando el sistema en un estado potencialmente inconsistente.

```java
// ¡TERRIBLE! NUNCA HAGAS ESTO
try {
    // ... algo que puede fallar
} catch (Exception e) {
    // Silencio... el error desaparece mágicamente.
}
```
Como mínimo, registra el error: `log.error("Ocurrió un error inesperado", e);`.

### 4. **Preserva la causa raíz: Envuelve las excepciones (Exception Wrapping).**
Cuando capturas una excepción de una capa inferior y lanzas una nueva excepción más apropiada para tu capa actual, **incluye la excepción original** como la "causa" o "inner exception".

```java
// MAL: Se pierde la información de la SQLException
catch (SQLException e) {
    throw new DataAccessException("Error al acceder a los datos.");
}

// BIEN: Se preserva la traza de pila original
catch (SQLException e) {
    throw new DataAccessException("Error al acceder a los datos.", e); // Pasamos 'e' como causa
}
```
Sin esto, la depuración en sistemas multicapa se vuelve una pesadilla.

### 5. **Limpia los recursos en `finally` (o su equivalente).**
Ya cubierto, pero es tan crucial que merece ser repetido. Garantiza que los recursos se liberen incluso si ocurre un error.

### 6. **Lanza excepciones al nivel de abstracción correcto.**
Una función que calcula una factura no debería lanzar una `SQLException`. Debería lanzar una `BillingException`. La capa de servicio es responsable de *traducir* las excepciones de bajo nivel (como `SQLException` o `IOException`) a excepciones que tengan sentido para su dominio de negocio. Este es el patrón **Exception Translation**.

### 7. **Define una estrategia de excepciones para tu aplicación.**
Decide como equipo: ¿Qué excepciones serán `checked` (si aplica)? ¿Cuáles serán `unchecked`? ¿Qué información deben contener? ¿Cómo se registrarán (logging)? ¿Qué excepciones provocarán una respuesta HTTP 500 vs. una 404? Esta consistencia es clave en proyectos grandes.

## 6. Patrones de Diseño Avanzados y Alternativas

Un ingeniero senior no solo usa excepciones, sino que sabe cuándo *no* usarlas.

### a) Result / Either Monad
Popularizado por lenguajes funcionales (Haskell, Scala, Rust), este patrón está ganando tracción en todas partes. En lugar de lanzar una excepción para un fallo *esperado* (ej. validación de datos, un usuario no encontrado), la función devuelve un objeto que representa tanto el éxito como el fallo.

```java
// Pseudocódigo de un objeto Result
public class Result<T, E> {
    private final T value;
    private final E error;

    // Métodos para saber si es éxito o error y obtener el valor/error
}

public Result<User, ValidationError> createUser(UserData data) {
    if (!data.isValid()) {
        return Result.failure(new ValidationError("Datos inválidos"));
    }
    User user = new User(data);
    return Result.success(user);
}

// Uso:
Result<User, ValidationError> result = createUser(data);
if (result.isSuccess()) {
    // ...
} else {
    // ... manejar el error de validación
}
```
**Ventaja:** Hace los posibles fallos explícitos en la firma del método sin la controversia de las `checked exceptions`. Es ideal para errores de dominio y validación, que no son realmente "excepcionales".

### b) Null Object Pattern
En lugar de devolver `null` y arriesgarte a un `NullPointerException`, devuelves un objeto especial que implementa la misma interfaz pero tiene un comportamiento "nulo" o por defecto.

```java
public interface User {
    String getName();
    boolean hasAccess();
}

public class RealUser implements User { /* ... */ }

public class NullUser implements User {
    public String getName() { return "Guest"; }
    public boolean hasAccess() { return false; }
}

// En lugar de devolver null, devuelves una instancia de NullUser.
// El código cliente no necesita comprobar si es nulo.
```

### c) Circuit Breaker Pattern
En sistemas distribuidos, si un servicio remoto falla repetidamente, seguir intentando llamarlo puede agotar los recursos (threads, sockets) y causar fallos en cascada. El patrón Circuit Breaker envuelve la llamada y, después de un número de fallos, "abre el circuito" y falla inmediatamente sin intentar la llamada, durante un tiempo.

> **Citación:** Este patrón fue popularizado y documentado extensamente por Michael Nygard en su libro *Release It!* y por Martin Fowler en su blog.

## 7. Consideraciones de Rendimiento

Como se mencionó, `throw` es costoso. La JVM (o el runtime correspondiente) debe:
1.  Detener la ejecución.
2.  Crear un nuevo objeto de excepción.
3.  **Recorrer toda la pila de llamadas (stack walk) para construir la traza de pila.** Este es el paso más caro.
4.  Buscar un manejador `catch`.

**Conclusión de rendimiento:** Usa excepciones para lo que son: **condiciones excepcionales**. No para errores de validación en un formulario que ocurren el 50% de las veces. Para eso, el patrón `Result` es mucho más eficiente.

## 8. Excepciones en el Mundo Asíncrono y Concurrente

Aquí las cosas se complican. Si un `Thread` o una `Task` lanza una excepción, ¿quién la captura?

*   **Java (`CompletableFuture`):** La excepción se almacena dentro del `Future`. No se lanza hasta que llamas a `.get()` o la manejas explícitamente con métodos como `.exceptionally()` o `.handle()`.
*   **.NET (`Task`):** Similar a Java. La excepción se envuelve en una `AggregateException` y se relanza cuando haces `await` sobre la tarea o accedes a su propiedad `.Result`.
*   **JavaScript (`Promise`):** Una excepción en una `Promise` la pone en estado "rejected". Debes manejarla con `.catch()` o en un bloque `try/catch` si usas `async/await`.

El principio clave es que las excepciones en código asíncrono no se propagan "mágicamente". Deben ser manejadas explícitamente en el punto donde se sincroniza el resultado de la operación asíncrona.

## Conclusión Final: La Filosofía de un Senior

Un desarrollador junior ve las excepciones como una forma de evitar que el programa se caiga. Un desarrollador senior las ve como una herramienta crítica para construir sistemas **robustos, depurables y mantenibles**.

*   **Robustez:** El sistema puede anticipar y manejar fallos sin corromper su estado.
*   **Depurabilidad:** Cuando algo falla, las excepciones proporcionan un contexto rico y preciso (stack trace, causa raíz) que permite diagnosticar el problema rápidamente.
*   **Mantenibilidad:** El código de negocio no está contaminado con la lógica de errores, y la estrategia de excepciones es clara y consistente en toda la aplicación.

Dominar las excepciones es dominar el arte de prepararse para el fracaso, que es, paradójicamente, la clave para construir software exitoso.

---
### Lecturas Recomendadas

1.  ***Effective Java, 3rd Edition*** de Joshua Bloch (Capítulos 10 sobre Excepciones).
2.  ***Clean Code: A Handbook of Agile Software Craftsmanship*** de Robert C. Martin (Capítulo 7 sobre Manejo de Errores).
3.  ***Release It! Design and Deploy Production-Ready Software*** de Michael T. Nygard (Para patrones de resiliencia como Circuit Breaker).
4.  **El blog de Martin Fowler** (martinfowler.com) para artículos sobre patrones de diseño de software.
