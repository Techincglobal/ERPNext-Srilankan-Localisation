# Copyright (c) 2026, servers@techincglobal.com and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
    filters = filters or {}
    _validate(filters)
    return _get_columns(), _get_data(filters)


def _validate(filters):
    if not filters.get("company"):
        frappe.throw(_("Please select a Company"))
    if not filters.get("from_date") or not filters.get("to_date"):
        frappe.throw(_("Please select a date range"))
    if filters["from_date"] > filters["to_date"]:
        frappe.throw(_("From Date cannot be after To Date"))


def _get_columns():
    return [
        {
            "label": _("Serial No"),
            "fieldname": "serial_no",
            "fieldtype": "Data",
            "width": 80,
        },
        {
            "label": _("Invoice Date"),
            "fieldname": "posting_date",
            "fieldtype": "Date",
            "width": 110,
        },
        {
            "label": _("Invoice No"),
            "fieldname": "name",
            "fieldtype": "Link",
            "options": "Purchase Invoice",
            "width": 170,
        },
        {
            "label": _("Supplier's TIN"),
            "fieldname": "supplier_tin",
            "fieldtype": "Data",
            "width": 140,
        },
        {
            "label": _("Name of Supplier"),
            "fieldname": "supplier_name",
            "fieldtype": "Data",
            "width": 200,
        },
        {
            "label": _("Taxable Value (LKR)"),
            "fieldname": "taxable_value",
            "fieldtype": "Currency",
            "width": 160,
        },
        {
            "label": _("VAT Amount (LKR)"),
            "fieldname": "vat_amount",
            "fieldtype": "Currency",
            "width": 150,
        },
    ]


def _get_data(filters):
    company = filters["company"]

    vat_account = frappe.db.get_value(
        "Account", {"account_name": "VAT Receivable", "company": company}, "name"
    )
    if not vat_account:
        frappe.throw(
            _(
                "VAT Receivable account not found for {0}. Ensure the Sri Lanka Chart of Accounts is installed."
            ).format(company)
        )

    rows = frappe.db.sql(
        """
		SELECT
			pi.posting_date,
			pi.name,
			pi.lk_supplier_tin_no AS supplier_tin,
			pi.supplier_name,
			COALESCE(MAX(ptc.net_amount), pi.net_total) * IF(pi.is_return, -1, 1) AS taxable_value,
			SUM(ptc.tax_amount_after_discount_amount) * IF(pi.is_return, -1, 1) AS vat_amount
		FROM `tabPurchase Invoice` pi
		INNER JOIN `tabPurchase Taxes and Charges` ptc
			ON  ptc.parent       = pi.name
			AND ptc.account_head = %(vat_account)s
		WHERE
			pi.docstatus    = 1
			AND pi.company      = %(company)s
			AND pi.posting_date BETWEEN %(from_date)s AND %(to_date)s
		GROUP BY pi.name
		ORDER BY pi.posting_date, pi.name
		""",
        {
            "company": company,
            "from_date": filters["from_date"],
            "to_date": filters["to_date"],
            "vat_account": vat_account,
        },
        as_dict=True,
    )

    for i, row in enumerate(rows, 1):
        row["serial_no"] = i

    return rows
