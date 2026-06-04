# Humanizer in SEO Article Pipelines

`humanizer` runs as a **required step** in recurring content pipelines, not just ad-hoc use.

## Pipeline usage pattern

Both active article cron jobs use it:
- `daily-medical-news` (chinahospitalsguide.com) — Chinese articles
- `daily-oriental-destiny-article` (oriental-destiny.com) — English articles

```markdown
1. Research → 2. SEO write → 3. Humanize ← this step ← 4. Publish → 5. Update sitemap → 6. Push
```

**Scoring rule (pipeline-enforced):** score must be >60. If ≤60, revise article and re-score until it passes. Do NOT skip or bypass this step regardless of time pressure.

## SEO content characteristics

When humanizing SEO articles in these pipelines, additional considerations:
- **Keyword density**: Don't strip keywords aggressively — preserve target terms naturally embedded
- **Headings**: SEO articles use Title Case headings — don't "correct" these to sentence case (that would be an editing choice, not an AI pattern)
- **Structure**: H2/H3 hierarchy is intentional for SEO — preserve it
- **Internal links**: Leave anchor text intact, don't humanize away contextual links
- **Length**: SEO articles are 800-1500 words. Don't aggressively compress — maintain word count for ranking signals

## Feng Shui / Bazi English Terminology (for English SEO articles)

When writing or humanizing English feng shui content (oriental-destiny.com), use native English terms — NOT direct Chinese translations:

| ❌ Wrong (direct translation) | ✅ Correct (native English/Western standard) |
|-------------------------------|----------------------------------------------|
| "Chi" | **Qi** — pinyin, dominant in Western usage; "Chi" is archaic |
| "Energy" (generic) | **Qi** — or "life force" contextually; never just "energy" |
| "Wind Water" | **Feng shui** — never translated, always proper noun |
| "Dark/bright side" | **yin and yang** — two words, lowercase |
| "Eight Trigrams" | **Bagua** — pinyin, preserved |
| "Five Elements" | **Five Elements** or **Wu Xing** (academic) |
| "Daoist" | **Taoist** — more common in Western publications |
| "Yijing" | **I Ching** — capitalized, popular usage |
| "Great polarity" | **Great Ultimate** or **Tai chi** |
| "Luo pan compass" | **Luo pan** or **feng shui compass** |
| "Dragon vein" | **dragon vein** — correct Western term |

### Western SEO article structure for feng shui
- Title: `"Feng Shui [Topic] Guide"` or `"[Number] Tips"`
- H2 subheadings with numbered lists (e.g., `"5 Feng Shui Tips for Your Bedroom"`)
- 800–1500 words for guides, 1200–1800 for room-specific
- FAQ section with schema markup at the end
- Meta description 150–160 characters with keyword

### Top feng shui article themes (high traffic, low competition)
- "Feng Shui for Specific Life Areas" (career, relationships, health)
- "Feng Shui Cures" (common problems and solutions)
- "Bathroom Feng Shui" (most competitors avoid — opportunity)
- "Bagua Map Guide", "Flying Star Feng Shui", "Qi Energy"
- "Yin and Yang Balance"

Research files: `memories/layer3/research/terminology_mapping.md` and `article_topics.md`

## What to watch for extra in SEO content

Beyond the 29 patterns, SEO articles commonly carry:
- **Overuse of the target keyword in first paragraph** (rewrite for natural placement)
- **"Click here" or "learn more" CTA patterns** (natural: "read more", "see the full guide")
- **Thin intro paragraphs that repeat the H1** (condense or rewrite)
- **Conclusion paragraphs that restate the intro** (merge or cut)
- **Title Case headings** — do NOT "correct" to sentence case; preserve for SEO