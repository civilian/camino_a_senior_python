import os
from ebooklib import epub

CONCEPTOS_DIR = "conceptos"
WAR_TIME_MD = "conceptos_war_time.md"
OUTPUT_EPUB = "camino_a_senior_python.epub"
OUTPUT_PDF = "camino_a_senior_python.pdf"
OUTPUT_WAR_TIME_EPUB = "camino_a_senior_python_war_time.epub"

def get_sorted_md_files(directory):
    files = [f for f in os.listdir(directory) if f.endswith(".md")]
    return sorted(files)

def md_to_html(md_text):
    try:
        import markdown
    except ImportError:
        raise ImportError("Debes instalar el paquete 'markdown' (pip install markdown)")

    # Extensiones base (siempre disponibles)
    extensions = ['tables', 'fenced_code']

    # Intentar añadir codehilite si Pygments está disponible
    try:
        import pygments
        extensions.append('codehilite')
    except ImportError:
        pass

    md = markdown.Markdown(extensions=extensions)
    return md.convert(md_text)

def format_filename_to_title(fname):
    """Convierte el nombre de archivo a un título legible."""
    title = fname.replace(".md", "")
    title = title.replace("_", " ")
    title = title.title()
    return title

def parse_war_time_md():
    """
    Parsea conceptos_war_time.md.
    Retorna:
      (war_title, war_intro, [filenames], rest_title, rest_intro)
    o (None, None, [], None, None) si no existe.

    Estructura esperada del archivo:
      # Título sección war_time
      intro texto...
      # conceptos
      archivo1.md
      ...
      # Título sección resto
      intro texto resto...
    """
    if not os.path.exists(WAR_TIME_MD):
        return None, None, [], None, None
    with open(WAR_TIME_MD, encoding="utf-8") as f:
        content = f.read()

    war_title = ""
    war_intro_lines = []
    files = []
    rest_title = ""
    rest_intro_lines = []

    in_conceptos = False
    in_rest = False

    for line in content.split("\n"):
        stripped = line.strip()
        if stripped.startswith("# ") and not war_title:
            war_title = stripped[2:].strip()
        elif stripped == "# conceptos":
            in_conceptos = True
        elif in_conceptos and not in_rest:
            if stripped.startswith("# "):
                # Segunda sección: título del bloque "resto"
                in_rest = True
                rest_title = stripped[2:].strip()
            elif stripped and not stripped.startswith("#"):
                files.append(stripped)
        elif in_rest:
            rest_intro_lines.append(line)
        elif war_title and not in_conceptos:
            war_intro_lines.append(line)

    return (
        war_title,
        "\n".join(war_intro_lines).strip(),
        files,
        rest_title or None,
        "\n".join(rest_intro_lines).strip() or None,
    )

def get_ordered_files(all_files, war_time_files):
    """
    Devuelve los archivos reordenados:
      1. _introduccion.md (si existe)
      2. Archivos de war_time (en el orden del war_time md, solo los que existen)
      3. El resto en orden alfabético (sin duplicados)
    """
    all_set = set(all_files)
    existing_war = [f for f in war_time_files if f in all_set]
    war_set = set(existing_war)
    intro = [f for f in all_files if f == "_introduccion.md"]
    rest = [f for f in all_files if f not in war_set and f != "_introduccion.md"]
    return intro + existing_war + rest

def _make_separator_chapter(file_name, title, intro_text, border_color, epub_css, nav_css):
    """Crea un capítulo EPUB de separación de sección (sin contenido de archivo)."""
    intro_html = md_to_html(intro_text) if intro_text else ""
    html = (
        f'<html><head><style>{epub_css}</style></head><body>'
        f'<h1 style="text-align:center;color:#2c3e50;border-bottom:3px solid {border_color};padding-bottom:0.5em;">'
        f'{title}</h1>'
        f'{intro_html}'
        f'</body></html>'
    )
    chapter = epub.EpubHtml(title=title, file_name=file_name, lang="es")
    chapter.content = html
    chapter.add_item(nav_css)
    return chapter

def _build_epub_book(title, identifier, files, war_time_info, rest_section, epub_css):
    """
    Construye y retorna un EpubBook con los archivos dados.
    war_time_info: (war_title, war_intro_text, war_files_set) o None.
    rest_section:  (rest_title, rest_intro_text) o None — inyectado antes del primer archivo fuera de war_time.
    """
    book = epub.EpubBook()
    book.set_identifier(identifier)
    book.set_title(title)
    book.set_language("es")
    book.add_author("Generado automáticamente")

    nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=epub_css)
    book.add_item(nav_css)

    spine = ['nav']
    toc = []

    war_title, war_intro_text, war_files_set = war_time_info if war_time_info else (None, None, set())
    rest_title, rest_intro_text = rest_section if rest_section else (None, None)
    war_intro_inserted = False
    rest_intro_inserted = False

    for fname in files:
        # Inyectar separador war_time antes del primer archivo war_time
        if war_title and not war_intro_inserted and fname in war_files_set:
            ch = _make_separator_chapter(
                "_war_time_intro.xhtml",
                war_title, war_intro_text, "#e74c3c", epub_css, nav_css
            )
            book.add_item(ch)
            spine.append(ch)
            toc.append(ch)
            war_intro_inserted = True

        # Inyectar separador resto antes del primer archivo fuera de war_time (y fuera de _introduccion)
        if rest_title and not rest_intro_inserted and fname != "_introduccion.md" and fname not in war_files_set:
            ch = _make_separator_chapter(
                "_rest_intro.xhtml",
                rest_title, rest_intro_text, "#27ae60", epub_css, nav_css
            )
            book.add_item(ch)
            spine.append(ch)
            toc.append(ch)
            rest_intro_inserted = True

        path = os.path.join(CONCEPTOS_DIR, fname)
        with open(path, encoding="utf-8") as f:
            md_content = f.read()

        html_content = md_to_html(md_content)

        if fname == "_introduccion.md":
            full_html_content = f'<html><head><style>{epub_css}</style></head><body>{html_content}</body></html>'
        else:
            chapter_heading_title = format_filename_to_title(fname)
            intro_html = (
                f'<h1 style="text-align:center;margin-bottom:1em;color:#2c3e50;'
                f'border-bottom:3px solid #3498db;padding-bottom:0.5em;">'
                f'Introducción: {chapter_heading_title}</h1>'
            )
            full_html_content = f'<html><head><style>{epub_css}</style></head><body>{intro_html}{html_content}</body></html>'

        chapter_title = "Introducción" if fname == "_introduccion.md" else fname.replace("_", " ").replace(".md", "").title()
        chapter = epub.EpubHtml(title=chapter_title,
                                file_name=fname.replace(".md", ".xhtml"),
                                lang="es")
        chapter.content = full_html_content
        chapter.add_item(nav_css)
        book.add_item(chapter)
        spine.append(chapter)
        toc.append(chapter)

    book.toc = tuple(toc)
    book.spine = spine
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    return book

# CSS compartido para EPUB
EPUB_CSS = """
body {
    font-family: Georgia, serif;
    font-size: 1em;
    line-height: 1.6;
    color: #333;
    padding: 1em;
}
h1 {
    font-size: 1.8em;
    color: #2c3e50;
    margin-top: 1.5em;
    margin-bottom: 0.8em;
    border-bottom: 2px solid #3498db;
    padding-bottom: 0.3em;
}
h2 {
    font-size: 1.5em;
    color: #34495e;
    margin-top: 1.2em;
    margin-bottom: 0.6em;
}
h3 {
    font-size: 1.2em;
    color: #555;
    margin-top: 1em;
    margin-bottom: 0.5em;
}
code {
    background-color: #f4f4f4;
    padding: 2px 6px;
    border-radius: 3px;
    font-family: 'Courier New', 'Consolas', monospace;
    font-size: 0.9em;
    border: 1px solid #ddd;
}
pre {
    background-color: #f8f8f8;
    border: 1px solid #ddd;
    border-radius: 4px;
    padding: 12px;
    overflow-x: auto;
    font-size: 0.85em;
    line-height: 1.4;
}
pre code {
    background-color: transparent;
    padding: 0;
    border: none;
    display: block;
}
table {
    border-collapse: collapse;
    width: 100%;
    margin: 1em 0;
    font-size: 0.95em;
}
th, td {
    border: 1px solid #ddd;
    padding: 8px 12px;
    text-align: left;
}
th {
    background-color: #3498db;
    color: white;
    font-weight: bold;
}
tr:nth-child(even) {
    background-color: #f9f9f9;
}
blockquote {
    border-left: 4px solid #3498db;
    margin-left: 0;
    padding-left: 1em;
    color: #555;
    font-style: italic;
}
"""

def generate_epub(ordered_files, war_time_info=None, rest_section=None):
    """Genera el archivo EPUB principal."""
    print("📚 Generando EPUB...")
    war_files_set = set(war_time_info[2]) if war_time_info else set()
    book = _build_epub_book(
        title="Camino a Senior Python",
        identifier="camino-a-senior-python",
        files=ordered_files,
        war_time_info=(war_time_info[0], war_time_info[1], war_files_set) if war_time_info else None,
        rest_section=rest_section,
        epub_css=EPUB_CSS,
    )
    epub.write_epub(OUTPUT_EPUB, book, {})
    print(f"✅ EPUB generado: {OUTPUT_EPUB}")

def generate_war_time_epub(war_time_files, war_title, war_intro_text):
    """Genera el EPUB reducido con solo los conceptos war_time."""
    print("⚔️  Generando EPUB War Time...")
    all_set = set(f for f in os.listdir(CONCEPTOS_DIR) if f.endswith(".md"))
    existing_war = [f for f in war_time_files if f in all_set]

    if not existing_war:
        print("⚠️  No se encontraron archivos war_time en conceptos/. EPUB War Time no generado.")
        return

    # Para el war_time epub, el war_time_info hace que se inyecte el intro antes del primer capítulo
    war_files_set = set(existing_war)
    book = _build_epub_book(
        title=f"Camino a Senior Python — {war_title}",
        identifier="camino-a-senior-python-war-time",
        files=existing_war,
        war_time_info=(war_title, war_intro_text, war_files_set),
        rest_section=None,
        epub_css=EPUB_CSS,
    )
    epub.write_epub(OUTPUT_WAR_TIME_EPUB, book, {})
    print(f"✅ EPUB War Time generado: {OUTPUT_WAR_TIME_EPUB}")

def generate_pdf(ordered_files, war_time_info=None, rest_section=None):
    """Genera el archivo PDF."""
    print("📄 Generando PDF...")
    try:
        from weasyprint import HTML, CSS
        from weasyprint.text.fonts import FontConfiguration
    except ImportError:
        raise ImportError("Debes instalar el paquete 'weasyprint' (pip install weasyprint)")

    css_style = """
    @page {
        size: A4;
        margin: 2cm;
    }
    body {
        font-family: 'Georgia', 'Times New Roman', serif;
        font-size: 11pt;
        line-height: 1.6;
        color: #333;
    }
    h1 {
        font-size: 24pt;
        color: #2c3e50;
        margin-top: 2em;
        margin-bottom: 1em;
        page-break-after: avoid;
        border-bottom: 2px solid #3498db;
        padding-bottom: 0.5em;
    }
    h2 {
        font-size: 18pt;
        color: #34495e;
        margin-top: 1.5em;
        margin-bottom: 0.8em;
        page-break-after: avoid;
    }
    h3 {
        font-size: 14pt;
        color: #555;
        margin-top: 1.2em;
        margin-bottom: 0.6em;
        page-break-after: avoid;
    }
    h4 {
        font-size: 12pt;
        color: #666;
        margin-top: 1em;
        margin-bottom: 0.5em;
    }
    code {
        background-color: #f4f4f4;
        padding: 2px 6px;
        border-radius: 3px;
        font-family: 'Courier New', 'Consolas', 'Monaco', monospace;
        font-size: 10pt;
        border: 1px solid #ddd;
        display: inline-block;
    }
    pre {
        background-color: #f8f8f8;
        border: 1px solid #ddd;
        border-radius: 4px;
        padding: 12px;
        overflow-x: auto;
        overflow-y: hidden;
        page-break-inside: avoid;
        font-size: 9pt;
        line-height: 1.4;
        margin: 1em 0;
    }
    pre code {
        background-color: transparent;
        padding: 0;
        border: none;
        display: block;
        white-space: pre;
        overflow-x: auto;
    }
    .codehilite {
        background-color: #f8f8f8;
        border: 1px solid #ddd;
        border-radius: 4px;
        padding: 12px;
        overflow-x: auto;
        page-break-inside: avoid;
        font-size: 9pt;
        line-height: 1.4;
    }
    .codehilite code {
        background-color: transparent;
        padding: 0;
        border: none;
        display: block;
    }
    blockquote {
        border-left: 4px solid #3498db;
        margin-left: 0;
        padding-left: 1em;
        color: #555;
        font-style: italic;
    }
    table {
        border-collapse: collapse;
        width: 100%;
        margin: 1em 0;
        page-break-inside: avoid;
        font-size: 10pt;
        border: 1px solid #ddd;
    }
    th, td {
        border: 1px solid #ddd;
        padding: 8px 12px;
        text-align: left;
        vertical-align: top;
    }
    th {
        background-color: #3498db;
        color: white;
        font-weight: bold;
        text-align: left;
    }
    tr:nth-child(even) {
        background-color: #f9f9f9;
    }
    tr:hover {
        background-color: #f0f0f0;
    }
    ul, ol {
        margin: 0.5em 0;
        padding-left: 2em;
    }
    li {
        margin: 0.3em 0;
    }
    a {
        color: #3498db;
        text-decoration: none;
    }
    hr {
        border: none;
        border-top: 1px solid #ddd;
        margin: 2em 0;
    }
    """

    war_title, war_intro_text, war_files_list = war_time_info if war_time_info else (None, None, [])
    war_files_set = set(war_files_list)
    rest_title, rest_intro_text = rest_section if rest_section else (None, None)
    war_intro_inserted = False
    rest_intro_inserted = False


    html_parts = []
    html_parts.append("""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Camino a Senior Python</title>
    </head>
    <body>
    """)

    # Portada
    html_parts.append("""
    <div style="text-align: center; page-break-after: always; padding-top: 10cm;">
        <h1 style="font-size: 36pt; border: none; margin: 0;">Camino a Senior Python</h1>
        <p style="font-size: 18pt; margin-top: 2em; color: #666;">Guía Completa de Conceptos</p>
    </div>
    """)

    for fname in ordered_files:
        # Inyectar sección war_time antes del primer capítulo war_time
        if war_title and not war_intro_inserted and fname in war_files_set:
            html_parts.append('<div style="page-break-before: always;"></div>')
            war_intro_html = md_to_html(war_intro_text) if war_intro_text else ""
            html_parts.append(
                f'<h1 style="text-align:center;margin-top:2em;margin-bottom:1em;color:#2c3e50;'
                f'border-bottom:3px solid #e74c3c;padding-bottom:0.5em;">{war_title}</h1>'
                f'{war_intro_html}'
            )
            war_intro_inserted = True

        # Inyectar separador resto antes del primer capítulo fuera de war_time
        if rest_title and not rest_intro_inserted and fname != "_introduccion.md" and fname not in war_files_set:
            html_parts.append('<div style="page-break-before: always;"></div>')
            rest_intro_html = md_to_html(rest_intro_text) if rest_intro_text else ""
            html_parts.append(
                f'<h1 style="text-align:center;margin-top:2em;margin-bottom:1em;color:#2c3e50;'
                f'border-bottom:3px solid #27ae60;padding-bottom:0.5em;">{rest_title}</h1>'
                f'{rest_intro_html}'
            )
            rest_intro_inserted = True

        path = os.path.join(CONCEPTOS_DIR, fname)
        with open(path, encoding="utf-8") as f:
            md_content = f.read()

        html_parts.append('<div style="page-break-before: always;"></div>')
        html_content = md_to_html(md_content)

        if fname != "_introduccion.md":
            chapter_heading_title = format_filename_to_title(fname)
            html_parts.append(
                f'<h1 style="text-align:center;margin-top:2em;margin-bottom:1.5em;color:#2c3e50;'
                f'border-bottom:3px solid #3498db;padding-bottom:0.5em;">'
                f'Introducción: {chapter_heading_title}</h1>'
            )

        html_parts.append(html_content)

    html_parts.append("</body></html>")

    full_html = "\n".join(html_parts)

    font_config = FontConfiguration()
    html_doc = HTML(string=full_html)
    css_doc = CSS(string=css_style, font_config=font_config)

    html_doc.write_pdf(OUTPUT_PDF, stylesheets=[css_doc], font_config=font_config)
    print(f"✅ PDF generado: {OUTPUT_PDF}")

def main():
    """Función principal que genera ambos formatos."""
    if not os.path.exists(CONCEPTOS_DIR):
        print(f"❌ Error: No se encontró el directorio {CONCEPTOS_DIR}")
        return

    all_files = get_sorted_md_files(CONCEPTOS_DIR)
    if not all_files:
        print(f"❌ No se encontraron archivos .md en {CONCEPTOS_DIR}")
        return

    # Parsear war_time
    war_title, war_intro_text, war_files_list, rest_title, rest_intro_text = parse_war_time_md()
    war_time_info = (war_title, war_intro_text, war_files_list) if war_title else None
    rest_section = (rest_title, rest_intro_text) if rest_title else None

    # Reordenar: _introduccion → war_time files → resto
    if war_time_info:
        ordered_files = get_ordered_files(all_files, war_files_list)
        missing = [f for f in war_files_list if f not in set(all_files)]
        if missing:
            print(f"⚠️  Archivos war_time no encontrados en {CONCEPTOS_DIR}/: {missing}")
    else:
        ordered_files = all_files

    print(f"📁 Encontrados {len(all_files)} archivos en {CONCEPTOS_DIR}/")
    if war_time_info:
        existing_war = [f for f in war_files_list if f in set(all_files)]
        print(f"⚔️  War Time: {len(existing_war)} capítulos prioritarios")
    print("=" * 60)

    try:
        # Generar EPUB principal
        generate_epub(ordered_files, war_time_info=war_time_info, rest_section=rest_section)
        print()

        # Generar PDF principal
        generate_pdf(ordered_files, war_time_info=war_time_info, rest_section=rest_section)
        print()

        # Generar EPUB War Time (solo si hay war_time configurado)
        if war_time_info:
            generate_war_time_epub(war_files_list, war_title, war_intro_text)

        print("\n" + "=" * 60)
        print("✅ Proceso completado exitosamente")
        print(f"📚 EPUB: {OUTPUT_EPUB}")
        print(f"📄 PDF: {OUTPUT_PDF}")
        if war_time_info:
            print(f"⚔️  EPUB War Time: {OUTPUT_WAR_TIME_EPUB}")

    except ImportError as e:
        print(f"\n❌ Error de dependencias: {e}")
        print("\n💡 Instala las dependencias necesarias:")
        print("   pip install ebooklib markdown weasyprint")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
