Entender la teoría es una cosa, pero ¿cómo se traduce en código que realmente funciona? Pasaremos de los papers académicos a la terminal, modelando nuestros datos no por lo que son, sino por las preguntas que necesitamos responder. Este es el cambio de mentalidad clave para dominar Cassandra.

# Cassandra

---

### 3. Evolución Histórica Detallada

La historia de Cassandra es la historia de la Web 2.0 y la explosión de los datos.

*   **~2005-2007 (Contexto):** El término "Big Data" está ganando tracción. Google publica sus papers sobre GFS, MapReduce y Bigtable. Amazon publica su paper sobre Dynamo. El mundo se da cuenta de que los sistemas RDBMS tradicionales no son la respuesta para la escala de internet. La comunidad de código abierto está en auge con proyectos como Hadoop.
*   **2007 (Concepción):** En Facebook, **Avinash Lakshman** y **Prashant Malik** comienzan a trabajar en Cassandra. Lakshman, habiendo trabajado en Dynamo, aporta el ADN de la disponibilidad y la descentralización. Malik aporta la visión de la aplicación para resolver el problema del Inbox Search.
*   **2008 (Nacimiento Público):** Facebook libera Cassandra. Es un momento decisivo. Mientras que Dynamo y Bigtable eran conceptos descritos en papers académicos, Cassandra era un sistema funcional y de código abierto que cualquiera podía usar.
*   **2009-2010 (Adopción y Madurez):** Empresas como Digg, Twitter y Rackspace comienzan a adoptarlo. Su entrada y graduación en la Fundación Apache le otorgan credibilidad y una comunidad vibrante. La gente empieza a ver que no es solo una "cosa de Facebook".
*   **2012 (El Salto Cuántico - Vnodes):** Antes de la versión 1.2, añadir un nuevo nodo a un clúster de Cassandra era una operación de alto riesgo que requería un cálculo manual y un rebalanceo masivo. La introducción de los **nodos virtuales (vnodes)** fue un cambio de juego. Cada nodo físico ahora posee muchos rangos pequeños y no contiguos en el anillo, lo que hace que añadir o quitar nodos sea una operación mucho más suave y automatizada. Este fue el momento en que Cassandra pasó de ser una herramienta para expertos en sistemas distribuidos a ser manejable por equipos de operaciones más generalistas.

> "Los sistemas distribuidos son un campo donde la experiencia se gana principalmente a través del fracaso." — **Jeff Hodges**, *Ingeniero en Twitter* (parafraseado de varias charlas y posts)

Esta cita encapsula el espíritu de la primera era de Cassandra. Los primeros adoptantes fueron pioneros que aprendieron lecciones duras, allanando el camino para las mejores prácticas que conocemos hoy.

---

### 4. Implementación Práctica: Manos a la Obra con Python

La teoría es elegante, pero el código es el que paga las facturas. Usemos el driver oficial de Python (`cassandra-driver`) para interactuar con un clúster de Cassandra.

#### Configuración Inicial

```bash
pip install cassandra-driver
```

#### Conexión y Creación del Esquema

El primer paso es siempre definir tu modelo de datos. En Cassandra, esto es **diseño guiado por consultas (query-driven design)**. No piensas en "qué datos tengo", sino en "¿qué preguntas necesito responder?".

```python
# 1_connect_and_setup.py
from cassandra.cluster import Cluster

# Asume que Cassandra está corriendo en localhost. 
# En producción, aquí irían las IPs de tus nodos.
cluster = Cluster(['127.0.0.1'])
session = cluster.connect()

# Crear un "Keyspace" es similar a crear una base de datos en SQL.
# SimpleStrategy es para clústeres de un solo centro de datos.
# replication_factor=1 significa que no hay réplicas (solo para desarrollo).
session.execute("""
    CREATE KEYSPACE IF NOT EXISTS my_app
    WITH replication = { 'class': 'SimpleStrategy', 'replication_factor': '1' }
""")

# Usar nuestro keyspace
session.set_keyspace('my_app')

# Crear una tabla para almacenar datos de videos por usuario.
# ¡Este es el corazón del modelado de datos en Cassandra!
session.execute("""
    CREATE TABLE IF NOT EXISTS videos_by_user (
        user_id uuid,
        video_id timeuuid,
        title text,
        upload_date timestamp,
        tags set<text>,
        PRIMARY KEY (user_id, upload_date)
    ) WITH CLUSTERING ORDER BY (upload_date DESC);
""")

print("Keyspace y tabla creados exitosamente.")
cluster.shutdown()
```

**Análisis del `PRIMARY KEY` (Nivel Senior):**

*   `PRIMARY KEY (user_id, upload_date)`: Esto es crucial.
    *   **Clave de Partición (`user_id`):** Es la primera parte. Determina en qué nodo del clúster se almacenarán los datos. Todas las filas con el mismo `user_id` vivirán juntas en el mismo nodo (y sus réplicas). Esto hace que las búsquedas por `user_id` sean extremadamente rápidas.
    *   **Clave de Clustering (`upload_date`):** Son las columnas restantes. Determinan el orden de las filas *dentro* de una partición. `WITH CLUSTERING ORDER BY (upload_date DESC)` nos da los videos más recientes de un usuario primero, ¡gratis!

#### Patrones de Uso: El Bueno, el Malo y el Feo

**El Bueno: Escritura y Lectura Eficiente (Query-First Design)**

Nuestro modelo está diseñado para la consulta: "Obtener los últimos videos subidos por un usuario específico".

```python
# 2_good_pattern.py
import uuid
from datetime import datetime
from cassandra.cluster import Cluster
from cassandra.util import uuid_from_time

cluster = Cluster(['127.0.0.1'])
session = cluster.connect('my_app')

user_id = uuid.uuid4()
now = datetime.utcnow()

# Usar sentencias preparadas es una mejor práctica para el rendimiento
# y la seguridad.
insert_statement = session.prepare("""
    INSERT INTO videos_by_user (user_id, video_id, title, upload_date, tags)
    VALUES (?, ?, ?, ?, ?)
""")

# Insertar algunos videos para nuestro usuario
session.execute(insert_statement, [user_id, uuid_from_time(now), "Mi viaje a la playa", now, {"viaje", "verano", "playa"}])
# ... insertar más videos ...

print(f"Videos insertados para el usuario {user_id}")

# La consulta que diseñamos
query_statement = session.prepare("SELECT title, upload_date FROM videos_by_user WHERE user_id = ?")

rows = session.execute(query_statement, [user_id])

print(f"\nVideos para el usuario {user_id}:")
for row in rows:
    print(f"- {row.title} (Subido el {row.upload_date})")

cluster.shutdown()
```

Esta consulta es rapidísima porque va directamente a un nodo, y dentro de ese nodo, los datos ya están ordenados en disco.

**El Malo: Intentar ser Relacional (Anti-Patrón)**

¿Qué pasa si queremos buscar videos por una etiqueta (`tag`)? Nuestra tabla `videos_by_user` es inútil para eso. Un principiante podría intentar esto:

```python
# Esto es un ANTI-PATRÓN. ¡No lo hagas en producción!
rows = session.execute("SELECT title FROM videos_by_user WHERE tags CONTAINS 'verano' ALLOW FILTERING")
```

`ALLOW FILTERING` es una señal de que estás haciendo algo mal. Le dice a Cassandra: "Oye, sé que no tienes un índice para esto. Por favor, recorre **todos los datos de todo el clúster**, carga cada fila en memoria y comprueba si el conjunto de etiquetas contiene 'verano'". Esto es el equivalente a un `full table scan` en SQL, pero a través de un clúster distribuido. Es una receta para el desastre.

**El Bueno (de nuevo): La Solución de Cassandra - Denormalización**

La forma correcta de resolver esto es crear **otra tabla**, optimizada para esa consulta específica.

```python
# 3_denormalization_solution.py

# ... (conexión al cluster) ...
session.execute("""
    CREATE TABLE IF NOT EXISTS videos_by_tag (
        tag text,
        upload_date timestamp,
        video_id timeuuid,
        title text,
        user_id uuid,
        PRIMARY KEY (tag, upload_date)
    ) WITH CLUSTERING ORDER BY (upload_date DESC);
""")

# Ahora, cada vez que subes un video, lo escribes en AMBAS tablas.
# Sí, duplicas los datos. ¡El espacio en disco es barato, el tiempo de consulta no!

# ... (lógica de inserción para ambas tablas) ...

# Y ahora, tu consulta es súper eficiente:
query_by_tag = session.prepare("SELECT title, user_id FROM videos_by_tag WHERE tag = ?")
rows = session.execute(query_by_tag, ['verano'])

print("\nVideos con la etiqueta 'verano':")
for row in rows:
    print(f"- {row.title} (Por usuario {row.user_id})")

# ... (shutdown) ...
```
Este es el cambio de mentalidad más grande para alguien que viene de SQL. En Cassandra, **la denormalización no es un vicio, es una virtud**.

#### Caso de Estudio: Netflix

Netflix es uno de los mayores usuarios de Cassandra del mundo. Lo utilizan para almacenar el historial de visualización de cada usuario.

*   **El Problema:** Cientos de millones de usuarios, cada uno viendo múltiples títulos al día. Esto genera billones de registros. Necesitan una disponibilidad del 100% (¡nadie quiere que Netflix se caiga!) y una latencia de escritura y lectura muy baja.
*   **La Solución Cassandra:**
    *   **Modelo de Datos:** Probablemente una tabla como `viewing_history` con `PRIMARY KEY (user_id, event_time)`. Esto permite obtener el historial de un usuario de forma eficiente, ordenado cronológicamente.
    *   **Escalabilidad:** A medida que Netflix crece, simplemente añaden más nodos a sus clústeres de Cassandra.
    *   **Disponibilidad:** Replican los datos en múltiples regiones geográficas (usando `NetworkTopologyStrategy`). Si un centro de datos en la costa este de EE. UU. se cae, el tráfico se redirige sin problemas a Europa o la costa oeste.

> "La consistencia eventual es uno de los secretos peor guardados en la disponibilidad de servicios a gran escala." — **Werner Vogels**, *CTO de Amazon*, "Eventually Consistent"* (2008)

Netflix vive y respira este principio, y Cassandra es la herramienta que se lo permite.