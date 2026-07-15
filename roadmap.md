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
- [ ] **EXP-15** — Validar la skill: correr el mismo problema con Fable 5 nativo vs skill en Sonnet — medir diferencia
- [ ] **EXP-16** — Identificar qué instrucciones de la skill tienen mayor impacto y cuáles son ruido
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

- Runs completados: 14
- Último experimento: EXP-14 (2026-07-15) — **ejemplos concretos (FASE 3)**: "agregar ejemplos" resultó ser la quinta instancia medida de consigna-trampa — la propiedad real (por EXP-03 aplicado a la propia skill) es *cerrar la semántica de frontera que la prosa de cada instrucción deja abierta*: el ejemplo es el oráculo de la instrucción. Hallazgos: (1) **el ejemplo que transfiere es el que contiene el error refutado** — el par que enseña procedimiento de detección es (lectura ingenua ejecutada → refutación → corrección), no (entrada → salida correcta); ese fue el criterio de admisión al banco. (2) **colocación por índice sobre la infraestructura existente**: las citas `(EXP-XX)` que ya saturan la skill se volvieron punteros resolubles a un banco de CASOS CANÓNICOS keyed por EXP-ID — descartados por materialización el apéndice desconectado (recuperación enterrada, EXP-02) y el inline exhaustivo (43×, EXP-12); cero ediciones sobre las instrucciones = cero riesgo de regresión. (3) **triage de EXP-11 hacia adentro**: 11 casos (no ~100) — solo gana ejemplo la instrucción cuyas lecturas divergen en decisiones caras. Banco: EXP-01 (1/4→3/8), EXP-04 (P=0.82→1.0), EXP-05 (182 vs 23), EXP-06 (precio de línea), EXP-07 (RSI al close), EXP-08+08b (signo/orden/conservación), EXP-09 ($20→$24), EXP-10 (18%/11%/3×/24%), EXP-11 (María), EXP-12 (43×/1.97×/3.7%). Skill v1.13 → v1.14 (+10%, contra 2-3× del inline). Criterio de éxito #2 del roadmap cubierto.
- Versión actual de la skill: 1.14
- Próximo experimento: EXP-15 (validar la skill: correr el mismo problema con Fable 5 nativo vs skill en Sonnet — medir diferencia)
---

## Criterio de éxito

La skill es "excepcional" cuando:
1. Un modelo Sonnet ejecutando la skill produce outputs indistinguibles de Fable 5 en >70% de los casos de prueba
2. La skill tiene ejemplos reales extraídos de experimentos (no hipotéticos)
3. Cada instrucción de la skill tiene evidencia de qué mejora y cuánto
