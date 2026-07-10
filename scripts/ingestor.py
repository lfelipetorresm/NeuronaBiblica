import os
import sys
import glob
from google import genai
from google.genai import types

# Configuración del Cliente Gemini
# Asegúrate de tener la variable de entorno GEMINI_API_KEY configurada
try:
    client = genai.Client()
except Exception as e:
    print("Error: No se encontró GEMINI_API_KEY. Configura la variable de entorno antes de ejecutar.")
    sys.exit(1)

def procesar_documento(ruta_archivo):
    """
    Lee un documento de texto, lo envía a Gemini para extraer conceptos, doctrinas y 
    palabras clave, y genera un archivo .md formateado para Obsidian.
    """
    print(f"Procesando: {ruta_archivo}...")
    
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            contenido = f.read()
    except Exception as e:
        print(f"Error al leer el archivo {ruta_archivo}: {e}")
        return

    # Prompt (Instrucción) para la IA
    prompt = f"""
    Eres un teólogo experto y erudito bíblico. Tu tarea es analizar el siguiente texto y extraer información clave para un sistema Zettelkasten (Obsidian).
    
    Debes identificar:
    1. Doctrinas principales abordadas (ej. Soteriología, Bautismo, Gracia).
    2. Conceptos teológicos importantes.
    3. Palabras clave generales.
    4. Citas bíblicas (si las hay).
    
    Genera un archivo en formato Markdown que siga esta estructura exacta:
    
    ---
    tipo: material_ingresado
    doctrinas: [lista separada por comas]
    conceptos: [lista separada por comas]
    palabras_clave: [lista separada por comas]
    ---
    
    # [Título inferido del texto]
    
    ## Resumen
    [Un resumen de 2-3 párrafos del texto original]
    
    ## Conceptos Clave Detectados
    (Crea una lista de conceptos, y envuélvelos en corchetes dobles de Obsidian, por ejemplo: [[Gracia]], [[Pecado Original]])
    
    ## Citas Bíblicas
    (Lista de citas encontradas, en formato de enlace: [[Juan 3-16]])
    
    ## Texto Original Procesado
    {contenido[:3000]}... (se ha truncado por longitud)
    """

    print("Analizando con Inteligencia Artificial (Gemini)...")
    
    # Usar el modelo gemini-flash-latest
    response = client.models.generate_content(
        model='gemini-flash-latest',
        contents=prompt,
    )
    
    markdown_result = response.text
    
    # Guardar el archivo en la bóveda
    nombre_base = os.path.basename(ruta_archivo).split('.')[0]
    ruta_salida = f"05_Materiales/{nombre_base}_Procesado.md"
    
    # Crear carpeta si no existe
    os.makedirs(os.path.dirname(ruta_salida), exist_ok=True)
    
    with open(ruta_salida, 'w', encoding='utf-8') as f:
        f.write(markdown_result)
        
    print(f"✅ Éxito! Archivo guardado en: {ruta_salida}\n")

if __name__ == "__main__":
    print("=== INGESTOR DE LA NEURONA BÍBLICA ===")
    
    # Directorio donde el usuario coloca los archivos nuevos (Bandeja de entrada)
    # Por ahora procesaremos archivos .txt en una carpeta temporal
    carpeta_inbox = "00_Inbox_Materiales_Nuevos"
    os.makedirs(carpeta_inbox, exist_ok=True)
    
    archivos = glob.glob(f"{carpeta_inbox}/*.txt")
    
    if not archivos:
        print(f"No se encontraron archivos .txt en la carpeta '{carpeta_inbox}'.")
        print("Coloca tus textos allí y vuelve a ejecutar este script.")
    else:
        for archivo in archivos:
            procesar_documento(archivo)
