import sqlite3
import os
import re
import unicodedata

db_path = r"C:\Users\lfeli\OneDrive\Estudios Felipe Torres\MATERIAL\Neurona\Materiales PDF\RV1960+ Reina Valera 1960 con Strong.bblx"
out_dir = r"C:\Users\lfeli\OneDrive\Estudios Felipe Torres\MATERIAL\Neurona\NeuronaBiblica\01_Biblia_Strong"
hubs_dir = r"C:\Users\lfeli\OneDrive\Estudios Felipe Torres\MATERIAL\Neurona\NeuronaBiblica\00_Diccionarios\Strong_Hubs"

os.makedirs(out_dir, exist_ok=True)
os.makedirs(hubs_dir, exist_ok=True)

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
    nfkd_form = unicodedata.normalize('NFKD', name)
    only_ascii = nfkd_form.encode('ASCII', 'ignore').decode('utf-8')
    return only_ascii.replace(' ', '_')

def clean_rtf_and_link(scripture):
    unique_strongs = set()
    # Find strong tags: {\cf11\super H7225 NCcSFC}
    # Some might not have \super, or might be formatted slightly differently.
    # We want to capture the H\d+ or G\d+
    
    def replacer(match):
        strong_code = match.group(1).strip()
        unique_strongs.add(strong_code)
        return f" [[{strong_code}]] "
        
    # Replace the Strong format block with the backlink
    scripture = re.sub(r'\{\\cf\d+\\super\s*([HG]\d+)[^}]*\}', replacer, scripture)
    
    # Sometimes it might just be \super without \cf
    scripture = re.sub(r'\{\\super\s*([HG]\d+)[^}]*\}', replacer, scripture)

    # Sometimes there's no brace if it's badly formatted? Usually it has braces.
    
    # Remove remaining RTF tags like \bullet, \par, \cf11
    scripture = re.sub(r'\\[a-z0-9]+\s*', '', scripture)
    scripture = re.sub(r'[{}]', '', scripture)
    
    # Clean up multiple spaces
    scripture = re.sub(r'\s+', ' ', scripture).strip()
    return scripture, unique_strongs

def process_bible():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    all_strongs = set()
    
    master_index_lines = [
        "---",
        "titulo: Índice Bíblico Maestro (Strong)",
        "tipo: indice_maestro",
        "estado: Procesado",
        "---",
        "",
        "# Índice Bíblico Maestro (Strong)",
        "",
        "La Santa Biblia (RV1960) interconectada con raíces Hebreas y Griegas.",
        "",
        "## Antiguo Testamento"
    ]
    
    for book_id in range(1, 67):
        book_name = bible_books[book_id - 1]
        file_name = f"{book_id:02d}_{sanitize_filename(book_name)}.md"
        
        if book_id == 40:
            master_index_lines.append("\n## Nuevo Testamento")
            
        master_index_lines.append(f"- [[{file_name.replace('.md', '')}]] ({book_name})")
        
        cursor.execute("SELECT Chapter, Verse, Scripture FROM Bible WHERE Book = ? ORDER BY Chapter, Verse", (book_id,))
        rows = cursor.fetchall()
        
        book_content = [f"""---
titulo: {book_name}
tipo: libro_biblico
estado: Procesado
etiquetas: ["#Biblia", "#{sanitize_filename(book_name)}"]
---

# {book_name}
"""]
        
        current_chapter = 0
        for row in rows:
            chap, ver, script = row
            if chap != current_chapter:
                book_content.append(f"\n### Capítulo {chap}\n")
                current_chapter = chap
            
            clean_script, strongs_found = clean_rtf_and_link(script)
            all_strongs.update(strongs_found)
            
            book_content.append(f"**{chap}:{ver}** {clean_script}  \n")
            
        file_path = os.path.join(out_dir, file_name)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("".join(book_content))
            
        print(f"Procesado: {book_name}")
        
    with open(os.path.join(out_dir, "Indice_Biblico_Maestro.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(master_index_lines))
        
    # Generate Strong Hubs
    print(f"Generando {len(all_strongs)} Nodos Puente Strong...")
    for strong in all_strongs:
        # Some might have bad characters if regex matched weirdly. Just sanity check
        if re.match(r'^[GH]\d+$', strong):
            hub_path = os.path.join(hubs_dir, f"{strong}.md")
            if not os.path.exists(hub_path):
                with open(hub_path, "w", encoding="utf-8") as f:
                    f.write(f"---\ntitulo: Raíz {strong}\ntipo: strong_hub\nestado: Procesado\netiquetas: [\"#Strong\", \"#{strong}\"]\n---\n\n# {strong}\n\n*Este es un nodo puente. Revisa los Backlinks (enlaces entrantes) para ver todos los versículos y definiciones del diccionario que usan esta raíz.*")

    print("Procesamiento de Biblia Strong completado.")

if __name__ == "__main__":
    process_bible()
