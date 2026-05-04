from frappe.desk.page.setup_wizard.setup_wizard import make_records

PAYMENT_METHODS = [
	{"doctype": "Mode of Payment", "mode_of_payment": "Credit/Debit Card", "type": "Cash", "enabled": 1},
	{"doctype": "Mode of Payment", "mode_of_payment": "Mobile Payment", "type": "Cash", "enabled": 1},
	{"doctype": "Mode of Payment", "mode_of_payment": "Online Payment", "type": "Cash", "enabled": 1},
]


def create_payment_methods():
	make_records(PAYMENT_METHODS)
