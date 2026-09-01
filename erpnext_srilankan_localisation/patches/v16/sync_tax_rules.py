import frappe

from erpnext_srilankan_localisation.setup.tax_rules import sync_tax_rules


def execute():
	for company in frappe.get_all("Company", filters={"country": "Sri Lanka"}, pluck="name"):
		sync_tax_rules(company)
