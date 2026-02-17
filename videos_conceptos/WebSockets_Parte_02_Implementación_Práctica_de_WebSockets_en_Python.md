¿Sabías que en 2011 los WebSockets casi mueren por un fallo de seguridad? Esa crisis dio forma al protocolo que usamos hoy. Después de explorar esa fascinante historia, pondremos manos a la obra y construiremos un servidor de chat funcional en Python.

# WebSockets

---

### 3. Evolución Histórica Detallada: Una Saga de Colaboración y Crisis

La historia de WebSocket es un microcosmos de cómo se construyen los estándares de Internet: una mezcla de necesidad, innovación, debate feroz y, finalmente, consenso.

| Fecha        | Hito Clave                                                              | Figuras/Grupos Clave    | Contexto Computacional                                                              |
|--------------|-------------------------------------------------------------------------|-------------------------|-----------------------------------------------------------------------------------|
| **~2006**    | Auge de "Comet" y Long-Polling. El dolor de la web en tiempo real es agudo. | Alex Russell (Dojo)     | Web 2.0, AJAX es el rey. Aplicaciones como Gmail y Google Maps empujan los límites. |
| **2008**     | Primera propuesta de WebSocket dentro del borrador de HTML5.              | Ian Hickson (Google)    | Nace Google Chrome. La guerra de los navegadores se reaviva, centrada en la velocidad y las capacidades. |
| **2010**     | Primeras implementaciones en Chrome 4 y Safari 5. Comienzan los borradores IETF "HyBi". | IETF, W3C               | HTML5 está ganando la batalla contra Flash. La web abierta necesita sus propias capacidades ricas. |
| **2011**     | **Crisis de Seguridad:** Vulnerabilidad de envenenamiento de caché de proxy. | Adam Barth              | La seguridad en la web se convierte en una preocupación principal. Los proxies son omnipresentes en las redes corporativas. |
| **Dic 2011** | **Nacimiento del Estándar:** Se publica el **RFC 6455**. Introduce el enmascaramiento obligatorio del cliente. | IETF                      | La estandarización es clave para la interoperabilidad. Fin de la "edad oscura" de los borradores. |
| **2012+**    | Adopción masiva. Surgen librerías de alto nivel como Socket.IO.            | Comunidad Open Source   | Node.js populariza la programación de red basada en eventos. El ecosistema explota. |
| **Hoy**      | Estándar maduro. Base para WebRTC, GraphQL Subscriptions, y más.          | Todos los navegadores   | La web en tiempo real es la norma, no la excepción. IoT, streaming, juegos en la nube. |

> "El objetivo del Protocolo WebSocket es proporcionar un mecanismo para que las aplicaciones basadas en navegador necesiten comunicación bidireccional con servidores que no dependan de abrir múltiples conexiones HTTP." — **I. Fette**, *RFC 6455, The WebSocket Protocol* (2011)

Este viaje, especialmente la crisis de seguridad de 2011, nos enseña una lección vital de ingeniería: **el mundo real es complicado**. Un protocolo teóricamente perfecto puede fallar estrepitosamente al interactuar con la infraestructura existente (proxies, en este caso). La solución (el enmascaramiento) añadió complejidad, pero garantizó la viabilidad en el mundo real.

---

### 4. Implementación Práctica: Hablando el Idioma de los Sockets en Python

La teoría es elegante, pero el código es la verdad. Usaremos la librería `websockets` de Python, una implementación excelente y fiel al RFC que se integra a la perfección con `asyncio`.

#### Ejemplo: Un Servidor de Eco y un Cliente Curioso

**Servidor (`server.py`)**

```python
import asyncio
import websockets
import logging

# Configurar un logging básico para ver qué pasa
logging.basicConfig(level=logging.INFO)

# Un conjunto para mantener un registro de todos los clientes conectados
CONNECTED_CLIENTS = set()

async def echo_and_broadcast(websocket, path):
    """
    Manejador para cada conexión de cliente.
    Se registra, escucha mensajes, los devuelve (eco),
    y los retransmite a todos los demás clientes.
    """
    # Registrar el nuevo cliente
    CONNECTED_CLIENTS.add(websocket)
    logging.info(f"Nuevo cliente conectado: {websocket.remote_address}. Total: {len(CONNECTED_CLIENTS)}")
    
    try:
        # El bucle `async for` es la forma idiomática de escuchar mensajes.
        # Se ejecuta hasta que el cliente se desconecta.
        async for message in websocket:
            logging.info(f"Mensaje recibido de {websocket.remote_address}: {message}")
            
            # 1. Patrón de Eco: Devolver el mensaje al remitente original
            await websocket.send(f"Eco: {message}")
            
            # 2. Patrón de Broadcast: Enviar el mensaje a todos los demás clientes
            # Creamos una copia de la lista de clientes para evitar problemas si alguien se desconecta
            # mientras estamos iterando.
            other_clients = [client for client in CONNECTED_CLIENTS if client != websocket]
            if other_clients:
                broadcast_message = f"Alguien dijo: {message}"
                # `asyncio.gather` es una forma eficiente de ejecutar muchas tareas `awaitable` en paralelo.
                await asyncio.gather(*[client.send(broadcast_message) for client in other_clients])

    except websockets.exceptions.ConnectionClosed as e:
        logging.warning(f"Cliente {websocket.remote_address} desconectado: {e}")
    finally:
        # Asegurarse de que el cliente se elimina del conjunto al desconectarse
        CONNECTED_CLIENTS.remove(websocket)
        logging.info(f"Cliente {websocket.remote_address} eliminado. Total: {len(CONNECTED_CLIENTS)}")

async def main():
    # Iniciar el servidor WebSocket en localhost, puerto 8765
    async with websockets.serve(echo_and_broadcast, "localhost", 8765):
        logging.info("Servidor WebSocket iniciado en ws://localhost:8765")
        # El servidor se ejecutará indefinidamente
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
```

**Cliente (`client.py`)**

```python
import asyncio
import websockets

async def listen_and_send():
    uri = "ws://localhost:8765"
    # `async with` maneja la conexión y el cierre de forma segura
    async with websockets.connect(uri) as websocket:
        print(f"Conectado a {uri}")

        # Tarea para escuchar mensajes del servidor
        async def receive_messages():
            try:
                async for message in websocket:
                    print(f"< Recibido: {message}")
            except websockets.exceptions.ConnectionClosed:
                print("Conexión cerrada por el servidor.")

        # Tarea para enviar mensajes al servidor
        async def send_messages():
            while True:
                message_to_send = await asyncio.to_thread(input, "Escribe un mensaje (o 'exit' para salir): ")
                if message_to_send.lower() == 'exit':
                    break
                await websocket.send(message_to_send)
                print(f"> Enviado: {message_to_send}")
            
            # Señal para que la tarea de recepción termine
            await websocket.close()

        # Ejecutar ambas tareas concurrentemente
        receive_task = asyncio.create_task(receive_messages())
        send_task = asyncio.create_task(send_messages())

        # Esperar a que ambas tareas terminen
        await asyncio.gather(receive_task, send_task)

if __name__ == "__main__":
    try:
        asyncio.run(listen_and_send())
    except KeyboardInterrupt:
        print("\nCliente cerrado.")
```

Para probarlo, ejecuta `server.py` en una terminal. Luego, abre dos o más terminales y ejecuta `client.py` en cada una. Verás cómo los mensajes de un cliente se retransmiten a los otros.

#### Comparación: "Antes vs Después"

**Antes (Long-Polling con una API REST):**

```javascript
// Cliente (JavaScript) - El Mal Camino
function longPoll() {
    fetch('/api/messages')
        .then(response => response.json())
        .then(data => {
            // Procesar datos...
            console.log(data);
            // Iniciar la siguiente petición inmediatamente
            longPoll();
        })
        .catch(error => {
            console.error("Error en long-polling, reintentando...", error);
            setTimeout(longPoll, 5000); // Esperar antes de reintentar
        });
}
longPoll();
```
*Observa la complejidad del manejo de errores, los reintentos y la sobrecarga de cada petición.*

**Después (WebSocket):**

```javascript
// Cliente (JavaScript) - El Buen Camino
const socket = new WebSocket('ws://localhost:8765');

socket.onopen = (event) => {
    console.log('Conexión establecida!');
    socket.send('Hola, servidor!');
};

socket.onmessage = (event) => {
    // Procesar datos...
    console.log(`Mensaje recibido: ${event.data}`);
};

socket.onclose = (event) => {
    console.log('Conexión cerrada. Intentando reconectar...');
    // Aquí iría la lógica de reconexión
};

socket.onerror = (error) => {
    console.error('Error de WebSocket:', error);
};
```
*La API es limpia, basada en eventos y representa el estado de la conexión de forma natural.*