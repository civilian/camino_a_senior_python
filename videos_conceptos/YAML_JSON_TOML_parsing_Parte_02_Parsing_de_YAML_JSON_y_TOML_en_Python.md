Saber la historia es importante, pero ¿cómo se traduce todo eso en código funcional y seguro? Vamos a pasar de la teoría a la práctica, viendo cómo manejar estos formatos en Python y, lo más importante, cómo evitar una de las vulnerabilidades más famosas que podría comprometer tu aplicación.

# YAML / JSON / TOML parsing

---

### 3. Evolución Histórica Detallada

| Año | Evento Clave | Formato | Figura(s) Clave | Contexto Computacional |
| :--- | :--- | :--- | :--- | :--- |
| **1958** | Se crea LISP | (Precursor) | John McCarthy | Nacen las S-expressions, la idea de "código como datos" y datos como árboles. |
| **1985** | Se popularizan los archivos INI | (Precursor) | Microsoft (Windows 1.0) | Necesidad de archivos de configuración simples y legibles por humanos en sistemas de escritorio. |
| **1998** | Se publica el estándar XML 1.0 | XML | W3C | La web está madurando; se necesita un estándar riguroso para el intercambio de datos estructurados. |
| **2001** | Se concibe YAML | YAML | Clark Evans, Ingy döt Net | Reacción a la complejidad de XML, con un enfoque extremo en la legibilidad humana. |
| **~2002** | Douglas Crockford populariza JSON | JSON | Douglas Crockford | La revolución AJAX está en marcha. Se necesita un formato de datos ligero para las aplicaciones web. |
| **2006** | Se publica el primer RFC para JSON (RFC 4627) | JSON | IETF | JSON se formaliza, consolidando su estatus como un estándar de internet. |
| **~2009** | Kubernetes y Ansible adoptan YAML | YAML | Google, Michael DeHaan | El movimiento DevOps despega. Se necesita un lenguaje legible para definir infraestructura y despliegues. |
| **2013** | Tom Preston-Werner crea TOML | TOML | Tom Preston-Werner | Reacción a la ambigüedad de YAML. Se busca un formato de configuración "obvio". |
| **2017** | Se publica el RFC 8259, el estándar actual de JSON | JSON | IETF | Refina el estándar, asegurando la interoperabilidad y aclarando detalles. |
| **2020** | PEP 621 estandariza `pyproject.toml` | TOML | Python Software Foundation | TOML se convierte en el estándar para la configuración de proyectos en el ecosistema Python. |

**Un Momento Decisivo: El "Norway Problem"**

YAML, en su búsqueda de la naturalidad, interpreta ciertos valores sin comillas. Por ejemplo, `NO` se interpreta como el booleano `false`. Esto causó problemas notorios cuando se usaban códigos de país de dos letras, como `NO` para Noruega. Un archivo de configuración que listaba países podía convertir silenciosamente a Noruega en un valor booleano, causando errores sutiles y difíciles de depurar. Este es un ejemplo clásico de cómo una decisión de diseño para la conveniencia humana puede crear ambigüedad para la máquina. TOML fue diseñado específicamente para evitar este tipo de problemas al requerir que las cadenas sean siempre citadas.

---

### 4. Implementación Práctica en Python

Vamos a ensuciarnos las manos. Python, con su filosofía de "baterías incluidas" y su rico ecosistema, tiene un soporte excelente para los tres formatos.

#### Escenario: Configuración de una Aplicación de Microservicios

Imaginemos que estamos configurando un servicio que necesita una conexión a la base de datos, una clave de API y una lista de características activadas.

#### JSON: El Rigorista

**`config.json`**
```json
{
  "database": {
    "host": "db.example.com",
    "port": 5432,
    "user": "admin"
  },
  "api_key": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
  "features": [
    "feature_a",
    "feature_b"
  ],
  "enabled": true,
  "retry_attempts": 3
}
```

**Parsing en Python (Bueno vs. Malo)**

```python
import json

# --- MAL: Abrir archivos sin un `with` statement ---
# Si ocurre un error, el archivo podría no cerrarse correctamente.
# f = open('config.json')
# config_data = json.load(f)
# f.close()

# --- BIEN: Usando un gestor de contexto ---
# Garantiza que el archivo se cierre incluso si hay errores.
try:
    with open('config.json', 'r') as f:
        config = json.load(f)  # .load() para leer desde un archivo
        print("Configuración JSON cargada:")
        print(config['database']['host'])

    # Para parsear desde una cadena (e.g., respuesta de API)
    json_string = '{"status": "ok"}'
    data = json.loads(json_string) # .loads() para leer desde una cadena (load-string)
    print(f"Estado de la API: {data['status']}")

except FileNotFoundError:
    print("Error: No se encontró config.json")
except json.JSONDecodeError as e:
    print(f"Error al decodificar JSON: {e}")

```

#### YAML: El Humanista

**`config.yaml`**
```yaml
# Configuración de la base de datos
database:
  host: db.example.com
  port: 5432
  user: admin

# Clave de la API externa
api_key: a1b2c3d4-e5f6-7890-1234-567890abcdef

# Lista de características habilitadas
features:
  - feature_a
  - feature_b

enabled: true # Opcionalmente: yes, on
retry_attempts: 3
```
*Nota la ausencia de comas, llaves y corchetes. Es mucho más limpio a la vista.*

**Parsing en Python (El Peligro Oculto)**

Necesitarás `pip install PyYAML`.

```python
import yaml

# --- MUY MAL Y PELIGROSO: Usar yaml.load() sin un Loader ---
# Esta es una de las vulnerabilidades más famosas en el ecosistema Python.
# `yaml.load()` puede ejecutar código arbitrario si el archivo YAML está maliciosamente diseñado.
# NUNCA uses esto con datos no confiables.
#
# Ejemplo malicioso en un archivo YAML:
# !!python/object/apply:os.system ["echo '¡He sido hackeado!'"]

# --- BIEN Y SEGURO: Usar yaml.safe_load() ---
# `safe_load` limita el parsing a tipos de datos simples (diccionarios, listas, strings, etc.)
# y previene la ejecución de código.
try:
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)
        print("\nConfiguración YAML cargada:")
        print(config['database']['host'])
        print(f"¿Servicio habilitado? {config['enabled']}")

except FileNotFoundError:
    print("Error: No se encontró config.yaml")
except yaml.YAMLError as e:
    print(f"Error al parsear YAML: {e}")
```

#### TOML: El Minimalista

**`config.toml`**
```toml
# Configuración principal de la aplicación
enabled = true
retry_attempts = 3
api_key = "a1b2c3d4-e5f6-7890-1234-567890abcdef"

[database]
host = "db.example.com"
port = 5432
user = "admin"

# Las listas son explícitas
features = ["feature_a", "feature_b"]
```
*La estructura de tablas `[database]` es explícita y evita la ambigüedad de la indentación de YAML.*

**Parsing en Python (El Estándar Moderno)**

A partir de Python 3.11, `tomllib` está en la biblioteca estándar para leer. Para escribir, o en versiones anteriores, necesitarás `pip install tomli`.

```python
# En Python 3.11+
import tomllib

# En Python < 3.11, usa `import tomli as tomllib` después de `pip install tomli`

try:
    with open('config.toml', 'rb') as f: # TOML se lee en modo binario
        config = tomllib.load(f)
        print("\nConfiguración TOML cargada:")
        print(config['database']['host'])
        
except FileNotFoundError:
    print("Error: No se encontró config.toml")
except tomllib.TOMLDecodeError as e:
    print(f"Error al decodificar TOML: {e}")
```