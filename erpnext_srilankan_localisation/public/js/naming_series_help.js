// Appends a short description of this app's custom naming series
// attributes (TYY/MMM/TYYYY/YEARSEQ) to the "Document Naming Settings"
// page's own built-in help text - without touching Frappe's own content,
// which is static HTML baked into the help_html field's options.
//
// Loaded globally (app_include_js) rather than scoped via doctype_js:
// this doctype's own __js bundle isn't reliably evaluated on first visit
function lk_append_naming_series_help(frm) {
	const field = frm.get_field("help_html");
	if (!field || field.$wrapper.find(".lk-naming-series-help").length) {
		return;
	}

	field.$wrapper.append(`
		<div class="well lk-naming-series-help">
			<b>${__("Sri Lanka Localisation attributes")}</b>
			<ul>
				<li><code>.TYY.</code> - ${__("Year in 2 digits, from the document's own transaction date")}</li>
				<li><code>.MMM.</code> - ${__(
					"Month abbreviation (JAN-DEC), from the document's own transaction date"
				)}</li>
				<li><code>.TYYYY.</code> - ${__("Year in 4 digits, from the document's own transaction date")}</li>
				<li><code>YEARSEQ</code> - ${__(
					"Gapless annual sequence number that resets every year - available on Sales Invoice and Purchase Invoice, for Sri Lankan tax invoice numbering"
				)}</li>
			</ul>
			${__(
				"You can add more than one YEARSEQ-based series for the same doctype (e.g. a separate series for credit/debit notes, or per company) - each gets its own independent counter, scoped by whatever text in the series comes before YEARSEQ."
			)}
		</div>
	`);
}

// Frappe's own transaction_type handler (document_naming_settings.js core)
// re-fetches naming_series_options asynchronously, and once that resolves,
// re-renders this section - including the help_html field, which resets it
// back to just its static options and wipes anything appended to it. A
// MutationObserver reacts to that the instant it happens, however long the
// request actually takes, rather than guessing at a delay.
function lk_keep_naming_series_help_alive(frm) {
	const field = frm.get_field("help_html");
	if (!field || field.$wrapper.data("lkHelpObserverAttached")) {
		return;
	}
	field.$wrapper.data("lkHelpObserverAttached", true);

	new MutationObserver(() => {
		if (!field.$wrapper.find(".lk-naming-series-help").length) {
			lk_append_naming_series_help(frm);
		}
	}).observe(field.$wrapper[0], { childList: true });
}

// "Update Series Counter" has no help field of its own to append to (just
// Prefix / Current Value / a button) - insert a block directly above the
// Prefix field instead, explaining how the YEARSEQ counter key is built and
// the specific mix-up this app's own YEARSEQ series cause in that field's
// prefix search (see utils/naming.py _yearseq_key and the Document Naming
// Settings _get_prefixes/NamingSeries.get_prefix core implementation this
// is describing).
function lk_append_series_counter_help(frm) {
	const field = frm.get_field("prefix");
	if (!field || field.$wrapper.parent().find(".lk-series-counter-help").length) {
		return;
	}

	$(`
		<div class="well lk-series-counter-help">
			<b>${__("Sri Lanka Localisation attributes")}</b><br><br>
			<b>${__("How the counter works for YEARSEQ-based series")}</b>
			<p>${__(
				"Each YEARSEQ series has its own counter, keyed by the doctype, whatever text in the series isn't a date variable, and the year - for example a Sales Invoice credit note series becomes a counter key like"
			)} <code>YEARSEQ-Sales Invoice-RET-2026</code>.</p>
			<p><b>${__(
				"When searching for a prefix below, the same YEARSEQ series can show up as two different-looking entries:"
			)}</b></p>
			<ul>
				<li>${__("one that looks like")} <code>26OCT-YEARSEQ</code> - ${__(
		"this is only a preview Frappe generates from the naming series template - it resolves TYY/MMM but doesn't recognise YEARSEQ, so it leaves it as literal text. It does not correspond to any real counter."
	)}</li>
				<li>${__("one that looks like")} <code>YEARSEQ-Sales Invoice-2026</code> - ${__(
		"this is the real counter that actually drives the next number. Always update this one, not the other."
	)}</li>
			</ul>
		</div>
	`).insertBefore(field.$wrapper);
}

frappe.ui.form.on("Document Naming Settings", {
	onload_post_render(frm) {
		lk_append_naming_series_help(frm);
		lk_append_series_counter_help(frm);
		lk_keep_naming_series_help_alive(frm);
	},
	refresh(frm) {
		lk_append_naming_series_help(frm);
		lk_append_series_counter_help(frm);
		lk_keep_naming_series_help_alive(frm);
	},
});
