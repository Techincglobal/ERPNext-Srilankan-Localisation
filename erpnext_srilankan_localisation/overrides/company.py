import frappe
from frappe import _

from erpnext_srilankan_localisation.setup.tax_templates import create_sri_lanka_tax_setup

def after_insert(doc, method=None):
	if doc.country == "Sri Lanka":
		create_sri_lanka_tax_setup(doc.name)
