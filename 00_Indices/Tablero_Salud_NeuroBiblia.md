---
titulo: Tablero de Salud del SOC (Sistema Operativo de Conocimiento)
tipo: dashboard
estado: Activo
etiquetas: ["#Salud", "#Metricas", "#SOC", "#Auditoria"]
---

# 📊 Tablero de Salud: NEURONA BÍBLICA

Este tablero es actualizado por el **Gabinete de Expertos (Agente 08 Auditor y Agente 13 Ontólogo)** tras cada ciclo del Protocolo de Auditoría Incremental. Mide la calidad, integridad y conectividad de toda la base de conocimiento.

> [!TIP]
> **A la IA (Cuando seas invocada para auditoría):**
> Actualiza los valores de este tablero basándote en la evaluación de la carpeta o archivos recién ingresados. No necesitas recalcular todo desde cero, solo estima el impacto del nuevo material sobre las métricas globales.

---

## 📈 Indicadores Globales de Salud

| Métrica | Valor Estimado | Estado | Descripción |
| :--- | :---: | :---: | :--- |
| **Total de Documentos** | 49,584 | 🟢 | Nodos activos (Incluyendo Strong y Keil-Delitzsch) |
| **Cohesión** | 98.6 % | 🟢 | Medida en que los documentos están enlazados lógicamente (Hubs generados) |
| **Sinapsis** | 97 % | 🟢 | Calidad y profundidad de los enlaces bidireccionales |
| **Indexación** | 99 % | 🟢 | Porcentaje de documentos registrados en el Índice Maestro |
| **Cobertura Doctrinal** | 96 % | 🟢 | Desarrollo sistemático de la Teología |
| **Cobertura Histórica** | 97 % | 🟢 | Documentación de contextos y trasfondos (Mejorado con 10_Historia_Geografia) |
| **Calidad Global (GPA)** | **97.8 %** | 🟢 | Promedio general del Sistema Operativo de Conocimiento |

---

## ⚠️ Alertas y Cuellos de Botella (Radar de Anomalías)

| Anomalía | Cantidad | Acción Requerida | Responsable |
| :--- | :---: | :--- | :--- |
| **Documentos Huérfanos** | 0 | Curados por `soc_auditor_supremo.py` | Agente 13 Ontólogo |
| **Documentos Duplicados** | 0 | Fusionar o eliminar redundancia | Agente 08 Auditor |
| **Backlinks Faltantes** | ~10 | Nivel aceptable de dispersión en colas largas | Agente 13 Ontólogo |

---

## 🔄 Última Auditoría Incremental

- **Fecha de Auditoría:** 14 de Julio de 2026
- **Archivos Escaneados:** `10_Historia_Geografia/Historia_y_Geografia_Biblica`.
- **Fase Ejecutada:** Integración SOC (Pipeline ETL para PDF, Enriquecimiento YAML).
- **Veredicto:** El material "Historia y Geografía de la Biblia" se fragmentó en 16 nuevos nodos. Se actualizaron los perfiles agénticos (Agente 03 Historiador) para consultar esta nueva arquitectura. Se generó su propio Hub Maestro de cohesión.
