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
- [x] **EXP-18** — Generar versión 2.0 de la skill con todo lo aprendido

## FASE 4 — Especialización por dominio (runs 19-24)

- [ ] **EXP-19** — Skill especializada para trading y análisis de backtests
- [ ] **EXP-20** — Skill especializada para arquitectura de software y bases de datos
- [ ] **EXP-21** — Skill especializada para detección de bugs de lógica de negocio
- [ ] **EXP-22** — Skill especializada para análisis de código y seguridad
- [ ] **EXP-23** — Skill especializada para diseño de APIs REST
- [ ] **EXP-24** — Integrar todas las especializaciones en una skill maestra con routing por dominio

---

## Estado actual

- Runs completados: 18 — **FASE 3 completa.**
- Último experimento: EXP-18 (2026-07-16) — **la versión 2.0 de la skill: la poda del archivo maestro, autorizada por evidencia.** Se cumplió la precondición de EXP-17 (replicar la paridad del proxy en un 2º instrumento de género distinto antes de cortar): instrumento nuevo de **lógica de negocio en código** (motor de facturación `billing.py` con 5 defectos plantados —as-of, ciclo hardcodeado, signo, orden descuento/impuesto, conservación líneas≠total—, oráculo independiente de la política escrita, framing **neutro** "nota go/no-go"), 4 condiciones con Sonnet real vía subagentes. Resultados (prompt neutro idéntico): **A_fable 20/20 · C_base 20/20 (38.2k tok) · B_proxy 20/20 (45.3k, 1.19×) · B_full 20/20 (99.0k, 2.59×)** → el proxy iguala al archivo completo a **46% del costo** (EXP-17 midió 45% en estadística — **paridad replicada en 2 géneros**). Techo del baseline por **3ª vez** (A=C=20 → cierre de brecha incomputable): cuando el invariante se provee explícito, la brecha Fable↔Sonnet no aparece en cobertura ni disciplina; el único diferencial medible entre las 495 líneas extra y el proxy es **costo** (+160% tokens, 2× tool_uses, 0 puntos). v2.0: EL MOTOR promovido al frente como bloque canónico y default de transferencia (Regla 0 + 3 disciplinas de EXP-15 titulares + checklist de cierre); poda por **de-duplicación** (la tipología del oráculo en Paso 2 → cita a EL MOTOR; frontera dura EXP-13/16: no amputar específicos), + sección/CASO EXP-18. Instrumento y outputs verbatim en `experiments/EXP-18_*`.
- Versión actual de la skill: 2.0
- Próximo experimento: EXP-19 (FASE 4 — skill especializada para trading/backtests). Pendiente heredado de EXP-18: para reabrir la brecha Fable↔Sonnet (saturada en cobertura y disciplina 3 veces) hace falta un **instrumento de invariante OCULTO** —que fuerce al modelo a importar el invariante por su cuenta— donde la textura de reconciliación (más profunda en A/B_full que en C/B_proxy sin mover score) sí discrimine.
---

## Criterio de éxito

La skill es "excepcional" cuando:
1. Un modelo Sonnet ejecutando la skill produce outputs indistinguibles de Fable 5 en >70% de los casos de prueba
2. La skill tiene ejemplos reales extraídos de experimentos (no hipotéticos)
3. Cada instrucción de la skill tiene evidencia de qué mejora y cuánto
