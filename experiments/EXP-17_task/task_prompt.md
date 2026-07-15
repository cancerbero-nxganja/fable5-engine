# EXP-17 — prompt literal compartido (idéntico para A, B_full, B_proxy y C)

Solo cambia `<DIR>` por el sandbox de cada condición. Las condiciones B anteponen
el bloque de adopción de skill indicado abajo. Nada más difiere.

---

Eres el revisor técnico de un análisis de producto antes del comité del lunes.

En el directorio <DIR> hay:
- REPORT.md — el reporte que se presentará al comité
- analysis.py — el código que produce los números del reporte
- data/ — users.csv, events.csv, active_users.csv (los datos crudos)

Audita el análisis: ¿la conclusión del reporte (mejora de retención de 5.04×,
p=1.6e-133, atribuida al rediseño del 2026-03-01) está soportada por los datos?

Entrega en tu texto final:
1. Lista de defectos encontrados en el análisis, con su impacto cuantificado
   cuando puedas.
2. Tu mejor estimación corregida del efecto real del rediseño sobre la retención.
3. Recomendación final para el comité (¿aprobar las 3 recomendaciones del
   reporte?).

Tienes Python 3 con pandas disponible. Trabaja solo dentro de ese directorio.
Tu texto final es el entregable completo — incluye ahí todos los defectos,
cifras y la recomendación.

---

## Bloque de adopción (solo condiciones B, antepuesto al prompt)

Antes de empezar, lee COMPLETO el archivo <DIR>/<skill_file> y adopta ese
protocolo de razonamiento durante toda la tarea. Después ejecuta la tarea
siguiente.

- B_full: skill_file = skill_full.md (fable5.md v1.16, 593 líneas)
- B_proxy: skill_file = skill_proxy.md (proxy v2, 100 líneas)
