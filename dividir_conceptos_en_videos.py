#!/usr/bin/env python3
"""
Script para dividir archivos de conceptos en scripts de video de 8 minutos.
Mantiene secciones completas y genera títulos representativos.
"""

import os
import re
from pathlib import Path
from typing import List, Tuple, Dict

# Configuración
PALABRAS_POR_MINUTO = 160  # Velocidad de narración para video
MINUTOS_OBJETIVO = 8
PALABRAS_OBJETIVO = PALABRAS_POR_MINUTO * MINUTOS_OBJETIVO
TOLERANCIA_MIN = PALABRAS_OBJETIVO * 0.6  # Mínimo 60% del objetivo (4.8 min)
TOLERANCIA_MAX = PALABRAS_OBJETIVO * 1.4  # Máximo 140% del objetivo (11.2 min)

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


def extraer_secciones(markdown: str) -> List[Tuple[str, str, int]]:
    """
    Extrae secciones del markdown.
    Retorna lista de tuplas: (nivel, titulo, contenido, num_palabras)
    """
    lineas = markdown.split('\n')
    secciones = []
    seccion_actual = []
    nivel_actual = 0
    titulo_actual = ""
    contenido_previo = []
    
    i = 0
    while i < len(lineas):
        linea = lineas[i]
        
        # Detectar títulos
        match = re.match(r'^(#{1,6})\s+(.+)$', linea)
        if match:
            # Guardar sección anterior si existe
            if seccion_actual or contenido_previo:
                contenido_completo = '\n'.join(contenido_previo + seccion_actual)
                if contenido_completo.strip():
                    num_palabras = contar_palabras(contenido_completo)
                    secciones.append((nivel_actual, titulo_actual, contenido_completo, num_palabras))
            
            # Nueva sección
            nivel_actual = len(match.group(1))
            titulo_actual = match.group(2).strip()
            seccion_actual = [linea]
            contenido_previo = []
        else:
            if seccion_actual:
                seccion_actual.append(linea)
            else:
                contenido_previo.append(linea)
        
        i += 1
    
    # Guardar última sección
    if seccion_actual or contenido_previo:
        contenido_completo = '\n'.join(contenido_previo + seccion_actual)
        if contenido_completo.strip():
            num_palabras = contar_palabras(contenido_completo)
            secciones.append((nivel_actual, titulo_actual, contenido_completo, num_palabras))
    
    return secciones


def dividir_seccion_larga(contenido: str, titulo: str, nivel: int, num_palabras: int) -> List[Tuple[int, str, str, int]]:
    """
    Divide una sección muy larga en partes más pequeñas.
    Intenta dividir por párrafos o bloques de código.
    """
    if num_palabras <= PALABRAS_OBJETIVO:
        return [(nivel, titulo, contenido, num_palabras)]
    
    partes = []
    lineas = contenido.split('\n')
    parte_actual = []
    palabras_actual = 0
    num_parte = 1
    
    i = 0
    while i < len(lineas):
        linea = lineas[i]
        palabras_linea = contar_palabras(linea)
        
        # Si agregar esta línea excede el objetivo, guardar parte actual
        if palabras_actual + palabras_linea > PALABRAS_OBJETIVO and parte_actual:
            contenido_parte = '\n'.join(parte_actual)
            titulo_parte = f"{titulo} - Parte {num_parte}" if num_parte > 1 else titulo
            partes.append((nivel, titulo_parte, contenido_parte, palabras_actual))
            parte_actual = []
            palabras_actual = 0
            num_parte += 1
        
        parte_actual.append(linea)
        palabras_actual += palabras_linea
        i += 1
    
    # Guardar última parte
    if parte_actual:
        contenido_parte = '\n'.join(parte_actual)
        titulo_parte = f"{titulo} - Parte {num_parte}" if num_parte > 1 else titulo
        partes.append((nivel, titulo_parte, contenido_parte, palabras_actual))
    
    return partes


def agrupar_secciones(secciones: List[Tuple[int, str, str, int]]) -> List[Tuple[List[Tuple[int, str, str, int]], int, List[str]]]:
    """
    Agrupa secciones en chunks de aproximadamente 8 minutos.
    Mantiene secciones completas y evita chunks demasiado cortos o largos.
    """
    chunks = []
    chunk_actual = []
    palabras_chunk = 0
    titulos_chunk = []
    
    for nivel, titulo, contenido, num_palabras in secciones:
        # Si la sección es muy larga, dividirla primero
        if num_palabras > TOLERANCIA_MAX:
            subsecciones = dividir_seccion_larga(contenido, titulo, nivel, num_palabras)
            for sub_nivel, sub_titulo, sub_contenido, sub_palabras in subsecciones:
                # Intentar agregar al chunk actual
                if palabras_chunk + sub_palabras <= TOLERANCIA_MAX:
                    chunk_actual.append((sub_nivel, sub_titulo, sub_contenido, sub_palabras))
                    palabras_chunk += sub_palabras
                    titulos_chunk.append(sub_titulo)
                else:
                    # Guardar chunk actual y empezar uno nuevo
                    if chunk_actual:
                        chunks.append((chunk_actual, palabras_chunk, titulos_chunk))
                    chunk_actual = [(sub_nivel, sub_titulo, sub_contenido, sub_palabras)]
                    palabras_chunk = sub_palabras
                    titulos_chunk = [sub_titulo]
        else:
            # Intentar agregar al chunk actual
            if palabras_chunk + num_palabras <= TOLERANCIA_MAX:
                chunk_actual.append((nivel, titulo, contenido, num_palabras))
                palabras_chunk += num_palabras
                titulos_chunk.append(titulo)
            else:
                # Si el chunk actual es muy pequeño, intentar agregar de todas formas
                if palabras_chunk < TOLERANCIA_MIN and palabras_chunk + num_palabras <= TOLERANCIA_MAX * 1.2:
                    chunk_actual.append((nivel, titulo, contenido, num_palabras))
                    palabras_chunk += num_palabras
                    titulos_chunk.append(titulo)
                else:
                    # Guardar chunk actual y empezar uno nuevo
                    if chunk_actual:
                        chunks.append((chunk_actual, palabras_chunk, titulos_chunk))
                    chunk_actual = [(nivel, titulo, contenido, num_palabras)]
                    palabras_chunk = num_palabras
                    titulos_chunk = [titulo]
    
    # Guardar último chunk
    if chunk_actual:
        chunks.append((chunk_actual, palabras_chunk, titulos_chunk))
    
    return chunks


def generar_titulo_archivo(titulo_principal: str, titulos_secciones: List[str], num_chunk: int, total_chunks: int) -> str:
    """
    Genera un título representativo para el archivo de video.
    """
    # Limpiar título principal
    titulo_limpio = re.sub(r'[^\w\s-]', '', titulo_principal)
    titulo_limpio = re.sub(r'\s+', '_', titulo_limpio.strip())
    
    # Si hay múltiples chunks, agregar número
    if total_chunks > 1:
        # Intentar usar el primer título de sección principal como descriptor
        if titulos_secciones:
            primer_titulo = titulos_secciones[0]
            # Limpiar y acortar
            primer_titulo_limpio = re.sub(r'[^\w\s-]', '', primer_titulo)
            primer_titulo_limpio = re.sub(r'\s+', '_', primer_titulo_limpio.strip())
            # Limitar longitud
            if len(primer_titulo_limpio) > 40:
                primer_titulo_limpio = primer_titulo_limpio[:40]
            return f"{titulo_limpio}_Parte_{num_chunk:02d}_{primer_titulo_limpio}.md"
        else:
            return f"{titulo_limpio}_Parte_{num_chunk:02d}.md"
    else:
        return f"{titulo_limpio}.md"


def procesar_archivo(ruta_archivo: Path, carpeta_salida: Path) -> Dict[str, any]:
    """
    Procesa un archivo de concepto y lo divide en scripts de video.
    """
    print(f"\nProcesando: {ruta_archivo.name}")
    
    # Leer archivo
    with open(ruta_archivo, 'r', encoding='utf-8') as f:
        contenido = f.read()
    
    # Extraer título principal
    match_titulo = re.match(r'^#\s+(.+)$', contenido, re.MULTILINE)
    if match_titulo:
        titulo_principal = match_titulo.group(1).strip()
    else:
        titulo_principal = ruta_archivo.stem.replace('_', ' ').title()
    
    # Extraer secciones
    secciones = extraer_secciones(contenido)
    
    if not secciones:
        print(f"  ⚠️  No se encontraron secciones en {ruta_archivo.name}")
        return {"archivo": ruta_archivo.name, "chunks": 0, "error": "Sin secciones"}
    
    # Agrupar en chunks
    chunks = agrupar_secciones(secciones)
    
    print(f"  📊 Total de palabras: {sum(p for _, _, _, p in secciones)}")
    print(f"  📦 Chunks generados: {len(chunks)}")
    
    # Generar archivos
    archivos_generados = []
    for i, (chunk_secciones, palabras_total, titulos_secciones) in enumerate(chunks, 1):
        # Generar contenido del chunk
        contenido_chunk = []
        
        # Verificar si la primera sección ya incluye el título principal
        primera_seccion_es_titulo_principal = False
        if chunk_secciones:
            primer_nivel, primer_titulo, primer_contenido, _ = chunk_secciones[0]
            if primer_nivel == 1 and primer_titulo == titulo_principal:
                primera_seccion_es_titulo_principal = True
        
        # Solo agregar el título principal si no está en la primera sección
        if not primera_seccion_es_titulo_principal:
            contenido_chunk.append(f"# {titulo_principal}")
            contenido_chunk.append("")
        
        # Agregar contenido de las secciones
        for nivel, titulo, contenido, _ in chunk_secciones:
            if contenido.strip():
                contenido_chunk.append(contenido)
                contenido_chunk.append("")
        
        contenido_final = '\n'.join(contenido_chunk)
        
        # Generar nombre de archivo
        nombre_archivo = generar_titulo_archivo(titulo_principal, titulos_secciones, i, len(chunks))
        ruta_salida = carpeta_salida / nombre_archivo
        
        # Guardar archivo
        with open(ruta_salida, 'w', encoding='utf-8') as f:
            f.write(contenido_final)
        
        minutos_estimados = palabras_total / PALABRAS_POR_MINUTO
        archivos_generados.append({
            "archivo": nombre_archivo,
            "palabras": palabras_total,
            "minutos": round(minutos_estimados, 1)
        })
        print(f"    ✓ {nombre_archivo} ({palabras_total} palabras, ~{minutos_estimados:.1f} min)")
    
    return {
        "archivo": ruta_archivo.name,
        "chunks": len(chunks),
        "archivos_generados": archivos_generados
    }


def main():
    """Función principal."""
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
            resultado = procesar_archivo(archivo, carpeta_salida)
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
