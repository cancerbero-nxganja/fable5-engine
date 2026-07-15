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

- Runs completados: 12
- Último experimento: EXP-12 (2026-07-15) — uso óptimo de herramientas: **"usa herramientas de forma óptima" es la 7ª consigna-trampa** — la optimalidad no es de la llamada sino de la **economía de la afirmación que respalda**. La herramienta es la instancia material del principio diferencial (EXP-05): el canal más barato por el que el mundo puede desmentirte. CUÁNDO: disparador **por afirmación** (única-fuente-es-mi-generación + clase A–G), filtro económico `p·d·C > c` — con error 30× la llamada, verificar domina desde p>3.7% [CALC2] ("verifica la clase C" pasa de regla dura a teorema del modelo). CUÁL: por **refutación, no afinidad temática**; la observación **más estrecha que decide la pregunta** — leer el archivo entero para una pregunta puntual costó **43× más contexto que grep+lectura dirigida [CALC3, medido sobre este repo]** y el excedente fabrica la zona de fallo de recuperación enterrada (EXP-02): primera defensa contra el **sobre-uso** (la skill solo defendía el sub-uso). ORDEN: refutadores por **costo/p_kill ascendente** — exactamente óptimo, verificado por fuerza bruta en **2000/2000 instancias [CALC1]**; el orden "lógico de construcción" paga **1.97×** el óptimo (kill-cheapness de EXP-07 formalizada con factor de pérdida medido); observaciones independientes en **lote paralelo** (k round-trips → 1 [CALC4]; "planifica la frontera, no el camino"); secuencia sana observar → computar → mutar → verificar, mutaciones entre dos observaciones. Nuevo detector doble: **cero silencioso** (búsqueda sin resultados ≠ ausencia hasta validar el patrón sobre un positivo conocido) y **verde-nunca-visto-rojo** — "no encontró" y "no podía encontrar" son indistinguibles desde dentro. FASE 2 completa.
- Versión actual de la skill: 1.12
- Próximo experimento: EXP-13 (refinar la skill con los patrones de razonamiento de Fase 2 — arranca FASE 3, destilación)

---

## Criterio de éxito

La skill es "excepcional" cuando:
1. Un modelo Sonnet ejecutando la skill produce outputs indistinguibles de Fable 5 en >70% de los casos de prueba
2. La skill tiene ejemplos reales extraídos de experimentos (no hipotéticos)
3. Cada instrucción de la skill tiene evidencia de qué mejora y cuánto
