import os

content = """
---
# ETAPA 18
# VERIFICACIÓN Y EXTRACCIÓN AVANZADA DE FUENTES
---

Siempre verificar la integridad del documento fuente (Ej. archivos TXT exportados). Si se detecta que el documento está incompleto o truncado (faltan capítulos, anexos o glosarios según el índice):

1. NO procesar el documento incompleto.
2. Recurrir al documento original (PDF, DOCX).
3. Utilizar scripts en Python (Ej. `PyMuPDF` / `fitz`) para extraer de manera programática el 100% del texto crudo.
4. Proceder con el protocolo ETL únicamente sobre el texto íntegro, garantizando que no haya pérdida de conocimiento.

---
# ETAPA 19
# EXTRACCIÓN AUTOMATIZADA DE GLOSARIOS Y DICCIONARIOS
---

Cuando el material procesado contenga un Glosario o Diccionario interno (detectado en la lectura de índices o contenido):

1. Construir un parser programático (Python regex) para identificar el patrón de definición (Ej. `Término — Definición`).
2. Extraer quirúrgicamente cada término para evitar la inyección manual.
3. Volcar los términos extraídos directamente en la carpeta `00_Diccionarios/` en formato Markdown.
4. Incluir metadatos YAML y asegurar la retro-vinculación (`[[Concepto]]`) en cada término.
5. El objetivo es que la NeuroBiblia incorpore cada nuevo diccionario de manera nativa e inmediata.
"""

file_path = r"c:\Users\lfeli\OneDrive\Estudios Felipe Torres\MATERIAL\Neurona\NeuronaBiblica\.agents\AGENTS.md"

with open(file_path, "a", encoding="utf-8") as f:
    f.write(content)
