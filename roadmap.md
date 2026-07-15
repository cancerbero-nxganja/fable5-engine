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
- [x] **EXP-17** — Refinar el "modo proxy" con las instrucciones que más reducen la brecha
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

- Runs completados: 17
- Último experimento: EXP-17 (2026-07-15) — **la poda del modo proxy, medida.** Instrumento nuevo (retención de producto: 5.04× fabricado = 2.30 definición × 1.56 survivorship × 1.40 mix, efecto real nulo, corrección falsa incrustada, pseudo-replicación). Calibración en dos intentos: framing "audita" → Sonnet base **20/20** (techo; defectos no-canónicos NO rompen el techo — el framing que nombra la conducta la activa); framing neutro → C2 = **17/20**, con los 3 puntos perdidos exactamente en el cluster de EXP-15 (R1 reconciliación multiplicativa, R2 residuo, P3 veredicto: entregó "1.46× real" sin correr la estratificación que él mismo pidió). Resultados (prompt neutro literal idéntico): A Fable 20/20 (28k tok) · B_full 20/20 (96.5k, **2.36×** baseline — costo replicado de EXP-15) · **B_proxy (100 líneas) 20/20 (43.8k, 1.07×)**. Cierre de brecha 1.0 ambas skills (n=1, denominador 3 — baja potencia, reportado como tal). El proxy fue la única condición con la reconciliación explícita "1.40 × 2.30 × 1.56 = 5.04" — "un hecho, un hogar" medido sobre el output. Proxy validado en `experiments/EXP-17_proxy/fable5_proxy_v2.md`; skill v1.16 → v1.17 (sección EXP-17 con 6 instrucciones + 2 señales de detector + CASO EXP-17; el archivo maestro NO se podó — esa es EXP-18).
- Versión actual de la skill: 1.17
- Próximo experimento: EXP-18 (generar la versión 2.0 de la skill con todo lo aprendido — la poda del archivo maestro; precondición actualizada por EXP-17: replicar la paridad del proxy en un **segundo instrumento** de género distinto antes de cortar, y medir con rúbrica de disciplina + economía de tokens, no con la banda 30–70% que resultó inalcanzable)
---

## Criterio de éxito

La skill es "excepcional" cuando:
1. Un modelo Sonnet ejecutando la skill produce outputs indistinguibles de Fable 5 en >70% de los casos de prueba
2. La skill tiene ejemplos reales extraídos de experimentos (no hipotéticos)
3. Cada instrucción de la skill tiene evidencia de qué mejora y cuánto
