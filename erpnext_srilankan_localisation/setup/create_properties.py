import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

from erpnext_srilankan_localisation.setup.custom_fields import CUSTOM_FIELDS
from erpnext_srilankan_localisation.setup.property_setters import PROPERTIES


def initial_setup():
	create_custom_fields(CUSTOM_FIELDS, update=True)
	create_property_setters(PROPERTIES)


def create_property_setters(properties):
	for prop in properties:
		if prop.get("property") == "options" and "\n" in (prop.get("value") or ""):
			prop = _merge_with_existing_options(prop)
		elif _property_setter_exists(prop):
			# A single-value property (e.g. naming_series' "default") can't be
			# merged like a list. Leave it alone if it's already set - on a
			# site that already had its own choice before this app touched
			# it, re-running setup shouldn't silently override that choice.
			continue

		frappe.make_property_setter(
			prop,
			validate_fields_for_doctype=False,
			is_system_generated=prop.get("is_system_generated", True),
		)


def _property_setter_exists(prop):
	return bool(
		frappe.db.exists(
			"Property Setter",
			{
				"doc_type": prop.get("doctype"),
				"field_name": prop.get("fieldname"),
				"property": prop.get("property"),
			},
		)
	)


def _merge_with_existing_options(prop):
	"""For a multi-line "options" property (e.g. naming_series), add this
	app's required lines to whatever is already there instead of replacing
	the whole list - make_property_setter fully overwrites the property
	otherwise, silently discarding any option added by hand through
	Customize Form.

	Reads the field's current *effective* options via its meta, not just the
	Property Setter table directly - a doctype's options can come baked into
	its own JSON (e.g. Sales Invoice ships "ACC-SINV-.YYYY.-\\nACC-SINV-RET-
	.YYYY.-" natively, no Property Setter involved). On a fresh site with no
	Property Setter yet, querying the table directly would miss that native
	value entirely and let our own list silently replace it.
	"""
	field = frappe.get_meta(prop.get("doctype"), cached=False).get_field(prop.get("fieldname"))
	existing_value = field.options if field else None
	if not existing_value:
		return prop

	existing_lines = [line for line in existing_value.split("\n") if line]
	required_lines = [line for line in prop["value"].split("\n") if line]
	merged_lines = existing_lines + [line for line in required_lines if line not in existing_lines]

	return {**prop, "value": "\n".join(merged_lines)}
