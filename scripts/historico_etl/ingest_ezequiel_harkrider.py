import zipfile
import re
import os
import html

epub_path = r"C:\Users\lfeli\OneDrive\Estudios Felipe Torres\MATERIAL\Neurona\Materiales PDF\EZEQUIEL - Robert Harkrider, Josue I. Hernandez.epub"
output_dir = r"C:\Users\lfeli\OneDrive\Estudios Felipe Torres\MATERIAL\Neurona\NeuronaBiblica\02_Exegesis\Ezequiel_Harkrider"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

yaml_template = """---
titulo: "{clean_title}"
autor: "Robert Harkrider, Josué I. Hernandez"
fuente: "Ezequiel - Un Cuaderno de Estudio para Maestros"
tipo: material_estudio
estado: Procesado
etiquetas: ["#Exegesis", "#Ezequiel", "#Profetas", "#Harkrider"]
---

"""

terms_to_link = [
    "Dios", "Cristo", "Jesús", "Espíritu Santo", "Pablo", "Moisés", "David",
    "Ezequiel", "Jerusalén", "Judá", "Israel", "Babilonia", "profecía", 
    "verdad", "iglesia", "evangelio", "bautismo", "fe", "ley", "gracia",
    "Antiguo Testamento", "Nuevo Testamento", "escritura", "biblia"
]

def add_backlinks(text):
    for term in terms_to_link:
        pattern = r'(?<!\[\[)\b(' + term + r')\b(?!\]\])'
        text = re.sub(pattern, r'[[\1]]', text, flags=re.IGNORECASE)
    return text

def strip_tags(html_str):
    text = re.sub(r'<style.*?>.*?</style>', '', html_str, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<script.*?>.*?</script>', '', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<p.*?>', '\n', text, flags=re.IGNORECASE)
    text = re.sub(r'<br\s*/?>', '\n', text, flags=re.IGNORECASE)
    text = re.sub(r'<[^>]+>', ' ', text)
    text = html.unescape(text)
    lines = [l.strip() for l in text.split('\n')]
    text = '\n'.join([l for l in lines if l])
    return text

with zipfile.ZipFile(epub_path, 'r') as z:
    names = [n for n in z.namelist() if n.startswith('OPS/chapter-') and n.endswith('.xhtml')]
    names.sort()

    index_content = "# Índice Maestro: Ezequiel (Robert Harkrider)\n\n"

    for idx, name in enumerate(names):
        content_html = z.read(name).decode('utf-8')
        content_text = strip_tags(content_html)
        content_text = add_backlinks(content_text)
        
        base_name = name.replace('OPS/', '').replace('.xhtml', '')
        title = f"Ezequiel Parte {idx+1}"
        filename = f"{idx+1:02d}_{base_name}.md"
        
        filepath = os.path.join(output_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(yaml_template.format(clean_title=title))
            f.write(f"# {title}\n\n")
            f.write(content_text)
            
        index_content += f"- [[{filename.replace('.md', '')}]]\n"

    with open(os.path.join(output_dir, '00_Indice_Ezequiel.md'), 'w', encoding='utf-8') as f:
        f.write(yaml_template.format(clean_title="Índice Ezequiel"))
        f.write(index_content)
        
print(f"EPUB Extraction Complete. {len(names)} files processed.")
