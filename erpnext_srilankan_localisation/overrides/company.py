import frappe

from erpnext_srilankan_localisation.setup.tax_rules import sync_tax_rules
from erpnext_srilankan_localisation.setup.tax_templates import create_sri_lanka_tax_setup, sync_sscl_sales_templates
from erpnext_srilankan_localisation.setup.wht_categories import create_wht_categories


def on_update(doc, method=None):
	if doc.country != "Sri Lanka":
		return

	if not doc.get("lk_tax_setup_completed"):
		if create_sri_lanka_tax_setup(doc.name):
			create_wht_categories()
			frappe.db.set_value("Company", doc.name, "lk_tax_setup_completed", 1)

	sync_sscl_sales_templates(doc.name)
	sync_tax_rules(doc.name)
