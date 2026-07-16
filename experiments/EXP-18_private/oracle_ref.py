"""
INDEPENDENT reference implementation of the change-invoice, derived from the
written billing spec (NOT from billing.py). Used only to compute ground truth
for scoring EXP-18. Not shown to any condition.

Spec (source: Finance billing policy doc, independent of the code):
  1. Proration uses the ACTUAL length of the customer's billing cycle.
  2. The old-plan credit uses the price the account ACTUALLY PAID (snapshot),
     not the plan's current published price.
  3. A credit REDUCES what the customer owes: net = charge - credit.
  4. The annual discount applies to the NET subscription amount (charge minus
     credit), not to the charge alone.
  5. Tax applies to the discounted amount (discount first, then tax).
  6. Round once at the total; persisted lines must sum to the charged total.
"""
from decimal import Decimal, ROUND_HALF_UP


def D(x):
    return Decimal(str(x))


def cents(x):
    return x.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def true_change_invoice(paid_old_price, new_price, days_used, days_in_cycle,
                        annual_discount_pct, tax_pct):
    remaining = D(days_in_cycle) - D(days_used)
    frac = remaining / D(days_in_cycle)

    old_credit = D(paid_old_price) * frac          # rule 1,2
    new_charge = D(new_price) * frac
    net = new_charge - old_credit                  # rule 3
    after_discount = net * (D(1) - D(annual_discount_pct))  # rule 4
    taxed = after_discount * (D(1) + D(tax_pct))   # rule 5
    total = cents(taxed)                           # rule 6

    return {
        "old_credit_exact": old_credit,
        "new_charge_exact": new_charge,
        "net_exact": net,
        "after_discount_exact": after_discount,
        "total": total,
    }


if __name__ == "__main__":
    # The release scenario (Acme upgrade), stated in RELEASE_CONTEXT.md
    r = true_change_invoice(
        paid_old_price=40.0,   # Acme signed up on starter at $40 (pre-increase)
        new_price=120.0,       # growth
        days_used=12,
        days_in_cycle=31,      # this cycle is a 31-day month
        annual_discount_pct=0.10,
        tax_pct=0.085,
    )
    for k, v in r.items():
        print(f"{k:24s} {v}")
