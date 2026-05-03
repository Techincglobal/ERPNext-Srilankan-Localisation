import frappe

from erpnext_srilankan_localisation.setup.chart_of_accounts import remove_sri_lanka_chart_of_accounts
from erpnext_srilankan_localisation.setup.custom_fields import CUSTOM_FIELDS


def remove_setup():
    delete_custom_field(CUSTOM_FIELDS)
    remove_sri_lanka_chart_of_accounts()


def delete_custom_field(custom_fields):
    for doctypes, fields in custom_fields.items():
        if isinstance(fields, dict):
            fields = [fields]

        if isinstance(doctypes, str):
            doctypes = (doctypes,)

        for doctype in doctypes:
            frappe.db.delete(
                "Custom Field",
                {
                    "fieldname": ("in", [field["fieldname"] for field in fields]),
                    "dt": doctype,
                },
            )
            frappe.clear_cache(doctype=doctype)
