# Copyright (c) 2026, servers@techincglobal.com and Contributors
# See license.txt

from unittest.mock import patch

import frappe
from frappe.tests import IntegrationTestCase
from frappe.utils import now_datetime

from erpnext_srilankan_localisation.overrides.validations import validate_sales_invoice
from erpnext_srilankan_localisation.utils.jinja import get_address_display
from erpnext_srilankan_localisation.utils.naming import parse_naming_series_variable

EXTRA_TEST_RECORD_DEPENDENCIES = []
IGNORE_TEST_RECORD_DEPENDENCIES = []


class IntegrationTestLKTaxSettings(IntegrationTestCase):

	def setUp(self):
		self.settings = frappe.get_single("LK Tax Settings")
		self._original_enforce = self.settings.enforce_tin_validation

	def tearDown(self):
		self.settings.enforce_tin_validation = self._original_enforce
		self.settings.save(ignore_permissions=True)

	# --- Naming series: TYY ---

	def test_tyy_returns_two_digit_year(self):
		doc = frappe._dict(posting_date="2026-01-15")
		self.assertEqual(parse_naming_series_variable(doc, "TYY"), "26")

	def test_tyy_falls_back_to_today_when_no_doc(self):
		expected = now_datetime().date().strftime("%y")
		self.assertEqual(parse_naming_series_variable(None, "TYY"), expected)

	def test_tyy_falls_back_to_today_when_no_posting_date(self):
		expected = now_datetime().date().strftime("%y")
		self.assertEqual(parse_naming_series_variable(frappe._dict(), "TYY"), expected)

	# --- Naming series: MMM ---

	def test_mmm_returns_uppercase_month_abbreviation(self):
		doc = frappe._dict(posting_date="2026-01-15")
		self.assertEqual(parse_naming_series_variable(doc, "MMM"), "JAN")

	def test_mmm_returns_correct_month_for_december(self):
		doc = frappe._dict(posting_date="2026-12-01")
		self.assertEqual(parse_naming_series_variable(doc, "MMM"), "DEC")

	def test_mmm_returns_correct_month_for_july(self):
		doc = frappe._dict(posting_date="2026-07-10")
		self.assertEqual(parse_naming_series_variable(doc, "MMM"), "JUL")

	# --- TIN validation ---

	def test_tin_validation_skipped_when_enforcement_disabled(self):
		self.settings.enforce_tin_validation = 0
		self.settings.save(ignore_permissions=True)

		doc = frappe._dict(company="_Test Company", lk_customer_tin_no="")
		validate_sales_invoice(doc)  # must not raise

	def test_tin_validation_skipped_for_non_sri_lanka_company(self):
		self.settings.enforce_tin_validation = 1
		self.settings.save(ignore_permissions=True)

		with patch.object(frappe.db, "get_value", return_value="India"):
			doc = frappe._dict(company="_Test Company", lk_customer_tin_no="")
			validate_sales_invoice(doc)  # must not raise

	def test_tin_validation_throws_when_tin_missing_for_sl_company(self):
		self.settings.enforce_tin_validation = 1
		self.settings.save(ignore_permissions=True)

		with patch.object(frappe.db, "get_value", return_value="Sri Lanka"):
			doc = frappe._dict(company="_Test Company", lk_customer_tin_no="")
			with self.assertRaises(frappe.ValidationError):
				validate_sales_invoice(doc)

	def test_tin_validation_passes_when_tin_present_for_sl_company(self):
		self.settings.enforce_tin_validation = 1
		self.settings.save(ignore_permissions=True)

		with patch.object(frappe.db, "get_value", return_value="Sri Lanka"):
			doc = frappe._dict(company="_Test Company", lk_customer_tin_no="123456789V")
			validate_sales_invoice(doc)  # must not raise

	# --- Address display ---

	def test_address_display_returns_empty_for_none(self):
		self.assertEqual(get_address_display(None), "")

	def test_address_display_returns_empty_for_missing_record(self):
		self.assertEqual(get_address_display("nonexistent-address-xyz-lk"), "")
