La teoría sobre Waterfall y Agile es interesante, pero ¿cómo se traduce realmente en el día a día de un desarrollador? Vamos a tomar un proyecto simple, un acortador de URLs, y a construirlo de dos maneras radicalmente distintas. Veremos cómo la elección del SDLC impacta directamente en el código, el diseño y la toma de decisiones.

# SDLC

### 4. Implementación Práctica: Del Diagrama al Código

Teoría es una cosa, pero ¿cómo se ve esto en la práctica? Vamos a construir un proyecto simple, un **acortador de URLs**, y veremos cómo lo abordaríamos con dos SDLCs radicalmente diferentes.

**Proyecto: "PyShorty" - Un Acortador de URLs en Python**

Funcionalidad básica:
1.  Recibir una URL larga.
2.  Generar un código corto y único.
3.  Almacenar la correspondencia.
4.  Dado un código corto, redirigir a la URL larga original.

#### Enfoque 1: El Camino del Waterfall (Cascada)

Este enfoque es rígido, secuencial y exhaustivo en cada fase.

**Fase 1: Análisis de Requisitos (Semanas 1-2)**
*   Se crea un documento de 50 páginas (Software Requirements Specification - SRS).
*   Define *todo*: formato de la URL, longitud exacta del código corto (6 caracteres alfanuméricos), tipo de base de datos (PostgreSQL), endpoints de la API (con esquemas JSON exactos), diseño de la UI (wireframes detallados).
*   **Resultado:** Un documento firmado y "congelado". No se permiten cambios.

**Fase 2: Diseño del Sistema (Semanas 3-4)**
*   Se crea un documento de diseño de arquitectura.
*   Diagramas UML, esquema de la base de datos completo, diseño de clases.
*   **Ejemplo de Diseño (Pseudo-código/Diagrama):**
    ```
    +----------------+       +-------------------+
    |   API Layer    |------>|  ShorteningLogic  |
    | (Flask/FastAPI)|       | (Genera/Valida)   |
    +----------------+       +-------------------+
                                     |
                                     v
                           +-------------------+
                           |  Persistence Layer|
                           | (SQLAlchemy/PG)   |
                           +-------------------+
    ```

**Fase 3: Implementación (Semanas 5-8)**
*   Ahora, y solo ahora, se escribe el código. El equipo de desarrollo recibe las especificaciones y no debe desviarse.

```python
# pyshorty/storage.py - Escrito según el diseño de la Fase 2
import string
import random
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = "postgresql://user:password@localhost/pyshorty"
Base = declarative_base()

class URLMap(Base):
    __tablename__ = 'url_maps'
    id = Column(Integer, primary_key=True)
    short_code = Column(String(6), unique=True, index=True)
    long_url = Column(String, index=True)

# ... (código para inicializar la DB, crear sesión, etc.)

# pyshorty/logic.py
def generate_short_code(length: int = 6) -> str:
    """Genera un código corto alfanumérico único."""
    # En Waterfall, esta lógica fue definida en el documento de diseño.
    chars = string.ascii_letters + string.digits
    # NOTA: En un sistema real, necesitaríamos verificar la unicidad en la DB.
    # Esto se habría especificado en el SRS.
    return ''.join(random.choice(chars) for _ in range(length))

# ... resto del código ...
```

**Fase 4: Pruebas (Semanas 9-10)**
*   El equipo de QA recibe la aplicación "terminada" y la prueba contra el documento de requisitos original.
*   Se reportan bugs. El equipo de desarrollo los arregla. Este ciclo puede ser largo y doloroso.

**Fase 5: Despliegue y Mantenimiento (Semana 11 en adelante)**
*   Finalmente, se despliega. El mantenimiento se basa en arreglar bugs o iniciar un *nuevo* proyecto Waterfall para la versión 2.0.

**Antes vs. Después (Waterfall)**
*   **Antes:** Caos. Código escrito sin un plan claro.
*   **Después:** Un proceso estructurado. Predecible, pero lento y terriblemente inflexible. ¿Qué pasa si a mitad de camino el cliente decide que quiere códigos de 7 caracteres? Desastre.

---

#### Enfoque 2: La Danza del Agile (Scrum)

Este enfoque es iterativo, incremental y se centra en entregar valor rápidamente.

**Planificación del Producto (Backlog)**
*   Creamos "Historias de Usuario".
    *   "Como usuario, quiero introducir una URL larga y obtener una corta para poder compartirla fácilmente." (Prioridad Alta)
    *   "Como usuario, quiero usar un código corto y ser redirigido a la URL original." (Prioridad Alta)
    *   "Como usuario, quiero ver estadísticas de clics de mis URLs." (Prioridad Media)
    *   "Como administrador, quiero un panel para gestionar todas las URLs." (Prioridad Baja)

**Sprint 1 (2 semanas) - Objetivo: Crear un MVP funcional**
*   **Planificación del Sprint:** Elegimos las dos primeras historias.
*   **Desarrollo:** El equipo trabaja en conjunto. El diseño emerge a medida que se necesita.
    *   "Ok, para el MVP, usemos SQLite. Es más rápido de configurar. Podemos migrar a Postgres después si es necesario."
    *   "Empecemos con un endpoint de API simple. La UI puede esperar al siguiente sprint."

```python
# sprint_1/main.py - Código simple y funcional para el MVP
from flask import Flask, request, redirect, jsonify
import string
import random
import sqlite3

app = Flask(__name__)
# Usamos SQLite para empezar rápido. ¡Decisión ágil!
DB_FILE = "pyshorty_sprint1.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS url_maps (
        short_code TEXT PRIMARY KEY,
        long_url TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()

# ... (funciones de ayuda para la DB) ...

def generate_short_code(length: int = 6) -> str:
    # La misma lógica, pero decidida y escrita en el mismo sprint
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

@app.route('/shorten', methods=['POST'])
def shorten_url():
    # Implementación de la primera historia de usuario
    # ...
    return jsonify({"short_code": short_code})

@app.route('/<short_code>')
def redirect_to_url(short_code):
    # Implementación de la segunda historia de usuario
    # ...
    return redirect(long_url)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
```
*   **Revisión del Sprint:** Al final de las 2 semanas, el equipo muestra un producto funcional (aunque mínimo) a los stakeholders. Reciben feedback inmediato. "¡Genial! Pero, ¿podríamos hacer que la API devuelva la URL completa con el dominio?"
*   **Retrospectiva:** El equipo discute qué fue bien y qué mal. "La configuración de la base de datos nos tomó más tiempo de lo esperado".

**Sprint 2 (2 semanas) - Objetivo: Añadir UI y mejorar la API**
*   Se toma el feedback de la revisión y se planifica el siguiente incremento de funcionalidad.

**Mal vs. Bien (Agile)**
*   **Mal (Cargo Cult Agile):** Hacer reuniones diarias sin comunicarse. Tener sprints pero sin entregar software funcional al final. Es solo Waterfall en pequeños trozos.
*   **Bien:** Un equipo auto-organizado que entrega valor tangible en cada ciclo, se adapta al cambio y mejora continuamente su proceso.