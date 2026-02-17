¿Cómo pasamos de la elegante teoría de ACID a los sistemas que usamos hoy? La historia está llena de gigantes y revoluciones que dieron forma a la tecnología que damos por sentada.

Y lo más importante, ¿cómo se ve esto en código real? Vamos a escribirlo juntos y a ver la delgada línea que separa un desastre de datos de un sistema fiable.

# Transactions

## 3. Evolución Histórica Detallada: Una Saga de Gigantes

La historia de las transacciones es la historia de cómo la computación pasó de ser una herramienta de cálculo a ser el sistema nervioso central de la civilización moderna.

### Timeline del Concepto

| Década | Hito Clave | Figuras/Proyectos Clave | Contexto Computacional |
| :--- | :--- | :--- | :--- |
| **1960s** | Sistemas de archivos ad-hoc. Problemas de concurrencia se manejan manualmente. | - | Mainframes de segunda generación. Procesamiento por lotes. |
| **1970s** | **Nacimiento del concepto.** System R define la arquitectura transaccional. Se formaliza ACID. | **Jim Gray, Donald Chamberlin, Raymond Boyce (IBM System R)**, Michael Stonebraker (Ingres) | Auge de los mainframes. Necesidad de sistemas interactivos multiusuario (OLTP). |
| **1980s** | **Comercialización y Estandarización.** Las bases de datos relacionales (Oracle, DB2) hacen de ACID una característica estándar. | Larry Ellison (Oracle) | La era de los miniordenadores y el inicio de la PC. SQL se convierte en el estándar. |
| **1990s** | **La Conquista de la Distribución.** Protocolo de **Two-Phase Commit (2PC)** para transacciones distribuidas. | The Open Group (Estándar XA) | Arquitecturas cliente-servidor. El auge de las redes empresariales. |
| **2000s** | **La Rebelión de la Web.** El Teorema CAP (Brewer, 2000) pone en duda la viabilidad de ACID a escala masiva. Nace **BASE** y el movimiento NoSQL. | Eric Brewer, Werner Vogels (Amazon Dynamo) | Explosión de la Web 2.0. Google, Amazon, Facebook operan a una escala sin precedentes. |
| **2010s** | **La Síntesis.** **NewSQL** busca combinar la escalabilidad de NoSQL con las garantías de ACID. Patrones como **Sagas** para microservicios. | Google (Spanner), Cockroach Labs, Pat Helland | Cloud computing, arquitecturas de microservicios. La consistencia vuelve a ser importante. |
| **2020s** | **El Futuro.** Transacciones en sistemas descentralizados (Blockchain), HTAP (Hybrid Transactional/Analytical Processing). | - | Edge computing, IA/ML, Web3. La línea entre lo analítico y lo transaccional se difumina. |

### Figuras Clave: El Panteón Transaccional

*   **Jim Gray (1944-2007?):** El padre de las transacciones. Ganador del Premio Turing en 1998 por sus contribuciones. Su desaparición en el mar en 2007 es una de las grandes tragedias de la computación. Su trabajo es la base de todo lo que discutimos.
*   **Pat Helland:** Un arquitecto de sistemas distribuidos (trabajó en Amazon, Microsoft) que ha escrito ensayos influyentes sobre las realidades de los sistemas distribuidos, argumentando que la vida más allá de las transacciones distribuidas es inevitable y que debemos abrazar la eventualidad.

> "Accountants don't use erasers. Instead, they add new entries to the ledger to correct mistakes or capture changes. This is the core insight behind many scalable and robust distributed systems." — **Pat Helland**, *Life Beyond Distributed Transactions: An Apostate's Opinion* (2007)

Esta cita es la semilla filosófica detrás de patrones como Sagas y el diseño de sistemas de "solo apéndice" (append-only).

## 4. Implementación Práctica: Del Papiro a Python

La teoría es elegante, pero el código es donde la goma se encuentra con el camino. Usaremos Python y `sqlite3` (que viene incorporado) para ilustrar estos conceptos de forma tangible.

### Escenario: Una Simple Transferencia Bancaria

Imaginemos dos cuentas, la de Alice con 100€ y la de Bob con 50€. Queremos transferir 20€ de Alice a Bob.

**La forma INCORRECTA (sin transacción):**

```python
import sqlite3
import os

DB_FILE = "bank_bad.db"

def setup_database():
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE accounts (id TEXT PRIMARY KEY, balance INTEGER)")
    cursor.execute("INSERT INTO accounts (id, balance) VALUES ('Alice', 100)")
    cursor.execute("INSERT INTO accounts (id, balance) VALUES ('Bob', 50)")
    conn.commit()
    conn.close()

def transfer_money_bad(from_id, to_id, amount):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    print("Iniciando transferencia...")
    
    # 1. Leer el saldo de Alice
    cursor.execute("SELECT balance FROM accounts WHERE id = ?", (from_id,))
    from_balance = cursor.fetchone()[0]
    print(f"Saldo de {from_id}: {from_balance}")
    
    # 2. Debitar de Alice
    if from_balance >= amount:
        new_from_balance = from_balance - amount
        cursor.execute("UPDATE accounts SET balance = ? WHERE id = ?", (new_from_balance, from_id))
        conn.commit() # ¡Punto de fallo!
        print(f"Debitado {amount} de {from_id}. Nuevo saldo: {new_from_balance}")
        
        # --- IMAGINA UN CRASH DEL SISTEMA AQUÍ ---
        # raise Exception("¡Oh no! El sistema se ha caído.")
        # ----------------------------------------
        
        # 3. Acreditar a Bob
        cursor.execute("SELECT balance FROM accounts WHERE id = ?", (to_id,))
        to_balance = cursor.fetchone()[0]
        new_to_balance = to_balance + amount
        cursor.execute("UPDATE accounts SET balance = ? WHERE id = ?", (new_to_balance, to_id))
        conn.commit()
        print(f"Acreditado {amount} a {to_id}. Nuevo saldo: {new_to_balance}")
        
    else:
        print("Fondos insuficientes.")
        
    conn.close()

def check_balances():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM accounts")
    print("\n--- Saldos actuales ---")
    total = 0
    for row in cursor.fetchall():
        print(f"{row[0]}: {row[1]}")
        total += row[1]
    print(f"Dinero total en el sistema: {total}") # Debería ser siempre 150
    print("-----------------------\n")

# --- Ejecución ---
setup_database()
check_balances()
# Descomenta la línea de la excepción para ver el desastre
transfer_money_bad('Alice', 'Bob', 20) 
check_balances()
```

Si ejecutas este código y la excepción se lanza, verás que el dinero ha desaparecido de Alice, pero nunca ha llegado a Bob. ¡Hemos creado dinero de la nada (o más bien, lo hemos destruido)! El total del sistema ya no es 150. **Hemos violado la Atomicidad y la Consistencia.**

**La forma CORRECTA (con transacción):**

El patrón de uso moderno en Python es el gestor de contexto (`with`), que maneja el `commit` y `rollback` automáticamente.

```python
import sqlite3
import os

DB_FILE = "bank_good.db"

# setup_database y check_balances son iguales, solo cambia el nombre del archivo

def setup_database_good():
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE accounts (id TEXT PRIMARY KEY, balance INTEGER)")
    cursor.execute("INSERT INTO accounts (id, balance) VALUES ('Alice', 100)")
    cursor.execute("INSERT INTO accounts (id, balance) VALUES ('Bob', 50)")
    conn.commit()
    conn.close()

def transfer_money_good(from_id, to_id, amount):
    # La conexión a la base de datos se maneja como un gestor de contexto.
    # sqlite3 por defecto inicia una transacción en la primera sentencia de modificación de datos.
    # El bloque 'with' se encargará de hacer conn.commit() si todo va bien,
    # o conn.rollback() si se lanza una excepción.
    try:
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            print("Iniciando transferencia atómica...")
            
            # 1. Leer y debitar de Alice (en una sola operación si es posible)
            cursor.execute("SELECT balance FROM accounts WHERE id = ?", (from_id,))
            from_balance = cursor.fetchone()[0]
            
            if from_balance < amount:
                raise ValueError("Fondos insuficientes.")

            cursor.execute("UPDATE accounts SET balance = balance - ? WHERE id = ?", (amount, from_id))
            print(f"Debitado {amount} de {from_id}.")

            # --- IMAGINA UN CRASH DEL SISTEMA AQUÍ ---
            # raise Exception("¡Oh no! El sistema se ha caído.")
            # ----------------------------------------

            # 2. Acreditar a Bob
            cursor.execute("UPDATE accounts SET balance = balance + ? WHERE id = ?", (amount, to_id))
            print(f"Acreditado {amount} a {to_id}.")
            
        print("Transferencia completada y comprometida.")
    except Exception as e:
        print(f"Error en la transferencia: {e}. La transacción ha sido revertida (rollback).")

# --- Ejecución ---
setup_database_good()
check_balances() # Alice: 100, Bob: 50, Total: 150
transfer_money_good('Alice', 'Bob', 20)
check_balances() # Alice: 80, Bob: 70, Total: 150 (CORRECTO)

print("\n--- Probando una transferencia fallida ---")
setup_database_good()
check_balances() # Alice: 100, Bob: 50, Total: 150
# Simulamos el fallo dentro de la función
transfer_money_good('Alice', 'Bob', 20) # (Aquí dentro se lanzaría la excepción)
check_balances() # Alice: 100, Bob: 50, Total: 150 (¡CORRECTO! No ha cambiado nada)
```

En la versión "buena", si la excepción se produce, el bloque `with` detecta el error y automáticamente ejecuta un `ROLLBACK`. El estado de la base de datos vuelve a ser el de antes de que empezara la transacción. La atomicidad se preserva, y con ella, la consistencia del sistema.