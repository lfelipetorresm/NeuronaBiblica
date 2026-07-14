import fitz
import os
import re

pdf_path = r"C:\Users\lfeli\OneDrive\Estudios Felipe Torres\MATERIAL\Neurona\Materiales PDF\musica-instrumental-y-adoracion-en-el-nt.-james-d.-bales.pdf"
output_dir = r"C:\Users\lfeli\OneDrive\Estudios Felipe Torres\MATERIAL\Neurona\NeuronaBiblica\05_Materiales\Bales_Musica_Instrumental"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

doc = fitz.open(pdf_path)

# Extract all text
full_text = ""
for page in doc:
    full_text += page.get_text() + "\n"

# Simple normalization
full_text = full_text.replace("-\n", "")

# We need to split by "CAPÍTULO" or similar.
# The book has "INTRODUCCIÓN", "CAPÍTULO 1", etc.
chapters = re.split(r'\n(CAPÍTULO\s+\d+|INTRODUCCIÓN|BIBLIOGRAFÍA)\s*\n', full_text)

# chapters will be [pre-text, "INTRODUCCIÓN", text, "CAPÍTULO 1", text, ...]

# Terms to backlink
terms_to_link = [
    "Dios", "Cristo", "Jesús", "Espíritu Santo", "Pablo", "Moisés", "David",
    "adoración", "instrumento", "música", "canto", "salmo", "himno", "iglesia",
    "bautismo", "fe", "ley", "gracia", "verdad", "Antiguo Testamento", "Nuevo Testamento",
    "Nuevo Pacto", "Antiguo Pacto", "Jerusalén", "tabernáculo", "templo", "sacrificio"
]

def add_backlinks(text):
    for term in terms_to_link:
        # Avoid linking inside already linked [[term]] or inside words
        pattern = r'(?<!\[\[)\b(' + term + r')\b(?!\]\])'
        text = re.sub(pattern, r'[[\1]]', text, flags=re.IGNORECASE)
    return text

yaml_template = """---
titulo: "{title}"
autor: "James D. Bales"
fuente: "Música Instrumental y Adoración en el Nuevo Testamento"
estado: Procesado
etiquetas: ["#Doctrina", "#Adoracion", "#MusicaInstrumental"]
---

"""

index_content = """# Índice Maestro: Música Instrumental y Adoración en el Nuevo Testamento (James D. Bales)

"""

# Handle pre-text (Title page, preface, index)
pre_text = chapters[0].strip()
if pre_text:
    pre_text = add_backlinks(pre_text)
    with open(os.path.join(output_dir, "00_Prefacio.md"), "w", encoding="utf-8") as f:
        f.write(yaml_template.format(title="Prefacio e Índice") + pre_text)
    index_content += "- [[00_Prefacio]]\n"

for i in range(1, len(chapters), 2):
    title = chapters[i].strip()
    content = chapters[i+1].strip()
    
    # Format filename
    safe_title = title.replace(" ", "_").replace("Í", "I").replace("Ó", "O")
    filename = f"{safe_title}.md"
    
    # Process content
    content = add_backlinks(content)
    
    with open(os.path.join(output_dir, filename), "w", encoding="utf-8") as f:
        f.write(yaml_template.format(title=title) + f"# {title}\n\n" + content)
        
    index_content += f"- [[{safe_title}]]\n"

# Save index
with open(os.path.join(output_dir, "00_Indice_Bales_Musica.md"), "w", encoding="utf-8") as f:
    f.write(yaml_template.format(title="Índice Maestro") + index_content)

print(f"Processed {len(chapters)//2} chapters successfully.")
