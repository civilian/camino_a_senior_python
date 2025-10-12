import os
from ebooklib import epub

CONCEPTOS_DIR = "conceptos"
OUTPUT_FILE = "camino_a_senior_python.epub"

def get_sorted_md_files(directory):
    files = [f for f in os.listdir(directory) if f.endswith(".md")]
    return sorted(files)

def md_to_html(md_text):
    try:
        import markdown
    except ImportError:
        raise ImportError("Debes instalar el paquete 'markdown' (pip install markdown)")
    return markdown.markdown(md_text)

def main():
    book = epub.EpubBook()
    book.set_identifier("camino-a-senior-python")
    book.set_title("Camino a Senior Python")
    book.set_language("es")
    book.add_author("Generado automáticamente")

    spine = ['nav']
    toc = []

    files = get_sorted_md_files(CONCEPTOS_DIR)
    for fname in files:
        path = os.path.join(CONCEPTOS_DIR, fname)
        with open(path, encoding="utf-8") as f:
            md_content = f.read()
        html_content = md_to_html(md_content)
        chapter = epub.EpubHtml(title=fname.replace("_", " ").replace(".md", "").title(),
                                file_name=fname.replace(".md", ".xhtml"),
                                lang="es")
        chapter.content = html_content
        book.add_item(chapter)
        spine.append(chapter)
        toc.append(chapter)

    # Agregar tabla de contenido y navegación
    book.toc = tuple(toc)
    book.spine = spine
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    epub.write_epub(OUTPUT_FILE, book, {})

if __name__ == "__main__":
    main()