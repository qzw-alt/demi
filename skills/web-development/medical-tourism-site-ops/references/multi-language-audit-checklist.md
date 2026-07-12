# Multi-language audit checklist (chinahospitalsguide.com)

Companion to `SKILL.md` §"Multi-language audit + incremental review workflow".
This file is the **executable checklist** — copy-paste commands and the
rationale for each. Use when user says "再帮我审查一下" / "审计一下" / "看看有什么问题".

## Pre-flight (5 commands, 10 seconds)

```bash
cd ~/chinahospitalsguide

# 1. What's behind / ahead / local untracked / stash?
git fetch --all --prune 2>&1 | tail -5
echo "--- status ---"
git status -sb
echo "--- stash ---"
git stash list
echo "--- ahead/behind ---"
git rev-list --left-right --count HEAD...origin/master
```

**Decision tree:**

| Behind count | Stash present | Action |
|---|---|---|
| 0 | no | Nothing to sync — proceed to audit |
| 1+ | no | `git pull --ff-only origin master`, then audit |
| 0 | yes | DO NOT pop stash — surface to user, audit only what user pushed |
| 1+ | yes | `git pull --ff-only`, then surface stash contents to user separately |

**NEVER drop a stash without explicit user OK**. Stashes are usually abandoned
case work (e.g. Maria Rios pipeline work from 2026-07-07) and silently
deleting them is data loss.

## The 7 audit checks (run all 7, every audit round)

### Check 1: Schema is a JSON array

```bash
# For each language's index page, confirm schema opens with `[` not `{`
for f in index.html id.html ru.html ar.html; do
  echo "=== $f ==="
  grep -A 1 'application/ld+json' $f | head -3
done
```

**Expected**: First non-blank char after `<script type="application/ld+json">` is `[`.
**Bug signal**: Two adjacent `{...}{...}` blocks — Google Rich Results Test
will silently parse only the first object. **Already-fixed evidence**:
`index.html` since commit `abd00c3` (2026-07-11).

### Check 2: Lang-flag active state visibility

```bash
# The buggy form: inline rgba(255,255,255,0.X) that user can't see
grep -E 'class="lang-flag".*style=".*background:rgba\(255,255,255,0\.[0-9]+\)' \
  index.html id.html ru.html ar.html \
  id-pricing.html ru-pricing.html ar-pricing.html \
  id-contact.html ru-contact.html ar-contact.html
```

**Expected**: 0 hits. The active state should use `class="lang-flag active"`
+ a visible style block in `styles.css` (`.lang-flag.active { background: rgba(255,255,255,0.22); }`).
**Already-fixed evidence**: since commit `051016a` (2026-07-11).

### Check 3: hreflang completeness

```bash
# Every ML page must declare en + own-lang + x-default + every other lang's equivalent
# Count expected per file (e.g. index.html declares all 4 + x-default = 5)
for f in id.html ru.html ar.html \
         id-pricing.html ru-pricing.html ar-pricing.html \
         id-contact.html ru-contact.html ar-contact.html; do
  count=$(grep -c "hreflang" $f)
  echo "$f: $count hreflang tags"
done
```

**Expected counts** (as of 2026-07-11):
- `index.html` / `id.html` / `ru.html` / `ar.html`: 5 each (en + ru + ar + id + x-default)
- All `*-pricing.html` and `*-contact.html`: 5 each
- `index.html` declares its own lang as `x-default` (the canonical "default" landing)

**Bug signal**: count < 5 means incomplete hreflang set → SEO penalty.
**Already-fixed evidence**: since commit `1027384` (2026-07-11).

### Check 4: Centralized config coverage

```bash
# Find any hardcoded values that should live in _data/site.json
echo "=== PayPal client-id hardcoded? ==="
grep -lE 'BAAuEJ4aj4Glmel3a35W5yg1QY9idTSZt5LkxbWG' *.html *.njk 2>/dev/null
echo "=== WhatsApp number hardcoded? ==="
grep -lE '\+86.{0,3}157.{0,3}6310.{0,3}7083' *.html 2>/dev/null
echo "=== GA ID hardcoded? ==="
grep -lE 'G-RVYZENK472' *.html 2>/dev/null | wc -l
echo "(should match 1 = styles.css / _includes/head.njk; or = number of ML page files if template not used)"
```

**Expected**: PayPal client-id should appear in `_data/site.json` + `pricing.njk` (via `{{ site.paypalClientId }}` template) + `pricing.html` (build artifact). It should NOT appear in `pricing.njk` as a hardcoded literal — that's the wiring bug.

**Already-fixed evidence**: `_data/site.json` adds `paypalClientId` + `whatsapp` + `paypalButtons` keys since commit `1027384` (2026-07-11). BUT the wiring to templates is incomplete — see check 5.

### Check 5: "Added field, forgot to wire it up" trap

```bash
# Look for template usages of the centralized config
echo "=== Template uses site.paypalClientId? ==="
grep -rE 'site\.paypalClientId' _includes/ *.njk 2>/dev/null
echo "=== Template uses site.whatsapp? ==="
grep -rE 'site\.whatsapp' _includes/ *.njk 2>/dev/null
echo "=== Template uses site.paypalButtons? ==="
grep -rE 'site\.paypalButtons' _includes/ *.njk 2>/dev/null
```

**Expected after wiring**: All three return hits in `.njk` files.
**Current state (2026-07-11)**: 0 hits. The `_data/site.json` fields exist
but no consumer reads them — the centralization is a lie.

**The fix** (5 lines, 1 commit):
```yaml
# pricing.njk frontmatter, replace line 8 with:
extraHead: '<script src="https://www.paypal.com/sdk/js?client-id={{ site.paypalClientId }}&components=hosted-buttons&disable-funding=venmo&currency=USD&locale=en_US" async onload="window._ppLoaded=1;document.dispatchEvent(new Event(\'pp:loaded\'))" onerror="window._ppFailed=1;document.dispatchEvent(new Event(\'pp:failed\'))"></script>'
```
Then rebuild with `npx @11ty/eleventy` and verify with check 4 grep again.

### Check 6: Arabic nav RTL hack

```bash
grep -E 'nav-container.*style="direction:ltr"' ar.html ar-pricing.html ar-contact.html
```

**Expected**: 0 hits. RTL pages should use a CSS class (`.navbar.rtl` or
similar) to handle the EN|RU|AR|ID language strip display, not inline style
attribute (which only applies to the container, not the inner `ul/li`).

**Already-fixed evidence**: NONE as of 2026-07-11. Still on the todo list.

### Check 7: Multi-language pages schema parity

```bash
echo "=== Which ML pages have schema? ==="
for f in id-pricing.html ru-pricing.html ar-pricing.html \
         id-contact.html ru-contact.html ar-contact.html; do
  has_schema=$(grep -c "application/ld+json" $f 2>/dev/null || echo 0)
  echo "$f: schema=$has_schema"
done
```

**Expected**: All 6 return `schema=1` (or more — if multiple JSON-LD blocks).
**Current state (2026-07-11)**: All 6 return 0 — no schema at all on ML pricing/contact pages. SEO parity gap.

**The fix**: Copy the JSON-LD block from `index.html` lines 274-298 (the
MedicalBusiness + WebSite array) into each of the 6 ML pages, adjusting the
`url` field to the page's canonical URL.

## Done-condition: report format

After running all 7 checks, report in this structure to the user:

```
✅ Sync done: HEAD now <sha>, behind 0
✅ Stash: <list with status>
✅ Check 1 schema array: <pass/fail with line refs>
✅ Check 2 lang-flag active: <pass/fail>
✅ Check 3 hreflang: <pass/fail with counts>
✅ Check 4 centralized config: <pass/fail with line refs>
✅ Check 5 wired templates: <pass/fail — biggest signal>
✅ Check 6 AR RTL hack: <pass/fail>
✅ Check 7 ML schema parity: <pass/fail with per-file table>

🎯 Next priority items (P0/P1/P2):
- P0: ...
- P1: ...
- P2: ...

❓ Awaiting your call:
- Branch / commit / push direction?
- Any of these I can take a first pass on?
```

The user will either say "I made more changes, audit again" (loop) or give
specific items to fix. Do NOT preemptively open a branch or modify files.

## Audit frequency cheat sheet

- **Every commit the user makes**: re-run checks 1-7 (the diff may have
  introduced a regression in a check that previously passed).
- **Once per week** even if no commits: catch rot from upstream library
  updates (e.g. Eleventy 3.x or styles.css drift).
- **Before any deploy-related commit**: full audit + GitHub Actions build
  success in CI.
