import frappe


def sync_tax_rules(company: str):
	for template in frappe.get_all(
		"Sales Taxes and Charges Template",
		filters={"company": company},
		fields=["name", "tax_category"],
	):
		_sync_tax_rule("Sales", company, template.tax_category, template.name)

	for template in frappe.get_all(
		"Purchase Taxes and Charges Template",
		filters={"company": company},
		fields=["name", "tax_category"],
	):
		_sync_tax_rule("Purchase", company, template.tax_category, template.name)


def _sync_tax_rule(tax_type: str, company: str, tax_category: str, template_name: str):
	if not tax_category:
		return

	template_field = "sales_tax_template" if tax_type == "Sales" else "purchase_tax_template"
	existing = frappe.db.exists(
		"Tax Rule", {"company": company, "tax_category": tax_category, "tax_type": tax_type}
	)

	if existing:
		frappe.db.set_value("Tax Rule", existing, template_field, template_name)
		return

	frappe.get_doc(
		{
			"doctype": "Tax Rule",
			"tax_type": tax_type,
			"company": company,
			"tax_category": tax_category,
			template_field: template_name,
		}
	).insert(ignore_permissions=True)
