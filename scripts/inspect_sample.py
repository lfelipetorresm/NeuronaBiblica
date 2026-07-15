import sqlite3
import sys
import codecs

sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)
db_path = r'C:\Users\lfeli\OneDrive\Estudios Felipe Torres\MATERIAL\Neurona\Materiales PDF\DFD-B&L Diccionario de figuras de dicción.dctx'

conn = sqlite3.connect(db_path)
cur = conn.cursor()
cur.execute("SELECT Topic, Definition FROM Dictionary LIMIT 3;")
samples = cur.fetchall()
for s in samples:
    print(f"Topic: {s[0]}")
    print(f"Def Snippet: {s[1][:200]}")
    print("-" * 50)
conn.close()
