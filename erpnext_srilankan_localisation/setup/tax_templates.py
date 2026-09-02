import frappe
from frappe.desk.page.setup_wizard.setup_wizard import make_records

TAX_CATEGORIES = [
	"Sales - VAT",
	"Sales - VAT + SSCL",
	"Sales - Non VAT",
	"Sales - SSCL",
	"Purchase - VAT",
	"Purchase - Non VAT",
]

SSCL_LIABLE_TURNOVER_PCT = {
	"Importation": 100,
	"Manufacturing": 85,
	"General Services": 100,
	"Registered Distributor": 25,
	"Other Wholesale or Retail": 50,
}
SSCL_STATUTORY_RATE = 2.5


def remove_erpnext_default_setup(company: str):
	"""
	Remove the generic Sri Lanka tax setup ERPNext auto-creates from country_wise_tax.json:
	  - 'Sri Lanka Tax' sales and purchase templates
	  - 'VAT' account (leaf, tax_rate=12)
	  - 'Duties and Taxes' group account (only if it has no remaining children)

	Templates are deleted first because they reference the VAT account.
	"""
	for doctype in ("Sales Taxes and Charges Template", "Purchase Taxes and Charges Template"):
		for name in frappe.get_all(doctype, filters={"company": company, "title": "Sri Lanka Tax"}, pluck="name"):
			frappe.delete_doc(doctype, name, ignore_permissions=True, force=True)

	vat_account = frappe.db.get_value(
		"Account",
		{"account_name": "VAT", "company": company, "tax_rate": 12, "is_group": 0},
		"name",
	)
	if vat_account:
		frappe.delete_doc("Account", vat_account, ignore_permissions=True, force=True)

	duties_account = frappe.db.get_value(
		"Account",
		{"account_name": "Duties and Taxes", "company": company, "is_group": 1},
		"name",
	)
	if duties_account and not frappe.db.exists("Account", {"parent_account": duties_account}):
		frappe.delete_doc("Account", duties_account, ignore_permissions=True, force=True)


def create_sri_lanka_tax_setup(company: str) -> bool:
	"""One-time base setup: VAT and Non-VAT tax categories/templates.

	Returns True once this has actually completed (the company has the LK
	chart of accounts) - the caller uses this to mark the company as done so
	a later, unrelated save of the company doesn't re-run this and resurrect
	a template/category the user deliberately deleted. SSCL templates are
	handled separately (see sync_sscl_sales_templates) since SSCL
	registration/category can genuinely change after this has run once.
	"""
	abbr = frappe.get_cached_value("Company", company, "abbr")

	create_tax_categories()

	if not _has_required_accounts(company):
		return False

	remove_erpnext_default_setup(company)
	create_sales_tax_templates(company, abbr)
	create_purchase_tax_templates(company, abbr)
	return True


def _has_required_accounts(company: str) -> bool:
	"""Skip template setup if the company doesn't have the Sri Lankan COA."""
	return all(
		frappe.db.exists("Account", {"account_name": name, "company": company})
		for name in ["VAT Payable", "VAT Receivable"]
	)


def _get_account(account_name: str, company: str) -> str | None:
	return frappe.db.get_value("Account", {"account_name": account_name, "company": company}, "name")


def create_tax_categories():
	make_records([{"doctype": "Tax Category", "title": title} for title in TAX_CATEGORIES])


def _get_effective_sscl_rate(company: str) -> float | None:
	is_registered, category = frappe.db.get_value(
		"Company", company, ["lk_is_sscl_registered", "lk_sscl_business_category"]
	)
	if not is_registered or not category:
		return None

	liable_pct = SSCL_LIABLE_TURNOVER_PCT.get(category)
	if not liable_pct:
		return None

	return round(SSCL_STATUTORY_RATE * liable_pct / 100, 4)


def create_sales_tax_templates(company: str, abbr: str):
	"""Base sales templates only (VAT, Non VAT) - part of the one-time setup.
	SSCL templates are handled separately by sync_sscl_sales_templates.
	"""
	vat_payable = _get_account("VAT Payable", company)

	templates = [
		{
			"title": "Sales - VAT",
			"tax_category": "Sales - VAT",
			"taxes": [
				{
					"charge_type": "On Net Total",
					"account_head": vat_payable,
					"rate": 18.0,
					"description": "VAT 18%",
				}
			],
		},
		{
			"title": "Sales - Non VAT",
			"tax_category": "Sales - Non VAT",
			"taxes": [],
		},
	]

	_insert_sales_templates(templates, company)


def sync_sscl_sales_templates(company: str):
	"""Create the SSCL sales templates if the company is SSCL registered
	with a declared business category. Unlike create_sri_lanka_tax_setup,
	this is meant to be called on every Company save (not gated behind a
	one-time-setup flag), since SSCL registration/category can genuinely
	change after the company's base setup has already run once.
	"""
	sscl_rate = _get_effective_sscl_rate(company)
	if sscl_rate is None:
		return

	vat_payable = _get_account("VAT Payable", company)
	sscl_payable = _get_account("SSCL Payable", company)

	templates = [
		{
			"title": "Sales - VAT + SSCL",
			"tax_category": "Sales - VAT + SSCL",
			"taxes": [
				{
					"charge_type": "On Net Total",
					"account_head": sscl_payable,
					"rate": sscl_rate,
					"description": f"SSCL {sscl_rate}%",
				},
				{
					"charge_type": "On Previous Row Total",
					"account_head": vat_payable,
					"rate": 18.0,
					"row_id": 1,
					"description": "VAT 18%",
				},
			],
		},
		{
			"title": "Sales - SSCL",
			"tax_category": "Sales - SSCL",
			"taxes": [
				{
					"charge_type": "On Net Total",
					"account_head": sscl_payable,
					"rate": sscl_rate,
					"description": f"SSCL {sscl_rate}%",
				}
			],
		},
	]

	_insert_sales_templates(templates, company)


def create_purchase_tax_templates(company: str, abbr: str):
	vat_receivable = _get_account("VAT Receivable", company)

	templates = [
		{
			"title": "Purchase - VAT",
			"tax_category": "Purchase - VAT",
			"taxes": [
				{
					"charge_type": "On Net Total",
					"account_head": vat_receivable,
					"rate": 18.0,
					"description": "VAT 18%",
				}
			],
		},
		{
			"title": "Purchase - Non VAT",
			"tax_category": "Purchase - Non VAT",
			"taxes": [],
		},
	]

	_insert_purchase_templates(templates, company)


def _insert_sales_templates(templates: list, company: str):
	for t in templates:
		if frappe.db.exists("Sales Taxes and Charges Template", {"company": company, "title": t["title"]}):
			continue
		if not all(tax.get("account_head") for tax in t["taxes"]):
			continue
		frappe.get_doc(
			{
				"doctype": "Sales Taxes and Charges Template",
				"title": t["title"],
				"company": company,
				"tax_category": t["tax_category"],
				"taxes": [
					{
						"doctype": "Sales Taxes and Charges",
						"charge_type": tax["charge_type"],
						"account_head": tax["account_head"],
						"rate": tax["rate"],
						"description": tax.get("description"),
						"row_id": tax.get("row_id"),
						"included_in_print_rate": tax.get("included_in_print_rate", 0),
					}
					for tax in t["taxes"]
				],
			}
		).insert(ignore_permissions=True, ignore_if_duplicate=True)


def _insert_purchase_templates(templates: list, company: str):
	for t in templates:
		if frappe.db.exists("Purchase Taxes and Charges Template", {"company": company, "title": t["title"]}):
			continue
		if not all(tax.get("account_head") for tax in t["taxes"]):
			continue
		frappe.get_doc(
			{
				"doctype": "Purchase Taxes and Charges Template",
				"title": t["title"],
				"company": company,
				"tax_category": t["tax_category"],
				"taxes": [
					{
						"doctype": "Purchase Taxes and Charges",
						"charge_type": tax["charge_type"],
						"account_head": tax["account_head"],
						"rate": tax["rate"],
						"description": tax.get("description"),
						"row_id": tax.get("row_id"),
					}
					for tax in t["taxes"]
				],
			}
		).insert(ignore_permissions=True, ignore_if_duplicate=True)
