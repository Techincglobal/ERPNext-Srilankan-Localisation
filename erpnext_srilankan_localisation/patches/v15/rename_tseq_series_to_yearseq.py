import frappe


def execute():
	"""Rename legacy TSEQ-{year} Series rows to YEARSEQ-{year}, and update the
	naming_series value stored on existing Sales Invoices to match.

	The annual invoice-numbering marker was renamed from TSEQ to YEARSEQ.
	Without this:
	
	- Any site that already has a TSEQ-{year} counter would silently start a
	  fresh YEARSEQ-{year} counter at 1, colliding with invoice names already
	  issued under the old counter.

	- Existing Sales Invoices still carry the literal old string
	  ("TYY.MMM.-.TSEQ.####") in their naming_series field, since that value
	  is copied onto the document at creation time, not a live reference to
	  the current options list. Every hook that checks for "YEARSEQ" in
	  naming_series (the posting-date lock, the delete-revert) would silently
	  stop applying to those documents.
	"""
	old_rows = frappe.db.sql("SELECT name, current FROM `tabSeries` WHERE name LIKE 'TSEQ-%'")

	for old_name, current in old_rows:
		new_name = old_name.replace("TSEQ-", "YEARSEQ-", 1)
		existing = frappe.db.sql("SELECT current FROM `tabSeries` WHERE name = %s", (new_name,))

		if existing:
			# A YEARSEQ-{year} row already exists (e.g. an invoice was created under
			# the new code before this patch ran). Keep the higher value so the
			# counter is never moved backward, then drop the old row.
			if existing[0][0] < current:
				frappe.db.sql("UPDATE `tabSeries` SET current = %s WHERE name = %s", (current, new_name))
			frappe.db.sql("DELETE FROM `tabSeries` WHERE name = %s", (old_name,))
		else:
			frappe.db.sql("UPDATE `tabSeries` SET name = %s WHERE name = %s", (new_name, old_name))

	frappe.db.sql(
		"UPDATE `tabSales Invoice` SET naming_series = REPLACE(naming_series, 'TSEQ', 'YEARSEQ') "
		"WHERE naming_series LIKE '%TSEQ%'"
	)
