import frappe
from frappe.modules.import_file import import_file_by_path


def execute():
	"""Delete the app's Workspace Sidebar and re-import it fresh from its
	fixture, so its item list ends up clean and non-duplicated.

	A site that already had this sidebar (under its pre-rename name "Sri
	Lanka Localisation", or re-synced more than once some other way) can end
	up with its items duplicated - the generic fixture importer only does a
	clean delete-then-recreate when the record doesn't already exist yet, so
	a stray duplicate-laden copy is safer to just discard than to guess at
	merging.

	Patches run *before* frappe.model.sync.sync_all() has another chance to
	run in the same migrate, so simply deleting the record here and hoping
	fixture sync re-creates it afterwards doesn't work - the import has to
	be forced explicitly, right here.
	"""
	frappe.db.delete("Workspace Sidebar Item", {"parent": "Erpnext Srilankan Localisation"})
	frappe.db.delete("Workspace Sidebar", {"name": "Erpnext Srilankan Localisation"})

	path = frappe.get_app_path(
		"erpnext_srilankan_localisation", "workspace_sidebar", "erpnext_srilankan_localisation.json"
	)
	import_file_by_path(path, force=True)

	frappe.cache.delete_key("desktop_icons")
	frappe.cache.delete_key("bootinfo")
