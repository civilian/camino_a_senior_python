Entender la historia de una tecnología nos da contexto, pero ¿cómo la llevamos a la práctica? Ahora que conocemos el 'porqué' de GraphQL, es hora de ensuciarnos las manos. Veremos cómo tres bibliotecas de Python abordan el mismo problema con filosofías muy diferentes: Code-First vs. Schema-First.

# GraphQL (Graphene, ariadne, Tartiflette)

---

### 3. Evolución Histórica Detallada

Para entender verdaderamente una tecnología, debemos entender el contexto en el que nació. La década de 2010 fue la era de la "API Economy" y el auge de las Single-Page Applications (SPAs) con frameworks como Angular y React (otro producto de Facebook de la misma época).

| Año | Evento Clave | Contexto Computacional | Figuras Clave |
| :--- | :--- | :--- | :--- |
| **2012** | Inicia el desarrollo interno de GraphQL en Facebook. | El tráfico móvil supera al de escritorio. Las SPAs se vuelven la norma. Las redes 3G son la realidad para millones de usuarios. | Lee Byron, Dan Schafer, Nick Schrock |
| **2015** | **Lanzamiento público de la especificación GraphQL.** | React ya ha ganado una tracción masiva. La idea de componentes que declaran sus propias dependencias de datos encaja perfectamente con GraphQL. | Facebook Open Source |
| **2016** | Apollo GraphQL lanza su suite de herramientas. | La comunidad necesita más que una especificación; necesita herramientas de producción. Apollo llena ese vacío. | Geoff Schmidt |
| **2017** | GitHub anuncia su v4 API, completamente en GraphQL. | Un voto de confianza masivo de un pilar de la comunidad de desarrolladores. Demuestra que GraphQL está listo para el "prime time". | GitHub Engineering |
| **2018** | **Creación de la GraphQL Foundation.** | Para asegurar la longevidad y la neutralidad del estándar, se traslada a la Linux Foundation. Empresas como Google, Twitter, y AWS se unen. | The Linux Foundation |
| **2020+** | Maduración de conceptos como Federación y `defer`/`stream`. | Las arquitecturas de microservicios se vuelven dominantes. La Federación de Apollo se convierte en el estándar de facto para unificar múltiples servicios GraphQL. | Apollo GraphQL Team |

Este viaje desde una solución interna a un estándar global abierto es un testimonio del poder de resolver un problema real y compartir la solución con el mundo.

---

### 4. Implementación Práctica en Python

Basta de teoría. Es hora de escribir código. En Python, el ecosistema de GraphQL se divide principalmente en dos filosofías: **Code-First** y **Schema-First**.

*   **Code-First (Graphene):** Defiendes tus tipos y esquema usando clases y código Python. Ideal para integrarse con ORMs como Django o SQLAlchemy.
*   **Schema-First (Ariadne, Tartiflette):** Escribes tu esquema en el SDL de GraphQL y luego "conectas" tu código Python (resolvers) a ese esquema. Promueve una separación más clara de las preocupaciones.

Vamos a modelar un sistema simple de Blog con `Autores` y `Publicaciones`.

#### Escenario: Una API para un Blog

**El Esquema (SDL):** Este será nuestro contrato.

```graphql
type Author {
  id: ID!
  name: String!
  posts: [Post!]
}

type Post {
  id: ID!
  title: String!
  content: String!
  author: Author!
}

type Query {
  allPosts: [Post!]
  postById(id: ID!): Post
}
```

**Datos de ejemplo:**

```python
# Simulación de nuestra base de datos
authors_data = {
    "1": {"id": "1", "name": "J.R.R. Tolkien"},
    "2": {"id": "2", "name": "C.S. Lewis"},
}

posts_data = {
    "1": {"id": "1", "title": "The Hobbit", "content": "...", "author_id": "1"},
    "2": {"id": "2", "title": "The Lion, the Witch and the Wardrobe", "content": "...", "author_id": "2"},
    "3": {"id": "3", "title": "The Fellowship of the Ring", "content": "...", "author_id": "1"},
}
```

#### Implementación 1: Graphene (Code-First)

Graphene se siente muy familiar si vienes de Django. Es orientado a objetos y explícito.

```python
# pip install graphene
import graphene

# 1. Definir los ObjectTypes que mapean al esquema
class Author(graphene.ObjectType):
    id = graphene.ID()
    name = graphene.String()
    posts = graphene.List(lambda: Post)

    def resolve_posts(parent, info):
        # En un caso real, aquí harías una consulta a la BD
        author_id = parent.id
        return [Post(**p) for p in posts_data.values() if p["author_id"] == author_id]

class Post(graphene.ObjectType):
    id = graphene.ID()
    title = graphene.String()
    content = graphene.String()
    author = graphene.Field(Author)

    def resolve_author(parent, info):
        author_id = parent.author_id
        return Author(**authors_data[author_id])

# 2. Definir la Query raíz
class Query(graphene.ObjectType):
    all_posts = graphene.List(Post)
    post_by_id = graphene.Field(Post, id=graphene.ID(required=True))

    def resolve_all_posts(root, info):
        # Mapeamos los datos del diccionario a nuestros objetos Post
        # Nótese que pasamos el author_id para que el resolver de Post pueda usarlo
        return [Post(**p) for p in posts_data.values()]

    def resolve_post_by_id(root, info, id):
        post_data = posts_data.get(id)
        if post_data:
            return Post(**post_data)
        return None

# 3. Crear el esquema ejecutable
schema = graphene.Schema(query=Query)

# Para probarlo:
query_string = """
    query {
      allPosts {
        title
        author {
          name
        }
      }
    }
"""
result = schema.execute(query_string)
print(result.data)
# Salida: {'allPosts': [{'title': 'The Hobbit', 'author': {'name': 'J.R.R. Tolkien'}}, ...]}
```

**Análisis (Graphene):**
*   **Bueno:** Excelente integración con ORMs, muy explícito, el código es la única fuente de verdad.
*   **Malo:** Puede volverse verboso. La definición del esquema está mezclada con la lógica de resolución, lo que puede dificultar la lectura.

#### Implementación 2: Ariadne (Schema-First)

Ariadne es elegante y minimalista. El SDL es el rey.

```python
# pip install ariadne
from ariadne import QueryType, ObjectType, make_executable_schema, gql

# 1. El SDL es la fuente de verdad
type_defs = gql("""
    type Author {
      id: ID!
      name: String!
      posts: [Post!]
    }
    # ... (el resto del SDL de antes) ...
    type Query {
      allPosts: [Post!]
      postById(id: ID!): Post
    }
""")

# 2. Crear objetos para enlazar resolvers
query = QueryType()
post = ObjectType("Post")
author = ObjectType("Author")

# 3. Enlazar funciones a los campos del esquema
@query.field("allPosts")
def resolve_all_posts(_, info):
    return posts_data.values()

@query.field("postById")
def resolve_post_by_id(_, info, id):
    return posts_data.get(id)

@post.field("author")
def resolve_post_author(post_obj, info):
    author_id = post_obj["author_id"]
    return authors_data.get(author_id)

@author.field("posts")
def resolve_author_posts(author_obj, info):
    author_id = author_obj["id"]
    return [p for p in posts_data.values() if p["author_id"] == author_id]

# 4. Crear el esquema ejecutable
schema = make_executable_schema(type_defs, query, post, author)

# Probarlo (el mismo query_string de antes)
# ... el código para ejecutar es un poco más complejo con Ariadne para async,
# pero el concepto central es el mismo.
```

**Análisis (Ariadne):**
*   **Bueno:** Separación limpia entre esquema y lógica. El SDL es fácil de compartir con equipos de frontend. Menos "boilerplate".
*   **Malo:** La "magia" del enlace puede ser menos obvia para principiantes. Requiere mantener el SDL y los resolvers en sincronía.

#### Implementación 3: Tartiflette (Schema-First, Async-first)

Tartiflette está diseñado desde cero para ser asíncrono, lo que lo hace ideal para aplicaciones de alto rendimiento basadas en `asyncio`.

```python
# pip install tartiflette tartiflette-aiohttp
import asyncio
from tartiflette import Resolver, Engine

# 1. SDL en un archivo o string
sdl = """
    type Author { ... }
    type Post { ... }
    type Query { ... }
"""

# 2. Usar decoradores para enlazar resolvers
@Resolver("Query.allPosts")
async def resolve_all_posts(parent, args, context, info):
    return posts_data.values()

@Resolver("Query.postById")
async def resolve_post_by_id(parent, args, context, info):
    return posts_data.get(args['id'])

@Resolver("Post.author")
async def resolve_post_author(parent, args, context, info):
    author_id = parent["author_id"]
    return authors_data.get(author_id)

# ... y así sucesivamente para Author.posts

# 3. Crear y "cocinar" el motor
engine = Engine(sdl)

async def main():
    result = await engine.execute(query_string)
    print(result)

# asyncio.run(main())
```

**Análisis (Tartiflette):**
*   **Bueno:** Rendimiento excepcional gracias a `asyncio`. El enfoque de "motor" es potente.
*   **Malo:** La curva de aprendizaje de `asyncio` puede ser un obstáculo. El ecosistema es menos maduro que el de Graphene o Ariadne.

#### Comparativa de Bibliotecas Python

| Característica | Graphene | Ariadne | Tartiflette |
| :--- | :--- | :--- | :--- |
| **Filosofía** | Code-First | Schema-First | Schema-First |
| **Estilo** | Orientado a Objetos | Funcional, declarativo | Funcional, basado en decoradores |
| **Soporte Async** | Sí (con `graphene.Future`) | Nativo y excelente | **Nativo y obligatorio** |
| **Curva de Aprendizaje** | Fácil (para OOP/Django devs) | Moderada | Moderada (requiere `asyncio`) |
| **Ideal para...** | Proyectos existentes con ORMs | Nuevos proyectos, APIs públicas | Servicios de alto rendimiento, microservicios |