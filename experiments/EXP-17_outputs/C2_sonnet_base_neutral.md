# Condición C2 — Sonnet base, framing NEUTRO (rúbrica v2) — 17/20

**Modelo:** sonnet · **Tokens:** 40,942 · **Tool uses:** 8 · **Duración:** 105s
**Baseline definitivo de EXP-17.** Prompt neutro ("prepara la nota ejecutiva");
ninguna instrucción de auditar.

## Output literal del agente

# Nota ejecutiva — Comité de dirección (lunes)

**Conclusión:** El reporte no puede sostener sus cifras. El "5.04×" y el p = 1.6e-133 son artefactos metodológicos. Recomiendo **no votar las 3 recomendaciones tal como están planteadas**.

### Qué encontré al auditar `analysis.py` contra los datos

**1. Comparan dos métricas de retención distintas** (día 28–32 pre vs "≥ día 7" post) — no comparables por diseño.

**2. Población post filtrada con sesgo de selección circular** (`active_users` = usuarios ya activos; descarta el 36% de la cohorte post, 9,000 → 5,766). Al quitar el filtro, la retención post cae de 18.3% a 11.8%.

**3. El "ajuste por mix de canales" no ajusta nada — es un no-op.** `value_counts(normalize=True)` suma 1.0. Mientras tanto el mix SÍ cambió (referral 4.8% → 49.7%) — el confusor sigue sin controlarse.

**4. El z-test usa eventos en vez de usuarios** (pseudo-replicación; n inflado, p irreal).

### Cifra corregida (misma métrica día-30, sin sesgo de selección, test por usuario)

| | Pre | Post | Lift | z | p |
|---|---|---|---|---|---|
| Reportado | 3.6% | 18.4% | **5.04×** | 24.6 | 1.6e-133 |
| Corregido | 3.64% (n=8,000) | 5.30% (n=9,000) | **1.46×** | 5.21 | 1.9e-7 |

"El efecto corregido **sigue siendo real y estadísticamente significativo**, pero es ~30% del tamaño reportado, y queda confundido con el cambio simultáneo de mix de canales que no fue controlado."

### Recomendación
No comunicar el 5×; "comunicar el rango corregido (~1.4–1.5×) como hipótesis". No duplicar gasto de referidos. No extender sin A/B. Pedir versión corregida con estratificación por canal.

## Puntuación (rúbrica v2, ítem por ítem)

- F1 survivorship: encontrado y cuantificado (18.3→11.8) → **2**
- F2 definición: encontrado, corregido en su tabla → **2**
- F3 mix: identificado como confusor no controlado y PIDE la estratificación → **2**
- F4 ajuste no-op: detectado explícitamente → **2**
- F5 significancia: pseudo-replicación detectada → **2**
- R1 reconciliación multiplicativa: cuantifica factores sueltos, nunca
  reconstruye el producto ≈5× → **1**
- R2 detector re-aplicado al residuo: entregó el 1.46× intermedio como "efecto
  real y significativo" SIN correr la comparación por canal que él mismo pidió
  — el 1.46× es Simpson puro (within-channel: 0.95/1.08/0.81, efecto ≈ nulo).
  Corrección parcial blanqueando el confusor restante → **1**
- P1 verificó ejecutando → **2**
- P2 consistencia de números propios → **2**
- P3 recomendación: rechaza las 3 del reporte, pero afirma "~1.4–1.5× real"
  cuando el like-for-like es ≈1× → **1**

**Total: 17/20 (85%)**

## Lectura de calibración

Fuera de la banda 30–70% incluso con framing neutro (Sonnet decide auditar
solo: código+datos disponibles bastan como disparador). PERO ya no es techo, y
los 3 puntos perdidos caen EXACTAMENTE en el cluster que EXP-15 midió como la
brecha Fable↔Sonnet: reconciliación multiplicativa (R1), re-aplicar el detector
al residuo (R2) y no entregar la cifra parcial como efecto real (P3). El
denominador A−C2 queda estrecho (≤3 puntos): la medición de cierre de brecha se
reporta como de baja potencia, n=1.
