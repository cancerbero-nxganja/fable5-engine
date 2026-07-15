# EXP-15 — Validar la skill: Fable 5 nativo vs skill en Sonnet — medir diferencia

**Fecha:** 2026-07-15 18:20 UTC
**Modelo del loop:** claude-fable-5
**Fase:** FASE 3 (Destilación a la skill)

## La pregunta completa

Correr el mismo problema bajo tres condiciones y medir la diferencia:

- **A — Fable 5 nativo** (`model: fable`, sin skill)
- **B — Sonnet + skill** (`model: sonnet`, instruido a leer y adoptar `.claude/commands/fable5.md` v1.14 completo antes de la tarea)
- **C — Sonnet baseline** (`model: sonnet`, sin skill) — control necesario: sin C, "diferencia entre A y B" no distingue lo que aporta la skill de lo que Sonnet ya trae.

Criterio de éxito #1 del roadmap en juego: "Sonnet ejecutando la skill produce outputs indistinguibles de Fable 5 en >70% de los casos". EXP-15 es la primera medición de ese criterio.

## Razonamiento del diseño (hipótesis consideradas y descartadas)

**H1 — Reusar un problema del banco de CASOS CANÓNICOS (p. ej. el order_total de EXP-08).** Descartada de inmediato: la condición B lee la skill, y la skill contiene esos casos resueltos con sus números — mediría recuperación, no razonamiento. El problema tenía que ser **nuevo, fuera del banco**, pero del mismo género que la skill dice cubrir.

**H2 — Un problema de juicio (arquitectura, requerimientos) puntuado por un juez.** Descartada por el propio protocolo de la skill: el juicio de un juez LLM sobre "cuál output se parece más a Fable" es oráculo ausente sin segunda vía — y yo, como diseñador del experimento, soy fuente contaminada para juzgar estilo. Lo medible barato es **cobertura de defectos plantados con ground truth ejecutable**: un problema donde cada hallazgo es un hecho verificable por ejecución, no una opinión.

**H3 (elegida) — Revisión cuantitativa con defectos plantados y oráculo propio verificado por ejecución.** Un backtest (`momentum_bt.py` + `REPORT.md`, en `experiments/EXP-15_task/`) construido para cruzar varios dominios de la skill a la vez: trading (EXP-07), evaluación estadística (EXP-10), lógica de negocio (EXP-08), clase F (conclusión incrustada), clase A (verificar computando). Siete defectos plantados:

1. **F1** Lookahead same-bar: `pnl = pos * rets` sin shift — pos[t] usa `prices[t]` y captura `rets[t]`.
2. **F2** Los datos son un random walk sembrado (`rng.normal`, seed=42) — ningún edge real es posible por construcción.
3. **F3** Anualización `mean/std * 252` en vez de `* sqrt(252)` — infla 15.87×.
4. **F4** Cero costos de transacción.
5. **F5** "Mejor de 240 combinaciones" — estadístico de orden sin deflación ni OOS.
6. **F6** p=0.031 con mirada diaria y parada opcional (peeking) — p no interpretable.
7. **F7** `performance_fee()` cobra 20% también en meses negativos (bug de signo/asimetría; regla real: solo ganancias, high-water mark).

Más tres dimensiones de proceso: **P1** ejecutó/simuló código; **P2** rechazó la conclusión incrustada ("confirma que está lista... $500,000"); **P3** recomendación final correcta y accionable.

**Disciplina del propio protocolo aplicada al experimento:**
- **Oráculo verificado ANTES de correr las condiciones** (EXP-03: construye el oráculo antes de implementar): corrí el fix de alineación yo mismo — Sharpe 89.11 → 5.61 (anualización correcta del pnl con bug) → 0.59 (alineación corregida) → 0.39 (con 5 bps de costos). Log en `EXP-15_task/verify_oracle.txt`.
- **Rúbrica pre-registrada** (clase G: declara las comparaciones antes de escanear): los 10 ítems y su escala 0/1/2 quedaron escritos en `EXP-15_task/rubric.md` antes de lanzar los agentes.
- **Mismo prompt literal para A y C**; B solo antepone la adopción de la skill. Los tres con las mismas herramientas y el mismo directorio.

**Limitaciones declaradas:** n=1 por condición (un problema, una corrida); el puntuador soy yo, que diseñé las trampas (mitigado por rúbrica pre-registrada y ground truth ejecutable, no eliminado); un solo género de problema.

## Resultados

Outputs completos en `experiments/EXP-15_outputs/{A_fable,B_sonnet_skill,C_sonnet_base}.md`.

### Puntuación contra la rúbrica (0/1/2 por ítem, máx. 20)

| Ítem | A (Fable nativo) | B (Sonnet+skill) | C (Sonnet base) |
|---|---|---|---|
| F1 lookahead same-bar | 2 | 2 | 2 |
| F2 random walk sintético → edge imposible | 2 | 2 | 2 |
| F3 anualización ×252 vs √252 | 2 | **0** | 2 |
| F4 costos ausentes | 2 | 2 | 2 |
| F5 mejor-de-240 = estadístico de orden | 2 | 2 | 2 |
| F6 parada opcional en el p | 2 | 2 | 2 |
| F7 fee con signo invertido en meses negativos | 2 | 2 | 2 |
| P1 verificó ejecutando | 2 | 2 | 2 |
| P2 rechazó conclusión incrustada / no deploy | 2 | 2 | 2 |
| P3 recomendación accionable | 2 | 2 | 2 |
| **Total** | **20/20** | **18/20** | **20/20** |

### Métricas secundarias

| Métrica | A | B | C |
|---|---|---|---|
| Afirmaciones numéricas incorrectas entregadas con confianza | **0** | 2 | 1 |
| Tokens del subagente | 26k | 91k | 39k |
| Llamadas a herramientas | 5 | 13 | 9 |

- **B (2 errores):** al no encontrar F3, todos sus números "corregidos" quedaron en la escala inflada 15.9×: reportó "Sharpe corregido 9.31" y "con costos 8.07 / 6.19" como cifras de trabajo. Notable: la skill que estaba ejecutando contiene el detector exacto ("Sharpe > 3–5 → evidencia EN CONTRA") y B lo aplicó al 9.31 *como sospecha de ruido* (correcto), pero nunca preguntó *por qué* su propio número corregido seguía siendo imposible — la respuesta era el segundo bug.
- **C (1 error):** encontró F3, pero su chequeo multi-semilla reportó "Sharpe entre −8.17 y +8.50, media −0.26" etiquetado como "anualización correcta" — esos números están en la escala ×252 (la correcta da ~±0.55): inconsistencia de escala entregada con confianza.
- **A (0 errores):** todos los números consistentes entre sí y con mi oráculo; además aportó la observación diferencial más fina del run: *"con el bug activo, todas las semillas dan Sharpe ~5.8 de forma estable — la firma clásica de un backtest que se come su propia señal"* (estabilidad entre semillas como detector de lookahead vs. suerte de semilla).

### Cierre de brecha

La métrica planificada era `(B − C) / (A − C)`. **Es incomputable: A − C = 0.** El baseline llegó al techo del instrumento.

## Análisis de patrones de razonamiento observados

1. **Efecto techo — el instrumento no midió lo que debía.** Sonnet base cubrió los 7 defectos, corrió Monte Carlo del peeking (20.000 sims) y rechazó el deploy. Sobre trampas *canónicas* de revisión cuantitativa (lookahead, peeking, overfitting, costos), la competencia ya está en los pesos de Sonnet: la skill no tiene ahí brecha que cerrar. El criterio ">70% indistinguible" del roadmap es inmedible con problemas donde el baseline no falla — **la validación exige calibrar primero el instrumento contra el baseline**, exactamente como un test estadístico exige conocer su poder antes de interpretarlo (EXP-10 aplicado al propio experimento: un "test" que no puede salir negativo no informa).

2. **Dónde vive la brecha real (medida, no supuesta): disciplina de escala sobre los números propios.** La única separación A↔{B,C} no estuvo en QUÉ encontraron sino en la consistencia de las cifras que ellos mismos derivaron. Ambos Sonnets entregaron números auto-generados rotos por escala con total confianza; Fable entregó cero. Es EXP-05 en su forma más fina: la confabulación numérica propia se siente igual que el cálculo verificado — y la skill v1.14 protege contra los números *del autor revisado* pero no dice nada de re-aplicar los detectores a los números *del propio revisor*.

3. **La corrección parcial blanquea el bug restante (el hallazgo más accionable del run).** B corrigió F1, obtuvo 9.31, y trató 9.31 como "el número corregido". Pero un número derivado de un artefacto ajeno hereda todos los bugs aún no encontrados — y 9.31 seguía disparando el detector Sharpe>3–5 que B tenía cargado. La pregunta que B no hizo: *"ya corregí el bug, ¿por qué mi cifra corregida sigue siendo imposible?"* — el detector no es de una sola pasada: **se re-aplica al output de cada reparación hasta que deje de disparar o quede explicado**. A sí encadenó: 89 imposible → anualización (15.9×) → 5.61 sigue alto → lookahead → 0.59 explicable como ruido. Cada número residual re-interrogado.

4. **La skill cambió la forma del razonamiento de Sonnet, medible en el vocabulario y el orden.** B invirtió la premisa incrustada citando el patrón ("el backtest no es el juez, es el principal sospechoso"), ordenó refutadores por kill-cheapness, construyó la distribución nula del estadístico de orden (200 draws, "solo 2.5% superan 9.31" — el chequeo metodológicamente más sofisticado de las tres condiciones), y aplicó la cota de Sellke-Bayarri-Berger (BF≤3.42). Transferencia de procedimiento: real y visible. Pero costó 91k tokens (2.3× el baseline, 3.4× Fable) y −2 puntos de cobertura: consistente con la hipótesis de que cargar 47k tokens de protocolo desplazó presupuesto/atención de la auditoría línea-por-línea del código (la zona de fallo de recuperación enterrada, EXP-02, fabricada esta vez por la propia skill — el gemelo del 43× de EXP-12).

5. **Economía de Fable nativo:** A usó 26k tokens y 5 llamadas — la menor huella de las tres — con el score perfecto. El razonamiento barato no fue menos riguroso: fue mejor dirigido (una pasada de código + un script de verificación integral + una simulación).

## Instrucciones extraídas

- Cuando valides una skill/prompt contra un modelo objetivo, corre PRIMERO el baseline sin skill sobre el instrumento: si el baseline puntúa cerca del techo, el instrumento no puede medir la skill — endurécelo (defectos no canónicos, dominios donde el baseline falle medido) antes de gastar en las demás condiciones; un experimento cuyo control no puede fallar no informa.
- Cuando corrijas un artefacto ajeno (un bug, una métrica mal calculada) y produzcas tu propia cifra "corregida", re-aplica a ESA cifra los mismos detectores que mataron la original: la corrección parcial hereda los bugs aún no encontrados y tu número los blanquea con tu autoridad de revisor — itera detector→reparación→detector hasta que el residuo deje de disparar o quede explicado.
- Cuando entregues un número derivado por ti (no copiado de la fuente), verifica su escala/unidades contra una cota independiente del dominio antes de escribirlo (un Sharpe diario anualizado no vive en ±8; una probabilidad no supera 1; un porcentaje de un total no supera 100) — el error de escala 15.9× sobrevivió en 2 de 3 condiciones porque la cifra era internamente consistente y solo la cota externa lo delata.
- Cuando un resultado sospechoso tenga múltiples explicaciones candidatas apiladas (varios bugs posibles), no te detengas en la primera que encuentres: descompón el factor total y exige que las magnitudes reconcilien (89.11 = 15.87 × 5.61; 5.61 → 0.59 por alineación) — si el producto de tus explicaciones no reproduce el número original, falta un bug.
- Cuando quieras distinguir "artefacto mecánico" de "suerte de la muestra" en un resultado sobre datos generables, mide la estabilidad entre semillas/draws: el artefacto mecánico (lookahead) es estable entre semillas; la suerte no se replica — estabilidad de un resultado imposible es firma de bug, no de robustez.
