import os
import re
import math

def build_hubs_and_link(root_dir):
    print("--- INICIANDO MOTOR DE AUDITORÍA SUPREMO ---")
    
    # 1. Recopilar todos los archivos agrupados por directorio
    dir_files = {}
    for r, d, f in os.walk(root_dir):
        if '.git' in r or '.obsidian' in r or '.agents' in r or 'scripts' in r:
            continue
        
        md_files = [file for file in f if file.endswith('.md') and not file.startswith('Hub_')]
        if md_files:
            dir_files[r] = md_files

    total_hubs_created = 0
    total_files_linked = 0
    
    hub_registry = []

    # 2. Generar Hubs para directorios con muchos archivos
    for directory, files in dir_files.items():
        rel_dir = os.path.relpath(directory, root_dir)
        
        # Si la carpeta tiene menos de 5 archivos, no necesitamos un Hub masivo, 
        # pero para asegurar cohesión total, generaremos Hubs para TODO directorio
        
        # Agrupar archivos en trozos de 1000 para no hacer archivos markdown inmensos
        chunk_size = 1000
        num_chunks = math.ceil(len(files) / chunk_size)
        
        for i in range(num_chunks):
            chunk = files[i*chunk_size : (i+1)*chunk_size]
            hub_name = f"Hub_{os.path.basename(directory)}_{i+1}.md"
            hub_path = os.path.join(directory, hub_name)
            
            with open(hub_path, 'w', encoding='utf-8') as h:
                h.write(f"---\n")
                h.write(f"titulo: Hub de Indexación - {os.path.basename(directory)} (Parte {i+1})\n")
                h.write(f"tipo: moc_generado\n")
                h.write(f"etiquetas: [\"#Hub\", \"#IndexacionAutomatica\"]\n")
                h.write(f"---\n\n")
                h.write(f"# 🗂️ MOC Automático: {os.path.basename(directory)} (Parte {i+1})\n\n")
                h.write(f"> Este archivo fue generado por el Motor SOC para garantizar que ningún nodo quede huérfano.\n\n")
                
                for file in chunk:
                    name_without_ext = os.path.splitext(file)[0]
                    h.write(f"- [[{name_without_ext}]]\n")
                    total_files_linked += 1
            
            total_hubs_created += 1
            # Guardamos la referencia para el Índice General
            hub_registry.append(os.path.join(rel_dir, hub_name))
            
    print(f"EXITO: Se crearon {total_hubs_created} Hubs Maestros.")
    print(f"EXITO: Se inyectaron {total_files_linked} enlaces de cohesion.")
    
    # 3. Conectar todos los Hubs al Indice General
    indice_path = os.path.join(root_dir, '00_Indices', '00_Indice_General.md')
    if os.path.exists(indice_path):
        with open(indice_path, 'a', encoding='utf-8') as f:
            f.write("\n\n## 🌐 Hubs Generados (Capa de Cohesión SOC)\n")
            f.write("> Hubs masivos para interconectar los 49,000 archivos.\n\n")
            for hub in hub_registry:
                hub_basename = os.path.splitext(os.path.basename(hub))[0]
                f.write(f"- [[{hub_basename}]]\n")
        print("EXITO: Indice General actualizado con la nueva topologia.")
    else:
        print("ADVERTENCIA: No se encontro 00_Indice_General.md")

if __name__ == "__main__":
    vault_path = r"c:\Users\lfeli\OneDrive\Estudios Felipe Torres\MATERIAL\Neurona\NeuronaBiblica"
    build_hubs_and_link(vault_path)
