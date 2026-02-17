Ahora que entendemos la teoría, ¿cómo se ve en la práctica? Imagina que estás construyendo un sistema bancario donde un error podría costar millones. ¿Confiarías la lógica de una transferencia a tu aplicación o la encerrarías en la bóveda segura de la base de datos?

# Stored Procedures

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