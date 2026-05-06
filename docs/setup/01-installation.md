# Installation

## Prerequisites

- ERPNext v15 bench environment
- `erpnext` app already installed on the site

## Steps

### 1. Get the app

```bash
bench get-app https://github.com/Techincglobal/erpnext_srilankan_localisation --branch develop
```

### 2. Install on your site

```bash
bench --site <your-site> install-app erpnext_srilankan_localisation
```

The install script will automatically:
- Copy the Sri Lanka Chart of Accounts into ERPNext
- Create custom fields on Company, Customer, Supplier, Sales Invoice, and Purchase Invoice
- Set up the Sri Lanka naming series on Sales Invoice
- Create standard payment methods (Credit/Debit Card, Mobile Payment, Online Payment)
- Create tax categories, tax templates, and WHT categories for any existing Sri Lankan companies

### 3. Run the setup wizard

If setting up a new site, run the ERPNext setup wizard and select **Sri Lanka** as the company country.

![Setup wizard — company setup page](../images/Setup%20wizard%20-%20company%20setup%20page.png)

Select **Sri Lanka** from the country dropdown:

![Setup wizard — Sri Lanka selected](../images/Setup%20wizard%20-%20Sri%20Lanka%20selected.png)

The Sri Lanka Chart of Accounts will be available automatically:

![Setup wizard — Sri Lanka Chart of Accounts visible](../images/Setup%20wizard%20-%20Sri%20Lanka%20CoA%20visible.png)

The app hooks into the wizard to:
- Remove ERPNext's generic "Sri Lanka Tax" account and template
- Create the full set of Sri Lankan tax templates automatically

### 4. For existing sites

If you are installing on a site that already has a Sri Lankan company, run migrate after install:

```bash
bench --site <your-site> migrate
```

This re-runs the full setup for all Sri Lankan companies found on the site — it is safe to run multiple times.

---

> Next: [Company Setup](02-company-setup.md)
