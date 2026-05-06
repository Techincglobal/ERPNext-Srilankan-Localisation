# LK Tax Settings

**LK Tax Settings** is a single settings page that controls validation behaviour for Sri Lankan compliance. Access it by searching for **LK Tax Settings** in the desk search bar.

![LK Tax Settings page](../images/LK%20Tax%20Settings.png)

---

## Settings

### Enforce TIN on Tax Invoice Submission

| Value | Behaviour |
|---|---|
| **Off** (default) | Sales Invoices can be submitted without a customer TIN |
| **On** | Sales Invoices for Sri Lankan companies cannot be submitted unless the customer has a TIN on record |

When enabled, submitting a Sales Invoice without a customer TIN will show:

> *Customer TIN is required to submit a Tax Invoice. Add the TIN to the customer record first.*

---

## When to enable

Turn this on once your customer data is clean and TINs have been entered for all VAT-registered customers. Enabling it on a live system before TINs are populated will block invoice submission for those customers.

**Recommended workflow:**
1. Leave the setting off during initial data migration
2. Enter TINs on all VAT-registered customer records (see [Customer Setup](../setup/03-customer-supplier-setup.md))
3. Enable the validation once data is complete

---

> Next: [Naming Series](03-naming-series.md)
