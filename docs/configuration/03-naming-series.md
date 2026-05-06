# Naming Series

Sales Invoices can be numbered using a date-based format. A common Sri Lanka-oriented series used in this app is:

```text
TYY.MMM.-.#####
```

This produces invoice numbers like:

```text
26.MAY.-00001
```

Where:
- `TYY` = two-digit year from the posting date
- `MMM` = three-letter uppercase month from the posting date

---

## Variables

| Variable | Resolves to | Example |
|---|---|---|
| `TYY` | Two-digit year from posting date | `26` |
| `MMM` | Three-letter uppercase month from posting date | `MAY` |

These custom variables work alongside normal ERPNext naming series parts.

---

## How to configure

1. Go to **Settings → Naming Series**
2. Select **Sales Invoice**
3. Add the series you want to use
4. Save and test the preview

![Naming Series — Sales Invoice](../images/Naming%20Series%20for%20Sales%20Invoice.png)

If needed, you can keep ERPNext’s standard series as an alternative.

---

## Practical note

If your production format needs a slightly different output, such as a different separator style, update the naming series options before rollout and test the generated preview names first.

---

> Next: [Currency & Rounding](04-currency-rounding.md)
