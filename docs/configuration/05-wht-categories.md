# WHT Categories

Withholding Tax (WHT) is deducted by the purchaser from their payment and remitted directly to the IRD. The app creates seven Tax Withholding Categories on install, covering all common Sri Lankan payment types.

---

## Categories created on install

![Withholding Tax Category list](../images/Withholding%20Tax%20Category%20List.png)

| Category | Rate | Threshold (per month) |
|---|---|---|
| WHT - Interest 10% | 10% | None |
| WHT - Service Fees (Resident) 5% | 5% | LKR 100,000 |
| WHT - Rent (Resident) 10% | 10% | LKR 100,000 |
| WHT - Rent (Non-Resident) 14% | 14% | None |
| WHT - Service Fees (Non-Resident) 14% | 14% | None |
| WHT - Royalties 14% | 14% | None |
| WHT - Dividends 15% | 15% | None |

Each category is automatically linked to the **WHT Payable** account for every Sri Lankan company on the site, and rate rows are added for all existing fiscal years.

![WHT — Service Fees category detail](../images/WHT%20-%20Service%20Fees%20template%20detaill.png)

> **Note:** ERPNext's threshold logic is cumulative per fiscal year, not strictly per calendar month. For the resident service fees and rent categories, the LKR 100,000 single-transaction threshold approximates the IRD monthly rule. If a supplier has multiple smaller invoices in a month, apply WHT manually using the checkbox on the invoice.

---

## Assigning WHT to a Supplier

Open the **Supplier** record, go to the **Tax Withholding** section, and set **Tax Withholding Category** to the relevant category (e.g. `WHT - Rent (Resident) 10%` for a resident landlord).

Once set, every Purchase Invoice for that supplier will show an **Apply Tax Withholding Amount** checkbox.

---

## Applying WHT on a Sales Invoice

On a Sales Invoice, WHT can be applied at item level via the `tax_withholding_category` field on each item row, or at the header level via the **Apply TDS** checkbox.

When WHT is applied, the Tax Invoice print format shows it as a clean deduction:

![Tax Invoice — WHT deduction on print](../images/Tax%20Invoice%20-%20LK%20PDF%20preview.png)

The totals section on the invoice will display:

| | |
|---|---|
| Total Value of Supply | base amount |
| SSCL / VAT | tax amounts |
| **Total Amount including Tax** | pre-WHT total |
| Less: Withholding Tax (WHT) | ( WHT amount ) |
| **Net Amount Payable** | amount the customer pays |

The **Amount in Words** also reflects the net payable figure.

---

## Updating rates for a new fiscal year

When a new fiscal year is created, run migrate to add rate rows for it automatically:

```bash
bench --site <your-site> migrate
```

To update a rate (e.g. if IRD changes the interest rate), open the Tax Withholding Category record and edit the rate row for the relevant fiscal year.

---

> Next: [LK Tax Settings](02-lk-tax-settings.md)
