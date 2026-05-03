from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

from erpnext_srilankan_localisation.setup.custom_fields import CUSTOM_FIELDS


def initial_setup():
    create_custom_fields(CUSTOM_FIELDS, update=True)
