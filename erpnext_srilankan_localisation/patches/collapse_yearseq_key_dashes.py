import re

import frappe


def execute():
	"""Collapse double/multiple dashes in existing YEARSEQ-* Series keys.

	_yearseq_key now collapses runs of "-" into one (a naming series' own
	literal dashes, e.g. around a {company} placeholder, combined with the
	dashes the function inserts between doctype/scope/year, were stacking up
	into confusing names like "YEARSEQ-Sales Invoice--APIT (Demo)--2026" in
	Document Naming Settings). Rename existing rows the same way, merging
	(keeping the higher value) if the cleaned-up name already exists.
	"""
	rows = frappe.db.sql(r"SELECT name, current FROM `tabSeries` WHERE name LIKE 'YEARSEQ-%'")

	for old_name, current in rows:
		new_name = re.sub(r"-{2,}", "-", old_name)
		if new_name == old_name:
			continue

		existing = frappe.db.sql("SELECT current FROM `tabSeries` WHERE name = %s", (new_name,))
		if existing:
			if existing[0][0] < current:
				frappe.db.sql("UPDATE `tabSeries` SET current = %s WHERE name = %s", (current, new_name))
			frappe.db.sql("DELETE FROM `tabSeries` WHERE name = %s", (old_name,))
		else:
			frappe.db.sql("UPDATE `tabSeries` SET name = %s WHERE name = %s", (new_name, old_name))
