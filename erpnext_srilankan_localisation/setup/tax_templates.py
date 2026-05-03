import frappe
from frappe.desk.page.setup_wizard.setup_wizard import make_records

TAX_CATEGORIES = [
	"Sales VAT 18%",
	"Purchase VAT 18%",
	"Sales VAT + SSCL",
	"Purchase VAT + SSCL",
	"Non VAT",
	"NON VAT - Purchase",
	"VAT Exempt",
	"SVAT",
	"SSCL",
	"SUSPENDED TAX",
	"TAX INVOICE",
]


def create_sri_lanka_tax_setup(company: str):
	abbr = frappe.get_cached_value("Company", company, "abbr")

	create_tax_categories()

	if not _has_required_accounts(company):
		return

	create_sales_tax_templates(company, abbr)
	create_purchase_tax_templates(company, abbr)


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


def create_sales_tax_templates(company: str, abbr: str):
	vat_payable = _get_account("VAT Payable", company)
	sscl_payable = _get_account("SSCL Payable", company)
	svat_suspense = _get_account("SVAT Suspense", company)

	templates = [
		{
			"title": f"Sales VAT 18% - {abbr}",
			"tax_category": "Sales VAT 18%",
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
			"title": f"Sales VAT + SSCL - {abbr}",
			"tax_category": "Sales VAT + SSCL",
			"taxes": [
				{
					"charge_type": "On Net Total",
					"account_head": sscl_payable,
					"rate": 2.5,
					"description": "SSCL 2.5%",
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
			"title": f"SSCL - {abbr}",
			"tax_category": "SSCL",
			"taxes": [
				{
					"charge_type": "On Net Total",
					"account_head": sscl_payable,
					"rate": 2.5,
					"description": "SSCL 2.5%",
				}
			],
		},
		{
			"title": f"SVAT - {abbr}",
			"tax_category": "SVAT",
			"taxes": [
				{
					"charge_type": "On Net Total",
					"account_head": svat_suspense,
					"rate": 18.0,
					"description": "SVAT Suspense",
					"included_in_print_rate": 1,
				}
			],
		},
		{
			"title": f"SUSPENDED TAX - {abbr}",
			"tax_category": "SUSPENDED TAX",
			"taxes": [
				{
					"charge_type": "On Net Total",
					"account_head": vat_payable,
					"rate": 18.0,
					"description": "Suspended Tax",
				}
			],
		},
		{
			"title": f"TAX INVOICE - {abbr}",
			"tax_category": "TAX INVOICE",
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
			"title": f"Non VAT Sales - {abbr}",
			"tax_category": "Non VAT",
			"taxes": [],
		},
		{
			"title": f"VAT Exempt Sales - {abbr}",
			"tax_category": "VAT Exempt",
			"taxes": [],
		},
	]

	_insert_sales_templates(templates, company)


def create_purchase_tax_templates(company: str, abbr: str):
	vat_receivable = _get_account("VAT Receivable", company)
	sscl_payable = _get_account("SSCL Payable", company)

	templates = [
		{
			"title": f"Purchase VAT 18% - {abbr}",
			"tax_category": "Purchase VAT 18%",
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
			"title": f"Purchase VAT + SSCL - {abbr}",
			"tax_category": "Purchase VAT + SSCL",
			"taxes": [
				{
					"charge_type": "On Net Total",
					"account_head": sscl_payable,
					"rate": 2.5,
					"description": "SSCL 2.5%",
				},
				{
					"charge_type": "On Previous Row Total",
					"account_head": vat_receivable,
					"rate": 18.0,
					"row_id": 1,
					"description": "VAT 18%",
				},
			],
		},
		{
			"title": f"Non VAT Purchase - {abbr}",
			"tax_category": "NON VAT - Purchase",
			"taxes": [],
		},
	]

	_insert_purchase_templates(templates, company)


def _insert_sales_templates(templates: list, company: str):
	for t in templates:
		if frappe.db.exists("Sales Taxes and Charges Template", t["title"]):
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
		).insert(ignore_permissions=True)


def _insert_purchase_templates(templates: list, company: str):
	for t in templates:
		if frappe.db.exists("Purchase Taxes and Charges Template", t["title"]):
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
		).insert(ignore_permissions=True)
