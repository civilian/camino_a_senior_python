# GRASP

Claro que sí. Prepárate para una inmersión profunda en GRASP. Esto no es solo una lista de patrones; es una filosofía de diseño orientada a objetos que, una vez internalizada, cambia fundamentalmente la forma en que piensas sobre el código y la asignación de responsabilidades. Dominar esto es un pilar fundamental para alcanzar la seniority.

---

# Guía Profunda de GRASP para el Desarrollador Senior

## ¿Qué es GRASP y por qué es crucial para la Seniority?

GRASP son las siglas de **General Responsibility Assignment Software Patterns** (Patrones Generales de Asignación de Responsabilidades de Software). Fueron documentados por Craig Larman en su influyente libro *"Applying UML and Patterns: An Introduction to Object-Oriented Analysis and Design and Iterative Development"*.

A diferencia de los patrones de diseño del "Gang of Four" (GoF), que ofrecen soluciones a problemas de diseño recurrentes (ej. Singleton, Factory, Observer), GRASP no son soluciones concretas. Son **principios o heurísticas fundamentales** que te guían en la decisión más importante del Diseño Orientado a Objetos (OOD): **¿Qué objeto debe ser responsable de qué?**

Un desarrollador junior puede implementar un patrón Factory. Un desarrollador senior entiende *por qué* la responsabilidad de la creación de objetos se aisló en esa Factory, y puede justificar esa decisión usando los principios de GRASP como **Creator**, **Low Coupling** y **High Cohesion**. GRASP es el "porqué" detrás de muchas decisiones de diseño.

> **Citación Clave:** "El diseño orientado a objetos se trata fundamentalmente de asignar responsabilidades a los objetos." - Craig Larman, *Applying UML and Patterns*.

## Los 9 Principios de GRASP

Vamos a desglosar cada uno de los nueve principios. Los primeros cinco son los más fundamentales, y los últimos cuatro son más específicos y avanzados.

---

### Los Fundamentales

#### 1. Information Expert (Experto en Información)

-   **Pregunta Clave:** ¿A quién se le asigna una responsabilidad?
-   **Solución:** Asigna la responsabilidad a la clase que tiene la **información necesaria** para cumplirla.

**Explicación Profunda:**
Este es el principio más importante y fundamental de GRASP. Guía la colocación de responsabilidades basándose en la proximidad de los datos. Si una clase necesita calcular un total, y esa clase contiene todos los elementos y sus precios, esa clase es la "Experta en Información" y debe tener el método `calcularTotal()`.

Hacer lo contrario (que otra clase pida los datos, los procese y devuelva el resultado) viola la encapsulación y aumenta el acoplamiento, ya que la clase externa ahora depende de la estructura interna de la clase experta. El Experto en Información promueve la encapsulación y conduce naturalmente a una alta cohesión.

> **Citación de Larman:** "Assign a responsibility to the information expert—the class that has the information necessary to fulfill the responsibility." (Larman, C. 2004. *Applying UML and Patterns*, 3rd ed. Prentice Hall, p. 299).

**Ejemplo (Java):**

Imagina un sistema de ventas. Tenemos una clase `Venta` que contiene una lista de `LineaDeVenta`. Cada `LineaDeVenta` tiene una cantidad y una referencia a un `Producto` con un precio.

**MAL (Sin Experto en Información):** Una clase `CalculadoraTotal` que pide los datos.

```java
// MAL: Esta clase rompe la encapsulación y aumenta el acoplamiento.
public class CalculadoraTotal {
    public double calcular(Venta venta) {
        double total = 0;
        // Pide los datos internos de 'venta'
        for (LineaDeVenta linea : venta.getLineasDeVenta()) {
            // Pide los datos internos de 'linea'
            Producto producto = linea.getProducto();
            total += producto.getPrecio() * linea.getCantidad();
        }
        return total;
    }
}
```

**BIEN (Aplicando Experto en Información):**

```java
public class Producto {
    private double precio;
    // ... getters
}

public class LineaDeVenta {
    private int cantidad;
    private Producto producto;

    // LineaDeVenta es experta en su propio subtotal
    public double getSubtotal() {
        return producto.getPrecio() * cantidad;
    }
    // ...
}

public class Venta {
    private List<LineaDeVenta> lineasDeVenta;

    // Venta es la experta en el total, ya que conoce todas sus líneas.
    // Delega el cálculo del subtotal a la experta en ello: LineaDeVenta.
    public double getTotal() {
        double total = 0;
        for (LineaDeVenta linea : lineasDeVenta) {
            total += linea.getSubtotal(); // ¡Colaboración de expertos!
        }
        return total;
    }
    // ...
}
```
En el buen ejemplo, cada objeto es responsable de lo que conoce. Esto reduce dependencias y hace el sistema más fácil de mantener.

---

#### 2. Creator (Creador)

-   **Pregunta Clave:** ¿Quién debe ser responsable de crear una nueva instancia de una clase?
-   **Solución:** Asigna a la clase B la responsabilidad de crear una instancia de la clase A si una o más de las siguientes condiciones son verdaderas:
    -   B "contiene" o agrega objetos de A.
    -   B registra instancias de A.
    -   B usa de cerca objetos de A.
    -   B tiene los datos de inicialización para A.

**Explicación Profunda:**
Este patrón busca encontrar el creador más lógico para un objeto, lo que mantiene bajo el acoplamiento. Si una `Venta` está compuesta por `LineaDeVenta`s, es natural que la `Venta` sea la responsable de crear esas `LineaDeVenta`s. Esto se alinea con el principio de Experto en Información: la `Venta` tiene el contexto para crear sus propias líneas.

Este patrón es la base de patrones GoF como **Factory Method** y **Abstract Factory**, que son implementaciones más sofisticadas del principio Creator.

**Ejemplo (C#):**

```csharp
// Venta es el "agregado raíz" y contiene LineasDeVenta.
public class Venta
{
    private List<LineaDeVenta> _lineas = new List<LineaDeVenta>();
    public IReadOnlyList<LineaDeVenta> Lineas => _lineas.AsReadOnly();

    // Venta es la CREADORA de LineaDeVenta porque la "contiene" y tiene
    // la información necesaria (producto y cantidad) para crearla.
    public void AgregarProducto(Producto producto, int cantidad)
    {
        // La creación ocurre aquí, dentro de la clase que la va a contener.
        var nuevaLinea = new LineaDeVenta(producto, cantidad);
        _lineas.Add(nuevaLinea);
    }
}

public class LineaDeVenta
{
    public Producto Producto { get; private set; }
    public int Cantidad { get; private set; }

    // El constructor es usado por su Creador (Venta).
    public LineaDeVenta(Producto producto, int cantidad)
    {
        Producto = producto;
        Cantidad = cantidad;
    }
}
```

---

#### 3. Controller (Controlador)

-   **Pregunta Clave:** ¿Quién debe recibir y coordinar una "operación del sistema"?
-   **Solución:** Asigna la responsabilidad a una clase que represente uno de los siguientes:
    1.  El sistema en general (un "Controlador de Fachada", ej. `SistemaDeVentas`).
    2.  Un escenario de caso de uso (un "Controlador de Caso de Uso", ej. `ProcesarVentaHandler`).

**Explicación Profunda:**
Este patrón desacopla la capa de UI (o la capa de entrega en general, como una API) del modelo de dominio. La UI no debe contener lógica de negocio. En su lugar, delega las peticiones a un objeto Controlador. El Controlador recibe la petición, localiza la información necesaria en el modelo de dominio, invoca los métodos apropiados y coordina la respuesta.

Esto evita el "bloat" en las clases de la UI y permite que el modelo de dominio sea reutilizable con diferentes interfaces. Es la base de arquitecturas como **MVC (Model-View-Controller)**, **MVP (Model-View-Presenter)** y **MVVM (Model-View-ViewModel)**.

**Ejemplo (Conceptual - Python/Flask):**

```python
# Modelo de Dominio (domain_model.py)
class VentaService:
    def crear_nueva_venta(self, datos_cliente):
        # Lógica de negocio para crear una venta...
        print("Venta creada en el dominio.")
        return {"status": "ok", "venta_id": 123}

# Capa de Controlador (controllers.py)
class VentaController:
    def __init__(self, venta_service: VentaService):
        self._venta_service = venta_service

    # Este método recibe la petición y la coordina.
    def procesar_peticion_crear_venta(self, request_data):
        # 1. Recibe la petición (de la UI/API).
        # 2. Delega el trabajo al modelo de dominio.
        resultado = self._venta_service.crear_nueva_venta(request_data['cliente'])
        # 3. Prepara la respuesta para la UI/API.
        return {"http_status": 201, "body": resultado}

# Capa de UI/API (app.py - Flask)
from flask import Flask, request
from domain_model import VentaService
from controllers import VentaController

app = Flask(__name__)
venta_service = VentaService()
venta_controller = VentaController(venta_service)

@app.route('/ventas', methods=['POST'])
def crear_venta_endpoint():
    # La UI/API solo sabe de su controlador, no de la lógica de negocio.
    # Es delgada y solo se encarga de la interacción.
    datos = request.get_json()
    respuesta = venta_controller.procesar_peticion_crear_venta(datos)
    return respuesta['body'], respuesta['http_status']
```

---

#### 4. Low Coupling (Bajo Acoplamiento)

-   **Pregunta Clave:** ¿Cómo reducir el impacto del cambio?
-   **Solución:** Asigna responsabilidades de manera que el acoplamiento (dependencia entre clases) permanezca bajo.

**Explicación Profunda:**
Este es un principio evaluativo, un objetivo a alcanzar. El acoplamiento es una medida de cuán fuertemente está conectada una clase a otra. Un alto acoplamiento es problemático porque:
-   Un cambio en una clase puede forzar cambios en otras clases (efecto dominó).
-   Es más difícil entender una clase de forma aislada.
-   La reutilización de una clase es más difícil porque requiere arrastrar todas sus dependencias.

El **Experto en Información** promueve el bajo acoplamiento. El uso de **interfaces** en lugar de clases concretas es una técnica clave para lograrlo.

> **Citación:** "Coupling is a measure of how strongly one element is connected to, has knowledge of, or relies on other elements." (Larman, C. 2004. *Applying UML and Patterns*, 3rd ed. Prentice Hall, p. 285).

**Ejemplo (Java):**

**MAL (Alto Acoplamiento):** La clase `CajaRegistradora` depende directamente de una clase concreta `ImpresoraFiscalEpson`.

```java
public class ImpresoraFiscalEpson {
    public void imprimirTicket(String texto) {
        // Lógica específica para impresoras Epson...
        System.out.println("EPSON PRINTER: " + texto);
    }
}

public class CajaRegistradora {
    private ImpresoraFiscalEpson impresora = new ImpresoraFiscalEpson(); // ¡Acoplamiento fuerte!

    public void finalizarVenta(double total) {
        impresora.imprimirTicket("Total: " + total);
    }
}
```
Si mañana cambiamos a una impresora HP, tenemos que modificar la clase `CajaRegistradora`.

**BIEN (Bajo Acoplamiento):** Depender de una abstracción (interfaz).

```java
// Abstracción
public interface ImpresoraFiscal {
    void imprimirTicket(String texto);
}

// Implementaciones concretas
public class ImpresoraFiscalEpson implements ImpresoraFiscal {
    @Override
    public void imprimirTicket(String texto) { /* ... */ }
}

public class ImpresoraFiscalHP implements ImpresoraFiscal {
    @Override
    public void imprimirTicket(String texto) { /* ... */ }
}

public class CajaRegistradora {
    // Depende de la interfaz, no de la implementación.
    private final ImpresoraFiscal impresora;

    // La dependencia se inyecta (Dependency Injection)
    public CajaRegistradora(ImpresoraFiscal impresora) {
        this.impresora = impresora;
    }

    public void finalizarVenta(double total) {
        impresora.imprimirTicket("Total: " + total);
    }
}
```
Ahora `CajaRegistradora` no sabe qué impresora específica está usando. Podemos cambiar de impresora sin tocar su código. Esto se relaciona directamente con el principio de Inversión de Dependencias (la 'D' de SOLID).

---

#### 5. High Cohesion (Alta Cohesión)

-   **Pregunta Clave:** ¿Cómo mantener los objetos enfocados, comprensibles y manejables?
-   **Solución:** Asigna responsabilidades de manera que la cohesión permanezca alta.

**Explicación Profunda:**
La cohesión es una medida de cuán relacionadas y enfocadas están las responsabilidades de una clase.
-   **Alta Cohesión (Deseable):** La clase tiene un conjunto pequeño de responsabilidades altamente relacionadas (ej. una clase `ConexionBD` que solo maneja la conexión, apertura y cierre de la base de datos).
-   **Baja Cohesión (Problemático):** La clase hace muchas cosas no relacionadas (ej. una clase `Utilidades` que lee ficheros, formatea fechas, envía emails y calcula impuestos). A esto se le llama un "God Object" o "Blob".

La baja cohesión hace que las clases sean difíciles de entender, mantener y reutilizar. El **Experto en Información** naturalmente promueve la alta cohesión.

**Ejemplo (Conceptual):**

**MAL (Baja Cohesión):**

```
class GestorDeTodo {
    + conectarBD()
    + ejecutarQuery(sql)
    + generarPDF(datos)
    + enviarEmail(destinatario, asunto, cuerpo)
    + validarFormulario(form)
    + parsearXML(xmlString)
}
```
Esta clase es un desastre de mantenimiento.

**BIEN (Alta Cohesión):**

```
class RepositorioDeUsuarios {
    + conectarBD()
    + buscarUsuario(id)
    + guardarUsuario(usuario)
}

class GeneradorDeReportesPDF {
    + generar(datos)
}

class ServicioDeNotificaciones {
    + enviarEmail(destinatario, asunto, cuerpo)
}
```
Cada clase tiene un propósito claro y único.

---

### Los Avanzados

Estos patrones se usan para resolver problemas más complejos que surgen al aplicar los cinco primeros.

#### 6. Polymorphism (Polimorfismo)

-   **Pregunta Clave:** ¿Cómo manejar variaciones basadas en el tipo? ¿Cómo crear componentes conectables ("pluggable")?
-   **Solución:** Cuando un comportamiento relacionado varía según el tipo (clase), asigna la responsabilidad de ese comportamiento a los tipos para los que varía, usando operaciones polimórficas.

**Explicación Profunda:**
En lugar de usar condicionales (`if/else` o `switch`) para cambiar el comportamiento basado en el tipo de un objeto, usa polimorfismo. Define una interfaz o una clase base con un método, y deja que cada subclase implemente ese método de manera diferente.

Esto elimina los condicionales, reduce el acoplamiento y hace que el sistema sea extensible. Añadir un nuevo tipo no requiere modificar el código existente, solo añadir una nueva clase que implemente la interfaz. Esto es una manifestación directa del **Principio Abierto/Cerrado** (la 'O' de SOLID).

**Ejemplo (C#):**

**MAL (Sin Polimorfismo):**

```csharp
public enum TipoDeCuenta { Corriente, Ahorro, Inversion }

public class CalculadoraDeIntereses
{
    // ¡Este switch es una señal de alarma!
    public decimal Calcular(CuentaBancaria cuenta)
    {
        switch (cuenta.Tipo)
        {
            case TipoDeCuenta.Corriente:
                return 0; // Sin interés
            case TipoDeCuenta.Ahorro:
                return cuenta.Saldo * 0.01m;
            case TipoDeCuenta.Inversion:
                return cuenta.Saldo * 0.05m;
            default:
                throw new Exception("Tipo de cuenta no soportado");
        }
    }
}
```
Si añadimos un nuevo tipo de cuenta, hay que modificar esta clase.

**BIEN (Con Polimorfismo):**

```csharp
public abstract class CuentaBancaria
{
    public decimal Saldo { get; protected set; }
    public abstract decimal CalcularInteres(); // Operación polimórfica
}

public class CuentaCorriente : CuentaBancaria
{
    public override decimal CalcularInteres() => 0;
}

public class CuentaDeAhorro : CuentaBancaria
{
    public override decimal CalcularInteres() => Saldo * 0.01m;
}

public class CuentaDeInversion : CuentaBancaria
{
    public override decimal CalcularInteres() => Saldo * 0.05m;
}

// El cliente no necesita saber el tipo concreto.
public class Banco
{
    public void PagarIntereses(List<CuentaBancaria> cuentas)
    {
        foreach (var cuenta in cuentas)
        {
            // No hay if/switch. Simplemente se invoca el método.
            decimal interes = cuenta.CalcularInteres();
            // ... pagar interés
        }
    }
}
```

---

#### 7. Pure Fabrication (Fabricación Pura)

-   **Pregunta Clave:** ¿Qué objeto debería tener la responsabilidad cuando el **Experto en Información** conduce a un mal diseño (baja cohesión, alto acoplamiento)?
-   **Solución:** Crea una clase artificial que no representa un concepto del dominio del problema, y asígnale un conjunto de responsabilidades cohesivas.

**Explicación Profunda:**
A veces, seguir el Experto en Información al pie de la letra nos llevaría a poner una responsabilidad en una clase del dominio que no encaja bien. Por ejemplo, ¿quién es responsable de guardar un objeto `Venta` en la base de datos? La clase `Venta` tiene la información (es la Experta), pero mezclar lógica de negocio con lógica de persistencia (SQL, ORM) daría como resultado una **baja cohesión** y un **alto acoplamiento** con la infraestructura de la base de datos.

La solución es una **Fabricación Pura**: inventamos una clase que no existe en el mundo real, como `VentaRepository` o `VentaDAO`. Esta clase es altamente cohesiva (solo se encarga de la persistencia de Ventas) y mantiene el modelo de dominio limpio y desacoplado de la infraestructura. Los patrones **Repository** y **Service** son ejemplos clásicos de Fabricaciones Puras.

> **Citación:** "A Pure Fabrication is a class that does not represent a concept in the problem domain, specially made up to achieve low coupling, high cohesion, and the reuse potential thereof." (Larman, C. 2004. *Applying UML and Patterns*, 3rd ed. Prentice Hall, p. 435).

**Ejemplo (Java):**

```java
// Clase del dominio, pura, sin conocimiento de la persistencia.
public class Venta {
    // ... atributos y lógica de negocio
}

// FABRICACIÓN PURA: No existe el concepto de "repositorio" en una tienda real.
// Es una clase inventada para lograr un buen diseño.
public class VentaRepository {
    private final DataSource dataSource;

    public VentaRepository(DataSource dataSource) {
        this.dataSource = dataSource;
    }

    // Alta cohesión: solo se encarga de la persistencia de Ventas.
    public void guardar(Venta venta) {
        // Lógica para guardar la venta en la base de datos...
    }

    public Venta buscarPorId(int id) {
        // Lógica para buscar la venta en la base de datos...
        return null;
    }
}
```

---

#### 8. Indirection (Indirección)

-   **Pregunta Clave:** ¿Cómo evitar el acoplamiento directo entre dos o más elementos? ¿Cómo desacoplarlos?
-   **Solución:** Asigna la responsabilidad a un objeto intermediario para que medie entre otros componentes o servicios.

**Explicación Profunda:**
La indirección es un principio fundamental en software para reducir el acoplamiento. En lugar de que A hable directamente con B, A habla con un intermediario I, que a su vez habla con B. Esto desacopla A de B. Si B cambia, solo I necesita ser actualizado, no A.

Muchos patrones de software se basan en la indirección:
-   **Controller** es una indirección entre la UI y el modelo.
-   **Adapter** es una indirección para adaptar una interfaz a otra.
-   **Facade** es una indirección que simplifica un subsistema complejo.
-   **Proxy** es una indirección para controlar el acceso a un objeto.

**Ejemplo (C#):** Usando un **Adapter** como indirección.

Imagina que tu sistema de E-commerce usa la API de Stripe para procesar pagos, pero quieres poder cambiar a PayPal en el futuro.

```csharp
// Interfaz de nuestro sistema (estable)
public interface IPasarelaDePago
{
    bool RealizarPago(decimal monto, string numeroTarjeta);
}

// INDIRECCIÓN (Adapter): Acopla nuestro sistema a la API externa.
public class StripeAdapter : IPasarelaDePago
{
    private readonly StripeApi _stripeApi; // API de un tercero

    public StripeAdapter(StripeApi stripeApi) { _stripeApi = stripeApi; }

    public bool RealizarPago(decimal monto, string numeroTarjeta)
    {
        // Traduce la llamada de nuestro sistema a la llamada específica de Stripe.
        return _stripeApi.Charge(monto, numeroTarjeta);
    }
}

// Nuestro código de negocio solo conoce la interfaz.
public class ServicioDeCheckout
{
    private readonly IPasarelaDePago _pasarela;

    public ServicioDeCheckout(IPasarelaDePago pasarela) { _pasarela = pasarela; }

    public void ProcesarOrden()
    {
        // ...
        _pasarela.RealizarPago(100.00m, "1234...");
    }
}
```
El `StripeAdapter` es el intermediario. Si cambiamos a PayPal, solo creamos un `PayPalAdapter` y lo inyectamos en `ServicioDeCheckout` sin cambiar una sola línea de este último.

---

#### 9. Protected Variations (Variaciones Protegidas)

-   **Pregunta Clave:** ¿Cómo diseñar objetos y sistemas para que las variaciones o inestabilidades en ciertos elementos no impacten a otros?
-   **Solución:** Identifica los puntos de variación o inestabilidad predecibles y asigna responsabilidades para crear una interfaz estable a su alrededor.

**Explicación Profunda:**
Este principio es la motivación detrás de muchos mecanismos y patrones. Es el "porqué" del **Polimorfismo**, la **Indirección**, y el **Principio Abierto/Cerrado**. La idea es encapsular la parte que es probable que cambie detrás de una interfaz que sea improbable que cambie.

Ejemplos de puntos de variación:
-   APIs de terceros (sistemas de pago, envío de emails).
-   Formatos de datos (JSON, XML, BSON).
-   Reglas de negocio que cambian con frecuencia (impuestos, descuentos).
-   Tecnología de persistencia (SQL Server, PostgreSQL, MongoDB).

El patrón **Polymorphism** protege al cliente del algoritmo específico. El patrón **Indirection** (como el Adapter) protege al sistema de la API específica de un tercero.

> **Citación:** "Identify points of predicted variation or instability; assign responsibilities to create a stable interface around them." (Larman, C. 2004. *Applying UML and Patterns*, 3rd ed. Prentice Hall, p. 445).

Este principio te obliga a pensar como un arquitecto: **"¿Qué es lo más probable que cambie en este sistema en el futuro?"** y luego a construir barreras (interfaces) para proteger el resto del sistema de esos cambios.

## Conclusión: El Camino a la Seniority con GRASP

Dominar GRASP no es memorizar nueve nombres. Es internalizar una forma de razonar sobre el diseño de software. Cuando te enfrentes a una nueva funcionalidad, tu mente de "senior" debería empezar a hacerse estas preguntas de forma automática:

1.  **¿Quién es el experto en información aquí?** (Information Expert) -> Esto te da un punto de partida para colocar la lógica de negocio.
2.  **¿Esto pertenece a una clase del dominio o estoy mezclando responsabilidades?** (High Cohesion) -> Si la respuesta es "mezclando", entonces...
3.  **¿Debería crear una clase nueva para esto?** (Pure Fabrication) -> Como un `Repository` o un `Service`.
4.  **¿Quién debería crear este nuevo objeto?** (Creator) -> Probablemente la clase que lo va a contener o usar.
5.  **¿Cómo se activará esta lógica desde el exterior (UI, API)?** (Controller) -> Necesito un punto de entrada que desacople la presentación del dominio.
6.  **¿Estoy dependiendo de una clase concreta que podría cambiar?** (Low Coupling) -> Si es así, necesito una interfaz.
7.  **¿Este "algo" que podría cambiar es un punto de variación predecible?** (Protected Variations) -> Si es así, la interfaz es obligatoria.
8.  **¿Estoy usando `if/else` basados en el tipo de un objeto?** -> Debería usar **Polymorphism**.
9.  **¿Necesito desacoplar estos dos componentes?** -> Quizás necesite un intermediario (**Indirection**).

Cuando puedes justificar tus decisiones de diseño usando este vocabulario y estos principios, no solo estás escribiendo código; estás **diseñando software de manera deliberada y profesional**. Esa es la verdadera marca de un desarrollador senior.
