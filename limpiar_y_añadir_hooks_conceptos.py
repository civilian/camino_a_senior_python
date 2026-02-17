#!/usr/bin/env python3
"""
Script para limpiar archivos de conceptos: eliminar frases introductorias
y añadir hooks al inicio usando Gemini.
Modifica los archivos originales sin crear nuevos.
"""

import os
import re
from pathlib import Path
from typing import Dict, Any
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

# Configuración
CARPETA_CONCEPTOS = "conceptos"


def eliminar_frases_introductorias(contenido: str) -> str:
    """
    Elimina frases introductorias comunes del contenido.
    """
    contenido_limpio = contenido.strip()
    
    # Patrones de frases a eliminar (al inicio del contenido o después de saltos de línea)
    frases_a_eliminar = [
        r'^¡Absolutamente![^\n]*\n',
        r'^Ponte cómodo[^\n]*\n',
        r'^Acomódense[^\n]*\n',
        r'^Prepárate[^\n]*\n',
        r'^Sírvete[^\n]*\n',
        r'^Hoy vamos a aprender[^\n]*\n',
        r'^Hoy no vamos a aprender[^\n]*\n',
        r'^Prepárate para[^\n]*\n',
        r'^Acomódate[^\n]*\n',
        r'^Antes de comenzar[^\n]*\n',
        r'^Antes de empezar[^\n]*\n',
    ]
    
    # Eliminar frases al inicio
    for patron in frases_a_eliminar:
        contenido_limpio = re.sub(patron, '', contenido_limpio, flags=re.IGNORECASE | re.MULTILINE)
    
    # Eliminar líneas vacías múltiples al inicio
    contenido_limpio = re.sub(r'^\n{2,}', '\n', contenido_limpio)
    
    return contenido_limpio.strip()


def generar_hook_con_gemini(contenido: str, titulo_principal: str, llm: ChatGoogleGenerativeAI) -> str:
    """
    Genera un hook apropiado para el contenido usando Gemini.
    """
    # Obtener las primeras 1000 palabras para dar contexto a Gemini
    palabras = contenido.split()
    preview = ' '.join(palabras[:1000])
    
    prompt = f"""Eres un experto en crear hooks (ganchos) para contenido educativo técnico. Tu tarea es crear un hook de 2-4 líneas que capture la atención y conecte con el contenido.

## INSTRUCCIONES:

1. **El hook debe ser**:
   - Amable y conversacional, como si estuvieras hablando con un colega
   - Conectar naturalmente con el contenido que sigue
   - Hacer una pregunta, plantear un problema, o crear curiosidad de forma natural
   - Directo al punto, pero de forma amigable
   - Específico al contenido, no genérico

2. **NO usar**:
   - "¡Absolutamente!"
   - "Ponte cómodo"
   - "Prepárate"
   - "Acomódense"
   - "Hoy vamos a aprender..."
   - Cualquier frase que hable de prepararse para el video o el aprendizaje
   - Menciones de que es un video o que el espectador debe prepararse

3. **Ejemplos de hooks BUENOS**:
   - "¿Alguna vez te has preguntado por qué algunos sistemas fallan mientras otros resisten? La respuesta está en cómo manejamos la consistencia de los datos."
   - "Imagina que estás construyendo un sistema bancario. Un error podría costar millones. ¿Cómo garantizas que cada transacción sea perfecta?"
   - "En 2009, un bug en un sistema de trading causó pérdidas de 440 millones de dólares en 45 minutos. ¿Qué salió mal? Vamos a descubrirlo."

4. **Ejemplos de hooks MALOS (NO usar)**:
   - "¡Absolutamente! Ponte cómodo y prepárate para aprender..."
   - "Acomódense, futuros arquitectos del software..."
   - "Hoy vamos a aprender sobre..."

5. **Formato**: El hook debe estar en formato markdown, puede usar negritas o énfasis si es apropiado.

## CONTEXTO:

**Título del contenido**: {titulo_principal}

**Preview del contenido** (primeras 1000 palabras):
{preview}

## TAREA:

Genera UN hook de 2-4 líneas que sea específico para este contenido sobre {titulo_principal}. El hook debe ser provocativo, intrigante o crear curiosidad de forma natural.

Responde SOLO con el hook, sin texto adicional, sin explicaciones, sin comillas alrededor. Solo el texto del hook.
"""

    try:
        response = llm.invoke(prompt)
        hook = response.content if hasattr(response, "content") else str(response)
        
        # Limpiar el hook de posibles comillas o texto adicional
        hook = hook.strip()
        hook = re.sub(r'^["\']|["\']$', '', hook)  # Eliminar comillas al inicio/fin
        hook = re.sub(r'^Hook:\s*', '', hook, flags=re.IGNORECASE)
        hook = re.sub(r'^```.*?\n', '', hook, flags=re.DOTALL)
        hook = re.sub(r'\n```.*?$', '', hook, flags=re.DOTALL)
        
        return hook.strip()
        
    except Exception as e:
        print(f"  ⚠️  Error generando hook con Gemini: {e}")
        return ""


def procesar_archivo(ruta_archivo: Path, llm: ChatGoogleGenerativeAI) -> Dict[str, Any]:
    """
    Procesa un archivo de concepto: elimina frases introductorias y añade hook.
    Modifica el archivo original.
    """
    print(f"\nProcesando: {ruta_archivo.name}")
    
    # Leer archivo
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            contenido_original = f.read()
    except Exception as e:
        print(f"  ❌ Error leyendo archivo: {e}")
        return {"archivo": ruta_archivo.name, "exito": False, "error": str(e)}
    
    # Extraer título principal
    match_titulo = re.match(r'^#\s+(.+)$', contenido_original, re.MULTILINE)
    if match_titulo:
        titulo_principal = match_titulo.group(1).strip()
    else:
        titulo_principal = ruta_archivo.stem.replace('_', ' ').title()
    
    print(f"  📝 Título: {titulo_principal}")
    
    # Eliminar frases introductorias
    print(f"  🧹 Eliminando frases introductorias...")
    contenido_limpio = eliminar_frases_introductorias(contenido_original)
    
    # Verificar si ya tiene un hook al inicio
    # Un hook típicamente está antes del título principal
    tiene_hook = False
    if contenido_limpio.startswith("#"):
        # Si empieza directamente con el título, no tiene hook
        tiene_hook = False
    else:
        # Verificar si hay texto antes del título que parezca un hook
        match_titulo_limpio = re.search(r'^#\s+', contenido_limpio, re.MULTILINE)
        if match_titulo_limpio:
            texto_antes = contenido_limpio[:match_titulo_limpio.start()].strip()
            # Si hay texto antes del título y no es muy largo, podría ser un hook existente
            if texto_antes and len(texto_antes.split('\n')) <= 5:
                tiene_hook = True
                print(f"  ℹ️  El archivo ya tiene un hook. Se generará uno nuevo.")
    
    # Generar hook con Gemini
    print(f"  🤖 Generando hook con Gemini...")
    hook = generar_hook_con_gemini(contenido_limpio, titulo_principal, llm)
    
    if not hook:
        print(f"  ⚠️  No se pudo generar hook. Continuando sin hook...")
        contenido_final = contenido_limpio
    else:
        print(f"  ✓ Hook generado: {hook[:80]}...")
        
        # Construir contenido final con hook
        # Si el contenido ya tiene el título principal al inicio, añadir hook antes
        if contenido_limpio.startswith(f"# {titulo_principal}"):
            contenido_final = f"{hook}\n\n{contenido_limpio}"
        elif re.match(r'^#\s+', contenido_limpio, re.MULTILINE):
            # Hay un título pero no es el principal, añadir hook al inicio
            contenido_final = f"{hook}\n\n{contenido_limpio}"
        else:
            # No hay título claro, añadir título y hook
            contenido_final = f"{hook}\n\n# {titulo_principal}\n\n{contenido_limpio}"
    
    # Guardar archivo modificado
    try:
        with open(ruta_archivo, 'w', encoding='utf-8') as f:
            f.write(contenido_final)
        print(f"  ✅ Archivo modificado exitosamente")
        return {
            "archivo": ruta_archivo.name,
            "exito": True,
            "hook_generado": bool(hook),
            "tiene_hook_previo": tiene_hook
        }
    except Exception as e:
        print(f"  ❌ Error guardando archivo: {e}")
        return {"archivo": ruta_archivo.name, "exito": False, "error": str(e)}


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
        temperature=0.3
    )
    
    # Obtener archivos de conceptos
    carpeta_conceptos = Path(CARPETA_CONCEPTOS)
    archivos = sorted(carpeta_conceptos.glob("*.md"))
    
    if not archivos:
        print(f"❌ No se encontraron archivos .md en {CARPETA_CONCEPTOS}/")
        return
    
    print(f"📚 Encontrados {len(archivos)} archivos en {CARPETA_CONCEPTOS}/")
    print("=" * 80)
    print("⚠️  ADVERTENCIA: Este script MODIFICARÁ los archivos originales")
    print("=" * 80)
    
    # Procesar cada archivo
    resultados = []
    for archivo in archivos:
        try:
            resultado = procesar_archivo(archivo, llm)
            resultados.append(resultado)
        except Exception as e:
            print(f"  ❌ Error procesando {archivo.name}: {e}")
            resultados.append({
                "archivo": archivo.name,
                "exito": False,
                "error": str(e)
            })
    
    # Resumen
    print("\n" + "=" * 80)
    print("📊 RESUMEN")
    print("=" * 80)
    archivos_exitosos = len([r for r in resultados if r.get("exito", False)])
    archivos_con_error = len([r for r in resultados if r.get("error")])
    hooks_generados = len([r for r in resultados if r.get("hook_generado", False)])
    
    print(f"✅ Archivos procesados exitosamente: {archivos_exitosos}/{len(archivos)}")
    if archivos_con_error > 0:
        print(f"❌ Archivos con error: {archivos_con_error}")
    print(f"🎣 Hooks generados: {hooks_generados}")
    print(f"📁 Carpeta procesada: {carpeta_conceptos.absolute()}")
    
    # Mostrar archivos con error si los hay
    if archivos_con_error > 0:
        print("\n❌ Archivos con error:")
        for r in resultados:
            if r.get("error"):
                print(f"   - {r['archivo']}: {r.get('error', 'Error desconocido')}")


if __name__ == "__main__":
    main()
