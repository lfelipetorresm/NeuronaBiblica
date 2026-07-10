import os
import re

BASE_DIR = r"C:\Users\lfeli\OneDrive\Estudios Felipe Torres\MATERIAL\Neurona\NeuronaBiblica"

# List of OT books for heuristic
OT_BOOKS = [
    "Génesis", "Éxodo", "Levítico", "Números", "Deuteronomio",
    "Josué", "Jueces", "Rut", "1 Samuel", "2 Samuel",
    "1 Reyes", "2 Reyes", "1 Crónicas", "2 Crónicas", "Esdras",
    "Nehemías", "Ester", "Job", "Salmos", "Proverbios",
    "Eclesiastés", "Cantares", "Isaías", "Jeremías", "Lamentaciones",
    "Ezequiel", "Daniel", "Oseas", "Joel", "Amós",
    "Abdías", "Jonás", "Miqueas", "Nahúm", "Habacuc",
    "Sofonías", "Hageo", "Zacarías", "Malaquías"
]

def determine_encoding(filepath):
    path_lower = filepath.lower()
    if 'vine_nt' in path_lower or 'partain' in path_lower:
        return 'windows-1253' # Greek
    if 'vine_at' in path_lower:
        return 'windows-1255' # Hebrew
        
    # For Walton-Keener or generated sermons, check filename for OT books
    filename = os.path.basename(filepath)
    for book in OT_BOOKS:
        # replace spaces and accents for matching if necessary, but simple in is fine
        # Some are named "ContextoCultural_Genesis_Cap_01"
        book_safe = book.replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u")
        if book in filename or book_safe in filename:
            return 'windows-1255' # Hebrew
            
    # Default fallback to Greek (most common in NT context)
    return 'windows-1253'

def is_mojibake(word):
    # Strip common markdown/punctuation
    clean_word = word.strip('.,;:\'\"()[]{}!?><-*_#')
    if not clean_word:
        return False
    
    # Must have at least one alphabetic character
    has_alpha = any(c.isalpha() for c in clean_word)
    # Must NOT have any standard ascii letter
    has_ascii = bool(re.search(r'[a-zA-Z]', clean_word))
    
    return has_alpha and not has_ascii

def fix_mojibake(word, encoding):
    clean_word = word.strip('.,;:\'\"()[]{}!?><-*_#')
    try:
        raw_bytes = clean_word.encode('windows-1252')
        fixed = raw_bytes.decode(encoding)
        return word.replace(clean_word, fixed)
    except Exception:
        # Some characters might not exist in 1255/1253, try the other as fallback
        try:
            alt_enc = 'windows-1253' if encoding == 'windows-1255' else 'windows-1255'
            fixed = raw_bytes.decode(alt_enc)
            return word.replace(clean_word, fixed)
        except Exception:
            return word

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    encoding = determine_encoding(filepath)
        
    tokens = re.split(r'(\s+)', content)
    changed = False
    
    for i, token in enumerate(tokens):
        if not token.isspace() and is_mojibake(token):
            fixed_token = fix_mojibake(token, encoding)
            if fixed_token != token:
                tokens[i] = fixed_token
                changed = True
                
    if changed:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("".join(tokens))
        return True
    return False

def main():
    total_files = 0
    fixed_files = 0
    
    # List of directories to process
    target_dirs = [
        r"00_Diccionarios\Diccionario_Vine_NT",
        r"00_Diccionarios\Diccionario_Vine_AT",
        r"02_Exegesis\Comentario_Partain_Reeves",
        r"02_Exegesis\Contexto_Cultural_Walton_Keener",
        r"06_Sermones_Generados"
    ]
    
    for rel_dir in target_dirs:
        abs_dir = os.path.join(BASE_DIR, rel_dir)
        if not os.path.exists(abs_dir):
            continue
            
        for root, dirs, files in os.walk(abs_dir):
            for file in files:
                if file.endswith('.md'):
                    total_files += 1
                    filepath = os.path.join(root, file)
                    try:
                        if process_file(filepath):
                            fixed_files += 1
                    except Exception as e:
                        print(f"Error procesando {file}: {e}")
                        
    print(f"Proceso finalizado. Total archivos analizados: {total_files}")
    print(f"Archivos reparados con éxito (que contenían mojibake): {fixed_files}")

if __name__ == "__main__":
    main()
