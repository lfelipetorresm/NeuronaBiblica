import os
import re

in_file = r"C:\Users\lfeli\OneDrive\Estudios Felipe Torres\MATERIAL\Neurona\Materiales PDF\INTERROGANTES Y RESPUESTAS.txt"
out_dir = r"C:\Users\lfeli\OneDrive\Estudios Felipe Torres\MATERIAL\Neurona\NeuronaBiblica\08_Preguntas_y_Respuestas\Interrogantes_y_Respuestas"

os.makedirs(out_dir, exist_ok=True)

# Regex for bible references and keywords
def add_backlinks(text):
    # Bible references basic matching (e.g. Mat. 5:32, 1 Cor. 5:1, Juan 1:1, etc.)
    # We won't parse perfectly every book abbreviation, but let's do a few common ones
    books = ['Gén', 'Éx', 'Lev', 'Núm', 'Deut', 'Jos', 'Jue', 'Rut', '1 Sam', '2 Sam', '1 Rey', '2 Rey', 
             '1 Crón', '2 Crón', 'Esd', 'Neh', 'Est', 'Job', 'Sal', 'Prov', 'Ecl', 'Cant', 'Isa', 'Jer', 
             'Lam', 'Eze', 'Dan', 'Os', 'Jl', 'Am', 'Abd', 'Jon', 'Miq', 'Nah', 'Hab', 'Sof', 'Hag', 'Zac', 'Mal',
             'Mat', 'Mar', 'Luc', 'Juan', 'Hech', 'Rom', '1 Cor', '2 Cor', 'Gál', 'Efes', 'Fil', 'Col', 
             '1 Tes', '2 Tes', '1 Tim', '2 Tim', 'Tito', 'File', 'Heb', 'Sant', '1 Ped', '2 Ped', 
             '1 Juan', '2 Juan', '3 Juan', 'Jud', 'Apoc']
    
    # Just a basic approach: link strong concepts if needed, but here we focus on the text itself
    # Replace some concepts (just a basic example of semantics)
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

    # The document has a large index. We look for the first actual question which is "1. " or similar.
    # The delimiter between Q&As seems to be "* * *"
    blocks = content.split('* * *')
    
    index_lines = [
        "---",
        "titulo: Índice Interrogantes y Respuestas",
        "tipo: indice_maestro",
        "autor: Bill H. Reeves",
        "estado: Procesado",
        "etiquetas: [\"#Preguntas\", \"#Respuestas\", \"#Doctrina\"]",
        "---",
        "",
        "# Interrogantes y Respuestas",
        "**Por Bill H. Reeves**",
        ""
    ]
    
    count = 0
    # Process from the second block (block 0 is usually intro/index)
    for block in blocks[1:]:
        block = block.strip()
        if not block:
            continue
            
        # Extract title: e.g. "105. QUERER IR AL INSTITUTO"
        match = re.search(r'(\d+)\.\s+([^\n]+)', block)
        if match:
            q_num = match.group(1)
            raw_title = match.group(2)
            clean_title = sanitize_title(raw_title)
            
            # Extract question and answer
            parts = block.split('- - -')
            question_text = parts[0].replace(match.group(0), '').strip()
            answer_text = parts[1].strip() if len(parts) > 1 else ""
            
            q_num_int = int(q_num)
            filename = f"Pregunta_{q_num_int:03d}_{clean_title.replace(' ', '_')}.md"
            filepath = os.path.join(out_dir, filename)
            
            md_content = [
                "---",
                f"titulo: Pregunta {q_num} - {clean_title}",
                "tipo: pregunta_respuesta",
                "autor: Bill H. Reeves",
                "estado: Procesado",
                "etiquetas: [\"#Pregunta\", \"#Reeves\"]",
                "---",
                "",
                f"# {q_num}. {clean_title}",
                "",
                "## Interrogante",
                add_backlinks(question_text),
                "",
                "## Respuesta",
                add_backlinks(answer_text)
            ]
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write("\n".join(md_content))
                
            index_lines.append(f"- [[{filename.replace('.md', '')}|{q_num}. {clean_title}]]")
            count += 1
            
    # Write Index
    idx_path = os.path.join(out_dir, "00_Indice_Interrogantes_y_Respuestas.md")
    with open(idx_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(index_lines))
        
    print(f"Generadas {count} preguntas y respuestas.")

if __name__ == "__main__":
    process()
