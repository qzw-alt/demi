# JSON-LD Typo and `replace_all` Destruction Pitfalls

Verified 2026-07-29, chinahospitalsguide.com China 2026-30 TCM five-year plan article. Both pitfalls occurred in the same cron run, costing 6 extra tool calls on recovery. The SKILL.md carries one-line pointers; this file has the full transcript and decision rules.

## Pitfall 1: JSON-LD `"@type": "Text"` typo in FAQPage answers

When writing a FAQPage `acceptedAnswer` block from scratch, the schema.org `"@type"` value must be `"Answer"` (not `"Text"`). The two are visually similar and the FAT-FINGER risk is high when typing 5 FAQ entries in sequence.

**What the 07-29 typo block looked like (broken):**
```json
{
  "@type": "Question",
  "name": "Does China's 2026-30 TCM plan affect international patients?",
  "acceptedAnswer": {
    "@type": "Text": "Yes. The plan reinforces what foreign patients already see..."
  }
}
```

**What the correct block should look like:**
```json
{
  "@type": "Question",
  "name": "Does China's 2026-30 TCM plan affect international patients?",
  "acceptedAnswer": {
    "@type": "Answer",
    "text": "Yes. The plan reinforces what foreign patients already see..."
  }
}
```

**Why it matters:** the entire FAQPage block becomes invalid; Google's rich-result eligibility is lost; the article's Q&A may not appear in search results.

## Pitfall 2: `replace_all=true` on JSON-LD key-value pairs silently strips adjacent text content

The natural fix for a typo that appears 5 times in 5 different surrounding contexts is `replace_all=true`. **Don't do this for JSON-LD key-value pairs.** The patch tool's regex matches the `"@type": "Text"` token PLUS the trailing text content as one continuous token, then replaces it with just the corrected key, silently destroying the answer text.

**What happened on 07-29:**
- old_string: `"@type": "Text": "Yes. The plan..."` (collapsed to `"@type": "Text"` as the search anchor)
- new_string: `"@type": "Answer",`
- Result: all 5 FAQ entries lost their answer text. Each entry now reads `"acceptedAnswer": { "@type": "Answer", }` with no `text` field.

**Recovery took 6 tool calls:** 1 detection call (read_file showing the empty text fields) + 1 destructive patch + 5 individual restore patches (one per Q&A entry).

## Decision rules

When a JSON-LD typo appears N times in different surrounding contexts, choose one of:

1. **N individual `patch` calls** with enough surrounding context (the question name + 1-2 lines) to make each match unique. Slowest (2N+1 tool calls), safest.
2. **Rewrite the entire schema block in one `write_file` call** (read_file first to grab the current block, then write_file the corrected version). Fastest (1 tool call), requires reading then writing the whole file.
3. **`replace_all=true` only when the matched token has zero content after it** — for example, fixing a repeated banned word in body prose (`actually` → `in fact` with replace_all works because the replacement is 1:1 with no surrounding context to strip). NEVER use `replace_all=true` on `"@type": "<value>"` key-value pairs in JSON-LD.

## Detection recipe (3 lines)

After any `write_file` or `patch` that writes a JSON-LD block, run:

```bash
grep -E '"@type": "(Text|FAQPage|Question|Answer)"' FILE
```

Expected output:
- 1 `"@type": "FAQPage"` entry
- N `"@type": "Question"` entries (one per Q&A)
- N `"@type": "Answer"` entries (one per acceptedAnswer)
- 0 `"@type": "Text"` entries

Any `"@type": "Text"` hit means the typo is present. Any mismatch between the count of `"@type": "Question"` and `"@type": "Answer"` entries means a `replace_all` destruction happened and answer text is missing.

## Cost of getting it wrong

- Recovery loop: 6-10 tool calls
- Publishable JSON-LD bug if not caught: Google rich-result loss; Q&A content invisible to crawlers
- The bug is silent — the article still renders, the body still reads correctly, only the structured-data layer is broken

## Related

- The `@@type` (double-`@`) sibling pitfall is in the parent SKILL.md, "Article template pitfalls" section — same schema.org context, different typo
- The `humanizer` skill's `@@type` rule applies to all 5 schema-org types (Article, FAQPage, Question, Answer, Organization), not just the `publisher` block