import sqlite3
import re
import os

db_path = r"c:\Users\lfeli\OneDrive\Estudios Felipe Torres\MATERIAL\Neurona\Materiales PDF\COMENTARIO AL AT - KEIL-DELITZSCH.cmti"
out_dir = r"c:\Users\lfeli\OneDrive\Estudios Felipe Torres\MATERIAL\Neurona\NeuronaBiblica\02_Exegesis\Comentarios\Keil_Delitzsch"

os.makedirs(out_dir, exist_ok=True)

book_mapping = {
    1: "01_Genesis", 2: "02_Exodo", 3: "03_Levitico", 4: "04_Numeros", 
    5: "05_Deuteronomio", 6: "06_Josue", 7: "07_Jueces", 8: "08_Rut",
    9: "09_1_Samuel", 10: "10_2_Samuel", 11: "11_1_Reyes", 12: "12_2_Reyes",
    13: "13_1_Cronicas", 14: "14_2_Cronicas", 15: "15_Esdras", 
    16: "16_Nehemias", 17: "17_Ester"
}

def clean_html(text):
    if not text: return ""
    
    # Preserve <ref> by converting it to [[ref]]
    text = re.sub(r'<ref>(.*?)</ref>', r'[[\1]]', text, flags=re.IGNORECASE)
    
    # Handle bold / italics if they exist
    text = re.sub(r'<b>(.*?)</b>', r'**\1**', text, flags=re.IGNORECASE)
    text = re.sub(r'<i>(.*?)</i>', r'*\1*', text, flags=re.IGNORECASE)
    
    # Strip spans, divs, and other tags
    text = re.sub(r'<[^>]+>', '', text)
    
    # Decode basic HTML entities
    text = text.replace("&nbsp;", " ")
    text = text.replace("&lt;", "<").replace("&gt;", ">")
    text = text.replace("&amp;", "&")
    
    return text.strip()

conn = sqlite3.connect(db_path)
cur = conn.cursor()
# We will query and sort by Book, ChapterBegin, VerseBegin
cur.execute("SELECT Book, ChapterBegin, VerseBegin, VerseEnd, Comments FROM VerseCommentary ORDER BY Book, ChapterBegin, VerseBegin")
rows = cur.fetchall()

# Group by Book
books_data = {}
for book_id, chapter, verse_b, verse_e, comments in rows:
    if book_id not in book_mapping: continue
    book_name = book_mapping[book_id]
    
    if book_name not in books_data:
        books_data[book_name] = {}
        
    if chapter not in books_data[book_name]:
        books_data[book_name][chapter] = []
        
    books_data[book_name][chapter].append((verse_b, verse_e, comments))

for book_name, chapters in books_data.items():
    filepath = os.path.join(out_dir, f"{book_name}.md")
    
    display_name = book_name.split("_", 1)[1].replace("_", " ")
    
    content = [
        "---",
        "tipo: comentario_biblico",
        "autor: Keil & Delitzsch",
        f"libro: {display_name}",
        "epoca: Antiguo Testamento",
        "estado: Procesado",
        "etiquetas: [\"#Comentario\", \"#AT\", \"#KeilDelitzsch\", \"#Exegesis\"]",
        "---",
        "",
        f"# {display_name} - Comentario Keil & Delitzsch",
        ""
    ]
    
    for chapter in sorted(chapters.keys()):
        content.append(f"## Capítulo {chapter}")
        for verse_b, verse_e, comment in chapters[chapter]:
            verse_title = f"Versículo {verse_b}" if verse_b == verse_e else f"Versículos {verse_b}-{verse_e}"
            clean_comment = clean_html(comment)
            content.append(f"### {verse_title}")
            content.append(clean_comment)
            content.append("")
            
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write("\n".join(content))

print("Procesamiento de Comentarios completado.")
