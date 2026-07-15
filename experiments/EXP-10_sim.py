"""EXP-10: simulaciones que respaldan cada afirmacion cuantitativa del razonamiento.
Caso: A/B test, baseline 5.0%, reportado 5.9% (+18% rel), n=12000/rama, 9 dias, p=0.03.
Subgrupo: Android+semana1 p=0.008.
"""
import numpy as np
from math import sqrt, erf

rng = np.random.default_rng(20260715)

def z_to_p(z):
    # two-sided p from z
    return 2 * (1 - 0.5 * (1 + erf(abs(z) / sqrt(2))))

def two_prop_z(x1, n1, x2, n2):
    p1, p2 = x1 / n1, x2 / n2
    p = (x1 + x2) / (n1 + n2)
    se = sqrt(p * (1 - p) * (1 / n1 + 1 / n2))
    if se == 0:
        return 0.0, 1.0
    z = (p2 - p1) / se
    return z, z_to_p(z)

# ---------------------------------------------------------------
# SIM 1: optional stopping (peeking diaria, 9 miradas, parar si p<0.05)
# H0 verdadera: ambas ramas 5.0%. n acumula 1333/dia/rama hasta ~12000.
# ---------------------------------------------------------------
def sim_peeking(n_sims=20000, days=9, per_day=1334, p0=0.05, alpha=0.05):
    hits = 0
    for _ in range(n_sims):
        cA = cB = nA = nB = 0
        for d in range(days):
            cA += rng.binomial(per_day, p0); nA += per_day
            cB += rng.binomial(per_day, p0); nB += per_day
            _, p = two_prop_z(cA, nA, cB, nB)
            if p < alpha:
                hits += 1
                break
    return hits / n_sims

fpr_peek = sim_peeking()
print(f"SIM1 peeking: P(declarar 'p<0.05' bajo H0 con 9 miradas diarias) = {fpr_peek:.3f}")
print(f"      (el 'p=0.03' reportado con parada opcional tiene error tipo I real ~{fpr_peek:.0%}, no 5%)")

# ---------------------------------------------------------------
# SIM 2: subgrupos. H0 verdadera. Analista explora K subgrupos
# (3 plataformas x 4 semanas = 12 celdas, n~1000/celda/rama).
# P(algun subgrupo con p<0.01)?
# ---------------------------------------------------------------
def sim_subgroups(n_sims=20000, K=12, n_cell=1000, p0=0.05):
    hits01 = 0
    hits008 = 0
    for _ in range(n_sims):
        pmin = 1.0
        for _ in range(K):
            cA = rng.binomial(n_cell, p0)
            cB = rng.binomial(n_cell, p0)
            _, p = two_prop_z(cA, n_cell, cB, n_cell)
            pmin = min(pmin, p)
        if pmin < 0.01: hits01 += 1
        if pmin < 0.008: hits008 += 1
    return hits01 / n_sims, hits008 / n_sims

sg01, sg008 = sim_subgroups()
print(f"SIM2 subgrupos: P(min p de 12 celdas < 0.01 bajo H0) = {sg01:.3f}; P(<0.008) = {sg008:.3f}")

# ---------------------------------------------------------------
# SIM 3: winner's curse. Efecto real modesto: +5% relativo (5.0% -> 5.25%).
# n=12000/rama, test unico al final. Entre los sims significativos (p<0.05, B>A):
# lift relativo estimado promedio vs real.
# ---------------------------------------------------------------
def sim_winners_curse(n_sims=40000, n=12000, p0=0.05, lift_rel=0.05):
    p1 = p0 * (1 + lift_rel)
    est_lifts_sig = []
    sig = 0
    for _ in range(n_sims):
        cA = rng.binomial(n, p0)
        cB = rng.binomial(n, p1)
        _, p = two_prop_z(cA, n, cB, n)
        if p < 0.05 and cB / n > cA / n:
            sig += 1
            est_lifts_sig.append((cB / n - cA / n) / (cA / n))
    power = sig / n_sims
    mean_est = float(np.mean(est_lifts_sig))
    return power, mean_est

power, mean_est = sim_winners_curse()
print(f"SIM3 winner's curse: efecto real +5% rel, n=12000/rama -> poder = {power:.2f}")
print(f"      lift estimado promedio CONDICIONAL a significancia = +{mean_est:.1%} (inflacion x{mean_est/0.05:.1f})")

# ---------------------------------------------------------------
# SIM 4: posterior. De cada 100 tests que corre el equipo, ~10 tienen
# efecto real (+5% rel tipico). Con el poder medido en SIM3 y el error
# tipo I real de SIM1 (peeking), P(efecto real | 'significativo')?
# ---------------------------------------------------------------
def posterior(prior, power_, alpha_):
    return prior * power_ / (prior * power_ + (1 - prior) * alpha_)

for prior in (0.10, 0.30):
    post_clean = posterior(prior, power, 0.05)
    post_peek = posterior(prior, power, fpr_peek)  # poder tambien sube con peeking, aprox conservadora
    print(f"SIM4 posterior: prior={prior:.0%} -> P(real|sig) = {post_clean:.2f} (test limpio), "
          f"= {post_peek:.2f} (con peeking, cota superior)")

# ---------------------------------------------------------------
# SIM 5: el +18% relativo reportado, si el efecto tipico real es +5%,
# cae donde en la distribucion de estimaciones significativas?
# Y: cuanta evidencia aporta p=0.03 solo? (factor de Bayes aproximado
# via cota de Sellke-Bayarri-Berger: BF <= 1/(-e p ln p))
# ---------------------------------------------------------------
from math import e, log
p_rep = 0.03
bf_bound = 1 / (-e * p_rep * log(p_rep))
print(f"SIM5 cota SBB: p=0.03 -> factor de Bayes maximo contra H0 = {bf_bound:.1f} (evidencia debil)")
