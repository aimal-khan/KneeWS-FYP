# Prototypes

This directory contains two zero-dependency interactive HTML demonstrations of the KneeWS system. No web server, internet connection, or installed packages are required — simply open the files directly in any modern browser.

All data displayed in these prototypes is **entirely synthetic**. No real patient data, trained model weights, or clinical findings are embedded.

---

## Walkthrough (`walkthrough/`)

A guided 6-step demonstration designed for a ~90-second live pitch or presentation.

| File | Variant |
|:---|:---|
| `kneews_walkthrough.html` | PRIMARY — report reliability against 58 expert-labelled studies |
| `kneews_walkthrough_optionb.html` | Option B — reliability estimated from model disagreements |

**Step-by-step flow:**
1. *Read the report* — identifies 4 named vs 8 unmentioned findings from a synthetic radiology report
2. Toggle standard practice vs KneeWS weak supervision
3. View the four supervision rule states
4. See label calibration against the gold set (PRIMARY) or internal disagreement (Option B)
5. Toggle between model predictions — striped bar indicates model abstention
6. Summary view of multi-label output across 12 abnormalities

---

## Dashboard (`dashboard/`)

An 11-screen interactive feature explorer, with each screen mapped 1:1 to the 10 registered system features. Designed to be kept open in a background browser tab during Q&A for quick reference.

| File | Variant |
|:---|:---|
| `kneews_primary.html` | PRIMARY variant |
| `kneews_optionb.html` | Option B variant |

Useful for demonstrating:
- Disagreement case handling
- The labelling workbench interface
- Multi-institution onboarding flow
- Reporting pipeline details

---

## Opening the Prototypes

```bash
# Option A: Open directly in browser (macOS)
open prototypes/walkthrough/kneews_walkthrough.html

# Option B: Use the local dev server (serves all 4 simultaneously)
python scripts/serve_prototypes.py
```
