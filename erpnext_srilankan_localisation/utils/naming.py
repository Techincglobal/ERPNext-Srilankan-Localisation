import re

import frappe
from frappe import _
from frappe.model.naming import getseries
from frappe.utils import cint, getdate, now_datetime

MONTH_CODES = (
	"JAN", "FEB", "MAR", "APR", "MAY", "JUN",
	"JUL", "AUG", "SEP", "OCT", "NOV", "DEC",
)

# Fieldnames ERPNext uses for a document's transaction date, checked in order.
# Sales/Purchase Invoice, Delivery Note etc. use posting_date; Purchase Order,
# Sales Order etc. use transaction_date.
DATE_FIELDNAMES = ("posting_date", "transaction_date")


def _get_reference_date(doc):
	"""Resolve the document's own transaction date, whatever it's called on
	this doctype. Falls back to today when doc is None or has neither field
	(e.g. when Frappe resolves a naming series preview with no document).
	"""
	if doc:
		for fieldname in DATE_FIELDNAMES:
			value = doc.get(fieldname)
			if value:
				return getdate(value)
	return now_datetime().date()



# Date-variable tokens excluded when building the YEARSEQ counter key - these
# must vary every month/day for the naming series to make sense, so they'd
# defeat the annual counter if included in its key.
DATE_VARIABLE_TOKENS = {"YY", "MM", "DD", "YYYY", "JJJ", "WW", "timestamp", "TYY", "MMM", "TYYYY"}


def _yearseq_key(doc, naming_series, ref_date):
	"""Counter key built from the naming series' own non-date-variable parts,
	resolved the same way the visible prefix is - not from doc.company or
	doc.is_return.

	A literal segment (e.g. "CR-" for credit notes, or a company code) or a
	field placeholder (e.g. "{abbr}", resolved from the document's own
	company) both automatically separate the counter exactly in step with
	whatever separates the visible name - because if two series resolve to
	the same visible prefix they must share a counter anyway (they'd collide
	on insert otherwise), and if they resolve differently they get
	independent counters for free. No assumption about which fields exist on
	a given doctype, and no naming series options to maintain per company -
	one series with "{abbr}" in it already scales to every company.
	"""
	from frappe.model.naming import parse_naming_series

	parts = naming_series.split(".")
	scope_parts = [
		p for p in parts
		if p and p != "YEARSEQ" and not p.startswith("#") and p not in DATE_VARIABLE_TOKENS
	]
	scope = parse_naming_series(".".join(scope_parts), doc=doc) if scope_parts else ""

	key = f"YEARSEQ-{doc.doctype}"
	if scope:
		key += f"-{scope}"
	key += f"-{ref_date.strftime('%Y')}"

	# Collapse runs of "-" into one - the naming series' own literal dashes
	# (used as visible separators, e.g. around {company}) combined with the
	# dashes this function inserts between doctype/scope/year otherwise stack
	# up into confusing double dashes in the resulting Series/key name.
	return re.sub(r"-{2,}", "-", key)


def parse_naming_series_variable(doc, variable):
	"""Handler for custom naming series variables registered via naming_series_variables hook."""
	ref_date = _get_reference_date(doc)

	if variable == "TYY":
		return ref_date.strftime("%y")

	if variable == "MMM":
		return MONTH_CODES[ref_date.month - 1]

	if variable == "TYYYY":
		return ref_date.strftime("%Y")


def autoname_with_annual_sequence(doc, method):
	"""Doc event handler for doctypes using YEARSEQ in their naming series.

	Series format example: TYYYY.MMM.-.YEARSEQ.#####
	  - Parts before YEARSEQ are resolved normally (TYY, TYYYY, MMM, literals,
	    field placeholders like {abbr})
	  - YEARSEQ uses a counter scoped by doctype and by the naming series'
	    own non-date text (see _yearseq_key), that continues across all
	    months within the year
	  - ##### controls digit count — use ###### for 6 digits, etc.
	"""
	naming_series = doc.get("naming_series")
	if not naming_series or "YEARSEQ" not in naming_series:
		return

	from frappe.model.naming import parse_naming_series

	parts = naming_series.split(".")

	hash_part = next((p for p in parts if p.startswith("#")), "#####")
	digits = len(hash_part)

	ref_date = _get_reference_date(doc)

	prefix_parts = [p for p in parts if p != "YEARSEQ" and not p.startswith("#")]
	prefix = parse_naming_series(".".join(prefix_parts), doc=doc)

	doc.name = prefix + getseries(_yearseq_key(doc, naming_series, ref_date), digits)


def revert_annual_sequence_on_delete(doc, method):
	"""on_trash handler: revert the YEARSEQ counter when a draft holding the
	most recently allocated number is deleted.

	Only reverts for drafts (docstatus 0) and only when the deleted document's
	number matches the counter's current value — mirrors the safety check
	core Frappe uses for ordinary naming series (see revert_series_if_last),
	so deleting an older/unrelated draft can never desync the counter.
	Cancelled or submitted documents are never reverted: a legally issued
	number stays retired even if the document is later voided.
	"""
	if doc.docstatus != 0:
		return
	naming_series = doc.get("naming_series")
	if not naming_series or "YEARSEQ" not in naming_series:
		return

	parts = naming_series.split(".")
	hash_part = next((p for p in parts if p.startswith("#")), "#####")
	digits = len(hash_part)
	count = cint(doc.name[-digits:])

	ref_date = _get_reference_date(doc)
	key = _yearseq_key(doc, naming_series, ref_date)

	current = frappe.db.sql("SELECT current FROM `tabSeries` WHERE name = %s FOR UPDATE", (key,))
	if current and current[0][0] == count:
		frappe.db.sql("UPDATE `tabSeries` SET current = current - 1 WHERE name = %s", (key,))


def validate_posting_date_locked(doc, method):
	"""Block transaction-date edits that would cross a month/year boundary
	after the legal document number (embedded in doc.name via YEARSEQ) has
	been allocated.
	"""
	naming_series = doc.get("naming_series")
	if doc.is_new() or not naming_series or "YEARSEQ" not in naming_series:
		return

	before_save = doc.get_doc_before_save()
	if not before_save:
		return

	old_date = _get_reference_date(before_save)
	new_date = _get_reference_date(doc)

	if (old_date.year, old_date.month) != (new_date.year, new_date.month):
		frappe.throw(
			_(
				"Transaction date cannot be moved to a different month or year once the "
				"document number {0} has been generated. Cancel and amend the document instead."
			).format(doc.name)
		)
