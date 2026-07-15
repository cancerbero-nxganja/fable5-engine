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

- Runs completados: 11
- Último experimento: EXP-11 (2026-07-15) — manejo de ambigüedad en requerimientos: **"maneja la ambigüedad" es la 6ª consigna-trampa** — la ambigüedad no es propiedad del texto sino del par **(texto, decisión)**: solo importa la que hace divergir decisiones caras. La peligrosa es **invisible desde dentro** (EXP-05 aplicado a la lectura): leer compila con defaults y el rellenado no deja rastro — releer es segunda cuenta, no segunda vista; el detector es material: **caminar una entidad concreta con nombre y fechas por el texto** (el ejemplo de EXP-03 invertido: allí cerraba fronteras, aquí las abre). Números calculados (clase A, `experiments/EXP-11_sim.py`): un párrafo de 3 frases = 8 dimensiones × 2–3 lecturas = **864 implementaciones**; elección silenciosa con 80% de acierto por dimensión → **16.8%** de acertar la intención completa (falsifica "elige la interpretación más útil" del Paso 1 v1.10 — primera auto-falsificación de la skill); triage divergencia × irreversibilidad → 3 de 8 dimensiones (auth, PII, reversibilidad — todas invariantes del dominio) concentran **92.7%** del riesgo; sin canal de consulta la lectura menos probable pero barata de corregir domina **5.3×** (minimax-regret ≠ máx-verosimilitud). Taxonomía: ambigüedad **léxica / de frontera / de omisión** (la de omisión — auth, PII, tenancy — no tiene frase que releer). Tipología del oráculo completa con el 5º tipo: **consultable-caro** (el autor: responde, pero cada consulta es un round-trip y reacciona a concreciones mejor de lo que especifica → lote decisión+default, ejemplo caminado en vez de paráfrasis)
- Versión actual de la skill: 1.11
- Próximo experimento: EXP-12 (uso óptimo de herramientas: cuándo, cuáles, en qué orden)

---

## Criterio de éxito

La skill es "excepcional" cuando:
1. Un modelo Sonnet ejecutando la skill produce outputs indistinguibles de Fable 5 en >70% de los casos de prueba
2. La skill tiene ejemplos reales extraídos de experimentos (no hipotéticos)
3. Cada instrucción de la skill tiene evidencia de qué mejora y cuánto
