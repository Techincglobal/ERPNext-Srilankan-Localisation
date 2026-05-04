import frappe


def create_print_formats():
	_upsert_print_format(
		name="Tax Invoice - LK",
		html_file="tax_invoice_lk.html",
	)


def _upsert_print_format(name: str, html_file: str):
	html = _read_html(html_file)

	if frappe.db.exists("Print Format", name):
		frappe.db.set_value("Print Format", name, "html", html)
	else:
		frappe.get_doc(
			{
				"doctype": "Print Format",
				"name": name,
				"doc_type": "Sales Invoice",
				"module": "Erpnext Srilankan Localisation",
				"print_format_type": "Jinja",
				"custom_format": 1,
				"standard": "No",
				"pdf_generator": "wkhtmltopdf",
				"margin_top": 20.0,
				"margin_bottom": 40.0,
				"margin_left": 0.0,
				"margin_right": 0.0,
				"page_number": "Hide",
				"html": html,
			}
		).insert(ignore_permissions=True)


def _read_html(filename: str) -> str:
	path = frappe.get_app_path("erpnext_srilankan_localisation", "print_formats", filename)
	with open(path) as f:
		return f.read()
