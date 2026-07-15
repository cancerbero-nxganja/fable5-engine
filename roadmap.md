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
- [ ] **EXP-10** — Documentar cómo Fable 5 evalúa si un resultado estadístico es real o artefacto
- [ ] **EXP-11** — Documentar cómo Fable 5 maneja ambigüedad en requerimientos
- [ ] **EXP-12** — Documentar cómo Fable 5 usa herramientas de forma óptima (cuándo, cuáles, en qué orden)

## FASE 3 — Destilación a la skill (runs 13-18)

- [ ] **EXP-13** — Refinar la skill con los patrones de razonamiento documentados en Fase 2
- [ ] **EXP-14** — Agregar ejemplos concretos extraídos de los experimentos anteriores
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

- Runs completados: 9
- Último experimento: EXP-09 (2026-07-15) — diseño de esquemas de base de datos sin redundancia: **"sin redundancia" es una consigna-trampa** (como "detecta", EXP-08). "Redundancia" confunde tres cosas que se separan con dos preguntas de frontera — **frontera A (temporal, EXP-06/07):** ¿la fuente cambia tras el evento? y **frontera B (dueño, EXP-06/08):** ¿la copia tiene dueño mecánico? Tres clases: (1) copia derivable-sin-dueño = redundancia patológica (anomalía de update, normalízala); (2) **snapshot as-of** (precio de línea, dirección de envío) = NO es redundancia, es un registro histórico (consérvala); (3) copia derivada **con dueño declarativo** (columna generada, vista materializada con `CHECK` de conservación) = redundancia gobernada (legítima como decisión de rendimiento). Meta-hallazgo: la frontera as-of de EXP-06 asciende de regla de aplicación a **operador generador de tablas** del esquema; la normalización es oráculo semi-honesto pero **ciego al tiempo** (no distingue snapshot de duplicado) → córrela *después* de la frontera A. Asimetría **a favor** por primera vez: el motor regala dueños mecánicos declarativos, así que "todo invariante, un dueño mecánico" (EXP-06) es aquí lo más barato → mapea cada invariante a una constraint
- Versión actual de la skill: 1.9
- Próximo experimento: EXP-10 (evaluar si un resultado estadístico es real o artefacto)

---

## Criterio de éxito

La skill es "excepcional" cuando:
1. Un modelo Sonnet ejecutando la skill produce outputs indistinguibles de Fable 5 en >70% de los casos de prueba
2. La skill tiene ejemplos reales extraídos de experimentos (no hipotéticos)
3. Cada instrucción de la skill tiene evidencia de qué mejora y cuánto
