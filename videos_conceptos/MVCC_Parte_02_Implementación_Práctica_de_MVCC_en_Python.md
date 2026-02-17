Hemos visto cómo MVCC evolucionó desde una tesis académica hasta el estándar de la industria. Pero, ¿cómo funciona realmente bajo el capó? Vamos a desmitificarlo construyendo nuestra propia versión simplificada en Python para ver las reglas de visibilidad en acción.

# MVCC

---

### 3. Evolución Histórica Detallada

| Fecha       | Evento Clave                                                              | Figuras Clave          | Contexto Computacional                                                                   |
|-------------|---------------------------------------------------------------------------|------------------------|------------------------------------------------------------------------------------------|
| **1973**    | Jim Gray publica su influyente trabajo sobre granularidad de bloqueos.    | Jim Gray               | El bloqueo es el paradigma dominante. Se debate sobre bloquear filas, páginas o tablas. |
| **1978**    | Tesis doctoral de David P. Reed en el MIT.                                | David P. Reed          | La investigación en sistemas distribuidos explora alternativas a la coordinación central. |
| **1981**    | Philip Bernstein y Nathan Goodman publican "Concurrency Control in Distributed Database Systems". | Bernstein, Goodman     | Se formalizan muchos algoritmos de concurrencia, incluyendo variantes de versionado.      |
| **1984**    | Se lanza **InterBase 1.0**, una de las primeras BBDD comerciales con MVCC. | Jim Starkey            | El mercado de las BBDD está en auge. Oracle y DB2 dominan con modelos basados en bloqueo. |
| **1986**    | Oracle Database v5.1 introduce su modelo de consistencia de lectura.      | Larry Ellison          | Oracle busca una ventaja competitiva en rendimiento para sistemas OLTP.                  |
| **1995**    | El proyecto **Postgres95** (sucesor de Postgres) se basa en MVCC.          | Stonebraker, et al.    | El software de código abierto empieza a ganar tracción. Linux 1.2.0 es lanzado.       |
| **2000**    | Innobase Oy licencia su motor de almacenamiento **InnoDB** a MySQL AB.      | Heikki Tuuri           | La burbuja de las .com impulsa la necesidad de bases de datos web escalables y gratuitas.  |
| **2010s**   | Auge de las BBDD **NewSQL** (CockroachDB, TiDB, YugabyteDB).                | Varios                 | Se busca combinar la escalabilidad de NoSQL con las garantías ACID de SQL. MVCC es clave. |

**Anécdota Histórica**: Michael Stonebraker, una figura legendaria y a veces controvertida (creador de Ingres, Postgres, y ganador del Premio Turing), fue un gran defensor de MVCC. Su argumento era que el código para el control de concurrencia basado en bloqueos era notoriamente complejo y propenso a errores (deadlocks, livelocks). MVCC, aunque con sus propias complejidades (como la recolección de basura), ofrecía un modelo conceptualmente más limpio para el aislamiento.

---

### 4. Implementación Práctica: Construyendo un Mini-MVCC en Python

Para desmitificar MVCC, vamos a construir una simulación simplificada. No será una base de datos de producción, pero ilustrará los principios básicos de `xmin`, `xmax` y la visibilidad de la instantánea.

```python
import time
from threading import Lock, Thread
from typing import Dict, Any, Optional, Set, Tuple

# Un contador global y atómico para los IDs de transacción
class TransactionManager:
    def __init__(self):
        self.tx_counter = 0
        self.lock = Lock()
        self.active_transactions: Set[int] = set()
        self.committed_transactions: Set[int] = set()

    def begin(self) -> Tuple[int, Set[int]]:
        """Inicia una nueva transacción y le da una instantánea."""
        with self.lock:
            self.tx_counter += 1
            tx_id = self.tx_counter
            # La instantánea es el conjunto de transacciones activas en este momento.
            # Una transacción no puede ver los cambios de otras transacciones que
            # estaban activas cuando comenzó.
            snapshot = self.active_transactions.copy()
            self.active_transactions.add(tx_id)
            return tx_id, snapshot

    def commit(self, tx_id: int):
        """Marca una transacción como confirmada."""
        with self.lock:
            self.active_transactions.remove(tx_id)
            self.committed_transactions.add(tx_id)

    def abort(self, tx_id: int):
        """Marca una transacción como abortada."""
        with self.lock:
            self.active_transactions.remove(tx_id)

# Representa una versión de una fila
class Version:
    def __init__(self, data: Any, xmin: int, xmax: Optional[int] = None):
        self.data = data
        self.xmin = xmin
        self.xmax = xmax

    def __repr__(self):
        return f"Version(data={self.data}, xmin={self.xmin}, xmax={self.xmax})"

# Nuestro almacén de datos con MVCC
class MVCCStore:
    def __init__(self):
        # Un diccionario donde la clave es la clave del dato y el valor es una lista de versiones
        self._data: Dict[str, list[Version]] = {}
        self.lock = Lock()

    def read(self, key: str, tx_id: int, snapshot: Set[int], tx_manager: TransactionManager) -> Optional[Any]:
        """
        La lógica de visibilidad del núcleo de MVCC.
        Encuentra la versión correcta de una fila para una transacción dada.
        """
        with self.lock:
            if key not in self._data:
                return None

            versions = self._data[key]
            for version in reversed(versions):  # Empezamos por la más reciente
                # Regla 1: ¿Fue creada por una transacción ya confirmada?
                # (O por nuestra propia transacción)
                is_committed_creator = version.xmin in tx_manager.committed_transactions
                is_own_creation = version.xmin == tx_id
                
                if not (is_committed_creator or is_own_creation):
                    continue

                # Regla 2: ¿Es visible en nuestra instantánea?
                # Su creador no debe estar en nuestra instantánea (a menos que seamos nosotros).
                if version.xmin in snapshot and not is_own_creation:
                    continue

                # Regla 3: ¿Ha sido borrada por una transacción visible?
                if version.xmax is not None:
                    # Si la transacción que la borró está en nuestra instantánea,
                    # entonces para nosotros, el borrado ya ocurrió.
                    if version.xmax in snapshot:
                        continue
                    # Si la transacción que la borró ya está confirmada y no es la nuestra,
                    # no la vemos.
                    if version.xmax in tx_manager.committed_transactions and version.xmax != tx_id:
                        continue
                
                # Si pasa todas las reglas, esta es la versión que vemos.
                return version.data
            return None

    def write(self, key: str, value: Any, tx_id: int):
        """
        Escribir un valor. En MVCC, esto significa crear una nueva versión.
        """
        with self.lock:
            new_version = Version(data=value, xmin=tx_id)
            
            if key not in self._data:
                self._data[key] = [new_version]
            else:
                # "Borramos" la versión anterior marcando su xmax con nuestro tx_id
                # (Esto solo será visible si hacemos commit)
                latest_version = self._data[key][-1]
                if latest_version.xmax is None:
                    latest_version.xmax = tx_id
                
                self._data[key].append(new_version)

### Caso de Estudio: "Antes vs Después" y "Mal vs Bien"

#### Escenario: El Contador Concurrente

Imaginemos que tenemos un contador en la base de datos y dos procesos quieren leerlo, incrementarlo y escribirlo.

**El enfoque "Mal" (sin control de concurrencia o con bloqueo pesimista):**

1.  Proceso A lee `contador = 10`.
2.  Proceso B lee `contador = 10`.
3.  Proceso A calcula `10 + 1 = 11` y escribe `contador = 11`.
4.  Proceso B calcula `10 + 1 = 11` y escribe `contador = 11`.
    **Resultado:** ¡Una actualización perdida! El contador debería ser 12.

**El enfoque "Bien" (usando nuestro MVCCStore):**

```python
def worker(name: str, store: MVCCStore, tx_manager: TransactionManager):
    print(f"[{name}] Iniciando transacción.")
    tx_id, snapshot = tx_manager.begin()
    
    try:
        # Leer el valor actual visible para nuestra transacción
        current_value = store.read("counter", tx_id, snapshot, tx_manager) or 0
        print(f"[{name}] Leyó el contador: {current_value}. Snapshot de transacciones activas: {snapshot}")
        
        time.sleep(0.1) # Simular trabajo
        
        new_value = current_value + 1
        print(f"[{name}] Escribiendo nuevo valor: {new_value}")
        store.write("counter", new_value, tx_id)
        
        tx_manager.commit(tx_id)
        print(f"[{name}] Commit realizado.")
    except Exception as e:
        print(f"[{name}] Abortando transacción: {e}")
        tx_manager.abort(tx_id)

# --- Simulación ---
store = MVCCStore()
tx_manager = TransactionManager()

# Inicializar el contador
init_tx, init_snapshot = tx_manager.begin()
store.write("counter", 10, init_tx)
tx_manager.commit(init_tx)
print("Contador inicializado a 10.\n")

# Lanzar dos workers concurrentes
thread1 = Thread(target=worker, args=("Worker A", store, tx_manager))
thread2 = Thread(target=worker, args=("Worker B", store, tx_manager))

thread1.start()
time.sleep(0.05) # Asegurar que B empiece un poco después
thread2.start()

thread1.join()
thread2.join()

# Leer el resultado final
final_tx, final_snapshot = tx_manager.begin()
final_value = store.read("counter", final_tx, final_snapshot, tx_manager)
tx_manager.commit(final_tx)

print(f"\nValor final del contador: {final_value}")
print("Historial de versiones:", store._data["counter"])
```

**Salida Esperada:**

```
Contador inicializado a 10.

[Worker A] Iniciando transacción.
[Worker A] Leyó el contador: 10. Snapshot de transacciones activas: set()
[Worker B] Iniciando transacción.
[Worker B] Leyó el contador: 10. Snapshot de transacciones activas: {2}
[Worker A] Escribiendo nuevo valor: 11
[Worker A] Commit realizado.
[Worker B] Escribiendo nuevo valor: 11
[Worker B] Commit realizado.

Valor final del contador: 11
Historial de versiones: [Version(data=10, xmin=1, xmax=2), Version(data=11, xmin=2, xmax=3), Version(data=11, xmin=3, xmax=None)]
```
**¡Espera! ¿Por qué el resultado sigue siendo 11?**

Aquí es donde nuestro ejemplo simplificado revela una verdad de nivel senior: **MVCC con Snapshot Isolation previene lecturas sucias y lecturas no repetibles, pero NO previene las actualizaciones perdidas por sí solo**. Este fenómeno se llama **Write Skew**. Ambas transacciones leyeron el mismo estado inicial (`10`), y aunque la escritura de A invalidó la versión que B leyó, el "snapshot" de B ya estaba fijado.

Para solucionar esto, las bases de datos reales usan una capa adicional:
1.  **Detección de conflictos de escritura:** En el `COMMIT`, la base de datos comprueba si la versión que una transacción leyó para basar su escritura sigue siendo la última versión visible. Si no, la transacción que intenta hacer commit en segundo lugar falla y debe reintentarse.
2.  **Niveles de aislamiento más altos:** El nivel `SERIALIZABLE` en bases de datos como PostgreSQL usa técnicas como **Serializable Snapshot Isolation (SSI)** para detectar estos ciclos peligrosos y abortar una de las transacciones.

Nuestro código demuestra perfectamente el poder y la limitación del Snapshot Isolation básico.