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

- Runs completados: 10
- Último experimento: EXP-10 (2026-07-15) — evaluación de resultados estadísticos: **"¿es real?" es la 5ª consigna-trampa** — la propiedad no vive en el número sino en el **procedimiento que lo generó**, y el procedimiento no viene impreso en el número. Asimetría estructural vs. EXP-04: allí eres el analista; aquí el resultado **llega hecho** y llegó *porque fue interesante* — el canal de atención selecciona, así que **todo resultado mostrado es un estadístico de orden por defecto** (el "mejor de N" de EXP-07 generalizado) y el sesgo al alza es el caso por defecto. Números medidos por simulación (clase A en modo generativo): peeking 9 miradas → error tipo I real **18%**; 12 subgrupos → min p<0.01 el **11%**; winner's curse con poder 14% → estimación **×3.0** el efecto real; posterior con prior 10% → P(real|sig)=**24%** (≈8% con peeking); cota SBB: p=0.03 → **BF≤3.5**. Hallazgos eje: re-análisis del mismo dato = segunda *cuenta*, no segunda *vista* (la única segunda vía es replicación en datos no usados en la búsqueda); **la deflación es parámetro de diseño** (el test confirmatorio se dimensiona contra el efecto deflactado, no el reportado, o nace infrapotenciado y su fallo se lee como refutación); tipología del oráculo completa con el tipo **diferido** (replicación honesta pero no disponible al decidir → interrogatorio + deflación + posterior)
- Versión actual de la skill: 1.10
- Próximo experimento: EXP-11 (manejo de ambigüedad en requerimientos)

---

## Criterio de éxito

La skill es "excepcional" cuando:
1. Un modelo Sonnet ejecutando la skill produce outputs indistinguibles de Fable 5 en >70% de los casos de prueba
2. La skill tiene ejemplos reales extraídos de experimentos (no hipotéticos)
3. Cada instrucción de la skill tiene evidencia de qué mejora y cuánto
