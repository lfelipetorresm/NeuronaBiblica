import os
import re

in_file = r"C:\Users\lfeli\OneDrive\Estudios Felipe Torres\MATERIAL\Neurona\Materiales PDF\LA IGLESIA DEL NUEVO TESTAMENTO.txt"
out_dir = r"C:\Users\lfeli\OneDrive\Estudios Felipe Torres\MATERIAL\Neurona\NeuronaBiblica\07_Doctrinas\La_Iglesia_Del_Nuevo_Testamento"

os.makedirs(out_dir, exist_ok=True)

def add_backlinks(text):
    books = ['Gén', 'Éx', 'Lev', 'Núm', 'Deut', 'Jos', 'Jue', 'Rut', '1 Sam', '2 Sam', '1 Rey', '2 Rey', 
             '1 Crón', '2 Crón', 'Esd', 'Neh', 'Est', 'Job', 'Sal', 'Prov', 'Ecl', 'Cant', 'Isa', 'Jer', 
             'Lam', 'Eze', 'Dan', 'Os', 'Jl', 'Am', 'Abd', 'Jon', 'Miq', 'Nah', 'Hab', 'Sof', 'Hag', 'Zac', 'Mal',
             'Mat', 'Mar', 'Luc', 'Juan', 'Hech', 'Rom', '1 Cor', '2 Cor', 'Gál', 'Efes', 'Fil', 'Col', 
             '1 Tes', '2 Tes', '1 Tim', '2 Tim', 'Tito', 'File', 'Heb', 'Sant', '1 Pedro', '2 Pedro', 
             '1 Juan', '2 Juan', '3 Juan', 'Judas', 'Apoc']
    
    concepts = ['iglesia', 'bautismo', 'pecado', 'salvación', 'arrepentimiento', 'fe', 'Cristo', 'Jesús', 'Dios', 'Espíritu Santo']
    for c in concepts:
        text = re.sub(fr'(?<!\[\[)\b({c})\b(?!\]\])', rf'[[\1]]', text, flags=re.IGNORECASE)
    return text

def sanitize_title(title):
    t = re.sub(r'[\\/*?:"<>|]', "", title)
    t = t.replace('\n', ' ').replace('\r', '').strip()
    return t[:100]

def process():
    with open(in_file, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # Split by "Lección [Roman_Numeral]"
    # However, "Lección I -- ..." appears in the index. We want exactly "Lección I\n" or "Lección I \n"
    # Find all occurrences of the pattern that start a line
    pattern = r'\nLección\s+([IVXLCDM]+)\s*\n'
    parts = re.split(pattern, content)
    
    # parts[0] is the intro/index
    intro_text = parts[0].strip()
    
    index_lines = [
        "---",
        "titulo: Índice de La Iglesia del Nuevo Testamento",
        "tipo: indice_maestro",
        "autor: Roy E. Cogdill",
        "estado: Procesado",
        "etiquetas: [\"#Doctrina\", \"#Iglesia\", \"#Cogdill\"]",
        "---",
        "",
        "# La Iglesia del Nuevo Testamento",
        "**Por Roy E. Cogdill**",
        ""
    ]
    
    count = 0
    # parts[1] is the roman numeral "I", parts[2] is the content of lesson I, etc.
    for i in range(1, len(parts), 2):
        if i + 1 >= len(parts):
            break
            
        lesson_num_roman = parts[i]
        lesson_content = parts[i+1].strip()
        
        # The first line of lesson_content should be the title
        lines = lesson_content.split('\n', 1)
        if len(lines) > 0:
            raw_title = lines[0].strip()
            rest = lines[1].strip() if len(lines) > 1 else ""
        else:
            raw_title = f"Lección {lesson_num_roman}"
            rest = lesson_content
            
        clean_title = sanitize_title(raw_title)
        lesson_id = (i // 2) + 1
        
        filename = f"Leccion_{lesson_id:02d}_{clean_title.replace(' ', '_')}.md"
        filepath = os.path.join(out_dir, filename)
        
        md_content = [
            "---",
            f"titulo: Lección {lesson_num_roman} - {clean_title}",
            "tipo: leccion_doctrinal",
            "autor: Roy E. Cogdill",
            "estado: Procesado",
            "etiquetas: [\"#Doctrina\", \"#Iglesia\"]",
            "---",
            "",
            f"# Lección {lesson_num_roman}: {clean_title}",
            "",
            add_backlinks(rest)
        ]
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("\n".join(md_content))
            
        index_lines.append(f"- [[{filename.replace('.md', '')}|Lección {lesson_num_roman}: {clean_title}]]")
        count += 1
        
    # Write Index
    idx_path = os.path.join(out_dir, "00_Indice_Iglesia_NT.md")
    with open(idx_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(index_lines))
        
    print(f"Generadas {count} lecciones doctrinales.")

if __name__ == "__main__":
    process()
