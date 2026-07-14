import sqlite3
import re
import os

db_path = r"c:\Users\lfeli\OneDrive\Estudios Felipe Torres\MATERIAL\Neurona\Materiales PDF\NCSE Nueva Concordancia Strong Exhaustiva.dctx"
out_dir = r"c:\Users\lfeli\OneDrive\Estudios Felipe Torres\MATERIAL\Neurona\NeuronaBiblica\01_Biblia_Strong\Concordancia"

os.makedirs(out_dir, exist_ok=True)

def decode_rtf_hex(match):
    hex_val = match.group(1)
    try:
        return bytes.fromhex(hex_val).decode('cp1252')
    except:
        return ""

def clean_rtf(rtf_text):
    text = re.sub(r"\\'([0-9a-fA-F]{2})", decode_rtf_hex, rtf_text)
    
    # In the concordance, verses are usually separated by \par
    lines = text.split('\\par')
    
    clean_lines = []
    for line in lines:
        if not line.strip(): continue
        
        # Extract verses and strongs
        # Verse is often like \ul Num_16:46} or something.
        # Strong is like H175
        strongs = re.findall(r'\b([HG]\d+)\b', line)
        
        # Clean RTF
        line_clean = re.sub(r'{\\\w+(?:\d+)?(?:\\\w+(?:\d+)?)*\s?', '', line)
        line_clean = re.sub(r'\\[a-z]+\d*\s?', '', line_clean)
        line_clean = re.sub(r'[{}]', '', line_clean)
        
        # Format the line for markdown
        line_clean = line_clean.strip()
        if line_clean:
            # Re-inject strongs as markdown links
            for st in strongs:
                if st in line_clean:
                    line_clean = re.sub(rf'\b{st}\b', f'[[{st}]]', line_clean)
            clean_lines.append(f"- {line_clean}")
            
    return "\n".join(clean_lines)

def sanitize_filename(name):
    # Remove invalid characters for windows filenames
    return re.sub(r'[<>:"/\\|?*]', '', name).strip()

conn = sqlite3.connect(db_path)
cur = conn.cursor()
cur.execute("SELECT Topic, Definition FROM Dictionary")
rows = cur.fetchall()

print(f"Processing {len(rows)} concordance entries...")

for topic, definition in rows:
    # Topic is the Spanish word
    clean_def = clean_rtf(definition)
    
    filename = sanitize_filename(topic)
    if not filename: continue
    filename += ".md"
    filepath = os.path.join(out_dir, filename)
    
    content = f"""---
tipo: concordancia
palabra: {topic}
estado: Procesado
etiquetas: ["#Concordancia"]
---

# {topic}

{clean_def}
"""
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
    except Exception as e:
        print(f"Failed to write {filename}: {e}")

print("Concordancia procesada exitosamente.")
