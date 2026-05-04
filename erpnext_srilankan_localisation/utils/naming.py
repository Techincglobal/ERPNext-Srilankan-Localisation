from frappe.model import naming as _frappe_naming

_original_parse_naming_series = _frappe_naming.parse_naming_series


def _extended_parse_naming_series(parts, doctype=None, doc=None):
	from frappe.utils import getdate, now_datetime

	if isinstance(parts, str):
		parts = parts.split(".")

	# Use posting_date from the document so backdated entries get the correct
	# month/year stamp. Fall back to today if the doctype has no posting_date.
	if doc and doc.get("posting_date"):
		ref_date = getdate(doc.posting_date)
	else:
		ref_date = now_datetime().date()

	yy = ref_date.strftime("%y")
	mmm = ref_date.strftime("%b").upper()

	# YY  → 2-digit year from posting_date
	# MMM → 3-letter month from posting_date (counter resets monthly)
	parts = [yy if p == "YY" else mmm if p == "MMM" else p for p in parts]

	return _original_parse_naming_series(parts, doctype=doctype, doc=doc)


def patch_naming_series():
	_frappe_naming.parse_naming_series = _extended_parse_naming_series
