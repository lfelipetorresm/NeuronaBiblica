import re
from pathlib import Path

source_file = Path(r"C:\Users\lfeli\OneDrive\Estudios Felipe Torres\MATERIAL\Neurona\NeuronaBiblica\05_Homiletica_y_Oratoria\Homiletica_Alvarenga\Predicando_La_Palabra\05_Glosario_y_Anexos.md")
dest_file = Path(r"C:\Users\lfeli\OneDrive\Estudios Felipe Torres\MATERIAL\Neurona\NeuronaBiblica\00_Diccionarios\Diccionario_Homiletico.md")

with open(source_file, "r", encoding="utf-8") as f:
    text = f.read()

# Find glossary start
match = re.search(r'GLOSARIO DE T[EÉ]RMINOS USADOS', text, re.IGNORECASE)
if match:
    glossary_text = text[match.start():]
else:
    print("Glossary not found!")
    exit(1)

# Basic cleanup: remove page numbers (e.g. "266", "Glosario de términos", etc)
glossary_text = re.sub(r'Glosario de t[eé]rminos\s+\d+', '', glossary_text, flags=re.IGNORECASE)
glossary_text = re.sub(r'^\s*\d+\s*$', '', glossary_text, flags=re.MULTILINE)

# The terms are separated by em dashes (or replacement character if encoding issue)
# Let's extract them
terms = []
# split by double newline
blocks = glossary_text.split('\n\n')

for block in blocks:
    block = block.replace('\n', ' ').strip()
    if '—' in block:
        parts = block.split('—', 1)
        terms.append((parts[0].strip(), parts[1].strip()))
    elif '-' in block:
        parts = block.split('-', 1)
        terms.append((parts[0].strip(), parts[1].strip()))
    elif '\ufffd' in block:
        parts = block.split('\ufffd', 1)
        terms.append((parts[0].strip(), parts[1].strip()))

# Build markdown
md = """---
titulo: "Diccionario Homilético"
fuente: "Willie A. Alvarenga (Predicando la Palabra de Dios)"
etiquetas: [Diccionario, Homilética]
---

# Diccionario Homilético

Este diccionario recopila definiciones fundamentales relacionadas con la preparación y presentación de sermones, extraídas directamente de la obra "Predicando la Palabra de Dios" de Willie A. Alvarenga.

"""

# Sort terms alphabetically (ignoring backlink brackets)
def sort_key(x):
    return x[0].replace('[[', '').replace(']]', '').lower()

terms.sort(key=sort_key)

for term, definition in terms:
    if term and definition and len(term) < 50: # Avoid false positives
        clean_term = term.replace('[[', '').replace(']]', '')
        md += f"## [[{clean_term}]]\n"
        md += f"**Definición:** {definition}\n\n"

# Create output dir if not exists
dest_file.parent.mkdir(parents=True, exist_ok=True)
with open(dest_file, "w", encoding="utf-8") as f:
    f.write(md)

print(f"Diccionario_Homiletico.md created with {len(terms)} terms.")
