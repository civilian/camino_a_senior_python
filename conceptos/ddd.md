# DDD

Claro que sí. Prepárate para una inmersión profunda en Domain-Driven Design (DDD). Esto no es solo un tutorial, es una guía de estudio diseñada para cambiar tu forma de pensar sobre el software, que es el verdadero salto hacia la senioridad.

# Guía Profunda de Domain-Driven Design (DDD) para Desarrolladores Senior

## Introducción: ¿Qué es DDD y por qué debería importarte?

Domain-Driven Design no es un framework, ni una tecnología. Es una **filosofía y un conjunto de prácticas para diseñar software que modela un dominio de negocio complejo**. Su objetivo principal es gestionar la complejidad inherente a los grandes sistemas de software.

Un desarrollador junior ve el software como una serie de operaciones CRUD (Crear, Leer, Actualizar, Borrar) sobre una base de datos. Un desarrollador senior entiende que el software es una **representación viva y útil de un proceso de negocio**. DDD es el puente que te lleva de la primera visión a la segunda.

La obra seminal es el libro de Eric Evans:

> "The heart of software is its ability to solve domain-related problems for its user. All other features, vital as they may be, support this basic purpose. When the domain is complex, this is a difficult task. This book is about how to make it easier."
> — **Eric Evans, *Domain-Driven Design: Tackling Complexity in the Heart of Software* (2003)**

---

## Parte I: El Pensamiento Estratégico (The Big Picture)

Aquí es donde DDD brilla y donde se distingue un verdadero practicante. Los patrones estratégicos se centran en el panorama general, en cómo dividir un sistema masivo en partes manejables y coherentes.

### 1. Ubiquitous Language (Lenguaje Ubicuo)

Este es el pilar fundamental de DDD. Sin él, todo lo demás se desmorona.

*   **¿Qué es?** Un lenguaje compartido, riguroso y sin ambigüedades, desarrollado en colaboración por el equipo de desarrollo y los expertos del dominio (los stakeholders, usuarios, analistas de negocio). Este lenguaje se utiliza en **todas las conversaciones, diagramas, documentos y, lo más importante, en el código**.
*   **¿Por qué es crucial?** Elimina la "traducción". El analista no habla de "Prospectos de Venta" para que el desarrollador lo implemente como una clase `Customer` con un `status = 'potential'`. Si el negocio lo llama "Prospecto", en el código existe una clase `Prospecto`.
*   **Ejemplo:** En un dominio de logística, no dices "el ítem se mueve". Dices: "el `Paquete` es `Despachado` desde el `Almacén` de origen y entra en `Tránsito` hacia el `Centro de Distribución`". Cada uno de esos sustantivos y verbos en negrita debería corresponder a un concepto o método en tu código.

> "Use the model as the backbone of a language. Commit the team to exercising that language relentlessly in all communication within the team and in the code."
> — **Eric Evans, *Domain-Driven Design* (2003)**

### 2. Bounded Context (Contexto Delimitado)

Un sistema grande no tiene un único modelo. Tiene varios. El Bounded Context es la frontera explícita dentro de la cual un modelo de dominio particular es consistente y aplicable.

*   **¿Qué es?** Un límite conceptual (p. ej., un microservicio, un módulo) donde un término específico del Lenguaje Ubicuo tiene un significado único y bien definido.
*   **¿Por qué es crucial?** Permite la autonomía de los equipos y la claridad del modelo. La palabra "Cliente" significa cosas muy diferentes en contextos distintos:
    *   **Contexto de Ventas:** Un `Cliente` tiene historial de compras, potencial de venta, y está asociado a un `Vendedor`.
    *   **Contexto de Soporte:** Un `Cliente` tiene tickets de soporte, historial de incidencias, y un nivel de servicio (SLA).
    *   **Contexto de Facturación:** Un `Cliente` tiene datos fiscales, métodos de pago y facturas pendientes.
*   Intentar crear una única clase `Cliente` "monstruo" para satisfacer a todos estos contextos es una receta para el desastre. DDD te dice: **no lo hagas**. Crea modelos separados y coherentes dentro de sus propios Bounded Contexts.

### 3. Context Map (Mapa de Contextos)

Un Mapa de Contextos es la forma de visualizar y documentar las relaciones entre diferentes Bounded Contexts. Es una herramienta de nivel de arquitectura.

*   **¿Qué es?** Un diagrama que muestra los Bounded Contexts y las relaciones entre ellos. No es opcional; es esencial para entender cómo fluye la información y el poder en el sistema.
*   **Patrones de Relación Comunes:**
    *   **Partnership (Asociación):** Dos equipos/contextos colaboran estrechamente. El éxito de uno depende del otro.
    *   **Shared Kernel (Núcleo Compartido):** Dos contextos comparten una pequeña parte del modelo (y el código). Debe usarse con mucho cuidado, ya que crea un acoplamiento fuerte.
    *   **Customer-Supplier (Cliente-Proveedor):** Un contexto (el "downstream") consume los servicios de otro (el "upstream"). El equipo upstream tiene poder sobre el downstream.
    *   **Conformist (Conformista):** Un contexto downstream se adhiere ciegamente al modelo del upstream. No hay espacio para la negociación. Típico cuando se integra con un sistema heredado o de un tercero.
    *   **Anticorruption Layer (ACL - Capa Anticorrupción):** El patrón más defensivo y útil. El contexto downstream crea una capa de traducción explícita que aísla su modelo interno del modelo del sistema upstream. Esto protege tu modelo de ser "corrompido" por modelos externos.
    *   **Open Host Service (OHS - Servicio de Host Abierto):** El contexto upstream define un protocolo público y bien documentado (como una API REST) para que otros contextos se integren.
    *   **Separate Ways (Caminos Separados):** Los contextos no se integran en absoluto. A veces, la integración es más costosa que la duplicación manual de datos.

### 4. Subdominios (Core, Supporting, Generic)

No todas las partes de tu negocio son igual de importantes. DDD te ayuda a enfocar tus esfuerzos.

*   **Core Domain (Dominio Principal):** Esta es la parte del negocio que te da una ventaja competitiva. Aquí es donde debes aplicar DDD con todo su rigor. Es el "corazón del software". Aquí inviertes a tus mejores desarrolladores.
*   **Supporting Subdomain (Subdominio de Soporte):** Lógica de negocio necesaria para que el negocio funcione, pero que no es una ventaja competitiva. Puede ser desarrollada internamente, pero con menos rigor que el Core Domain.
*   **Generic Subdomain (Subdominio Genérico):** Problemas ya resueltos que no son específicos de tu negocio (p. ej., autenticación, envío de emails). La mejor estrategia aquí es **comprar una solución, no construirla**.

---

## Parte II: Los Bloques de Construcción Tácticos (The Building Blocks)

Estos son los patrones que aplicas **dentro de un Bounded Context** para crear un modelo de dominio rico y expresivo.

### 1. Entities (Entidades)

*   **Definición:** Objetos que tienen una **identidad** que perdura a lo largo del tiempo y a través de cambios en sus atributos. No se definen por sus propiedades, sino por quiénes son.
*   **Ejemplo:** Una `Persona` es una entidad. Su nombre o dirección pueden cambiar, pero sigue siendo la misma persona. Su identidad (p. ej., un DNI o un UUID) es lo que la define.
*   **Clave:** La identidad debe ser gestionada cuidadosamente a lo largo de todo el ciclo de vida del objeto.

### 2. Value Objects (Objetos de Valor)

*   **Definición:** Objetos que describen una característica o un atributo. No tienen identidad conceptual. Se definen por la **combinación de sus valores**.
*   **Características Clave:**
    *   **Inmutabilidad:** Una vez creados, no pueden ser modificados. Si necesitas un cambio, creas una nueva instancia (`dinero.add(otroDinero)` devuelve un *nuevo* objeto `Dinero`, no modifica el original).
    *   **Igualdad Estructural:** Dos Value Objects son iguales si todos sus atributos son iguales.
    *   **Autovalidación:** Un Value Object no debería poder existir en un estado inválido (p. ej., un objeto `EmailAddress` se valida en su constructor).
*   **Ejemplo:** `Dinero` (compuesto por `cantidad` y `divisa`), `Dirección` (compuesto por `calle`, `ciudad`, `códigoPostal`), un rango de fechas. Usar `string` para un email o `decimal` para dinero es un "code smell". Crea un Value Object.

> "Many objects have no conceptual identity. These objects describe characteristics of a thing. [...] An object that represents a descriptive aspect of the domain with no conceptual identity is called a VALUE OBJECT."
> — **Eric Evans, *Domain-Driven Design* (2003)**

### 3. Aggregates (Agregados)

Este es uno de los conceptos más difíciles y poderosos de DDD.

*   **Definición:** Un clúster de entidades y objetos de valor que se tratan como una única unidad para los cambios de datos. Es una **barrera de consistencia transaccional**.
*   **Componentes:**
    *   **Aggregate Root (Raíz del Agregado):** Una entidad específica dentro del agregado que actúa como el único punto de entrada. Los objetos externos solo pueden hacer referencia a la raíz.
    *   **Límite (Boundary):** El límite del agregado define qué está dentro y qué está fuera.
*   **Reglas de Oro:**
    1.  **Acceso Único a través de la Raíz:** El código cliente solo puede interactuar con el Aggregate Root. Nunca puede modificar directamente una entidad interna del agregado.
    2.  **Referencias por ID:** Un agregado puede hacer referencia a otro agregado, pero **solo a través de su identidad (ID)**, nunca con una referencia directa al objeto. Esto es CRUCIAL para evitar agregados gigantes y mantener los límites de consistencia claros.
    3.  **Consistencia Transaccional:** Cualquier operación sobre el agregado debe cumplir todas sus invariantes (reglas de negocio) dentro de una única transacción. La consistencia entre agregados es, por lo general, **eventual**.
*   **Ejemplo:** Una `OrdenDeCompra` es un Aggregate Root. Contiene una lista de `LineaDeOrden` (que son entidades locales) y una `DireccionDeEnvio` (un Value Object). No puedes añadir una `LineaDeOrden` directamente; tienes que llamar a `orden.agregarLinea(...)`. La `OrdenDeCompra` se asegura de que el total se recalcule y que no se exceda un límite de crédito.

### 4. Repositories (Repositorios)

*   **Definición:** Un objeto que media entre el dominio y la capa de persistencia (base de datos). Proporciona una **interfaz de tipo colección** para acceder a los Aggregate Roots.
*   **Propósito:** Abstraer la complejidad de la persistencia. El modelo de dominio no sabe si los datos vienen de SQL, NoSQL o un archivo de texto.
*   **Reglas:**
    *   Debe haber un repositorio por cada Aggregate Root.
    *   La interfaz del repositorio se define en la capa de dominio, pero la implementación está en la capa de infraestructura (esto es el Principio de Inversión de Dependencias en acción).
    *   Los métodos del repositorio deben hablar el Lenguaje Ubicuo (p. ej., `findOverdueInvoices()` en lugar de `findByStatusAndDate(...)`).

### 5. Factories (Fábricas) y Services (Servicios)

*   **Factories:** Cuando la creación de un objeto (especialmente un Agregado) es compleja y no es responsabilidad de un simple constructor, se utiliza una Factory. Encapsula la lógica de creación.
*   **Domain Services (Servicios de Dominio):** A veces, una operación importante del dominio no encaja naturalmente en ninguna entidad u objeto de valor. Un servicio de dominio es un objeto **sin estado** que implementa esta lógica.
    *   **Ejemplo:** Un servicio que calcula la mejor ruta de envío para un paquete, tomando como entrada varios `Almacenes` y `PolíticasDeEnvío`. La lógica es compleja y no pertenece a un solo almacén.

### 6. Domain Events (Eventos de Dominio)

*   **Definición:** Un objeto que representa algo que **ha sucedido** en el dominio y que es de interés para otras partes del sistema (posiblemente en otros Bounded Contexts).
*   **Características:**
    *   Son inmutables y se nombran en tiempo pasado (p. ej., `PedidoRealizado`, `ContraseñaCambiada`).
    *   Son el mecanismo principal para lograr la **consistencia eventual** entre agregados y Bounded Contexts.
*   **Ejemplo:** Cuando una `OrdenDeCompra` se paga, dispara un evento `OrdenPagada`. El Bounded Context de Envíos puede suscribirse a este evento para iniciar el proceso de despacho, sin que el contexto de Facturación necesite conocerlo directamente.

---

## Parte III: Arquitectura y DDD

DDD no prescribe una arquitectura única, pero se beneficia enormemente de arquitecturas que aíslan el dominio.

### 1. Layered Architecture (Arquitectura en Capas)

La arquitectura clásica propuesta por Evans.

*   **User Interface (UI):** Responsable de la presentación.
*   **Application Layer (Capa de Aplicación):** Orquesta las tareas. No contiene lógica de negocio. Llama a los repositorios para obtener agregados, invoca métodos en ellos y los vuelve a guardar. Aquí viven los *Casos de Uso*.
*   **Domain Layer (Capa de Dominio):** El corazón del software. Contiene las Entidades, Value Objects, Agregados, Servicios de Dominio y las interfaces de los Repositorios.
*   **Infrastructure Layer (Capa de Infraestructura):** La implementación de todo lo externo: persistencia (implementación de repositorios), envío de emails, llamadas a APIs externas, etc.

**Regla de Dependencia:** Las capas superiores solo pueden depender de las capas inferiores. La capa de Dominio no sabe nada de la base de datos ni de la UI.

### 2. Hexagonal Architecture (Ports and Adapters)

Una evolución de la arquitectura en capas, más flexible.

*   **Core (El Hexágono):** Contiene la lógica de aplicación y de dominio. No tiene dependencias con el mundo exterior.
*   **Ports (Puertos):** Son las APIs del core (p. ej., interfaces de repositorio, interfaces de servicios de aplicación). Definen cómo se puede interactuar con el core.
*   **Adapters (Adaptadores):** Son la implementación de los puertos. Conectan el core con el mundo exterior.
    *   **Driving Adapters:** Inician la interacción (p. ej., un controlador de API REST, un consumidor de colas de mensajes).
    *   **Driven Adapters:** Son invocados por el core (p. ej., una implementación de repositorio para PostgreSQL, un cliente de una API externa).

Esta arquitectura hace que el dominio sea agnóstico a la tecnología y altamente testeable.

### 3. CQRS (Command Query Responsibility Segregation)

Un patrón que encaja perfectamente con DDD.

*   **Principio:** Segregar las operaciones que cambian el estado (**Commands**) de las que leen el estado (**Queries**).
*   **Lado de Escritura (Commands):** Utiliza el modelo de dominio rico de DDD (Agregados, Entidades) para procesar los comandos y garantizar la consistencia.
*   **Lado de Lectura (Queries):** Utiliza un modelo de datos optimizado para las consultas (p. ej., vistas materializadas, DTOs planos). Puede saltarse completamente el modelo de dominio para obtener los datos de la forma más eficiente posible.
*   **¿Por qué es útil?** Los requerimientos para escribir datos (consistencia, validación) son muy diferentes de los requerimientos para leerlos (rendimiento, flexibilidad). CQRS permite optimizar cada lado de forma independiente.

### 4. Event Sourcing

Un patrón avanzado que lleva los Domain Events al siguiente nivel.

*   **Principio:** En lugar de guardar el estado actual de una entidad, se guarda la **secuencia completa de eventos** que la han llevado a ese estado. El estado actual se reconstruye reproduciendo los eventos.
*   **Ventajas:**
    *   Auditoría completa y gratuita.
    *   Capacidad de depurar y analizar el sistema en cualquier punto del tiempo.
    *   Flexibilidad para crear nuevas proyecciones de lectura (modelos de query) a partir de los eventos existentes.
*   **Desventajas:** Es conceptualmente más complejo y requiere una infraestructura diferente.

---

## El Salto a la Senioridad: El Cambio de Mentalidad

Saber las definiciones no te hace senior. Aplicar la filosofía, sí.

1.  **Enamórate del Problema, no de la Solución:** Un desarrollador senior con mentalidad DDD pasa más tiempo entendiendo el negocio que escribiendo código. El código es un subproducto de un buen modelo.
2.  **El Código es un Diálogo Continuo:** El Lenguaje Ubicuo y el modelo no se definen una vez y se olvidan. Se refinan constantemente a medida que el equipo aprende más sobre el dominio. Esto se llama **Model Discovery** y es un proceso iterativo.
3.  **La Colaboración es Obligatoria:** DDD no es algo que un programador pueda hacer solo en su rincón. Requiere una colaboración intensa y continua con los expertos del dominio.
4.  **Piensa en Comportamiento, no en Datos:** No diseñes tus clases pensando en las tablas de la base de datos. Diseña tus objetos pensando en las **responsabilidades, invariantes y comportamientos** que representan en el mundo real. Un `Anemic Domain Model` (clases con solo getters y setters) es un anti-patrón de DDD.
5.  **Los Límites son tus Amigos:** Aprende a amar los Bounded Contexts y los Aggregates. La habilidad de un arquitecto senior no reside en conectar todo, sino en saber **dónde trazar las líneas** para mantener la complejidad bajo control.

> "The model is not the UML diagrams. The model is not the code. The model is not the documents. The model is the idea in people's heads. The diagrams and the code are expressions of the model."
> — **Vaughn Vernon, *Implementing Domain-Driven Design* (2013)**

## Lecturas Recomendadas para Profundizar

1.  **Eric Evans - *Domain-Driven Design: Tackling Complexity in the Heart of Software* (El "Libro Azul"):** La biblia. Denso, pero fundamental.
2.  **Vaughn Vernon - *Implementing Domain-Driven Design* (El "Libro Rojo"):** Mucho más práctico y orientado a la implementación, con ejemplos de código. Una guía excelente para aplicar las ideas de Evans.
3.  **Vaughn Vernon - *Domain-Driven Design Distilled* (El "Libro Verde"):** Una introducción concisa y accesible. Ideal para empezar.
4.  **Martin Fowler - [Bliki sobre DDD](https://martinfowler.com/tags/domain%20driven%20design.html):** Artículos y resúmenes de alta calidad sobre los conceptos clave.

Dominar DDD es un viaje, no un destino. Empieza aplicando un Value Object donde antes usabas un tipo primitivo. Intenta identificar los Agregados en tu próximo feature. Dibuja un Context Map de tu sistema actual. Cada paso te acercará a pensar y construir software de una manera más robusta, mantenible y alineada con el negocio que le da vida.
