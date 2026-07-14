import re
import os

txt_path = r"c:\Users\lfeli\OneDrive\Estudios Felipe Torres\MATERIAL\Neurona\Materiales PDF\LOS INSTRUMENTOS MUSICALES EN LA ADORACION.txt"
md_path = r"c:\Users\lfeli\OneDrive\Estudios Felipe Torres\MATERIAL\Neurona\NeuronaBiblica\05_Materiales\Alvarenga_Instrumentos_Adoracion.md"

with open(txt_path, 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

# 1. Clean OCR issues (missing 'N' in caps words, page numbers, etc.)
text = re.sub(r'^\s*-\s*\d+\s*-\s*$', '', text, flags=re.MULTILINE)
text = re.sub(r'^Willie A\.? Alvarenga\s*$', '', text, flags=re.MULTILINE)
text = re.sub(r'^U  ESTUDIO BREVE SOBRE LOS\s*I STRUME TOS MUSICALES E  LA\s*ADORACIÓ\s*$', '', text, flags=re.MULTILINE)
text = re.sub(r'^U  ESTUDIO BREVE SOBRE LOS I STRUME TOS  MUSICALES E  LA ADORACIÓ\s*$', '', text, flags=re.MULTILINE)

replacements = {
    "I STRUME TOS": "INSTRUMENTOS",
    "ADORACIÓ": "ADORACIÓN",
    "U  ESTUDIO": "UN ESTUDIO",
    "E  LA": "EN LA",
    "CO TE IDO": "CONTENIDO",
    "I TRODUCCIÓ": "INTRODUCCIÓN",
    "PU TO": "PUNTO",
    "I CO SISTE CIA": "INCONSISTENCIA",
    "A TIGUO": "ANTIGUO",
    "TESTAME TO": "TESTAMENTO",
    " UEVO": "NUEVO",
    "RAZO ES": "RAZONES",
    "EVIDE CIA": "EVIDENCIA",
    "ACLARACIÓ": "ACLARACIÓN",
    "PRI CIPIOS": "PRINCIPIOS",
    "PRI CIPIO": "PRINCIPIO",
    "PATRÓ": "PATRÓN",
    "DIVI O": "DIVINO",
    "RESTAURACIÓ": "RESTAURACIÓN",
    "CO CLUSIÓ": "CONCLUSIÓN",
    "otas": "Notas",
    "ota:": "Nota:"
}

for bad, good in replacements.items():
    text = text.replace(bad, good)

# 2. Add headings for ALL CAPS lines
lines = text.split('\n')
out_lines = []
for line in lines:
    stripped = line.strip()
    if stripped and stripped.isupper() and len(stripped) > 5 and len(stripped) < 80:
        out_lines.append(f"\n## {stripped}\n")
    else:
        out_lines.append(line)
text = '\n'.join(out_lines)

# 3. Add bidirectional links for key concepts
key_concepts = ["Antiguo Testamento", "Nuevo Testamento", "Autoridad", "canto", "sábado", "pecado", "fe", "Cristo", "Espíritu Santo", "sacrificios"]
for concept in key_concepts:
    # match exact whole words, case insensitive, avoiding already bracketed
    pattern = r'(?<!\[\[)\b(' + concept + r')\b(?!\]\])'
    text = re.sub(pattern, r'[[\1]]', text, flags=re.IGNORECASE)

# 4. Append to the existing Markdown file
with open(md_path, 'r', encoding='utf-8') as f:
    existing_md = f.read()

new_content = existing_md + "\n\n---\n\n# TEXTO ÍNTEGRO ORIGINAL\n\n" + text

with open(md_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("ETL script completado con exito. El archivo MD ha sido actualizado.")
