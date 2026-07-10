import sqlite3
import os
import re
import unicodedata

try:
    from striprtf.striprtf import rtf_to_text
    HAS_STRIPRTF = True
except ImportError:
    HAS_STRIPRTF = False

db_path = r"C:\Users\lfeli\OneDrive\Estudios Felipe Torres\MATERIAL\Neurona\Materiales PDF\02CCCB-WaltonKeener.cmti"
out_dir = r"C:\Users\lfeli\OneDrive\Estudios Felipe Torres\MATERIAL\Neurona\NeuronaBiblica\02_Exegesis\Contexto_Cultural_Walton_Keener"

os.makedirs(out_dir, exist_ok=True)

bible_books = {
    1: "Génesis", 2: "Éxodo", 3: "Levítico", 4: "Números", 5: "Deuteronomio",
    6: "Josué", 7: "Jueces", 8: "Rut", 9: "1 Samuel", 10: "2 Samuel",
    11: "1 Reyes", 12: "2 Reyes", 13: "1 Crónicas", 14: "2 Crónicas", 15: "Esdras",
    16: "Nehemías", 17: "Ester", 18: "Job", 19: "Salmos", 20: "Proverbios",
    21: "Eclesiastés", 22: "Cantares", 23: "Isaías", 24: "Jeremías", 25: "Lamentaciones",
    26: "Ezequiel", 27: "Daniel", 28: "Oseas", 29: "Joel", 30: "Amós",
    31: "Abdías", 32: "Jonás", 33: "Miqueas", 34: "Nahúm", 35: "Habacuc",
    36: "Sofonías", 37: "Hageo", 38: "Zacarías", 39: "Malaquías",
    40: "Mateo", 41: "Marcos", 42: "Lucas", 43: "Juan", 44: "Hechos",
    45: "Romanos", 46: "1 Corintios", 47: "2 Corintios", 48: "Gálatas",
    49: "Efesios", 50: "Filipenses", 51: "Colosenses", 52: "1 Tesalonicenses",
    53: "2 Tesalonicenses", 54: "1 Timoteo", 55: "2 Timoteo", 56: "Tito",
    57: "Filemón", 58: "Hebreos", 59: "Santiago", 60: "1 Pedro", 61: "2 Pedro",
    62: "1 Juan", 63: "2 Juan", 64: "3 Juan", 65: "Judas", 66: "Apocalipsis"
}

def sanitize(name):
    nfkd = unicodedata.normalize('NFKD', name)
    ascii_only = nfkd.encode('ASCII', 'ignore').decode('utf-8')
    return ascii_only.replace(' ', '_')

def clean_rtf(text):
    if not text:
        return ""
    # Try striprtf first
    if HAS_STRIPRTF:
        try:
            # Wrap in proper RTF header if missing
            if not text.strip().startswith(r'{\rtf'):
                text = r'{\rtf1\ansi ' + text + '}'
            cleaned = rtf_to_text(text)
            return cleaned.strip()
        except Exception:
            pass
    # Fallback: manual RTF cleaning
    text = re.sub(r'\{\\[^}]*\}', '', text)
    text = re.sub(r'\\[a-zA-Z0-9]+\s?', '', text)
    text = re.sub(r'[{}]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def clean_html(text):
    if not text:
        return ""
    # Sometimes MySword uses HTML instead of RTF
    text = re.sub(r'<[^>]+>', '', text)
    return text.strip()

def process_text(text):
    # Some commentaries are RTF, some are HTML, some are plain text.
    if text.strip().startswith(r'{\rtf'):
        return clean_rtf(text)
    elif '<' in text and '>' in text:
        return clean_html(text)
    else:
        return text.strip()

def add_backlinks(text):
    """Wrap bible references and key concepts in [[]] backlinks"""
    # Strong codes
    text = re.sub(r'(?<!\[\[)\b([GH]\d{1,4})\b(?!\]\])', r'[[\1]]', text)
    return text

def process_commentary():
    conn = sqlite3.connect(db_path)
    
    # Check if table VerseCommentary exists, if not maybe just Verses (different versions)
    # The user check showed: 'VerseCommentary', 'ChapterCommentary', 'BookCommentary'
    
    # Get book introductions
    books_data = {}
    try:
        books_rows = conn.execute("SELECT Book, Comments FROM BookCommentary").fetchall()
        for row in books_rows:
            book_id = row[0]
            intro = process_text(row[1]) if row[1] else ""
            books_data[book_id] = intro
    except sqlite3.OperationalError:
        pass # Table might not exist or be empty
    
    # Get all verse comments
    try:
        verses = conn.execute(
            "SELECT Book, ChapterBegin, VerseBegin, VerseEnd, Comments FROM VerseCommentary ORDER BY Book, ChapterBegin, VerseBegin"
        ).fetchall()
    except sqlite3.OperationalError:
        verses = []
    
    # Group by book
    from collections import defaultdict
    book_verses = defaultdict(list)
    for v in verses:
        book_id, chap, v_from, v_to, comment = v
        book_verses[book_id].append((chap, v_from, v_to, comment))
    
    index_lines = [
        "---",
        "titulo: Índice del Comentario de Contexto Cultural",
        "tipo: indice_maestro",
        "autor: John H. Walton y Craig S. Keener",
        "estado: Procesado",
        "etiquetas: [\"#Comentario\", \"#Exegesis\", \"#ContextoCultural\", \"#AntiguoTestamento\", \"#NuevoTestamento\"]",
        "---",
        "",
        "# Comentario del Contexto Cultural de la Biblia",
        "## John H. Walton y Craig S. Keener",
        "",
        "Comentario del trasfondo histórico y cultural de cada versículo de la Biblia.",
        ""
    ]
    
    total_files = 0
    
    for book_id in sorted(book_verses.keys()):
        book_name = bible_books.get(book_id, f"Libro_{book_id}")
        safe_name = sanitize(book_name)
        
        # Group verses by chapter
        chapters = defaultdict(list)
        for chap, v_from, v_to, comment in book_verses[book_id]:
            chapters[chap].append((v_from, v_to, comment))
        
        # Create a sub-index for this book
        book_index_lines = [
            "---",
            f"titulo: Contexto Cultural de {book_name}",
            "tipo: indice_libro",
            f"autor: Walton y Keener",
            "estado: Procesado",
            f"etiquetas: [\"#Comentario\", \"#ContextoCultural\", \"#{safe_name}\"]",
            "---",
            "",
            f"# Contexto Cultural de [[{book_name}]]",
            ""
        ]
        
        if book_id in books_data and books_data[book_id]:
            book_index_lines.append("## Introducción")
            book_index_lines.append(add_backlinks(books_data[book_id]))
            book_index_lines.append("")
        
        book_index_lines.append("## Capítulos")
        
        for chap_num in sorted(chapters.keys()):
            chap_file = f"ContextoCultural_{safe_name}_Cap_{chap_num:02d}"
            book_index_lines.append(f"- [[{chap_file}]]")
            
            # Write chapter file
            chap_content = [
                "---",
                f"titulo: Contexto Cultural de {book_name} {chap_num}",
                "tipo: comentario_cultural",
                f"autor: Walton y Keener",
                "estado: Procesado",
                f"etiquetas: [\"#Comentario\", \"#ContextoCultural\", \"#{safe_name}\"]",
                "---",
                "",
                f"# Contexto Cultural de [[{book_name}]] - Capítulo {chap_num}",
                ""
            ]
            
            for v_from, v_to, comment in sorted(chapters[chap_num]):
                cleaned = process_text(comment)
                cleaned = add_backlinks(cleaned)
                if v_from == v_to:
                    chap_content.append(f"### {book_name} {chap_num}:{v_from}")
                else:
                    chap_content.append(f"### {book_name} {chap_num}:{v_from}-{v_to}")
                chap_content.append(cleaned)
                chap_content.append("")
            
            chap_path = os.path.join(out_dir, f"{chap_file}.md")
            with open(chap_path, "w", encoding="utf-8") as f:
                f.write("\n".join(chap_content))
            total_files += 1
        
        book_idx_path = os.path.join(out_dir, f"00_Indice_CCCB_{safe_name}.md")
        with open(book_idx_path, "w", encoding="utf-8") as f:
            f.write("\n".join(book_index_lines))
        total_files += 1
        
        index_lines.append(f"- [[00_Indice_CCCB_{safe_name}|{book_name}]]")
    
    # Write master index
    idx_path = os.path.join(out_dir, "00_Indice_Contexto_Cultural.md")
    with open(idx_path, "w", encoding="utf-8") as f:
        f.write("\n".join(index_lines))
    total_files += 1
    
    print(f"Procesamiento completado: {total_files} archivos generados.")
    print(f"Versículos comentados: {len(verses)}")
    print(f"Libros procesados: {len(book_verses)}")
    
    conn.close()

if __name__ == "__main__":
    process_commentary()
