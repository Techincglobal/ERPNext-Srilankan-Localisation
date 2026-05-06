import frappe
from frappe import _


def validate_sales_invoice(doc, method=None):
	settings = frappe.get_single("LK Tax Settings")
	if not settings.enforce_tin_validation:
		return

	if frappe.db.get_value("Company", doc.company, "country") != "Sri Lanka":
		return

	if not doc.lk_customer_tin_no:
		frappe.throw(
			_("Customer TIN is required to submit a Tax Invoice. Add the TIN to the customer record first."),
			title=_("Missing Customer TIN"),
		)
