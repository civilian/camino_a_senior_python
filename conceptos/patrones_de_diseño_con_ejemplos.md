¿Alguna vez te has encontrado codificando una solución y pensando "tiene que haber un nombre para este problema, una forma estándar de resolverlo"?

Esa intuición es el primer paso para pensar como un arquitecto de software.
Resulta que ese "vocabulario" de soluciones no solo existe, sino que está a nuestro alcance para construir sistemas más robustos y elegantes.

# patrones de diseño con ejemplos

***

# Guía Maestra de Patrones de Diseño: De Programador a Arquitecto de Software

## 1. Introducción Profunda: El Nacimiento de un Lenguaje Común

Imagínate ser un arquitecto de edificios en un mundo sin un vocabulario compartido. Cada vez que quieres describir un "arco", una "columna" o una "viga", tienes que explicar el concepto desde cero. Sería ineficiente, propenso a errores y limitaría enormemente la complejidad de lo que podrías construir. A finales de los 80 y principios de los 90, la ingeniería de software se encontraba en una crisis similar.

**Contexto Histórico: ¿Quién, Cuándo, Dónde y Por Qué?**

El concepto no nació en el vacío. Su inspiración proviene de la arquitectura civil. El arquitecto **Christopher Alexander**, en su libro de 1977, *A Pattern Language: Towns, Buildings, Construction*, propuso la idea de que los problemas de diseño comunes en nuestro entorno físico tienen soluciones recurrentes y probadas, a las que llamó "patrones".

> "Cada patrón describe un problema que ocurre una y otra vez en nuestro entorno, y luego describe el núcleo de la solución a ese problema, de tal manera que puedes usar esta solución un millón de veces, sin hacerlo nunca de la misma manera dos veces." — **Christopher Alexander**, *A Pattern Language: Towns, Buildings, Construction* (1977)

Este concepto resonó en la comunidad de programación orientada a objetos (OO), que luchaba con la creciente complejidad del software. Programadores como Kent Beck y Ward Cunningham comenzaron a aplicar las ideas de Alexander al desarrollo de software en el lenguaje Smalltalk.

El momento decisivo llegó en 1994 con la publicación del libro **"Design Patterns: Elements of Reusable Object-Oriented Software"**. Sus autores, Erich Gamma, Richard Helm, Ralph Johnson y John Vlissides, serían inmortalizados como la **"Gang of Four" (GoF)**. Este libro no inventó los patrones, sino que los catalogó, les dio un nombre y un formato estandarizado, creando un lenguaje común para todos los desarrolladores.

**El Problema que Resuelve: La Tiranía de la Complejidad**

A medida que los sistemas de software crecían, los desarrolladores se enfrentaban a problemas recurrentes:
*   ¿Cómo crear objetos sin acoplar el cliente a clases concretas?
*   ¿Cómo añadir funcionalidades a un objeto dinámicamente sin usar herencia masiva?
*   ¿Cómo permitir que objetos dispares colaboren sin conocerse entre sí?
*   ¿Cómo encapsular un algoritmo para que sea intercambiable?

Los patrones de diseño ofrecen soluciones probadas, elegantes y reutilizables para estos y otros problemas. No son código que se copia y pega, sino **recetas o planos** para resolver un problema de diseño en un contexto particular. Son la sabiduría colectiva de la comunidad de software, destilada en 23 soluciones arquetípicas.

**Evolución: De un Catálogo a un Ecosistema**

Desde 1994, el concepto ha evolucionado drásticamente:
*   **Expansión:** El catálogo original de 23 patrones de la GoF se ha expandido. Han surgido patrones específicos para la concurrencia, sistemas distribuidos, microservicios (p. ej., Circuit Breaker, Saga), y programación funcional.
*   **Crítica y Refinamiento:** La comunidad ha aprendido que los patrones no son balas de plata. El uso excesivo ("Pattern-itis") puede llevar a una complejidad innecesaria. Algunos patrones, como el Singleton, son ahora considerados por muchos como anti-patrones en ciertos contextos.
*   **Integración en Lenguajes y Frameworks:** Muchos lenguajes y frameworks modernos incorporan patrones de diseño directamente en su núcleo. El patrón Observer es la base de casi todos los sistemas de eventos en GUI (React, Vue) y backend (Node.js EventEmitter). El patrón Iterator está integrado en los bucles `for...of` de muchos lenguajes.

Hoy, entender los patrones de diseño no es solo conocer un catálogo, es entender los principios fundamentales del buen diseño de software.

## 2. Fundamentos Teóricos: Los Pilares Invisibles

Los patrones de diseño no son trucos de magia; se sustentan en décadas de investigación en ciencias de la computación y principios de ingeniería de software.

**Base Teórica: Abstracción y Composición**

En su núcleo, la mayoría de los patrones de diseño son una manifestación de dos de los pilares más importantes de la computación:
1.  **Abstracción:** Ocultar la complejidad de la implementación detrás de una interfaz simple. Un patrón como **Facade** es la abstracción en su forma más pura.
2.  **Composición sobre Herencia:** Un principio fundamental del diseño OO. En lugar de construir funcionalidades heredando de una clase base (una relación "es un"), se construyen ensamblando objetos más pequeños (una relación "tiene un"). Patrones como **Strategy**, **Decorator** y **Composite** son ejemplos canónicos de este principio.

> "Programa hacia una interfaz, no hacia una implementación." — **Erich Gamma et al.**, *Design Patterns: Elements of Reusable Object-Oriented Software* (1994)

Esta famosa cita del libro de la GoF es la esencia de por qué los patrones funcionan. Al depender de abstracciones (interfaces o clases base abstractas) en lugar de clases concretas, creamos sistemas flexibles, desacoplados y extensibles.

**Principios Subyacentes: S.O.L.I.D.**

Los patrones de diseño son la encarnación práctica de los principios de diseño de software. Los más famosos son los principios SOLID, acuñados por Robert C. Martin:

*   **(S) Principio de Responsabilidad Única (SRP):** Una clase debe tener una, y solo una, razón para cambiar. Patrones como **Facade** y **Proxy** ayudan a separar responsabilidades.
*   **(O) Principio Abierto/Cerrado (OCP):** Las entidades de software deben estar abiertas a la extensión, pero cerradas a la modificación. El patrón **Strategy** es el ejemplo perfecto: puedes añadir nuevos algoritmos (estrategias) sin modificar el contexto que los utiliza.
*   **(L) Principio de Sustitución de Liskov (LSP):** Los subtipos deben ser sustituibles por sus tipos base sin alterar la corrección del programa. Los patrones que dependen de la herencia, como **Template Method**, se basan fundamentalmente en este principio.
*   **(I) Principio de Segregación de Interfaces (ISP):** Ningún cliente debe ser forzado a depender de métodos que no utiliza. El patrón **Adapter** puede ayudar a adaptar una interfaz grande a una más pequeña y específica que el cliente necesita.
*   **(D) Principio de Inversión de Dependencia (DIP):** Los módulos de alto nivel no deben depender de los de bajo nivel. Ambos deben depender de abstracciones. Este es el principio central que habilita la mayoría de los patrones. El patrón **Factory Method** y los frameworks de Inyección de Dependencia son implementaciones directas de este principio.

**Relación con Otros Conceptos**

Los patrones son un puente entre los principios abstractos (como SOLID) y el código concreto. Se relacionan con la historia de la computación al ser una evolución natural de la búsqueda de la reutilización de código, un viaje que comenzó con las subrutinas en los años 50, pasó por los módulos en los 70 y llegó a su apogeo con la programación orientada a objetos en los 80 y 90.

## 3. Evolución Histórica Detallada

| Fecha       | Hito                                                               | Figuras Clave                  | Contexto Histórico                                                                                               |
|-------------|--------------------------------------------------------------------|--------------------------------|------------------------------------------------------------------------------------------------------------------|
| **1977**    | Publicación de "A Pattern Language"                                | Christopher Alexander          | La arquitectura civil busca formas de codificar el conocimiento de diseño.                                       |
| **1987**    | Kent Beck y Ward Cunningham aplican las ideas de Alexander a Smalltalk | Kent Beck, Ward Cunningham     | La programación orientada a objetos (Smalltalk, C++) gana popularidad. La complejidad del software aumenta.      |
| **1991**    | Erich Gamma presenta su tesis doctoral sobre patrones de diseño      | Erich Gamma                    | La comunidad académica de OO comienza a formalizar la idea de patrones.                                          |
| **1994**    | **Publicación de "Design Patterns: Elements of Reusable OO Software"** | **Gang of Four (GoF)**         | **El Big Bang.** El libro se convierte en un best-seller y establece un vocabulario estándar para los desarrolladores. |
| **Finales 90s** | Auge de Java y los "J2EE Patterns"                                 | Sun Microsystems, varios autores | La industria adopta masivamente Java para aplicaciones empresariales, creando la necesidad de patrones a gran escala. |
| **2002**    | Martin Fowler publica "Patterns of Enterprise Application Architecture" | Martin Fowler                  | Se extiende el concepto de patrones más allá de los objetos individuales a la arquitectura de sistemas completos. |
| **2010s**   | Patrones para nuevas arquitecturas (Microservicios, Cloud)         | Netflix, Google, Amazon        | El auge de la nube y los sistemas distribuidos crea nuevos problemas recurrentes que requieren nuevos patrones.      |
| **Presente**| Los patrones son un concepto maduro, integrado en el ADN del software | Toda la comunidad de software  | Se enseñan en universidades, se usan en entrevistas y son una parte fundamental del día a día de un desarrollador. |

## 4. Implementación Práctica en Python

Vamos a explorar tres patrones fundamentales de cada categoría de la GoF: Creacional, Estructural y Comportamental. Usaremos Python por su claridad y expresividad.

### 4.1 Patrón Creacional: Factory Method (Método de Fábrica)

**Analogía:** Imagina una empresa de logística. El cliente no necesita saber si su paquete irá en un camión, un barco o un avión. Solo le dice a la empresa "envía esto de A a B", y la empresa (la fábrica) elige el transporte adecuado según las necesidades (distancia, peso, etc.).

**Problema que resuelve:** Permite que una clase delegue la creación de objetos a sus subclases. Esto desacopla el código cliente de las clases concretas que necesita instanciar.

**Caso de Estudio: Un sistema de exportación de documentos**

Nuestro sistema necesita exportar datos a diferentes formatos (JSON, XML).

**El Mal Camino (Antes): Acoplamiento Fuerte**

```python
# mal_ejemplo.py
import json
import xml.etree.ElementTree as et

class DocumentExporter:
    def export(self, data, format_type):
        if format_type == 'json':
            # Lógica de exportación a JSON
            print("Exportando a JSON...")
            return json.dumps(data)
        elif format_type == 'xml':
            # Lógica de exportación a XML
            print("Exportando a XML...")
            root = et.Element('data')
            for key, value in data.items():
                child = et.Element(key)
                child.text = str(value)
                root.append(child)
            return et.tostring(root, encoding='unicode')
        else:
            raise ValueError(f"Formato desconocido: {format_type}")

# Código cliente
data = {"name": "Alice", "age": 30}
exporter = DocumentExporter()
json_output = exporter.export(data, 'json')
xml_output = exporter.export(data, 'xml')

# ¿Qué pasa si queremos añadir PDF? ¡Tenemos que modificar la clase DocumentExporter!
# Esto viola el Principio Abierto/Cerrado.
```

**El Buen Camino (Después): Usando Factory Method**

```python
# buen_ejemplo_factory.py
from abc import ABC, abstractmethod
import json
import xml.etree.ElementTree as et

# 1. La Interfaz del Producto (Exporter)
class Exporter(ABC):
    @abstractmethod
    def export(self, data: dict) -> str:
        pass

# 2. Productos Concretos
class JSONExporter(Exporter):
    def export(self, data: dict) -> str:
        print("Usando el exportador JSON...")
        return json.dumps(data)

class XMLExporter(Exporter):
    def export(self, data: dict) -> str:
        print("Usando el exportador XML...")
        root = et.Element('data')
        for key, value in data.items():
            child = et.Element(key)
            child.text = str(value)
            root.append(child)
        return et.tostring(root, encoding='unicode')

# 3. La Interfaz del Creador (La Fábrica)
class ExporterFactory(ABC):
    @abstractmethod
    def get_exporter(self) -> Exporter:
        """Este es el "Factory Method"."""
        pass

    def export_data(self, data: dict) -> str:
        """El código cliente usa esta clase, no los exportadores concretos."""
        exporter = self.get_exporter()
        return exporter.export(data)

# 4. Creadores Concretos
class JSONExporterFactory(ExporterFactory):
    def get_exporter(self) -> Exporter:
        return JSONExporter()

class XMLExporterFactory(ExporterFactory):
    def get_exporter(self) -> Exporter:
        return XMLExporter()

# Código cliente
def client_code(factory: ExporterFactory, data: dict):
    result = factory.export_data(data)
    print(f"Resultado de la exportación:\n{result}\n")

data_to_export = {"name": "Bob", "role": "Developer"}
client_code(JSONExporterFactory(), data_to_export)
client_code(XMLExporterFactory(), data_to_export)

# ¡Ahora podemos añadir un exportador de PDF sin tocar el código existente!
class PDFExporter(Exporter):
    def export(self, data: dict) -> str:
        print("Usando el exportador PDF...")
        return f"PDF_CONTENT_FOR_{data['name']}"

class PDFExporterFactory(ExporterFactory):
    def get_exporter(self) -> Exporter:
        return PDFExporter()

client_code(PDFExporterFactory(), data_to_export)
```
**Resultado:** El código cliente ahora depende de una abstracción (`ExporterFactory`) y no de las clases concretas. Hemos cumplido el Principio de Inversión de Dependencia y el Principio Abierto/Cerrado.

### 4.2 Patrón Estructural: Decorator (Decorador)

**Analogía:** Piensa en una taza de café. La base es el café solo. Puedes "decorarlo" con leche, luego con azúcar, luego con canela. Cada "decorador" añade una nueva funcionalidad (sabor y costo) sin cambiar el café original.

**Problema que resuelve:** Permite añadir responsabilidades a un objeto de forma dinámica. Es una alternativa flexible a la herencia para extender la funcionalidad.

**Caso de Estudio: Un sistema de notificaciones**

Tenemos un sistema que envía notificaciones. Queremos poder enviar notificaciones por múltiples canales (Email, SMS, Slack) de forma combinada.

**El Mal Camino (Antes): Explosión de Clases con Herencia**

Si usamos herencia, necesitaríamos clases como `EmailNotifier`, `SMSNotifier`, `EmailAndSMSNotifier`, `EmailAndSMSAndSlackNotifier`... ¡Esto es insostenible!

**El Buen Camino (Después): Usando Decorator**

```python
# buen_ejemplo_decorator.py
from abc import ABC, abstractmethod

# 1. La Interfaz del Componente
class Notifier(ABC):
    @abstractmethod
    def send(self, message: str):
        pass

# 2. El Componente Concreto (la base)
class EmailNotifier(Notifier):
    def send(self, message: str):
        print(f"Enviando por Email: '{message}'")

# 3. El Decorador Base (mantiene la misma interfaz)
class BaseDecorator(Notifier):
    def __init__(self, wrapped: Notifier):
        self._wrapped = wrapped

    def send(self, message: str):
        self._wrapped.send(message)

# 4. Decoradores Concretos
class SMSDecorator(BaseDecorator):
    def send(self, message: str):
        super().send(message) # Llama al objeto envuelto primero
        print(f"Enviando por SMS: '{message}'")

class SlackDecorator(BaseDecorator):
    def send(self, message: str):
        super().send(message)
        print(f"Enviando por Slack: '{message}'")

# Código cliente
message = "¡El sistema estará en mantenimiento a las 2 AM!"

# Enviar solo por email
print("--- Notificación simple ---")
simple_notifier = EmailNotifier()
simple_notifier.send(message)

# Enviar por Email y SMS
print("\n--- Notificación Email + SMS ---")
email_sms_notifier = SMSDecorator(EmailNotifier())
email_sms_notifier.send(message)

# Enviar por Email, SMS y Slack
print("\n--- Notificación Email + SMS + Slack ---")
full_notifier = SlackDecorator(SMSDecorator(EmailNotifier()))
full_notifier.send(message)
```
**Resultado:** Podemos combinar funcionalidades en tiempo de ejecución de cualquier manera que queramos, envolviendo un objeto en múltiples decoradores. Esto sigue el principio de Composición sobre Herencia.

### 4.3 Patrón Comportamental: Strategy (Estrategia)

**Analogía:** Cuando viajas al aeropuerto, puedes elegir una estrategia: ir en taxi (caro pero rápido), en autobús (barato pero lento) o en tu propio coche (costo intermedio, flexible). El objetivo es el mismo (llegar al aeropuerto), pero el algoritmo (la estrategia) es intercambiable.

**Problema que resuelve:** Define una familia de algoritmos, encapsula cada uno de ellos y los hace intercambiables. Permite que el algoritmo varíe independientemente de los clientes que lo utilizan.

**Caso de Estudio: Un sistema de ordenación de datos**

Necesitamos ordenar una lista de elementos, pero queremos poder cambiar el algoritmo de ordenación (rápido, por nombre, por fecha, etc.) en tiempo de ejecución.

**El Mal Camino (Antes): Lógica Condicional**

```python
# mal_ejemplo_strategy.py
class DataSorter:
    def sort(self, data: list, strategy: str):
        print(f"Ordenando con la estrategia: {strategy}")
        if strategy == 'quick_sort':
            # Lógica de quick sort
            return sorted(data)
        elif strategy == 'bubble_sort':
            # Lógica de bubble sort (simulada)
            print("Usando bubble sort (lento)...")
            return sorted(data)
        elif strategy == 'reverse':
            # Lógica de orden inverso
            return sorted(data, reverse=True)
        else:
            raise ValueError("Estrategia no válida")

# Código cliente
sorter = DataSorter()
my_data = [3, 1, 4, 1, 5, 9, 2, 6]
sorted_data = sorter.sort(my_data, 'quick_sort')
# Para añadir un nuevo algoritmo, hay que modificar la clase DataSorter.
# ¡Violación del Principio Abierto/Cerrado!
```

**El Buen Camino (Después): Usando Strategy**

```python
# buen_ejemplo_strategy.py
from abc import ABC, abstractmethod
from typing import List

# 1. La Interfaz de la Estrategia
class SortStrategy(ABC):
    @abstractmethod
    def sort(self, data: List) -> List:
        pass

# 2. Estrategias Concretas
class QuickSortStrategy(SortStrategy):
    def sort(self, data: List) -> List:
        print("Estrategia: Quick Sort")
        return sorted(data)

class ReverseOrderStrategy(SortStrategy):
    def sort(self, data: List) -> List:
        print("Estrategia: Orden Inverso")
        return sorted(data, reverse=True)

class BubbleSortStrategy(SortStrategy):
    def sort(self, data: List) -> List:
        print("Estrategia: Bubble Sort (simulado, para demostrar flexibilidad)")
        # Aquí iría una implementación real de bubble sort
        return sorted(data)

# 3. El Contexto (la clase que usa la estrategia)
class SorterContext:
    def __init__(self, strategy: SortStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: SortStrategy):
        self._strategy = strategy

    def execute_sort(self, data: List) -> List:
        print("Contexto: Ejecutando la ordenación.")
        result = self._strategy.sort(data)
        print(f"Resultado: {result}")
        return result

# Código cliente
data_to_sort = [5, 2, 8, 1, 9, 4]

# Usar Quick Sort
quick_sort = QuickSortStrategy()
context = SorterContext(quick_sort)
context.execute_sort(data_to_sort)

print("-" * 20)

# Cambiar la estrategia en tiempo de ejecución a Orden Inverso
reverse_sort = ReverseOrderStrategy()
context.set_strategy(reverse_sort)
context.execute_sort(data_to_sort)
```
**Resultado:** El `SorterContext` no conoce los detalles de ningún algoritmo de ordenación. Solo sabe que tiene un objeto que cumple con la interfaz `SortStrategy`. Podemos añadir nuevos algoritmos creando nuevas clases de estrategia sin modificar el contexto en absoluto.

### 4.4 Patrón Creacional: Builder (Constructor)

**Analogía:** Cuando pides una hamburguesa personalizada en un restaurante, no recibes de golpe un objeto "hamburguesa completa". Dices: "quiero pan, luego la carne, luego queso, sin cebolla, con extra de salsa". El empleado (el director) usa una receta paso a paso (el builder) para construirla. Al final dices "entrégame la hamburguesa" y la recibes completa.

**Problema que resuelve:** Permite construir objetos complejos paso a paso. Separa la construcción de un objeto de su representación, de modo que el mismo proceso de construcción puede crear diferentes representaciones.

**Caso de Estudio: Construcción de consultas SQL**

Queremos construir consultas SQL complejas de forma legible y flexible, sin concatenar strings manualmente.

**El Mal Camino (Antes): Constructores con demasiados parámetros**

```python
# mal_ejemplo_builder.py

class QueryBuilder:
    def build_query(self, table, columns=None, where=None,
                    order_by=None, limit=None, joins=None):
        # Un constructor con 6 parámetros opcionales es una "Telescoping Constructor"
        # Es difícil de leer y propenso a errores al llamarlo
        query = f"SELECT {', '.join(columns) if columns else '*'} FROM {table}"
        if joins:
            for join in joins:
                query += f" JOIN {join}"
        if where:
            query += f" WHERE {where}"
        if order_by:
            query += f" ORDER BY {order_by}"
        if limit:
            query += f" LIMIT {limit}"
        return query

# Código cliente: ¿qué significa cada argumento?
q = QueryBuilder().build_query("users", ["id", "name"], "age > 18",
                               "name ASC", 10, ["orders ON users.id = orders.user_id"])
print(q)
```

**El Buen Camino (Después): Usando Builder**

```python
# buen_ejemplo_builder.py
from __future__ import annotations

# 1. El Builder
class QueryBuilder:
    def __init__(self, table: str):
        self._table = table
        self._columns: list[str] = ["*"]
        self._joins: list[str] = []
        self._where: str | None = None
        self._order_by: str | None = None
        self._limit: int | None = None

    def select(self, *columns: str) -> QueryBuilder:
        self._columns = list(columns)
        return self  # Devuelve self para permitir encadenamiento (fluent interface)

    def join(self, join_clause: str) -> QueryBuilder:
        self._joins.append(join_clause)
        return self

    def where(self, condition: str) -> QueryBuilder:
        self._where = condition
        return self

    def order_by(self, column: str) -> QueryBuilder:
        self._order_by = column
        return self

    def limit(self, count: int) -> QueryBuilder:
        self._limit = count
        return self

    def build(self) -> str:
        """Paso final: construye y devuelve el objeto (la query)."""
        query = f"SELECT {', '.join(self._columns)} FROM {self._table}"
        for join in self._joins:
            query += f" JOIN {join}"
        if self._where:
            query += f" WHERE {self._where}"
        if self._order_by:
            query += f" ORDER BY {self._order_by}"
        if self._limit:
            query += f" LIMIT {self._limit}"
        return query

# Código cliente: legible como prosa
query = (
    QueryBuilder("users")
    .select("users.id", "users.name", "orders.total")
    .join("orders ON users.id = orders.user_id")
    .where("users.age > 18")
    .order_by("users.name ASC")
    .limit(10)
    .build()
)
print(query)
# SELECT users.id, users.name, orders.total FROM users
# JOIN orders ON users.id = orders.user_id
# WHERE users.age > 18
# ORDER BY users.name ASC
# LIMIT 10
```
**Resultado:** Cada paso de construcción es claro y nombrado. Podemos construir consultas simples o complejas con el mismo builder. La interfaz fluida (método encadenado que devuelve `self`) hace el código casi legible como lenguaje natural.

---

### 4.5 Patrón Creacional: Singleton

**Analogía:** El presidente de un país. No importa cuántas veces preguntes "¿quién es el presidente?", siempre obtienes la misma persona, no se crea un presidente nuevo cada vez.

**Problema que resuelve:** Garantiza que una clase tenga una única instancia y proporciona un punto de acceso global a ella. Útil para gestores de configuración, pools de conexiones de base de datos o sistemas de logging.

**Caso de Estudio: Gestor de configuración de aplicación**

```python
# buen_ejemplo_singleton.py
import threading

class AppConfig:
    _instance: "AppConfig | None" = None
    _lock: threading.Lock = threading.Lock()

    def __new__(cls) -> "AppConfig":
        # Double-checked locking: seguro en entornos multihilo
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:  # Segunda comprobación tras adquirir el lock
                    print("Creando la única instancia de AppConfig...")
                    cls._instance = super().__new__(cls)
                    cls._instance._settings = {}
        return cls._instance

    def set(self, key: str, value) -> None:
        self._settings[key] = value

    def get(self, key: str, default=None):
        return self._settings.get(key, default)

# Código cliente
config1 = AppConfig()
config1.set("DB_HOST", "localhost")

config2 = AppConfig()
print(config2.get("DB_HOST"))  # "localhost" — ambos apuntan al mismo objeto
print(config1 is config2)       # True
```

> **Advertencia senior:** El Singleton es el patrón más controvertido del catálogo GoF. Facilita la introducción de estado global implícito, lo que dificulta el testing (no se puede inyectar un mock fácilmente) y crea acoplamiento oculto. En la mayoría de los casos modernos, se prefiere la **Inyección de Dependencias** con un contenedor que gestione el ciclo de vida de la instancia.

---

### 4.6 Patrón Estructural: Adapter (Adaptador)

**Analogía:** Un enchufe de viaje. Tu portátil americano tiene un clavija de tipo A, pero el enchufe europeo es de tipo C. El adaptador no cambia el enchufe de la pared ni el de tu portátil; simplemente traduce entre ambos.

**Problema que resuelve:** Permite que interfaces incompatibles trabajen juntas. Convierte la interfaz de una clase en otra que el cliente espera. Es especialmente útil cuando integras librerías de terceros o código legado.

**Caso de Estudio: Integrar una librería de pagos externa**

Nuestra aplicación usa una interfaz `PaymentProcessor`. Debemos integrar un servicio externo (`StripeAPI`) que tiene una interfaz totalmente diferente.

```python
# buen_ejemplo_adapter.py

# --- Lo que nuestra aplicación espera (la interfaz estándar) ---
from abc import ABC, abstractmethod

class PaymentProcessor(ABC):
    @abstractmethod
    def pay(self, amount: float, currency: str) -> bool:
        pass

# --- La librería externa (no podemos modificarla) ---
class StripeAPI:
    """Clase de terceros con una interfaz incompatible."""
    def create_charge(self, amount_in_cents: int, currency_code: str,
                      source: str = "tok_visa") -> dict:
        print(f"[Stripe] Procesando cargo: {amount_in_cents} centavos de {currency_code}")
        return {"status": "succeeded", "id": "ch_abc123"}

# --- El Adaptador: traduce nuestra interfaz a la de Stripe ---
class StripeAdapter(PaymentProcessor):
    def __init__(self, stripe_api: StripeAPI):
        self._stripe = stripe_api

    def pay(self, amount: float, currency: str) -> bool:
        # Traduce: nuestra interfaz espera euros, Stripe espera centavos
        amount_in_cents = int(amount * 100)
        result = self._stripe.create_charge(amount_in_cents, currency.upper())
        return result.get("status") == "succeeded"

# --- Código cliente: solo conoce PaymentProcessor ---
def checkout(processor: PaymentProcessor, total: float):
    success = processor.pay(total, "eur")
    if success:
        print("Pago completado con éxito.")
    else:
        print("El pago falló.")

stripe_client = StripeAPI()
adapter = StripeAdapter(stripe_client)
checkout(adapter, 49.99)
# [Stripe] Procesando cargo: 4999 centavos de EUR
# Pago completado con éxito.
```
**Resultado:** El código cliente usa `PaymentProcessor` y no sabe nada de Stripe. Si mañana cambiamos a PayPal, solo creamos un `PayPalAdapter` y no tocamos el resto de la aplicación.

---

### 4.7 Patrón Estructural: Facade (Fachada)

**Analogía:** El panel de control de un avión tiene miles de sistemas complejos detrás (hidráulico, eléctrico, combustible). El piloto interactúa con una interfaz simplificada (la cabina) que oculta toda esa complejidad. La fachada es la cabina.

**Problema que resuelve:** Proporciona una interfaz simplificada a un conjunto de interfaces complejas en un subsistema. Reduce la dependencia del código externo de los detalles internos del subsistema.

**Caso de Estudio: Sistema de procesamiento de pedidos e-commerce**

Un pedido implica coordinar inventario, pagos y notificaciones. Sin una fachada, el código cliente tiene que conocer y orquestar todos estos subsistemas.

```python
# buen_ejemplo_facade.py

# --- Subsistemas complejos ---
class InventoryService:
    def check_stock(self, product_id: str, qty: int) -> bool:
        print(f"[Inventario] Verificando stock de '{product_id}' ({qty} unidades)...")
        return True  # Simulado

    def reserve(self, product_id: str, qty: int) -> None:
        print(f"[Inventario] Reservando {qty}x '{product_id}'.")

class PaymentService:
    def charge(self, user_id: str, amount: float) -> bool:
        print(f"[Pagos] Cobrando €{amount:.2f} al usuario '{user_id}'...")
        return True  # Simulado

class NotificationService:
    def send_confirmation(self, user_id: str, order_id: str) -> None:
        print(f"[Notif.] Email de confirmación enviado a '{user_id}' (pedido {order_id}).")

class ShippingService:
    def schedule(self, order_id: str, address: str) -> str:
        tracking = f"TRACK-{order_id[:8].upper()}"
        print(f"[Envío] Pedido {order_id} programado para '{address}'. Tracking: {tracking}")
        return tracking

# --- La Fachada: orquesta todos los subsistemas ---
import uuid

class OrderFacade:
    def __init__(self):
        self._inventory = InventoryService()
        self._payment = PaymentService()
        self._notification = NotificationService()
        self._shipping = ShippingService()

    def place_order(self, user_id: str, product_id: str,
                    qty: int, amount: float, address: str) -> str | None:
        """Interfaz simplificada para completar un pedido."""
        if not self._inventory.check_stock(product_id, qty):
            print("Error: sin stock.")
            return None

        if not self._payment.charge(user_id, amount):
            print("Error: pago rechazado.")
            return None

        order_id = str(uuid.uuid4())
        self._inventory.reserve(product_id, qty)
        tracking = self._shipping.schedule(order_id, address)
        self._notification.send_confirmation(user_id, order_id)

        print(f"\nPedido {order_id} completado. Tracking: {tracking}")
        return order_id

# --- Código cliente: una sola llamada en lugar de coordinar 4 servicios ---
facade = OrderFacade()
facade.place_order(
    user_id="user_42",
    product_id="python-book-gof",
    qty=1,
    amount=39.99,
    address="Calle Mayor 1, Madrid"
)
```
**Resultado:** El cliente hace una llamada a `place_order` y la fachada se encarga de todo. Los subsistemas siguen existiendo y son accesibles directamente si se necesitan, pero la fachada ofrece el camino más simple para el caso de uso más común.

---

### 4.8 Patrón Comportamental: Observer (Observador)

**Analogía:** Suscribirse a un canal de YouTube. El canal (el *sujeto*) no sabe cuántos suscriptores tiene ni qué harán cuando llegue una notificación. Cada suscriptor (el *observador*) decide por sí mismo qué hacer cuando recibe el aviso de nuevo vídeo.

**Problema que resuelve:** Define una dependencia uno-a-muchos entre objetos, de modo que cuando un objeto cambia de estado, todos sus dependientes son notificados y actualizados automáticamente. Es la base de casi todos los sistemas de eventos.

**Caso de Estudio: Sistema de alertas de precio de producto**

Los usuarios pueden suscribirse a un producto. Cuando el precio baja, todos reciben una notificación según su canal preferido.

```python
# buen_ejemplo_observer.py
from abc import ABC, abstractmethod

# 1. La interfaz del Observador
class PriceObserver(ABC):
    @abstractmethod
    def update(self, product: str, new_price: float) -> None:
        pass

# 2. El Sujeto (el que emite eventos)
class Product:
    def __init__(self, name: str, price: float):
        self.name = name
        self._price = price
        self._observers: list[PriceObserver] = []

    def subscribe(self, observer: PriceObserver) -> None:
        self._observers.append(observer)

    def unsubscribe(self, observer: PriceObserver) -> None:
        self._observers.remove(observer)

    def _notify(self) -> None:
        for observer in self._observers:
            observer.update(self.name, self._price)

    @property
    def price(self) -> float:
        return self._price

    @price.setter
    def price(self, new_price: float) -> None:
        if new_price < self._price:
            print(f"\n[Producto] '{self.name}' bajó de €{self._price} a €{new_price}. Notificando...")
            self._price = new_price
            self._notify()
        else:
            self._price = new_price

# 3. Observadores Concretos
class EmailAlert(PriceObserver):
    def __init__(self, email: str):
        self._email = email

    def update(self, product: str, new_price: float) -> None:
        print(f"  [Email → {self._email}] ¡Alerta! '{product}' ahora cuesta €{new_price:.2f}")

class PushNotification(PriceObserver):
    def __init__(self, device_id: str):
        self._device = device_id

    def update(self, product: str, new_price: float) -> None:
        print(f"  [Push → {self._device}] '{product}' bajó a €{new_price:.2f} 🎉")

# 4. Código cliente
laptop = Product("MacBook Pro M4", 2499.00)

alice = EmailAlert("alice@example.com")
bob = PushNotification("device_bob_iphone")
carol = EmailAlert("carol@example.com")

laptop.subscribe(alice)
laptop.subscribe(bob)
laptop.subscribe(carol)

laptop.price = 1999.00  # Notifica a todos
laptop.unsubscribe(carol)
laptop.price = 1799.00  # Notifica solo a Alice y Bob
```
**Resultado:** El objeto `Product` no conoce los detalles de sus suscriptores, solo sabe que implementan `PriceObserver`. Podemos añadir o quitar observadores en tiempo de ejecución sin tocar el sujeto. Este patrón es la base de sistemas de eventos, buses de mensajes y frameworks reactivos.

---

### 4.9 Patrón Comportamental: Command (Comando)

**Analogía:** Un control remoto. Cada botón encapsula una acción (subir volumen, cambiar canal). El control remoto no sabe cómo funciona el televisor internamente; solo sabe que puede "ejecutar" comandos. Además, si tienes un botón de deshacer, puedes revertir el último comando ejecutado.

**Problema que resuelve:** Encapsula una solicitud como un objeto, lo que permite parametrizar clientes con diferentes solicitudes, encolar o registrar solicitudes y soportar operaciones que se pueden deshacer (undo/redo).

**Caso de Estudio: Editor de texto con historial de deshacer**

```python
# buen_ejemplo_command.py
from abc import ABC, abstractmethod

# 1. La interfaz del Comando
class Command(ABC):
    @abstractmethod
    def execute(self) -> None:
        pass

    @abstractmethod
    def undo(self) -> None:
        pass

# 2. El Receptor (el objeto que sabe cómo hacer el trabajo)
class TextEditor:
    def __init__(self):
        self._text = ""

    def insert(self, text: str) -> None:
        self._text += text

    def delete(self, count: int) -> None:
        self._text = self._text[:-count]

    def get_text(self) -> str:
        return self._text

# 3. Comandos Concretos
class InsertTextCommand(Command):
    def __init__(self, editor: TextEditor, text: str):
        self._editor = editor
        self._text = text

    def execute(self) -> None:
        self._editor.insert(self._text)

    def undo(self) -> None:
        self._editor.delete(len(self._text))

class DeleteTextCommand(Command):
    def __init__(self, editor: TextEditor, count: int):
        self._editor = editor
        self._count = count
        self._deleted: str = ""

    def execute(self) -> None:
        self._deleted = self._editor.get_text()[-self._count:]
        self._editor.delete(self._count)

    def undo(self) -> None:
        self._editor.insert(self._deleted)

# 4. El Invocador: gestiona el historial de comandos
class EditorHistory:
    def __init__(self):
        self._history: list[Command] = []

    def execute(self, command: Command) -> None:
        command.execute()
        self._history.append(command)

    def undo(self) -> None:
        if self._history:
            command = self._history.pop()
            command.undo()
            print("  [Undo] Acción revertida.")
        else:
            print("  [Undo] No hay nada que deshacer.")

# 5. Código cliente
editor = TextEditor()
history = EditorHistory()

history.execute(InsertTextCommand(editor, "Hola, "))
print(f"Texto: '{editor.get_text()}'")  # 'Hola, '

history.execute(InsertTextCommand(editor, "mundo"))
print(f"Texto: '{editor.get_text()}'")  # 'Hola, mundo'

history.execute(DeleteTextCommand(editor, 5))
print(f"Texto: '{editor.get_text()}'")  # 'Hola, '

history.undo()  # Deshace el Delete
print(f"Texto: '{editor.get_text()}'")  # 'Hola, mundo'

history.undo()  # Deshace el segundo Insert
print(f"Texto: '{editor.get_text()}'")  # 'Hola, '
```
**Resultado:** La lógica de deshacer está completamente encapsulada en cada comando. El `EditorHistory` no sabe nada sobre el texto; solo sabe que puede llamar a `execute` y `undo`. Podemos añadir comandos de copiar, pegar o aplicar formato sin tocar el historial. Este patrón también es la base de los sistemas de macros, colas de tareas y transacciones.

---

### 4.10 Patrón Creacional: Abstract Factory (Fábrica Abstracta)

**Analogía:** Una fábrica de muebles. Si eliges el estilo "Victoriano", obtendrás silla victoriana, mesa victoriana y sofá victoriano — todos coherentes entre sí. Si cambias a "Moderno", obtienes los equivalentes modernos. Nunca mezclas estilos sin darte cuenta.

**Problema que resuelve:** Proporciona una interfaz para crear familias de objetos relacionados o dependientes sin especificar sus clases concretas. La diferencia con Factory Method es que aquí se crean **familias enteras** de productos, no un solo tipo.

**Caso de Estudio: UI multiplataforma (Windows / macOS)**

```python
# buen_ejemplo_abstract_factory.py
from abc import ABC, abstractmethod

# --- Familia de productos: Botón ---
class Button(ABC):
    @abstractmethod
    def render(self) -> str:
        pass

class WindowsButton(Button):
    def render(self) -> str:
        return "[Windows Button]"

class MacOSButton(Button):
    def render(self) -> str:
        return "(macOS Button)"

# --- Familia de productos: Checkbox ---
class Checkbox(ABC):
    @abstractmethod
    def render(self) -> str:
        pass

class WindowsCheckbox(Checkbox):
    def render(self) -> str:
        return "[x] Windows Checkbox"

class MacOSCheckbox(Checkbox):
    def render(self) -> str:
        return "(✓) macOS Checkbox"

# --- La Fábrica Abstracta ---
class UIFactory(ABC):
    @abstractmethod
    def create_button(self) -> Button:
        pass

    @abstractmethod
    def create_checkbox(self) -> Checkbox:
        pass

# --- Fábricas Concretas: cada una crea una familia coherente ---
class WindowsUIFactory(UIFactory):
    def create_button(self) -> Button:
        return WindowsButton()

    def create_checkbox(self) -> Checkbox:
        return WindowsCheckbox()

class MacOSUIFactory(UIFactory):
    def create_button(self) -> Button:
        return MacOSButton()

    def create_checkbox(self) -> Checkbox:
        return MacOSCheckbox()

# --- Código cliente: solo depende de la interfaz abstracta ---
def render_ui(factory: UIFactory) -> None:
    button = factory.create_button()
    checkbox = factory.create_checkbox()
    print(f"  Botón:    {button.render()}")
    print(f"  Checkbox: {checkbox.render()}")

print("UI en Windows:")
render_ui(WindowsUIFactory())

print("UI en macOS:")
render_ui(MacOSUIFactory())
```
**Resultado:** Cambiar de plataforma es cambiar la fábrica. El código cliente nunca importa `WindowsButton` ni `MacOSButton` directamente, garantizando que todos los widgets sean siempre de la misma familia.

---

### 4.11 Patrón Creacional: Prototype (Prototipo)

**Analogía:** Clonar una oveja (la famosa Dolly). En lugar de crear una nueva oveja desde cero (gestación, etc.), copias una que ya existe. En software, "clonar" un objeto complejo ya configurado es mucho más eficiente que construirlo de cero.

**Problema que resuelve:** Permite copiar objetos existentes sin que el código dependa de sus clases. Útil cuando la creación de un objeto es costosa (conexiones a BD, parsing de configuración) o cuando el objeto tiene un estado inicial complejo.

**Caso de Estudio: Configuraciones de servidor predefinidas**

```python
# buen_ejemplo_prototype.py
import copy

class ServerConfig:
    def __init__(self, host: str, port: int, max_connections: int,
                 features: list[str]):
        self.host = host
        self.port = port
        self.max_connections = max_connections
        self.features = features  # Lista mutable — hay que clonar en profundidad

    def clone(self) -> "ServerConfig":
        """Clon profundo: copia el objeto y todas sus referencias."""
        return copy.deepcopy(self)

    def __repr__(self) -> str:
        return (f"ServerConfig(host={self.host!r}, port={self.port}, "
                f"max_conn={self.max_connections}, features={self.features})")

# Prototipo base
base_config = ServerConfig(
    host="0.0.0.0",
    port=8080,
    max_connections=100,
    features=["logging", "auth"]
)

# Clonar y personalizar sin afectar al prototipo
dev_config = base_config.clone()
dev_config.host = "localhost"
dev_config.max_connections = 5
dev_config.features.append("debug_toolbar")

prod_config = base_config.clone()
prod_config.port = 443
prod_config.max_connections = 1000
prod_config.features.append("rate_limiting")

print("Base:  ", base_config)
print("Dev:   ", dev_config)
print("Prod:  ", prod_config)
# Los tres son independientes: modificar dev o prod no altera base_config
```
**Resultado:** Partimos de un prototipo bien configurado y derivamos variantes sin reconstruir desde cero. El clon profundo (`deepcopy`) es fundamental para que los objetos internos mutables no se compartan entre copias.

---

### 4.12 Patrón Estructural: Proxy

**Analogía:** Un intermediario o representante legal. Cuando no puedes hablar directamente con una persona famosa, hablas con su representante, que decide si te pasa la llamada, te bloquea, o te da una respuesta en caché. El representante tiene la misma "interfaz" que la persona real.

**Problema que resuelve:** Proporciona un sustituto o marcador de posición para otro objeto, controlando el acceso a él. Usos típicos: caché, control de acceso, logging, carga diferida (*lazy loading*).

**Caso de Estudio: Proxy de caché para una API costosa**

```python
# buen_ejemplo_proxy.py
from abc import ABC, abstractmethod
import time

# 1. La interfaz común
class WeatherService(ABC):
    @abstractmethod
    def get_temperature(self, city: str) -> float:
        pass

# 2. El servicio real (llamada costosa)
class RealWeatherService(WeatherService):
    def get_temperature(self, city: str) -> float:
        print(f"  [API] Consultando temperatura real de '{city}'...")
        time.sleep(0.1)  # Simula latencia de red
        return {"Madrid": 22.5, "Barcelona": 24.0, "Sevilla": 28.3}.get(city, 20.0)

# 3. El Proxy con caché
class CachedWeatherProxy(WeatherService):
    def __init__(self, real_service: WeatherService, ttl_seconds: int = 60):
        self._service = real_service
        self._cache: dict[str, tuple[float, float]] = {}  # ciudad → (temp, timestamp)
        self._ttl = ttl_seconds

    def get_temperature(self, city: str) -> float:
        now = time.time()
        if city in self._cache:
            temp, cached_at = self._cache[city]
            if now - cached_at < self._ttl:
                print(f"  [Cache] Temperatura de '{city}' servida desde caché.")
                return temp

        temp = self._service.get_temperature(city)
        self._cache[city] = (temp, now)
        return temp

# 4. Código cliente: no sabe si habla con el real o el proxy
def show_weather(service: WeatherService, city: str) -> None:
    print(f"Temperatura en {city}: {service.get_temperature(city)}°C")

proxy = CachedWeatherProxy(RealWeatherService(), ttl_seconds=30)

show_weather(proxy, "Madrid")   # Consulta real
show_weather(proxy, "Madrid")   # Desde caché
show_weather(proxy, "Sevilla")  # Consulta real
show_weather(proxy, "Sevilla")  # Desde caché
```
**Resultado:** El cliente usa exactamente la misma interfaz tanto si habla con el servicio real como con el proxy. El proxy añade caché de forma completamente transparente. Podríamos añadir un `AuthProxy` o `LoggingProxy` encima sin modificar nada.

---

### 4.13 Patrón Estructural: Composite (Compuesto)

**Analogía:** El sistema de archivos de tu ordenador. Una carpeta puede contener ficheros o subcarpetas. Una subcarpeta puede a su vez contener más ficheros y carpetas. Cuando calculas el tamaño de una carpeta, no distingues si un elemento es un fichero o una carpeta: simplemente llamas a `get_size()` en todos.

**Problema que resuelve:** Permite tratar objetos individuales y composiciones de objetos de manera uniforme. Ideal para estructuras jerárquicas en forma de árbol.

**Caso de Estudio: Sistema de archivos simplificado**

```python
# buen_ejemplo_composite.py
from abc import ABC, abstractmethod

# 1. La interfaz del componente (igual para hoja y compuesto)
class FileSystemItem(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def get_size(self) -> int:
        pass

    @abstractmethod
    def display(self, indent: int = 0) -> None:
        pass

# 2. La Hoja (nodo sin hijos)
class File(FileSystemItem):
    def __init__(self, name: str, size: int):
        super().__init__(name)
        self._size = size

    def get_size(self) -> int:
        return self._size

    def display(self, indent: int = 0) -> None:
        print(f"{'  ' * indent}📄 {self.name} ({self._size} KB)")

# 3. El Compuesto (nodo con hijos)
class Directory(FileSystemItem):
    def __init__(self, name: str):
        super().__init__(name)
        self._children: list[FileSystemItem] = []

    def add(self, item: FileSystemItem) -> None:
        self._children.append(item)

    def get_size(self) -> int:
        return sum(child.get_size() for child in self._children)

    def display(self, indent: int = 0) -> None:
        print(f"{'  ' * indent}📁 {self.name}/ ({self.get_size()} KB)")
        for child in self._children:
            child.display(indent + 1)

# 4. Código cliente: trata File y Directory de forma idéntica
root = Directory("proyecto")
src = Directory("src")
src.add(File("main.py", 12))
src.add(File("utils.py", 8))

tests = Directory("tests")
tests.add(File("test_main.py", 5))

root.add(src)
root.add(tests)
root.add(File("README.md", 2))

root.display()
print(f"\nTamaño total del proyecto: {root.get_size()} KB")
```
**Resultado:** El cliente llama a `get_size()` o `display()` sin saber si está ante un fichero o un directorio. Añadir nuevos tipos de nodo (p. ej., `SymLink`) no requiere tocar el código que recorre el árbol.

---

### 4.14 Patrón Comportamental: Template Method (Método Plantilla)

**Analogía:** Una receta de cocina con pasos fijos ("precalentar el horno", "hornear", "enfriar") pero con ingredientes variables según el tipo de pan. El proceso es siempre el mismo; lo que cambia son los detalles de cada paso.

**Problema que resuelve:** Define el esqueleto de un algoritmo en una clase base, dejando que las subclases redefinen ciertos pasos sin cambiar la estructura del algoritmo. Evita duplicar el "andamio" del proceso en cada subclase.

**Caso de Estudio: Pipeline de importación de datos**

```python
# buen_ejemplo_template_method.py
from abc import ABC, abstractmethod

class DataImporter(ABC):
    """Define el esqueleto del proceso de importación."""

    def import_data(self, source: str) -> None:
        """El Template Method: no se sobreescribe."""
        raw = self.read(source)
        parsed = self.parse(raw)
        validated = self.validate(parsed)
        self.save(validated)
        self.on_success(source)  # Hook opcional

    @abstractmethod
    def read(self, source: str) -> str:
        pass

    @abstractmethod
    def parse(self, raw: str) -> list[dict]:
        pass

    def validate(self, data: list[dict]) -> list[dict]:
        """Paso con implementación por defecto (puede sobreescribirse)."""
        return [row for row in data if row]

    @abstractmethod
    def save(self, data: list[dict]) -> None:
        pass

    def on_success(self, source: str) -> None:
        """Hook vacío: las subclases pueden sobreescribirlo opcionalmente."""
        pass

# --- Implementación para CSV ---
class CSVImporter(DataImporter):
    def read(self, source: str) -> str:
        print(f"[CSV] Leyendo fichero: {source}")
        return "nombre,edad\nAlice,30\nBob,25"

    def parse(self, raw: str) -> list[dict]:
        print("[CSV] Parseando CSV...")
        lines = raw.strip().split("\n")
        headers = lines[0].split(",")
        return [dict(zip(headers, line.split(","))) for line in lines[1:]]

    def save(self, data: list[dict]) -> None:
        print(f"[CSV] Guardando {len(data)} registros en BD: {data}")

    def on_success(self, source: str) -> None:
        print(f"[CSV] Importación de '{source}' completada con éxito.")

# --- Implementación para JSON ---
import json

class JSONImporter(DataImporter):
    def read(self, source: str) -> str:
        print(f"[JSON] Leyendo fichero: {source}")
        return '[{"nombre": "Carol", "edad": 28}]'

    def parse(self, raw: str) -> list[dict]:
        print("[JSON] Parseando JSON...")
        return json.loads(raw)

    def save(self, data: list[dict]) -> None:
        print(f"[JSON] Guardando {len(data)} registros en BD: {data}")

# Código cliente
CSVImporter().import_data("usuarios.csv")
print()
JSONImporter().import_data("usuarios.json")
```
**Resultado:** El flujo `leer → parsear → validar → guardar → notificar` está definido una sola vez en la clase base. Las subclases solo rellenan los pasos específicos de su formato. Si mañana añadimos validación de esquema, la añadimos en un solo lugar.

---

### 4.15 Patrón Comportamental: Chain of Responsibility (Cadena de Responsabilidad)

**Analogía:** Una solicitud de reembolso en una empresa. Si el importe es pequeño, lo aprueba el manager. Si es mayor, sube al director. Si es muy grande, requiere al CEO. La solicitud sube por la cadena hasta que alguien la gestiona.

**Problema que resuelve:** Permite pasar solicitudes a lo largo de una cadena de manejadores. Al recibir una solicitud, cada manejador decide procesarla o pasarla al siguiente. Desacopla al emisor del receptor.

**Caso de Estudio: Pipeline de validación de peticiones HTTP**

```python
# buen_ejemplo_chain.py
from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class HttpRequest:
    path: str
    api_key: str | None
    body_size_kb: int
    role: str  # "guest", "user", "admin"

# 1. La interfaz del manejador
class Middleware(ABC):
    def __init__(self):
        self._next: Middleware | None = None

    def set_next(self, handler: Middleware) -> Middleware:
        self._next = handler
        return handler  # Permite encadenamiento: a.set_next(b).set_next(c)

    def handle(self, request: HttpRequest) -> str | None:
        if self._next:
            return self._next.handle(request)
        return "✅ Petición procesada correctamente."

    @abstractmethod
    def check(self, request: HttpRequest) -> str | None:
        """Devuelve un mensaje de error o None si la comprobación pasa."""
        pass

    def handle(self, request: HttpRequest) -> str | None:
        error = self.check(request)
        if error:
            return f"❌ Bloqueado en {self.__class__.__name__}: {error}"
        if self._next:
            return self._next.handle(request)
        return "✅ Petición procesada correctamente."

# 2. Manejadores Concretos
class AuthMiddleware(Middleware):
    def check(self, request: HttpRequest) -> str | None:
        if not request.api_key:
            return "API key requerida."
        return None

class RateLimitMiddleware(Middleware):
    def check(self, request: HttpRequest) -> str | None:
        if request.body_size_kb > 100:
            return f"Cuerpo demasiado grande ({request.body_size_kb} KB > 100 KB)."
        return None

class AdminRouteMiddleware(Middleware):
    def check(self, request: HttpRequest) -> str | None:
        if request.path.startswith("/admin") and request.role != "admin":
            return f"Ruta '/admin' requiere rol admin (tienes: {request.role!r})."
        return None

# 3. Construcción de la cadena
auth = AuthMiddleware()
rate = RateLimitMiddleware()
admin_guard = AdminRouteMiddleware()

auth.set_next(rate).set_next(admin_guard)

# 4. Código cliente
requests = [
    HttpRequest(path="/home",   api_key=None,      body_size_kb=5,   role="guest"),
    HttpRequest(path="/home",   api_key="abc123",  body_size_kb=200, role="user"),
    HttpRequest(path="/admin",  api_key="abc123",  body_size_kb=10,  role="user"),
    HttpRequest(path="/admin",  api_key="abc123",  body_size_kb=10,  role="admin"),
]

for req in requests:
    print(f"GET {req.path!r:10} → {auth.handle(req)}")
```
**Resultado:** Cada middleware tiene una única responsabilidad. Podemos reordenar, añadir o eliminar eslabones de la cadena sin tocar los demás. Es la base de frameworks web como Django middleware o Express.js.

---

### 4.16 Patrón Comportamental: State (Estado)

**Analogía:** Una máquina expendedora. Su comportamiento cambia radicalmente según su estado: "sin monedas" (ignora el botón de producto), "con monedas" (permite seleccionar), "dispensando" (no acepta más monedas). El mismo botón tiene efectos completamente distintos según el estado.

**Problema que resuelve:** Permite que un objeto altere su comportamiento cuando su estado interno cambia. El objeto parecerá cambiar de clase. Elimina los grandes bloques `if/elif` basados en estado que son difíciles de mantener.

**Caso de Estudio: Gestión de pedidos en e-commerce**

```python
# buen_ejemplo_state.py
from __future__ import annotations
from abc import ABC, abstractmethod

class Order:
    """El Contexto: delega el comportamiento al estado actual."""
    def __init__(self):
        self._state: OrderState = PendingState(self)
        self.items: list[str] = []

    def set_state(self, state: OrderState) -> None:
        print(f"  [Transición] {self._state.__class__.__name__} → {state.__class__.__name__}")
        self._state = state

    def pay(self) -> None:
        self._state.pay()

    def ship(self) -> None:
        self._state.ship()

    def cancel(self) -> None:
        self._state.cancel()

    def __repr__(self) -> str:
        return f"Order(estado={self._state.__class__.__name__})"

# La interfaz del Estado
class OrderState(ABC):
    def __init__(self, order: Order):
        self._order = order

    @abstractmethod
    def pay(self) -> None: pass

    @abstractmethod
    def ship(self) -> None: pass

    @abstractmethod
    def cancel(self) -> None: pass

# Estados Concretos
class PendingState(OrderState):
    def pay(self) -> None:
        print("Pago recibido.")
        self._order.set_state(PaidState(self._order))

    def ship(self) -> None:
        print("⚠️  No se puede enviar: el pedido aún no está pagado.")

    def cancel(self) -> None:
        print("Pedido cancelado desde estado pendiente.")
        self._order.set_state(CancelledState(self._order))

class PaidState(OrderState):
    def pay(self) -> None:
        print("⚠️  El pedido ya está pagado.")

    def ship(self) -> None:
        print("Pedido enviado al almacén para preparación.")
        self._order.set_state(ShippedState(self._order))

    def cancel(self) -> None:
        print("Pedido cancelado. Se iniciará el reembolso.")
        self._order.set_state(CancelledState(self._order))

class ShippedState(OrderState):
    def pay(self) -> None:
        print("⚠️  El pedido ya está pagado.")

    def ship(self) -> None:
        print("⚠️  El pedido ya fue enviado.")

    def cancel(self) -> None:
        print("⚠️  No se puede cancelar: el pedido ya está en camino.")

class CancelledState(OrderState):
    def pay(self) -> None:
        print("⚠️  El pedido está cancelado, no se puede pagar.")

    def ship(self) -> None:
        print("⚠️  El pedido está cancelado, no se puede enviar.")

    def cancel(self) -> None:
        print("⚠️  El pedido ya está cancelado.")

# Código cliente
order = Order()
print(f"Estado inicial: {order}\n")

order.ship()    # ⚠️ Bloqueado
order.pay()     # Transición a Paid
order.pay()     # ⚠️ Ya pagado
order.ship()    # Transición a Shipped
order.cancel()  # ⚠️ Bloqueado
```
**Resultado:** Cada estado encapsula exactamente qué está permitido hacer en ese momento. No hay ningún `if self.status == "paid"` disperso por el código. Añadir un nuevo estado (`ReturnedState`, `DeliveredState`) es simplemente crear una nueva clase sin tocar las demás.

---

## 5. Nivel Senior - Conceptos Avanzados

Aquí es donde separamos a los programadores de los arquitectos. No se trata solo de usar patrones, sino de entender sus implicaciones profundas.

**Trade-offs: El Costo de la Abstracción**

*   **Complejidad:** Los patrones casi siempre introducen más clases e interfaces. Un simple `if/else` puede convertirse en un patrón Strategy con 4 clases. **¿Cuándo vale la pena?** Cuando la flexibilidad y la extensibilidad futuras son más importantes que la simplicidad inicial. Un desarrollador senior sabe cuándo anticipar el cambio y cuándo aplicar el principio YAGNI (You Ain't Gonna Need It).
*   **Indirección:** Los patrones aumentan los niveles de indirección. Para entender qué hace el código, a menudo tienes que saltar entre varias clases (el contexto, la interfaz de la estrategia, la estrategia concreta). Esto puede hacer que el código sea más difícil de depurar y seguir.
*   **Rendimiento:** La indirección puede tener un costo de rendimiento (aunque generalmente es insignificante en la mayoría de las aplicaciones). Por ejemplo, llamar a un método a través de una interfaz puede ser ligeramente más lento que una llamada directa. En sistemas de ultra-baja latencia, esto podría ser un factor.

**Anti-Patrones: El Lado Oscuro**

Un anti-patrón es una solución común a un problema que resulta ser ineficaz o contraproducente.

*   **Singleton como Estado Global:** El patrón Singleton es famoso por ser mal utilizado. A menudo se convierte en una forma elegante de introducir estado global, lo que hace que el código sea difícil de testear, propenso a efectos secundarios y un cuello de botella en entornos concurrentes.
    > "Los singletons son mentirosos. Dicen 'no te preocupes por cómo me crean', y ocultan sus dependencias. Un sistema que usa singletons es un sistema que miente sobre sus dependencias." — **Miško Hevery**, *The Clean Code Talks - "Global State and Singletons"* (2008)
*   **Golden Hammer (Martillo de Oro):** Después de aprender un patrón, es tentador aplicarlo en todas partes. Un desarrollador que acaba de descubrir el patrón Strategy podría empezar a reemplazar cada `if/else` con él, llevando a una sobre-ingeniería masiva.
*   **Pattern-itis (Sobre-ingeniería):** Aplicar patrones por el simple hecho de aplicarlos, creando una arquitectura innecesariamente compleja para un problema simple.

**Integración y Composición de Patrones**

Los patrones rara vez viven aislados. Los sistemas complejos los combinan:
*   Un **Factory Method** puede crear e instanciar un objeto **Strategy**.
*   Un **Composite** puede usar un patrón **Iterator** para recorrer su estructura de árbol.
*   Un **Facade** puede ocultar la complejidad de un subsistema que internamente usa **Observer** y **Mediator**.
*   Se puede aplicar un **Decorator** a un objeto **Proxy**.

Un arquitecto de software no piensa en patrones individuales, sino en cómo componerlos para construir una arquitectura coherente y robusta.

**Consideraciones de Escalabilidad, Seguridad y Rendimiento**

*   **Escalabilidad:** Patrones como **Proxy** pueden ser cruciales para la escalabilidad, implementando caché o balanceo de carga. Patrones como **Observer** pueden causar problemas de "notification storm" en sistemas a gran escala si no se gestionan con cuidado (p. ej., usando colas de mensajes).
*   **Seguridad:** El patrón **Proxy** es fundamental para la seguridad, permitiendo controlar el acceso a un objeto. Un **Decorator** puede añadir capas de logging o auditoría de seguridad de forma transparente.
*   **Concurrencia:** Patrones como **Singleton** requieren un manejo cuidadoso (double-checked locking) en entornos multihilo para evitar race conditions durante la instanciación. Han surgido patrones específicos de concurrencia como **Producer-Consumer** y **Read-Write Lock**.

## 6. Referencias y Citaciones Académicas

1.  > "Each pattern describes a problem which occurs over and over again in our environment, and then describes the core of the solution to that problem, in such a way that you can use this solution a million times over, without ever doing it the same way twice." — **Christopher Alexander et al.**, *A Pattern Language: Towns, Buildings, Construction* (1977). [ISBN: 978-0195019193]

2.  > "Program to an 'interface', not an 'implementation'." — **Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides**, *Design Patterns: Elements of Reusable Object-Oriented Software* (1994). [ISBN: 978-0201633610]

3.  > "One of the key properties of a framework is that the methods defined by the user to tailor the framework will often be called from within the framework itself, rather than from the user's application code. The framework often plays the role of the main program in coordinating and sequencing application activity. This inversion of control gives frameworks their power and flexibility." — **Ralph E. Johnson & Brian Foote**, *Designing Reusable Classes* (1988). [Enlace al paper](http://www.laputan.org/drc/drc.html) (Una de las primeras discusiones sobre los principios que llevaron a los patrones).

4.  > "Composition is a more powerful reuse mechanism than inheritance because it is more flexible. With composition, you can change the behavior of a class at run-time by changing the objects it is composed of." — **James O. Coplien**, *Multi-Paradigm Design for C++* (1998). [ISBN: 978-0201824674]

5.  > "The Liskov Substitution Principle (LSP) states that subtypes must be substitutable for their base types." — **Robert C. Martin**, *The Liskov Substitution Principle, C++ Report* (1996). [Enlace al artículo original](https://web.archive.org/web/20000914212726/http://www.objectmentor.com/resources/articles/lsp.pdf)

6.  > "AntiPatterns are a natural and beneficial extension to the work on design patterns. AntiPatterns provide a common vocabulary for identifying, analyzing, and solving recurring problems in software development." — **William J. Brown, Raphael C. Malveau, Hays W. "Skip" McCormick, Thomas J. Mowbray**, *AntiPatterns: Refactoring Software, Architectures, and Projects in Crisis* (1998). [ISBN: 978-0471197133]

7.  > "Singletons are nothing more than a fancy name for global variables. The two are functionally equivalent. They both create a global state that can be secretly and unexpectedly modified by any part of the code base." — **Miško Hevery**, *The Clean Code Talks - "Global State and Singletons"* (2008). [Enlace al video](https://www.youtube.com/watch?v=RlfLCWKxHJ0)

8.  > "A microservices architecture is not a silver bullet. It has many benefits, but also has significant costs. You should only consider using it for complex systems that have to be scalable and evolvable." — **Chris Richardson**, *Microservices Patterns* (2018). [ISBN: 978-1617294549] (Ejemplo de la evolución de patrones a nuevas arquitecturas).

9.  > "The best patterns are the ones you don't even notice. The best patterns are the ones that are so deeply embedded in the language or the framework that you don't even realize you're using them." — **Martin Fowler**, *Refactoring: Improving the Design of Existing Code* (1999). [ISBN: 978-0201485677]

10. > "The Strategy pattern suggests that you take a class that does something specific in a lot of different ways and extract all of these algorithms into separate classes called strategies." — **Alexander Shvets**, *Dive Into Design Patterns* (2018). [Enlace al recurso](https://refactoring.guru/design-patterns) (Una excelente referencia moderna y accesible).

***

### Conclusión

Hemos viajado desde los cimientos arquitectónicos de Christopher Alexander hasta las complejas arquitecturas de microservicios de hoy. Hemos visto que los patrones de diseño no son un conjunto de reglas rígidas, sino un lenguaje para discutir y resolver problemas de diseño.

Un programador intermedio sabe *qué* es un patrón. Un programador senior entiende *por qué* existe, *cuándo* aplicarlo, y, lo que es más importante, *cuándo no hacerlo*. Los patrones son herramientas, no objetivos. El verdadero objetivo es construir software robusto, mantenible y elegante. Ahora tienes el mapa y la brújula para hacerlo. El resto del viaje es tuyo.
