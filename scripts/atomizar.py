import os

in_path = r"05_Homiletica_y_Oratoria\PREPARACION_Y_PRESENTACION_DE_SERMONES.md"
out_dir = r"05_Homiletica_y_Oratoria\PREPARACION_Y_PRESENTACION"
os.makedirs(out_dir, exist_ok=True)

with open(in_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

boundaries = [90, 286, 544, 701, 889, len(lines)]
names = [
    "Leccion_1_Preparacion_Predicador",
    "Leccion_2_El_Bosquejo",
    "Leccion_3_El_Sermon_Tematico",
    "Leccion_4_El_Sermon_Textual",
    "Leccion_5_La_Presentacion_Del_Sermon"
]
tags = '["#Homiletica", "#Oratoria", "#Preparacion"]'

for i in range(5):
    start = boundaries[i]
    end = boundaries[i+1]
    content = "".join(lines[start:end])
    
    yaml = f"---\ntitulo: {names[i].replace('_', ' ')}\ntipo: leccion_homiletica\netiquetas: {tags}\n---\n\n"
    
    out_file = os.path.join(out_dir, f"{names[i]}.md")
    with open(out_file, "w", encoding="utf-8") as out_f:
        out_f.write(yaml + content)

os.remove(in_path)
print("Atomizacion exitosa y archivo maestro eliminado.")
