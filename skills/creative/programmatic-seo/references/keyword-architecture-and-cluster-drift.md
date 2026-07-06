# Keyword architecture: primary keyword template + cluster-drift detection

Companion to the umbrella `programmatic-seo` skill. The umbrella SKILL.md exceeded its 100KB limit, so the keyword architecture recipe lives here.

## The primary-keyword template

```
[Primary Keyword]: [Long-tail Hook] | <Site Name>
```

- **Primary Keyword** = `X <Head Term>` where `<Head Term>` is the cluster-defining word (`Feng Shui` / `BaZi` / `Destiny` for oriental-destiny.com; a disease or procedure + site anchor for chinahospitalsguide.com).
- `X` = a concrete topic object — a place, an object, a solar term, a demographic, a sub-technique. NOT a temporal adverb alone (`Eve` / `Morning` / `Tonight`), NOT a vague container word.
- **Long-tail Hook** = a scene-setting qualifier that adds specificity without competing with the Primary Keyword.

### Examples (✅ / ❌)

| Pattern | Status | Why |
|---|---|---|
| `Front Garden Feng Shui for July: What to Do in the Fire-to-Earth Transition` | ✅ | X = "Front Garden" (concrete), head term = "Feng Shui" |
| `Li Qiu Feng Shui: What to Do on the Eve Before the Fire-to-Earth Handoff` | ✅ | X = "Li Qiu" (solar term — concrete), head term = "Feng Shui" |
| `Li Qiu Eve: The Night Before the Fire-to-Earth Handoff` | ❌ | X = "Li Qiu Eve" (temporal adverb only), head term "Feng Shui" DROPPED |
| `July Outdoor Reading` | ❌ | No head term, no concrete object — pure noise |

## Why this matters (verified 2026-07-06)

A site publishing daily articles builds topical authority as a **cluster**, not isolated pages. Google's topical-authority signal rewards sites where many pages share a head term and branch outward via the `X` axis.

The oriental-destiny.com July thread is the canonical example:

```
07-01: Front Garden Feng Shui for July: ...
07-02: Back Garden Feng Shui for July: ...
07-03: Balcony Feng Shui for July: ...
07-04: Rooftop Terrace Feng Shui for July: ...
07-05: Outdoor Feng Shui Close-Out: ...
07-06: Li Qiu Feng Shui: ...           ← THE FIX (was: "Li Qiu Eve")
```

The 07-06 article shipped with `Li Qiu Eve` as primary keyword — a phrase with effectively zero search volume, and worse, the article was supposed to **cap** the July thread. The body content was correct; the headline and meta were disconnected from the cluster, so the cluster broke at its most important article.

The fix was surgical — replace the keyword in five places that all move together (see checklist below). Body content untouched.

## Five-place-edit checklist (the keyword-fix recipe)

When fixing a ship-already article's primary keyword, edit ALL of these in a single multi-line `patch`:

| # | Location | Edit |
|---|---|---|
| 1 | `<title>` | Replace the keyword phrase |
| 2 | `<meta name="description">` content | Primary Keyword in first sentence |
| 3 | `<meta property="og:title">` content | Same as title |
| 4 | `<meta property="og:description">` content | Same wording pattern as description |
| 5 | `<h1>` (and `.subtitle` if it carries the keyword) | Same as title |
| 6 | `schema.org` JSON-LD `"headline"` and `"description"` | Same as title + description |

**Pitfall: do NOT add a `<meta name="keywords">` tag.** Google has ignored it since 2009, and the prior 5 articles on the cluster don't have one. Consistency with the existing template matters more than a 0-impact tag.

**Pitfall: there should be exactly ONE `<title>` tag.** When patching, double-check you don't leave a duplicate — the diff tool won't flag it, but the browser picks an arbitrary one and SEO suffers. The 2026-07-06 fix accidentally created a duplicate `<title>` mid-patch and had to follow up with a second patch.

**Pitfall: when the cron prompt and the repo disagree on branch name, the push fails.** The 2026-07-06 fix verified the deployed branch is `main` (`git symbolic-ref refs/remotes/origin/HEAD`) before pushing, even though the prompt said `master`. Always verify before `git push`.

## Cron-prompt hardening (HARD RULE block)

If you control the cron prompt, add a HARD RULE block at the top:

```
## 关键词模板 (HARD RULE)

每篇文章的 <title>, <h1>, og:title, schema.org headline 必须按:

  [Primary Keyword]: [Long-tail Hook] | Oriental Destiny

Primary Keyword = X Feng Shui / X BaZi / X Destiny 形态
X = 具体对象 (Front Garden / Li Qiu / Bedroom), 不能是纯时间副词 (Eve / Morning)
描述首句必须出现 Primary Keyword

✅ `Front Garden Feng Shui for July: ...`
❌ `Li Qiu Eve: ...`  (主词 Feng Shui 缺失)

写完自查: grep -oE '<title>[^<]+</title>' fate-YYYY-MM-DD.html, 不匹配就重写
```

The ✅/❌ side-by-side is what survives prompt compression. Without it, cron agents re-introduce the same drift pattern within 1-2 runs.

## Cluster-drift detection (post-publish)

```bash
cd <repo>
# Coherence check — last 7 titles in one shot
for f in $(ls -t fate-*.html | head -7); do
  echo -n "$(basename $f): "
  grep -oE '<title>[^<]+</title>' "$f" | head -1
done
```

If today's title is the odd one out (no shared head term with the prior 6), the cluster has fractured. Rewrite the headline before the next cron run, or — if it already shipped — apply the five-place-edit checklist above.

### The shared-head-term test (more rigorous)

```bash
prior_head=$(for f in $(ls -t fate-*.html | head -6 | tail -5); do
  grep -oE '<title>[^<]+</title>' "$f" | head -1
done | grep -oE 'Feng Shui|BaZi|Destiny|Tarot' | sort | uniq -c | sort -rn | head -1 | awk '{print $2}')
today=$(grep -oE '<title>[^<]+</title>' fate-$(date +%Y-%m-%d).html | head -1)
echo "Cluster head: $prior_head"
echo "Today:        $today"
# If $prior_head doesn't appear in $today, the cluster is fractured.
```

### Cron-side enforcement

The cron-side enforcement pattern (template self-check before de-AI gate) lives in `seo-article-publish-cron` skill under "Primary keyword and headline template (HARD RULE)". That skill is the right place to enforce; this file is the right place to design the template.

## Origin

This recipe is verified against the 2026-07-06 fix of `fate-2026-07-06.html` on oriental-destiny.com — commit `dcab9c1`, branch `main`, push `79e4391..dcab9c1 main -> main`. Before fix: title was `Li Qiu Eve: The Night Before the Fire-to-Earth Handoff`. After fix: `Li Qiu Feng Shui: What to Do on the Eve Before the Fire-to-Earth Handoff`. Body unchanged.