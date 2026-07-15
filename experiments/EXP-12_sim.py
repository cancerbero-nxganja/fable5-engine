"""
EXP-12 — Modelos calculados para "uso óptimo de herramientas".

Cuatro cálculos (clase A: consecuencias de modelos declarados, no opiniones):

CALC1  Orden de refutadores: verificar numéricamente que ordenar chequeos
       independientes por costo/p_kill ascendente (regla de Smith / kill-cheapness
       de EXP-07) minimiza el costo esperado hasta el primer kill, y medir
       cuánto pierde el "orden lógico de construcción" y el peor orden.
CALC2  Umbral económico de verificación: p* = c/(d·C). ¿A partir de qué
       probabilidad de error conviene comprar la observación?
CALC3  Medición real sobre este repo: costo en tokens de "leer el archivo
       entero" vs "grep + lectura dirigida" para responder una pregunta puntual.
CALC4  Lote vs secuencial: round-trips de k observaciones independientes.

Los parámetros (costos, probabilidades) son modelos declarados; lo medido es
la CONSECUENCIA de esos supuestos, y las conclusiones se testean por robustez.
"""

import itertools
import random
import os

random.seed(12)  # reproducible; el run no depende del reloj

# ---------------------------------------------------------------- CALC1
# Pipeline de chequeos independientes sobre un artefacto posiblemente malo.
# Cada chequeo i tiene costo c_i y probabilidad p_i de matar (detectar el
# fallo) condicional a que el fallo exista y ese chequeo lo cubra.
# Costo esperado de un orden = sum_i c_i * prod_{j<i} (1 - p_j)
# (pagas el chequeo i solo si ninguno anterior mató).

def expected_cost(order, checks):
    surv, total = 1.0, 0.0
    for i in order:
        c, p = checks[i]
        total += surv * c
        surv *= (1 - p)
    return total

def best_worst(checks):
    idx = range(len(checks))
    costs = {o: expected_cost(o, checks) for o in itertools.permutations(idx)}
    return min(costs.values()), max(costs.values()), costs

# Instancia concreta: los 6 refutadores de una estrategia de trading (EXP-07),
# costos relativos (horas) y p_kill estimadas del texto de EXP-07.
# Orden "lógico de construcción": señal→ejecución→sizing ≈ (as-of, atribución,
# OOS, costos, ejecución, sizing) puestos como los construiría alguien
# siguiendo el flujo natural: primero lo barato de codear, no lo que más mata.
trading = [
    (2, 0.35),   # 0 lookahead/as-of
    (1, 0.45),   # 1 costos y capacidad
    (6, 0.30),   # 2 OOS deflactado
    (4, 0.15),   # 3 atribución a factores
    (8, 0.10),   # 4 realismo de ejecución
    (3, 0.05),   # 5 dimensionamiento
]
build_order = (3, 2, 0, 4, 5, 1)      # como se "construye": análisis → ejecución, costos al final
ratio_order = tuple(sorted(range(6), key=lambda i: trading[i][0] / trading[i][1]))
best, worst, _ = best_worst(trading)

print("CALC1 — orden de refutadores (instancia trading, EXP-07)")
print(f"  orden por costo/p_kill {ratio_order}: costo esperado = {expected_cost(ratio_order, trading):.2f}")
print(f"  óptimo por fuerza bruta            = {best:.2f}  (¿coincide?: {abs(expected_cost(ratio_order, trading)-best) < 1e-9})")
print(f"  orden 'lógico de construcción'     = {expected_cost(build_order, trading):.2f}  ({expected_cost(build_order, trading)/best:.2f}x el óptimo)")
print(f"  peor orden                         = {worst:.2f}  ({worst/best:.2f}x el óptimo)")

# Robustez: 2000 instancias aleatorias de 6 chequeos; ¿la regla del ratio
# coincide con el óptimo por fuerza bruta? ¿cuánto pierde un orden aleatorio?
hits, rand_loss = 0, []
for _ in range(2000):
    checks = [(random.uniform(0.5, 10), random.uniform(0.02, 0.6)) for _ in range(6)]
    ro = tuple(sorted(range(6), key=lambda i: checks[i][0] / checks[i][1]))
    b, w, costs = best_worst(checks)
    if abs(expected_cost(ro, checks) - b) < 1e-9:
        hits += 1
    rnd = random.choice(list(costs.values()))
    rand_loss.append(rnd / b)
print(f"  robustez: ratio-order == óptimo en {hits}/2000 instancias aleatorias")
print(f"  orden aleatorio: {sum(rand_loss)/len(rand_loss):.2f}x el óptimo en promedio")

# ---------------------------------------------------------------- CALC2
# ¿Cuándo conviene comprar una observación (tool call) antes de afirmar?
# c = costo de la llamada; C = costo del error si se entrega sin verificar;
# d = prob. de que la observación detecte el error si existe;
# p = prob. previa de que la afirmación esté mal (confabulación).
# Verificar domina  <=>  p·d·C > c  <=>  p > p* = c/(d·C)
print("\nCALC2 — umbral económico de verificación p* = c/(d·C), con d=0.9")
for C_over_c in (3, 10, 30, 100):
    print(f"  error {C_over_c:>3}x más caro que la llamada -> verifica si p > {1/(0.9*C_over_c):.3f}")

# ---------------------------------------------------------------- CALC3
# Medición REAL sobre este repo: responder "¿qué dice la skill sobre
# validación cruzada?" leyendo el archivo entero vs grep + lectura dirigida.
skill = "/tmp/fable5/.claude/commands/fable5.md"
whole = os.path.getsize(skill)
with open(skill, encoding="utf-8") as f:
    lines = f.readlines()
hits_lines = [i for i, l in enumerate(lines) if "validación cruzada" in l]
window = 6  # lo que un Grep -C 3 devuelve por hit, aprox
targeted = sum(len(lines[j].encode()) for i in hits_lines
               for j in range(max(0, i - window // 2), min(len(lines), i + window // 2 + 1)))
print("\nCALC3 — medición real en este repo (pregunta puntual sobre la skill)")
print(f"  leer el archivo entero : {whole:,} bytes (~{whole//4:,} tokens)")
print(f"  grep + ventana dirigida: {targeted:,} bytes (~{targeted//4:,} tokens)  [{len(hits_lines)} hits]")
print(f"  factor de contexto     : {whole/targeted:.0f}x")

# ---------------------------------------------------------------- CALC4
# k observaciones independientes: secuencial paga k round-trips, lote paga 1.
print("\nCALC4 — lote vs secuencial (latencia L por round-trip)")
for k in (3, 5, 8):
    print(f"  k={k}: secuencial = {k}L, lote = 1L  -> ahorro {k}x en latencia de pared")
