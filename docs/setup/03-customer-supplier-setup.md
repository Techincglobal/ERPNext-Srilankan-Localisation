# Customer & Supplier Setup

The app adds a **Tax Registration** section to both Customer and Supplier. These fields support tax invoices and invoice-level fetched data.

---

## Customer

![Customer — Tax Registration section](../images/Customer%20tax%20registration.png)

### Fields

| Field | Description |
|---|---|
| **BRC No** | Business Registration Certificate number |
| **TIN Registration No** | Customer TIN |
| **VAT Registered** | Marks the customer as VAT registered |
| **VAT No** | Customer VAT registration number |
| **VAT Registration Certificate** | Optional supporting attachment |

### Invoice usage

The customer TIN and VAT No flow automatically into Sales Invoices as read-only fetched values.

![Sales Invoice — Customer TIN and VAT No fetched](../images/Submitted%20Sales%20Invoice%20with%20Tin%20No%20and%20Vat%20No.png)

---

## Supplier

![Supplier — Tax Registration section](../images/Supplier%20tax%20registration.png)

The Supplier form includes the same tax registration fields for:
- BRC No
- TIN Registration No
- VAT Registered
- VAT No
- VAT Registration Certificate

These can be used later on Purchase Invoices and purchase-side compliance workflows.

---

## Recommended setup order

1. Create or clean the Company record
2. Enter Customer tax registration details
3. Enter Supplier tax registration details
4. Test Sales Invoice creation with fetched customer tax data
5. Test print format output

---

> Next: [Tax Templates](../configuration/01-tax-templates.md)
