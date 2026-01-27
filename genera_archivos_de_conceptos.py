import os
import re

# Si quieres usar Gemini vía LangChain, necesitas instalar:
# pip install langchain-google-genai google-generativeai python-dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv  # <-- Añadido para cargar .env

INPUT_FILE = "habilidades_python.md"
OUTPUT_DIR = "conceptos"

def to_snake_case(text):
    text = text.strip().replace("/", " ")
    text = re.sub(r"[^\w\s]", "", text)
    text = re.sub(r"\s+", "_", text)
    return text.lower()

def is_concept_line(line):
    line = line.strip()
    return line.startswith("-") and len(line) > 2

def extract_concept(line):
    return line.lstrip("-").strip()

def get_gemini_response(concept, llm):
    prompt = f"""Eres un experto educador de programación con décadas de experiencia, combinando profundidad técnica con narrativa cautivadora. Tu tarea es crear una guía exhaustiva y profunda sobre: **{concept}**

## OBJETIVO PRINCIPAL
Crear una guía que transforme a un programador de nivel intermedio a nivel **SENIOR** en este concepto específico. La guía debe ser tan profunda que después de leerla, el lector pueda justificar decisiones de diseño, entender trade-offs, y aplicar el concepto en contextos complejos.

## ESTRUCTURA REQUERIDA

1. **Introducción Profunda**: 
   - Contexto histórico: quién creó el concepto, cuándo, dónde y por qué surgió
   - Problema que resuelve: qué necesidad específica de la ingeniería de software o computación aborda
   - Evolución desde su origen hasta el estado actual: hitos importantes, versiones, mejoras

2. **Fundamentos Teóricos y Matemáticos**:
   - Base teórica: fundamentos matemáticos, computacionales o de ingeniería detrás del concepto
   - Principios subyacentes: qué teorías o paradigmas lo sustentan
   - Relación con otros conceptos: cómo se conecta con la historia de la computación

3. **Evolución Histórica Detallada**:
   - Timeline del concepto: desde su concepción hasta hoy
   - Figuras clave: personas importantes que contribuyeron
   - Momentos decisivos: cambios importantes que marcaron su desarrollo
   - Contexto histórico: qué estaba pasando en la computación/ingeniería cuando surgió

4. **Implementación Práctica**:
   - Ejemplos de código reales y funcionales en Python
   - Patrones de uso comunes y avanzados
   - Casos de estudio del mundo real
   - Comparaciones: "antes vs después", "mal vs bien"

5. **Nivel Senior - Conceptos Avanzados**:
   - Optimizaciones y técnicas avanzadas
   - Trade-offs: cuándo usar y cuándo NO usar este concepto
   - Anti-patrones: errores comunes y cómo evitarlos
   - Integración con otros conceptos avanzados
   - Consideraciones de rendimiento, seguridad, escalabilidad

6. **Referencias y Citaciones Académicas**:
   - Mínimo 8-12 referencias reales (papers académicos, libros reconocidos, documentación oficial)
   - Formato: > "Cita textual exacta" — **Autor**, *Fuente* (Año)
   - Incluye enlaces cuando sea posible
   - Referencias históricas relevantes de la computación

## ESTILO Y TONO

- **Profesional pero accesible**: Técnico pero comprensible
- **Narrativa rica**: Incluye anécdotas históricas relevantes de la computación e ingeniería
- **Cultura integrada**: Incorpora referencias sutiles y naturales a:
  - Cultura pop (cuando sea relevante y añada valor)
  - Poemas o literatura (si hay conexiones significativas)
  - Cultura de programadores (memes, chistes internos, referencias a la comunidad)
  - Historia de la computación (personajes, eventos, momentos icónicos)
- **Analogías claras**: Usa metáforas del mundo real para explicar conceptos complejos
- **Explicación del "por qué"**: No solo el "qué" y "cómo", sino el razonamiento detrás de cada decisión

## FORMATO Y PRESENTACIÓN

- Usa Markdown completo: títulos (##), subtítulos (###), listas, bloques de código con sintaxis
- Ejemplos de código: Incluye código Python funcional, bien comentado, con explicaciones
- Citas destacadas: Usa bloques de cita (>) para referencias importantes y citas textuales
- Tablas comparativas: Cuando ayuden a contrastar conceptos, enfoques o herramientas
- Diagramas en texto: Usa ASCII art o descripciones claras cuando ayuden a visualizar conceptos

## CITACIONES Y REFERENCIAS

- **Cantidad**: Mínimo 8-12 referencias reales y verificables
- **Tipos**: Papers académicos, libros reconocidos, documentación oficial, artículos de expertos
- **Formato de citas**: 
  > "Texto de la cita exacta" — **Nombre del Autor**, *Título de la Fuente* (Año)
- **Enlaces**: Incluye URLs cuando sea posible y relevante
- **Diversidad**: Incluye referencias históricas, técnicas y contemporáneas

## LONGITUD Y PROFUNDIDAD

- **Mínimo 2500-3000 palabras**: Suficiente profundidad para alcanzar nivel senior
- **Cobertura completa**: Cada aspecto del concepto debe estar cubierto en detalle
- **Profundidad técnica**: No superficialidades, sino entendimiento profundo

## REQUISITOS CRÍTICOS

- ✅ **No placeholders**: Todo el contenido debe ser real y específico
- ✅ **Técnicamente correcto**: Verifica que toda la información sea precisa y actualizada
- ✅ **Valor real**: Cada sección debe aportar conocimiento genuino
- ✅ **Ejemplos concretos**: Código real, no pseudocódigo genérico
- ✅ **Contexto histórico**: Conecta el concepto con la historia de la computación
- ✅ **Perspectiva senior**: Enfócate en lo que un senior necesita saber, no solo lo básico

## ELEMENTOS ESPECIALES A INCLUIR

- **Anécdotas históricas**: Momentos icónicos de la computación relacionados con el concepto
- **Referencias culturales**: Integradas naturalmente cuando añadan contexto o claridad
- **Humor sutil**: Chistes de ingeniería, cultura de programadores, o referencias históricas cuando sea apropiado
- **Conexiones interdisciplinarias**: Relaciona el concepto con matemáticas, física, filosofía cuando sea relevante

---

Ahora, crea la guía completa, exhaustiva y profunda sobre **{concept}**. Recuerda: el objetivo es que después de leer esta guía, alguien pueda considerarse senior en este tema específico."""
    response = llm.invoke(prompt)
    return response.content if hasattr(response, "content") else str(response)

def main():
    load_dotenv()  # <-- Carga variables de entorno desde .env
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    # Configura tu API KEY de Gemini en la variable de entorno GOOGLE_API_KEY
    llm = ChatGoogleGenerativeAI(model="models/gemini-2.5-pro", temperature=0.5)
    with open(INPUT_FILE, encoding="utf-8") as f:
        for line in f:
            if is_concept_line(line):
                concept = extract_concept(line)
                filename = to_snake_case(concept) + ".md"
                filepath = os.path.join(OUTPUT_DIR, filename)
                print(f"Generando: {filepath}")
                respuesta = get_gemini_response(concept, llm)
                with open(filepath, "w", encoding="utf-8") as out:
                    out.write(f"# {concept}\n\n{respuesta}\n")

if __name__ == "__main__":
    main()