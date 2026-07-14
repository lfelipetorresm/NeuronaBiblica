import sqlite3
import re
import os

db_path = r"c:\Users\lfeli\OneDrive\Estudios Felipe Torres\MATERIAL\Neurona\Materiales PDF\Strong (Esp) Diccionario Strong en Español.dctx"

def clean_rtf(rtf_text):
    # This is a very rudimentary RTF stripper
    # Extract transliteration (usually in bold {\b word})
    translit_match = re.search(r'\{\\b\s+([^}]+)\}', rtf_text)
    translit = translit_match.group(1).strip() if translit_match else ""

    # Remove RTF control words
    text = re.sub(r'{\\\w+(?:\d+)?(?:\\\w+(?:\d+)?)*\s?', '', rtf_text)
    text = re.sub(r'\\[a-z]+\d*\s?', '', text)
    text = re.sub(r'[{}]', '', text)
    text = re.sub(r'\\\'[0-9a-fA-F]{2}', '', text) # remove hex chars
    
    # Clean up whitespace
    text = text.replace('\n', ' ').replace('\r', ' ')
    text = re.sub(r'\s+', ' ', text).strip()
    
    return translit, text

conn = sqlite3.connect(db_path)
cur = conn.cursor()
cur.execute("SELECT Topic, Definition FROM Dictionary LIMIT 5")
for topic, definition in cur.fetchall():
    translit, clean_def = clean_rtf(definition)
    print(f"Topic: {topic}")
    print(f"Translit: {translit}")
    print(f"Def: {clean_def}")
    print("---")
