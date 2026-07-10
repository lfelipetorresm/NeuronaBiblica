import os
import re

dir_path = r"05_Homiletica_y_Oratoria\PREPARACION_Y_PRESENTACION"
files = [f for f in os.listdir(dir_path) if f.endswith(".md")]

keywords = ["Sermón", "sermón", "Bosquejo", "bosquejo", "Biblia", "Antiguo Testamento", "Nuevo Testamento", "Predicador", "predicador", "Evangelista", "evangelista", "Oración", "oración"]

for filename in files:
    filepath = os.path.join(dir_path, filename)
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Remove PDF artifacts like "Lección \n 1"
    content = re.sub(r'Lección\s*\n\s*\d+\s*\n', '', content)
    
    # Remove page numbers like 1.2, 3.4
    content = re.sub(r'(?m)^\s*\d+\.\d+\s*$', '', content)
    
    # Remove empty lines with just spaces
    content = re.sub(r'(?m)^\s+$', '', content)
    
    # Split by lines
    lines = content.split('\n')
    new_lines = []
    
    in_yaml = False
    for i, line in enumerate(lines):
        if line.strip() == "---":
            in_yaml = not in_yaml
            new_lines.append(line)
            continue
            
        if in_yaml:
            new_lines.append(line)
            continue
            
        # Detect headings: short lines, no punctuation at end, first char upper
        s = line.strip()
        if len(s) > 0 and len(s) < 50 and s[0].isupper() and s[-1] not in ['.', ':', ',', ';', '?', '!']:
            # don't make it a heading if it starts with roman numeral or bullet
            if not re.match(r'^(I|V|X)+\.|^\d+\.|^[A-Z]\.', s):
                if not s.startswith('#'):
                    line = "## " + s
        
        new_lines.append(line)

    # Join lines back
    text = '\n'.join(new_lines)
    
    # Fix hard line breaks in paragraphs
    text = re.sub(r'([^\.\!\?:;])\n([a-záéíóúñ])', r'\1 \2', text)
    
    # Add links for keywords (only first match per keyword to avoid clutter, or maybe just simple replace)
    # To keep it safe, we'll just link the first 2 occurrences of each keyword
    for kw in keywords:
        # Regex to find keyword not already in brackets
        pattern = r'(?<!\[\[)\b(' + kw + r')\b(?!\]\])'
        text = re.sub(pattern, r'[[\1]]', text, count=2)
        
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(text)
        
print("Formateo completado.")
