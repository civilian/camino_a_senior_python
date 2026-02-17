Imagina que te contratan para un trabajo y te entregan un manual de 500 páginas con reglas para cada departamento, aunque solo trabajes en uno. ¿Absurdo, verdad? En software, hacemos esto todo el tiempo, y vamos a ver cómo evitarlo con los dos últimos principios de SOLID, que nos abrirán las puertas al diseño de arquitecturas verdaderamente flexibles.

# SOLID

#### I - Interface Segregation Principle (ISP)
*El principio del "no me obligues".* Ningún cliente debería ser forzado a depender de métodos que no usa. Es mejor tener muchas interfaces pequeñas y específicas que una grande y genérica.

**Analogía:** Un restaurante con un menú de 500 páginas (interfaz "gorda") vs. un restaurante que te da un menú para desayunos, otro para almuerzos y otro para cenas (interfaces segregadas). Solo usas el que necesitas.

**Mal (Antes):**

```python
# MAL: Interfaz "gorda" que obliga a todos los trabajadores a implementarla.
class IWorker(ABC):
    @abstractmethod
    def work(self): pass
    
    @abstractmethod
    def eat(self): pass

class HumanWorker(IWorker):
    def work(self):
        print("Humano trabajando...")
    def eat(self):
        print("Humano comiendo...")

class RobotWorker(IWorker):
    def work(self):
        print("Robot trabajando...")
    
    def eat(self):
        # Un robot no come. Esta implementación es forzada y sin sentido.
        # Podríamos poner 'pass' o lanzar una excepción, ambas son malas señales.
        raise NotImplementedError("Los robots no comen")
```
**¿Por qué es malo?** `RobotWorker` es forzado a implementar un método `eat` que no tiene sentido para él. Esto es una señal de que la abstracción `IWorker` es demasiado grande.

**Bien (Después):**

```python
# BIEN: Interfaces pequeñas y específicas (en Python, usamos Protocolos o ABCs).
class IWorkable(ABC):
    @abstractmethod
    def work(self): pass

class IEatable(ABC):
    @abstractmethod
    def eat(self): pass

# Las clases implementan solo las interfaces que necesitan.
class HumanWorker(IWorkable, IEatable):
    def work(self):
        print("Humano trabajando...")
    def eat(self):
        print("Humano comiendo...")

class RobotWorker(IWorkable):
    def work(self):
        print("Robot trabajando...")

# El código cliente ahora puede depender de la capacidad específica que requiere.
def manage_work(worker: IWorkable):
    worker.work()

manage_work(HumanWorker())
manage_work(RobotWorker())
```
Ahora, nuestro sistema es más flexible. Podemos tener `IEatable` para un `Animal`, o `IWorkable` para una `Impresora3D`.

#### D - Dependency Inversion Principle (DIP)
*El principio de "no me llames, yo te llamo" (The Hollywood Principle).* Los módulos de alto nivel no deben depender de los módulos de bajo nivel. Ambos deben depender de abstracciones. Además, las abstracciones no deben depender de los detalles; los detalles deben depender de las abstracciones.

**Analogía:** No sueldas una lámpara directamente a los cables de la pared. Usas un enchufe (una abstracción). La lámpara (módulo de alto nivel) no depende del cableado específico de la pared (módulo de bajo nivel). Ambos dependen del estándar del enchufe.

**Diagrama ASCII:**

**Mal:** `[Módulo de Alto Nivel] ---> [Módulo de Bajo Nivel Concreto]`
**Bien:** `[Módulo de Alto Nivel] ---> [Interfaz] <--- [Módulo de Bajo Nivel Concreto]`

**Mal (Antes):**

```python
# MAL: El módulo de alto nivel (Research) depende directamente del de bajo nivel (Relationships).
from enum import Enum

class Relationship(Enum):
    PARENT = 0
    CHILD = 1
    SIBLING = 2

class Person:
    def __init__(self, name):
        self.name = name

# Módulo de bajo nivel (almacenamiento de datos)
class Relationships:
    def __init__(self):
        self.relations = []
    
    def add_parent_and_child(self, parent, child):
        self.relations.append((parent, Relationship.PARENT, child))
        self.relations.append((child, Relationship.CHILD, parent))

# Módulo de alto nivel (lógica de negocio)
class Research:
    def __init__(self, relationships: Relationships):
        # ¡Dependencia directa de una clase concreta y su implementación interna!
        relations = relationships.relations
        for r in relations:
            if r[0].name == "John" and r[1] == Relationship.PARENT:
                print(f"John es padre de {r[2].name}")
```
**¿Por qué es malo?** `Research` está fuertemente acoplado a la implementación interna de `Relationships` (su lista `relations`). Si `Relationships` decide cambiar su forma de almacenar datos (a un diccionario, una base de datos), la clase `Research` se romperá y tendrá que ser modificada.

**Bien (Después):**

```python
# BIEN: Ambos módulos dependen de una abstracción.
from abc import ABC, abstractmethod

class RelationshipBrowser(ABC):
    @abstractmethod
    def find_all_children_of(self, name):
        pass

# Módulo de bajo nivel, ahora implementa la abstracción.
class Relationships(RelationshipBrowser): # <--- Depende de la abstracción
    def __init__(self):
        self.relations = []
    
    def add_parent_and_child(self, parent, child):
        self.relations.append((parent, Relationship.PARENT, child))
        self.relations.append((child, Relationship.CHILD, parent))

    def find_all_children_of(self, name):
        for r in self.relations:
            if r[0].name == name and r[1] == Relationship.PARENT:
                yield r[2]

# Módulo de alto nivel, ahora depende de la abstracción.
class Research:
    def __init__(self, browser: RelationshipBrowser): # <--- Depende de la abstracción
        for p in browser.find_all_children_of("John"):
            print(f"John es padre de {p.name}")

# Uso
parent = Person("John")
child1 = Person("Chris")
child2 = Person("Matt")

relationships = Relationships()
relationships.add_parent_and_child(parent, child1)
relationships.add_parent_and_child(parent, child2)

# Inyectamos la dependencia
research = Research(relationships)
```
Ahora `Research` no sabe ni le importa cómo `Relationships` almacena los datos. Solo le importa que cumpla el contrato de `RelationshipBrowser`. Podemos cambiar `Relationships` por `DatabaseRelationships` sin tocar `Research` en absoluto. Esto es la base de la **Inyección de Dependencias**.

---

### 5. Nivel Senior - Conceptos Avanzados: Más Allá del Acrónimo

Un programador intermedio conoce los principios. Un senior sabe cuándo aplicarlos, cuándo doblarlos y cuáles son sus consecuencias.

#### Trade-offs: La Navaja de Ockham del Código

SOLID no es una ley divina. Es una herramienta. Aplicar SOLID ciegamente puede llevar a una "sobre-ingeniería".

*   **Complejidad vs. Flexibilidad:** Aplicar OCP y DIP introduce más clases e interfaces. Para un script simple o un prototipo, esto es un exceso de complejidad (viola el principio YAGNI - "You Ain't Gonna Need It"). Para un sistema empresarial a largo plazo, esta flexibilidad es crucial.
*   **Rendimiento:** La indirección introducida por DIP (a través de interfaces) puede tener un costo de rendimiento minúsculo. En el 99.9% de las aplicaciones, es irrelevante. En sistemas de ultra-baja latencia (como el trading de alta frecuencia), cada salto de puntero cuenta y podría ser un trade-off a considerar.
*   **Cohesión vs. SRP:** A veces, dividir una clase por SRP puede llevar a dos clases que están tan íntimamente ligadas que es más difícil entenderlas por separado que juntas. La clave de SRP es "una razón para cambiar". Si dos responsabilidades siempre cambian juntas, podrían pertenecer a la misma clase.

**¿Cuándo NO usar SOLID (o usarlo con moderación)?**
*   **Prototipos y MVPs:** La velocidad es clave. La rigidez no es un problema si vas a tirar el código.
*   **Código muy específico y estable:** Si estás escribiendo un driver para un hardware que no cambiará en 10 años, la extensibilidad de OCP es menos crítica.
*   **Módulos de datos puros (DTOs):** Las clases que solo contienen datos no suelen beneficiarse de la mayoría de los principios SOLID.

#### Anti-Patrones: El Lado Oscuro

| Principio | Anti-Patrón Común | Descripción |
| :--- | :--- | :--- |
| **SRP** | **God Object / The Blob** | Una clase masiva que hace de todo: lógica de negocio, acceso a datos, UI. Es el epicentro de la rigidez y fragilidad. |
| **OCP** | **Cascadas de `if/elif/else` o `switch`** | El código que comprueba un tipo o una enumeración y se ramifica es una señal de que debería estar usando polimorfismo. |
| **LSP** | **Herencia por Reutilización de Código** | Heredar de una clase solo para usar un par de sus métodos, pero rompiendo su contrato conductual. |
| **LSP** | **Métodos que lanzan `NotImplementedError`** | Una subclase que anula un método de la clase base para decir "no hago esto" está violando el contrato. |
| **ISP** | **Interfaz Gorda (Fat Interface)** | Una interfaz con docenas de métodos, obligando a los clientes a implementar cosas que no necesitan. |
| **DIP** | **Acoplamiento a Concreciones (Concrete Coupling)** | Módulos de alto nivel que importan y crean instancias de módulos de bajo nivel directamente, en lugar de recibir abstracciones. |

#### Integración con Otros Conceptos Avanzados

*   **Arquitectura Limpia (Clean Architecture):** DIP es la piedra angular de la Arquitectura Limpia/Hexagonal/Cebolla. La "Regla de la Dependencia" (las dependencias solo apuntan hacia adentro, hacia las abstracciones) es una aplicación de DIP a nivel de arquitectura.
*   **Domain-Driven Design (DDD):** SOLID ayuda a crear agregados y entidades cohesivas (SRP) y a desacoplar el dominio de la infraestructura (DIP).
*   **Patrones de Diseño (Design Patterns):** Muchos patrones son implementaciones de principios SOLID. El patrón **Strategy** y **Template Method** son encarnaciones de OCP. El patrón **Adapter** puede usarse para reparar violaciones de LSP. El patrón **Factory** y la **Inyección de Dependencias** son la forma de implementar DIP.

---

### 6. Referencias y Citaciones Académicas: Los Hombros de Gigantes

1.  > "The single responsibility principle (SRP) states that a class should have one and only one reason to change." — **Robert C. Martin**, *Agile Software Development, Principles, Patterns, and Practices* (2002)
2.  > "Software entities (classes, modules, functions, etc.) should be open for extension, but closed for modification." — **Bertrand Meyer**, *Object-Oriented Software Construction* (1988)
3.  > "Subtypes must be substitutable for their base types." — **Barbara Liskov**, *Keynote at OOPSLA'87, "Data Abstraction and Hierarchy"* (1987)
4.  > "Clients should not be forced to depend upon interfaces that they do not use." — **Robert C. Martin**, *Agile Software Development, Principles, Patterns, and Practices* (2002)
5.  > "A. High-level modules should not depend on low-level modules. Both should depend on abstractions. B. Abstractions should not depend on details. Details should depend on abstractions." — **Robert C. Martin**, *The Dependency Inversion Principle*, The C++ Report (1996)
6.  > "We must be able to change our minds. That’s what agility is all about. The purpose of a software architecture is to create options." — **Robert C. Martin**, *Clean Architecture: A Craftsman's Guide to Software Structure and Design* (2017) [Link](https://www.oreilly.com/library/view/clean-architecture-a/9780134494166/)
7.  > "A design is a big ball of mud if it does not have a discernible architecture." — **Brian Foote, Joseph Yoder**, *Big Ball of Mud* (1999) [Link](http://www.laputan.org/mud/)
8.  > "The primary mechanisms for implementing the OCP are abstraction and polymorphism." — **Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides**, *Design Patterns: Elements of Reusable Object-Oriented Software* (1994)
9.  > "The criteria for decomposing a system into modules is information hiding." — **David L. Parnas**, *On the Criteria To Be Used in Decomposing Systems into Modules*, Communications of the ACM (1972) [Link](https://dl.acm.org/doi/10.1145/361598.361623)
10. > "Working with legacy code is like being a surgeon. You have to be careful and precise, and you need to know the anatomy of the system you are working on." — **Michael C. Feathers**, *Working Effectively with Legacy Code* (2004)
11. > "Every high-quality architectural structure is made of a set of smaller patterns, and these patterns in turn are made of even smaller patterns." — **Christopher Alexander**, *A Pattern Language: Towns, Buildings, Construction* (1977)
12. > "The Law of Demeter for functions/methods requires that a method M of an object O may only invoke the methods of the following kinds of objects: O itself; M's parameters; Any objects created/instantiated within M; O's direct component objects." — **Karl Lieberherr, Ian Holland**, *Assuring Good Style for Object-Oriented Programs*, IEEE Software (1989) [Este principio, aunque no es parte de SOLID, está profundamente relacionado con el bajo acoplamiento].

---

**Conclusión:**

SOLID no es un dogma, es una brújula. No te dirá exactamente cómo construir tu sistema, pero te señalará la dirección correcta: hacia un software que sea un placer mantener, que pueda crecer y adaptarse, y que resista la entropía inevitable del tiempo. Dominar estos principios es dar el salto de escribir código que *funciona* a crear software que *perdura*. Ahora, ve y construye catedrales, no bolas de lodo.