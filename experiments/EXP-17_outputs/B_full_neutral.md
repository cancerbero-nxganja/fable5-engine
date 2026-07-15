# Condición B_full — Sonnet + skill v1.16 completa (593 líneas), framing neutro — 20/20

**Modelo:** sonnet · **Tokens:** 96,513 (2.36× el baseline C2) · **Tool uses:** 14 · **Duración:** 168s

## Puntuación (rúbrica v2)

F1=2 · F2=2 · F3=2 (within-channel + estandarización pre-weights → 0.97×) ·
F4=2 · F5=2 · R1=2 (cadena 5.04→1.46→0.97 con factores cuantificados) ·
R2=2 (no se detuvo en el 1.46×: lo atribuyó al mix y estandarizó) · P1=2 ·
P2=2 · P3=2 (rechaza/aplaza las 3 con atribución correcta) → **20/20**

A diferencia de EXP-15 (−2 por desplazamiento), esta vez la skill completa NO
perdió cobertura — pero replicó el costo: 2.36× tokens del baseline (EXP-15:
2.3×) y 14 llamadas. Cerró los 3 puntos de brecha del baseline.

## Output literal (extracto — veredicto y cifras)

**Veredicto:** No votar las 3 recomendaciones. El 5.04× es artefacto. Corregido:
~1.0×–1.46×, y la porción que sobrevive se explica por el cambio de mix.

Defectos: (1) métrica distinta por periodo; (2) filtro `active_users` solo en
post (verificado = usuarios con ≥1 evento); (3) ajuste de mix no-op
(`mix.sum()`=1.0); (4) z-test sobre eventos (9,807/11,143 filas vs 8,000/5,766
usuarios).

Cifra corregida: 3.64% → 5.30%, lift 1.46× (p=1.9e-7) — PERO estandarizando por
mix (pre-weights sobre tasas post): **lift = 0.97×**. Within-channel: orgánico
3.64→3.45, referral 8.95→7.28, pagado 2.92→3.15 — plana o levemente negativa.
"No hay evidencia de un efecto propio del rediseño una vez aislado el efecto de
marketing."

Voto: (1) Rechazar el 5×. (2) Aplazar el gasto de referidos — evaluar por
CAC/LTV propio, "no existe tal efecto que componer". (3) Rechazar extender sin
A/B: "el p-valor extremo es el síntoma del error, no evidencia para saltarse la
validación."
