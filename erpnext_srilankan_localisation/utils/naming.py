import frappe
from frappe.utils import getdate, now_datetime


def parse_naming_series_variable(doc, variable):
	"""Handler for custom naming series variables registered via naming_series_variables hook."""
	if doc and doc.get("posting_date"):
		ref_date = getdate(doc.posting_date)
	else:
		ref_date = now_datetime().date()

	if variable == "TYY":
		return ref_date.strftime("%y")

	if variable == "MMM":
		return ref_date.strftime("%b").upper()

	if variable == "TYYYY":
		return ref_date.strftime("%Y")


def autoname_with_annual_sequence(doc, method):
	"""Doc event handler for doctypes using TSEQ in their naming series.

	Series format example: TYYYY.MMM.-.TSEQ.#####
	  - Parts before TSEQ are resolved normally (TYY, TYYYY, MMM, literals)
	  - TSEQ uses a year-based counter that continues across all months
	  - ##### controls digit count — use ###### for 6 digits, etc.
	"""
	if not doc.naming_series or "TSEQ" not in doc.naming_series:
		return

	from frappe.model.naming import parse_naming_series

	parts = doc.naming_series.split(".")

	hash_part = next((p for p in parts if p.startswith("#")), "#####")
	digits = len(hash_part)

	if doc.get("posting_date"):
		ref_date = getdate(doc.posting_date)
	else:
		ref_date = now_datetime().date()

	prefix_parts = [p for p in parts if p != "TSEQ" and not p.startswith("#")]
	prefix = parse_naming_series(".".join(prefix_parts), doc=doc)

	doc.name = prefix + _get_annual_sequence(ref_date, digits)


def _get_annual_sequence(ref_date, digits=5):
	"""Atomically increment and return a zero-padded counter keyed by year.

	Counter resets each year, continues across all months within the year.
	"""
	key = f"TSEQ-{ref_date.strftime('%Y')}"
	current = frappe.db.sql(
		"SELECT current FROM `tabSeries` WHERE name = %s FOR UPDATE", (key,)
	)
	if current and current[0][0] is not None:
		new_val = current[0][0] + 1
		frappe.db.sql("UPDATE `tabSeries` SET current = %s WHERE name = %s", (new_val, key))
	else:
		new_val = 1
		frappe.db.sql("INSERT INTO `tabSeries` (name, current) VALUES (%s, 1)", (key,))
	return str(new_val).zfill(digits)
