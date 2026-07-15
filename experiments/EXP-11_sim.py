# EXP-11 — Cómputos del argumento (clase A: toda afirmación cuantitativa propia se calcula, no se opina)
# Caso: "Envía un recordatorio semanal a los usuarios inactivos; tras 3 recordatorios sin actividad,
#        desactiva la cuenta y notifica al admin. Agrega un endpoint para exportar los usuarios a CSV."
#
# Dimensiones ambiguas detectadas por el ejemplo caminado (ver EXP-11.md), con:
#  - número de lecturas plausibles
#  - costo relativo de rework si la lectura elegida resulta equivocada
#    (unidades relativas: 1 = cambiar una línea/config; 100 = daño difícil de revertir)

DIMS = {
    "A1 def. de 'inactivo' (login/actividad-clave/sesión)": (3, 8),
    "A2 ventana de inactividad (30d/desde-registro/config)": (3, 3),
    "A3 'cada semana': ancla global vs por-usuario":        (2, 1),
    "A4 actividad intermedia resetea el contador":          (2, 2),
    "A5 'desactiva': soft/bloqueo-admin/borrado":           (3, 40),
    "A6 'notifica al admin': por-usuario vs digest":        (2, 1),
    "A7 CSV: todos los campos (PII) vs subset":             (2, 50),
    "A8 auth del endpoint (omitida en el texto)":           (2, 100),
}

# ── CALC1: cuántos programas distintos caben en el párrafo ─────────────────
readings = 1
for n, _ in DIMS.values():
    readings *= n
print(f"CALC1  lecturas combinadas del párrafo = {readings} implementaciones distintas")

# ── CALC2: P(acertar la intención en TODAS las dimensiones) eligiendo en silencio ──
# modelo declarado: p=0.8 de acertar cada dimensión por contexto (generoso para 2-3 lecturas)
p = 0.8
k = len(DIMS)
print(f"CALC2  P(intención acertada en las {k} dimensiones) con p=0.8 c/u = {p**k:.3f}")

# ── CALC3: concentración del riesgo esperado (triage divergencia × irreversibilidad) ──
# modelo declarado: p_wrong=0.2 uniforme; el riesgo esperado por dimensión = 0.2 * costo
costs = sorted(((c, name) for name, (_, c) in DIMS.items()), reverse=True)
total = sum(c for c, _ in costs)
acum = 0
print("CALC3  riesgo esperado por dimensión (p_wrong=0.2 uniforme):")
for i, (c, name) in enumerate(costs, 1):
    acum += c
    print(f"       #{i} {name:55s} costo {c:3d}  acumulado {100*acum/total:5.1f}%")
top3 = sum(c for c, _ in costs[:3])
print(f"CALC3  las 3 dimensiones más caras concentran {100*top3/total:.1f}% del riesgo esperado"
      f" → 3 preguntas en un lote eliminan ~{100*top3/total:.0f}% del riesgo")

# ── CALC4: lectura minimax-regret vs máximo-verosímil (cuando no se puede preguntar) ──
# A5 'desactiva': lectura "bloqueo admin" P=0.6, costo si equivocada 40 (usuarios legítimos
# expulsados, churn); lectura "soft/reversible" P=0.4, costo si equivocada 5 (reactivar es 1 config).
pB, cB = 0.6, 40   # elegir la MÁS probable (bloqueo): pagas cB si era la otra (prob 0.4)
pS, cS = 0.4, 5    # elegir la MENOS probable (soft): pagas cS si era la otra (prob 0.6)
er_B = (1 - pB) * cB
er_S = (1 - pS) * cS
print(f"CALC4  costo esperado eligiendo la lectura más probable (bloqueo) = {er_B:.1f}")
print(f"       costo esperado eligiendo la más barata de corregir (soft)  = {er_S:.1f}")
print(f"       la lectura MENOS probable domina por {er_B/er_S:.1f}x → minimax-regret ≠ máx-verosimilitud")

# ── CALC5: preguntar incremental vs en lote (round-trips esperados) ────────
# modelo: cada ambigüedad descubierta al tocarla dispara su propia pregunta si se pregunta
# incrementalmente; en lote, el ejemplo caminado las descubre todas antes de empezar.
n_ask = 3  # solo las del triage
print(f"CALC5  round-trips: incremental = hasta {n_ask} bloqueos secuenciales (latencia sumada);"
      f" lote tras ejemplo caminado = 1")
