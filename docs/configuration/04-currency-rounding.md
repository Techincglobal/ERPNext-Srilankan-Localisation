# Currency & Rounding

Sri Lankan Rupees (LKR) do not use cent values in practice. This page explains how to configure ERPNext to display LKR amounts as whole numbers.

---

## Enable rounding on Sales Invoice

ERPNext has a built-in **Round Off** option on Sales Invoice that rounds the grand total to the nearest whole rupee.

To round automatically:

1. Open a Sales Invoice
2. In the **Totals** section, tick **Round Off**
3. The **Rounding Adjustment** row will appear and the **Rounded Total** will be a whole number

![Global settings — rounded total](../images/Global%20settings%20rounded%20total.png)

> The Tax Invoice print format uses `doc.rounded_total` when available, falling back to `doc.grand_total`. Enabling Round Off ensures the printed total is always a whole rupee.

---

## Set up rounding accounts on the company

For the rounding adjustment to post correctly to the General Ledger, assign a rounding account on the company record:

![Company — setting up rounded-off accounts](../images/Setting%20up%20rounded%20off%20accounts%20in%20company.png)

1. Open your **Company** record
2. Scroll to the **Accounts** section
3. Set **Round Off Account** to an appropriate income/expense account (typically a small rounding difference account)
4. Save

---

## Result

After these steps, all LKR amounts on invoices, reports, and the Tax Invoice print format display as whole rupees without a decimal separator.
