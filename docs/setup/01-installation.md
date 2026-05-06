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

The install flow sets up:
- Sri Lanka chart of accounts support
- custom fields on Company, Customer, and Supplier
- fetched invoice fields for customer TIN and VAT
- tax categories
- sales and purchase tax templates
- LK Tax Settings
- naming series support
- withholding tax categories

### 3. Run the setup wizard for a new site

When creating a new site, select **Sri Lanka** in the setup wizard.

![Setup wizard — Sri Lanka selected](../images/Setup%20wizard%20-%20Sri%20Lanka%20selected.png)

During company setup, select the **Sri Lanka - Standard Chart of Accounts**.

![Setup wizard — Sri Lanka Chart of Accounts visible](../images/Setup%20wizard%20-%20Sri%20Lanka%20CoA%20visible.png)

![Setup wizard — company setup page](../images/Setup%20wizard%20-%20company%20setup%20page.png)

### 4. Existing sites

If you install on an existing Sri Lankan site, run migrate after install:

```bash
bench --site <your-site> migrate
```

This is useful when you need setup patches and fixtures to be applied again safely.

---

> Next: [Company Setup](02-company-setup.md)
