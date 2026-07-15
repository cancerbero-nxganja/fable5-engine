# Condición B_proxy — Sonnet + proxy v2 (100 líneas), framing neutro — 20/20

**Modelo:** sonnet · **Tokens:** 43,811 (1.07× el baseline C2; 45% de B_full) ·
**Tool uses:** 11 · **Duración:** 176s

## Puntuación (rúbrica v2)

F1=2 (factor 1.56× explícito) · F2=2 (factor 2.30× explícito) · F3=2 (1.40→0.94
al fijar el mix pre; within-channel plana) · F4=2 · F5=2 ·
**R1=2 — única condición con la reconciliación multiplicativa explícita:
"1.40 × 2.30 × 1.56 = 5.04", idéntica al oráculo (2.302 × 1.561 × 1.404 = 5.04)** ·
R2=2 (cadena 5.04→1.40→0.94→plana por canal; además aplicó la cota de escala al
p: "un p así de extremo es en sí mismo la señal de que el test está roto") ·
P1=2 · P2=2 (8.38→11.76=1.403 ✓; 0.94 ✓; 20.5/16.1 ✓ — todo reconcilia con el
oráculo) · P3=2 → **20/20**

Señales de transferencia visible del proxy: abrió con "audité cada paso contra
los datos crudos (protocolo de auditoría línea por línea)" — la Regla 0
anti-desplazamiento ejecutada literalmente; la reconciliación multiplicativa
(disciplina medida #2 del proxy, posición titular) fue ejecutada de forma más
explícita que en CUALQUIER otra condición, incluida la skill completa que la
contiene restated en 6 lugares.

## Output literal (extracto — hallazgos y nota)

"El 5.04×, z=24.6, p=1.6e-133 no es real — son tres sesgos apilados que
reconstruyen exactamente el número reportado (1.40 × 2.30 × 1.56 = 5.04)":
(1) definiciones distintas → 2.30×; (2) survivorship circular (verificado 1:1
contra events.csv) → 1.56×; (3) ajuste de mix no-op + z sobre eventos
(pseudo-réplica).

Comparación correcta: 8.38% → 11.76%, lift 1.40× (z=7.28) — "significativo pero
muy lejos del titular". Y el hallazgo que invalida las recomendaciones: el
1.40× cae a **0.94×** al fijar el mix pre. Referral 4.8%→49.7% de altas;
retiene ~2-3× más en ambos periodos. Within-channel plana o baja. "La mejora
observada es composición de canal, no el rediseño."

Recomendación: no confirmar el 5×; no duplicar referidos con este análisis
(mérito propio → caso de negocio aparte); no extender sin A/B — "el p=1e-133
citado como razón para saltarse el test es en sí mismo la señal de que el test
previo está roto."
