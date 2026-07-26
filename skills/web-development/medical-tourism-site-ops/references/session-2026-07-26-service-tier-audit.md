# Session 2026-07-26 Lessons — Service-Tier Rename + Mobile Bar Audit

**Source session**: 2026-07-26 — multi-round audit of `chinahospitalsguide.com` service tier rename + mobile bar coverage.

**Trigger**: user said "服务流程是否合理，能否增加中间档" → we collaborated on a 3-tier pricing plan (`planning/pricing-redesign-2026-07-24.md`), then over 7 commits the user rolled out the rename site-wide and asked for audit after each batch.

**What this session taught** that the parent SKILL.md did NOT yet capture:

1. **Eleventy audit must scan BOTH `.html` AND `.njk`** — verified across 5 audit rounds.
2. **`.html`/`.njk` dual-track bug** — "ci: deploy" commits only renamed source, never re-built; **fix = delete `.html` at repo root**.
3. **Multi-pass audit pattern** — produce delta tables, not just point-in-time snapshots.
4. **Shared UI components (mobile bar) belong in `_includes/`, NOT per-template HTML** — verify with `grep "{% include"` after add.
5. **Commit message typos mislead audit** — verify against actual file content.

## The 7-commit sequence (user's side)

| Commit | Type | Real action | Real vs claimed |
|---|---|---|---|
| `022f1b3` | `fix` | Add `$149` mention to 4 landing pages | Matches |
| `3f109d1` | `fix` | Rename 3 "Pre-Arrival" terms in `about.njk` | Matches |
| `508a39f` | `chore` | Delete 6 `.html` files (served by `.njk`) | Matches (structural fix) |
| `c820efc` | `chore` | Delete `services.html` | Matches |
| `c873029` | `fix` | Replace natural-language "pre-arrival" with "pre-travel" | Matches |
| `21f9188` | `ci` | "force rebuild to flush all caches" | **Questionable** — did it actually rebuild? |
| `91ecd73` | `fix` | Update `inject-schema.js` with L1/L2/L3 names + Offers schema | Matches |
| `b046c25` | `fix` | Symmetric layout for "What Only China Can Do" cards | Matches |
| `f53baca` | `fix` | Add mobile-bottom-bar to 3 multi-language pricing pages | Matches (only .html, not .njk) |

The 5-audit-round sequence (my side):

| Round | Scan target | Conflict count | Surprise |
|---|---|---|---|
| 1 | `.html` only | 51 mentions / 12 files | First baseline |
| 2 | `.html` after pull | 49 / 11 | Stories.html now renamed |
| 3 | `.html` + `.njk` (first time) | 9 / 6 | **Discovered**: `.njk` templates had the rename already, `.html` was the stale build artifact |
| 4 | Same + delete verification | 9 / 6 | All 7 user-initiated commits verified |
| 5 | Both, plus mobile-bottom-bar coverage | 1 / 1 (natural language) | Final state |

## Why round 3 was the breakthrough

Until round 3, I assumed `.html` files were the source of truth and was renaming strings in them. The 4 CI "deploy" commits (`b47de7b` / `a7bf243` / `414a4f7` / `b306ec5`) **claimed** to deploy the rename across all pages, but a closer look at `_site/` (when the user eventually confirmed `npm run build` did run) revealed the build had succeeded and the `.html` files at repo root had **also** been renamed — just not all of them.

The user's **structural fix** (commit `508a39f`) was decisive: **delete the `.html` files, keep only the `.njk`**. After that, the dual-track problem disappeared.

## The `mobile-bottom-bar` failure mode (verified live)

`_includes/mobile-bottom-bar.njk` was created (in `_includes/` directory), the CSS was added to `styles.css` (or as inline blocks per template), but **0 of 8 core `.njk` templates** included the partial:

```
about.njk: NO
contact-new.njk: NO
contact.njk: NO
hospitals.njk: NO
how-it-works.njk: NO
index.njk: NO
pricing.njk: NO
services.njk: NO
```

**Result**: a future `npm run build` would regenerate `.html` files that lose their hand-written mobile bars.

**The fix** (when user applies it): add `{% include "mobile-bottom-bar.njk" %}` to every `.njk` template that should have a mobile bar, BEFORE the next build.

## Distinguishing "档名/产品名" from "natural-language description"

Same characters, different meanings. The audit must distinguish:

| Expression | Meaning | Action |
|---|---|---|
| `Hospital Match` | Old tier name (L1) | Rename to `Hospital Shortlist` |
| `Hospital Matching` | Natural language (action: "we are matching you with a hospital") | Keep |
| `Hospital matches` | Natural language (noun: "2-3 hospital matches + cost comparison") | Keep |
| `Pre-Arrival Service` | Old tier name in product context | Rename to `Pre-Travel Service` |
| `pre-arrival planning` | Natural language (description of L3 work) | Rename to `pre-travel planning` (consistency) |
| `pre-arrival video consultation` | Product sub-item (case-sharing program) | Rename to `pre-travel video consultation` |

**Audit regex patterns**:

```python
patterns = {
    'Hospital Match (tier name)': r'Hospital Match(?!ing)',   # not followed by 'ing'
    'Hospital Matching (natural language)': r'Hospital Matching',
    'hospital matches (natural language)': r'hospital matches',  # lowercase
    'Pre-Arrival Service (tier name)': r'Pre-Arrival Service',
    'pre-arrival (natural language)': r'pre-arrival',  # lowercase, may include 'planning' etc.
}
```

Show file context for each match — if the surrounding words are "matching" or "matches" or describe a process, it's natural language; if it's the tier name in a heading or product list, it's a real rename target.

## The 7 user-driven audit messages (verbatim, for future signal-detection)

1. "对比下目前网站的服务描述" — first audit request
2. "再次确认一遍 然后写一份指导报告给我" — multi-pass audit + report
3. "已修改完 你审计一下" — round 1 of fixes
4. "再次修改完了 你再看看" — round 2
5. "手机端我也做了修改" — round 3 (focus on mobile)
6. "我先看一下，再想想，后续我们再定" — break-the-loop signal, archive
7. "好了 又改好了 你再审查一下" — round 4

The "再看看" / "再次审计" / "再审查一下" pattern is **iterative audit** — same content, multiple passes. Pre-cooked script + delta computation is the right answer, not rebuilding the audit each time.

## The mobile-bottom-bar audit recipe (canonical)

```bash
# 1. Check which .html files have the bar (built or hand-written)
for f in *.html; do
  echo "$f: $(grep -c 'mobile-bottom-bar' "$f")"
done

# 2. Check which .njk files include the partial
for f in *.njk; do
  echo "$f: $(grep -c '{% include "mobile-bottom-bar' "$f")"
done

# 3. Check _includes/ for the partial definition
ls _includes/*.njk

# 4. Cross-reference: is the partial referenced by every .njk that should render it?
```

For 8 .njk templates and 1 partial, expected output:
- 8 templates × 0 includes → bug (no template uses the partial)
- 8 templates × 1 include → fixed

## Final state (2026-07-26, end of session)

| Aspect | Status |
|---|---|
| 3-tier pricing in `.njk` | ✅ pricing.njk, contact-new.njk, services.njk, thank-you.html, ar-pricing.html, id-pricing.html, ru-pricing.html |
| 3-tier pricing in remaining `.html` | ⚠️ 8 .njk source files reference it, but no .html output committed (build not run yet) |
| Pre-Arrival natural language | ✅ 0 remaining |
| Hospital Match tier name | ✅ 0 remaining (1 "hospital matches" natural language kept intentionally) |
| Mobile bottom bar in `.njk` | ❌ 0/8 templates include the partial |
| Mobile bottom bar in `.html` | ✅ 14 hand-written, ⚠️ will be lost on next build |
| commit `528e891` price typo | ⚠️ Confirmed typo, not real prices |

## The "再看看" → delta computation recipe

```python
# Save previous audit result
import json
prev = json.loads(Path('audit-prev.json').read_text())
curr = json.loads(Path('audit-curr.json').read_text())

# Compute delta
changes = []
for file, hits in curr.items():
    if file not in prev:
        changes.append((file, 'NEW', hits))
    elif hits != prev[file]:
        diff = {k: (prev[file].get(k, 0), v) for k, v in hits.items() if prev[file].get(k, 0) != v}
        changes.append((file, 'CHANGED', diff))

print(f'Files changed since last audit: {len(changes)}')
for f, kind, content in changes[:5]:
    print(f'  {kind}: {f}')
    print(f'    {content}')
```

Or simpler: just store the conflict count over rounds and report the delta each round.

## What the user said about workflow (signals for future)

- "我先看一下，再想想，后续我们再定" — **break the loop**, don't keep pushing
- "你说了这么多选择 但是我现在让你做" — **state assumptions, then commit to one** (over-paragraphed options in `clarify` confuse the user)
- "你问" — **they want to be asked before drafting**, not after
- "你帮我写一份回复" — **the actual draft is what they want, not 4-question preflight**; preflight only when the answer is genuinely undetermined
- "今天 5 分钟内" — **time pressure exists**, default to short output

## What this session did NOT cover (still gaps)

- **The actual `_includes/mobile-bottom-bar.njk` include patch** — not done, would be a follow-up commit
- **The .njk ↔ .html sync problem resolution** — depends on whether the user wants `_site/`-only or repo-root `.html` tracking
- **Mobile bar language variants** — current partial is English-only; needs `mobile-bottom-bar-ar.njk`, `id.njk`, `ru.njk` for multi-language sites
- **3-tier pricing page verification on build** — once `_includes/` includes land, need to run `npm run build` and curl-verify each pricing page
- **The 8 `.njk` files that should include `mobile-bottom-bar.njk`** — actual list (about, contact-new, contact, hospitals, how-it-works, index, pricing, services)

## Takeaways (encoded in parent SKILL.md already)

1. Always scan both `.html` and `.njk` in one Python pass
2. Distinguish tier-name vs natural-language (regex with negative lookahead)
3. Shared components live in `_includes/` only
4. Commit message can lie; verify against file content
5. Multi-pass audit = delta computation, not new audits
6. **`.html` at repo root is a build artifact** — delete if `.njk` generates it (decisive fix)

End of session notes.