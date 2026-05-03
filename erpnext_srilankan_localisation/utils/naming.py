from frappe.model import naming as _frappe_naming

_original_parse_naming_series = _frappe_naming.parse_naming_series

# Fixed placeholder used as the counter key in tabSeries for MMMYC.
# The month is substituted into the final name AFTER the counter is generated,
# so the counter prefix stays constant for the whole year.
_MMMYC_PLACEHOLDER = "__LK_MMMYC__"


def _extended_parse_naming_series(parts, doctype=None, doc=None):
	from frappe.utils import now_datetime

	if isinstance(parts, str):
		parts = parts.split(".")

	mmm = now_datetime().strftime("%b").upper()
	has_mmmyc = "MMMYC" in parts

	# MMM   → month in name, counter key includes month (resets monthly)
	# MMMYC → month in name, counter key excludes month (resets yearly only)
	parts = [mmm if p == "MMM" else _MMMYC_PLACEHOLDER if p == "MMMYC" else p for p in parts]

	result = _original_parse_naming_series(parts, doctype=doctype, doc=doc)

	if has_mmmyc:
		result = result.replace(_MMMYC_PLACEHOLDER, mmm)

	return result


def patch_naming_series():
	_frappe_naming.parse_naming_series = _extended_parse_naming_series
