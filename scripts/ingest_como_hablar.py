import os, re
from pathlib import Path

SOURCE_FILE = Path(r'C:\Users\lfeli\OneDrive\Estudios Felipe Torres\MATERIAL\Neurona\Materiales PDF\COMO HABLAR EN PUBLICO.txt')
DEST_DIR = Path(r'C:\Users\lfeli\OneDrive\Estudios Felipe Torres\MATERIAL\Neurona\NeuronaBiblica\05_Homiletica_y_Oratoria\Oratoria_Israel_Gonzalez')

CONCEPTS = [
    'oratoria', 'nerviosismo', 'volumen', 'tono', 'ritmo', 'público',
    'contacto visual', 'discurso', 'Jesús', 'Pedro', 'Juan', 'Pablo',
    'Biblia', 'gestos', 'postura', 'comunicación'
]

def load_text():
    with open(SOURCE_FILE, 'r', encoding='utf-8', errors='ignore') as f:
        return f.read()

def convert_headings(text):
    # Convert specific all-caps headings to markdown ##
    headings = [
        "INTRODUCCIÓN.",
        "¿DE QUE PROVECHO ES PARA USTED?",
        "POR QUE UN LIBRO SOBRE EL TEMA",
        "¿POR QUE ES TAN ATEMORIZANTE HABLAR EN PUBLICO?",
        "APRENDIENDO DE LA BIBLIA.",
        "COMO CONTROLAR EL NERVIOSISMO",
        "EL CULTIVO DE UN ESTILO DE EXPRESIÓN NATURAL.",
        "HAGA SENTIR SU PRESENCIA",
        "TERMINE DE MANERA IMPRESIONANTE",
        "PLANIFIQUE Y ORGANICE SU MENSAJE",
        "ENSAYE SU DISCURSO",
        "COMO DIRIGIR PERÍODOS DE PREGUNTAS Y RESPUESTAS",
        "CONCLUSIÓN"
    ]
    for h in headings:
        # Match exactly with or without punctuation, handle newlines
        pattern = re.compile(r'^\s*' + re.escape(h) + r'\s*$', re.MULTILINE | re.IGNORECASE)
        # Title case it for beauty
        title = h.title()
        text = pattern.sub(f'\n## {title}\n', text)
    return text

def apply_backlinks(text):
    for concept in CONCEPTS:
        pattern = r'(?<!\[\[)\b(' + re.escape(concept) + r')\b(?!\]\])'
        text = re.sub(pattern, r'[[\1]]', text, flags=re.IGNORECASE)
    
    # Simple regex for bible references e.g. 1Pedro.3:15. or Mat.7:28-29 or Hech. 4:13
    # This might need some generic capture
    bible_pattern = r'(?<!\[\[)(\b(?:[1-3]\s*)?[A-Z][a-záéíóú]+\.?\s*\d+:\d+(?:-\d+)?\b)(?!\]\])'
    text = re.sub(bible_pattern, r'[[\1]]', text)
    
    return text

def generate_yaml():
    return """---
titulo: "Cómo Hablar en Público"
autor: "Israel González"
fuente: "COMO HABLAR EN PUBLICO.txt"
tipo: "Artículo/Guía"
tema: "Oratoria"
palabras_clave:
  - Oratoria
  - Homilética
  - Comunicación
estado: Procesado
---

# Cómo Hablar en Público

"""

def process():
    DEST_DIR.mkdir(parents=True, exist_ok=True)
    text = load_text()
    
    # Remove title line "COMO HABLAR EN PÚBLICO Por Israel González"
    text = re.sub(r'^\s*COMO HABLAR EN PÚBLICO Por Israel González\s*', '', text)
    
    text = convert_headings(text)
    text = apply_backlinks(text)
    
    final_content = generate_yaml() + text
    
    out_file = DEST_DIR / "01_Como_Hablar_En_Publico.md"
    with open(out_file, 'w', encoding='utf-8') as f:
        f.write(final_content)
        
    print(f"File created: {out_file}")

process()
