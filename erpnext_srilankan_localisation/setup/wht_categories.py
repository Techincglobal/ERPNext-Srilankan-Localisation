import frappe

# Sri Lanka WHT categories (2024-25 rates).
# single_threshold is per-calendar-month per payee in LKR.
WHT_CATEGORIES = [
	{
		"name": "WHT - Interest 10%",
		"rate": 10.0,
		"single_threshold": 0,
		"cumulative_threshold": 0,
	},
	{
		"name": "WHT - Service Fees (Resident) 5%",
		"rate": 5.0,
		"single_threshold": 100000,
		"cumulative_threshold": 0,
	},
	{
		"name": "WHT - Rent (Resident) 10%",
		"rate": 10.0,
		"single_threshold": 100000,
		"cumulative_threshold": 0,
	},
	{
		"name": "WHT - Rent (Non-Resident) 14%",
		"rate": 14.0,
		"single_threshold": 0,
		"cumulative_threshold": 0,
	},
	{
		"name": "WHT - Service Fees (Non-Resident) 14%",
		"rate": 14.0,
		"single_threshold": 0,
		"cumulative_threshold": 0,
	},
	{
		"name": "WHT - Royalties 14%",
		"rate": 14.0,
		"single_threshold": 0,
		"cumulative_threshold": 0,
	},
	{
		"name": "WHT - Dividends 15%",
		"rate": 15.0,
		"single_threshold": 0,
		"cumulative_threshold": 0,
	},
]


def create_wht_categories():
	fiscal_years = frappe.get_all(
		"Fiscal Year",
		fields=["year_start_date", "year_end_date"],
	)

	sl_companies = frappe.get_all("Company", filters={"country": "Sri Lanka"}, pluck="name")
	wht_accounts = {
		company: frappe.db.get_value(
			"Account", {"account_name": "WHT Payable", "company": company}, "name"
		)
		for company in sl_companies
	}
	wht_accounts = {c: a for c, a in wht_accounts.items() if a}

	for cat in WHT_CATEGORIES:
		if not frappe.db.exists("Tax Withholding Category", cat["name"]):
			_create_wht_category(cat, fiscal_years, wht_accounts)
		else:
			_update_wht_category(cat, fiscal_years, wht_accounts)


def _create_wht_category(cat: dict, fiscal_years: list, wht_accounts: dict):
	if not fiscal_years or not wht_accounts:
		return

	doc = frappe.get_doc(
		{
			"doctype": "Tax Withholding Category",
			"name": cat["name"],
			"category_name": cat["name"],
		}
	)
	for fy in fiscal_years:
		doc.append(
			"rates",
			{
				"from_date": fy.year_start_date,
				"to_date": fy.year_end_date,
				"tax_withholding_rate": cat["rate"],
				"single_threshold": cat["single_threshold"],
				"cumulative_threshold": cat["cumulative_threshold"],
			},
		)
	for company, account in wht_accounts.items():
		doc.append("accounts", {"company": company, "account": account})
	doc.insert(ignore_permissions=True)


def _update_wht_category(cat: dict, fiscal_years: list, wht_accounts: dict):
	doc = frappe.get_doc("Tax Withholding Category", cat["name"])
	existing_ranges = {
		(str(row.from_date), str(row.to_date)) for row in doc.rates
	}
	existing_companies = {row.company for row in doc.accounts}
	changed = False

	for fy in fiscal_years:
		key = (str(fy.year_start_date), str(fy.year_end_date))
		if key not in existing_ranges:
			doc.append(
				"rates",
				{
					"from_date": fy.year_start_date,
					"to_date": fy.year_end_date,
					"tax_withholding_rate": cat["rate"],
					"single_threshold": cat["single_threshold"],
					"cumulative_threshold": cat["cumulative_threshold"],
				},
			)
			changed = True

	for company, account in wht_accounts.items():
		if company not in existing_companies:
			doc.append("accounts", {"company": company, "account": account})
			changed = True

	if changed:
		doc.save(ignore_permissions=True)
