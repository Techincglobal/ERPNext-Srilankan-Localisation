import os
import shutil

import frappe

CHART_FILE = "lk_standard_chart_of_accounts.json"


def copy_sri_lanka_chart_of_accounts():
	source = frappe.get_app_path(
		"erpnext_srilankan_localisation",
		"fixtures",
		"chart_of_accounts",
		CHART_FILE,
	)
	target = frappe.get_app_path(
		"erpnext",
		"accounts",
		"doctype",
		"account",
		"chart_of_accounts",
		"verified",
		CHART_FILE,
	)
	os.makedirs(os.path.dirname(target), exist_ok=True)
	shutil.copyfile(source, target)
	frappe.clear_cache()


def remove_sri_lanka_chart_of_accounts():
	target = frappe.get_app_path(
		"erpnext",
		"accounts",
		"doctype",
		"account",
		"chart_of_accounts",
		"verified",
		CHART_FILE,
	)
	if os.path.exists(target):
		os.remove(target)
	frappe.clear_cache()
