import re

import frappe
from frappe.query_builder.functions import IfNull, Year
from frappe.utils import cint

# Doctypes wired up to use YEARSEQ in their naming series. Extend this list if
# YEARSEQ is registered (doc_events + a naming series option) on another doctype.
YEARSEQ_DOCTYPES = ["Sales Invoice"]


def execute():
	"""Split the old per-year YEARSEQ-{year} counter into counters scoped by
	doctype and return-flag: YEARSEQ-{doctype}[-RET]-{year}.

	The YEARSEQ counter key changed from "YEARSEQ-{year}" (shared by every
	document using it) to "YEARSEQ-{doctype}[-RET]-{year}" (independent per
	doctype, and per return/non-return for doctypes with an is_return flag).
	Without this, a site with an existing merged counter would have it
	silently ignored, and a fresh YEARSEQ-{doctype}-{year} counter would
	start at 0 - colliding with document names already issued under the
	old merged counter.

	Each new counter is seeded from the highest number actually found in a
	matching document's name, not from the old counter's stored value - the
	stored value can already have drifted from reality (e.g. an admin
	manually moved it, or a duplicate insert attempt was rolled back after
	incrementing).
	"""
	old_rows = frappe.db.sql(r"SELECT name FROM `tabSeries` WHERE name REGEXP '^YEARSEQ-[0-9]{4}$'")
	if not old_rows:
		return

	for (old_name,) in old_rows:
		year = old_name.split("-")[1]

		for doctype in YEARSEQ_DOCTYPES:
			has_is_return = frappe.db.has_column(doctype, "is_return")

			return_variants = [(1, "-RET"), (0, "")] if has_is_return else [(0, "")]
			for is_return, suffix in return_variants:
				DocTypeTable = frappe.qb.DocType(doctype)
				query = (
					frappe.qb.from_(DocTypeTable)
					.select(DocTypeTable.name)
					.where(DocTypeTable.naming_series.like("%YEARSEQ%"))
					.where(Year(DocTypeTable.posting_date) == year)
				)
				if has_is_return:
					query = query.where(IfNull(DocTypeTable.is_return, 0) == is_return)

				rows = query.run()

				max_seq = 0
				for (doc_name,) in rows:
					match = re.search(r"(\d+)$", doc_name)
					if match:
						max_seq = max(max_seq, cint(match.group(1)))

				if max_seq == 0:
					continue

				new_key = f"YEARSEQ-{doctype}{suffix}-{year}"
				existing = frappe.db.sql("SELECT current FROM `tabSeries` WHERE name = %s", (new_key,))
				if existing:
					if existing[0][0] < max_seq:
						frappe.db.sql(
							"UPDATE `tabSeries` SET current = %s WHERE name = %s", (max_seq, new_key)
						)
				else:
					frappe.db.sql(
						"INSERT INTO `tabSeries` (name, current) VALUES (%s, %s)", (new_key, max_seq)
					)

		frappe.db.sql("DELETE FROM `tabSeries` WHERE name = %s", (old_name,))
