# Naming Series

Sales Invoices are numbered automatically using a date-stamped format. The default series is:

```
TYY.MMM.-.#####
```

This produces invoice numbers like `26.MAY.-00001`, where `26` is the two-digit year and `MAY` is the three-letter month, both derived from the invoice's **posting date**.

---

## How the variables work

| Variable | Resolves to | Example |
|---|---|---|
| `TYY` | Two-digit year from posting date | `26` |
| `MMM` | Three-letter uppercase month from posting date | `MAY` |

These are custom variables registered by the app in `hooks.py`. Standard ERPNext variables like `YYYY` and `.####` also work alongside them.

---

## Changing the series

If you need a different format:

1. Go to **Settings → Naming Series**
2. Select **Sales Invoice** from the document type dropdown
3. Add or change the series in the options list
4. Set the default

![Naming Series — Sales Invoice](../images/Naming%20Series%20for%20Sales%20Invoice.png)

The standard ERPNext format `SINV-.YYYY.-` is included as an alternative option.

---

> Next: [Currency & Rounding](04-currency-rounding.md)
