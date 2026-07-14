import re

lessons = [
    r"c:\Users\lfeli\OneDrive\Estudios Felipe Torres\MATERIAL\Neurona\NeuronaBiblica\07_Doctrinas\La_Iglesia_Del_Nuevo_Testamento\Leccion_35_La_disciplina_de_la_iglesia.md",
    r"c:\Users\lfeli\OneDrive\Estudios Felipe Torres\MATERIAL\Neurona\NeuronaBiblica\07_Doctrinas\La_Iglesia_Del_Nuevo_Testamento\Leccion_36_El_día_del_Señor.md",
    r"c:\Users\lfeli\OneDrive\Estudios Felipe Torres\MATERIAL\Neurona\NeuronaBiblica\07_Doctrinas\La_Iglesia_Del_Nuevo_Testamento\Leccion_37_La_cena_del_Señor.md"
]

concepts = [
    "disciplina", "ancianos", "obispos", "pecado", "Sana Doctrina", "rebeldía",
    "Día del Señor", "Sábado", "sábado", "Antiguo Testamento", "Nuevo Testamento",
    "ley de Moisés", "Espíritu Santo", "Pentecostés", "Cena del Señor", 
    "partimiento del pan", "evangelio", "Cristo", "comunión", "apóstoles",
    "Pablo", "Moisés", "gracia", "resurrección", "adorar"
]

for file_path in lessons:
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()

    for concept in concepts:
        # Match word ignoring case, avoiding double linking, and avoiding being part of another word
        pattern = r'(?<!\[\[)\b(' + concept + r')\b(?!\]\])'
        text = re.sub(pattern, r'[[\1]]', text, flags=re.IGNORECASE)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(text)

print("Linking completed for 35, 36, 37")
