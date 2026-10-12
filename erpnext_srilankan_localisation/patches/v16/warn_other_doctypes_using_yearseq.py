import click
import frappe

# Doctypes this app explicitly wires up for YEARSEQ via hooks.py doc_events.
# Keep this in sync with hooks.py if that list ever changes.
HOOKED_DOCTYPES = {"Sales Invoice", "Purchase Invoice"}


def execute():
	"""Warn if any doctype other than the ones this app explicitly hooks up
	(see hooks.py doc_events) has a naming series option containing YEARSEQ.

	Before this app scoped its annual-sequence hooks to specific doctypes,
	they were wired up via a "*" wildcard on every doctype - so if a site had
	manually added a YEARSEQ-based naming series option to some other
	doctype (e.g. via Customize Form), it would have silently worked. Now
	that the hooks are scoped, that doctype's autoname/validate/on_trash
	handling for YEARSEQ would silently stop firing. Flag it loudly instead
	of letting it fail silently.
	"""
	rows = frappe.db.sql(
		"""
		SELECT doc_type FROM `tabProperty Setter`
		WHERE field_name = 'naming_series' AND property = 'options' AND value LIKE %s
		""",
		("%YEARSEQ%",),
	)

	affected = sorted({row[0] for row in rows if row[0] not in HOOKED_DOCTYPES})
	if not affected:
		return

	message = (
		"ERPNext Sri Lankan Localisation: found YEARSEQ in the naming series options "
		f"of {', '.join(affected)}, which this app no longer hooks up automatically - "
		"only Sales Invoice and Purchase Invoice get the annual-sequence "
		"autoname/validate/on_trash handling now (see hooks.py doc_events). If you rely "
		"on YEARSEQ numbering there, ask for it to be added explicitly; otherwise remove "
		"YEARSEQ from that doctype's naming series options to avoid confusion."
	)

	click.secho(message, fg="yellow")
	frappe.log_error(title="YEARSEQ naming series on unhooked doctype", message=message)
