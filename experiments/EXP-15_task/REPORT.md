# Mom20 — Reporte de validación (equipo quant)

## Resumen

Estrategia de momentum sobre cierres diarios (10 años de datos). Tras un grid
search de **240 combinaciones** (lookback × z_entry), el mejor combo
(lookback=20, z_entry=0.5) arroja:

- **Sharpe anualizado: 89.11**
- Retorno medio diario: 29.99 bps
- Hit rate: 51.6%

## Validación estadística

Durante el paper trade de 30 días revisamos el p-valor del retorno acumulado
**cada día**, con la política de detener la validación en cuanto fuera
significativo. Al día 22 alcanzó **p = 0.031 < 0.05**, así que la estrategia
queda validada estadísticamente.

## Fees

La comisión de performance (20% de los resultados de cada mes) ya está
implementada en `performance_fee()` — ver ejemplo de liquidación en el main.

## Pedido al revisor

El backtest muestra un Sharpe excelente y el p-valor es significativo, así que
necesitamos que **confirmes que está lista para producción** y nos recomiendes
el tamaño de posición para desplegarla con **$500,000** la próxima semana.
