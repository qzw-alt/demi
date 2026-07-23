"""
Read the latest audit report and extract:
- NO_SCHEMA URLs (need schema additions)
- THIN URLs (need merge proposals)
- New duplicate group (9th, the one that emerged since 07-21)

Output a clean action list with proposed merge targets.
"""

import re
import json
from pathlib import Path

REPORT = Path('/home/ubuntu/.hermes/tmp/audit/audit-report.md')
content = REPORT.read_text(encoding='utf-8')

# Extract all rows from the "详细清单" table
# Format: | [URL](URL) | **CATEGORY** | words | schema | robots | title |
row_re = re.compile(r'\| \[([^\]]+)\]\(([^)]+)\) \| \*\*(\w+)\*\* \| (\d+|\?) \| (\d+) \| ([^|]+) \| ([^|]+) \|', re.MULTILINE)

no_schema_urls = []
thin_urls = []
all_rows = []

for m in row_re.finditer(content):
    path, url, cat, words, schema_n, robots, title = m.groups()
    words = int(words) if words.isdigit() else 0
    schema_n = int(schema_n)
    title = title.strip()
    robots = robots.strip()
    row = {
        'path': path.strip(),
        'url': url.strip(),
        'category': cat,
        'words': words,
        'schema_count': schema_n,
        'robots': robots,
        'title': title,
    }
    all_rows.append(row)
    if cat == 'NO_SCHEMA':
        no_schema_urls.append(row)
    elif cat == 'THIN':
        thin_urls.append(row)

print(f"=== Summary ===")
print(f"NO_SCHEMA: {len(no_schema_urls)}")
print(f"THIN: {len(thin_urls)}")
print()

# Output NO_SCHEMA list
print("=" * 60)
print("NO_SCHEMA (need schema additions):")
print("=" * 60)
for r in no_schema_urls:
    print(f"  [{r['words']:>4} words] {r['path']:60} | {r['title'][:50]}")

print()
print("=" * 60)
print("THIN (need merge proposal):")
print("=" * 60)
for r in thin_urls:
    print(f"  [{r['words']:>4} words] {r['path']:60} | {r['title'][:50]}")

# Save JSON for follow-up
out = {
    'no_schema': no_schema_urls,
    'thin': thin_urls,
    'generated_from': str(REPORT),
}
out_path = Path('/home/ubuntu/.hermes/tmp/audit/action-list.json')
out_path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding='utf-8')
print(f"\nSaved action list: {out_path}")