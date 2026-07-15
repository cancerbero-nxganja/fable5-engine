# EXP-17 — Rúbrica PRE-REGISTRADA (escrita antes de lanzar ninguna condición)

Escala por ítem: 0 = no lo encontró/no lo hizo · 1 = parcial (lo menciona sin
cuantificar o sin usarlo en la conclusión) · 2 = completo. Máx 20.

Ground truth ejecutable: `verify_oracle.txt` — efecto real del rediseño = nulo
por construcción; 5.04 = 2.30 (definición) × 1.56 (survivorship) × 1.40 (mix).

## Defectos plantados (hallazgos)

- **F1 — Survivorship en el denominador post**: el post usa `active_users`
  (solo usuarios con ≥1 evento) como población; el pre usa la tabla completa.
  Factor 1.56×. (2 = lo nombra Y cuantifica o corrige su efecto.)
- **F2 — Cambio de definición**: pre = evento en día 28–32; post = cualquier
  evento ≥ día 7 (dos funciones distintas: `d30_retention` vs `retention_rate`).
  Factor 2.30×. (2 = lo nombra Y cuantifica o corrige.)
- **F3 — Confusión por mix de canales**: el mix pasa de 5% → 50% referral, y
  referral retiene 2.5× más que organic/paid; sin comparación within-channel el
  pooled compara poblaciones distintas. Factor ~1.40×. (2 = corre o pide la
  comparación por canal.)
- **F4 — El ajuste de mix es un no-op (corrección falsa)**: `pre_ret * mix.sum()`
  multiplica por 1.0 — el reporte declara "ya ajustado por mix" y el código no
  ajusta nada. (2 = detecta explícitamente que la corrección declarada no hace
  nada; 1 = desconfía del ajuste sin verificar el código.)
- **F5 — Pseudo-replicación en la significancia**: el z-test corre sobre
  observaciones-evento (n≈21k eventos), no sobre usuarios (la unidad de
  aleatorización/análisis), y además compara definiciones distintas en cada
  brazo. El p no es interpretable. (2 = identifica la unidad equivocada o que
  el test compara definiciones distintas.)

## Disciplinas de proceso (la brecha medida en EXP-15)

- **R1 — Reconciliación multiplicativa**: descompone el 5.04× en factores
  medidos cuyo producto reconstruye ≈5× (tolerancia ±15%). (1 = descompone sin
  reconciliar el producto.)
- **R2 — Detector re-aplicado al residuo**: tras corregir el primer defecto, no
  entrega la cifra parcial como "corregida": re-interroga el residuo hasta que
  el lift restante quede explicado (~1.0×) o justificado. Evidencia: cadena de
  cifras intermedias re-cuestionadas. (1 = corrige ≥2 defectos pero entrega una
  cifra intermedia como final sin re-interrogarla.)
- **P1 — Verificó ejecutando**: corrió `analysis.py` y/o recomputó sobre el dato
  completo con código propio (no juzgó solo leyendo).
- **P2 — Consistencia de los números propios**: 2 = cero cifras auto-derivadas
  entregadas con confianza que sean inconsistentes en escala/definición entre
  sí; 1 = una; 0 = dos o más.
- **P3 — Recomendación final correcta**: no validar el 5×; el efecto like-for-like
  es ≈1× (sin evidencia de mejora); no duplicar gasto ni saltarse el A/B con
  base en este análisis. (2 = las tres cosas; 1 = rechaza el 5× pero acepta
  alguna recomendación derivada.)

## Condiciones (mismo prompt literal; B_* anteponen la adopción de su skill)

- **C — Sonnet base** (calibración: debe puntuar 30–70% ANTES de correr el resto)
- **A — Fable 5 nativo** (referencia superior)
- **B_full — Sonnet + skill v1.16 completa** (594 líneas)
- **B_proxy — Sonnet + proxy v2 podado** (la apuesta de EXP-17)

Métrica principal: cierre de brecha (B−C)/(A−C) por condición B, computable solo
si C < A. Métricas secundarias: tokens, llamadas a herramientas, cifras
inconsistentes entregadas.
