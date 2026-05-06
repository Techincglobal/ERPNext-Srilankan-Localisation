# Currency & Rounding

This app does **not** force a global currency precision change for LKR. Instead, invoice rounding is handled using ERPNext’s rounded total behaviour together with a company round-off account.

---

## Rounded total on invoices

On Sales Invoices, ERPNext can round the final total and store the difference as a rounding adjustment.

![Global settings — rounded total](../images/Global%20settings%20rounded%20total.png)

A submitted Sales Invoice can therefore show:
- **Grand Total**
- **Rounding Adjustment**
- **Rounded Total**

This is useful when the printed invoice should show a cleaner payable figure.

---

## Company round-off setup

To ensure the rounding difference posts correctly, set a round-off account in the Company record.

![Company — setting up rounded-off accounts](../images/Setting%20up%20rounded%20off%20accounts%20in%20company.png)

Recommended steps:
1. Open the **Company** record
2. Go to the **Accounts** tab
3. Set **Round Off Account**
4. Set **Round Off Cost Center** if required
5. Save

---

## Important note

This approach is intentionally limited to **invoice rounding**. It avoids changing global currency precision, which could affect other transactions that still need decimals.

---

## Result

When combined with the Tax Invoice print format, rounded totals help produce a cleaner payable amount on invoices while keeping ERPNext accounting entries balanced through the round-off account.

---

> Next: [WHT Categories](05-wht-categories.md)
