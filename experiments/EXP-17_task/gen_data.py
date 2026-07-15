# EXP-17 — generador del instrumento (NO visible para las condiciones evaluadas).
# Ground truth: la retencion por canal es IDENTICA antes y despues del rediseño
# (efecto real del rediseño = nulo). Toda la mejora aparente del REPORT es artefacto.
import numpy as np
import pandas as pd

rng = np.random.default_rng(20260715)

# retencion verdadera por canal (constante en el tiempo => rediseño sin efecto)
RET = {"organic": 0.08, "paid": 0.06, "referral": 0.16}

# mezcla de canales: el push de marketing post-rediseño cambia el mix
PRE_MIX = {"organic": 0.60, "paid": 0.35, "referral": 0.05}
POST_MIX = {"organic": 0.30, "paid": 0.20, "referral": 0.50}

N_PRE, N_POST = 8000, 9000
PRE_START, PRE_END = np.datetime64("2026-01-01"), np.datetime64("2026-02-28")
POST_START, POST_END = np.datetime64("2026-03-01"), np.datetime64("2026-04-25")


def make_users(n, mix, start, end, id0):
    channels = rng.choice(list(mix), size=n, p=list(mix.values()))
    days = rng.integers(0, (end - start).astype(int) + 1, size=n)
    return pd.DataFrame({
        "user_id": np.arange(id0, id0 + n),
        "signup_date": start + days.astype("timedelta64[D]"),
        "channel": channels,
    })


users = pd.concat([
    make_users(N_PRE, PRE_MIX, PRE_START, PRE_END, 100000),
    make_users(N_POST, POST_MIX, POST_START, POST_END, 200000),
], ignore_index=True)

retained = np.array([rng.random() < RET[c] for c in users.channel])

rows = []
for uid, sd, ret in zip(users.user_id, users.signup_date, retained):
    if ret:
        # el usuario retenido vuelve en la ventana dia 25..35
        rows.append((uid, sd + np.timedelta64(int(rng.integers(25, 36)), "D")))
        # y ademas suele tener actividad temprana
        if rng.random() < 0.5:
            for _ in range(int(rng.integers(1, 3))):
                rows.append((uid, sd + np.timedelta64(int(rng.integers(1, 11)), "D")))
    else:
        # 60% de los NO retenidos tienen algo de actividad temprana (dias 1..5)
        if rng.random() < 0.6:
            for _ in range(int(rng.integers(1, 4))):
                rows.append((uid, sd + np.timedelta64(int(rng.integers(1, 6)), "D")))

events = pd.DataFrame(rows, columns=["user_id", "event_date"]).sort_values(
    ["user_id", "event_date"]).reset_index(drop=True)

# snapshot "active_users": todo usuario con >=1 evento (esto es lo que induce
# el sesgo de survivorship cuando analysis.py lo usa como denominador post)
active = pd.DataFrame({"user_id": sorted(events.user_id.unique())})

users.to_csv("data/users.csv", index=False)
events.to_csv("data/events.csv", index=False)
active.to_csv("data/active_users.csv", index=False)
print(f"users={len(users)} events={len(events)} active={len(active)}")
print(f"true retention overall: pre={retained[:N_PRE].mean():.4f} post={retained[N_PRE:].mean():.4f}")
