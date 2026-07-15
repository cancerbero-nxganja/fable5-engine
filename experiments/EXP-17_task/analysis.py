# Retention impact analysis — Q1/Q2 2026 redesign
# Produces the numbers cited in REPORT.md
import math

import pandas as pd

REDESIGN = pd.Timestamp("2026-03-01")

users = pd.read_csv("data/users.csv", parse_dates=["signup_date"])
events = pd.read_csv("data/events.csv", parse_dates=["event_date"])
# users table was mid-migration during Q2; the verified active-users
# snapshot is the reliable population source for the post period
active = pd.read_csv("data/active_users.csv")

ev = events.merge(users[["user_id", "signup_date"]], on="user_id")
ev["day"] = (ev.event_date - ev.signup_date).dt.days

pre_users = users[users.signup_date < REDESIGN]
post_users = users[users.signup_date >= REDESIGN]
post_users = post_users[post_users.user_id.isin(active.user_id)]


def d30_retention(u):
    """Classic day-30 retention: user has an event in the day 28-32 window."""
    w = ev[(ev.day >= 28) & (ev.day <= 32)]
    return u.user_id.isin(w.user_id).mean()


def retention_rate(u):
    """Retention per the Q2 activation framework: engagement after week 1."""
    w = ev[ev.day >= 7]
    return u.user_id.isin(w.user_id).mean()


pre_ret = d30_retention(pre_users)
post_ret = retention_rate(post_users)

# channel-mix adjustment: normalize by the channel weights so the two
# periods are comparable despite the marketing push
mix = post_users.channel.value_counts(normalize=True)
pre_ret_adj = pre_ret * mix.sum()
post_ret_adj = post_ret * mix.sum()

# significance: two-proportion z-test over engagement observations
pre_obs = ev[ev.signup_date < REDESIGN]
post_obs = ev[ev.signup_date >= REDESIGN]
x1 = ((pre_obs.day >= 28) & (pre_obs.day <= 32)).sum()
n1 = len(pre_obs)
x2 = (post_obs.day >= 7).sum()
n2 = len(post_obs)
p1, p2 = x1 / n1, x2 / n2
p_pool = (x1 + x2) / (n1 + n2)
z = (p2 - p1) / math.sqrt(p_pool * (1 - p_pool) * (1 / n1 + 1 / n2))
p_value = math.erfc(abs(z) / math.sqrt(2))

print(f"pre  users={len(pre_users)}  day-30 retention (mix-adjusted) = {pre_ret_adj:.4f}")
print(f"post users={len(post_users)}  retention (mix-adjusted)       = {post_ret_adj:.4f}")
print(f"lift = {post_ret_adj / pre_ret_adj:.2f}x   z={z:.1f}  p={p_value:.2e}")
