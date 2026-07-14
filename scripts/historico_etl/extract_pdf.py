import sys
import subprocess
from pathlib import Path

try:
    import fitz  # PyMuPDF
except ImportError:
    print("Installing PyMuPDF...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "PyMuPDF"])
    import fitz

pdf_path = r"c:\Users\lfeli\OneDrive\Estudios Felipe Torres\MATERIAL\Neurona\Materiales PDF\PREDICANDO LA PALABRA DE DIOS.pdf"
out_path = r"c:\Users\lfeli\OneDrive\Estudios Felipe Torres\MATERIAL\Neurona\Materiales PDF\PREDICANDO LA PALABRA DE DIOS COMPLETO.txt"

print(f"Opening {pdf_path}")
doc = fitz.open(pdf_path)
text = ""
for page in doc:
    text += page.get_text()

with open(out_path, "w", encoding="utf-8") as f:
    f.write(text)

print(f"Extracted {len(text)} characters.")
