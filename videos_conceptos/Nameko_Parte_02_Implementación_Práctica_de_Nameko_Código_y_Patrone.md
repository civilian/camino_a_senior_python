La teoría es fascinante, pero ¿cómo se ve todo esto en código real? Es hora de dejar los diagramas y empezar a construir. Vamos a crear nuestro primer servicio y a descubrir los patrones que hacen que los sistemas distribuidos realmente funcionen.

# Nameko

---

## 4. Implementación Práctica: De la Teoría al Código

Hablemos en el lenguaje de los programadores: el código.

### Ejemplo Canónico: El Traductor de Saludos

Imagina que tenemos un servicio que traduce "Hola" a diferentes idiomas.

**1. El Servicio Traductor (`translator_service.py`)**

```python
# translator_service.py
import os
from nameko.rpc import rpc

# Variable de entorno para configurar el broker de mensajes (RabbitMQ)
# Ejemplo: AMQP_URI=amqp://guest:guest@localhost
AMQP_URI = os.environ.get('AMQP_URI')

class TranslatorService:
    """
    Un servicio simple que "traduce" saludos.
    En un caso real, podría llamar a una API externa o a una base de datos.
    """
    name = "translator_service" # Nombre canónico del servicio

    translations = {
        "en": "Hello",
        "es": "Hola",
        "fr": "Bonjour",
        "de": "Guten Tag"
    }

    @rpc
    def translate(self, language_code, word):
        """
        El decorador @rpc expone este método para ser llamado remotamente.
        Nameko se encarga de:
        1. Crear una cola dedicada para este servicio.
        2. Escuchar en esa cola por peticiones RPC.
        3. Deserializar los argumentos (language_code, word).
        4. Llamar a este método con los argumentos.
        5. Serializar el valor de retorno.
        6. Enviar la respuesta de vuelta a una cola de respuesta temporal.
        """
        print(f"[*] Recibida petición de traducción para '{word}' a '{language_code}'")
        if word.lower() == "hello":
            return self.translations.get(language_code, "Sorry, language not found.")
        return "Sorry, I can only translate 'hello'."

# Para ejecutar este servicio:
# 1. Instala nameko: pip install nameko
# 2. Asegúrate de que RabbitMQ está corriendo.
# 3. Exporta la variable de entorno: export AMQP_URI="amqp://guest:guest@localhost"
# 4. Ejecuta desde la terminal: nameko run translator_service
```

**2. El Cliente (o Shell Interactiva de Nameko)**

La forma más fácil de interactuar con un servicio Nameko es usando la shell que provee.

Abre otra terminal y ejecuta:
`nameko shell --broker amqp://guest:guest@localhost`

Dentro de la shell de Nameko (que es una shell de iPython):

```python
# Llama al método `translate` del servicio `translator_service`
>>> n.rpc.translator_service.translate(language_code="es", word="hello")
[*] Recibida petición de traducción para 'hello' a 'es'  # <-- Esto se imprime en la terminal del servicio
'Hola'

>>> n.rpc.translator_service.translate(language_code="fr", word="hello")
[*] Recibida petición de traducción para 'hello' a 'fr'
'Bonjour'

>>> n.rpc.translator_service.translate(language_code="jp", word="hello")
[*] Recibida petición de traducción para 'hello' a 'jp'
'Sorry, language not found.'
```
¡Magia! Has ejecutado código en un proceso (el servicio) desde otro (la shell) sin escribir una sola línea de código de red, serialización o gestión de colas. Eso es el poder de la abstracción de Nameko.

### Patrones de Uso Comunes y Avanzados

#### Patrón 1: Servicio a Servicio (El pan de cada día)

Imagina un servicio de `greeter` que usa el `translator_service`.

```python
# greeter_service.py
import os
from nameko.rpc import rpc, RpcProxy

AMQP_URI = os.environ.get('AMQP_URI')

class GreeterService:
    name = "greeter_service"

    # Inyección de Dependencias en acción.
    # Nameko crea un proxy para llamar al translator_service.
    translator = RpcProxy("translator_service")

    @rpc
    def greet(self, name, language="en"):
        """
        Saluda a un usuario en su idioma preferido.
        """
        print(f"[*] Recibida petición de saludo para '{name}' en '{language}'")
        
        # La llamada parece local, pero es una llamada de red a otro servicio.
        hello_in_language = self.translator.translate(language, "hello")
        
        return f"{hello_in_language}, {name}!"

# Ejecuta este servicio: nameko run greeter_service
```

Ahora desde la `nameko shell`:
`>>> n.rpc.greeter_service.greet(name="Alice", language="de")`
`'Guten Tag, Alice!'`

#### Patrón 2: Publicar/Suscribir (Eventos para Desacoplar)

RPC acopla al llamador con el llamado. Para un desacoplamiento máximo, usamos eventos. Imagina que cuando un usuario se registra, múltiples servicios necesitan reaccionar: enviar un email de bienvenida, preparar su perfil, etc.

```python
# user_service.py
from nameko.rpc import rpc
from nameko.events import EventDispatcher, event_handler

class UserService:
    name = "user_service"
    dispatch = EventDispatcher() # Inyecta el despachador de eventos

    @rpc
    def register_user(self, email, password):
        # ... lógica para crear el usuario en la BD ...
        print(f"[*] Registrando nuevo usuario: {email}")
        
        # Dispara un evento con los datos del nuevo usuario.
        # No sabe ni le importa quién está escuchando.
        self.dispatch("user_created", {"email": email, "id": 123})
        return "User registered successfully."

# email_service.py
class EmailService:
    name = "email_service"

    @event_handler("user_service", "user_created")
    def handle_user_created(self, payload):
        """
        Este método se ejecuta CADA VEZ que user_service dispara "user_created".
        """
        print(f"[*] Enviando email de bienvenida a {payload['email']}")
        # ... lógica para enviar el email ...

# profile_service.py
class ProfileService:
    name = "profile_service"
    
    @event_handler("user_service", "user_created")
    def handle_user_created(self, payload):
        print(f"[*] Creando perfil para el usuario ID {payload['id']}")
        # ... lógica para inicializar el perfil ...
```
Ejecuta los tres servicios (`nameko run user_service email_service profile_service`).
Desde la shell, llama a `n.rpc.user_service.register_user("test@example.com", "pass")`.
Verás los logs en las terminales de `email_service` y `profile_service`, demostrando que ambos reaccionaron al mismo evento de forma independiente.

### Comparaciones: "Mal vs. Bien"

| Mal: Alto Acoplamiento (El Monolito Distribuido) | Bien: Bajo Acoplamiento (Event-Driven) |
| :--- | :--- |
| El servicio de `Órdenes` llama por RPC al servicio de `Notificaciones`, luego al de `Inventario`, luego al de `Facturación` en una cadena larga y frágil. Si `Facturación` falla, la orden entera falla. | El servicio de `Órdenes` procesa la orden y emite un evento `order_placed`. Los servicios de `Notificaciones`, `Inventario` y `Facturación` se suscriben a este evento y reaccionan de forma independiente y en paralelo. El sistema es más resiliente. |
| **Código "Malo" (conceptual):**<br> `def place_order():`<br> `  self.inventory.decrement(item)`<br> `  self.billing.charge(user)`<br> `  self.notifications.send_email()` | **Código "Bueno" (conceptual):**<br> `def place_order():`<br> `  # ...` <br> `  self.dispatch("order_placed", data)` |