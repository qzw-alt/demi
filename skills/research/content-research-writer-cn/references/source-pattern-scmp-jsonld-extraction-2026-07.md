# SCMP `articleBody` JSON-LD extraction pattern (verified 2026-07-19)

## Refines the 2026-06-29 "SCMP structurally gated" pitfall

The 2026-06-29 HKUMed QMH SCMP piece had a structurally gated HTML body. The 2026-07-19 Winnie Chan Wang Goldman→TCM SCMP piece is also 1.2MB HTML with gated HTML body, but the `articleBody` field inside the JSON-LD `<script type="application/ld+json">` block contains the full ~8,200-char article text, extractable in a single Python pass.

## Detection rule (verified 2026-07-19)

Parse all JSON-LD blocks. If `articleBody` length > 5,000 chars, the body is available via JSON-LD even when the HTML body is gated. If `articleBody` is 0 or under 1,000 chars, the JSON-LD layer is also gated — fall back to Mirage News for HKUMed/HK hospital stories, or skip the story.

## Working recipe (verified 2026-07-19)

```python
import re, json
with open('/tmp/scmp.html') as f: c = f.read()
blocks = re.findall(r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>', c, re.DOTALL)
for b in blocks:
    if 'articleBody' in b:
        try: obj = json.loads(b)
        except: obj = json.loads(b.replace('\n',' ').replace('\r',''))
        def find_body(o):
            if isinstance(o, dict):
                if 'articleBody' in o: return o['articleBody']
                for v in o.values():
                    r = find_body(v)
                    if r: return r
            elif isinstance(o, list):
                for v in o:
                    r = find_body(v)
                    if r: return r
            return None
        ab = find_body(obj)
        if ab and len(ab) > 5000: print(ab); break
```

## General rule

Always try the JSON-LD `articleBody` extraction first on SCMP URLs before giving up. The gate is at the HTML body layer, not the structured-data layer, for many SCMP lifestyle/health/TCM stories. The 2026-06-29 statement "Do NOT waste 2+ tool calls trying to bypass the SCMP paywall — the canonical page is structurally gated" is now wrong for SCMP lifestyle/health/TCM stories. For SCMP news/hard-news URLs, the gate may still be JSON-LD-deep — verify with the 5,000-char threshold before committing.

## What to do if JSON-LD body is empty

1. Search Mirage News for HKUMed/HK hospital press releases
2. Check the institutional press release directly (hku.hk/press/, med.hku.hk, etc.)
3. Check Hong Kong's Hospital Authority press releases (news.gov.hk)
4. Skip the story and pick the next candidate

## Verified-working SCMP URL examples

- `https://www.scmp.com/lifestyle/health-wellness/article/3360790/...` (2026-07-19, 8,207 chars via JSON-LD) — Template A case study
- `https://www.scmp.com/news/...` (2026-06-29, gated at HTML AND JSON-LD layers) — Mirage News fallback required
