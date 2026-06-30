# Codex Handoff: Report Generator Spec

The authoritative spec lives at:
**`/home/ubuntu/chinahospitalsguide/REPORT-GENERATOR-SPEC.md`**
(also at https://github.com/qzw-alt/chinahospitalsguide/blob/master/REPORT-GENERATOR-SPEC.md)

## What to reference

When Codex CLI picks up this task, hand it:
1. The spec doc above (has full breakdown)
2. The two template files:
   - `hospital-directory-basic-49.md` (¥49 format spec)
   - `hospital-directory-premium-399.md` (¥399 format spec)
3. The generator script: `scripts/generate-report.js`
4. The CSV data: `data/hospital-directory-51.csv`

## Priority summary (from spec)

| Priority | Task | File |
|----------|------|------|
| P1 | Hero stat labels → Chinese | generate-report.js |
| P1 | Button text → Chinese | generate-report.js |
| P1 | Hospital one-liner descriptions | generate-report.js + data |
| P1 | Premium: patient profile table | generate-report.js |
| P1 | Premium: 3-hospital comparison table | generate-report.js |
| P2 | Premium: "why choose us" table | generate-report.js |
| P2 | Premium: "about" section | generate-report.js |
| P2 | Hospital "why recommend" section | generate-report.js |
| P3 | Premium: hospital deep info (contacts, prices, lifestyle, watchouts) | generate-report.js + data |
| P3 | Expand CSV (Email, Price_Range, etc.) | data/hospital-directory-51.csv |
| P4 | Unused CSS cleanup | generate-report.js |
