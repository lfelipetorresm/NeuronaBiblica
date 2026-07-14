import sqlite3
import traceback

try:
    path = r'C:\Users\lfeli\OneDrive\Estudios Felipe Torres\MATERIAL\Neurona\Materiales PDF\Vine NT  Vine Nuevo Testamento.dctx'
    conn = sqlite3.connect(path)
    tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
    print('Tables in NT:', tables)
    
    # Check what columns the Dictionary table has
    if tables:
        dict_table = "Dictionary"
        cols = conn.execute(f"PRAGMA table_info({dict_table});").fetchall()
        print('Columns in table:', cols)
        
        # Read one entry
        entry = conn.execute(f"SELECT * FROM {dict_table} LIMIT 1;").fetchone()
        print('Sample entry:', entry[:2] if entry else None)
except Exception as e:
    print('Error:', e)
    traceback.print_exc()
