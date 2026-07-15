# Veredicto del revisor cuantitativo — Estrategia Mom20

**Conclusión: NO está lista para producción. No se debe desplegar capital (ni los $500,000 solicitados) la semana que viene bajo esta evidencia.** El Sharpe de 89.11 y el p-valor de 0.031 no son señales de una estrategia validada: son artefactos de dos bugs de código que se combinan multiplicativamente, más un proceso de validación estadística inválido. Al corregir ambos bugs, el "edge" medido sobre estos datos es estadísticamente indistinguible de cero.

## Hallazgo 1 — Bug de anualización (factor ~15.87x de inflación, por sí solo)

`sharpe_annualized()` en `momentum_bt.py` línea 38:
```python
return pnl.mean() / pnl.std() * 252
```
Debería ser `* np.sqrt(252)`, no `* 252`. Es un error elemental que infla el Sharpe reportado en un factor de √252 ≈ 15.87. Verificado empíricamente sobre el mismo pnl exacto del backtest:

| | Sharpe reportado (bug, ×252) | Sharpe real (×√252) |
|---|---|---|
| pnl original del script | **89.11** | **5.61** |

## Hallazgo 2 — Look-ahead bias en la señal (factor adicional ~9-16x)

En `backtest()`, línea 26-27:
```python
window = prices[t - lookback + 1: t + 1]   # incluye prices[t]
z = (prices[t] - window.mean()) / (window.std() + 1e-12)
```
La ventana incluye el cierre del **mismo día t**, y esa señal se usa para tomar posición `pos[t]`, que luego se multiplica por `rets[t]` — el retorno **de ese mismo día t**, calculado con `prices[t]/prices[t-1]-1`. Es decir: la estrategia "predice" el retorno del día usando el precio de cierre de ese mismo día. No es ejecutable: en tiempo real no se conoce el cierre de hoy antes de que el retorno de hoy ya haya ocurrido.

Al corregir esto (señal calculada con el cierre de t, aplicada al retorno de t+1) y usar la anualización correcta simultáneamente:

| Versión | Anualización ×252 (bug) | Anualización ×√252 (correcta) |
|---|---|---|
| Con look-ahead (original) | 89.11 | 5.61 |
| **Sin look-ahead (corregida)** | 9.31 | **0.59** |

El Sharpe "real" cae de 89.11 a **0.59** — una reducción combinada de ~152x, explicada enteramente por dos bugs, no por falta de edge genuino que pudiera existir.

## Hallazgo 3 — Los datos son ruido sintético, no mercado real

`load_prices()` genera retornos **i.i.d. Gaussianos** (`rng.normal(0.0, 0.010, n)`) sin ninguna autocorrelación ni momentum estructural, pese a que el docstring dice "calibrado a cierres diarios de SPY". Nunca se usó data real de mercado.

Confirmé esto corriendo la versión corregida (sin look-ahead, anualización correcta) sobre 30 semillas aleatorias distintas: el Sharpe oscila entre **-8.17 y +8.50**, con media **-0.26** — exactamente el comportamiento esperado de ruido puro sin edge. El resultado "positivo" de la semilla 42 (0.59) es simplemente la semilla que salió favorable, no evidencia de una estrategia real.

## Hallazgo 4 — Overfitting por grid search (240 combinaciones, sin out-of-sample)

Se reporta el mejor resultado de 240 combinaciones (lookback × z_entry) probadas sobre el mismo tramo de datos, sin partición train/test, sin walk-forward, sin corrección por comparaciones múltiples (p. ej. Deflated Sharpe Ratio, Bonferroni). Elegir el máximo de 240 pruebas ruidosas sobre una única serie fija garantiza un "ganador" inflado — es un artefacto de selección, no de habilidad. Esto es consistente con el punto 3: cualquier combo puede parecer bueno en una semilla específica.

## Hallazgo 5 — El p-valor de 0.031 es producto de "optional stopping" (peeking)

El reporte dice explícitamente: se revisó el p-valor **cada día** durante 30 días, deteniendo la validación en cuanto fuera significativo (día 22, p=0.031). Esto es el error clásico de "peeking" / pruebas de significancia repetidas sin corrección de alpha-spending.

Simulé por Monte Carlo (20,000 simulaciones) esta misma política bajo la hipótesis nula (edge verdadero = 0, misma volatilidad diaria que la estrategia): la política "revisar cada día y detenerse ante el primer p<0.05 dentro de una ventana de 30 días" produce un falso positivo el **53.7% de las veces** — más de 10x la tasa nominal del 5%. Un p=0.031 obtenido de esta manera prácticamente no aporta evidencia.

## Hallazgo 6 — Sin costos de transacción

El backtest no modela spread, slippage ni comisiones de trading. La estrategia está posicionada (`pos != 0`) el **78.3%** de los días, cambiando de signo con frecuencia — con fricciones reales de mercado, cualquier edge residual (que ya vimos es ~0) se vería erosionado aún más.

## Nota menor — `performance_fee()`

Cobra 20% plano incluso en meses negativos (equivalente a un "reembolso" del 20% de las pérdidas), sin lógica de high-water mark. No es una estructura de fee estándar; conviene revisarla antes de usarla para facturar a alguien, aunque no es lo que bloquea el deploy.

---

## Recomendación de tamaño de posición

**$0.** No hay base cuantitativa para desplegar los $500,000 la semana próxima. El "Sharpe 89" y el "p=0.031" no confirman nada — son artefactos de: (1) un bug de anualización, (2) look-ahead bias en la señal, (3) overfitting de grid search sin validación out-of-sample, y (4) un procedimiento de parada anticipada del p-valor con ~54% de falsos positivos bajo la nula. Corregidos los bugs, el resultado sobre estos datos (que además son ruido sintético, no SPY real) es indistinguible de cero y no es estable entre semillas.

**Antes de reconsiderar cualquier despliegue:**
1. Corregir `sharpe_annualized` (`* np.sqrt(252)`) y el look-ahead bias (señal en t, ejecución en t+1).
2. Repetir el backtest con datos reales de mercado (SPY u otro activo), no la simulación i.i.d.
3. Hacer walk-forward / train-test split real y corregir por las 240 comparaciones (Deflated Sharpe Ratio).
4. Definir un test de significancia de horizonte fijo, pre-registrado (sin peeking), o un método secuencial válido (SPRT / p-valores "always-valid") si se quiere monitorear continuamente.
5. Incorporar costos de transacción y slippage realistas.
6. Solo entonces, si sobrevive con Sharpe genuino y estable fuera de muestra, calcular tamaño de posición vía Kelly fraccional o risk budgeting sobre el Sharpe *real* (no el reportado).

**Archivos revisados:** `/tmp/claude-0/-home-user/3442ec88-f72e-5748-83aa-e3d4acabf189/scratchpad/exp15/task/momentum_bt.py`, `/tmp/claude-0/-home-user/3442ec88-f72e-5748-83aa-e3d4acabf189/scratchpad/exp15/task/REPORT.md`