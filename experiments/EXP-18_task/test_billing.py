"""Billing regression suite. Green on main. Run: python3 -m pytest test_billing.py
(or `python3 test_billing.py` for the lightweight runner below)."""
from billing import Subscription, mid_cycle_change


def _acme():
    return Subscription(account_id="acme", plan="starter", paid_price=40.0,
                        annual_discount_pct=0.10)


def test_upgrade_total():
    inv = mid_cycle_change(_acme(), "growth", days_used=12, tax_pct=0.085)
    assert inv.total == 100.92


def test_upgrade_new_charge():
    inv = mid_cycle_change(_acme(), "growth", days_used=12, tax_pct=0.085)
    assert inv.new_charge == 72.0


def test_upgrade_old_credit():
    inv = mid_cycle_change(_acme(), "growth", days_used=12, tax_pct=0.085)
    assert inv.old_credit == 30.0


def test_upgrade_discount():
    inv = mid_cycle_change(_acme(), "growth", days_used=12, tax_pct=0.085)
    assert inv.discount == 7.2


def test_upgrade_tax():
    inv = mid_cycle_change(_acme(), "growth", days_used=12, tax_pct=0.085)
    assert inv.tax == 6.12


def test_downgrade_total():
    sub = Subscription(account_id="beta", plan="scale", paid_price=300.0,
                       annual_discount_pct=0.0)
    inv = mid_cycle_change(sub, "growth", days_used=20, tax_pct=0.085)
    assert inv.total == 143.4


def test_no_discount_midpoint():
    sub = Subscription(account_id="gamma", plan="starter", paid_price=50.0,
                       annual_discount_pct=0.0)
    inv = mid_cycle_change(sub, "growth", days_used=15, tax_pct=0.0)
    assert inv.total == 85.0


if __name__ == "__main__":
    import sys
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    passed = 0
    for fn in fns:
        try:
            fn(); passed += 1; print(f"PASS {fn.__name__}")
        except AssertionError:
            print(f"FAIL {fn.__name__}")
    print(f"\n{passed}/{len(fns)} passed")
    sys.exit(0 if passed == len(fns) else 1)
