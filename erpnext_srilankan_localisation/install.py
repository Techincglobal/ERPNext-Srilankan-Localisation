import click
import frappe

from erpnext_srilankan_localisation.setup.chart_of_accounts import copy_sri_lanka_chart_of_accounts
from erpnext_srilankan_localisation.setup.create_properties import initial_setup
from erpnext_srilankan_localisation.setup.payment_methods import create_payment_methods
from erpnext_srilankan_localisation.setup.tax_templates import (
	create_sri_lanka_tax_setup,
	remove_erpnext_default_setup,
)
from erpnext_srilankan_localisation.setup.wht_categories import create_wht_categories


def after_setup_wizard(wizard_args=None):
	for company in frappe.get_all("Company", filters={"country": "Sri Lanka"}, pluck="name"):
		remove_erpnext_default_setup(company)
		create_sri_lanka_tax_setup(company)


def after_install():
	try:
		print("Setting up ERPNext Sri Lankan Localisation...")

		copy_sri_lanka_chart_of_accounts()
		initial_setup()
		create_payment_methods()
		for company in frappe.get_all("Company", filters={"country": "Sri Lanka"}, pluck="name"):
			create_sri_lanka_tax_setup(company)
		create_wht_categories()

		click.secho(
			"Thank you for installing ERPNext Sri Lankan Localisation!",
			fg="green",
		)

	except Exception as e:
		click.secho(
			"Installation for ERPNext Sri Lankan Localisation failed due to an error. "
			"Please try re-installing the app.",
			fg="bright_red",
		)
		raise e
