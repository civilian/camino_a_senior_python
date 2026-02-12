#!/usr/bin/env python3
"""
Script para dividir archivos de conceptos en scripts de video de 8 minutos usando Gemini.
Mantiene secciones completas y genera títulos representativos usando IA.
"""

import os
import re
from pathlib import Path
from typing import List, Dict, Any
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
import json

# Configuración
PALABRAS_POR_MINUTO = 160  # Velocidad de narración para video
MINUTOS_OBJETIVO = 8
PALABRAS_OBJETIVO = PALABRAS_POR_MINUTO * MINUTOS_OBJETIVO

CARPETA_CONCEPTOS = "conceptos"
CARPETA_VIDEOS = "videos_conceptos"


def contar_palabras(texto: str) -> int:
    """Cuenta las palabras en un texto, excluyendo código."""
    # Separar bloques de código
    partes = re.split(r'```[\s\S]*?```', texto)
    palabras = 0
    for parte in partes:
        # Contar palabras en texto normal
        palabras += len(re.findall(r'\b\w+\b', parte))
    return palabras


def dividir_con_gemini(contenido: str, titulo_principal: str, llm: ChatGoogleGenerativeAI) -> List[Dict[str, Any]]:
    """
    Usa Gemini para dividir el contenido en chunks de aproximadamente 8 minutos.
    Retorna una lista de diccionarios con 'titulo', 'contenido' y 'palabras'.
    """
    palabras_totales = contar_palabras(contenido)
    num_chunks_estimado = max(1, round(palabras_totales / PALABRAS_OBJETIVO))
    
    # Si el contenido es muy largo, necesitamos una estrategia diferente
    # Gemini tiene límites de tokens, así que para archivos muy grandes
    # podríamos necesitar dividir en múltiples llamadas
    
    prompt = f"""Eres un experto en crear scripts de video educativos. Tu tarea es dividir el siguiente contenido markdown en aproximadamente {num_chunks_estimado} partes, cada una de aproximadamente {PALABRAS_OBJETIVO} palabras (equivalente a {MINUTOS_OBJETIVO} minutos de narración).

## INSTRUCCIONES CRÍTICAS:

1. **NO RESUMAS NADA Y ELIMINA FRASES INTRODUCTORIAS COMUNES**: 
   - Debes mantener TODO el contenido original, palabra por palabra, sin omitir nada
   - EXCEPCIÓN: Elimina frases introductorias comunes como:
     * "¡Absolutamente!"
     * "Ponte cómodo"
     * "Acomódense"
     * "Prepárate para..."
     * "Hoy vamos a aprender..."
     * "Sírvete un café"
     * Cualquier frase que hable de prepararse para el video o el aprendizaje
   - Solo DIVIDE el contenido en partes, no lo resumas ni lo modifiques
   - Mantén el contenido técnico y educativo intacto

2. **Mantén secciones completas**: 
   - Nunca cortes una sección markdown (##, ###) a la mitad
   - Si una sección es muy larga (más de {int(PALABRAS_OBJETIVO * 1.3)} palabras), puedes dividirla en subsecciones, pero mantén la estructura de markdown intacta
   - Prioriza mantener secciones completas sobre el número exacto de palabras

3. **Objetivo de palabras por chunk**: 
   - Ideal: {PALABRAS_OBJETIVO} palabras por chunk ({MINUTOS_OBJETIVO} minutos)
   - Rango aceptable: {int(PALABRAS_OBJETIVO * 0.6)} a {int(PALABRAS_OBJETIVO * 1.4)} palabras
   - Es mejor tener chunks ligeramente más largos o cortos que cortar secciones

4. **Genera títulos representativos**: 
   - Cada chunk debe tener un título descriptivo y conciso (máximo 60 caracteres)
   - El título debe reflejar el contenido principal del chunk
   - Usa el título de la sección principal si es claro, o crea uno descriptivo

5. **HOOK OBLIGATORIO al inicio de cada chunk**: 
   - Cada chunk DEBE comenzar con un "hook" (gancho) de 2-4 líneas que capture la atención
   - El hook debe ser:
     * Amable y conversacional, como si estuvieras hablando con un colega
     * Conectar naturalmente con el contenido que sigue
     * Hacer una pregunta, plantear un problema, o crear curiosidad de forma natural
     * NO usar frases como "¡Absolutamente!", "Ponte cómodo", "Prepárate", "Acomódense", etc.
     * NO mencionar que es un video o que el espectador debe prepararse
     * Directo al punto, pero de forma amigable
   - Ejemplos de hooks BUENOS:
     * "¿Alguna vez te has preguntado por qué algunos sistemas fallan mientras otros resisten? La respuesta está en cómo manejamos la consistencia de los datos."
     * "Imagina que estás construyendo un sistema bancario. Un error podría costar millones. ¿Cómo garantizas que cada transacción sea perfecta?"
     * "En 2009, un bug en un sistema de trading causó pérdidas de 440 millones de dólares en 45 minutos. ¿Qué salió mal? Vamos a descubrirlo."
   - Ejemplos de hooks MALOS (NO usar):
     * "¡Absolutamente! Ponte cómodo y prepárate para aprender..."
     * "Acomódense, futuros arquitectos del software..."
     * "Hoy vamos a aprender sobre..."
   - El hook debe tener sentido con el contenido específico del chunk, no genérico
   - El hook debe estar en formato markdown, puede usar negritas o énfasis

6. **Estructura del contenido**: 
   - Cada chunk debe tener esta estructura:
     * Hook (2-4 líneas)
     * "# {titulo_principal}"
     * Todo el contenido markdown del chunk
   - Mantén la jerarquía de títulos (##, ###, ####) exactamente como está

7. **Preserva TODO el formato**: 
   - Mantén todos los bloques de código (```python ... ```) completos
   - Preserva listas, citas (>), tablas, enlaces, negritas, etc.
   - No modifiques el formato markdown de ninguna manera

8. **Formato de respuesta JSON**: Responde SOLO con un JSON válido, sin texto adicional. El formato exacto es:
{{
  "chunks": [
    {{
      "titulo": "Título descriptivo del chunk",
      "hook": "Hook de 2-4 líneas que capture la atención y conecte con el contenido. Debe ser provocativo, intrigante o crear curiosidad.",
      "contenido": "# {titulo_principal}\\n\\n[Todo el contenido markdown del chunk aquí, incluyendo títulos, texto, código, etc. sin modificar]",
      "palabras_estimadas": 1234
    }},
    {{
      "titulo": "Siguiente título",
      "hook": "Hook único para este chunk, relacionado con su contenido específico.",
      "contenido": "# {titulo_principal}\\n\\n[Contenido del siguiente chunk]",
      "palabras_estimadas": 1280
    }}
  ]
}}

## CONTENIDO A DIVIDIR:

{contenido}

## RECUERDA CRÍTICO:
- NO resumas, NO omitas, NO modifiques el contenido original
- ELIMINA frases como "¡Absolutamente!", "Ponte cómodo", "Acomódense", "Prepárate", etc.
- NO menciones que es un video o que el espectador debe prepararse
- Solo DIVIDE el contenido en partes
- Cada chunk DEBE tener un hook único, amable y que tenga sentido con su contenido específico
- El hook debe ser natural y conversacional, no genérico
- Mantén secciones completas
- Preserva TODO el formato markdown exactamente
- Responde SOLO con JSON válido, sin texto antes o después
"""

    try:
        response = llm.invoke(prompt)
        respuesta_texto = response.content if hasattr(response, "content") else str(response)
        
        # Limpiar la respuesta para extraer solo el JSON
        # Buscar el JSON entre ```json y ``` o directamente
        json_match = re.search(r'```json\s*(\{.*?\})\s*```', respuesta_texto, re.DOTALL)
        if json_match:
            json_str = json_match.group(1)
        else:
            # Intentar encontrar JSON directamente
            json_match = re.search(r'\{.*"chunks".*\}', respuesta_texto, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
            else:
                # Si no encuentra JSON, intentar parsear toda la respuesta
                json_str = respuesta_texto.strip()
        
        # Parsear JSON
        resultado = json.loads(json_str)
        
        # Validar y limpiar los chunks
        chunks_validos = []
        for chunk in resultado.get("chunks", []):
            titulo = chunk.get("titulo", "Sin título")
            hook = chunk.get("hook", "")
            contenido_chunk = chunk.get("contenido", "")
            palabras_est = chunk.get("palabras_estimadas", contar_palabras(contenido_chunk))
            
            # Limpiar el contenido del chunk de frases introductorias comunes
            contenido_limpio = contenido_chunk.strip()
            
            # Eliminar frases introductorias comunes al inicio
            frases_a_eliminar = [
                r'^¡Absolutamente![^\n]*\n',
                r'^Ponte cómodo[^\n]*\n',
                r'^Acomódense[^\n]*\n',
                r'^Prepárate[^\n]*\n',
                r'^Sírvete[^\n]*\n',
                r'^Hoy vamos a aprender[^\n]*\n',
                r'^Hoy no vamos a aprender[^\n]*\n',
            ]
            
            for patron in frases_a_eliminar:
                contenido_limpio = re.sub(patron, '', contenido_limpio, flags=re.IGNORECASE | re.MULTILINE)
            
            # Construir el contenido final con hook al inicio
            contenido_final = ""
            
            # Agregar hook si existe
            if hook.strip():
                contenido_final = f"{hook.strip()}\n\n"
            
            # Asegurar que el contenido tenga el título principal
            if not contenido_limpio.startswith(f"# {titulo_principal}"):
                contenido_final += f"# {titulo_principal}\n\n"
            
            # Agregar el contenido limpio del chunk
            contenido_final += contenido_limpio
            
            chunks_validos.append({
                "titulo": titulo,
                "hook": hook,
                "contenido": contenido_final,
                "palabras": palabras_est
            })
        
        return chunks_validos
        
    except json.JSONDecodeError as e:
        print(f"  ⚠️  Error parseando JSON de Gemini: {e}")
        print(f"  Respuesta recibida: {respuesta_texto[:500]}...")
        return []
    except Exception as e:
        print(f"  ⚠️  Error llamando a Gemini: {e}")
        return []


def generar_titulo_archivo(titulo_principal: str, titulo_chunk: str, num_chunk: int, total_chunks: int) -> str:
    """
    Genera un título representativo para el archivo de video.
    """
    # Limpiar título principal
    titulo_limpio = re.sub(r'[^\w\s-]', '', titulo_principal)
    titulo_limpio = re.sub(r'\s+', '_', titulo_limpio.strip())
    
    # Limpiar título del chunk
    titulo_chunk_limpio = re.sub(r'[^\w\s-]', '', titulo_chunk)
    titulo_chunk_limpio = re.sub(r'\s+', '_', titulo_chunk_limpio.strip())
    
    # Limitar longitud del título del chunk
    if len(titulo_chunk_limpio) > 50:
        titulo_chunk_limpio = titulo_chunk_limpio[:50]
    
    # Si hay múltiples chunks, agregar número
    if total_chunks > 1:
        return f"{titulo_limpio}_Parte_{num_chunk:02d}_{titulo_chunk_limpio}.md"
    else:
        return f"{titulo_limpio}.md"


def procesar_archivo(ruta_archivo: Path, carpeta_salida: Path, llm: ChatGoogleGenerativeAI) -> Dict[str, Any]:
    """
    Procesa un archivo de concepto y lo divide en scripts de video usando Gemini.
    """
    print(f"\nProcesando: {ruta_archivo.name}")
    
    # Leer archivo
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            contenido = f.read()
    except Exception as e:
        print(f"  ❌ Error leyendo archivo: {e}")
        return {"archivo": ruta_archivo.name, "chunks": 0, "error": str(e)}
    
    # Extraer título principal
    match_titulo = re.match(r'^#\s+(.+)$', contenido, re.MULTILINE)
    if match_titulo:
        titulo_principal = match_titulo.group(1).strip()
    else:
        titulo_principal = ruta_archivo.stem.replace('_', ' ').title()
    
    palabras_totales = contar_palabras(contenido)
    print(f"  📊 Total de palabras: {palabras_totales}")
    
    # Dividir usando Gemini
    print(f"  🤖 Consultando Gemini para dividir el contenido...")
    chunks = dividir_con_gemini(contenido, titulo_principal, llm)
    
    if not chunks:
        print(f"  ⚠️  No se pudieron generar chunks para {ruta_archivo.name}")
        return {"archivo": ruta_archivo.name, "chunks": 0, "error": "Error en Gemini"}
    
    print(f"  📦 Chunks generados: {len(chunks)}")
    
    # Generar archivos
    archivos_generados = []
    for i, chunk in enumerate(chunks, 1):
        titulo_chunk = chunk["titulo"]
        contenido_chunk = chunk["contenido"]
        palabras_chunk = chunk.get("palabras", contar_palabras(contenido_chunk))
        
        # Generar nombre de archivo
        nombre_archivo = generar_titulo_archivo(titulo_principal, titulo_chunk, i, len(chunks))
        ruta_salida = carpeta_salida / nombre_archivo
        
        # Guardar archivo
        try:
            with open(ruta_salida, 'w', encoding='utf-8') as f:
                f.write(contenido_chunk)
            
            minutos_estimados = palabras_chunk / PALABRAS_POR_MINUTO
            archivos_generados.append({
                "archivo": nombre_archivo,
                "palabras": palabras_chunk,
                "minutos": round(minutos_estimados, 1)
            })
            print(f"    ✓ {nombre_archivo} ({palabras_chunk} palabras, ~{minutos_estimados:.1f} min)")
        except Exception as e:
            print(f"    ❌ Error guardando {nombre_archivo}: {e}")
    
    return {
        "archivo": ruta_archivo.name,
        "chunks": len(chunks),
        "archivos_generados": archivos_generados
    }


def main():
    """Función principal."""
    # Cargar variables de entorno
    load_dotenv()
    
    # Verificar API key
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ Error: No se encontró GOOGLE_API_KEY en las variables de entorno")
        print("   Por favor, configura tu API key de Google en un archivo .env")
        return
    
    # Inicializar Gemini
    print("🤖 Inicializando Gemini...")
    llm = ChatGoogleGenerativeAI(
        model="models/gemini-2.5-pro",
        temperature=0.3  # Baja temperatura para respuestas más consistentes y estructuradas
    )
    
    # Crear carpeta de salida
    carpeta_salida = Path(CARPETA_VIDEOS)
    carpeta_salida.mkdir(exist_ok=True)
    
    # Obtener archivos de conceptos
    carpeta_conceptos = Path(CARPETA_CONCEPTOS)
    archivos = sorted(carpeta_conceptos.glob("*.md"))
    
    if not archivos:
        print(f"❌ No se encontraron archivos .md en {CARPETA_CONCEPTOS}/")
        return
    
    print(f"📚 Encontrados {len(archivos)} archivos en {CARPETA_CONCEPTOS}/")
    print(f"📁 Archivos de salida: {CARPETA_VIDEOS}/")
    print(f"⏱️  Objetivo: {MINUTOS_OBJETIVO} minutos por video (~{PALABRAS_OBJETIVO} palabras)")
    print("=" * 80)
    
    # Procesar cada archivo
    resultados = []
    for archivo in archivos:
        try:
            resultado = procesar_archivo(archivo, carpeta_salida, llm)
            resultados.append(resultado)
        except Exception as e:
            print(f"  ❌ Error procesando {archivo.name}: {e}")
            resultados.append({
                "archivo": archivo.name,
                "chunks": 0,
                "error": str(e)
            })
    
    # Resumen
    print("\n" + "=" * 80)
    print("📊 RESUMEN")
    print("=" * 80)
    total_chunks = sum(r.get("chunks", 0) for r in resultados)
    total_archivos = len([r for r in resultados if r.get("chunks", 0) > 0])
    print(f"✅ Archivos procesados: {total_archivos}/{len(archivos)}")
    print(f"📦 Total de scripts de video generados: {total_chunks}")
    print(f"📁 Carpeta de salida: {carpeta_salida.absolute()}")


if __name__ == "__main__":
    main()
