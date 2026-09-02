import frappe

from erpnext_srilankan_localisation.setup.tax_rules import sync_tax_rules
from erpnext_srilankan_localisation.setup.tax_templates import (
	create_purchase_tax_templates,
	create_sales_tax_templates,
	create_tax_categories,
	sync_sscl_sales_templates,
)

REQUIRED_ACCOUNTS = ["VAT Payable", "VAT Receivable"]


def execute():
	"""Provision the redesigned VAT/Non-VAT/SSCL tax setup for companies that
	were already set up before the SSCL/SVAT redesign.

	create_sri_lanka_tax_setup() only ever runs from Company.on_update(), and
	is gated behind lk_tax_setup_completed - a field that didn't exist before
	this redesign, so it defaults to falsy on every pre-existing company.
	The next real save of such a company would trigger the full
	create_sri_lanka_tax_setup() path anyway (including
	remove_erpnext_default_setup(), which unconditionally deletes ERPNext's
	generic "Sri Lanka Tax" template and default VAT/Duties accounts without
	checking whether anything references them) - deliberately left for that
	natural save to trigger, not for this patch to force.

	Only creates the new Tax Categories/templates - the same idempotent,
	name-based checks create_sales_tax_templates()/create_purchase_tax_templates()
	already use (new template titles like "Sales - VAT" don't collide with
	the old "Sales VAT 18%" naming, so this is purely additive). Retired
	SVAT/SUSPENDED TAX/Purchase VAT+SSCL templates and categories are left
	untouched.
	"""
	create_tax_categories()

	for company in frappe.get_all("Company", filters={"country": "Sri Lanka"}, pluck="name"):
		has_required_accounts = all(
			frappe.db.exists("Account", {"account_name": name, "company": company})
			for name in REQUIRED_ACCOUNTS
		)
		if not has_required_accounts:
			continue

		abbr = frappe.get_cached_value("Company", company, "abbr")
		create_sales_tax_templates(company, abbr)
		create_purchase_tax_templates(company, abbr)
		sync_sscl_sales_templates(company)
		sync_tax_rules(company)
