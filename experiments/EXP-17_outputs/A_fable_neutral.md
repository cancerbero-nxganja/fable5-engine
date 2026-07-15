# Condición A — Fable 5 nativo, framing neutro — 20/20

**Modelo:** claude-fable-5 · **Tokens:** 28,488 · **Tool uses:** 6 · **Duración:** 105s

## Puntuación (rúbrica v2)

F1=2 (36% excluido cuantificado) · F2=2 (con métrica laxa el pre ya daba 8.4%) ·
F3=2 (within-channel: 3.6→3.5 / 2.9→3.2 / 9.0→7.3) · F4=2 (no-op, con líneas de
código citadas) · F5=2 · R1=2 (cadena 18.4→5.3→3.5 vs pre 3.6 reconstruye el 5×) ·
R2=2 (nunca entregó cifra intermedia como final) · P1=2 · P2=2 (todas las cifras
consistentes con el oráculo: 8.4% pre-laxa, 3.5% estandarizada, referral ~2×) ·
P3=2 (rechaza #1 y #3; #2 "aplazar con caso de negocio propio", nota la caída
9.0→7.3 al escalar 12× como dilución de calidad) → **20/20**

Perfil de economía replicado de EXP-15: la menor huella de todas las condiciones
(28k tokens, 6 llamadas) con score perfecto. Observación diferencial extra: la
retención de referral CAYÓ al escalar el canal 12× — dilución de calidad que
ninguna otra condición señaló.

## Output literal

# Nota ejecutiva — Impacto del rediseño Q1/Q2 en retención

**Para:** Comité de dirección · **De:** Equipo Growth · **Fecha:** 2026-07-15

## Recomendación al comité: NO aprobar las 3 recomendaciones tal como están

Al preparar esta nota re-ejecutamos `analysis.py` sobre los datos fuente. Los números del reporte se reproducen, pero **la mejora de 5× no es real: es un artefacto de tres errores metodológicos**. Corregidos, el rediseño no muestra efecto medible sobre la retención.

| | Reporte | Análisis corregido |
|---|---|---|
| Retención pre | 3.6% | 3.6% (day-30) |
| Retención post | 18.4% | **5.3%** con la misma métrica y población; **3.5%** ajustada por mix |
| Lift | 5.04× (p≈1e-133) | **~1.0× — sin cambio significativo en ningún canal** (p entre 0.24 y 0.67) |

## Los tres errores

1. **Métricas distintas en cada período.** Pre: day-30 clásica. Post: "algún evento después de la semana 1". Con la métrica laxa, el período *pre* ya daba 8.4%, no 3.6%.
2. **Sesgo de supervivencia en la población post** (snapshot `active_users`: 5,766 de 9,000 signups; el 36% excluido son mayoritariamente usuarios que no retuvieron).
3. **El "ajuste por mix de canales" no ajusta nada** (`mix.sum()` = 1.0 por construcción; Simpson sin corregir). Referral 4.8%→49.7% de signups y retiene ~2× más. Por canal: organic 3.6%→3.5%, paid 2.9%→3.2%, referral 9.0%→7.3% — ninguno significativo. La p=1e-133 sale de un z-test sobre *eventos*.

## Voto sugerido

1. "Confirmar el 5×" — **Rechazar.** Efecto atribuible ~0.
2. "Duplicar gasto en referidos" — **Aplazar**: la retención de referral *cayó* de 9.0% a 7.3% al escalar 12× (dilución de calidad); merece caso de negocio propio con CAC/LTV.
3. "Extender sin A/B" — **Rechazar.** El p inválido hace el A/B *más* necesario.

**Nota fuera de página:** los problemas están en `analysis.py` líneas 23–32 (métricas), 20 (filtro), 40–42 (no-op), 45–54 (z-test sobre eventos). Cualquiera puede reproducir las cifras corregidas en cinco minutos.
