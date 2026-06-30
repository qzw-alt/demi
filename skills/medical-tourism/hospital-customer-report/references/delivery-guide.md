# Hospital Customer Report — Delivery Quick Reference

## Quick Commands (Modes)

```bash
cd /home/ubuntu/chinahospitalsguide

# Basic ($49) — Chinese content
node scripts/generate-report.js --name "Maria" --case "knee replacement" --city Beijing --basic

# Premium ($399) — Chinese content with service flow
node scripts/generate-report.js --name "John" --case "nutcracker syndrome" --city Xi'an --premium

# Quick match (English, no name)
node scripts/generate-report.js "knee replacement" Beijing
```

## Output Files

- Script outputs to: `reports/report-{name}-{timestamp}.html`
- Copy to repo root for GitHub Pages: `cp reports/report-*.html report-{descriptive-name}.html`
- All 3 Carlso Mendoza sample files updated together when regenerating:
  - `report-carlos-mendoza-1782619281101.html` (basic)
  - `report-carlos-mendoza-1782619281172.html` (premium)
  - `report-carlos-mendoza-1782621324477.html` (latest)

## Report Structure (current as of 2026-06-28)

Both versions: Hero → Cover Letter → How to Use → Price → Hospitals → Transport → Checklist

¥49 adds: Upgrade section
¥399 replaces Upgrade with: 6-step Service Flow

## ALL Content in Chinese

Cover letter, FAQ, labels, tables, service flow, checklist — everything on the page is in Chinese.
