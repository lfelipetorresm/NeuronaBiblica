import os
import re
from collections import defaultdict
from pathlib import Path

VAULT_DIR = Path(r'C:\Users\lfeli\OneDrive\Estudios Felipe Torres\MATERIAL\Neurona\NeuronaBiblica')
REPORT_FILE = VAULT_DIR / 'Reporte_Arquitecto.md'
INDICE_GENERAL = VAULT_DIR / '00_Indices' / '00_Indice_General.md'

def get_files():
    files = []
    for f in VAULT_DIR.rglob('*.md'):
        if '.agents' in f.parts or '.obsidian' in f.parts:
            continue
        files.append(f)
    return files

def parse_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except Exception:
        return None
    
    # Parse YAML
    metadata = {}
    yaml_match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if yaml_match:
        yaml_str = yaml_match.group(1)
        for line in yaml_str.split('\n'):
            line = line.strip()
            if not line or line.startswith('- '):
                continue
            if ':' in line:
                k, v = line.split(':', 1)
                metadata[k.strip()] = v.strip().strip('"').strip("'")
            
    # Extract links [[link]] or [[link|alias]]
    links_raw = re.findall(r'\[\[([^|\]]+)(?:\|[^\]]+)?\]\]', content)
    # Exclude image links if any, simple heuristic
    links = [l.strip() for l in links_raw if not l.lower().endswith(('.png', '.jpg', '.pdf'))]
    
    return {
        'path': filepath,
        'name': filepath.stem,
        'metadata': metadata,
        'content_length': len(content),
        'links_out': links,
        'is_template': "*Este nodo fue generado automáticamente" in content
    }

def calculate_quality(data):
    if data['is_template']:
        return 1
    score = 3 # base score
    if data['metadata']:
        score += 2
    if data['content_length'] > 1000:
        score += 2
    if data['content_length'] > 5000:
        score += 1
    if len(data['links_out']) > 5:
        score += 1
    if len(data['links_out']) > 15:
        score += 1
    return min(10, score)

def main():
    print("Iniciando análisis neuronal...")
    files = get_files()
    
    nodes = {}
    incoming = defaultdict(list)
    outgoing = defaultdict(list)
    
    # Pass 1: Parse all files
    for f in files:
        data = parse_file(f)
        if data:
            nodes[data['name'].lower()] = data
            
    # Build Graph
    for name_lower, data in nodes.items():
        for link in data['links_out']:
            link_lower = link.lower()
            outgoing[name_lower].append(link_lower)
            incoming[link_lower].append(name_lower)
            
    # Analysis Metrics
    vacios_detectados = []
    huerfanos = []
    aislados = []
    baja_conexion = []
    
    for name_lower, data in nodes.items():
        in_links = incoming.get(name_lower, [])
        out_links = outgoing.get(name_lower, [])
        total_links = len(in_links) + len(out_links)
        
        if total_links == 0:
            aislados.append(data['name'])
        elif len(in_links) == 0:
            huerfanos.append(data['name'])
            
        if total_links < 5:
            baja_conexion.append(data['name'])
            
        if data['is_template'] or data['content_length'] < 150:
            vacios_detectados.append(data['name'])
            
    # Duplicate logic: just by name for now, but Obsidian handles unique names. 
    # Real duplicates would be same content or synonymous titles, skipping complex NLP for now.

    # Generate Report
    report = []
    report.append("# REPORTE DEL ARQUITECTO DE LA NEUROBIBLIA\n")
    report.append("## Resumen Ejecutivo")
    report.append(f"Se analizaron **{len(nodes)}** nodos en el repositorio.")
    report.append(f"Se identificaron **{sum(len(v) for v in outgoing.values())}** sinapsis (enlaces) totales.")
    report.append(f"- Nodos con conexiones óptimas (>=5): {len(nodes) - len(baja_conexion)}")
    report.append(f"- Nodos con conexiones débiles (<5): {len(baja_conexion)}\n")
    
    report.append("## Calidad General del Repositorio")
    # Average quality
    avg_quality = sum(calculate_quality(d) for d in nodes.values()) / max(1, len(nodes))
    report.append(f"La calidad promedio algorítmica del repositorio es **{avg_quality:.1f}/10**.\n")
    report.append("*Nota: Los nodos autogenerados (plantillas) arrastran el promedio a 1. A medida que los llenes, la métrica subirá.*\n")
    
    report.append("## Documentos Huérfanos (Cero Enlaces Entrantes)")
    report.append("Estos nodos no están siendo referenciados por nadie más (excluyendo índices principales si no se cuentan):")
    if len(huerfanos) > 20:
        report.append(f"Se detectaron {len(huerfanos)} huérfanos. Ejemplos: " + ", ".join(huerfanos[:20]) + "...\n")
    else:
        report.append(", ".join(huerfanos) + "\n")
        
    report.append("## Vacíos Detectados")
    report.append(f"Se detectaron {len(vacios_detectados)} nodos que existen físicamente pero no tienen contenido desarrollado (plantillas o muy cortos).")
    report.append("Ejemplos prioritarios para desarrollar:")
    report.append("- " + "\\n- ".join(vacios_detectados[:15]) + "\n")
    
    report.append("## Mejoras Propuestas y Próximas Acciones Prioritarias")
    report.append("1. **Desarrollo de Vacíos:** Priorizar el llenado de los conceptos base en la carpeta `00_Conceptos/` que actualmente son plantillas.")
    report.append("2. **Fortalecimiento del Grafo:** Existen muchos nodos con `< 5` enlaces. Según la Regla Tarea 11, debemos enriquecer los textos existentes con más hipervínculos.")
    report.append("3. **Revisión de Huérfanos:** Conectar los documentos huérfanos desde otros sermones o estudios.")
    
    with open(REPORT_FILE, 'w', encoding='utf-8') as f:
        f.write("\n".join(report))
        
    print(f"Reporte generado en {REPORT_FILE}")
    
    # Generate Indice General
    INDICE_GENERAL.parent.mkdir(parents=True, exist_ok=True)
    indice_content = ["# Índice General Automatizado\n"]
    
    by_type = defaultdict(list)
    for data in nodes.values():
        t = data['metadata'].get('tipo', 'Sin Categoría') if isinstance(data['metadata'], dict) else 'Sin Categoría'
        if isinstance(t, list): t = t[0]
        by_type[str(t)].append(data['name'])
        
    for tipo, name_list in sorted(by_type.items()):
        indice_content.append(f"## {tipo}")
        for name in sorted(name_list):
            indice_content.append(f"- [[{name}]]")
        indice_content.append("")
        
    with open(INDICE_GENERAL, 'w', encoding='utf-8') as f:
        f.write("\n".join(indice_content))
        
    print(f"Índice General actualizado en {INDICE_GENERAL}")

if __name__ == '__main__':
    main()
