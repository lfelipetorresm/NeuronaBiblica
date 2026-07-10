import sqlite3
import traceback

try:
    path = r'C:\Users\lfeli\OneDrive\Estudios Felipe Torres\MATERIAL\Neurona\Materiales PDF\RV1960+ Reina Valera 1960 con Strong.bblx'
    conn = sqlite3.connect(path)
    tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
    print('Tables in Bible:', tables)
    
    if tables:
        # Check Bible table
        bible_table = "Bible"
        cols = conn.execute(f"PRAGMA table_info({bible_table});").fetchall()
        print('Columns in Bible table:', cols)
        
        # Read a few verses
        entries = conn.execute(f"SELECT Book, Chapter, Verse, Script FROM {bible_table} LIMIT 5;").fetchall()
        for entry in entries:
            print(f"Book: {entry[0]}, Chapter: {entry[1]}, Verse: {entry[2]}")
            print(f"Script: {entry[3][:100]}...") # print snippet
except Exception as e:
    print('Error:', e)
    traceback.print_exc()
