import frappe
from frappe import _


def validate_customer(doc, method=None):
	_validate_vat_fields(doc)
	if doc.customer_type != "Individual":
		_validate_business_tax_fields(doc)


def validate_supplier(doc, method=None):
	_validate_vat_fields(doc)
	if doc.supplier_type != "Individual":
		_validate_business_tax_fields(doc)


def _validate_vat_fields(doc):
	if not doc.get("lk_is_vat_registered"):
		return
	if not doc.get("lk_vat_no"):
		frappe.throw(_("VAT No is mandatory when VAT Registered is checked."))
	if not doc.get("lk_vat_registration_certificate"):
		frappe.throw(_("VAT Registration Certificate is mandatory when VAT Registered is checked."))


def _validate_business_tax_fields(doc):
	if not doc.get("lk_brc_no"):
		frappe.throw(_("BRC No is mandatory for a Company."))
	if not doc.get("lk_tin_no"):
		frappe.throw(_("TIN Registration No is mandatory for a Company."))
