import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

from erpnext_srilankan_localisation.setup.custom_fields import CUSTOM_FIELDS
from erpnext_srilankan_localisation.setup.property_setters import PROPERTIES


def initial_setup():
	create_custom_fields(CUSTOM_FIELDS, update=True)
	create_property_setters(PROPERTIES)


def create_property_setters(properties):
	for prop in properties:
		frappe.make_property_setter(
			prop,
			validate_fields_for_doctype=False,
			is_system_generated=prop.get("is_system_generated", True),
		)
