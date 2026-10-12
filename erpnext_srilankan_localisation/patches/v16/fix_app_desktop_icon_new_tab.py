import frappe


def execute():
	"""Fix this app's auto-generated Desktop Icon on sites that already have
	one from before this app shipped its own desktop_icon fixture.

	Frappe's own create_desktop_icons_from_installed_apps() always creates
	an "App"-type icon with link_type="External" from the add_to_apps_screen
	hook - frappe/desk/page/desktop/desktop.js then forces target="_blank"
	on any "External" icon unconditionally (it prepends window.location.origin
	to build the route, so it always looks like an "http(s)://..." link, even
	though our route is just an internal desk page, not another site). The
	app's own fixture now sets link_type="Workspace Sidebar" instead, which
	navigates in-app - but fixture sync only creates a Desktop Icon if one
	doesn't already exist, it never updates an existing one, so a site that
	already auto-generated the old-style icon needs it corrected explicitly.

	Also removes the separate "Sri Lanka Localisation" Desktop Icon that
	Frappe's create_desktop_icons_from_workspace() creates for the app's
	workspace - once the app icon above links straight to that workspace,
	this second one is redundant (and, worse, makes the app icon open a
	folder-style popup instead of navigating directly, since it then has a
	child icon).
	"""
	if frappe.db.exists("Desktop Icon", "Erpnext Srilankan Localisation"):
		frappe.db.set_value(
			"Desktop Icon",
			"Erpnext Srilankan Localisation",
			{
				"link_type": "Workspace Sidebar",
				"link": "/desk/sri-lanka-localisation",
				"link_to": "Sri Lanka Localisation",
				"parent_icon": "",
			},
		)

	frappe.db.delete("Desktop Icon", {"name": "Sri Lanka Localisation"})

	frappe.cache.delete_key("desktop_icons")
	frappe.cache.delete_key("bootinfo")
