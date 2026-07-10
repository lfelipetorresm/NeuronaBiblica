import os
import re
from pathlib import Path

VAULT_DIR = Path(r'C:\Users\lfeli\OneDrive\Estudios Felipe Torres\MATERIAL\Neurona\NeuronaBiblica')
INDEX_FILE = VAULT_DIR / '00_Indices' / '00_Indice_Tematico.md'

BIBLIAS_DIR = VAULT_DIR / '01_Biblias' / 'Textos_Referenciados'
CONCEPTOS_DIR = VAULT_DIR / '00_Conceptos'

BIBLIAS_DIR.mkdir(parents=True, exist_ok=True)
CONCEPTOS_DIR.mkdir(parents=True, exist_ok=True)

# List of bible book prefixes (including numbered ones) to identify a reference
BIBLE_BOOKS_REGEX = re.compile(
    r'^(1\s+|2\s+|3\s+|I\s+|II\s+|III\s+)?[A-Z][a-záéíóú]+\s*\d', 
    re.IGNORECASE
)

# Template
TEMPLATE = """---
titulo: "{title}"
tipo: "{tipo}"
estado: "Borrador"
---

# {title}

*Este nodo fue generado automáticamente por la Neurona Bíblica a partir del Índice Temático.*
"""

def get_existing_md_files():
    # Return a set of lowercase filenames (without extension)
    return {f.stem.lower() for f in VAULT_DIR.rglob('*.md')}

def is_bible_reference(concept_name):
    return bool(BIBLE_BOOKS_REGEX.search(concept_name))

def sanitize_filename(name):
    # Obsidian allows many characters, but we should remove invalid windows characters
    return re.sub(r'[<>:"/\\|?*]', '_', name)

def main():
    existing_files = get_existing_md_files()
    
    with open(INDEX_FILE, 'r', encoding='utf-8') as f:
        text = f.read()

    # Extract all concepts: `- **[[Concept|Alias]]**: ...` or `- **[[Concept]]**: ...`
    concepts_raw = re.findall(r'- \*\*\[\[([^|\]]+)(?:\|[^\]]+)?\]\]\*\*', text)
    
    # Remove duplicates but preserve order
    concepts = list(dict.fromkeys(concepts_raw))
    
    created_count = 0
    skipped_count = 0
    
    for concept in concepts:
        concept_clean = concept.strip()
        
        # Check if already exists (case insensitive match on stem)
        if concept_clean.lower() in existing_files:
            skipped_count += 1
            continue
            
        safe_name = sanitize_filename(concept_clean)
        
        if is_bible_reference(concept_clean):
            target_dir = BIBLIAS_DIR
            tipo = "Referencia Bíblica"
        else:
            target_dir = CONCEPTOS_DIR
            tipo = "Concepto"
            
        file_path = target_dir / f"{safe_name}.md"
        
        # In case the file exists exactly with this path (edge cases)
        if file_path.exists():
            skipped_count += 1
            continue
            
        content = TEMPLATE.format(title=concept_clean, tipo=tipo)
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            created_count += 1
        except Exception as e:
            print(f"Error creating {file_path}: {e}")
            
    print(f"Done! Created: {created_count} nodes. Skipped (already existed): {skipped_count} nodes.")

if __name__ == '__main__':
    main()
