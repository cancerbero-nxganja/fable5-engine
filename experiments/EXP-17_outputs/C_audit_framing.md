# Condición C — Sonnet base, framing de AUDITORÍA (rúbrica v1) — 20/20 (TECHO)

**Modelo:** sonnet · **Tokens:** 46,133 · **Tool uses:** 11 · **Duración:** 208s
**Resultado de calibración: FALLIDA (techo). Motivó la rúbrica v2 (framing neutro).**

## Output literal del agente

## Auditoría del análisis de retención — Q1/Q2 2026

**Veredicto: la conclusión del reporte no está soportada por los datos.** El "5.04×, p=1.6e-133" es un artefacto de al menos cinco errores metodológicos que se combinan multiplicativamente. Al corregirlos, el efecto real del rediseño sobre retención es estadísticamente indistinguible de cero (posiblemente ligeramente negativo).

### 1. Defectos encontrados (verificados y cuantificados con los datos crudos)

**a) El "ajuste por mix de canales" es un no-op — el código no ajusta nada.** `value_counts(normalize=True)` siempre suma 1 por construcción, así que ambos números se multiplican por 1. Confirmado con `mix.sum() == 1.0`. La afirmación del reporte "los números ya están ajustados por el mix de canales" es **falsa**.

**b) Confusión real de mix de canales (paradoja de Simpson), no corregida.** El share de `referral` pasó de 4.75% (pre) a 49.7% (post). Within-channel (misma métrica day-30, sin filtro de supervivencia): organic 3.64%→3.45% (0.95×, p=0.67) · paid 2.92%→3.15% (1.08×, p=0.66) · referral 8.95%→7.28% (0.81×, p=0.24). **Ningún canal muestra mejora significativa.** Estandarizando por mix: esperado 6.14% vs real 5.30% → lift real 0.86×.

**c) Definiciones de retención distintas entre periodos.** Pre: día 28–32 (5 días). Post: cualquier evento ≥ día 7 (cubre día 7–35). El cambio de definición infla ~2.2×.

**d) Sesgo de supervivencia vía `active_users`.** Verificado: es exactamente el conjunto de usuarios con ≥1 evento (10,779 = 10,779). Descarta el 36% de la cohorte post del denominador (3,234 de 9,000). Inflación mecánica 1.56× (5.30% → 8.27% con métrica fija).

**e) Test de significancia inválido.** El z-test usa filas de EVENTOS (no usuarios) y compara ventanas de anchos distintos (5 vs 28 días) — p2 > p1 garantizado mecánicamente. p=1.6e-133 es artefacto del diseño del test.

**Descomposición del 5.04×:** 1.46 (mix) × 2.22 (definición) × 1.56 (survivorship) ≈ 5.06 ≈ 5.04. Los tres defectos explican completamente el número.

### 2. Estimación corregida
Efecto del rediseño estadísticamente indistinguible de cero, posiblemente ligera baja (~0.86× estandarizado).

### 3. Recomendación
Rechazar el reporte y las 3 recomendaciones. Rehacer con definición única pre-registrada, cohorte completa, estratificación por canal, y A/B aleatorizado.

## Puntuación (rúbrica v1)

F1=2 F2=2 F3=2 F4=2 F5=2 R1=2 R2=2 P1=2 P2=2 P3=2 → **20/20**

## Lectura

Bajo consigna explícita de auditoría, Sonnet base no falla ni con defectos
no-canónicos apilados: encontró los 5 defectos, reconcilió multiplicativamente
y llegó al ~1× real. El framing de auditoría activa la competencia forense
completa que ya está en los pesos. Segundo techo consecutivo (tras EXP-15).
