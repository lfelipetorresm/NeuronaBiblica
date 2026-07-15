import sqlite3
import sys
import codecs

sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)

db_path = r'C:\Users\lfeli\OneDrive\Estudios Felipe Torres\MATERIAL\Neurona\Materiales PDF\DFD-B&L Diccionario de figuras de dicción.dctx'

try:
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    print('Tables:', cur.fetchall())
    
    cur.execute("PRAGMA table_info(Dictionary);")
    print('Dictionary Schema:', cur.fetchall())
    
    cur.execute("SELECT count(*) FROM Dictionary;")
    print('Count:', cur.fetchone()[0])
    
    cur.execute("SELECT Topic, Details FROM Dictionary LIMIT 1;")
    sample = cur.fetchone()
    print('Sample Topic:', sample[0])
    print('Sample Details Length:', len(sample[1]))
    conn.close()
except Exception as e:
    print(f"Error: {e}")
