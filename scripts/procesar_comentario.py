import sqlite3
import os
import re
import unicodedata

try:
    from striprtf.striprtf import rtf_to_text
    HAS_STRIPRTF = True
except ImportError:
    HAS_STRIPRTF = False

db_path = r"C:\Users\lfeli\OneDrive\Estudios Felipe Torres\MATERIAL\Neurona\Materiales PDF\WP-BR Comentario Al NT Por Partain - Reeves.cmtx"
out_dir = r"C:\Users\lfeli\OneDrive\Estudios Felipe Torres\MATERIAL\Neurona\NeuronaBiblica\02_Exegesis\Comentario_Partain_Reeves"

os.makedirs(out_dir, exist_ok=True)

# NT book IDs in MySword: 40-66
nt_books = {
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

def add_backlinks(text):
    """Wrap bible references and key concepts in [[]] backlinks"""
    # Strong codes
    text = re.sub(r'(?<!\[\[)\b([GH]\d{1,4})\b(?!\]\])', r'[[\1]]', text)
    # Bible references like Gén_12:3 -> [[Génesis 12:3]]
    # But also preserve the original text
    return text

def process_commentary():
    conn = sqlite3.connect(db_path)
    
    # Get book introductions
    books_data = {}
    books_rows = conn.execute("SELECT Book, Comments FROM Books").fetchall()
    for row in books_rows:
        book_id = row[0]
        intro = clean_rtf(row[1]) if row[1] else ""
        books_data[book_id] = intro
    
    # Get all verse comments
    verses = conn.execute(
        "SELECT Book, ChapterBegin, VerseBegin, VerseEnd, Comments FROM Verses ORDER BY Book, ChapterBegin, VerseBegin"
    ).fetchall()
    
    # Group by book
    from collections import defaultdict
    book_verses = defaultdict(list)
    for v in verses:
        book_id, chap, v_from, v_to, comment = v
        book_verses[book_id].append((chap, v_from, v_to, comment))
    
    index_lines = [
        "---",
        "titulo: Índice del Comentario Partain-Reeves",
        "tipo: indice_maestro",
        "autor: Wayne Partain y Bill H. Reeves",
        "estado: Procesado",
        "etiquetas: [\"#Comentario\", \"#Exegesis\", \"#NuevoTestamento\"]",
        "---",
        "",
        "# Comentario al Nuevo Testamento",
        "## Wayne Partain y Bill H. Reeves",
        "",
        "Comentario exegético versículo por versículo del Nuevo Testamento.",
        ""
    ]
    
    total_files = 0
    
    for book_id in sorted(book_verses.keys()):
        book_name = nt_books.get(book_id, f"Libro_{book_id}")
        safe_name = sanitize(book_name)
        
        # Group verses by chapter
        chapters = defaultdict(list)
        for chap, v_from, v_to, comment in book_verses[book_id]:
            chapters[chap].append((v_from, v_to, comment))
        
        # For big books, split by chapter
        if len(chapters) > 10:
            # Create a sub-index for this book
            book_index_lines = [
                "---",
                f"titulo: Comentario a {book_name}",
                "tipo: indice_libro",
                f"autor: Wayne Partain / Bill H. Reeves",
                "estado: Procesado",
                f"etiquetas: [\"#Comentario\", \"#Exegesis\", \"#{safe_name}\"]",
                "---",
                "",
                f"# Comentario a [[{book_name}]]",
                ""
            ]
            
            if book_id in books_data and books_data[book_id]:
                book_index_lines.append("## Introducción")
                book_index_lines.append(add_backlinks(books_data[book_id]))
                book_index_lines.append("")
            
            book_index_lines.append("## Capítulos")
            
            for chap_num in sorted(chapters.keys()):
                chap_file = f"Comentario_{safe_name}_Cap_{chap_num:02d}"
                book_index_lines.append(f"- [[{chap_file}]]")
                
                # Write chapter file
                chap_content = [
                    "---",
                    f"titulo: Comentario a {book_name} {chap_num}",
                    "tipo: comentario_exegetico",
                    f"autor: Wayne Partain / Bill H. Reeves",
                    "estado: Procesado",
                    f"etiquetas: [\"#Comentario\", \"#Exegesis\", \"#{safe_name}\"]",
                    "---",
                    "",
                    f"# Comentario a [[{book_name}]] - Capítulo {chap_num}",
                    ""
                ]
                
                for v_from, v_to, comment in sorted(chapters[chap_num]):
                    cleaned = clean_rtf(comment)
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
            
            book_idx_path = os.path.join(out_dir, f"00_Indice_Comentario_{safe_name}.md")
            with open(book_idx_path, "w", encoding="utf-8") as f:
                f.write("\n".join(book_index_lines))
            total_files += 1
            
            index_lines.append(f"- [[00_Indice_Comentario_{safe_name}|{book_name}]]")
        else:
            # Small book: single file
            content = [
                "---",
                f"titulo: Comentario a {book_name}",
                "tipo: comentario_exegetico",
                f"autor: Wayne Partain / Bill H. Reeves",
                "estado: Procesado",
                f"etiquetas: [\"#Comentario\", \"#Exegesis\", \"#{safe_name}\"]",
                "---",
                "",
                f"# Comentario a [[{book_name}]]",
                ""
            ]
            
            if book_id in books_data and books_data[book_id]:
                content.append("## Introducción")
                content.append(add_backlinks(books_data[book_id]))
                content.append("")
            
            for chap_num in sorted(chapters.keys()):
                content.append(f"## Capítulo {chap_num}")
                content.append("")
                for v_from, v_to, comment in sorted(chapters[chap_num]):
                    cleaned = clean_rtf(comment)
                    cleaned = add_backlinks(cleaned)
                    if v_from == v_to:
                        content.append(f"### {book_name} {chap_num}:{v_from}")
                    else:
                        content.append(f"### {book_name} {chap_num}:{v_from}-{v_to}")
                    content.append(cleaned)
                    content.append("")
            
            file_name = f"Comentario_{safe_name}.md"
            file_path = os.path.join(out_dir, file_name)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write("\n".join(content))
            total_files += 1
            
            index_lines.append(f"- [[Comentario_{safe_name}|{book_name}]]")
    
    # Write master index
    idx_path = os.path.join(out_dir, "00_Indice_Comentario_Partain_Reeves.md")
    with open(idx_path, "w", encoding="utf-8") as f:
        f.write("\n".join(index_lines))
    total_files += 1
    
    print(f"Procesamiento completado: {total_files} archivos generados.")
    print(f"Versículos comentados: {len(verses)}")
    print(f"Libros procesados: {len(book_verses)}")
    
    conn.close()

if __name__ == "__main__":
    process_commentary()
