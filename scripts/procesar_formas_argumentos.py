import fitz
import os
import re

pdf_path = r"C:\Users\lfeli\OneDrive\Estudios Felipe Torres\MATERIAL\Neurona\Materiales PDF\ARGUMENCOMPLETO.pdf"
output_dir = r"C:\Users\lfeli\OneDrive\Estudios Felipe Torres\MATERIAL\Neurona\NeuronaBiblica\04_Logica_y_Razonamiento\Formas_de_Argumentos"

os.makedirs(output_dir, exist_ok=True)

# List of keywords for backlinks
keywords = [
    "Falacia", "Falacias", "Argumento", "Argumentos", "Premisa", "Premisas", 
    "Conclusión", "Conclusiones", "Silogismo", "Silogismos", "Refutación", 
    "Lógica", "Conjetura", "Conjeturas", "Hermenéutica", "Dialéctica",
    "Sofisma", "Sofismas", "Analogía", "Causalidad", "Deducción", "Inducción"
]

def add_backlinks(text):
    for kw in keywords:
        pattern = re.compile(r'(?<!\[\[)\b(' + kw + r')\b(?!\]\])', re.IGNORECASE)
        text = pattern.sub(r'[[\1]]', text)
    return text

def process_pdf():
    doc = fitz.open(pdf_path)
    total_pages = len(doc)
    chunk_size = 20

    master_index_lines = [
        "---",
        "titulo: Índice Maestro - Formas de Argumentos",
        "autor: Ricardo García Damborenea",
        "tipo: indice_maestro",
        "estado: Procesado",
        "---",
        "",
        "# Índice Maestro: Formas de Argumentos",
        "",
        "Este libro ha sido fragmentado para facilitar su procesamiento y consulta en la Neurona Bíblica, cumpliendo las reglas de CERO RESÚMENES y extracción exhaustiva.",
        ""
    ]

    file_count = 1
    for start_page in range(0, total_pages, chunk_size):
        end_page = min(start_page + chunk_size, total_pages)
        chunk_text = ""
        for page_num in range(start_page, end_page):
            page = doc[page_num]
            chunk_text += f"\n\n## Página {page_num + 1}\n\n"
            chunk_text += page.get_text("text")
        
        chunk_text = add_backlinks(chunk_text)
        
        yaml_frontmatter = f"""---
titulo: "Formas de Argumentos - Parte {file_count}"
autor: "Ricardo García Damborenea"
fuente: "ARGUMENCOMPLETO.pdf"
tipo: "documento_neuronal"
tema: "Lógica y Razonamiento"
estado: Procesado
paginas: "{start_page + 1} a {end_page}"
etiquetas: ["#Logica", "#Argumentacion"]
---

# Formas de Argumentos - Parte {file_count} (Páginas {start_page + 1} a {end_page})

"""
        
        file_name = f"Formas_Argumentos_Parte_{file_count:02d}.md"
        file_path = os.path.join(output_dir, file_name)
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(yaml_frontmatter + chunk_text)
            
        master_index_lines.append(f"- [[{file_name.replace('.md', '')}]] (Páginas {start_page + 1} a {end_page})")
        
        file_count += 1

    with open(os.path.join(output_dir, "Indice_Formas_Argumentos.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(master_index_lines))

    print(f"Procesamiento completado. {file_count - 1} archivos creados en {output_dir}")

if __name__ == "__main__":
    process_pdf()
