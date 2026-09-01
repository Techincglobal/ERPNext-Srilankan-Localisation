from erpnext_srilankan_localisation.setup.tax_templates import create_sri_lanka_tax_setup


def on_update(doc, method=None):
	if doc.country != "Sri Lanka":
		return

	create_sri_lanka_tax_setup(doc.name)
