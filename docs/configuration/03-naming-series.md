# Naming Series

This app adds custom naming series variables and an annual-sequence mechanism for Sales Invoices. Two series formats are available out of the box.

---

## Available series

### Monthly restart — `TYY.MMM.-.#####`

The counter resets at the start of each month.

```text
TYY.MMM.-.#####  →  26JUN-00001, 26JUN-00002 … 26JUL-00001 (restarts)
```

### Annual sequence — `TYY.MMM.-.TSEQ.####`

The counter continues through the whole year and only resets on 1 January. The month is still visible in the name.

```text
TYY.MMM.-.TSEQ.####  →  26MAY-0001, 26JUN-0002, 26JUL-0003 …
```

The digit count is controlled by the number of `#` characters — `####` gives 4 digits, `#####` gives 5, and so on.

---

## Custom variables

| Variable | Resolves to | Source | Example |
|---|---|---|---|
| `TYY` | Two-digit year | `posting_date` | `26` |
| `MMM` | Three-letter uppercase month | `posting_date` | `JUN` |
| `TYYYY` | Four-digit year | `posting_date` | `2026` |

All three variables fall back to today's date when `posting_date` is not present on the document.

---

## How `TSEQ` works

`TSEQ` is not a naming series variable — it is a keyword detected by the `autoname` doc event on Sales Invoice. When the selected series contains `TSEQ`:

1. The parts before `TSEQ` are resolved normally (e.g. `TYY.MMM.-` → `26JUN-`).
2. The `#` count after `TSEQ` sets the digit width.
3. An atomic counter keyed by year (`TSEQ-{YYYY}` in `tabSeries`) is incremented and appended.

The resulting name is set directly on the document before Frappe's default naming runs.

---

## Document Naming Settings

Go to **Settings → Document Naming Settings** to view or change the current counter values.

| Series | Where to find the counter in the prefix dropdown |
|---|---|
| `TYY.MMM.-.#####` | `26JUN-` (current month's prefix) |
| `TYY.MMM.-.TSEQ.####` | `TSEQ-2026` (current year) |

> The `TSEQ` counter is stored under `TSEQ-{YYYY}` rather than a monthly prefix, so it appears as a single entry for the whole year.

Counter values are **never decremented** when a document is deleted or cancelled. This is intentional — invoice numbers must not be reused in accounting.

---

## How to configure

1. Go to **Settings → Document Naming Settings**.
2. Select **Sales Invoice** as the transaction.
3. The naming series options field shows the available series — edit if needed.
4. Save.

---

> Next: [Currency & Rounding](04-currency-rounding.md)
