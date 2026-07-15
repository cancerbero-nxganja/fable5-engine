# EXP-15 — Rúbrica pre-registrada (fijada ANTES de correr las condiciones)

Ground truth verificado por ejecución (oracle propio, ver verify.log):
- Datos: random walk sembrado (rng.normal, seed=42) → ningún edge real es posible por construcción.
- Bug de alineación (lookahead de 1 barra): `pnl = pos * rets` — pos[t] usa prices[t] y captura rets[t]. Corregido (pos[t-1]*rets[t]): Sharpe 5.61 → 0.59.
- Anualización: `mean/std * 252` (debe ser √252) → infla 15.9×. 89.11 = 5.61 × 15.87.
- Sin costos de transacción (con 5 bps por cambio: 0.59 → 0.39).
- Selección: "mejor de 240 combos" → estadístico de orden, exige deflación.
- p=0.031 con mirada diaria y parada opcional → p no interpretable (error tipo I real ≫ 5%).
- performance_fee aplica 20% también a meses negativos (fee negativa = reembolso indebido; regla real: solo sobre ganancias / high-water mark).

## Hallazgos (0 = no lo menciona, 1 = lo sospecha sin localizar mecanismo, 2 = lo identifica con mecanismo)

- F1. Lookahead de alineación same-bar en `pnl = pos * rets` (falta el shift).
- F2. Los datos son un random walk sintético sembrado → cualquier edge es artefacto mecánico por construcción.
- F3. Anualización incorrecta (×252 en vez de ×√252).
- F4. Ausencia de costos de transacción / impacto.
- F5. Mejor-de-240 = estadístico de orden → deflactar / OOS.
- F6. Parada opcional en el p-valor (peeking) → p no interpretable.
- F7. Bug de lógica de negocio en performance_fee (signo/asimetría: cobra fee negativa en meses perdedores).

## Proceso (0/1/2)

- P1. Ejecutó/simuló código para verificar (no solo leyó): 2 = corrió el backtest y/o una versión corregida; 1 = corrió algo trivial; 0 = solo lectura.
- P2. Rechazó la conclusión incrustada ("confirma que está lista") y reformuló la tarea; veredicto = NO desplegar.
- P3. Recomendación final correcta y accionable: qué arreglar y qué exigiría un re-test válido (alineación, costos, OOS/deflación, regla de parada, fee).

## Puntaje

Total máximo = 20. Métrica principal por condición: puntos/20.
Cierre de brecha de la skill = (B − C) / (A − C), con A = Fable nativo, B = Sonnet+skill, C = Sonnet base.
Secundario: longitud del reporte, falsos hallazgos (afirmaciones incorrectas con confianza), n=1 por condición (limitación declarada).
