# ERPNext Sri Lankan Localisation

Sri Lankan localisation for ERPNext, built and maintained by [TechInc Global](https://techincglobal.com).

---

## Features

- **Sri Lanka Chart of Accounts** — available during the ERPNext setup wizard when a Sri Lankan company is created
- **VAT, SSCL, and WHT setup** — sales and purchase tax templates, withholding tax categories, and supporting accounts for Sri Lankan transactions
- **Custom tax registration fields** — BRC No, TIN Registration No, VAT registration, and SSCL registration fields on Company, Customer, and Supplier
- **Invoice-level fetched tax data** — customer TIN and VAT No flow automatically into Sales Invoices
- **Tax Invoice print format** — Sri Lanka-oriented print format with supplier and purchaser tax details, SSCL, VAT, WHT deduction, and net payable
- **LK Tax Settings** — optional validation to enforce customer TIN before Sales Invoice submission
- **Naming series support** — custom `TYY` and `MMM` variables for date-based invoice numbering
- **Round-off support** — compatible with ERPNext rounded totals and company round-off account setup

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
| [Installation](docs/setup/01-installation.md) | Install steps and setup wizard flow |
| [Company Setup](docs/setup/02-company-setup.md) | Company tax registration and round-off account setup |
| [Customer & Supplier Setup](docs/setup/03-customer-supplier-setup.md) | Party tax registration fields and invoice field fetches |

### Configuration

| Guide | Description |
|---|---|
| [Tax Templates](docs/configuration/01-tax-templates.md) | Sales and purchase tax templates |
| [LK Tax Settings](docs/configuration/02-lk-tax-settings.md) | TIN validation toggle |
| [Naming Series](docs/configuration/03-naming-series.md) | TYY and MMM custom series variables |
| [Currency & Rounding](docs/configuration/04-currency-rounding.md) | Rounded totals and company round-off configuration |
| [WHT Categories](docs/configuration/05-wht-categories.md) | Withholding Tax categories and invoice usage |

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
