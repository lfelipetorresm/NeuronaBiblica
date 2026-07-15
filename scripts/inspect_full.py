import sqlite3
import sys
import codecs
from striprtf.striprtf import rtf_to_text

sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)
db_path = r'C:\Users\lfeli\OneDrive\Estudios Felipe Torres\MATERIAL\Neurona\Materiales PDF\DFD-B&L Diccionario de figuras de dicción.dctx'

conn = sqlite3.connect(db_path)
cur = conn.cursor()
cur.execute("SELECT Topic, Definition FROM Dictionary LIMIT 5;")
samples = cur.fetchall()
for s in samples:
    print(f"Topic Code: {s[0]}")
    text = rtf_to_text(s[1])
    print(f"Stripped Text:\n{text[:500]}")
    print("-" * 50)
conn.close()
