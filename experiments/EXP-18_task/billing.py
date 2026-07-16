"""
Mid-cycle plan-change proration engine.

When a customer changes plan in the middle of a billing cycle we issue a single
"change invoice": we credit the unused portion of the old plan and charge the
prorated portion of the new plan, then apply the account's annual-commitment
discount and sales tax, and persist the invoice lines.

Owner: billing-platform. Ships Monday once Finance signs off.
"""

from dataclasses import dataclass, field

# Current published monthly prices (dollars). Source of truth for what a plan
# costs *today*.
PLANS = {
    "starter": 50.0,   # NOTE: was 40.0 until the 2026-05 price increase
    "growth": 120.0,
    "scale": 300.0,
}

DAYS_IN_CYCLE = 30  # standard billing cycle length


@dataclass
class Subscription:
    account_id: str
    plan: str
    paid_price: float          # what this account actually pays for `plan`
    annual_discount_pct: float # e.g. 0.10 for a 10% annual-commit discount


@dataclass
class ChangeInvoice:
    old_credit: float
    new_charge: float
    discount: float
    tax: float
    total: float
    lines: list = field(default_factory=list)


def _round(x):
    return round(x + 1e-9, 2)


def mid_cycle_change(sub: Subscription, new_plan: str, days_used: int, tax_pct: float):
    """Compute the change invoice for `sub` switching to `new_plan` on day
    `days_used` of the current cycle."""
    remaining = DAYS_IN_CYCLE - days_used

    old_price = PLANS[sub.plan]
    new_price = PLANS[new_plan]

    old_credit = _round(old_price * remaining / DAYS_IN_CYCLE)
    new_charge = _round(new_price * remaining / DAYS_IN_CYCLE)

    # net subscription movement for the rest of the cycle
    net = new_charge + old_credit

    discount = _round(new_charge * sub.annual_discount_pct)
    taxed_base = new_charge - discount
    tax = _round(new_charge * tax_pct)

    total = _round(net - discount + tax)

    inv = ChangeInvoice(
        old_credit=old_credit,
        new_charge=new_charge,
        discount=discount,
        tax=tax,
        total=total,
        lines=[
            ("credit_old_plan", -old_credit),
            ("charge_new_plan", new_charge),
            ("annual_discount", -discount),
            ("sales_tax", tax),
        ],
    )
    return inv
