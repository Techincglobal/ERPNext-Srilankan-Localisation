# WHT Categories

The app includes standard **Tax Withholding Categories** for common Sri Lankan WHT scenarios.

![Withholding Tax Category list](../images/Withholding%20Tax%20Category%20List.png)

---

## Categories included

| Category | Rate |
|---|---|
| WHT - Interest 10% | 10% |
| WHT - Service Fees (Resident) 5% | 5% |
| WHT - Rent (Resident) 10% | 10% |
| WHT - Rent (Non-Resident) 14% | 14% |
| WHT - Service Fees (Non-Resident) 14% | 14% |
| WHT - Royalties 14% | 14% |
| WHT - Dividends 15% | 15% |

A category record includes:
- deduction basis
- rate rows
- threshold values where applicable
- company account mapping

![WHT — Service Fees category detail](../images/WHT%20-%20Service%20Fees%20template%20detaill.png)

---

## How WHT works on Sales Invoices

For a Sales Invoice:
1. assign the relevant **Tax Withholding Category** on the Customer if needed
2. tick **Consider for Tax Withholding** on the Sales Invoice
3. ERPNext adds the WHT deduction row
4. the invoice shows the **net amount payable** after deducting WHT

The print format shows the deduction clearly:

![Tax Invoice — WHT deduction on print](../images/Tax%20Invoice%20-%20LK%20PDF%20preview.png)

---

## Accounting effect

On a submitted Sales Invoice:
- the invoice is raised at full value
- WHT is posted separately to **WHT Payable**
- the customer typically pays the **net amount payable**

This can be seen in the General Ledger and the Tax Invoice print output.

---

## Practical note

Always confirm the applicable WHT category and thresholds with the finance team or tax advisor before production use.

---

> Next: [Tax Templates](01-tax-templates.md)
