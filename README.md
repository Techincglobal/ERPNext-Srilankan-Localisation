# ERPNext Sri Lankan Localisation

Sri Lankan localisation for ERPNext, built and maintained by [TechInc Global](https://techincglobal.com).

## Features

### Chart of Accounts
A Sri Lanka-specific chart of accounts is included and automatically applied when a new company with country **Sri Lanka** is created.

### Tax Setup
Tax categories and tax templates are created automatically for each Sri Lankan company:

**Sales templates**
- Sales VAT 18%
- Sales VAT + SSCL (2.5% SSCL on net + 18% VAT on SSCL-inclusive total)
- SSCL
- SVAT
- Suspended Tax
- Tax Invoice
- Non VAT Sales
- VAT Exempt Sales

**Purchase templates**
- Purchase VAT 18%
- Purchase VAT + SSCL
- Non VAT Purchase

### Custom Fields

**Company**
- BRC No
- TIN Registration No
- VAT Registered / VAT No / VAT Registration Certificate
- SSCL Registered / SSCL Registration No

**Customer & Supplier**
- BRC No
- TIN Registration No
- VAT Registered / VAT No / VAT Registration Certificate

**Sales Invoice**
- Mode of Payment (`lk_mode_of_payment`)
- Customer TIN No (fetched from Customer)
- Customer VAT No (fetched from Customer)

**Purchase Invoice**
- Supplier TIN No (fetched from Supplier)
- Supplier VAT No (fetched from Supplier)

### Payment Methods
The following modes of payment are created on install:
- Credit/Debit Card
- Mobile Payment
- Online Payment

### Naming Series Variables
Two custom naming series variables are available for use in document naming:

| Variable | Output | Example |
|----------|--------|---------|
| `TYY` | Two-digit fiscal year (from posting date) | `26` |
| `MMM` | Three-letter month abbreviation (from posting date) | `JAN` |

Example series: `SINV-TYY-MMM-.####` → `SINV-26-JAN-0001`

### Print Format
A **Tax Invoice - LK** print format for Sales Invoice is included, compliant with Sri Lankan tax invoice requirements. It displays supplier and purchaser TIN numbers, VAT details, and itemised amounts.

## Requirements

- ERPNext

## Installation

```bash
cd $PATH_TO_YOUR_BENCH
bench get-app $URL_OF_THIS_REPO --branch develop
bench install-app erpnext_srilankan_localisation
```

## Contributing

This app uses `pre-commit` for code formatting and linting. Install and enable it before contributing:

```bash
cd apps/erpnext_srilankan_localisation
pre-commit install
```

Tools configured:
- **ruff** — Python linting and formatting
- **eslint** — JavaScript linting
- **prettier** — JavaScript/CSS formatting
- **pyupgrade** — Python syntax upgrades

## License

MIT
