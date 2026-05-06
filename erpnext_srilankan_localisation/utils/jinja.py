import frappe
from frappe.query_builder import DocType


def get_address_display(address_name):
	if not address_name:
		return ""

	address = frappe.db.get_value(
		"Address",
		address_name,
		["address_line1", "address_line2", "city", "country"],
		as_dict=True,
	)

	if not address:
		return ""

	lines = [
		address.address_line1,
		address.address_line2,
		address.city,
		address.country,
	]

	return "<br>".join(line for line in lines if line)


def get_contact_number_from_contact(contact):
	ContactPhone = DocType("Contact Phone")
	Contact = DocType("Contact")

	phones = (
		frappe.qb.from_(ContactPhone)
		.select(ContactPhone.phone, ContactPhone.is_primary_mobile_no)
		.where(
			(ContactPhone.parent == contact)
			& (ContactPhone.parenttype == "Contact")
			& (ContactPhone.parentfield == "phone_nos")
		)
		.orderby(ContactPhone.is_primary_mobile_no, order=frappe.qb.desc)
		.run(as_dict=True)
	)

	contact_full_name = (
		frappe.qb.from_(Contact)
		.select(Contact.full_name)
		.where(Contact.name == contact)
		.run(as_dict=True)
	)

	return {
		"contact_name": contact_full_name[0]["full_name"] if contact_full_name else "",
		"primary_phone": phones[0]["phone"] if phones else "",
	}
