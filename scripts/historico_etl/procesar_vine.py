import sqlite3
import os
import unicodedata
import re
try:
    from striprtf.striprtf import rtf_to_text
except ImportError:
    print("Por favor instala striprtf: pip install striprtf")
    exit(1)

base_path = r"C:\Users\lfeli\OneDrive\Estudios Felipe Torres\MATERIAL\Neurona\Materiales PDF"
out_base = r"C:\Users\lfeli\OneDrive\Estudios Felipe Torres\MATERIAL\Neurona\NeuronaBiblica\00_Diccionarios"

dbs = [
    {
        "file": "Vine AT  Vine Antiguo Testamento.dctx",
        "folder": "Diccionario_Vine_AT",
        "tag": "#VineAT"
    },
    {
        "file": "Vine NT  Vine Nuevo Testamento.dctx",
        "folder": "Diccionario_Vine_NT",
        "tag": "#VineNT"
    }
]

def sanitize_filename(name):
    # Some topics have numbers like "1. PALABRA", so we split by dot or keep it.
    name = str(name).strip()
    name = re.sub(r'[\\/*?:"<>|]', "", name)
    name = name.replace('\n', '').replace('\r', '')
    return name

def process_db(db_info):
    db_path = os.path.join(base_path, db_info["file"])
    out_dir = os.path.join(out_base, db_info["folder"])
    os.makedirs(out_dir, exist_ok=True)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT Topic, Definition FROM Dictionary")
    rows = cursor.fetchall()
    
    master_index = [
        "---",
        f"titulo: Índice - {db_info['folder']}",
        "tipo: indice_maestro",
        "estado: Procesado",
        "---",
        "",
        f"# Índice - {db_info['folder']}",
        ""
    ]
    
    count = 0
    for row in rows:
        topic = row[0]
        definition_rtf = row[1]
        
        if not topic or not definition_rtf:
            continue
            
        # Clean RTF
        try:
            definition_clean = rtf_to_text(definition_rtf)
        except:
            # Fallback if striprtf fails
            definition_clean = definition_rtf
            
        clean_name = sanitize_filename(topic)
        if not clean_name:
            continue
            
        file_name = f"{clean_name}.md"
        file_path = os.path.join(out_dir, file_name)
        
        yaml_frontmatter = f"""---
titulo: "{clean_name}"
tipo: definicion_diccionario
estado: Procesado
etiquetas: ["#Diccionario", "{db_info['tag']}", "#{clean_name.replace(' ', '')}"]
---

# {clean_name}

{definition_clean}
"""
        
        # In case of duplicate names (e.g. two words with same spelling in different contexts),
        # append a number.
        counter = 1
        original_path = file_path
        while os.path.exists(file_path):
            file_path = os.path.join(out_dir, f"{clean_name}_{counter}.md")
            counter += 1
            
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(yaml_frontmatter)
            
        master_index.append(f"- [[{os.path.basename(file_path).replace('.md', '')}]]")
        count += 1
        
    with open(os.path.join(out_dir, f"Indice_{db_info['folder']}.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(master_index))
        
    print(f"Procesadas {count} palabras en {db_info['folder']}")

if __name__ == "__main__":
    for db in dbs:
        process_db(db)
