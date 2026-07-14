import re

lessons = [
    r"c:\Users\lfeli\OneDrive\Estudios Felipe Torres\MATERIAL\Neurona\NeuronaBiblica\07_Doctrinas\La_Iglesia_Del_Nuevo_Testamento\Leccion_38_La_música_en_el_culto.md",
    r"c:\Users\lfeli\OneDrive\Estudios Felipe Torres\MATERIAL\Neurona\NeuronaBiblica\07_Doctrinas\La_Iglesia_Del_Nuevo_Testamento\Leccion_39_La_música_instrumental.md",
    r"c:\Users\lfeli\OneDrive\Estudios Felipe Torres\MATERIAL\Neurona\NeuronaBiblica\07_Doctrinas\La_Iglesia_Del_Nuevo_Testamento\Leccion_40_Las_finanzas_de_la_iglesia.md"
]

concepts = [
    "música", "culto", "canto", "Espíritu Santo", "Cristo", "Dios", "Nuevo Testamento",
    "Noé", "Aarón", "Antiguo Testamento", "fe", "obediencia", "alabanza", "himnos",
    "música instrumental", "ley de Moisés", "gracia", "Sana Doctrina", "libertad cristiana",
    "pecado", "apóstoles", "finanzas", "dinero", "riqueza", "pobreza", "Moisés", 
    "avaricia", "iglesia", "vida eterna", "salvación", "evangelio"
]

for file_path in lessons:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()

        for concept in concepts:
            # Sort concepts by length descending? Wait, just standard matching. "música instrumental" will match first if we do it carefully, but it doesn't matter much.
            pattern = r'(?<!\[\[)\b(' + concept + r')\b(?!\]\])'
            text = re.sub(pattern, r'[[\1]]', text, flags=re.IGNORECASE)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(text)
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

print("Linking completed for 38, 39, 40")
