AQUI**

La diferencia entre un script que funciona y un sistema robusto está en la arquitectura. ¿Cómo pasamos de un código frágil y monolítico a un flujo de datos componible y elegante? Veamos un caso práctico que revela el poder de la LangChain Expression Language.

# LangChain

### 4. Implementación Práctica: Del Caos a la Componibilidad

#### Caso de Estudio: Construyendo un Asistente de Q&A sobre un Documento

**El Problema**: Tenemos un documento PDF largo (por ejemplo, un informe financiero) y queremos hacerle preguntas en lenguaje natural.

**El Enfoque "Antes de LangChain" (o el Mal Enfoque)**

Un desarrollador intermedio podría escribir un script monolítico:

```python
# mal_enfoque.py
import openai
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer

# 1. Cargar y trocear el texto (de forma manual y frágil)
reader = PdfReader("informe_anual.pdf")
texto_completo = ""
for page in reader.pages:
    texto_completo += page.extract_text()
chunks = [texto_completo[i:i+1000] for i in range(0, len(texto_completo), 800)] # Solapamiento manual

# 2. Crear embeddings (usando una librería directamente)
model_embed = SentenceTransformer('all-MiniLM-L6-v2')
chunk_embeddings = model_embed.encode(chunks)

# 3. Lógica de búsqueda manual
pregunta = "¿Cuál fue el ingreso neto en 2023?"
pregunta_embedding = model_embed.encode([pregunta])[0]

# Cálculo manual de similitud de coseno (simplificado)
import numpy as np
def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

similitudes = [cosine_similarity(pregunta_embedding, emb) for emb in chunk_embeddings]
indice_mejor = np.argmax(similitudes)
contexto = chunks[indice_mejor]

# 4. Construcción manual del prompt y llamada a la API
prompt = f"""
Contexto: {contexto}

Pregunta: {pregunta}

Responde la pregunta basándote únicamente en el contexto proporcionado.
"""

cliente_openai = openai.OpenAI(api_key="...")
respuesta = cliente_openai.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": prompt}]
)

print(respuesta.choices[0].message.content)
```

**Problemas de este enfoque**:
*   **Frágil**: El troceado de texto es ingenuo. La lógica de búsqueda está hardcodeada.
*   **No modular**: Todo está en un solo script. Cambiar el modelo de embeddings o el LLM requiere reescribir partes significativas.
*   **Difícil de extender**: ¿Y si queremos añadir memoria? ¿O usar múltiples documentos? Se convierte en un lío de código espagueti.

**El Enfoque "Con LangChain" (El Buen Enfoque - Nivel Senior)**

Usaremos las abstracciones correctas y el poder de LCEL.

```python
# buen_enfoque_lcel.py
import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# Configuración (¡siempre separada!)
os.environ["OPENAI_API_KEY"] = "..."

# --- 1. Fase de Indexación (se hace una sola vez) ---
# Carga y división de documentos con componentes especializados
loader = PyPDFLoader("informe_anual.pdf")
docs = loader.load()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = text_splitter.split_documents(docs)

# Creación del VectorStore (Base de datos de vectores)
# Abstrae el modelo de embeddings y el almacenamiento
vectorstore = FAISS.from_documents(documents=splits, embedding=OpenAIEmbeddings())
retriever = vectorstore.as_retriever()

# --- 2. Fase de Generación (se ejecuta para cada pregunta) ---
# Definición del prompt de manera segura y reutilizable
template = """
Responde la pregunta basándote únicamente en el siguiente contexto:
{context}

Pregunta: {question}
"""
prompt = ChatPromptTemplate.from_template(template)

# Definición del LLM
llm = ChatOpenAI(model_name="gpt-4o", temperature=0)

# Creación de la cadena con LCEL (LangChain Expression Language)
# ¡Aquí está la magia de la composición!
rag_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# --- 3. Invocación ---
pregunta = "¿Cuál fue el ingreso neto en 2023?"
respuesta = rag_chain.invoke(pregunta)

print(respuesta)

# ¿Quieres ver los documentos recuperados? La transparencia de LCEL lo permite.
# for chunk in retriever.get_relevant_documents(pregunta):
#     print(chunk.page_content)
#     print("-" * 20)
```

**Ventajas del enfoque Senior**:
*   **Modularidad**: Cada paso (`loader`, `text_splitter`, `vectorstore`, `retriever`, `prompt`, `llm`) es un objeto intercambiable. ¿Quieres usar embeddings de HuggingFace y un VectorStore en ChromaDB? Solo cambia dos líneas.
*   **Robustez**: `RecursiveCharacterTextSplitter` es mucho más inteligente que un split manual. Las librerías subyacentes están optimizadas.
*   **Componibilidad y Transparencia (LCEL)**: La línea `rag_chain = ...` es la clave. Es declarativa, legible y se parece a una tubería. Define el *flujo de datos* de manera explícita. Gracias a LCEL, esta cadena obtiene automáticamente:
    *   Streaming (`rag_chain.stream(pregunta)`)
    *   Ejecución asíncrona (`await rag_chain.ainvoke(pregunta)`)
    *   Paralelización de pasos cuando es posible.
*   **Mantenibilidad**: El código es limpio, fácil de razonar y de depurar (especialmente con LangSmith).