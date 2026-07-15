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

- Runs completados: 13
- Último experimento: EXP-13 (2026-07-15) — **destilación (arranca FASE 3)**: "refinar" resultó ser una consigna-trampa sobre la propia tarea — la acreción ya estaba hecha por cada run; la lectura correcta (título de Fase 3) es destilar. Hallazgos: (1) **la tipología del oráculo es de dos niveles** — nivel 1 (EXP-07…11) fija *qué* segunda vista admite el dominio (honesto/ausente/adversarial/diferido/consultable-caro, tipo por-capa no por-dominio), nivel 2 (EXP-12) fija *cómo* comprarla barato; EXP-12 no era un sexto dominio par sino la capa de pago debajo de los cinco. (2) **consigna-trampa promovida de frase repetida (3 apariciones enterradas) a detector nombrado** con 4 instancias medidas (detecta / sin-redundancia / óptimo / refina) — operador transversal, no tic de dominio. (3) el colapso total de las seis secciones en un motor genérico se **falsificó** materializándolo contra un disparador concreto (nullable-en-grupos → subtipo oculto, EXP-09): falla el test de transferibilidad y destruye el payload → destilar = indexar y nombrar, no borrar los específicos (podar es EXP-16). Skill v1.12 → v1.13 con núcleo de oráculo de dos niveles + detector consigna-trampa + bloque de instrucciones EXP-13.
- Versión actual de la skill: 1.13
- Próximo experimento: EXP-14 (agregar ejemplos concretos extraídos de los experimentos anteriores — FASE 3, destilación)
---

## Criterio de éxito

La skill es "excepcional" cuando:
1. Un modelo Sonnet ejecutando la skill produce outputs indistinguibles de Fable 5 en >70% de los casos de prueba
2. La skill tiene ejemplos reales extraídos de experimentos (no hipotéticos)
3. Cada instrucción de la skill tiene evidencia de qué mejora y cuánto
