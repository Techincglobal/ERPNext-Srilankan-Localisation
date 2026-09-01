from erpnext_srilankan_localisation.setup.create_properties import create_property_setters
from erpnext_srilankan_localisation.setup.property_setters import PROPERTIES


def execute():
	"""Push the YEARSEQ naming series option onto sites that installed this
	app before the YEARSEQ redesign.

	create_property_setters() is only ever called from after_install and
	setup_wizard_complete - both one-time events, never re-run on migrate.
	The other YEARSEQ patches migrate an existing site's counters and
	already-issued invoice names from TSEQ to YEARSEQ, but without this,
	the Sales Invoice naming_series dropdown itself would still be missing
	the new "TYY.MMM.-.YEARSEQ.####" option, so nobody could actually pick
	it for a new invoice.

	Calls create_property_setters() itself (not a raw property setter
	write) so its merge behaviour applies here too: existing options
	(including the old TSEQ line) are kept, not replaced.
	"""
	create_property_setters(PROPERTIES)
