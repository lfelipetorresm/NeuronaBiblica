import sqlite3
import re
import os

db_path = r"c:\Users\lfeli\OneDrive\Estudios Felipe Torres\MATERIAL\Neurona\Materiales PDF\Strong (Esp) Diccionario Strong en Español.dctx"
out_dir = r"c:\Users\lfeli\OneDrive\Estudios Felipe Torres\MATERIAL\Neurona\NeuronaBiblica\01_Biblia_Strong\Diccionario"

os.makedirs(os.path.join(out_dir, "Hebreo"), exist_ok=True)
os.makedirs(os.path.join(out_dir, "Griego"), exist_ok=True)

def decode_rtf_hex(match):
    hex_val = match.group(1)
    try:
        return bytes.fromhex(hex_val).decode('cp1252')
    except:
        return ""

def clean_rtf(rtf_text):
    # Extract transliteration (usually in bold {\b word})
    translit_match = re.search(r'\{\\b\s+([^}]+)\}', rtf_text)
    translit = translit_match.group(1).strip() if translit_match else ""

    # Decode hex characters like \'e0
    text = re.sub(r"\\'([0-9a-fA-F]{2})", decode_rtf_hex, rtf_text)
    
    # Remove RTF control words
    text = re.sub(r'{\\\w+(?:\d+)?(?:\\\w+(?:\d+)?)*\s?', '', text)
    text = re.sub(r'\\[a-z]+\d*\s?', '', text)
    text = re.sub(r'[{}]', '', text)
    
    # Clean up whitespace
    text = text.replace('\n', ' ').replace('\r', ' ')
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Remove the first garbage char if it's there (sometimes RTF leaves a stray '' or similar)
    if text.startswith(''):
        text = text[1:].strip()
        
    return translit, text

conn = sqlite3.connect(db_path)
cur = conn.cursor()
cur.execute("SELECT Topic, Definition FROM Dictionary")
rows = cur.fetchall()

print(f"Processing {len(rows)} dictionary entries...")

for topic, definition in rows:
    if not topic.startswith('H') and not topic.startswith('G'):
        continue
        
    translit, clean_def = clean_rtf(definition)
    
    # Identify Language
    lang = "Hebreo" if topic.startswith('H') else "Griego"
    
    # Format cross references: H123 or G123 to [[H123]]
    clean_def = re.sub(r'\b([HG]\d+)\b', r'[[\1]]', clean_def)
    
    filename = f"{topic}.md"
    filepath = os.path.join(out_dir, lang, filename)
    
    content = f"""---
tipo: diccionario_strong
strong_id: {topic}
idioma: {lang}
transliteracion: {translit}
estado: Procesado
etiquetas: ["#Strong", "#{lang}"]
---

# {topic} - {translit}

**Definición:**
{clean_def}
"""
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

print("Diccionario procesado exitosamente.")
