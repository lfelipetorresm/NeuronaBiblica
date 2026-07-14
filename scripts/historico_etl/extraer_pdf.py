import fitz
import os

pdf_path = r"C:\Users\lfeli\OneDrive\Estudios Felipe Torres\MATERIAL\Neurona\Materiales PDF\LA PREPARACION Y PRESENTACION DE SERMONES_unlocked.pdf"
out_path = r"C:\Users\lfeli\OneDrive\Estudios Felipe Torres\MATERIAL\Neurona\NeuronaBiblica\05_Homiletica_y_Oratoria\PREPARACION_Y_PRESENTACION_DE_SERMONES.md"

try:
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text("text") + "\n\n"

    yaml_header = """---
titulo: La Preparacion y Presentacion de Sermones
tipo: libro_homiletica
estado: Procesado
etiquetas: ["#Homiletica", "#Sermones", "#Oratoria"]
---

# La Preparación y Presentación de Sermones (Material Extraído)

"""

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(yaml_header + text)
    print(f"Extracted {doc.page_count} pages to {out_path}")
except Exception as e:
    print(f"Error: {e}")
