---
name: programmatic-seo
description: "Patch tool pitfalls and size-limit workarounds for HTML article edits — verified 2026-06-12 through 2026-07-14."
version: 1.0.0
---

# Patch Tool Pitfalls (HTML Article Edits)

This reference covers three distinct patch-tool failure modes that hit during cron-run article edits. Each has been verified at least once and has a working workaround.

## Pitfall 1: HTML entities in `old_string` get decoded silently (verified 2026-06-12)

When patching an HTML file whose `old_string` contains an HTML entity like `&mdash;` (em-dash), `&hellip;` (ellipsis), `&nbsp;`, or `&rsquo;`, the patch tool's fuzzy matcher strips the entity back to the underlying character (`—`, `…`, ` `, `'`) before searching, so the literal `&mdash;` in `old_string` will never match the file's encoded form. Symptom: `Could not find a match for old_string in the file` even though the substring is plainly there.

**Fixes:**
1. Use the decoded character directly in `old_string` (e.g. `&mdash;` → `—`). This works as long as the underlying character is unique enough to match.
2. Use a SHORTER unique substring that does NOT contain the entity. This is more robust when the surrounding text repeats.

**Example failure:** trying to patch `directions as they actually sit in your home` (preceded by `&mdash;` 6 chars before) failed because the entity got decoded. Using `directions as they sit in your home` (the same 10-word string, no entity in the substring) succeeded on the second attempt. The general rule: when patching HTML, never include an HTML entity in `old_string` if you can avoid it.

## Pitfall 2: large `new_string` content silently drops the `path` parameter (NEW pitfall — verified 2026-07-14)

When patching an HTML file with `new_string` content larger than ~2000-3000 characters (a multi-paragraph section, an entire ordered list, a long FAQ block), the patch tool can fail with `{error: "path required"}` even though the JSON call clearly contains a `path` field.

**Symptom:** the tool returns `path required` for the FIRST call with the long content, but smaller subsequent patches with shorter content work fine. The agent typically loops 3-4 times with the same long content before realizing the chunk size is the problem.

**Root cause hypothesis:** the JSON serialization of the parameters array silently drops the `path` field when `new_string` exceeds a size threshold — likely a serialization buffer issue in the parameter marshalling, not a logic bug in the patcher itself. The patcher's per-call logic is sound; the JSON-to-internal-parameter mapping loses one field on long strings.

**Fix:** break the patch into smaller chunks, each with `new_string` under ~2000 chars. Practical unit sizes:
- A single `<li>` element
- A single `<p>` paragraph
- A single `<div class="faq-item">` block
- A single short heading + paragraph pair

**Detection:** the error message is literally `path required` — if you see it, retry with a smaller chunk.

**Belt-and-suspenders:** always include a short `old_string` (one line) and a short `new_string` (under 2000 chars) when patching HTML; never try to replace an entire 8-item ordered list in a single patch call.

**Verified sequence from 2026-07-14:** the city lot article body content required 6+ sequential patches to replace the body content; each successful patch was <2000 chars; each failed patch was 2500+ chars. The agent wasted 4 iterations before recognizing the size threshold.

**Same constraint applies to `old_string` length,** but the failure mode there is "could not find match" (the fuzzy matcher becomes over-permissive at long lengths and finds wrong matches) not "path required." Keep both fields under ~2000 chars for reliable behavior.

## Pitfall 3: Sibling-subagent write warning is non-fatal (verified 2026-06-15, recurred 2026-06-16)

The `patch` tool returns a warning like `"<file> was modified by sibling subagent 'UUID' but this agent never read it. Read the file before writing to avoid overwriting the sibling's changes."` when a parallel cron (or subagent) has modified a shared file (almost always `sitemap.xml`) since the current agent last read it.

This happens because cron jobs run on overlapping schedules and both can touch `sitemap.xml` within seconds. The warning is **non-fatal** — the patch may still apply cleanly — but it is a yellow flag.

**Verified fastest recovery (2026-06-16):** `head -15 sitemap.xml` is enough to confirm the patch landed correctly. If your entry is the only one at the top, proceed to commit. If two entries are interleaved (rare but possible), read the full file and re-patch the merged version.

**Preventive measure:** `read_file` the shared file IMMEDIATELY BEFORE the `patch`, not just at the start of the run. The patch tool's "have I read this file" check is timestamp-based, not session-based, so a sibling write between read and patch will trigger the warning.

## When to reach for this reference

Any time the patch tool returns `path required` or `Could not find a match for old_string` on an HTML file edit during cron-run article work, check this file FIRST. The fix is usually just chunk size or entity encoding, not a logic issue with the patch target.