import os, re
from pathlib import Path

SOURCE_FILE = Path(r'C:\Users\lfeli\OneDrive\Estudios Felipe Torres\MATERIAL\Neurona\Materiales PDF\PREDICANDO LA PALABRA DE DIOS COMPLETO.txt')
DEST_DIR = Path(r'C:\Users\lfeli\OneDrive\Estudios Felipe Torres\MATERIAL\Neurona\NeuronaBiblica\05_Homiletica_y_Oratoria\Homiletica_Alvarenga\Predicando_La_Palabra')

# Dictionary of concepts
CONCEPTS = [
    'predicación', 'homilética', 'exégesis', 'hermenéutica', 'sermón', 
    'bosquejo', 'doctrina', 'evangelio', 'Cristo', 'Jesús', 'salvación',
    'Dios', 'Espíritu Santo', 'Pablo', 'Pedro', 'Timoteo', 'Tito',
    'fe', 'arrepentimiento', 'bautismo', 'verdad', 'Palabra de Dios'
]

def load_text():
    with open(SOURCE_FILE, 'r', encoding='utf-8', errors='ignore') as f:
        return f.read()

def normalize_text(text):
    text = text.replace('I TRODUCCIÓN', 'INTRODUCCIÓN')
    text = text.replace('i tro', 'intro')
    return text

def apply_backlinks(text):
    for concept in CONCEPTS:
        pattern = r'(?<!\[\[)\b(' + re.escape(concept) + r')\b(?!\]\])'
        text = re.sub(pattern, r'[[\1]]', text, flags=re.IGNORECASE)
    bible_pattern = r'(?<!\[\[)(\b(?:[1-3]\s+)?[A-Z][a-záéíóú]+\s+\d+:\d+(?:-\d+)?\b)(?!\]\])'
    text = re.sub(bible_pattern, r'[[\1]]', text)
    return text

def generate_yaml(title, theme, subtheme, extra_keywords=None):
    if extra_keywords is None: extra_keywords = []
    kw_str = '\n'.join([f'  - {kw}' for kw in extra_keywords + ['Homilética', 'Predicación', 'Alvarenga']])
    return f"""---
titulo: "{title}"
autor: "Willie A. Alvarenga"
fuente: "PREDICANDO LA PALABRA DE DIOS.txt"
tipo: "Libro"
tema: "{theme}"
subtema: "{subtheme}"
palabras_clave:
{kw_str}
estado: Procesado
---

"""

def split_and_save(text):
    DEST_DIR.mkdir(parents=True, exist_ok=True)
    
    # We will search from character 3000 to avoid the TOC
    toc_offset = 3000
    
    markers = [
        ('01_Introduccion_y_Nuestra_Condicion.md', r'INTRODUCCI[OÓ]N', r'LOS COMPONENTES DEL SERM[OÓ]N'),
        ('02_Los_Componentes_del_Sermon.md', r'LOS COMPONENTES DEL SERM[OÓ]N', r'PREDICANDO LA LECCI[OÓ]N'),
        ('03_La_Practica_y_El_Analisis.md', r'PREDICANDO LA LECCI[OÓ]N', r'LO QUE OTROS HAN DICHO SOBRE LA PREDICACI[OÓ]N'),
        ('04_Sermones_y_Evaluacion.md', r'LO QUE OTROS HAN DICHO SOBRE LA PREDICACI[OÓ]N', r'GLOSARIO DE T[EÉ]RMINOS USADOS'),
        ('05_Glosario_y_Anexos.md', r'GLOSARIO DE T[EÉ]RMINOS USADOS', None)
    ]
    
    master_index = generate_yaml('Índice Maestro - Predicando la Palabra', 'Homilética', 'Índice')
    master_index += '# Índice Maestro: PREDICANDO LA PALABRA DE DIOS\n\n'
    master_index += 'Documento extraído aplicando el Agente ETL de la Neurona Bíblica v1.0.\n\n## Partes\n\n'
    
    current_idx = toc_offset
    # Save the part before the offset into the first file
    prefix_text = text[:toc_offset]
    
    for filename, start_marker, end_marker in markers:
        # We start from current_idx
        start_match = re.search(start_marker, text[current_idx:], re.IGNORECASE)
        if start_match:
            start_pos = current_idx + start_match.start()
        else:
            print(f'Warning: Start marker {start_marker} not found. Using current idx.')
            start_pos = current_idx
            
        if end_marker:
            end_match = re.search(end_marker, text[start_pos + 10:], re.IGNORECASE)
            if end_match:
                end_pos = start_pos + 10 + end_match.start()
                current_idx = end_pos
            else:
                print(f'Warning: End marker {end_marker} not found.')
                end_pos = len(text)
        else:
            end_pos = len(text)
            
        chunk = text[start_pos:end_pos]
        
        # If this is the first file, prepend the prefix_text (Title, TOC, Dedicatoria, etc)
        if filename == '01_Introduccion_y_Nuestra_Condicion.md':
            start_pos = 0
            chunk = text[start_pos:end_pos]
        
        chunk = normalize_text(chunk)
        chunk = apply_backlinks(chunk)
        
        yaml = generate_yaml(filename.replace('.md', ''), 'Homilética', filename.split('_')[1])
        final_content = yaml + chunk
        
        with open(DEST_DIR / filename, 'w', encoding='utf-8') as f:
            f.write(final_content)
            
        master_index += f"- [[{filename.replace('.md', '')}]]\n"

    with open(DEST_DIR / '00_Indice_Maestro_Predicando.md', 'w', encoding='utf-8') as f:
        f.write(master_index)

text = load_text()
split_and_save(text)
print('Done!')
