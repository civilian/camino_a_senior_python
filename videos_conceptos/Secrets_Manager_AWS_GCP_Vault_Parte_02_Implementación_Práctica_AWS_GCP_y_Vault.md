Ya entendemos la teoría, pero ¿cómo se ve esto en el código del día a día? Pasemos del 'qué' al 'cómo' y veamos cómo interactuar con los guardianes de secretos de AWS, GCP y HashiCorp directamente desde Python.

# Secrets Manager (AWS, GCP, Vault)

### 4. Implementación Práctica: Del Dicho al Hecho

Basta de teoría. Veamos cómo estos guardianes digitales trabajan en la práctica con Python, el lenguaje franco de la infraestructura moderna.

#### Escenario:
Nuestra aplicación necesita conectarse a una base de datos PostgreSQL. En lugar de almacenar `postgres://user:password@host:port/db` en un archivo, lo guardaremos en un gestor de secretos.

#### Comparación Rápida: Antes vs. Después

| Aspecto              | Antes (Archivo `.env` o similar)                               | Después (Gestor de Secretos)                                                               |
| -------------------- | -------------------------------------------------------------- | ------------------------------------------------------------------------------------------ |
| **Seguridad**        | Texto plano en el disco. Riesgo de exposición en Git.          | Cifrado en reposo y en tránsito. Acceso controlado por IAM.                                |
| **Auditoría**        | Imposible saber quién leyó el archivo y cuándo.                | Registro detallado de cada acceso (solicitante, hora, secreto).                            |
| **Rotación**         | Manual, propensa a errores, requiere redespliegue.             | Automatizada, sin tiempo de inactividad, transparente para la aplicación.                  |
| **Gestión**          | Descentralizada y caótica (`secret-prod-v2-final.txt`).        | Centralizada, versionada y programática.                                                   |
| **Acceso Granular**  | Todo o nada. Si puedes leer el archivo, tienes el secreto.     | Políticas finas: este servicio solo puede leer este secreto específico.                    |

---

#### Ejemplo 1: AWS Secrets Manager con `boto3`

**Prerrequisitos:**
*   Tener credenciales de AWS configuradas (idealmente, ejecutar esto en una instancia EC2 o Lambda con un rol de IAM que tenga el permiso `secretsmanager:GetSecretValue`).
*   Haber creado un secreto en AWS Secrets Manager llamado `prod/my-app/postgres-uri`.

```python
# requirements: boto3
import boto3
import json
import os

def get_secret_from_aws(secret_name: str, region_name: str) -> str:
    """
    Recupera un secreto de AWS Secrets Manager.
    
    La autenticación se maneja implícitamente a través del SDK de AWS,
    que buscará credenciales en variables de entorno, archivos de configuración,
    o roles de IAM (la forma recomendada en producción).
    """
    # Crea un cliente de Secrets Manager
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        # La llamada a la API para obtener el valor del secreto
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except client.exceptions.ResourceNotFoundException:
        print(f"El secreto '{secret_name}' no fue encontrado.")
        raise
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")
        raise

    # Los secretos pueden ser una cadena o binarios. AWS recomienda almacenar
    # secretos complejos como una cadena JSON.
    if 'SecretString' in get_secret_value_response:
        secret = get_secret_value_response['SecretString']
        # Suponiendo que el secreto es un JSON con una clave 'uri'
        return json.loads(secret)['uri']
    else:
        # Manejo para secretos binarios (no es nuestro caso de uso)
        decoded_binary_secret = base64.b64decode(get_secret_value_response['SecretBinary'])
        return decoded_binary_secret

# --- Uso en la aplicación ---
if __name__ == "__main__":
    SECRET_NAME = "prod/my-app/postgres-uri"
    REGION = os.environ.get("AWS_REGION", "us-east-1")
    
    print("Intentando obtener la URI de la base de datos desde AWS Secrets Manager...")
    try:
        db_uri = get_secret_from_aws(SECRET_NAME, REGION)
        # Por supuesto, ¡NUNCA imprimas el secreto en una aplicación real!
        # Esto es solo para demostración.
        print("¡Éxito! Secreto recuperado.")
        # print(f"DB URI: {db_uri}") 
        # app.connect_to_db(db_uri)
    except Exception as e:
        print("No se pudo inicializar la aplicación. Falló la obtención del secreto.")

```

---

#### Ejemplo 2: Google Cloud Secret Manager con `google-cloud-secret-manager`

**Prerrequisitos:**
*   Autenticación de GCP configurada (ejecutando en GCE/GKE con una cuenta de servicio con el rol `Secret Manager Secret Accessor`).
*   Haber creado un secreto llamado `my-postgres-uri`.

```python
# requirements: google-cloud-secret-manager
from google.cloud import secretmanager
from google.api_core.exceptions import NotFound
import os

def get_secret_from_gcp(project_id: str, secret_id: str, version_id: str = "latest") -> str:
    """
    Recupera un secreto de Google Cloud Secret Manager.

    La autenticación se maneja a través de las Application Default Credentials (ADC)
    de Google Cloud.
    """
    client = secretmanager.SecretManagerServiceClient()

    # Construye el nombre completo del recurso del secreto
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"

    try:
        # Accede a la versión del secreto
        response = client.access_secret_version(request={"name": name})
    except NotFound:
        print(f"El secreto '{secret_id}' o la versión '{version_id}' no fue encontrado.")
        raise
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")
        raise

    # La carga útil del secreto se devuelve como bytes, así que la decodificamos
    payload = response.payload.data.decode("UTF-8")
    return payload

# --- Uso en la aplicación ---
if __name__ == "__main__":
    PROJECT_ID = os.environ.get("GCP_PROJECT")
    SECRET_ID = "my-postgres-uri"

    if not PROJECT_ID:
        print("La variable de entorno GCP_PROJECT no está configurada.")
    else:
        print("Intentando obtener la URI de la base de datos desde GCP Secret Manager...")
        try:
            db_uri = get_secret_from_gcp(PROJECT_ID, SECRET_ID)
            print("¡Éxito! Secreto recuperado.")
            # print(f"DB URI: {db_uri}")
        except Exception as e:
            print("No se pudo inicializar la aplicación. Falló la obtención del secreto.")

```

---

#### Ejemplo 3: HashiCorp Vault con `hvac`

**Prerrequisitos:**
*   Un servidor de Vault en ejecución y accesible.
*   Autenticación configurada. Usaremos el método `AppRole`, común para aplicaciones. La aplicación necesita un `ROLE_ID` y un `SECRET_ID` para autenticarse.

```python
# requirements: hvac
import hvac
import os

def get_secret_from_vault(vault_addr: str, role_id: str, secret_id: str, secret_path: str, secret_key: str) -> str:
    """
    Recupera un secreto de HashiCorp Vault usando autenticación AppRole.
    """
    client = hvac.Client(url=vault_addr)

    try:
        # 1. Autenticar usando AppRole para obtener un token de cliente
        auth_response = client.auth.approle.login(
            role_id=role_id,
            secret_id=secret_id,
        )
        # El token se almacena automáticamente en el cliente hvac
        client.token = auth_response['auth']['client_token']
        
        if not client.is_authenticated():
            raise Exception("Fallo en la autenticación con Vault AppRole.")

        # 2. Leer el secreto del motor de secretos KV (Key-Value) v2
        # La respuesta de KVv2 está anidada dentro de ['data']['data']
        read_secret_response = client.secrets.kv.v2.read_secret_version(path=secret_path)
        secret_value = read_secret_response['data']['data'][secret_key]
        
        return secret_value

    except Exception as e:
        print(f"Ocurrió un error al interactuar con Vault: {e}")
        raise

# --- Uso en la aplicación ---
if __name__ == "__main__":
    VAULT_ADDR = os.environ.get("VAULT_ADDR")
    ROLE_ID = os.environ.get("VAULT_ROLE_ID")
    SECRET_ID = os.environ.get("VAULT_SECRET_ID")
    
    SECRET_PATH = "my-app/postgres"
    SECRET_KEY = "uri"

    if not all([VAULT_ADDR, ROLE_ID, SECRET_ID]):
        print("Faltan variables de entorno de Vault (VAULT_ADDR, VAULT_ROLE_ID, VAULT_SECRET_ID).")
    else:
        print("Intentando obtener la URI de la base de datos desde HashiCorp Vault...")
        try:
            db_uri = get_secret_from_vault(VAULT_ADDR, ROLE_ID, SECRET_ID, SECRET_PATH, SECRET_KEY)
            print("¡Éxito! Secreto recuperado.")
            # print(f"DB URI: {db_uri}")
        except Exception as e:
            print("No se pudo inicializar la aplicación. Falló la obtención del secreto.")
```