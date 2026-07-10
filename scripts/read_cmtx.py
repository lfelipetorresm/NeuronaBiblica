import sqlite3

path = r'C:\Users\lfeli\OneDrive\Estudios Felipe Torres\MATERIAL\Neurona\Materiales PDF\WP-BR Comentario Al NT Por Partain - Reeves.cmtx'
conn = sqlite3.connect(path)

tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
print('Tables:', tables)

for t in tables:
    tname = t[0]
    cols = conn.execute(f"PRAGMA table_info({tname});").fetchall()
    print(f"\nTable {tname}:")
    for c in cols:
        print(f"  {c}")
    count = conn.execute(f"SELECT COUNT(*) FROM {tname}").fetchone()
    print(f"  Rows: {count[0]}")

# Sample raw rows
print("\n--- SAMPLE DATA ---")
for t in tables:
    tname = t[0]
    rows = conn.execute(f"SELECT * FROM {tname} LIMIT 3").fetchall()
    for r in rows:
        print(f"  [{tname}] columns={len(r)}")
        for i, val in enumerate(r):
            v = str(val)[:200] if val else "NULL"
            print(f"    col[{i}] = {v}")

conn.close()
