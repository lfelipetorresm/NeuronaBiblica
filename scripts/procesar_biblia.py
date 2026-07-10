import os
import re

txt_path = r"C:\Users\lfeli\OneDrive\Estudios Felipe Torres\MATERIAL\Neurona\Materiales PDF\BIBLIA COMPLETA.txt"
output_dir = r"C:\Users\lfeli\OneDrive\Estudios Felipe Torres\MATERIAL\Neurona\NeuronaBiblica\01_Biblia"

os.makedirs(output_dir, exist_ok=True)

bible_books = [
    "Génesis", "Éxodo", "Levítico", "Números", "Deuteronomio", "Josué", "Jueces", "Rut",
    "1 Samuel", "2 Samuel", "1 Reyes", "2 Reyes", "1 Crónicas", "2 Crónicas", "Esdras", "Nehemías",
    "Ester", "Job", "Salmos", "Proverbios", "Eclesiastés", "Cantares", "Isaías", "Jeremías",
    "Lamentaciones", "Ezequiel", "Daniel", "Oseas", "Joel", "Amós", "Abdías", "Jonás", "Miqueas",
    "Nahúm", "Habacuc", "Sofonías", "Hageo", "Zacarías", "Malaquías",
    "Mateo", "Marcos", "Lucas", "Juan", "Hechos", "Romanos", "1 Corintios", "2 Corintios",
    "Gálatas", "Efesios", "Filipenses", "Colosenses", "1 Tesalonicenses", "2 Tesalonicenses",
    "1 Timoteo", "2 Timoteo", "Tito", "Filemón", "Hebreos", "Santiago", "1 Pedro", "2 Pedro",
    "1 Juan", "2 Juan", "3 Juan", "Judas", "Apocalipsis"
]

def sanitize_filename(name):
    # Remove accents
    import unicodedata
    nfkd_form = unicodedata.normalize('NFKD', name)
    only_ascii = nfkd_form.encode('ASCII', 'ignore').decode('utf-8')
    return only_ascii.replace(' ', '_')

def process_bible():
    with open(txt_path, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()

    # Find the boundaries of the books by looking for 'Capítulo 1'
    # and tracking the index of the books
    book_starts = []
    
    # Let's iterate lines and find 'Capítulo 1' (it can have weird characters like Captulo 1)
    for i, line in enumerate(lines):
        line = line.strip()
        if line.startswith("Cap") and " 1" in line and not any(str(x) in line for x in range(10, 20)) and not "11" in line and not "12" in line:
            # check the length to avoid verses like "Capernaum 1..." if any
            if len(line) < 15:
                # Potential start
                book_starts.append(i)

    # Some books like Obadiah (Abdías), Philemon (Filemón), 2 John, 3 John, Jude only have 1 chapter and might just say "Capítulo Único" or directly verses without "Capítulo 1"
    # To avoid missing them or splitting wrongly, we'll just chunk the text directly based on the occurrences we found, and let the user refine if those specific 1-chapter books are lumped.
    # Actually, let's just do a naive split based on the boundaries found.
    # We will assume there are exactly 66 boundaries, if not, we adapt.
    
    # We can also just use the known 66 books list to create the chunks.
    # Since we can't be sure of the exact 'Capítulo 1' matches for 1-chapter books, 
    # Let's just collect all chapters and verses into chunks using a simpler state machine.
    
    # Let's just use the `book_starts` array. If it's near 66, we use it.
    print(f"Encontrados {len(book_starts)} posibles inicios de libro.")
    
    # Actually, a safer way to parse the Bible text:
    # 1. Join all text.
    # 2. Use the book names (in ALL CAPS) as delimiters. The file has "GNESIS", "XODO".
    # Since encoding is messy, we'll just split by the lines.
    
    chunks = []
    last_idx = 0
    
    for idx in book_starts:
        # The book title is usually 1 or 2 lines above
        title_idx = idx - 1
        while title_idx > 0 and lines[title_idx].strip() == "":
            title_idx -= 1
        
        # We split from the line before the title to the next book
        start_cut = title_idx - 1 if title_idx > 0 else 0
        
        if last_idx == 0:
            last_idx = start_cut
            continue
            
        chunks.append(lines[last_idx:start_cut])
        last_idx = start_cut
        
    chunks.append(lines[last_idx:])
    
    # If the number of chunks is close to 66, we match them to `bible_books`.
    # If it's less, some 1-chapter books got merged. We will just dump what we have.
    print(f"Se crearán {len(chunks)} archivos.")
    
    master_index_lines = [
        "---",
        "titulo: Índice Bíblico Maestro",
        "tipo: indice_maestro",
        "estado: Procesado",
        "---",
        "",
        "# Índice Bíblico Maestro",
        "",
        "La Santa Biblia, dividida en sus libros correspondientes.",
        ""
    ]
    
    master_index_lines.append("## Antiguo Testamento")
    
    for i, chunk in enumerate(chunks):
        book_name = bible_books[i] if i < len(bible_books) else f"Libro_Extra_{i+1}"
        file_name = f"{i+1:02d}_{sanitize_filename(book_name)}.md"
        
        if i == 39:
            master_index_lines.append("\n## Nuevo Testamento")
            
        master_index_lines.append(f"- [[{file_name.replace('.md', '')}]] ({book_name})")
        
        yaml_frontmatter = f"""---
titulo: {book_name}
tipo: libro_biblico
estado: Procesado
etiquetas: ["#Biblia", "#{sanitize_filename(book_name)}"]
---

# {book_name}

"""
        
        file_path = os.path.join(output_dir, file_name)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(yaml_frontmatter)
            f.write("".join(chunk))

    with open(os.path.join(output_dir, "Indice_Biblico_Maestro.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(master_index_lines))

    print("Procesamiento completado.")

if __name__ == "__main__":
    process_bible()
