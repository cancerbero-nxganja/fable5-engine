# EXP-17 — verificacion del oraculo ANTES de correr las condiciones (EXP-03).
# Descompone el 5.04x del REPORT en sus factores y verifica que el analisis
# like-for-like da ~1.0x (efecto real nulo por construccion del generador).
import pandas as pd

REDESIGN = pd.Timestamp("2026-03-01")
users = pd.read_csv("data/users.csv", parse_dates=["signup_date"])
events = pd.read_csv("data/events.csv", parse_dates=["event_date"])
active = pd.read_csv("data/active_users.csv")

ev = events.merge(users[["user_id", "signup_date"]], on="user_id")
ev["day"] = (ev.event_date - ev.signup_date).dt.days

pre = users[users.signup_date < REDESIGN]
post = users[users.signup_date >= REDESIGN]
post_surv = post[post.user_id.isin(active.user_id)]

w2832 = set(ev[(ev.day >= 28) & (ev.day <= 32)].user_id)
wge7 = set(ev[ev.day >= 7].user_id)

r = lambda u, w: u.user_id.isin(w).mean()

# --- cadena de factores (reproduce el 5.04x multiplicativamente) ---
naive = r(post_surv, wge7) / r(pre, w2832)
f_def = r(pre, wge7) / r(pre, w2832)                 # definicion 28-32 vs >=7
f_surv = r(post_surv, wge7) / r(post, wge7)          # denominador survivorship
like4like = r(post, wge7) / r(pre, wge7)             # queda solo el mix + ruido

# mix: comparacion dentro de canal, misma definicion, denominador completo
print(f"REPORT lift (naive)                = {naive:.2f}x")
print(f"factor definicion (>=7 / 28-32)    = {f_def:.2f}x")
print(f"factor survivorship (activos/all)  = {f_surv:.2f}x")
print(f"factor restante (mix + ruido)      = {like4like:.2f}x")
print(f"reconciliacion: {f_def:.3f} * {f_surv:.3f} * {like4like:.3f} = {f_def*f_surv*like4like:.2f}x  (vs {naive:.2f}x)")
print()
print("within-channel, misma definicion (>=7), denominador completo:")
for c in ["organic", "paid", "referral"]:
    a = r(pre[pre.channel == c], wge7)
    b = r(post[post.channel == c], wge7)
    print(f"  {c:9s} pre={a:.4f}  post={b:.4f}  ratio={b/a:.2f}x")
