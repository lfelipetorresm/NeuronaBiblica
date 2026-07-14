---
titulo: Protocolo de Auditoría Incremental (Algoritmo de SOC)
tipo: algoritmo_operativo
estado: Activo
etiquetas: ["#Protocolo", "#SOC", "#MejoraContinua", "#Auditoria"]
---

# ⚙️ Algoritmo de Mejora Continua: Protocolo de Auditoría Incremental

Este documento no es un "prompt" narrativo. Es el **Código Fuente Lógico** (el Sistema Operativo de Conocimiento) que rige el mantenimiento de la Bóveda. Cualquier Inteligencia Artificial invocada para tareas de mantenimiento debe ejecutar estricta y secuencialmente las siguientes 9 fases **sólo sobre el material nuevo o modificado (no sobre todo el millón de notas)**.

> [!IMPORTANT]
> **REGLA DE INCREMENTO:** A menos que el usuario exija una "Auditoría Completa" explícitamente, la IA debe preguntar: *"¿Cuáles fueron los últimos documentos modificados o agregados?"* y limitar este protocolo **exclusivamente a esos documentos y sus vecinos inmediatos**.

---

## El Algoritmo (Fases de Procesamiento)

### ⬇️ Fase 1: Escanear
**Actor Principal:** `Agente 01 Arquitecto`
- Recibir el bloque de documentos nuevos/modificados.
- Leer el contenido para entender la semántica, etiquetas y frontmatter.
- No modificar nada, solo ingestar la información en contexto.

### ⬇️ Fase 2: Detectar Errores
**Actor Principal:** `Agente 08 Auditor`
- Identificar enlaces rotos (`[[enlace_roto]]`).
- Identificar errores de Markdown o YAML (frontmatter incompleto).
- Detectar si falta Bibliografía o metadatos obligatorios en Sermones.

### ⬇️ Fase 3: Calcular Indicadores
**Actor Principal:** `Agente 08 Auditor`
- Evaluar la "salud" local del bloque de archivos.
- ¿Están bien cohesionados?
- Actualizar el `Tablero_Salud_NeuroBiblia.md` estimando el impacto de este nuevo bloque en los porcentajes globales.

### ⬇️ Fase 4: Crear Backlinks
**Actor Principal:** `Agente 13 Ontólogo`
- Buscar menciones no vinculadas (*unlinked mentions*) dentro del texto.
- Convertir palabras clave relevantes en enlaces `[[Backlink]]`.
- Cuidar de no sobre-enlazar (usar solo la primera aparición del término).

### ⬇️ Fase 5: Crear Sinapsis
**Actor Principal:** `Agente 13 Ontólogo`
- Conectar los nuevos archivos lógicamente usando el bloque `## 🔗 Relaciones Semánticas` (Define, Aclara, Contrasta, Precede, Habilita).
- Establecer vínculos explícitos a la doctrina (Ej. `07_Doctrinas`) y al léxico (Ej. `01_Biblia_Strong`).

### ⬇️ Fase 6: Actualizar Índices
**Actor Principal:** `Agente 12 Bibliotecario`
- Insertar los nuevos archivos en el MOC correspondiente (Ej. `00_Indice_General.md`).
- Organizar alfabéticamente o por categoría lógica.

### ⬇️ Fase 7: Eliminar Duplicados
**Actor Principal:** `Agente 11 Editor`
- Si el archivo nuevo aporta la misma información que un archivo viejo, fusionarlos.
- Eliminar la redundancia y dejar un solo nodo fuerte y unificado.

### ⬇️ Fase 8: Reestructurar
**Actor Principal:** `Agente 01 Arquitecto`
- Mover físicamente los archivos a la carpeta correcta si aterrizaron en el Inbox.
- Renombrar los archivos usando la convención de nomenclatura estándar (Ej. PascalCase o snake_case).

### ⬇️ Fase 9: Volver a Evaluar
**Actor Principal:** `Agente 08 Auditor`
- Re-verificar el bloque procesado.
- Si algún indicador local o global (Ej. Cohesión) cae por debajo del 95%, **Repetir desde la Fase 4**.
- Si todo es verde (>= 95%), detener el bucle y notificar al usuario.

---
*Fin de la Ejecución del SOC.*
