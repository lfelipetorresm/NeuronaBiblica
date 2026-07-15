import sqlite3
import os
import re
import codecs
from striprtf.striprtf import rtf_to_text

# Configuracion de rutas
db_path = r'C:\Users\lfeli\OneDrive\Estudios Felipe Torres\MATERIAL\Neurona\Materiales PDF\DFD-B&L Diccionario de figuras de dicción.dctx'
out_dir = r'C:\Users\lfeli\OneDrive\Estudios Felipe Torres\MATERIAL\Neurona\NeuronaBiblica\00_Diccionarios\Diccionario_Figuras_Diccion'

if not os.path.exists(out_dir):
    os.makedirs(out_dir)

def clean_filename(title):
    # Remover numeros romanos al principio (ej. "VI. Acciones...")
    title = re.sub(r'^[IVXLCDM]+\.\s*', '', title)
    # Remover simbolos extraños
    title = re.sub(r'[\\/*?:"<>|]', '', title)
    # Reemplazar espacios y otros caracteres por guiones bajos
    title = re.sub(r'[\s\.\-,]+', '_', title.strip())
    # Limpiar guiones bajos extra
    title = re.sub(r'_+', '_', title).strip('_')
    return title

# Paso 1: Leer todos los registros y parsear RTF
conn = sqlite3.connect(db_path)
cur = conn.cursor()
cur.execute("SELECT Topic, Definition FROM Dictionary")
rows = cur.fetchall()
conn.close()

figures = []
for topic_code, rtf_text in rows:
    if not rtf_text:
        continue
    text = rtf_to_text(rtf_text)
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    if not lines:
        continue
    
    raw_title = lines[0]
    # En algunos casos el titulo es muy largo o descriptivo, tomamos la primera linea
    clean_title = clean_filename(raw_title)
    
    # Si clean_title es muy corto o vacio, usamos el topic_code
    if len(clean_title) < 2:
        clean_title = topic_code.replace('-', '_')
        
    figures.append({
        'code': topic_code,
        'raw_title': raw_title,
        'clean_title': clean_title,
        'text': '\n'.join(lines[1:])
    })

# Paso 2: Crear mapa de sinapsis para enlazar figuras
# Si una figura menciona el raw_title o clean_title (sin guiones) de otra, lo enlazamos.
figure_names = {fig['clean_title'].replace('_', ' ').lower(): fig['clean_title'] for fig in figures}

def inyectar_sinapsis(texto):
    # Deteccion basica de referencias "v. en [Figura]" o "v. [Figura]"
    def reemplazar_v_en(match):
        termino = match.group(1).strip()
        termino_limpio = clean_filename(termino)
        return f"v. en [[{termino_limpio}]]"
    
    texto = re.sub(r'v\.\s*en\s+([A-Za-záéíóúÁÉÍÓÚñÑ]+)', reemplazar_v_en, texto, flags=re.IGNORECASE)
    
    # Deteccion de palabras clave exactas que coincidan con nombres de figuras
    # Esto podria ser muy ruidoso, asi que solo lo hacemos para las referencias explicitas o si es una figura rara.
    # Por seguridad, solo nos basaremos en referencias estilo "v. en..." o el usuario lo enlaza al usar la bóveda.
    return texto

# Paso 3: Escribir archivos Markdown
for fig in figures:
    filename = f"{fig['clean_title']}.md"
    filepath = os.path.join(out_dir, filename)
    
    texto_sinapsis = inyectar_sinapsis(fig['text'])
    
    frontmatter = f"""---
titulo: "{fig['raw_title']}"
tipo: definicion
estado: Procesado
etiquetas: ["#Diccionario", "#FigurasDeDiccion", "#Hermeneutica"]
---

# {fig['raw_title']}

{texto_sinapsis}

---
**Volver al índice:** [[00_Indice_Figuras_Diccion]]
"""
    with codecs.open(filepath, 'w', 'utf-8') as f:
        f.write(frontmatter)

# Paso 4: Escribir Indice Maestro
figures_sorted = sorted(figures, key=lambda x: x['clean_title'].lower())
indice_path = os.path.join(out_dir, "00_Indice_Figuras_Diccion.md")
indice_content = """---
titulo: "Índice de Figuras de Dicción"
tipo: navegacion
estado: Procesado
etiquetas: ["#MOC", "#Diccionario", "#FigurasDeDiccion"]
---

# 📖 Diccionario Expositivo de Figuras de Dicción

Este diccionario ha sido fragmentado y extraído en nodos atómicos para potenciar el análisis hermenéutico y retórico.

## Índice Alfabético

"""
for fig in figures_sorted:
    indice_content += f"- [[{fig['clean_title']}]] ({fig['raw_title']})\n"

with codecs.open(indice_path, 'w', 'utf-8') as f:
    f.write(indice_content)

print(f"✅ Se han generado {len(figures)} archivos y el 00_Indice_Figuras_Diccion.md en {out_dir}")
