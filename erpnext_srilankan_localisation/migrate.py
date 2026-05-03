import click
import frappe

from erpnext_srilankan_localisation.setup.chart_of_accounts import copy_sri_lanka_chart_of_accounts
from erpnext_srilankan_localisation.setup.create_properties import initial_setup
from erpnext_srilankan_localisation.setup.tax_templates import create_sri_lanka_tax_setup


def after_migrate():
	try:
		print("Running ERPNext Sri Lankan Localisation migrations...")

		copy_sri_lanka_chart_of_accounts()
		initial_setup()
		for company in frappe.get_all("Company", filters={"country": "Sri Lanka"}, pluck="name"):
			create_sri_lanka_tax_setup(company)

		click.secho(
			"ERPNext Sri Lankan Localisation migrations completed successfully.",
			fg="green",
		)

	except Exception as e:
		click.secho(
			"ERPNext Sri Lankan Localisation migration failed due to an error.",
			fg="bright_red",
		)
		raise e
