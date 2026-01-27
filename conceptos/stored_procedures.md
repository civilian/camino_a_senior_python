# Stored Procedures

¡Absolutamente! Ponte cómodo, sírvete un café (o tu bebida de compilación preferida), y prepárate para un viaje profundo. No vamos a aprender simplemente a escribir un `CREATE PROCEDURE`; vamos a desmantelar el concepto, entender su alma y reconstruirlo con la sabiduría de un arquitecto de sistemas senior.

***

## La Guía Definitiva para Stored Procedures: Del Código a la Catedral

Imagina por un momento que no eres un programador, sino un maestro chef en un restaurante con estrellas Michelin. Tu cocina (la base de datos) es un lugar de precisión y velocidad. ¿Le darías a cada cocinero novato acceso libre a todos los ingredientes y les permitirías improvisar una receta compleja bajo la presión del servicio de cena? Por supuesto que no. En su lugar, crearías una receta maestra, perfeccionada y optimizada, la registrarías y simplemente le dirías al equipo: "¡Ejecuta la receta 7, el *Boeuf Bourguignon*!".

Eso, en esencia, es un Stored Procedure (SP). No es solo un trozo de código; es una receta encapsulada, una pieza de lógica consagrada, que vive dentro de los muros sagrados de la base de datos, la catedral de nuestros datos.

---

### 1. Introducción Profunda: El Nacimiento de un Contrato

#### Contexto Histórico: El Grito de la Red
A finales de los años 70 y principios de los 80, el mundo de las bases de datos estaba en plena efervescencia. El modelo relacional de Edgar F. Codd, una idea de una belleza matemática casi platónica, se estaba materializando en sistemas como System R de IBM e Ingres de Berkeley. Sin embargo, la realidad era cruda: las redes eran lentas (hablamos de kilobits por segundo), y los ordenadores cliente eran... modestos, por decir lo menos.

El problema era evidente: si una aplicación necesitaba realizar una operación compleja de cinco pasos (un `SELECT`, dos `UPDATE`, un `INSERT`, y otro `SELECT`), tenía que hacer cinco viajes de ida y vuelta a través de esa red precaria. Cada viaje era un riesgo, una latencia, un coste.

Aquí es donde entra en escena **Sybase** a mediados de los 80. Liderados por figuras como Robert Epstein, estaban construyendo un nuevo sistema de gestión de bases de datos (RDBMS) desde cero, que se convertiría en el famoso **Sybase SQL Server**. Se dieron cuenta de que podían resolver este problema de "chatter" en la red. ¿Y si, en lugar de enviar cinco comandos SQL por separado, la aplicación pudiera enviar un solo comando: "ejecuta esta lógica de cinco pasos que ya conoces"?

Así, en 1987, Sybase SQL Server introdujo una de las implementaciones comerciales más influyentes de los Stored Procedures. No fueron los únicos con ideas similares (Ingres tenía procedimientos de base de datos), pero la implementación de Sybase, con su lenguaje Transact-SQL (T-SQL), fue la que realmente prendió la mecha.

#### El Problema que Resuelve
Un Stored Procedure no es una solución en busca de un problema. Nació de necesidades ingenieriles muy concretas:

1.  **Reducción de la Latencia de Red:** Como vimos, agrupar múltiples operaciones en una sola llamada reduce drásticamente el tráfico de red. Es la diferencia entre enviar las instrucciones paso a paso por carta y enviar un libro de recetas completo de una vez.
2.  **Centralización de la Lógica de Negocio:** En lugar de que la lógica para "crear un nuevo pedido" esté dispersa en tres aplicaciones diferentes (la web, la app móvil, el sistema de back-office), se puede encapsular en un único SP, `sp_CreateNewOrder`. Esto garantiza consistencia y facilita el mantenimiento.
3.  **Seguridad y Control de Acceso:** En lugar de dar permisos de `UPDATE` o `DELETE` sobre tablas críticas a las aplicaciones, se puede otorgar únicamente el permiso de `EXECUTE` sobre un SP. El SP actúa como un guardián, un *proxy* controlado. La aplicación no necesita saber la estructura de las tablas; solo necesita conocer el contrato del SP.
4.  **Rendimiento a través de la Pre-compilación:** El motor de la base de datos puede analizar, optimizar y compilar un SP la primera vez que se ejecuta. El resultado, el "plan de ejecución", se almacena en caché. Las llamadas posteriores son mucho más rápidas porque se saltan estos costosos pasos.

#### Evolución: De Receta Simple a Hechizo Complejo
*   **Años 80 (La Génesis):** Sybase y Oracle (con PL/SQL) popularizan los SPs. Son principalmente para agrupar comandos SQL.
*   **Años 90 (La Edad de Oro):** Microsoft licencia el código de Sybase para crear su propio SQL Server, llevando T-SQL a las masas. Los SPs se vuelven más potentes, con estructuras de control de flujo (IF/ELSE, WHILE), manejo de errores (TRY/CATCH) y la capacidad de devolver conjuntos de resultados complejos. Se convierten en el pilar de la arquitectura cliente-servidor.
*   **Años 2000 (El Cisma):** Llega la era de los Object-Relational Mappers (ORMs) como Hibernate y Entity Framework. Surge una nueva filosofía: la base de datos debe ser un "almacén de persistencia tonto", y toda la lógica debe residir en la capa de aplicación orientada a objetos. Los SPs son vistos por muchos como un anti-patrón, un vestigio del pasado que viola la separación de conceptos y crea un fuerte acoplamiento con el proveedor de la base de datos. Comienza la "guerra santa" entre los defensores de los ORM y los de los SPs.
*   **Años 2010 en adelante (El Renacimiento Matizado):** El péndulo vuelve a un punto medio. En el mundo de los microservicios, los SPs pueden definir una API de datos clara y estable para un servicio. En aplicaciones de alto rendimiento y procesamiento de datos masivos (ETL, Data Warehousing), su eficiencia es innegable. La comunidad entiende que no son una bala de plata, sino una herramienta poderosa en el arsenal de un ingeniero senior, para ser usada con discernimiento.

---

### 2. Fundamentos Teóricos y Matemáticos: El Fantasma en la Máquina Relacional

Aunque un SP parece puramente práctico, sus cimientos se hunden en principios computacionales profundos.

#### Base Teórica: El Matrimonio de lo Declarativo y lo Imperativo
El SQL estándar, basado en el álgebra relacional de Codd, es un lenguaje **declarativo**. Le dices al sistema *qué* quieres ("dame todos los usuarios de España"), pero no *cómo* conseguirlo. El optimizador de consultas de la base de datos se encarga del "cómo".

Los lenguajes de los Stored Procedures (T-SQL, PL/SQL, PL/pgSQL) introducen el mundo **imperativo** dentro de la base de datos. Permiten escribir algoritmos paso a paso: "primero, declara una variable; luego, abre un cursor; itera sobre los resultados; si se cumple una condición, actualiza una tabla; si no, inserta en otra".

> "La esencia de la computación es la descripción de los procesos. El propósito de un lenguaje de programación es proporcionar un marco para la organización de estos procesos." — **Harold Abelson & Gerald Jay Sussman**, *Structure and Interpretation of Computer Programs* (1985)

Los SPs son el puente entre estos dos mundos. Permiten organizar procesos complejos (imperativo) que operan sobre conjuntos de datos (declarativo), todo dentro del mismo entorno optimizado.

#### Principios Subyacentes
*   **Abstracción:** Un SP es una abstracción perfecta. Oculta la complejidad del esquema de la base de datos subyacente. La aplicación que llama a `sp_GetUserProfile(userId)` no necesita saber si los datos del perfil están en una, tres o cinco tablas normalizadas.
*   **Encapsulación:** Este es un principio tomado directamente de la programación orientada a objetos. Un SP encapsula la lógica de operación de los datos junto con los datos mismos. La tabla `Cuentas` y el SP `sp_TransferirFondos` forman una unidad cohesiva.
*   **Turing Completeness:** Los lenguajes como T-SQL y PL/SQL son Turing completos. Esto significa que, teóricamente, pueden resolver cualquier problema computable que una máquina de Turing pueda resolver. Es una afirmación poderosa que subraya que no son simples lenguajes de scripting, sino entornos de programación completos, aunque especializados.

#### Relación con la Historia de la Computación
El concepto de "procedimiento almacenado" es un eco de ideas más antiguas. En los albores de la programación, la idea de subrutinas o funciones que podían ser llamadas repetidamente fue un avance monumental (atribuido a pioneros como Maurice Wilkes con el EDSAC). Los SPs son la manifestación de esa idea en el dominio de las bases de datos. Son las subrutinas de la catedral de datos.

---

### 3. Evolución Histórica Detallada: Un Relato de Gigantes y Revoluciones

| Año(s) | Evento Clave | Figuras/Empresas Clave | Contexto Computacional |
| :--- | :--- | :--- | :--- |
| **1970** | Edgar F. Codd publica "A Relational Model of Data for Large Shared Data Banks". | Edgar F. Codd (IBM) | Nace la teoría relacional. Los sistemas jerárquicos y de red dominan. |
| **1974-79** | Desarrollo de System R en IBM. Creación de SEQUEL (más tarde SQL). | Donald Chamberlin, Raymond Boyce (IBM) | Se demuestra la viabilidad del modelo relacional. El concepto de "planes de acceso" pre-compilados es un precursor. |
| **1983** | Oracle lanza la v3, que incluye PL/SQL (Procedural Language/SQL). | Larry Ellison (Oracle) | Oracle se establece como un jugador dominante en el mercado de bases de datos comerciales. |
| **1987** | Sybase lanza Sybase SQL Server, con una implementación robusta de SPs en T-SQL. | Robert Epstein, Mark Hoffman, Tom Haggin (Sybase) | La arquitectura cliente-servidor está en auge. Las redes son lentas, haciendo que la optimización de SPs sea una "killer feature". |
| **1989** | Microsoft se asocia con Sybase para crear Microsoft SQL Server. | Microsoft, Sybase | Microsoft entra en el mercado de bases de datos empresariales, llevando T-SQL a una audiencia masiva. |
| **2001** | Se publica el "Manifesto for Agile Software Development". | Beck, Fowler, et al. | El cambio hacia el desarrollo iterativo y centrado en la aplicación favorece arquitecturas donde la lógica de negocio reside en el código de la aplicación, no en la BD. |
| **2002** | Martin Fowler describe el patrón "Anemic Domain Model". | Martin Fowler | Se articula la filosofía de que los objetos de dominio deben contener lógica de negocio, en contraposición a ser simples bolsas de datos manipuladas por servicios (o SPs). |
| **2010+** | Auge de NoSQL, Microservicios y DevOps. | AWS, Google, Netflix | El debate se matiza. Los SPs encuentran nuevos nichos en sistemas de alto rendimiento y como APIs de datos para microservicios, aunque su uso en aplicaciones web monolíticas disminuye. |

---

### 4. Implementación Práctica: Del Pergamino a la Terminal

Basta de teoría. Vamos a ensuciarnos las manos. Usaremos **PostgreSQL** (con su lenguaje PL/pgSQL) y **Python** (con la librería `psycopg2`).

#### Escenario: Un sistema bancario simple.
Necesitamos una función para transferir dinero entre dos cuentas de forma atómica (o todo tiene éxito, o todo falla).

**El Mal Camino (Lógica en la Aplicación):**

Imagina este código Python en tu aplicación.

```python
# MAL EJEMPLO - NO HACER ESTO EN PRODUCCIÓN
import psycopg2

def transfer_funds_in_app(conn, from_account, to_account, amount):
    """
    Transfiere fondos con la lógica en la aplicación.
    Este enfoque es PELIGROSO y propenso a errores.
    """
    cursor = conn.cursor()
    try:
        # 1. Comprobar si la cuenta de origen tiene fondos suficientes (Primer viaje a la BD)
        cursor.execute("SELECT balance FROM accounts WHERE account_id = %s", (from_account,))
        from_balance = cursor.fetchone()[0]

        if from_balance < amount:
            raise ValueError("Fondos insuficientes.")

        # 2. Restar de la cuenta de origen (Segundo viaje a la BD)
        cursor.execute("UPDATE accounts SET balance = balance - %s WHERE account_id = %s", (amount, from_account))

        # ¡¡¡PELIGRO!!! ¿Qué pasa si la aplicación se cae AHORA MISMO?
        # El dinero ha salido de una cuenta pero no ha llegado a la otra.

        # 3. Sumar a la cuenta de destino (Tercer viaje a la BD)
        cursor.execute("UPDATE accounts SET balance = balance + %s WHERE account_id = %s", (amount, to_account))

        conn.commit()
        print("Transferencia exitosa (en la app).")
    except (Exception, psycopg2.Error) as error:
        print(f"Error en la transferencia: {error}")
        conn.rollback()

```
**¿Por qué es malo?**
1.  **Múltiples Viajes de Red:** Tres consultas separadas. Lento.
2.  **Condiciones de Carrera (Race Conditions):** ¿Qué pasa si otro proceso lee el saldo justo después de nuestro primer `SELECT` pero antes de nuestro `UPDATE`? Podríamos permitir un sobregiro.
3.  **Falta de Atomicidad (parcialmente):** Aunque usamos `commit` y `rollback`, si la aplicación se bloquea entre el `UPDATE` 1 y el `UPDATE` 2, la transacción queda a medias en la base de datos hasta que se cierre la conexión, dejando los datos en un estado inconsistente.

**El Buen Camino (Usando un Stored Procedure):**

Primero, definimos el SP en nuestra base de datos PostgreSQL. Este es nuestro contrato sagrado.

```sql
-- BUEN EJEMPLO: El Stored Procedure en PostgreSQL (PL/pgSQL)
CREATE OR REPLACE FUNCTION transfer_funds(
    p_from_account INT,
    p_to_account INT,
    p_amount NUMERIC(10, 2)
) RETURNS VOID AS $$
DECLARE
    v_from_balance NUMERIC(10, 2);
BEGIN
    -- Bloqueamos las filas que vamos a modificar para evitar condiciones de carrera.
    -- SELECT ... FOR UPDATE es una herramienta de nivel senior.
    SELECT balance INTO v_from_balance FROM accounts
    WHERE account_id = p_from_account FOR UPDATE;

    -- Comprobamos si hay fondos suficientes
    IF v_from_balance < p_amount THEN
        RAISE EXCEPTION 'Fondos insuficientes en la cuenta %', p_from_account;
    END IF;

    -- Realizamos las operaciones
    UPDATE accounts
    SET balance = balance - p_amount
    WHERE account_id = p_from_account;

    UPDATE accounts
    SET balance = balance + p_amount
    WHERE account_id = p_to_account;

    -- No necesitamos COMMIT/ROLLBACK aquí. La transacción que llama al SP
    -- se encargará de ello, haciéndolo atómico por defecto.
END;
$$ LANGUAGE plpgsql;
```

Ahora, nuestro código Python se vuelve elegantemente simple y robusto.

```python
# BUEN EJEMPLO: Llamando al Stored Procedure desde Python
import psycopg2

def transfer_funds_with_sp(conn, from_account, to_account, amount):
    """
    Transfiere fondos llamando a un Stored Procedure.
    Este enfoque es seguro, rápido y robusto.
    """
    cursor = conn.cursor()
    try:
        # Un solo viaje a la base de datos.
        # La lógica compleja y transaccional está segura en la BD.
        cursor.execute("CALL transfer_funds(%s, %s, %s)", (from_account, to_account, amount))
        conn.commit()
        print("Transferencia exitosa (con SP).")
    except (Exception, psycopg2.Error) as error:
        print(f"Error en la transferencia: {error}")
        conn.rollback()

# --- Uso ---
# conn = psycopg2.connect(...)
# transfer_funds_with_sp(conn, 101, 102, 50.00)
# conn.close()
```

**La diferencia es abismal.** El código Python ya no conoce la lógica de negocio. Solo conoce el contrato: la función `transfer_funds` y sus parámetros. La operación es atómica, segura contra condiciones de carrera (gracias a `FOR UPDATE`) y mucho más rápida.

---

### 5. Nivel Senior - Conceptos Avanzados: Más Allá del `CREATE PROCEDURE`

Aquí es donde separamos a los programadores de los arquitectos.

#### Optimizaciones y Técnicas Avanzadas

*   **Plan Caching y Parameter Sniffing:** Como mencionamos, los SPs se compilan y su plan de ejecución se guarda en caché. Esto es genial... hasta que no lo es. El problema se llama *parameter sniffing*: el optimizador crea el plan basado en los parámetros de la *primera* ejecución. Si la primera llamada fue `sp_GetOrders('USA')` (millones de filas) y la siguiente es `sp_GetOrders('Liechtenstein')` (dos filas), el plan optimizado para millones de filas puede ser terriblemente ineficiente para dos.
    *   **Soluciones Senior:**
        *   **SQL Server:** Usar `WITH RECOMPILE` para forzar un nuevo plan cada vez (costoso pero a veces necesario). Usar `OPTIMIZE FOR` para indicarle al optimizador qué tipo de valor esperar.
        *   **PostgreSQL:** El planificador de PostgreSQL es generalmente más robusto y re-planifica con más frecuencia, pero el problema puede ocurrir. Analizar las consultas con `EXPLAIN ANALYZE` es clave.
*   **Conjuntos de Resultados Múltiples:** Un SP puede devolver varios `SELECT`s en una sola llamada. Esto es increíblemente útil para cargar un panel de control, por ejemplo, donde necesitas datos de usuarios, pedidos y productos de una sola vez. Reduce la latencia de red a su mínima expresión.
*   **Parámetros de Salida (OUTPUT):** En lugar de solo devolver un conjunto de resultados, un SP puede modificar variables pasadas como parámetros `OUTPUT`. Esto es útil para devolver valores individuales como un nuevo ID generado o un código de estado.
*   **Manejo de Transacciones Anidadas:** Comprender cómo `BEGIN TRAN`, `COMMIT`, `ROLLBACK` y `SAVEPOINT` interactúan dentro de los SPs es crucial. Un error aquí puede dejar transacciones abiertas que bloquean tablas enteras.

> "La ley de las abstracciones con fugas significa que, si bien las abstracciones intentan ocultar los detalles, a veces fallan y los detalles subyacentes se filtran, obligando al programador a comprenderlos." — **Joel Spolsky**, *The Law of Leaky Abstractions* (2002)
>
> Un SP es una abstracción. Entender el plan de ejecución y el parameter sniffing es entender sus "fugas".

#### Trade-offs: La Balanza del Arquitecto

No existe la magia. Usar SPs implica tomar decisiones conscientes.

| Ventaja (Cuándo USAR) | Desventaja (Cuándo NO USAR) |
| :--- | :--- |
| **Rendimiento Crítico:** Operaciones complejas sobre grandes volúmenes de datos (ETLs, reportes). | **Lógica de Negocio Simple:** Un CRUD básico. Un ORM es más rápido de desarrollar y más fácil de mantener. |
| **Seguridad Estricta:** Cuando las aplicaciones no deben tener acceso directo a las tablas. El SP es la API. | **Ecosistema de Múltiples BDs:** Si tu aplicación debe soportar PostgreSQL, SQL Server y Oracle, la lógica en la aplicación es más portable. |
| **Lógica de Datos Centralizada:** Cuando múltiples aplicaciones consumen la misma lógica (ej. `sp_ProcessEndOfDay`). | **Desarrollo Rápido y Prototipado:** El ciclo de desarrollo (escribir, probar, desplegar) de un SP es más lento que el de la lógica de aplicación. |
| **Atomicidad Compleja:** Transacciones que abarcan múltiples tablas y requieren una lógica condicional robusta. | **Vendor Lock-in:** El T-SQL de Microsoft no es el PL/SQL de Oracle. Te estás casando con un proveedor. |

#### Anti-Patrones: Los Caminos hacia el Desastre

*   **El SP "Dios":** Un procedimiento de 5000 líneas que hace de todo. Es imposible de mantener, probar y depurar. Un SP, como una función, debe hacer una cosa y hacerla bien.
*   **Lógica de Presentación en la BD:** Un SP que devuelve HTML o JSON formateado. Esto es una violación atroz de la separación de conceptos. La base de datos maneja datos; la aplicación maneja la presentación.
*   **SQL Dinámico Inseguro:** Construir cadenas de SQL dentro de un SP y ejecutarlas con `EXEC` o `EXECUTE IMMEDIATE` sin una parametrización adecuada. Esta es una invitación abierta a la inyección de SQL. Siempre usa procedimientos como `sp_executesql` (SQL Server) o el formato `USING` (PostgreSQL) para ejecutar SQL dinámico de forma segura.
*   **Ignorar el Control de Código Fuente:** El código de tus SPs es tan crítico como el de tu aplicación. Debe estar en un sistema de control de versiones (Git) y formar parte de tu proceso de CI/CD. Herramientas como Flyway o Liquibase son esenciales aquí.

---

### 6. Referencias y Citaciones Académicas: Sobre Hombros de Gigantes

Un verdadero senior conoce la historia y la teoría que sustenta su práctica.

1.  > "The relational model is based on the mathematical concept of a relation, which is a subset of the Cartesian product of a list of domains." — **E. F. Codd**, *A Relational Model of Data for Large Shared Data Banks* (1970). [Enlace](https://www.seas.upenn.edu/~zives/03f/cis550/codd.pdf)
    *   *El documento fundacional que lo empezó todo. Entender esto es entender el "porqué" de SQL.*

2.  > "A transaction is a collection of operations that forms a single logical unit of work. The properties of transactions are often summarized by the acronym ACID: atomicity, consistency, isolation, and durability." — **Jim Gray**, *The Transaction Concept: Virtues and Limitations* (1981).
    *   *Jim Gray, ganador del Premio Turing, formalizó el concepto de transacción. Los SPs son una herramienta principal para implementar transacciones ACID complejas.*

3.  > "PL/SQL is a procedural language extension to SQL. It allows developers to mix SQL statements with procedural constructs such as IF-THEN-ELSE, LOOP, and FOR." — **Oracle Corporation**, *Oracle Database PL/SQL Language Reference* (Documentación Oficial). [Enlace](https://docs.oracle.com/en/database/oracle/oracle-database/21/lnpls/index.html)
    *   *La documentación oficial es una fuente primaria indispensable.*

4.  > "An AnemicDomainModel is one where the domain objects have no business logic. They are just bags of getters and setters. The logic is all in a separate layer of 'manager' or 'service' objects." — **Martin Fowler**, *AnemicDomainModel Bliki Post* (2003). [Enlace](https://www.martinfowler.com/bliki/AnemicDomainModel.html)
    *   *La crítica más elocuente a la centralización excesiva de la lógica, que a menudo se manifiesta en el abuso de SPs.*

5.  > "The key idea of Sybase was to put a lot of the logic that had been in the application, or in the terminal, into the database server itself. This was revolutionary at the time." — **Entrevista con Robert Epstein**, *Computer History Museum*
    *   *Contexto histórico directo de uno de los creadores.*

6.  > "Parameter sniffing is not always a good thing. The query plan that is generated for the first execution of a stored procedure might not be optimal for subsequent executions with different parameter values." — **Microsoft Corporation**, *SQL Server Query Processing Architecture Guide* (Documentación Oficial). [Enlace](https://docs.microsoft.com/en-us/sql/relational-databases/query-processing-architecture-guide)
    *   *Una inmersión profunda en las complejidades del rendimiento que todo desarrollador senior de SQL debe conocer.*

7.  > "We recommend that you do not use stored procedures to create user interfaces. A stored procedure should be used to encapsulate a business process or a data-centric operation." — **Joe Celko**, *Joe Celko's SQL for Smarties: Advanced SQL Programming* (2014).
    *   *Joe Celko es una autoridad en SQL, y sus libros están llenos de sabiduría práctica y advertencias contra los malos hábitos.*

8.  > "The Cathedral and the Bazaar represent two different styles of software development. The cathedral model, in which source code is available with each software release, but code developed between releases is restricted to an exclusive group of software developers. The bazaar model, in which the code is developed over the Internet in view of the public." — **Eric S. Raymond**, *The Cathedral and the Bazaar* (1999).
    *   *Aunque trata sobre el desarrollo de código abierto, esta analogía es perfecta para el debate de SPs vs. lógica de aplicación. Los SPs son la "Catedral": centralizados, controlados, construidos por un grupo selecto (DBAs, ingenieros de datos). La lógica de aplicación es el "Bazar": descentralizada, visible para todos los desarrolladores, más caótica pero potencialmente más innovadora.*

***

### Conclusión: El Martillo del Maestro

Al final del día, un Stored Procedure no es ni bueno ni malo. Es una herramienta. Un martillo puede construir una casa o destrozar un pulgar. Un programador intermedio sabe *cómo* usar el martillo. Un programador senior sabe *cuándo* usarlo, *por qué* usarlo, y cuándo es mejor optar por un destornillador.

Has viajado desde su concepción en redes lentas hasta su lugar en la arquitectura moderna. Has visto su poder para garantizar la atomicidad y su riesgo de crear un monolito en la base de datos. Ahora, no solo puedes escribir un Stored Procedure. Puedes defenderlo, argumentar en su contra, diseñarlo para que sea mantenible y, lo más importante, tomar la decisión correcta para el sistema que estás construyendo. Has pasado de ser un simple cocinero a ser el chef que diseña la receta. Y ese, mi amigo, es el verdadero significado de la seniority.
