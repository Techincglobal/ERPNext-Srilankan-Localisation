# Customer & Supplier Setup

Both Customer and Supplier records have a **Tax Registration** section added by the app. These fields feed into invoices and the Tax Invoice print format automatically.

---

## Customer

![Customer — Tax Registration section](../images/Customer%20tax%20registration.png)

### Fields

| Field | Visible when | Description |
|---|---|---|
| **BRC No** | Customer Type is not Individual | Business Registration Certificate number |
| **TIN Registration No** | Customer Type is not Individual | IRD-issued TIN |
| **VAT Registered** | Always | Tick if the customer is VAT registered |
| **VAT No** | VAT Registered is ticked | Customer's VAT registration number |
| **VAT Registration Certificate** | VAT Registered is ticked | Attach IRD certificate (optional) |

### How to fill in

1. Open the Customer record
2. Scroll to the **Tax Registration** section
3. Enter **BRC No** and **TIN Registration No** for non-individual customers
4. If the customer is VAT registered, tick **VAT Registered** and enter the **VAT No**
5. Save

Once saved, these fields are automatically pulled through to Sales Invoices as read-only fetched fields:

![Sales Invoice — Customer TIN and VAT No fetched](../images/Submitted%20Sales%20Invoice%20with%20Tin%20No%20and%20Vat%20No.png)

---

## Supplier

The Supplier form has the same Tax Registration fields.

![Supplier — Tax Registration section](../images/Supplier%20tax%20registration.png)

The Supplier TIN and VAT No are automatically pulled through to Purchase Invoices.

---

> Next: [Tax Templates](../configuration/01-tax-templates.md)
