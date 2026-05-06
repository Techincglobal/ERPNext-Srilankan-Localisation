# ERPNext Sri Lankan Localisation

Sri Lankan localisation for ERPNext, built and maintained by [TechInc Global](https://techincglobal.com).

---

## Features

- **Sri Lanka Chart of Accounts** — automatically applied when a Sri Lankan company is created via the setup wizard
- **VAT & SSCL tax templates** — sales and purchase templates for 18% VAT, 2.5% SSCL, SVAT, and non-VAT transactions
- **WHT tax categories** — seven Withholding Tax categories (interest, service fees, rent, royalties, dividends) linked automatically to the WHT Payable account
- **Custom fields** — TIN, BRC No, and VAT/SSCL registration fields on Company, Customer, Supplier, Sales Invoice, and Purchase Invoice
- **Tax Invoice print format** — IRD-compliant layout with supplier/purchaser TIN, address, tax breakdown, and WHT deduction section
- **Naming series variables** — `TYY` (two-digit year) and `MMM` (three-letter month) for date-stamped invoice serials
- **LK Tax Settings** — configurable validation to enforce customer TIN on invoice submission
- **Payment methods** — Credit/Debit Card, Mobile Payment, and Online Payment created on install

---

## Requirements

- ERPNext v15

## Installation

```bash
bench get-app https://github.com/Techincglobal/erpnext_srilankan_localisation --branch develop
bench --site <your-site> install-app erpnext_srilankan_localisation
```

---

## Documentation

### Setup

| Guide | Description |
|---|---|
| [Installation](docs/setup/01-installation.md) | Full install steps and setup wizard walkthrough |
| [Company Setup](docs/setup/02-company-setup.md) | TIN, VAT, and SSCL fields on the company record |
| [Customer & Supplier Setup](docs/setup/03-customer-supplier-setup.md) | TIN and VAT fields on parties |

### Configuration

| Guide | Description |
|---|---|
| [Tax Templates](docs/configuration/01-tax-templates.md) | All VAT/SSCL tax templates explained |
| [WHT Categories](docs/configuration/05-wht-categories.md) | Withholding Tax categories and invoice usage |
| [LK Tax Settings](docs/configuration/02-lk-tax-settings.md) | TIN validation toggle |
| [Naming Series](docs/configuration/03-naming-series.md) | TYY and MMM custom series variables |
| [Currency & Rounding](docs/configuration/04-currency-rounding.md) | Removing cent values for LKR |

---

## Contributing

This app uses `pre-commit` for code formatting and linting:

```bash
cd apps/erpnext_srilankan_localisation
pre-commit install
```

Tools: **ruff** (Python), **eslint** + **prettier** (JS/CSS), **pyupgrade**

## License

MIT
