import frappe

from erpnext_srilankan_localisation.setup.chart_of_accounts import remove_sri_lanka_chart_of_accounts
from erpnext_srilankan_localisation.setup.custom_fields import CUSTOM_FIELDS
from erpnext_srilankan_localisation.setup.property_setters import PROPERTIES


def remove_setup():
	delete_custom_field(CUSTOM_FIELDS)
	delete_property_setters(PROPERTIES)
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


def delete_property_setters(properties):
	field_map = {
		"doctype": "doc_type",
		"fieldname": "field_name",
	}

	for prop in properties:
		filters = {}
		for key, db_field in field_map.items():
			if key in prop:
				filters[db_field] = prop[key]
		if "property" in prop:
			filters["property"] = prop["property"]

		frappe.db.delete("Property Setter", filters)
