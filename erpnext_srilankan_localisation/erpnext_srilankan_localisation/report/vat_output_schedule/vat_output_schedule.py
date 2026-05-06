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
            "label": _("Tax Invoice No"),
            "fieldname": "name",
            "fieldtype": "Link",
            "options": "Sales Invoice",
            "width": 170,
        },
        {
            "label": _("Purchaser's TIN"),
            "fieldname": "purchaser_tin",
            "fieldtype": "Data",
            "width": 140,
        },
        {
            "label": _("Name of Purchaser"),
            "fieldname": "customer_name",
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
        "Account", {"account_name": "VAT Payable", "company": company}, "name"
    )
    if not vat_account:
        frappe.throw(
            _(
                "VAT Payable account not found for {0}. Ensure the Sri Lanka Chart of Accounts is installed."
            ).format(company)
        )

    rows = frappe.db.sql(
        """
		SELECT
			si.posting_date,
			si.name,
			si.lk_customer_tin_no AS purchaser_tin,
			si.customer_name,
			COALESCE(MAX(stc.net_amount), si.net_total) * IF(si.is_return, -1, 1) AS taxable_value,
			SUM(stc.tax_amount_after_discount_amount) * IF(si.is_return, -1, 1) AS vat_amount
		FROM `tabSales Invoice` si
		INNER JOIN `tabSales Taxes and Charges` stc
			ON  stc.parent       = si.name
			AND stc.account_head = %(vat_account)s
		WHERE
			si.docstatus    = 1
			AND si.company      = %(company)s
			AND si.posting_date BETWEEN %(from_date)s AND %(to_date)s
		GROUP BY si.name
		ORDER BY si.posting_date, si.name
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
