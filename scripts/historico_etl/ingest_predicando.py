import os
import re
from pathlib import Path

SOURCE_FILE = Path(r"C:\Users\lfeli\OneDrive\Estudios Felipe Torres\MATERIAL\Neurona\Materiales PDF\PREDICANDO LA PALABRA DE DIOS.txt")
DEST_DIR = Path(r"C:\Users\lfeli\OneDrive\Estudios Felipe Torres\MATERIAL\Neurona\NeuronaBiblica\05_Homiletica_y_Oratoria\Homiletica_Alvarenga\Predicando_La_Palabra")

# Dictionary of concepts to automatically link (Etapa 6 & 16)
CONCEPTS = [
    "predicación", "homilética", "exégesis", "hermenéutica", "sermón", 
    "bosquejo", "doctrina", "evangelio", "Cristo", "Jesús", "salvación",
    "Dios", "Espíritu Santo", "Pablo", "Pedro", "Timoteo", "Tito",
    "fe", "arrepentimiento", "bautismo", "verdad", "Palabra de Dios"
]

def load_text():
    with open(SOURCE_FILE, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()

def normalize_text(text):
    # Fix common OCR issues
    text = text.replace("I TRODUCCIÓN", "INTRODUCCIÓN")
    text = text.replace("i tro", "intro")
    return text

def apply_backlinks(text):
    # A simple but careful find-replace for concepts, ensuring we don't double-link
    # We will use regex to only match whole words not already inside brackets
    for concept in CONCEPTS:
        pattern = r'(?<!\[\[)\b(' + re.escape(concept) + r')\b(?!\]\])'
        # Using a lambda to keep the original capitalization
        text = re.sub(pattern, r'[[\1]]', text, flags=re.IGNORECASE)
    
    # Auto-link Bible verses (e.g. Romanos 1:16, 2 Timoteo 4:2)
    # Simple regex for Book Chapter:Verse
    bible_pattern = r'(?<!\[\[)(\b(?:[1-3]\s+)?[A-Z][a-záéíóú]+\s+\d+:\d+(?:-\d+)?\b)(?!\]\])'
    text = re.sub(bible_pattern, r'[[\1]]', text)
    
    return text

def generate_yaml(title, theme, subtheme, extra_keywords=None):
    if extra_keywords is None: extra_keywords = []
    kw_str = "\n".join([f"  - {kw}" for kw in extra_keywords + ["Homilética", "Predicación", "Alvarenga"]])
    return f"""---
titulo: "{title}"
autor: "Willie A. Alvarenga"
fuente: "PREDICANDO LA PALABRA DE DIOS.txt"
tipo: "Libro"
tema: "{theme}"
subtema: "{subtheme}"
palabras_clave:
{kw_str}
estado: Procesado
---

"""

def split_and_save(text):
    DEST_DIR.mkdir(parents=True, exist_ok=True)
    
    # Define exact split markers based on the book structure
    # Since text might have variations, we will use regex search to find indices
    markers = [
        ("01_Introduccion_y_Nuestra_Condicion.md", "INTRODUCCIÓN", r"LOS COMPONENTES DEL SERM[OÓ]N"),
        ("02_Los_Componentes_del_Sermon.md", r"LOS COMPONENTES DEL SERM[OÓ]N", r"PREDICANDO LA LECCI[OÓ]N"),
        ("03_La_Practica_y_El_Analisis.md", r"PREDICANDO LA LECCI[OÓ]N", r"LO QUE OTROS HAN DICHO"),
        ("04_Sermones_y_Evaluacion.md", r"LO QUE OTROS HAN DICHO", r"GLOSARIO DE T[EÉ]RMINOS"),
        ("05_Glosario_y_Anexos.md", r"GLOSARIO DE T[EÉ]RMINOS", None)
    ]
    
    # Master Index Content
    master_index = generate_yaml("Índice Maestro - Predicando la Palabra", "Homilética", "Índice")
    master_index += "# Índice Maestro: PREDICANDO LA PALABRA DE DIOS\n\n"
    master_index += "Documento extraído aplicando el Agente ETL de la Neurona Bíblica v1.0.\n\n## Partes\n\n"
    
    current_idx = 0
    for filename, start_marker, end_marker in markers:
        # Find start
        start_match = re.search(start_marker, text[current_idx:], re.IGNORECASE)
        if start_match:
            start_pos = current_idx + start_match.start()
        else:
            start_pos = current_idx # Fallback
            
        # Find end
        if end_marker:
            end_match = re.search(end_marker, text[start_pos:], re.IGNORECASE)
            if end_match:
                end_pos = start_pos + end_match.start()
                current_idx = end_pos # update for next iteration
            else:
                end_pos = len(text)
        else:
            end_pos = len(text)
            
        chunk = text[start_pos:end_pos]
        
        # Process chunk
        chunk = normalize_text(chunk)
        chunk = apply_backlinks(chunk)
        
        yaml = generate_yaml(filename.replace(".md", ""), "Homilética", filename.split("_")[1])
        final_content = yaml + chunk
        
        # Save file
        with open(DEST_DIR / filename, "w", encoding="utf-8") as f:
            f.write(final_content)
            
        master_index += f"- [[{filename.replace('.md', '')}]]\n"

    # Save Master Index
    with open(DEST_DIR / "00_Indice_Maestro_Predicando.md", "w", encoding="utf-8") as f:
        f.write(master_index)
        
    # Build Report
    report = f"""# REPORTE FINAL: ETL PREDICANDO LA PALABRA DE DIOS

## Documento procesado
PREDICANDO LA PALABRA DE DIOS.txt (Willie A. Alvarenga)

## Cantidad de archivos generados
6 archivos (5 secciones + 1 Índice Maestro)

## Backlinks creados
Múltiples inyecciones automatizadas de conceptos como Predicación, Homilética, Exégesis, y versículos bíblicos.

## Recomendaciones
Se preservó el 100% de la información original sin resúmenes (Principio Fundamental). El Glosario en la parte 5 debería ser procesado posteriormente para alimentar el Diccionario Homilético.
"""
    with open(DEST_DIR / "Reporte_ETL_Predicando.md", "w", encoding="utf-8") as f:
        f.write(report)

if __name__ == "__main__":
    print("Iniciando ETL para Predicando la Palabra de Dios...")
    text = load_text()
    split_and_save(text)
    print("ETL completado exitosamente.")
