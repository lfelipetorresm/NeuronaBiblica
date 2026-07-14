import zipfile
import re
import os
import html

epub_path = r"C:\Users\lfeli\OneDrive\Estudios Felipe Torres\MATERIAL\Neurona\Materiales PDF\Notas Sobre Daniel - Bill H. Reeves.epub"
output_dir = r"C:\Users\lfeli\OneDrive\Estudios Felipe Torres\MATERIAL\Neurona\NeuronaBiblica\02_Exegesis\Notas_Sobre_Daniel_Reeves"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

yaml_template = """---
titulo: "{clean_title}"
autor: "Bill H. Reeves"
fuente: "Notas Sobre Daniel"
tipo: material_estudio
estado: Procesado
etiquetas: ["#Exegesis", "#Daniel", "#Profecia", "#Reeves"]
---

"""

terms_to_link = [
    "Dios", "Cristo", "Jesús", "Espíritu Santo", "Pablo", "Moisés", "David",
    "Daniel", "Babilonia", "Nabucodonosor", "profecía", "reino",
    "verdad", "iglesia", "evangelio", "bautismo", "fe", "ley", "gracia",
    "Antiguo Testamento", "Nuevo Testamento", "escritura", "biblia"
]

def add_backlinks(text):
    for term in terms_to_link:
        pattern = r'(?<!\[\[)\b(' + term + r')\b(?!\]\])'
        text = re.sub(pattern, r'[[\1]]', text, flags=re.IGNORECASE)
    return text

def strip_tags(html_str):
    # simple tag stripper
    text = re.sub(r'<style.*?>.*?</style>', '', html_str, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<script.*?>.*?</script>', '', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<p.*?>', '\n', text, flags=re.IGNORECASE)
    text = re.sub(r'<br\s*/?>', '\n', text, flags=re.IGNORECASE)
    text = re.sub(r'<[^>]+>', ' ', text)
    text = html.unescape(text)
    # cleanup extra spaces and lines
    lines = [l.strip() for l in text.split('\n')]
    text = '\n'.join([l for l in lines if l])
    return text

with zipfile.ZipFile(epub_path, 'r') as z:
    names = [n for n in z.namelist() if n.startswith('OPS/chapter-') and n.endswith('.xhtml')]
    # Sort files properly
    names.sort()

    index_content = "# Índice Maestro: Notas Sobre Daniel (Bill H. Reeves)\n\n"

    for idx, name in enumerate(names):
        content_html = z.read(name).decode('utf-8')
        content_text = strip_tags(content_html)
        content_text = add_backlinks(content_text)
        
        # Clean title
        base_name = name.replace('OPS/', '').replace('.xhtml', '')
        title = f"Daniel {base_name.replace('chapter-', 'Capitulo ')}"
        filename = f"{idx+1:02d}_{base_name}.md"
        
        filepath = os.path.join(output_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(yaml_template.format(clean_title=title))
            f.write(f"# {title}\n\n")
            f.write(content_text)
            
        index_content += f"- [[{filename.replace('.md', '')}]]\n"

    # Write Index
    with open(os.path.join(output_dir, '00_Indice_Daniel.md'), 'w', encoding='utf-8') as f:
        f.write(yaml_template.format(clean_title="Índice Daniel"))
        f.write(index_content)
        
print("EPUB Extraction Complete.")
