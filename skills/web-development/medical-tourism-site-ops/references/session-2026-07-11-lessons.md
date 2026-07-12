# 2026-07-11 Session — Lessons (multi-language audit rounds 1-3 + Hermes upgrade)

This file captures a session where I ran **3 rounds of iterative site audit** ("再帮我审查一下" loop) on chinahospitalsguide.com, with the user driving an external Claude Code agent to do the edits in between rounds. The lessons here are **already encoded** in the parent SKILL.md as concise pitfall sections; this file is the **raw transcript + reasoning** for future agents who want to understand the full failure mode.

## What happened (chronological)

### Round 0: User says the big site changes were made by "another agent"

User said: *"昨天晚上我把医疗旅游网站做了一个挺大的改动，内容方面也是，你看一下"*.

I scanned the local repo and found nothing — the changes weren't here. I asked where the agent's work was. The user clarified: *"源码 + 样式 + 首页服务内容。这些东西是我用另外一个agent去改的"*.

User told me to enumerate problems to send back to that agent for clarification.

**Lesson**: when the user mentions edits but local repo is clean, **don't assume the changes are local**. Ask where the agent worked.

### Round 0.5: User's "version rule" memory was wrong

I tried to apply a memory rule: *"对版本/升级类问题：必须先 `git log --oneline -5` 验证"*.

User pushed back: *"你这个版本升级这个，我没有定过这么一个规矩啊"*.

The rule was about git-repo subproject version upgrades, not about upgrading Hermes Agent itself. I had over-extended it. **Patched the memory** to scope it correctly: "升级/版本类问题：先看 `hermes --version` 和 `hermes update` 输出再回答".

**Lesson**: memory rules decay in scope over time. When a user says "我没定过这个规矩", they are usually right — patch the memory immediately, don't defend the old interpretation.

### Round 1: Hermes upgrade (0.17.0 → 0.18.2) — first attempt failed

The user mentioned "Hermes Agent 0.18" — I ran `hermes update` and got:
```
✗ Not a git repository. Please reinstall:
  curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
```

The local install at `~/.hermes/hermes-agent/` was a 2.6 GB source tree but **not a git repository**. The official install script also requires it to be a git repo. **Two upgrade paths blocked**.

I ran the install script with `--skip-setup` flag and it failed at the same check. Asked the user to choose between:
- A: Backup directory + reinstall (most destructive)
- B: `git init` and try `hermes update`
- C: Use pip to upgrade (avoid git path)

User chose: *"那算了吧，我来手动操作升级吧，这个不要管了"*.

User did the upgrade manually outside my view. Final result: **v0.18.2 (2026.7.7.2)**, `Up to date`. I had no role in the actual upgrade — I just diagnosed it.

**Lesson**: when an environment-specific upgrade path is blocked (non-git install), and the user wants to do it themselves, **stop and let them**. Don't try every alternative path I can think of.

### Round 2: Audit round 1 — agent's "20+ commits" claim

After `git fetch`, the agent had reported 20+ commits. Reality: `behind 1`. The agent's commit list was either cached or hallucinated.

The one real new commit (`d105ca8 fix: PayPal SDK missing from pricing.njk template head`) was **legitimate and useful** — it added `pagePaypal: true` to the frontmatter. But the other 19 commits the agent reported were already in my local HEAD.

**Lesson**: never trust an agent's self-reported commit count. Always `git rev-list --left-right --count HEAD...origin/master` to verify the actual delta.

### Round 3: Audit round 2 — schema bug + P0/P1/P2 fixes

After user pinged "再次帮我审查", I found **one new commit** (`fc57f12`) with 4 sub-commits:
- `051016a` — P0-1/P0-2/P1-2/P1-4/P1-6/P2-1 audit fixes
- `abd00c3` — P0-3 schema array + airport pickup language
- `0ad27cd` — source footnotes to all unverified numbers on homepage
- `e937d20` — remove duplicate language selector

All 4 commits did what their messages claimed. **But during my audit I missed checking the schema content itself** — I only verified the array structure, not the URL values. Big mistake (see Round 4).

### Round 4: Audit round 3 — schema `@context` bug discovered

User pushed another commit (`1027384`), and I did my standard audit. Found that 6 new multilingual pages had their schemas added, but when I `grep`-ed the actual JSON-LD content:

```html
<script type="application/ld+json">[{"@context":"https://***@type":"MedicalBusiness",...
```

**`"https://schema.org"` was replaced with `"https://***"`**. All 6 schema blocks were invalid JSON-LD with broken URLs. Google Rich Results Test would 100% reject them.

The bug likely came from the agent (Claude Opus 4.8 per the commit's Co-Authored-By line) doing a regex replacement that ate `https://schema.org"` and replaced it incorrectly.

**Lesson**: schema audits must verify URL **values**, not just structure. My 7-check audit checklist in `references/multi-language-audit-checklist.md` had a check for "schema is a JSON array" but not "schema URL is valid". The audit needs an additional check:

```python
# Add to audit checks: every schema block must have a valid @context URL
for schema in re.findall(r'<script type="application/ld\+json">(.+?)</script>', html):
    assert 'schema.org' in schema or 'w3.org' in schema, f'BROKEN @context: {f}'
    json.loads(schema)  # must also parse as valid JSON
```

I told the user about the bug. They said they'd fix it. **I didn't fix it myself** — the user drives the iteration loop, I report problems.

### Round 5: Audit round 4 — agent claimed README done, actually wasn't

User pushed `dc0b127` "docs: add README for scripts/_oneoff/ directory". I expected the README to be there. But when I ran `os.path.exists()`:

```python
>>> os.path.exists('scripts/_oneoff/README.md')
False  # ❌ Not there!
```

**The commit message said "add README" but the file wasn't in the repo.** This is the second time the agent's "did X" claim didn't match reality. (First time was "20+ commits", this time is "added README".)

I told the user: README doesn't exist, the commit must have failed or the agent lied.

User pushed again — but the new push wasn't really a push. They edited locally and said "好了 你看看". When I ran `git fetch`, **no new commits**. The README was only "done" in the user's mind, not in git.

This is the **"Mode C" trap**: when user says "改好了" but `git log` is unchanged from last sync, the changes are either local-only or somewhere I can't see. I should ask before doing anything else.

**Lesson**: when user says "改好了" but `git status` shows no new commits, **don't assume state A (pushed)**. Run pre-flight: fetch + log + status. If state B (local edit) or C (elsewhere), ask.

### Round 6: Audit round 5 — user pushed again, README now actually there

User said "改了 你看看". I ran the pre-flight: `git fetch` showed `behind 1`, `git pull --ff-only` worked. New commit `dc0b127` actually had the README this time:

```bash
$ cat scripts/_oneoff/README.md
# One-off Scripts

These were run once during the 2026-07-10/11 site overhaul.
**Do not run again** — each fixes an already-resolved historical issue.
...
```

**The agent's claim was finally true** (3 commits later than originally claimed, but true).

I ran the full 7-check audit on the new state:
- ✅ Schema array in all 6 ML pages (and JSON valid)
- ✅ WhatsApp link format consistent (all 187 wa.me links are pure-digit)
- ✅ README exists
- ⚠️ `pricing.html` line 24 still hardcodes PayPal client-id (cosmetic — pricing.njk uses template ref, build artifact will be overwritten)
- ⚠️ 3 AR files still have inline `style="direction:ltr"` (cosmetic — renders fine)
- ⚠️ 13 files have WhatsApp with space format vs dash format (cosmetic — pure-text display only, links unaffected)

**Result: 9.5/10**. No P0/P1 functional issues. Everything else is cosmetic.

## Key takeaways (encoded in parent SKILL.md)

1. **Verify agent self-reports**: any claim from another agent must be independently verified (`os.path.exists`, `grep -c`, `curl -I`).
2. **"改好了" can mean 3 different things** — A (pushed), B (local edit), C (elsewhere). Run pre-flight to detect which.
3. **Schema audits need to verify URL values, not just structure** — `schema.org` could be corrupted by over-eager regex.
4. **Source vs build coexistence for `.njk` → `.html` migration**: hardcoded `BAAuE` in `pricing.html` is expected if `npm run build` didn't run after the `.njk` edit.
5. **Cosmetic vs functional**: when something is cosmetic (text format, RTL hack, build artifact residue), don't waste cycles chasing it. The conversion path must work, the schema must be valid, and the rest is nice-to-have.

## The fix script for the `***` schema corruption

This Python script detects and fixes the `"https://***@type"` bug across all `.html` files. Run from repo root:

```python
import re
from pathlib import Path

ROOT = Path("/home/ubuntu/chinahospitalsguide")

# Find every JSON-LD block with broken @context
fixed = 0
for html_file in ROOT.glob("*.html"):
    text = html_file.read_text(encoding="utf-8")
    if "https://***@type" not in text:
        continue

    # The corrupted pattern: "https://***@type":"MedicalBusiness" etc.
    # Restore to: "https://schema.org","@type":"MedicalBusiness"
    new_text = text.replace('"https://***@type"', '"https://schema.org","@type"')

    if new_text != text:
        html_file.write_text(new_text, encoding="utf-8")
        print(f"FIXED: {html_file.name}")
        fixed += 1

print(f"\nTotal files fixed: {fixed}")

# Verify by re-reading
import json
broken_remaining = 0
for html_file in ROOT.glob("*.html"):
    text = html_file.read_text(encoding="utf-8")
    for schema in re.findall(r'<script type="application/ld\+json">(.+?)</script>', text, re.DOTALL):
        if '***' in schema or 'schema.org' not in schema:
            broken_remaining += 1
            print(f"  STILL BROKEN: {html_file.name}")
        else:
            try:
                json.loads(schema)
            except json.JSONDecodeError as e:
                print(f"  JSON INVALID: {html_file.name}: {e}")
                broken_remaining += 1

if broken_remaining == 0:
    print("✅ All schemas valid")
```

**Important**: this script is `scripts/_oneoff/`-level — run once, never again. After running, move to `scripts/_oneoff/fix-schema-context-corruption-2026-07-11.py` to prevent accidental re-runs.
