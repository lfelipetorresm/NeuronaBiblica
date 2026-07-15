import fitz
import re
import os

pdf_path = r"C:\Users\lfeli\OneDrive\Estudios Felipe Torres\MATERIAL\Neurona\Materiales PDF\Historia y Geografia de la Biblia.pdf"
output_dir = r"C:\Users\lfeli\OneDrive\Estudios Felipe Torres\MATERIAL\Neurona\NeuronaBiblica\10_Historia_Geografia\Historia_y_Geografia_Biblica"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

yaml_template = """---
titulo: "{clean_title}"
fuente: "Historia y Geografia de la Biblia"
tipo: historia_geografia
estado: Procesado
etiquetas: ["#Historia", "#Geografia", "#Biblia"]
---

"""

terms_to_link = [
    "Dios", "Cristo", "Jesús", "Espíritu Santo", "Pablo", "Moisés", "David",
    "Isaías", "Jerusalén", "Judá", "Israel", "Babilonia", "Canaán", "Egipto",
    "Roma", "Antiguo Testamento", "Nuevo Testamento", "Biblia", "Jordán",
    "Galilea", "Samaria", "Judea", "Persia", "Grecia", "Asiria"
]

def add_backlinks(text):
    for term in terms_to_link:
        pattern = r'(?<!\[\[)\b(' + term + r')\b(?!\]\])'
        text = re.sub(pattern, r'[[\1]]', text, flags=re.IGNORECASE)
    return text

doc = fitz.open(pdf_path)
total_pages = len(doc)
pages_per_chunk = 15

index_content = "# Índice Maestro: Historia y Geografía de la Biblia\n\n"

chunk_idx = 1
for start_page in range(0, total_pages, pages_per_chunk):
    end_page = min(start_page + pages_per_chunk, total_pages)
    text_content = ""
    for p in range(start_page, end_page):
        page = doc.load_page(p)
        text_content += page.get_text("text") + "\n\n"
        
    text_content = add_backlinks(text_content)
    title = f"Historia y Geografía - Parte {chunk_idx}"
    filename = f"{chunk_idx:02d}_Historia_Geografia_Parte_{chunk_idx}.md"
    
    filepath = os.path.join(output_dir, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(yaml_template.format(clean_title=title))
        f.write(f"# {title}\n\n")
        f.write(text_content)
        
    index_content += f"- [[{filename.replace('.md', '')}]]\n"
    chunk_idx += 1

with open(os.path.join(output_dir, '00_Indice_Historia_Geografia.md'), 'w', encoding='utf-8') as f:
    f.write(yaml_template.format(clean_title="Índice Historia y Geografía"))
    f.write(index_content)

print(f"PDF Extraction Complete. {chunk_idx - 1} chunks created.")
