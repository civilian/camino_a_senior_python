La teoría es fascinante, pero ¿cómo se ve OAuth en la práctica, línea por línea? Vamos a construir un flujo de autorización completo desde cero, usando Python. Veremos cómo el cliente, el usuario y el servidor interactúan en esta danza segura de códigos y tokens.

# OAuth

## 4. Implementación Práctica: Del Código a la Realidad

Hablemos en el lenguaje de los constructores: el código. Usaremos Python para ilustrar el flujo más común y seguro: el **Authorization Code Flow con PKCE**.

**Escenario**: Tenemos una aplicación web (`client_app.py`) que quiere acceder al perfil de un usuario en un servicio llamado "SuperService" (`authorization_server.py`).

### Los Actores en Código

*   **Servidor de Autorización (`authorization_server.py`)**: Usaremos Flask para simular Google, GitHub, etc. Gestiona el consentimiento del usuario y emite códigos y tokens.
*   **Aplicación Cliente (`client_app.py`)**: Una simple aplicación de consola que intentará acceder a los datos del usuario.

#### Paso 0: Preparación y PKCE

Antes de empezar, el cliente genera un `code_verifier` (una cadena aleatoria) y un `code_challenge` (su versión hasheada y codificada en base64). Esto es PKCE.

```python
# client_app.py (inicio)
import requests
import hashlib
import base64
import os
import webbrowser

# --- Configuración del Cliente ---
CLIENT_ID = "my-awesome-client"
CLIENT_SECRET = "super-secret-for-server-apps" # No usar en SPAs o apps móviles
REDIRECT_URI = "http://localhost:5001/callback"
AUTH_SERVER_URL = "http://localhost:5000"

# --- PKCE Generation ---
def generate_pkce_pair():
    code_verifier = base64.urlsafe_b64encode(os.urandom(40)).decode('utf-8').rstrip('=')
    sha256 = hashlib.sha256(code_verifier.encode('utf-8')).digest()
    code_challenge = base64.urlsafe_b64encode(sha256).decode('utf-8').rstrip('=')
    return code_verifier, code_challenge

code_verifier, code_challenge = generate_pkce_pair()
print(f"🔑 Generado Code Verifier (secreto del cliente): {code_verifier[:10]}...")
```

#### Paso 1: El Cliente Redirige al Usuario

El cliente construye una URL y redirige al usuario al servidor de autorización, pidiendo permiso (`scope`) para leer el perfil.

```python
# client_app.py (continuación)
def start_auth():
    auth_url = (
        f"{AUTH_SERVER_URL}/authorize?"
        f"response_type=code&"
        f"client_id={CLIENT_ID}&"
        f"redirect_uri={REDIRECT_URI}&"
        f"scope=profile:read&"
        f"code_challenge={code_challenge}&"
        f"code_challenge_method=S256&"
        f"state=random_state_string_for_csrf_protection" # ¡CRÍTICO para seguridad!
    )
    print(f"\n🚀 Paso 1: Redirigiendo al usuario para autorización...")
    print(f"Abra esta URL en su navegador:\n{auth_url}")
    webbrowser.open(auth_url)

# (Más tarde, el servidor de callback recibirá el código)
```

#### Paso 2: El Usuario da su Consentimiento

En el servidor de autorización, el usuario ve una pantalla de consentimiento. Si acepta, el servidor genera un `authorization_code` y lo asocia con el `code_challenge` recibido.

```python
# authorization_server.py (usando Flask)
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# Almacenamiento en memoria para la demo
auth_codes = {}

@app.route('/authorize')
def authorize():
    # ... (validar client_id, redirect_uri, etc.) ...
    client_id = request.args.get('client_id')
    code_challenge = request.args.get('code_challenge')
    
    # Guardar el challenge para más tarde
    temp_code = "random_auth_code_12345"
    auth_codes[temp_code] = {'code_challenge': code_challenge, 'client_id': client_id}
    
    # Mostrar pantalla de consentimiento (simplificada)
    return render_template_string("""
        <h1>Permitir que '{{ client_id }}' acceda a tu perfil?</h1>
        <form action="/consent" method="post">
            <input type="hidden" name="code" value="{{ code }}">
            <input type="hidden" name="redirect_uri" value="{{ redirect_uri }}">
            <input type="submit" value="Allow">
        </form>
    """, client_id=client_id, code=temp_code, redirect_uri=request.args.get('redirect_uri'))

@app.route('/consent', methods=['POST'])
def consent():
    code = request.form.get('code')
    redirect_uri = request.form.get('redirect_uri')
    # Redirigir de vuelta al cliente con el código
    return f'<script>window.location.href="{redirect_uri}?code={code}&state=random_state_string_for_csrf_protection"</script>'
```

#### Paso 3: Intercambio de Código por Token

El cliente recibe el código en su `redirect_uri`. Ahora, en el *backend*, intercambia ese código (junto con el `code_verifier` original) por un token de acceso.

```python
# client_app.py (en el endpoint de callback)
def handle_callback(code):
    print("\n🔄 Paso 3: Código de autorización recibido. Intercambiando por token...")
    
    token_url = f"{AUTH_SERVER_URL}/token"
    payload = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET, # Solo para clientes confidenciales
        'code_verifier': code_verifier # ¡La prueba de PKCE!
    }
    
    response = requests.post(token_url, data=payload)
    if response.status_code == 200:
        access_token = response.json().get('access_token')
        print("✅ ¡Token de acceso obtenido con éxito!")
        return access_token
    else:
        print(f"❌ Error al obtener el token: {response.text}")
        return None
```

El servidor de autorización valida todo: el código, el `client_id`, y lo más importante, que el hash del `code_verifier` recibido coincida con el `code_challenge` que guardó en el paso 2.

```python
# authorization_server.py (continuación)
@app.route('/token', methods=['POST'])
def token():
    # ... (validar grant_type, client_id, client_secret) ...
    code = request.form.get('code')
    code_verifier = request.form.get('code_verifier')
    
    if code not in auth_codes:
        return "Código inválido", 400
        
    # Verificación PKCE
    stored_challenge = auth_codes[code]['code_challenge']
    sha256 = hashlib.sha256(code_verifier.encode('utf-8')).digest()
    recreated_challenge = base64.urlsafe_b64encode(sha256).decode('utf-8').rstrip('=')

    if stored_challenge != recreated_challenge:
        return "PKCE verifier no coincide", 401

    # ¡Éxito! Emitir token
    del auth_codes[code] # El código es de un solo uso
    access_token = "jwt_or_opaque_token_here"
    return jsonify({'access_token': access_token, 'token_type': 'Bearer'})
```

#### Paso 4: Usar el Token para Acceder a Recursos

Con el token en mano, el cliente finalmente puede hacer lo que quería desde el principio.

```python
# client_app.py (continuación)
def get_user_profile(access_token):
    print("\n📡 Paso 4: Usando el token para acceder a la API de recursos...")
    
    profile_url = f"{AUTH_SERVER_URL}/api/profile"
    headers = {'Authorization': f'Bearer {access_token}'}
    
    response = requests.get(profile_url, headers=headers)
    if response.status_code == 200:
        print("🎉 Perfil de usuario obtenido:")
        print(response.json())
    else:
        print(f"❌ Error al acceder al recurso: {response.text}")

# --- Flujo principal ---
# (Se necesitaría un pequeño servidor web para recibir el callback,
# pero para la demo, simularemos que el usuario pega el código)
start_auth()
auth_code = input("Pegue el 'code' de la URL de redirección aquí: ")
token = handle_callback(auth_code)
if token:
    get_user_profile(token)
```

### Comparación: Antes vs. Después

| Característica        | Antes (Anti-Patrón de Contraseña)                               | Después (OAuth 2.0)                                                              | **El "Porqué" del Cambio**                                                                                             |
|-----------------------|-----------------------------------------------------------------|----------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------|
| **Credenciales**      | El cliente almacena usuario/contraseña del usuario.             | El cliente almacena un token de acceso temporal.                                 | **Principio de Mínimo Privilegio**: El token tiene permisos y vida limitados. El daño de una brecha es mucho menor. |
| **Permisos**          | Acceso total y absoluto a la cuenta del usuario.                | Acceso granular definido por `scopes` (`profile:read`, `posts:write`).           | **Control del Usuario**: El usuario sabe exactamente qué permisos está concediendo y puede negarse a los innecesarios. |
| **Revocación**        | El usuario debe cambiar su contraseña, rompiendo todo.          | El usuario puede revocar el acceso para una aplicación específica en la configuración. | **Gestión Centralizada**: El servidor de autorización actúa como un panel de control de confianza para el usuario.     |
| **Seguridad del Canal** | Depende de la implementación del cliente.                       | Forzado a través de TLS/HTTPS. El token se pasa en un header `Authorization`.    | **Estandarización**: Reduce la probabilidad de errores de implementación. "Bearer" es un esquema bien definido.        |