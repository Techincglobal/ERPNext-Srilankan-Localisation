# Tax Templates

The app creates a full set of Sri Lankan tax templates on install. Select the appropriate one from the **Taxes and Charges** field when creating a Sales Invoice or Purchase Invoice.

---

## Sales templates

![Sales tax template list](../images/Sales%20tax%20template%20list.png)

| Template | Use when |
|---|---|
| **Sales VAT 18%** | Standard sale subject to VAT only |
| **Sales VAT + SSCL** | Sale subject to both SSCL (2.5%) and VAT (18%) |
| **SSCL** | Sale subject to SSCL only |
| **SVAT** | Selling to a registered SVAT scheme customer |
| **SUSPENDED TAX** | Suspended tax transaction (as advised by your tax advisor) |
| **NON VAT - Sales** | Sale not subject to VAT |

The **Sales VAT + SSCL** template applies SSCL first, then VAT on the SSCL-inclusive total:

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

The taxes breakdown on a submitted invoice:

![Submitted Sales Invoice — taxes](../images/Submitted%20Sales%20Invoice%20taxes.png)

And the resulting General Ledger entries:

![General Ledger — submitted Sales Invoice](../images/General%20Ledger%20for%20Submitted%20Sales%20Invoice.png)

---

> If you are unsure which template applies to a transaction, consult your tax advisor.

---

> Next: [WHT Categories](05-wht-categories.md)
