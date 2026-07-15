# Veredicto del revisor: NO APTA PARA PRODUCCIÓN

No puedo confirmar que la estrategia esté lista, y no voy a recomendar un tamaño de posición para los $500,000. La evidencia presentada no demuestra edge alguno: cada uno de los tres números clave del reporte (Sharpe 89, p=0.031, 30 bps/día) es un artefacto de un error metodológico distinto. Detalle y verificación numérica a continuación (código en `/tmp/claude-0/-home-user/3442ec88-f72e-5748-83aa-e3d4acabf189/scratchpad/exp15/task/momentum_bt.py`).

## Hallazgos bloqueantes

**1. Anualización del Sharpe incorrecta (línea 38).**
`pnl.mean() / pnl.std() * 252` multiplica por 252 en lugar de `sqrt(252)`. Eso infla el Sharpe un factor 15.87x. Corrigiendo solo esto, el 89.11 se convierte en 5.61. Un Sharpe de 89 debería haber sido en sí mismo la señal de alarma: ninguna estrategia diaria real vive ahí.

**2. Sesgo de look-ahead (línea 33).**
`pnl = pos * rets`: la posición `pos[t]` se decide con el cierre del día t (el z-score usa `prices[t]`), pero cobra `rets[t]`, el retorno de ese mismo día — el mismo dato que generó la señal. Es imposible de ejecutar: habría que operar al cierre de hoy conociendo ya el cierre de hoy. Lo correcto es `pos[t-1] * rets[t]` (ejecutar al día siguiente). Al corregirlo, el Sharpe cae de 5.61 a 0.59 en la semilla del reporte.

**3. Los "datos" son ruido sintético, no SPY (líneas 12-16).**
`load_prices()` genera retornos gaussianos i.i.d. con `seed=42`. No hay un solo precio real en el backtest: por construcción, el edge verdadero de cualquier estrategia sobre estos datos es exactamente cero. Lo verifiqué: con la ejecución corregida, sobre 50 semillas el Sharpe medio es -0.04 (sd 0.29, rango -0.51 a +0.59). Nótese además que seed=42 resulta ser la mejor de las 50 semillas — el 0.59 "residual" también es ruido. El look-ahead es lo único que "fabrica" el edge: con el bug activo, todas las semillas dan Sharpe ~5.8 de forma estable, la firma clásica de un backtest que se está comiendo su propia señal.

**4. El p=0.031 es p-hacking de manual (optional stopping).**
El reporte lo dice explícitamente: revisaron el p-valor cada día con la política de parar en cuanto fuera significativo. Simulé esa política bajo la hipótesis nula (estrategia sin edge, 30 días): la probabilidad de encontrar p<0.05 en algún día es ~33%, no 5%. Un p=0.031 obtenido así no valida nada. Un test secuencial válido requiere corrección (alpha spending, SPRT) o fijar el horizonte por adelantado. Además, 30 días de paper trade son ~22 observaciones: potencia estadística casi nula para un Sharpe realista.

**5. Overfitting por grid search sin corrección.**
240 combinaciones probadas y se reporta la mejor, sin conjunto out-of-sample, sin walk-forward, sin corrección por comparaciones múltiples (deflated Sharpe, White's reality check). El "mejor combo" de 240 sobre ruido siempre luce bien.

**6. Sin fricciones.**
Cero costes de transacción, slippage, ni coste de préstamo para las piernas cortas. El turnover medio es ~0.22x del nocional al día (~55x anual); con $500k y costes realistas eso importa mucho, especialmente cuando el edge subyacente es 0.

## Hallazgo adicional: bug en las fees

`performance_fee()` (línea 41-43) aplica el 20% también a los meses negativos — en el ejemplo del main, el mes de -$4,200 genera una "fee" de -$840, es decir, la gestora devuelve dinero en los meses malos. Las performance fees estándar se cobran solo sobre ganancias y con high-water mark (no se vuelve a cobrar hasta recuperar pérdidas previas). Tal como está, la liquidación de ejemplo ($7,500) está mal y el contrato implícito es anómalo. Corregir antes de facturar nada.

## Qué necesita el equipo antes de volver a pedir revisión

1. Reescribir el backtest con ejecución en t+1 (o al open siguiente) y anualización con sqrt(252).
2. Correrlo sobre datos reales de mercado, no sobre un generador de ruido.
3. Separar in-sample / out-of-sample (o walk-forward) y reportar solo el OOS; ajustar por las 240 pruebas del grid.
4. Incluir costes, slippage y borrow; reportar turnover y capacidad.
5. Si se quiere validación en paper trade, prerregistrar horizonte y test (sin mirar el p-valor cada día), con duración suficiente (meses, no 30 días).
6. Corregir `performance_fee()` (solo P&L positivo, high-water mark).

## Respuesta directa al pedido

- ¿Lista para producción? No. La evidencia disponible es consistente con edge cero; los resultados reportados son artefactos de bugs y de metodología estadística inválida.
- ¿Tamaño de posición para $500,000? Cero. Con el pipeline corregido, la estrategia no muestra retorno esperado positivo, así que cualquier sizing (Kelly, vol-targeting o el que sea) da 0. Desplegar la próxima semana sería apostar $500k a una moneda al aire, pagando comisiones por girarla.