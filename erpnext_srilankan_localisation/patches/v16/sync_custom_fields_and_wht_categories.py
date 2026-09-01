from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

from erpnext_srilankan_localisation.setup.custom_fields import CUSTOM_FIELDS
from erpnext_srilankan_localisation.setup.wht_categories import create_wht_categories


def execute():
	create_custom_fields(CUSTOM_FIELDS, update=True)
	create_wht_categories()
