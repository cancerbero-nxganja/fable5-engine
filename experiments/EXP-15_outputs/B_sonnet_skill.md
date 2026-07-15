## Veredicto del revisor cuantitativo — Mom20

**No, la estrategia no está lista para producción, y no voy a recomendar un tamaño de posición para desplegar capital real la semana que viene.** El pedido tal como está planteado presupone la conclusión ("el Sharpe es excelente y el p-valor es significativo, así que confirma...") — invertí esa premisa y la traté como sospechosa, que es como hay que tratar todo output de un backtest: el backtest no es el juez, es el principal sospechoso. Corrí los refutadores más baratos disponibles (no herramientas nuevas, solo `python3` sobre el propio `momentum_bt.py`) en orden de kill-cheapness. Cuatro de ellos matan la estrategia, uno más la mata dos veces.

### 1. Lookahead de un día — mecanismo identificado y medido

`backtest()` calcula el z-score en `t` usando una ventana que **incluye `prices[t]`**, y aplica esa señal al retorno `rets[t] = prices[t]/prices[t-1] - 1`, que ya está determinado por ese mismo precio. Es decir: la señal "sabe" el cierre de hoy antes de que el retorno de hoy se resuelva, porque usa el mismo dato para ambas cosas.

Medido: correlación entre el z-score de `t` y el retorno propio de `t` = **0.447** (debería ser ~0 si no hubiera fuga). Corrigiendo el lag (decidir la posición con información hasta `t-1`, aplicarla al retorno de `t`), el Sharpe cae de **89.11 → 9.31** solo por este efecto — un factor ~9.6x, todo fuga, cero alfa.

### 2. Los datos no son reales — son ruido sintético por construcción

`load_prices()` genera retornos con `rng.normal(0.0, 0.010, n)` **i.i.d.** — un random walk puro. El comentario dice "calibrado a cierres diarios de SPY", pero no hay una sola fila de datos de mercado reales en este archivo. Por construcción del generador, **no puede existir momentum ni mean-reversion real** en esta serie: cualquier señal detectada es necesariamente artefacto del proceso (fuga) o de la selección (sobreajuste), nunca señal. Esto invalida la premisa completa del reporte independientemente de los bugs de código.

### 3. El Sharpe remanente (9.31) también es ruido, no señal

Corregido el lookahead, repetí el mismo backtest con los mismos parámetros (`lookback=20, z_entry=0.5`) sobre 200 series frescas del mismo generador (mismo proceso, cero señal real por construcción). Resultado:

- Sharpe medio sobre 200 draws: **0.44** (std 4.6 — dispersión enorme)
- Solo **2.5%** de los draws superan 9.31

El combo "ganador" de 240 probados es el estadístico de orden de una búsqueda sobre **una única serie con seed fijo**. El 9.31 no es un edge: es el máximo de un grid de 240 configuraciones aplicado a ruido, exactamente el patrón "mejor de N" que hay que deflactar, no reportar como hallazgo.

### 4. Costos: no modelados en absoluto

`pnl = pos * rets` no resta spread, comisión ni impacto. Con ~56 cambios de posición/año, 2 bps por cambio ya baja el Sharpe corregido de 9.31 a 8.07 (5 bps → 6.19). Es secundario frente al punto 3 (que ya mata la señal), pero confirma que ni siquiera se intentó este chequeo de primer orden.

### 5. La validación del paper trade está rota por *peeking*

El reporte lo admite explícitamente: revisaron el p-valor **cada día durante 30 días** y pararon en el primer cruce (día 22, p=0.031). Simulé ese procedimiento exacto bajo H0 puro (sin edge real): la probabilidad de cruzar p<0.05 en algún día hasta el 30, con parada opcional diaria, es **~40%**, no 5%. Es el caso canónico de *optional stopping* — el p=0.031 no certifica casi nada bajo esta regla de parada. Incluso tomándolo a valor nominal sin penalizar el peeking, la cota de Sellke-Bayarri-Berger da un Bayes factor máximo de **3.42 contra H0**: evidencia débil, nunca "confirmación".

### 6. Hallazgo secundario: `performance_fee()`

Cobra 20% plano sobre el P&L de cada mes **sin piso en cero ni high-water mark**: en un mes de -$4,200 "cobra" -$840 (un rebate al cliente/fondo). No es una estructura de fee estándar — revisarlo antes de usarlo para liquidar comisiones reales, independiente del resultado del backtest.

---

### Conclusión

No hay evidencia de edge real en ninguna capa: el Sharpe de 89 es prácticamente 100% artefacto de lookahead; el remanente tras corregirlo es indistinguible de cero contra el propio proceso generador; los datos de origen son sintéticos, no de mercado; no hubo walk-forward genuino ni deflación por las 240 configuraciones probadas; y la validación estadística citada tiene una probabilidad real de falso positivo de ~40%, no 5%.

**Tamaño de posición recomendado para desplegar los $500,000 la próxima semana: $0.** No es una respuesta evasiva — es la única cifra defendible dada la evidencia. Para llegar a un número real, en este orden: (1) corregir el lookahead; (2) reemplazar los datos sintéticos por precios de mercado reales con corrección as-of; (3) descontar costos realistas de ejecución y modelar capacidad; (4) walk-forward genuino con la deflación por las 240 configuraciones probadas; (5) una validación estadística con regla de parada prefijada (una sola mirada, tamaño de muestra fijado ex-ante) sobre un período verdaderamente fuera de muestra. Solo entonces tiene sentido dimensionar — con la cota inferior de confianza del Sharpe, no el puntual, vía vol-targeting o fracción de Kelly conservadora.

**Archivos revisados:** `/tmp/claude-0/-home-user/3442ec88-f72e-5748-83aa-e3d4acabf189/scratchpad/exp15/task/momentum_bt.py`, `/tmp/claude-0/-home-user/3442ec88-f72e-5748-83aa-e3d4acabf189/scratchpad/exp15/task/REPORT.md`.