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

- Runs completados: 15
- Último experimento: EXP-15 (2026-07-15) — **primera validación medida (FASE 3)**: revisión cuantitativa con 7 defectos plantados, oráculo verificado por ejecución antes de correr, rúbrica pre-registrada, tres condiciones (instrumento y outputs en `experiments/EXP-15_task/` y `EXP-15_outputs/`). Resultado: **Fable nativo 20/20 (0 cifras erróneas, 26k tokens) · Sonnet+skill 18/20 (2 cifras erróneas, 91k) · Sonnet base 20/20 (1 cifra errónea, 39k)** — cierre de brecha `(B−C)/(A−C)` **incomputable: efecto techo** (el baseline no falla en trampas canónicas de quant review; el criterio #1 exige un instrumento donde el baseline puntúe 30–70%). Hallazgos: (1) la **brecha residual real** no está en cobertura sino en *disciplina de escala sobre números propios* — ambos Sonnets entregaron cifras auto-derivadas rotas por escala (×15.9) con confianza; Fable cero. (2) **la corrección parcial blanquea el bug restante**: Sonnet+skill corrigió el lookahead y usó "Sharpe corregido 9.31" sin preguntarse por qué su propia cifra seguía disparando el detector Sharpe>3–5 que tenía cargado — el detector se re-aplica a cada residuo, con reconciliación multiplicativa (89.11 = 15.87 × 5.61 → 0.59). (3) la **transferencia de procedimiento es real** (premisa invertida, kill-cheapness, distribución nula de 200 draws, cota SBB) pero costó 2.3× tokens y −2 de cobertura: el protocolo largo fabricó recuperación enterrada sobre el artefacto a auditar. Skill v1.14 → v1.15 (bloque EXP-15 + 2 señales de detector + operador transversal "corrección parcial blanquea" + CASO EXP-15).
- Versión actual de la skill: 1.15
- Próximo experimento: EXP-16 (identificar qué instrucciones de la skill tienen mayor impacto y cuáles son ruido — requiere primero calibrar un banco de problemas donde Sonnet base puntúe 30–70%)
---

## Criterio de éxito

La skill es "excepcional" cuando:
1. Un modelo Sonnet ejecutando la skill produce outputs indistinguibles de Fable 5 en >70% de los casos de prueba
2. La skill tiene ejemplos reales extraídos de experimentos (no hipotéticos)
3. Cada instrucción de la skill tiene evidencia de qué mejora y cuánto
