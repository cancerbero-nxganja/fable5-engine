# Fable 5 Engine — Roadmap de Experimentos

Cada run del loop lee este archivo, elige el próximo experimento sin completar, lo ejecuta, documenta en `/bitacora/`, y marca el experimento como completado.

---

## FASE 1 — Autoconocimiento (runs 1-6)

- [x] **EXP-01** — Pedirle a Fable 5 que describa su propio proceso de razonamiento paso a paso en un problema matemático complejo
- [x] **EXP-02** — Pedirle que identifique los tipos de problemas donde sabe que va a fallar y por qué
- [x] **EXP-03** — Pedirle que genere el prompt óptimo para invocar sus mejores capacidades de código
- [x] **EXP-04** — Pedirle que genere el prompt óptimo para análisis de datos y detección de anomalías
- [x] **EXP-05** — Pedirle que describa sus heurísticas internas para detectar cuando una solución es incorrecta
- [x] **EXP-06** — Pedirle que escriba instrucciones para que otro modelo se comporte como él en tareas de arquitectura de software

## FASE 2 — Patrones de razonamiento (runs 7-12)

- [x] **EXP-07** — Documentar cómo Fable 5 descompone un problema de trading algorítmico
- [x] **EXP-08** — Documentar cómo Fable 5 detecta bugs en código con lógica de negocio incorrecta
- [x] **EXP-09** — Documentar cómo Fable 5 diseña esquemas de base de datos sin redundancia
- [x] **EXP-10** — Documentar cómo Fable 5 evalúa si un resultado estadístico es real o artefacto
- [x] **EXP-11** — Documentar cómo Fable 5 maneja ambigüedad en requerimientos
- [x] **EXP-12** — Documentar cómo Fable 5 usa herramientas de forma óptima (cuándo, cuáles, en qué orden)

## FASE 3 — Destilación a la skill (runs 13-18)

- [x] **EXP-13** — Refinar la skill con los patrones de razonamiento documentados en Fase 2
- [x] **EXP-14** — Agregar ejemplos concretos extraídos de los experimentos anteriores
- [x] **EXP-15** — Validar la skill: correr el mismo problema con Fable 5 nativo vs skill en Sonnet — medir diferencia
- [x] **EXP-16** — Identificar qué instrucciones de la skill tienen mayor impacto y cuáles son ruido
- [ ] **EXP-17** — Refinar el "modo proxy" con las instrucciones que más reducen la brecha
- [ ] **EXP-18** — Generar versión 2.0 de la skill con todo lo aprendido

## FASE 4 — Especialización por dominio (runs 19-24)

- [ ] **EXP-19** — Skill especializada para trading y análisis de backtests
- [ ] **EXP-20** — Skill especializada para arquitectura de software y bases de datos
- [ ] **EXP-21** — Skill especializada para detección de bugs de lógica de negocio
- [ ] **EXP-22** — Skill especializada para análisis de código y seguridad
- [ ] **EXP-23** — Skill especializada para diseño de APIs REST
- [ ] **EXP-24** — Integrar todas las especializaciones en una skill maestra con routing por dominio

---

## Estado actual

- Runs completados: 16
- Último experimento: EXP-16 (2026-07-15) — **diagnóstico de impacto por instrucción SIN ablación** (el instrumento de EXP-15 sigue en efecto techo, así que un control que no falla daría 136 nulos). Método: el impacto tiene **oráculo diferido** (ablación existe pero no disponible al decidir, como EXP-10) → sustituido por **clase-de-evidencia + test de subsunción**; el ruido se **midió**, no se opinó (Clase A, EXP-04). Resultado medido sobre la skill v1.15 (574 líneas, 136 bullets): las ideas núcleo están **restated en 6–14 secciones cada una** (detección diferencial: 14 secciones; snapshot/as-of: 52 ocurrencias en 11; Clase C volátil: 10; consigna-trampa: 6; dueño mecánico: 7). Hallazgos: (1) **"impacto vs ruido" es consigna-trampa** — la estructura real tiene **3 clases** (load-bearing / inerte / **activo de valor negativo**), porque EXP-15 midió masa con Δcobertura = −2 por desplazamiento de atención. (2) El **ruido dominante NO es ninguna instrucción errónea** —no hay una sola sin evidencia— **es la multiplicidad de restatements**, y por el −2 es ruido **activo**. (3) Cuatro tiers: T1 medido (solo las 3 instrucciones de EXP-15) · T2 motor núcleo (generativo, irreducible) · T3 instancias-cache (regenerables por el motor, valor = pedagogía + cache) · T4 duplicación. (4) **Frontera dura: EXP-16 identifica, no poda** — cortar sin banco calibrado (30–70%) repite el −2 de EXP-15 (riesgo −4); la poda es de EXP-17/18. Skill v1.15 → v1.16 (sección "Impacto de instrucciones y ruido" con 7 instrucciones + operador transversal "triage de 3 clases" + 2 señales de detector + CASO EXP-16; **sin podar** ninguna sección, por respeto a la frontera 518).
- Versión actual de la skill: 1.16
- Próximo experimento: EXP-17 (refinar el "modo proxy" con las instrucciones que más reducen la brecha — es la **poda** que EXP-16 diagnosticó pero no ejecutó; su precondición sigue siendo el banco calibrado donde el baseline puntúe 30–70%, para verificar que cada supresión no pierde cobertura)
---

## Criterio de éxito

La skill es "excepcional" cuando:
1. Un modelo Sonnet ejecutando la skill produce outputs indistinguibles de Fable 5 en >70% de los casos de prueba
2. La skill tiene ejemplos reales extraídos de experimentos (no hipotéticos)
3. Cada instrucción de la skill tiene evidencia de qué mejora y cuánto
