# Tax Templates

The app creates the standard Sri Lankan sales and purchase tax templates for supported transaction scenarios. Select the appropriate template from **Taxes and Charges** on a Sales Invoice or Purchase Invoice.

---

## Sales templates

![Sales tax template list](../images/Sales%20tax%20template%20list.png)

| Template | Use when |
|---|---|
| **Sales VAT 18%** | Standard sale subject to VAT only |
| **Sales VAT + SSCL** | Sale subject to both SSCL (2.5%) and VAT (18%) |
| **SSCL** | Sale subject to SSCL only |
| **SVAT** | Transaction handled under SVAT rules |
| **SUSPENDED TAX** | Suspended tax transaction, if applicable |
| **NON VAT - Sales** | Sale not subject to VAT |

The **Sales VAT + SSCL** template applies SSCL first and then VAT on the SSCL-inclusive total.

![Sales VAT + SSCL template — charge breakdown](../images/Sales%20VAT%20%2B%20SSCL%20template%20detail.png)

---

## Purchase templates

![Purchase tax template list](../images/Purchase%20tax%20template%20list.png)

| Template | Use when |
|---|---|
| **Purchase VAT 18%** | Standard purchase with recoverable VAT |
| **Purchase VAT + SSCL** | Purchase subject to both SSCL and VAT |
| **Non VAT Purchase** | Purchase not subject to VAT |

---

## On a submitted Sales Invoice

A submitted Sales Invoice shows the taxes populated from the selected template together with any WHT deduction applied on the invoice.

![Submitted Sales Invoice — taxes](../images/Submitted%20Sales%20Invoice%20taxes.png)

The resulting General Ledger entries confirm the tax and round-off postings.

![General Ledger — submitted Sales Invoice](../images/General%20Ledger%20for%20Submitted%20Sales%20Invoice.png)

---

## Notes

- Use **sales templates** on Sales Invoices and **purchase templates** on Purchase Invoices.
- If WHT applies, it appears as a separate deduction row on the invoice in addition to VAT and SSCL.
- Review account heads in each template before using the app in production.

---

> Next: [LK Tax Settings](02-lk-tax-settings.md)
