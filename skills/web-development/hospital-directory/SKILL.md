---
name: hospital-directory
description: "Maintain the hospital directory on chinahospitalsguide.com — add/update/edit hospital entries in the API JSON and frontend HTML. Covers the dual-file sync pattern, data schema, tag management, and known patch pitfalls."
version: 1.0.0
author: Hermes Agent
tags: [hospital-directory, chinahospitalsguide, data-maintenance, api]
---

# Hospital Directory Maintenance

Add, update, or edit hospital entries in the chinahospitalsguide.com directory.

## Files to Sync (MUST update both)

### 1. API Data (`api/v1/hospitals.json`)

Detailed JSON with structured metadata per hospital. Located at the repo root.

**Schema (key fields):**
```json
{
  "id": "kebab-case-id",
  "name": "English display name",
  "name_zh": "中文正式名称",
  "city": "Beijing/Shanghai/Guangzhou/Shenzhen/Xi'an, etc.",
  "district": "City district",
  "airport_info": "X-Ymin from Airport Name",
  "tags": ["tag1", "tag2", ...],  // See tags section below
  "rank": "Specialty ranking description",
  "phone": "Area code + number",
  "email": "Optional contact email",
  "website": "http://...",
  "international": true/false,
  "international_dept": {
    "phone": "...",
    "email": "...",
    "services": "Description of international services",
    "appointment_lead_days": "7-15"
  },
  "jci": true/false,
  "trust": {
    "score": 0.0-1.0,
    "level": "low/medium/high/very_high",
    "verified_fields": [...],
    "data_source": "single_source/dual_source/multi_source/official",
    "cross_validated": [...],
    "last_verified": "YYYY-MM-DD",
    "notes": [...]
  },
  "address": "Chinese address string",
  "specialties": {
    "specialty-key": "Ranking note, e.g. '#6 nationally'"
  }
}
```

**Insertion point safety (PITFALL):** When adding a new entry via `patch`, ALWAYS target the last entry's closing `}` and the array's `]` as the `old_string` boundary:

```
✅ CORRECT:
old_string: `    }\n  ]\n}`    →   new_string: `    },\n    { NEW ENTRY }\n  ]\n}`

The closing `],\n}` at the end of the file is your safe anchor. Never use an existing entry's content as the old_string to add before it — that REPLACES the entry instead of inserting alongside it.

```

**Verification:** After patch, validate JSON:
```bash
python3 -c "import json; data=json.load(open('api/v1/hospitals.json')); print(f'{len(data[\"hospitals\"])} hospitals, valid JSON')"
```

### 2. Frontend HTML (`hospitals.html`)

JavaScript `const hospitals = [...]` array embedded in the HTML page.

**Schema (compact form):**
```js
{ name: "Hospital Name", city: "City", district: "District", phone: "XXX-XXXXXXX", rank: "Rank description", airport: "X-Ymin from Airport Name", tags: ["tag1", "tag2"], international: true, jci: false, address: "中文地址", website: "http://..." }
```

**Insertion point:** The array ends with `];` — insert before that line. Use:
```
old_string: `    { name: "Last hospital in list", ... },\n];`
new_string: `    { name: "Last hospital in list", ... },\n    { name: "NEW HOSPITAL", ... },\n];`
```

### 3. Tag Mappings (if new tags are added)

If the new hospital uses a tag that doesn't exist in the `specialtyNames` mapping in `hospitals.html`, add it:

```js
const specialtyNames = {
    ...
    "new-tag": "Display Name",
};
```

Check existing tags first — `thoracic-surgery`, `infectious-disease`, and the standard tags below are already mapped.

### Existing Tags Reference

| Tag | Display Name | Notes |
|-----|-------------|-------|
| cardiology | Cardiology & Cardiac Surgery | |
| heart-surgery | Heart Surgery | |
| orthopedics | Orthopedics & Spine | |
| joint-replacement | Joint Replacement | |
| spine-surgery | Spine Surgery | |
| sports-medicine | Sports Medicine | |
| maternity | Maternity | |
| obstetrics | Obstetrics & Gynecology | |
| prenatal-diagnosis | Prenatal Diagnosis | |
| fertility | Fertility & IVF | |
| oncology | Oncology & Cancer Treatment | |
| cancer-surgery | Cancer Surgery | |
| radiotherapy | Radiotherapy | |
| neurosurgery | Neurosurgery & Neurology | |
| neurology | Neurology | |
| pediatrics | Pediatrics & Children's Health | |
| childrens-health | Children's Health | |
| general | General Medicine | |
| all-specialties | All Specialties | |
| international | International Dept | |
| vip-services | VIP Services | |
| gastroenterology | Gastroenterology | |
| geriatrics | Geriatrics | |
| plastic-surgery | Plastic Surgery | |
| kidney-disease | Kidney Disease | |
| hematology | Hematology | |
| respiratory | Respiratory Medicine | |
| military | Military Hospital | |
| tcm | Traditional Chinese Medicine (TCM) | |
| dental | Dental & Oral Surgery | |
| oral-surgery | Oral Surgery | |
| cosmetic-dental | Cosmetic Dentistry | |
| lasik | LASIK & Eye Surgery | |
| cataract | Cataract Surgery | |
| ent | ENT (Ear, Nose & Throat) | |
| urology | Urology | |
| cryosurgery | Cryosurgery | |
| nanoknife | Nanoknife Treatment | |
| ophthalmology | Ophthalmology | |
| gynecology | Gynecology | |
| liver-disease | Hepatology & Liver Disease | |
| acupuncture | Acupuncture & TCM | |
| rehabilitation | Rehabilitation Medicine | |
| thoracic-surgery | Thoracic Surgery | Added 2026-06-25 |
| infectious-disease | Infectious Disease | Added 2026-06-25 |

## Workflow

### Step 1: Gather Hospital Data

Required minimum fields:
- Name (English + Chinese)
- City + District
- Phone (main + international department if separate)
- Rank/specialty ranking (e.g. "#1 Thoracic Surgery (#6 nationally)")
- Airport info (travel time from nearest international airport)
- Tags (specialties — see table above)
- International department (phone, email, services, lead time)
- Address (Chinese)
- Website URL

Optional but valuable:
- Email
- Trust metadata (verify against official website, public rankings, direct contact)
- Specialty sub-details
- Price estimates for common procedures (when available)

### Step 2: Update API JSON (`api/v1/hospitals.json`)

1. Read the last 30 lines of the file to find the insertion point (the last entry before the closing `]`)
2. Use `patch` with the closing boundary as `old_string` (see pitfall above)
3. Validate JSON immediately with `python3 -c "import json; json.load(open(...))"`

### Step 3: Update Frontend HTML (`hospitals.html`)

1. Find the end of the `const hospitals = [...]` array (ends with `];`)
2. Insert new entry before `];`
3. If new tags: add to `specialtyNames` mapping
4. Verify the entry is present: grep or read the relevant lines

### Step 4: Verify

```bash
# JSON validity
python3 -c "import json; d=json.load(open('api/v1/hospitals.json')); print(f'{len(d[\"hospitals\"])} hospitals')"

# HTML has the entry
grep -c "HospitalName" hospitals.html    # should be >= 1

# No syntax errors (browser-parse the JS)
node -e "eval(require('fs').readFileSync('hospitals.html','utf8').match(/const hospitals = (\[.*?\]);/s)[1])" 2>&1
```

## Pitfalls

### 🚩 REPLACE vs INSERT (critical)

The `patch` tool's `old_string` is a **find-and-replace** operation. If you use an existing entry's content as `old_string` and your `new_string` is a different hospital, you've **replaced** the existing one, not added alongside it.

Always target the closing boundary delimiters:
- JSON: last `}\n  ]\n}` → insert before `]`
- HTML: `];` at end of JS array → insert before `];`

### 🚩 Sibling-subagent sitemap warning

If this runs as part of a cron job that shares `sitemap.xml` with other sites (e.g. both chinahospitalsguide.com and oriental-destiny.com cron jobs), the `patch` tool may warn about sibling-subagent writes. Read the file before patching (re-read even if you read it earlier) to avoid overwriting stale data.

### 🚩 Trust score calibration

When assigning `trust.score`, use these guidelines:
- **0.95+ (very_high):** Official source (hospital website), cross-validated with 2+ independent sources and public rankings
- **0.86-0.94 (high):** Multi-source with cross-validation but no direct official confirmation (e.g. phone call)
- **0.80-0.85 (medium):** Dual-source, one official
- **<0.80 (low):** Single source or unverified claims

### 🚩 International department info

When available, always include `international_dept` as a structured sub-object with phone, email, services, and appointment_lead_days. This is a key differentiator for medical tourism SEO and directly supports the `medical-tourism-client-intake` skill's workflow.

## Related Skills

- `medical-tourism-client-intake` — uses hospital database during patient intake
- `programmatic-seo` — broader site content management for chinahospitalsguide.com
