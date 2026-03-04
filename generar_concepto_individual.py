#!/usr/bin/env python3
"""
Genera UN archivo de concepto (por ejemplo, un servicio de AWS)
con contenido largo + hook inicial, usando Gemini.

Uso:
    GOOGLE_API_KEY=xxxx python generar_concepto_individual.py "AWS Lambda"
"""

import os
import re
import sys
from pathlib import Path

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

OUTPUT_DIR = "conceptos"


def to_snake_case(text: str) -> str:
    text = text.strip().replace("/", " ")
    text = re.sub(r"[^\w\s]", "", text)
    text = re.sub(r"\s+", "_", text)
    return text.lower()


def get_gemini_concept(concept: str, llm: ChatGoogleGenerativeAI) -> str:
    """Reutiliza el mismo prompt profundo de genera_archivos_de_conceptos.py."""
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

- Profesional pero accesible
- Narrativa rica
- Analogías claras
- Explicación del "por qué"

## FORMATO

- Markdown completo con código Python funcional.

Ahora, crea la guía completa, exhaustiva y profunda sobre **{concept}**."""
    response = llm.invoke(prompt)
    return response.content if hasattr(response, "content") else str(response)


def generar_hook(contenido: str, titulo: str, llm: ChatGoogleGenerativeAI) -> str:
    """Genera un hook corto al inicio, reutilizando el estilo de limpiar_y_añadir_hooks_conceptos.py."""
    palabras = contenido.split()
    preview = " ".join(palabras[:1000])

    prompt = f"""Eres un experto en crear hooks (ganchos) para contenido educativo técnico. Tu tarea es crear un hook de 2-4 líneas que capture la atención y conecte con el contenido.

## INSTRUCCIONES:

1. El hook debe ser:
   - Amable y conversacional, como si hablaras con un colega
   - Conectar naturalmente con el contenido que sigue
   - Hacer una pregunta, plantear un problema o crear curiosidad
   - Específico al contenido sobre {titulo}

2. NO usar frases como:
   - "¡Absolutamente!"
   - "Ponte cómodo"
   - "Prepárate"
   - "Hoy vamos a aprender..."

3. Formato: 2-4 líneas en Markdown, sin explicaciones extras.

## CONTEXTO (primeras 1000 palabras):
{preview}

Responde SOLO con el hook."""

    response = llm.invoke(prompt)
    hook = response.content if hasattr(response, "content") else str(response)
    hook = hook.strip()
    hook = re.sub(r'^["\']|["\']$', '', hook)  # quitar comillas envolventes
    return hook.strip()


def main() -> None:
    if len(sys.argv) < 2:
        print("Uso: python generar_concepto_individual.py \"AWS\"")
        sys.exit(1)

    concepto = sys.argv[1].strip()
    load_dotenv()

    if not os.getenv("GOOGLE_API_KEY"):
        print("❌ Falta GOOGLE_API_KEY en el entorno o en .env")
        sys.exit(1)

    llm = ChatGoogleGenerativeAI(model="models/gemini-2.5-pro", temperature=0.5)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    filename = to_snake_case(concepto) + ".md"
    filepath = Path(OUTPUT_DIR) / filename

    print(f"🧠 Generando contenido para: {concepto}")
    cuerpo = get_gemini_concept(concepto, llm)

    print("🎣 Generando hook inicial...")
    hook = generar_hook(cuerpo, concepto, llm)

    contenido_final = f"{hook}\n\n# {concepto}\n\n{cuerpo}\n"
    filepath.write_text(contenido_final, encoding="utf-8")

    print(f"✅ Archivo generado: {filepath}")


if __name__ == "__main__":
    main()

