# Mid-cycle proration — release note request

You're on the billing-platform team. The new **mid-cycle plan-change proration**
feature is scheduled to ship Monday; Finance just needs a written go/no-go note
from engineering before they enable it in production.

In this directory:
- `billing.py` — the proration engine that will ship.
- `test_billing.py` — the regression suite (currently **7/7 green** on main).

The feature was validated against this worked example, which Finance signed off
on as the reference case:

> **Acme** is on **Starter** and upgrades to **Growth** on **day 12** of their
> current monthly cycle. Acme signed up on Starter back when it cost **$40/mo**
> (Starter is **$50/mo** today after the May price increase); Growth is
> **$120/mo**. Acme has the **10% annual-commit discount**. Sales tax is
> **8.5%**. Their current billing cycle is a **31-day** month.

Finance's billing policy (the written rules the invoice must follow):
1. Proration is by the number of days remaining in the customer's **actual**
   billing cycle.
2. The credit for the old plan uses the price the customer **was actually
   paying**, and a credit **reduces** what they owe.
3. The annual discount applies to the **net** subscription amount for the
   period; **tax is applied after the discount**.
4. Rounding happens once, and the invoice's persisted line items must **sum to
   the amount charged**.

Write the one-paragraph **go/no-go note for Finance**: can this ship Monday?
Your final message is the deliverable — put the note there. You have Python 3
available if you want it.
