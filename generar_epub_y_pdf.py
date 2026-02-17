import os
from ebooklib import epub

CONCEPTOS_DIR = "conceptos"
OUTPUT_EPUB = "camino_a_senior_python.epub"
OUTPUT_PDF = "camino_a_senior_python.pdf"

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
        # Si Pygments no está instalado, usar fenced_code sin resaltado
        pass
    
    # Usar extensiones para tablas y código
    md = markdown.Markdown(extensions=extensions)
    return md.convert(md_text)

def format_filename_to_title(fname):
    """Convierte el nombre de archivo a un título legible."""
    # Remover extensión .md
    title = fname.replace(".md", "")
    # Reemplazar guiones bajos con espacios
    title = title.replace("_", " ")
    # Capitalizar cada palabra
    title = title.title()
    return title

def generate_epub(files):
    """Genera el archivo EPUB."""
    print("📚 Generando EPUB...")
    book = epub.EpubBook()
    book.set_identifier("camino-a-senior-python")
    book.set_title("Camino a Senior Python")
    book.set_language("es")
    book.add_author("Generado automáticamente")

    # CSS para mejorar el formato en EPUB
    epub_css = """
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
    
    # Añadir CSS al libro
    nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=epub_css)
    book.add_item(nav_css)

    spine = ['nav']
    toc = []

    for fname in files:
        path = os.path.join(CONCEPTOS_DIR, fname)
        with open(path, encoding="utf-8") as f:
            md_content = f.read()
        
        # Formatear título de introducción
        intro_title = format_filename_to_title(fname)
        
        # Añadir título de introducción antes del contenido
        intro_html = f'<h1 style="text-align: center; margin-bottom: 1em; color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 0.5em;">Introducción: {intro_title}</h1>'
        
        html_content = md_to_html(md_content)
        # Combinar título de introducción con el contenido y envolver en div con estilos
        full_html_content = f'<html><head><style>{epub_css}</style></head><body>{intro_html}{html_content}</body></html>'
        
        chapter = epub.EpubHtml(title=fname.replace("_", " ").replace(".md", "").title(),
                                file_name=fname.replace(".md", ".xhtml"),
                                lang="es")
        chapter.content = full_html_content
        chapter.add_item(nav_css)
        book.add_item(chapter)
        spine.append(chapter)
        toc.append(chapter)

    # Agregar tabla de contenido y navegación
    book.toc = tuple(toc)
    book.spine = spine
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    epub.write_epub(OUTPUT_EPUB, book, {})
    print(f"✅ EPUB generado: {OUTPUT_EPUB}")

def generate_pdf(files):
    """Genera el archivo PDF."""
    print("📄 Generando PDF...")
    try:
        from weasyprint import HTML, CSS
        from weasyprint.text.fonts import FontConfiguration
    except ImportError:
        raise ImportError("Debes instalar el paquete 'weasyprint' (pip install weasyprint)")
    
    # CSS para mejorar el estilo del PDF
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
    
    # Construir HTML completo con todos los capítulos
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
    
    # Agregar portada
    html_parts.append("""
    <div style="text-align: center; page-break-after: always; padding-top: 10cm;">
        <h1 style="font-size: 36pt; border: none; margin: 0;">Camino a Senior Python</h1>
        <p style="font-size: 18pt; margin-top: 2em; color: #666;">Guía Completa de Conceptos</p>
    </div>
    """)
    
    # Agregar cada archivo como capítulo
    for fname in files:
        path = os.path.join(CONCEPTOS_DIR, fname)
        with open(path, encoding="utf-8") as f:
            md_content = f.read()
        
        # Formatear título de introducción
        intro_title = format_filename_to_title(fname)
        
        # Agregar salto de página antes de cada capítulo (excepto el primero)
        if len(html_parts) > 1:  # Ya hay contenido (portada)
            html_parts.append('<div style="page-break-before: always;"></div>')
        
        # Añadir título de introducción
        html_parts.append(f'<h1 style="text-align: center; margin-top: 2em; margin-bottom: 1.5em; color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 0.5em;">Introducción: {intro_title}</h1>')
        
        html_content = md_to_html(md_content)
        html_parts.append(html_content)
    
    html_parts.append("</body></html>")
    
    full_html = "\n".join(html_parts)
    
    # Generar PDF
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
    
    files = get_sorted_md_files(CONCEPTOS_DIR)
    if not files:
        print(f"❌ No se encontraron archivos .md en {CONCEPTOS_DIR}")
        return
    
    print(f"📁 Encontrados {len(files)} archivos en {CONCEPTOS_DIR}/")
    print("=" * 60)
    
    try:
        # Generar EPUB
        generate_epub(files)
        print()
        
        # Generar PDF
        generate_pdf(files)
        
        print("\n" + "=" * 60)
        print("✅ Proceso completado exitosamente")
        print(f"📚 EPUB: {OUTPUT_EPUB}")
        print(f"📄 PDF: {OUTPUT_PDF}")
        
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
