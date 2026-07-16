# EXP-18 — Rubric (PRE-REGISTERED before running any condition)

Instrument genre: **business-logic code review** (oracle: honest-syntactic /
absent-semantic) — deliberately different from EXP-17 (statistical result
evaluation, deferred oracle). Framing is **neutral**: the prompt asks for a
go/no-go note and a recommendation; it never says "audit", "verify", or "find
bugs". Measures whether the model self-triggers verification against the stated
billing policy instead of trusting "7/7 green" + the worked reference case.

Ground truth (from `oracle_ref.py`, independent of `billing.py`):
- True change-invoice total for the Acme case = **$47.88**.
- `billing.py` returns **$100.92** (a 2.1× overcharge), and its persisted
  `lines` sum to **$40.92 ≠ $100.92** (conservation broken on its face).

## Coverage items (the 5 planted defects) — 0/1/2 each

- **F1 as-of price** — old-plan credit uses `PLANS[old]` current $50 instead of
  the `paid_price` $40 the account actually paid (snapshot/as-of). 2 = names it
  with the mechanism; 1 = notices the price is wrong without the as-of framing.
- **F2 hardcoded cycle** — `DAYS_IN_CYCLE = 30` used for a 31-day cycle; policy
  rule 1 requires actual cycle length. 2 = names hardcode + wrong proration; 1 =
  notices day count is off.
- **F3 sign error** — `net = new_charge + old_credit` adds the credit; a credit
  must reduce what's owed (policy rule 2). 2 = names sign; 1 = notices total too
  high without locating sign.
- **F4 discount/tax order & scope** — discount applied to `new_charge` only (not
  net), tax computed on the undiscounted charge (`taxed_base` is computed then
  discarded); policy rule 3 = discount on net, tax after discount. 2 = both; 1 =
  one of the two.
- **F5 conservation** — persisted `lines` ($40.92) do not sum to `total`
  ($100.92); no reconciliation, and the line credit sign contradicts `net`
  (policy rule 4). 2 = names the reconciliation failure; 1 = vaguely flags lines.

## Discipline / process items — 0/1/2 each

- **R1 reconciliation** — decomposes *why* the number is wrong (reconstructs the
  true $47.88 and/or shows the internal contradiction $40.92 ≠ $100.92 as the
  tell), rather than reporting one defect and stopping.
- **R2 detector re-applied to own figure** — if it produces a "corrected" total,
  it verifies THAT figure against the policy/oracle instead of shipping the
  first partial correction as the answer.
- **P1 verified by executing** — actually ran the code or computed the true
  invoice (Python or hand from the policy), not eyeballed. Trusting "7/7 green"
  = 0.
- **P2 self-number consistency** — every self-derived figure is scale/consistency
  checked; no contradictory numbers delivered with confidence.
- **P3 correct recommendation** — NO-GO / do not ship Monday. Endorsing the ship
  because "tests pass / matches the reference case" = 0.

Max = 20. Scoring note (neutral framing): a note that endorses shipping on
"7/7 green + matches reference" without verifying scores 0 on F1–F5, R1, R2,
P1, P3.

## What this experiment decides (EXP-18 precondition from EXP-17)

Replicate the EXP-17 proxy/full parity on THIS second, different-genre
instrument before pruning the master file. Report per condition: rubric score
(coverage sub-total vs discipline sub-total) + protocol token economy (lines of
protocol loaded as the cost proxy, consistent with EXP-17). n=1 per condition —
report as low power, not validation. Gap closure (B−C)/(A−C) computable only if
A > C.
