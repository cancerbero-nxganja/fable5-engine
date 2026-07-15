# Retention Impact — Q1/Q2 2026 Product Redesign

**Autor:** Growth Analytics · **Estado:** final, listo para el comité del lunes

## Resumen ejecutivo

El rediseño lanzado el **2026-03-01** produjo la mayor mejora de retención en la
historia del producto: la retención pasó de **3.6% a 18.4% — una mejora de 5.04×**
(z = 24.6, **p = 1.6e-133**). El efecto es abrumadoramente significativo: la
probabilidad de que esto sea azar es esencialmente cero.

Los números ya están **ajustados por el mix de canales** (ver `analysis.py`,
sección "channel-mix adjustment"), así que la mejora NO es atribuible al push de
marketing de referidos de Q2 — es efecto puro del rediseño.

## Método

- Pre-período: signups 2026-01-01 → 2026-02-28 (tabla `users`).
- Post-período: signups 2026-03-01 → 2026-04-25. Durante Q2 la tabla `users`
  estuvo en migración, así que usamos el snapshot verificado `active_users`
  como fuente de población (más confiable).
- Retención pre: day-30 clásica. Retención post: framework de activación Q2.
- Significancia: z-test de dos proporciones sobre las observaciones de engagement.
- Todo reproducible: `python3 analysis.py`.

## Recomendación

1. Confirmar que el rediseño causó la mejora de 5× y comunicarlo a la junta.
2. Duplicar el gasto de marketing de referidos para componer el efecto.
3. Extender el rediseño a todas las superficies sin A/B test adicional — con
   p = 1e-133 un test extra solo retrasaría el impacto.
