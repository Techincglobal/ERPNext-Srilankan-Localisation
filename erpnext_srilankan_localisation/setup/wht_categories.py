import frappe

FAR_FUTURE = "2099-12-31"

WHT_CATEGORIES = [
	{
		"name": "WHT - Interest or Discount",
		"rates": [
			{"from_date": "2023-01-01", "to_date": "2025-03-31", "rate": 5.0},
			{"from_date": "2025-04-01", "to_date": FAR_FUTURE, "rate": 10.0},
		],
	},
	{
		"name": "WHT - Service Fees (Resident Individual)",
		"rates": [
			{"from_date": "2023-01-01", "to_date": FAR_FUTURE, "rate": 5.0, "single_threshold": 100000},
		],
	},
	{
		"name": "WHT - Rent (Resident)",
		"rates": [
			{"from_date": "2023-01-01", "to_date": FAR_FUTURE, "rate": 10.0, "single_threshold": 100000},
		],
	},
	{
		"name": "WHT - Rent (Non-Resident)",
		"rates": [{"from_date": "2023-01-01", "to_date": FAR_FUTURE, "rate": 14.0}],
	},
	{
		"name": "WHT - Service Fees or Insurance Premium (Non-Resident)",
		"rates": [{"from_date": "2023-01-01", "to_date": FAR_FUTURE, "rate": 14.0}],
	},
	{
		"name": "WHT - Royalty",
		"rates": [{"from_date": "2023-01-01", "to_date": FAR_FUTURE, "rate": 14.0}],
	},
	{
		"name": "WHT - Dividend",
		"rates": [{"from_date": "2023-01-01", "to_date": FAR_FUTURE, "rate": 15.0}],
	},
	{
		"name": "WHT - Charge, Natural Resource Payment or Premium",
		"rates": [{"from_date": "2023-01-01", "to_date": FAR_FUTURE, "rate": 14.0}],
	},
	{
		"name": "WHT - Non-Resident Transport or Telecom Service",
		"rates": [{"from_date": "2023-01-01", "to_date": FAR_FUTURE, "rate": 2.0}],
	},
]


def create_wht_categories():
	sl_companies = frappe.get_all("Company", filters={"country": "Sri Lanka"}, pluck="name")

	wht_accounts = {
		company: frappe.db.get_value(
			"Account", {"account_name": "WHT Payable", "company": company}, "name"
		)
		for company in sl_companies
	}
	wht_accounts = {company: account for company, account in wht_accounts.items() if account}

	for category in WHT_CATEGORIES:
		_sync_wht_category(category, wht_accounts)


def _sync_wht_category(category: dict, wht_accounts: dict):
	name = category["name"]
	exists = frappe.db.exists("Tax Withholding Category", name)

	if not exists and not wht_accounts:
		# accounts is a mandatory child table - nothing to create yet since
		# no Sri Lankan company has a WHT Payable account. Company.on_update()
		# will call this again once one exists.
		return

	if exists:
		doc = frappe.get_doc("Tax Withholding Category", name)
	else:
		doc = frappe.new_doc("Tax Withholding Category")
		doc.name = name
		doc.category_name = name

	_sync_rates(doc, category["rates"])
	_sync_accounts(doc, wht_accounts)

	if doc.is_new():
		doc.insert(ignore_permissions=True)
	else:
		doc.save(ignore_permissions=True)


def _sync_rates(doc, configured_rates: list):
	existing = {(str(row.from_date), str(row.to_date)): row for row in doc.rates}

	for rate in configured_rates:
		key = (rate["from_date"], rate["to_date"])
		if key in existing:
			row = existing[key]
			row.tax_withholding_rate = rate["rate"]
			row.single_threshold = rate.get("single_threshold", 0)
			row.cumulative_threshold = rate.get("cumulative_threshold", 0)
		else:
			doc.append(
				"rates",
				{
					"from_date": rate["from_date"],
					"to_date": rate["to_date"],
					"tax_withholding_rate": rate["rate"],
					"single_threshold": rate.get("single_threshold", 0),
					"cumulative_threshold": rate.get("cumulative_threshold", 0),
				},
			)


def _sync_accounts(doc, wht_accounts: dict):
	existing = {row.company: row for row in doc.accounts}

	for company, account in wht_accounts.items():
		if company in existing:
			existing[company].account = account
		else:
			doc.append("accounts", {"company": company, "account": account})
