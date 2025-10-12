# Design Doc: Generador de Archivos de Conceptos desde Markdown

## Objetivo

Desarrollar un script en Python/langchain que lea un archivo Markdown (habilidades_python.md), extraiga cada concepto listado, y genere un archivo `.md` por concepto en una carpeta conceptos.  
Cada archivo debe tener el nombre del concepto en snake_case y contener la respuesta a esta pregunta, gemini de google debe contestar la pregunta en cada uno de los archivos:  
> "Enséñame sobre NOMBRE_DEL_ARCHIVO lo más profundo posible, lo suficiente para volverme senior en programación."
Donde NOMBRE_DEL_ARCHIVO es una variable que corresponde al nombre del archivo que se esta creando.

---

## Requerimientos

### Funcionales

- Leer el archivo habilidades_python.md línea por línea.
- Identificar líneas que representen conceptos (líneas que comienzan con `-`).
- Extraer el nombre del concepto de cada línea.
- Convertir el nombre del concepto a snake_case para el nombre del archivo.
- Crear un archivo `.md` por concepto en la carpeta conceptos.
- Escribir en cada archivo:
  - El nombre del concepto como título.
  - La pregunta para IA.

### No funcionales

- El script debe ser idempotente (puede ejecutarse varias veces sin efectos adversos).
- El script debe ser portable y ejecutarse en cualquier sistema operativo con Python 3.
- El código debe ser legible y fácil de mantener.

---

## Diseño

### Estructura de Archivos

```
/mnt/D/repos/camino_a_senior_python/
│
├─ habilidades_python.md
├─ genera_archivos_de_conceptos.py
└─ conceptos/
    ├─ python_core.md
    ├─ recursion.md
    └─ ...
```

### Lógica del Script

1. **Lectura del archivo fuente:**  
   Abrir y leer habilidades_python.md línea por línea.

2. **Identificación de conceptos:**  
   Considerar como concepto cualquier línea que comience con `-` y tenga más de 2 caracteres.

3. **Conversión a snake_case:**  
   - Eliminar caracteres especiales.
   - Reemplazar espacios y barras `/` por guiones bajos `_`.
   - Convertir a minúsculas.

4. **Creación de archivos:**  
   - Crear la carpeta conceptos si no existe.
   - Por cada concepto, crear un archivo `.md` con el nombre en snake_case.
   - Escribir el título y la pregunta para IA en el archivo.

---

## Ejemplo de Archivo Generado

**Entrada:**  
`- Object Oriented Programming (OOP)`

**Archivo generado:**  
`object_oriented_programming_oop.md`

**Contenido:**
```markdown
# Object Oriented Programming (OOP)

Enséñame sobre este tema lo más profundo posible, lo suficiente para volverme senior en programación.
```

---

## Consideraciones

- **Duplicados:** Si un concepto aparece más de una vez, el archivo se sobrescribirá.
- **Subcarpetas:** No se crean subcarpetas por sección, pero se puede extender fácilmente.
- **Extensibilidad:** El script puede adaptarse para incluir más información en los archivos generados.

---

## Futuras Mejoras

- Ignorar duplicados y no sobrescribir archivos existentes.
- Crear subcarpetas por sección del Markdown.
- Permitir personalizar el prompt para IA.
- Añadir logging y manejo de errores más robusto.

---

## Conclusión

Este script automatiza la generación de archivos de conceptos, facilitando el estudio y consulta de temas clave del ecosistema Python, y prepara cada archivo para ser usado como prompt para una IA educativa.