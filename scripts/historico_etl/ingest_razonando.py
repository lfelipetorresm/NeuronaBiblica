import fitz
import os
import re

pdf_path = r"C:\Users\lfeli\OneDrive\Estudios Felipe Torres\MATERIAL\Neurona\Materiales PDF\libro-razonando-correctamente.pdf"
output_dir = r"C:\Users\lfeli\OneDrive\Estudios Felipe Torres\MATERIAL\Neurona\NeuronaBiblica\04_Logica_y_Razonamiento\Razonando_Correctamente"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

doc = fitz.open(pdf_path)
toc = doc.get_toc()

sections = []
for i in range(len(toc)):
    level, title, page = toc[i]
    start_page = page - 1
    
    if i < len(toc) - 1:
        end_page = toc[i+1][2] - 1
    else:
        end_page = doc.page_count
        
    sections.append({
        "title": title.replace(".pdf", ""),
        "start": start_page,
        "end": end_page
    })

terms_to_link = [
    "Dios", "Cristo", "Jesús", "Espíritu Santo", "Pablo", "Moisés", "David",
    "razonamiento", "lógica", "argumento", "hermenéutica", "exégesis", 
    "verdad", "falacia", "iglesia", "evangelio", "bautismo", "fe", "ley", "gracia",
    "Antiguo Testamento", "Nuevo Testamento", "escritura", "biblia"
]

def add_backlinks(text):
    for term in terms_to_link:
        pattern = r'(?<!\[\[)\b(' + term + r')\b(?!\]\])'
        text = re.sub(pattern, r'[[\1]]', text, flags=re.IGNORECASE)
    return text

yaml_template = """---
titulo: "{clean_title}"
autor: "Willie Alvarenga"
fuente: "Razonando Correctamente"
estado: Procesado
etiquetas: ["#Logica", "#Razonamiento", "#Hermeneutica", "#Apologetica"]
---

"""

index_content = """# Índice Maestro: Razonando Correctamente (Willie Alvarenga)

"""

for idx, sec in enumerate(sections):
    title = sec['title']
    clean_title = re.sub(r'^\d+[a-z]?\.\-\s*', '', title)
    safe_name = re.sub(r'[^a-zA-Z0-9_\-]', '_', clean_title).strip('_')
    if not safe_name:
        safe_name = f"Seccion_{idx}"
        
    filename = f"{idx:02d}_{safe_name}.md"
    
    content = ""
    for p in range(sec['start'], sec['end']):
        content += doc[p].get_text("text") + "\n\n"
        
    content = content.replace("-\n", "")
    content = add_backlinks(content)
    
    filepath = os.path.join(output_dir, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(yaml_template.format(clean_title=clean_title) + f"# {clean_title}\n\n" + content)
        
    index_content += f"- [[{filename.replace('.md', '')}]]\n"

with open(os.path.join(output_dir, "00_Indice_Razonando.md"), "w", encoding="utf-8") as f:
    f.write(yaml_template.format(clean_title="Índice Razonando Correctamente") + index_content)

print(f"Processed {len(sections)} sections successfully.")
