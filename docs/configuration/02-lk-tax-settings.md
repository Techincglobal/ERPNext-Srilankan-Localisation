# LK Tax Settings

**LK Tax Settings** is a small settings page for Sri Lanka-specific validation behaviour. Access it by searching for **LK Tax Settings** in the desk search bar.

![LK Tax Settings page](../images/LK%20Tax%20Settings.png)

---

## Setting available

### Enforce TIN on Tax Invoice Submission

| Value | Behaviour |
|---|---|
| **Off** (default) | Sales Invoices can be submitted without a customer TIN |
| **On** | Sales Invoices cannot be submitted unless the customer has a TIN on record |

When enabled, the expected workflow is:
1. Enter the customer TIN in the Customer record
2. Create the Sales Invoice
3. Submit only after the customer TIN is present

---

## Recommended usage

Turn this on after customer master data has been cleaned and TINs have been entered where required.

Recommended sequence:
1. Complete customer setup
2. Test invoice creation
3. Enable the setting
4. Re-test invoice submission without a TIN to confirm validation works

---

> Next: [Naming Series](03-naming-series.md)
