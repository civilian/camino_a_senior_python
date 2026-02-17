Saber la teoría es una cosa, pero ¿cómo se traduce en código robusto y eficiente? Un simple `requests.get()` esconde décadas de evolución. Exploremos cómo un ingeniero senior maneja las conexiones, elige los formatos de datos correctos y asegura la comunicación con criptografía.

# Internet & HTTP Concepts (RFC7231, RFC7540, JSON, XML, HTTPS)

## 4. Implementación Práctica en Python

Usaremos la biblioteca `requests`, el estándar de facto en Python para trabajar con HTTP. Es una obra de arte de diseño de API.

### Ejemplo 1: Solicitud GET y POST con JSON

```python
import requests
import json

# --- GET: Obteniendo datos de una API pública ---
# JSONPlaceholder es una excelente API falsa para pruebas.
API_URL = "https://jsonplaceholder.typicode.com/posts/1"

print("--- Realizando una solicitud GET ---")
try:
    response = requests.get(API_URL)
    
    # Siempre verifica el código de estado. ¡Esto es crucial!
    response.raise_for_status()  # Lanza una excepción para códigos de error (4xx o 5xx)

    # requests puede decodificar JSON por nosotros
    post_data = response.json()
    
    print(f"Título del post: {post_data['title']}")
    print(f"Código de estado: {response.status_code}")
    print("Cabeceras de respuesta (parcial):")
    print(f"  Content-Type: {response.headers.get('Content-Type')}")
    print(f"  Date: {response.headers.get('Date')}")

except requests.exceptions.RequestException as e:
    print(f"Error en la solicitud: {e}")

# --- POST: Creando un nuevo recurso ---
print("\n--- Realizando una solicitud POST ---")
new_post = {
    "title": "Un post desde Python",
    "body": "Este es el cuerpo de nuestro nuevo post.",
    "userId": 1
}

# Las cabeceras le dicen al servidor qué tipo de datos estamos enviando
headers = {
    "Content-Type": "application/json; charset=utf-8"
}

try:
    # Enviamos nuestro diccionario Python, requests lo codificará a JSON
    response = requests.post(
        "https://jsonplaceholder.typicode.com/posts",
        json=new_post,  # Usar el argumento 'json' es la forma moderna y correcta
        headers=headers
    )
    response.raise_for_status()
    
    created_post = response.json()
    print("Post creado exitosamente:")
    print(created_post)
    print(f"Código de estado: {response.status_code}") # Debería ser 201 Created

except requests.exceptions.RequestException as e:
    print(f"Error en la solicitud: {e}")
```

### Comparación: "Mal vs. Bien" - Manejo de Conexiones

Un desarrollador junior podría hacer múltiples llamadas así:

```python
# MAL: Abre y cierra una nueva conexión TCP para cada solicitud. Ineficiente.
for i in range(1, 6):
    requests.get(f"https://jsonplaceholder.typicode.com/posts/{i}")
print("MAL: 5 conexiones TCP creadas y destruidas.")
```

Un desarrollador senior entiende el coste del handshake TCP y usa una **Sesión**:

```python
# BIEN: Usa un objeto Session para reutilizar la conexión TCP (Keep-Alive).
with requests.Session() as session:
    for i in range(1, 6):
        session.get(f"https://jsonplaceholder.typicode.com/posts/{i}")
print("BIEN: 1 conexión TCP reutilizada para 5 solicitudes.")
```
La diferencia en rendimiento en aplicaciones de alta carga es abismal.

### Caso de Estudio: JSON vs. XML

A principios de los 2000, XML era el rey para las APIs (en el paradigma SOAP).

**XML (eXtensible Markup Language):**
```xml
<post>
  <userId>1</userId>
  <id>1</id>
  <title>sunt aut facere repellat provident occaecati excepturi optio reprehenderit</title>
  <body>quia et suscipit\nsuscipit recusandae consequuntur expedita et cum\nreprehenderit molestiae ut ut quas totam\nnostrum rerum est autem sunt rem eveniet architecto</body>
</post>
```

**JSON (JavaScript Object Notation):**
```json
{
  "userId": 1,
  "id": 1,
  "title": "sunt aut facere repellat provident occaecati excepturi optio reprehenderit",
  "body": "quia et suscipit\nsuscipit recusandae consequuntur expedita et cum\nreprehenderit molestiae ut ut quas totam\nnostrum rerum est autem sunt rem eveniet architecto"
}
```

**¿Por qué ganó JSON en el mundo de las APIs web?**
| Característica | JSON | XML | Veredicto Senior |
| :--- | :--- | :--- | :--- |
| **Verbosidad** | Bajo | Alto (etiquetas de apertura/cierre) | JSON transfiere menos datos, crucial para móvil. |
| **Parsing** | Simple y rápido, nativo en JS. | Más complejo (requiere un parser DOM/SAX). | La simplicidad de JSON reduce la carga en cliente y servidor. |
| **Legibilidad** | Alta para humanos. | Alta, pero más densa. | Empate subjetivo, pero muchos prefieren la sintaxis de JSON. |
| **Tipos de Datos** | Soporta strings, números, booleanos, arrays, objetos. | Todo es un string, los tipos se definen en un schema (XSD). | El tipado nativo de JSON se mapea directamente a los lenguajes de programación. |
| **Esquemas** | Menos maduro (JSON Schema existe pero es menos usado). | Muy robusto (XSD, DTD). | XML es superior en entornos donde la validación estricta y los contratos de datos son primordiales (ej. finanzas, gobierno). |

**Decisión de diseño:** Para la mayoría de las APIs web modernas, donde el rendimiento y la facilidad de uso son clave, **JSON es la elección por defecto**. XML sigue siendo relevante en sistemas empresariales heredados o en dominios que requieren una validación de esquema extremadamente rigurosa.

## 5. Nivel Senior - Conceptos Avanzados

### HTTP/1.1 vs HTTP/2: El problema del "Head-of-Line Blocking"

En HTTP/1.1 con Keep-Alive, un cliente puede enviar múltiples solicitudes por la misma conexión, pero debe esperar la respuesta completa de la primera antes de recibir la segunda. Esto es **Head-of-Line (HOL) Blocking**.

**Analogía:** Imagina una caja de supermercado (la conexión TCP). En HTTP/1.1, aunque tengas 5 artículos pequeños (peticiones), si la persona delante de ti tiene un carro lleno (una petición lenta), tienes que esperar a que termine.

```
HTTP/1.1 Pipelining (Teórico):
Cliente:  [REQ1]--[REQ2]--[REQ3]----------------> Servidor
Servidor: <---------------[RESP1]--[RESP2]--[RESP3]-- Cliente
           (Si RESP1 es lenta, RESP2 y RESP3 se bloquean)

HTTP/2 Multiplexing:
Cliente:  [S1-REQ][S2-REQ][S1-DAT][S3-REQ][S2-DAT]...> Servidor
          <..[S1-RESP][S2-RESP][S3-RESP][S1-DAT]...  Cliente
          (Streams S1, S2, S3 intercalados en una única conexión)
```
HTTP/2 resuelve esto con **streams**. Cada par solicitud/respuesta tiene su propio stream, y los frames de diferentes streams se pueden intercalar (multiplexar) en la misma conexión. El carro lleno de la analogía ya no bloquea a los que tienen pocos artículos.

### HTTPS: La Criptografía Detrás del Candado Verde
HTTPS no es un protocolo nuevo; es **HTTP sobre TLS (Transport Layer Security)**. Su objetivo es proporcionar:
1.  **Cifrado:** Nadie en el medio puede leer los datos.
2.  **Integridad:** Nadie puede modificar los datos sin que se detecte.
3.  **Autenticación:** Estás seguro de que te estás comunicando con el servidor correcto (evita ataques Man-in-the-Middle).

**El Handshake TLS (simplificado):**
1.  **ClientHello:** El cliente dice "Hola, quiero hablar de forma segura. Aquí están mis capacidades de cifrado (cipher suites) y una cadena aleatoria".
2.  **ServerHello:** El servidor responde "Hola. De tus opciones, elijo esta cipher suite. Aquí está mi certificado (mi 'DNI') y mi propia cadena aleatoria".
3.  **Verificación del Certificado:** El cliente verifica el certificado del servidor con una Autoridad de Certificación (CA) de confianza (preinstalada en tu SO/navegador). Esto prueba que `google.com` es realmente Google.
4.  **Intercambio de Claves:** El cliente genera una "clave pre-maestra", la cifra con la **clave pública** del servidor (que estaba en el certificado) y la envía.
5.  **Creación de Claves de Sesión:** Tanto el cliente como el servidor usan las cadenas aleatorias y la clave pre-maestra para generar de forma independiente un conjunto idéntico de **claves de sesión simétricas**.
6.  **Finished:** A partir de ahora, toda la comunicación se cifra y descifra usando estas claves de sesión simétricas, que son mucho más rápidas que la criptografía asimétrica (pública/privada) usada solo para el intercambio inicial.

> "La seguridad a menudo se percibe como una barrera para la usabilidad, pero en el caso de la web, TLS no solo protege a los usuarios, sino que también habilita nuevas y potentes capacidades de la plataforma que requieren un origen seguro." — **Ilya Grigorik**, *High Performance Browser Networking* (2013)