import fitz
import sys

pdf_path = r"C:\Users\lfeli\OneDrive\Estudios Felipe Torres\MATERIAL\Neurona\Materiales PDF\libro-razonando-correctamente.pdf"

try:
    doc = fitz.open(pdf_path)
    print(f"Total pages: {doc.page_count}")
    
    # Check if there is a TOC
    toc = doc.get_toc()
    if toc:
        print("Table of Contents:")
        for item in toc:
            print(item)
    else:
        print("No TOC found. Printing first 10 pages text preview...")
        for i in range(min(10, doc.page_count)):
            text = doc[i].get_text("text").split('\n')
            # print non-empty lines
            lines = [l.strip() for l in text if l.strip()]
            print(f"--- Page {i+1} ---")
            print("\n".join(lines[:20]))
            
except Exception as e:
    print(f"Error: {e}")
