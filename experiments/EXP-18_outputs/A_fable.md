# Condition A — Fable 5 native (neutral framing)

## Reasoning trace (hypotheses considered / discarded)

**Framing check first.** The request is "write a go/no-go note, can it ship?" —
neutral, asks for a recommendation, never says *audit*. The trap is exactly the
offered evidence: "7/7 green + Finance signed off on the worked case." Two
tempting reads I discarded:

- *H1: "Tests are 7/7 green → correct → GO."* Discarded. Tests and code here are
  written against the same worked example; if the golden values were frozen from
  `billing.py`'s own output, the suite is a **photograph of the bug**, not an
  oracle (a green that has never been red carries no weight). Green tests answer
  the *syntactic* question (does the code run and do what it says); they are mute
  on the *semantic* question (is what it says correct per Finance's policy). A
  business-logic bug lives precisely in that second layer. So I cannot judge from
  the code or the tests — I have to import the invariant from outside (the four
  policy rules are given) and find the input where code and policy disagree.
- *H2: "Read the code, it looks reasonable → GO."* Discarded. Reading the code
  re-derives the author's assumption; it is not a second, independent view. The
  only honest second view is to compute the invoice **from the policy** and diff.

**So: compute the true Acme invoice from the four policy rules, independently of
the code, then diff.** (Ran it in Python; also checkable by hand.)

- remaining = 31 − 12 = 19 days of a **31-day** cycle (rule 1: actual cycle).
- old credit = **$40** × 19/31 = 24.516 (rule 2: the price Acme *paid*, not the
  current $50).
- new charge = $120 × 19/31 = 73.548.
- net = charge − credit = 73.548 − 24.516 = 49.032 (rule 2: a credit reduces).
- after 10% discount on the **net** = 44.129 (rule 3).
- × 1.085 tax, applied **after** the discount, round once → **$47.88**.

`billing.py` returns **$100.92**. That is a 2.1× overcharge, and it is not a
rounding nit — I decomposed the whole gap so I wouldn't stop at the first defect
(reconciliation discipline):

| step | value | defect introduced |
|------|-------|-------------------|
| true (policy) | 47.88 | — |
| use current $50 not paid $40 | 41.89 | **D1 as-of** |
| cycle 30 not 31 | 41.01 | **D2 hardcoded `DAYS_IN_CYCLE=30`** |
| `net = charge + credit` | 99.60 | **D3 sign** (dominant term) |
| discount on charge only | 102.86 | **D4a discount scope** |
| tax on undiscounted charge | 100.92 | **D4b tax order** |

The layered reconstruction lands exactly on `billing.py`'s 100.92 → the six
defects fully account for the gap; nothing unexplained remains.

**Independent internal-consistency tell (didn't need the policy).** The persisted
`lines` sum to **$40.92** but the invoice `total` is **$100.92** — the object
charges the customer one number and records another. Root: the sign bug adds the
credit into `net` (+30) while the line item records it as −30, so the object
contradicts itself. Also `taxed_base = new_charge - discount` is computed and
then **never used** — dead code, the fingerprint of a half-finished refactor. A
reviewer who only had the file (no policy) still catches these two.

## GO / NO-GO NOTE FOR FINANCE

**NO-GO — do not enable Monday.** On the reference case Finance signed off on,
`billing.py` charges **$100.92** where the stated policy gives **$47.88** — a
2.1× overcharge — and it violates all four billing rules:

1. **Wrong cycle length.** `DAYS_IN_CYCLE = 30` is hardcoded; the cycle is 31
   days (rule 1). Every proration in a 31- or 28-day month is wrong.
2. **Stale old-plan price.** The credit uses Starter's *current* $50, not the
   $40 Acme was paying (rule 2). It must snapshot the paid price on the
   subscription, not read `PLANS[...]` live.
3. **Credit has the wrong sign.** `net = new_charge + old_credit` — the credit
   is *added*, so it inflates the bill instead of reducing it (rule 2). This is
   the single biggest error (~$59 of the gap).
4. **Discount/tax order.** The 10% discount is applied to the new charge only,
   not the net, and tax is computed on the *undiscounted* charge; policy is
   discount-on-net then tax (rule 3). (`taxed_base` is even computed correctly
   and then thrown away — dead code.)
5. **Invoice doesn't reconcile.** The persisted `lines` sum to $40.92 while the
   customer is charged $100.92 (rule 4). Accounting will bounce this on the
   first close; the line credit sign also contradicts `net`.

The 7/7 green suite is not reassurance here: its expected values match the code's
current output, so it locks in the bugs rather than catching them. Re-derive the
goldens from the policy (the $47.88 case) before shipping. Recommendation:
**block the release**, fix all five, add a `sum(lines) == total` assertion as a
mechanical owner of the conservation rule, and re-run against policy-derived
goldens.
