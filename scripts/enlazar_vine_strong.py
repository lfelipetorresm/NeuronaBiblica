import os
import re

directories = [
    r"C:\Users\lfeli\OneDrive\Estudios Felipe Torres\MATERIAL\Neurona\NeuronaBiblica\00_Diccionarios\Diccionario_Vine_NT",
    r"C:\Users\lfeli\OneDrive\Estudios Felipe Torres\MATERIAL\Neurona\NeuronaBiblica\00_Diccionarios\Diccionario_Vine_AT"
]

pattern = re.compile(r'(?<!\[\[)\b([GH]\d{1,4})\b(?!\]\])')

count_modified = 0

for d in directories:
    for root, _, files in os.walk(d):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check if it has any G1234 or H1234
                new_content, num_subs = pattern.subn(r'[[\1]]', content)
                
                if num_subs > 0:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    count_modified += 1

print(f"Modificados {count_modified} archivos en los diccionarios añadiendo enlaces Strong.")
