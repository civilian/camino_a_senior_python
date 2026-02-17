¿Alguna vez has visto una clase que intenta hacerlo todo y termina siendo un desastre? Vamos a tomar un ejemplo común, un sistema de pedidos, y lo transformaremos de un 'God Object' frágil a un diseño robusto y elegante usando los 9 principios de GRASP, paso a paso.

# GRASP

### 4. Implementación Práctica: De la Teoría al Teclado en Python

Vamos a construir un sistema simple de procesamiento de pedidos para una tienda online. Empezaremos con un diseño "ingenuo" y lo refactorizaremos aplicando los 9 principios de GRASP.

#### **El Escenario: Una Tienda Online Simple**

Un cliente realiza un pedido que contiene varios productos. El sistema debe calcular el total y procesar el pago.

#### **Versión 1: El Anti-Patrón "God Object" (Mal Diseño)**

Un desarrollador intermedio podría empezar con una única clase `Order` que lo hace todo.

```python
# MAL: Un objeto que lo sabe y lo hace todo (Baja Cohesión, Alto Acoplamiento)
class Order:
    def __init__(self, customer_name, address):
        self.customer_name = customer_name
        self.address = address
        self.items = []
        self.payment_type = None
        self.card_number = None

    def add_item(self, product_name, quantity, price):
        self.items.append({"name": product_name, "qty": quantity, "price": price})

    def calculate_total(self):
        total = 0
        for item in self.items:
            total += item['qty'] * item['price']
        # Añadir impuesto
        total *= 1.21
        return total

    def process_payment(self, payment_type, card_number=None):
        self.payment_type = payment_type
        self.card_number = card_number
        total_amount = self.calculate_total()
        
        if self.payment_type == "credit_card":
            print(f"Connecting to payment gateway...")
            print(f"Charging ${total_amount:.2f} to card {self.card_number}")
            # Lógica compleja de la pasarela de pago aquí...
            return True
        elif self.payment_type == "paypal":
            print(f"Redirecting to PayPal for amount ${total_amount:.2f}")
            # Lógica de redirección de PayPal aquí...
            return True
        return False

# Uso
order = Order("John Doe", "123 Main St")
order.add_item("Laptop", 1, 1200)
order.add_item("Mouse", 1, 25)
order.process_payment("credit_card", "4111-...")
```

**Problemas:**
*   **Baja Cohesión:** La clase `Order` hace de todo: gestiona ítems, calcula totales, maneja la lógica de pago. Sus responsabilidades no están relacionadas.
*   **Alto Acoplamiento:** Está directamente acoplada a los detalles de la pasarela de pago. Si la API de pago cambia, hay que modificar `Order`.
*   **Violación de SRP (Single Responsibility Principle):** Tiene múltiples razones para cambiar.

#### **Versión 2: Refactorizando con GRASP (Buen Diseño)**

Apliquemos los principios de GRASP para desentrañar este lío.

##### **1. Information Expert (El Experto en Información)**
*Principio: Asigna una responsabilidad al objeto que tiene la información necesaria para cumplirla.*

**Pregunta:** ¿Quién debe calcular el total de un ítem de línea?
**Respuesta:** El propio ítem de línea, ya que conoce su cantidad y precio. ¿Y el total del pedido? El pedido, ya que conoce todos sus ítems de línea.

```python
# BIEN: Aplicando Information Expert
class Product:
    def __init__(self, name: str, price: float):
        self.name = name
        self.price = price

class LineItem:
    def __init__(self, product: Product, quantity: int):
        self.product = product
        self.quantity = quantity

    def get_subtotal(self) -> float: # LineItem es el experto en su subtotal
        return self.product.price * self.quantity

class Order:
    def __init__(self, customer_name: str, address: str):
        self.customer_name = customer_name
        self.address = address
        self.line_items: list[LineItem] = []

    def add_item(self, product: Product, quantity: int):
        # 2. Creator (Creador)
        # Principio: Asigna la responsabilidad de crear un objeto A a la clase B si B "contiene" o "agrega" A.
        # Aquí, Order contiene LineItems, por lo que es un buen candidato para crearlos.
        self.line_items.append(LineItem(product, quantity))

    def calculate_total(self) -> float: # Order es el experto en el total
        return sum(item.get_subtotal() for item in self.line_items)
```
**Mejoras:** Ahora cada clase es responsable de la información que posee. La cohesión de `LineItem` y `Order` ha aumentado.

##### **3. Controller (Controlador)**
*Principio: Asigna la responsabilidad de manejar los eventos del sistema a una clase que represente el sistema global o un caso de uso.*

**Pregunta:** ¿Quién debe recibir la petición HTTP para crear un pedido?
**Respuesta:** No el objeto `Order` directamente. Un objeto `OrderController` que actúe como intermediario entre la capa de UI/API y el modelo de dominio.

```python
# BIEN: Aplicando Controller
class OrderController:
    def create_order(self, request_data):
        # 1. Recibe y parsea la petición (de un framework web como Flask/Django)
        customer_name = request_data['customer_name']
        items_data = request_data['items']
        
        # 2. Crea los objetos de dominio
        order = Order(customer_name, "Address from request")
        for item in items_data:
            # (Suponemos que obtenemos el producto de una base de datos)
            product = Product(item['product_name'], item['price'])
            order.add_item(product, item['quantity'])
            
        # 3. Delega el trabajo al dominio
        # ... aquí iría la lógica de pago, que veremos a continuación
        
        # 4. Devuelve una respuesta
        return {"status": "success", "order_id": id(order), "total": order.calculate_total()}

# Simulación de uso
controller = OrderController()
request = {
    "customer_name": "Jane Doe",
    "items": [
        {"product_name": "Keyboard", "price": 75, "quantity": 1},
        {"product_name": "Monitor", "price": 300, "quantity": 2}
    ]
}
response = controller.create_order(request)
print(response)
```
**Mejoras:** Hemos desacoplado la lógica de la interfaz de usuario/API de nuestro modelo de dominio (`Order`). `Order` ya no sabe nada sobre peticiones HTTP.

##### **4. Low Coupling (Bajo Acoplamiento) y 5. High Cohesion (Alta Cohesión)**
Estos son los principios rectores que motivan las siguientes decisiones. Queremos que las clases sean independientes y enfocadas.

##### **6. Polymorphism (Polimorfismo)**
*Principio: Cuando un comportamiento relacionado varía según el tipo, asigna la responsabilidad de ese comportamiento usando operaciones polimórficas a los tipos para los que varía.*

**Pregunta:** La lógica de pago varía (Tarjeta, PayPal). ¿Cómo manejamos esto sin `if/elif/else`?
**Respuesta:** Con una interfaz `PaymentMethod` y clases concretas.

```python
from abc import ABC, abstractmethod

class PaymentMethod(ABC):
    @abstractmethod
    def pay(self, amount: float) -> bool:
        pass

class CreditCardPayment(PaymentMethod):
    def pay(self, amount: float) -> bool:
        print(f"Charging ${amount:.2f} via Credit Card.")
        # Lógica de la pasarela de tarjeta
        return True

class PayPalPayment(PaymentMethod):
    def pay(self, amount: float) -> bool:
        print(f"Processing ${amount:.2f} via PayPal.")
        # Lógica de la API de PayPal
        return True
```
**Mejoras:** `Order` ya no necesita saber sobre los detalles de cada método de pago. Simplemente interactuará con la interfaz `PaymentMethod`. Esto reduce el acoplamiento y facilita la adición de nuevos métodos de pago (ej. `CryptoPayment`) sin modificar el código existente (abierto a extensión, cerrado a modificación - ¡hola, OCP de SOLID!).

##### **7. Pure Fabrication (Fabricación Pura)**
*Principio: Si no encuentras una clase del mundo real para una responsabilidad, crea una clase artificial que no represente un concepto del dominio.*

**Pregunta:** ¿Quién debe procesar el pago? `Order` no debería, es de baja cohesión. `PaymentMethod` tampoco, su responsabilidad es solo *ejecutar* el pago.
**Respuesta:** Creemos un `PaymentProcessor`, una Fabricación Pura. Su único propósito es coordinar el pago.

```python
# BIEN: Aplicando Pure Fabrication
class PaymentProcessor:
    def process(self, order: Order, payment_method: PaymentMethod) -> bool:
        total = order.calculate_total()
        # Podría haber lógica adicional aquí: verificar stock, aplicar descuentos, etc.
        return payment_method.pay(total)
```
**Mejoras:** La cohesión de `Order` aumenta enormemente. La lógica de orquestación del pago ahora reside en una clase dedicada y cohesiva.

##### **8. Indirection (Indirección)**
*Principio: Para evitar el acoplamiento directo entre dos elementos, introduce un intermediario para que se comuniquen a través de él.*

**Pregunta:** Nuestro `CreditCardPayment` habla directamente con una "pasarela de pago". ¿Qué pasa si cambiamos de proveedor (de Stripe a Adyen)?
**Respuesta:** Introducimos un `PaymentGatewayAdapter` que desacopla nuestra lógica de la implementación específica de la pasarela.

```python
# BIEN: Aplicando Indirection y 9. Protected Variations (Variaciones Protegidas)
# Principio PV: Identifica puntos de variación o inestabilidad predecibles y asigna responsabilidades para crear una interfaz estable a su alrededor.

# La API externa es un punto de inestabilidad. La protegemos con un Adapter.
class PaymentGateway(ABC):
    @abstractmethod
    def charge(self, amount: float, card_details: dict) -> str: # transaction_id
        pass

# Implementación específica de un proveedor
class StripeGateway(PaymentGateway):
    def charge(self, amount: float, card_details: dict) -> str:
        print(f"[STRIPE API] Charging {amount} to {card_details['number']}")
        return "stripe_txn_123"

class AdyenGateway(PaymentGateway):
    def charge(self, amount: float, card_details: dict) -> str:
        print(f"[ADYEN API] Processing payment of {amount} for card ending in {card_details['number'][-4:]}")
        return "adyen_txn_abc"

# Nuestro CreditCardPayment ahora usa la indirección del Gateway
class CreditCardPayment(PaymentMethod):
    def __init__(self, card_details: dict, gateway: PaymentGateway):
        self.card_details = card_details
        self.gateway = gateway # Inyección de dependencias

    def pay(self, amount: float) -> bool:
        transaction_id = self.gateway.charge(amount, self.card_details)
        return bool(transaction_id)
```

#### **Versión Final: Un Diseño Senior**

```python
# --- El código completo y bien diseñado ---
# (Incluiría todas las clases definidas anteriormente: Product, LineItem, Order,
#  PaymentMethod, CreditCardPayment, PayPalPayment, PaymentProcessor, PaymentGateway, etc.)

# --- Flujo de uso a nivel de Controller ---
class OrderController:
    def __init__(self, payment_gateway: PaymentGateway):
        self.payment_gateway = payment_gateway

    def place_order(self, request_data):
        # ... crear Order y LineItems como antes ...
        order = Order(request_data['customer_name'], "...")
        # ... añadir items ...

        # Elegir el método de pago
        payment_type = request_data['payment']['type']
        if payment_type == 'credit_card':
            payment_method = CreditCardPayment(
                request_data['payment']['details'],
                self.payment_gateway # Usamos el gateway inyectado
            )
        elif payment_type == 'paypal':
            payment_method = PayPalPayment()
        else:
            raise ValueError("Unsupported payment method")
            
        # Usar la Fabricación Pura para procesar
        processor = PaymentProcessor()
        success = processor.process(order, payment_method)

        if success:
            return {"status": "Order placed successfully"}
        else:
            return {"status": "Payment failed"}

# --- Configuración y Ejecución (Dependency Injection) ---
stripe_gateway = StripeGateway()
controller = OrderController(payment_gateway=stripe_gateway)

# Simular una petición de API
api_request = {
    "customer_name": "Senior Dev",
    "items": [...],
    "payment": {
        "type": "credit_card",
        "details": {"number": "4242-...", "cvc": "123"}
    }
}
controller.place_order(api_request)
```

| Principio GRASP | Antes (Diseño Malo) | Después (Diseño Bueno) |
| :--- | :--- | :--- |
| **Information Expert** | `Order` calculaba todo, incluso con datos que no poseía directamente. | `LineItem` calcula su subtotal. `Order` calcula el total delegando. |
| **Creator** | No estaba claro quién creaba qué. | `Order` crea sus `LineItem`, siguiendo el principio de agregación. |
| **Controller** | La lógica de la UI y del dominio estaban mezcladas en `Order`. | `OrderController` maneja la petición y delega en el dominio. |
| **Low Coupling** | `Order` estaba fuertemente acoplado a la lógica de pago. | `Order` no sabe nada de pagos. `PaymentProcessor` y `PaymentMethod` están débilmente acoplados. |
| **High Cohesion** | `Order` tenía responsabilidades de pedido, cálculo, pago, etc. (baja cohesión). | Cada clase tiene un propósito único y enfocado (alta cohesión). |
| **Polymorphism** | Un bloque `if/elif` gigante para los tipos de pago. | Interfaz `PaymentMethod` con implementaciones concretas. |
| **Pure Fabrication** | La lógica de orquestación del pago estaba sin hogar, forzada dentro de `Order`. | `PaymentProcessor` es creado para albergar esta lógica. |
| **Indirection** | La lógica de pago llamaba directamente a una API de pasarela específica. | Se introduce `PaymentGateway` para desacoplar de la implementación concreta. |
| **Protected Variations**| Cualquier cambio en la API de pago requería modificar la clase `Order`. | El patrón Adapter (`StripeGateway`) protege al resto del sistema de cambios en la API externa. |

---