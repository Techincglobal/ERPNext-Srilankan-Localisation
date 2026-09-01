import re

import frappe
from frappe.model.naming import parse_naming_series
from frappe.utils import cint, getdate

# Doctypes known to have used YEARSEQ under the previous
# YEARSEQ-{doctype}[-RET]-{year} key scheme. Historical patches only ever
# touched Sales Invoice.
YEARSEQ_DOCTYPES = ["Sales Invoice"]
DATE_FIELDNAMES = ("posting_date", "transaction_date")
DATE_VARIABLE_TOKENS = {"YY", "MM", "DD", "YYYY", "JJJ", "WW", "timestamp", "TYY", "MMM", "TYYYY"}


def _new_key(doctype, naming_series, year, doc):
	parts = naming_series.split(".")
	scope_parts = [
		p for p in parts
		if p and p != "YEARSEQ" and not p.startswith("#") and p not in DATE_VARIABLE_TOKENS
	]
	scope = parse_naming_series(".".join(scope_parts), doc=doc) if scope_parts else ""
	key = f"YEARSEQ-{doctype}"
	if scope:
		key += f"-{scope}"
	return f"{key}-{year}"


def execute():
	"""Re-key YEARSEQ counters from YEARSEQ-{doctype}[-RET]-{year} to
	YEARSEQ-{doctype}[-{resolved naming series text}]-{year}.

	The key changed again: it's no longer derived from doc.doctype/
	doc.is_return, but from the naming series pattern's own non-date text,
	resolved the same way the visible prefix is (see utils/naming.py -
	_yearseq_key). Seeds each new key from the highest number actually found
	in a matching document's name (not from the old counter's stored value,
	which can already have drifted - see split_yearseq_counter_by_doctype
	for why), then drops the old doctype/return-scoped rows.
	"""
	for doctype in YEARSEQ_DOCTYPES:
		table = f"tab{doctype}"
		date_col = next((f for f in DATE_FIELDNAMES if frappe.db.has_column(doctype, f)), None)
		if not date_col:
			continue

		rows = frappe.db.sql(
			f"SELECT name, naming_series, `{date_col}` FROM `{table}` WHERE naming_series LIKE %s",  # noqa: S608
			("%YEARSEQ%",),
		)

		max_by_key = {}
		for doc_name, naming_series, date_value in rows:
			if not date_value:
				continue
			match = re.search(r"(\d+)$", doc_name)
			if not match:
				continue
			seq = cint(match.group(1))
			year = getdate(date_value).strftime("%Y")
			doc = frappe.db.get_value(doctype, doc_name, ["*"], as_dict=True)
			key = _new_key(doctype, naming_series, year, doc)
			max_by_key[key] = max(max_by_key.get(key, 0), seq)

		for key, max_seq in max_by_key.items():
			existing = frappe.db.sql("SELECT current FROM `tabSeries` WHERE name = %s", (key,))
			if existing:
				if existing[0][0] < max_seq:
					frappe.db.sql("UPDATE `tabSeries` SET current = %s WHERE name = %s", (max_seq, key))
			else:
				frappe.db.sql(
					"INSERT INTO `tabSeries` (name, current) VALUES (%s, %s)", (key, max_seq)
				)

	# Drop the now-obsolete doctype/return-scoped rows from the previous scheme.
	frappe.db.sql(
		r"DELETE FROM `tabSeries` WHERE name REGEXP '^YEARSEQ-(Sales Invoice|Purchase Order)(-RET)?-[0-9]{4}$'"
	)
