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
