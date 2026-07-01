# oriental-destiny.com Deployment Reference

(verified across 2026-06-XX daily cron runs)

This document captures deployment-specific patterns for oriental-destiny.com. The general cron run workflow lives in this skill's main SKILL.md; site-specific facts (filenames, branch names, research sources) live here.

## Repository

- GitHub: https://github.com/qzw-alt/oriental-destiny
- Local proxy required: port 10808 (HTTP)
- Git SSL backend: openssl (schannel fails in sandbox)
- Push pattern: `git -c http.sslBackend=openssl push`
- Branch: `main` (NOT `master` — the cron prompt says `master` but the actual deployed branch is `main`)

## SSH push setup

The oriental-destiny.com cron runs hit GitHub HTTPS auth failures on 2026-06-03, 2026-06-04, 2026-06-06. The 2026-06-06 troubleshooting run switched the remote to SSH (`git remote set-url origin git@github.com:qzw-alt/oriental-destiny.git`) using the existing `~/.ssh/id_ed25519` key. The 2026-06-07 cron run applied the **same SSH fix to chinahospitalsguide.com** (which had been failing on every cron since 2026-06-03 with the same auth error) and confirmed both fixes are durable. **If the push ever fails again, first check `git remote -v` — the URL should be `git@github.com:...` (SSH), not `https://github.com/...`.** If it has reverted to HTTPS, repeat the SSH switch.

## Cron prompt dead references

The oriental-destiny cron job prompt contains two references that look authoritative but are wrong. Both have been verified dead as of 2026-06-20:

1. **`seo-content-writer` skill (does not exist).** The cron prompt lists this as an attached skill. It is not in the Hermes library and is silently skipped on every run. The actual workflow is this skill (`programmatic-seo`) + `humanizer`. Ignore the `seo-content-writer` mention and proceed.

2. **`memories/layer3/research/competitor-research.md` (does not exist).** The cron prompt instructs the agent to read this file for research. That path returns "file not found" on every run. The actual research notes for this site live at:
   - `/home/ubuntu/.hermes/memories/layer3/research/article_topics.md` — high-traffic topic categories, content calendar by month, low-competition opportunities
   - `/home/ubuntu/.hermes/memories/layer3/research/terminology_mapping.md` — Chinese → English terminology mapping, Western SEO phrasing, banned romanization patterns

   Read both at the start of every run before picking the day's topic. The `article_topics.md` content calendar tells the primary + secondary topic for the current month (e.g. June = Summer Feng Shui / Fire Element).

## Article layout convention

- Articles sit at the **repo root** as `.html` files (not under `news/` or `blog/`)
- Filename convention is descriptive, not date-stamped: `feng-shui-bracelet-meaning.html`, `bazi-calculator-guide.html`, etc.
- The cron prompt's `fate-YYYY-MM-DD.html` filename is a recent (2026-06-02+) cron-specific convention, also at root, not under `news/`
- Each article uses `templates/fate-article-template.html` (in this skill's `templates/` directory) as a starting scaffold — copy and fill in bracketed placeholders

## Voice profile

- First-person, conversational, willing to use em dashes for asides
- "Leverage" and "actually" are AI-vocab (banned)
- Em-dash baseline: 10-18 per ~1200 words (verified 2026-06-02)

## Seasonal content threading

When the content calendar calls for a month-long theme (June 2026 = Fire Month / Summer), thread the daily articles through distinct sub-topics in a stable order. See SKILL.md "Seasonal content threading" section for the verified June 2026 sequence and the "Room walk completion milestone" + "Referenced-but-never-covered pivot" + "Thread close-out checklist" patterns.

## Related reference docs in this skill

- `references/site-audit-signals.md` — 5-call audit recipe for surfacing homepage/link/orphan-content issues before major content work (verified 2026-07-01 on chinahospitalsguide.com; pattern generalizes to any site)
- `references/content-matrix-overhaul.md` — full playbook for batch pillar work (11 pages + 49 augmented articles + cron prompt rewrite in one session)
- `references/cron-run-pitfalls.md` — operational pitfalls hit during daily cron runs
- `references/cron-read-secrets-block.md` — injection scanner constraint that affects skill attachment
- `references/push-credential-troubleshooting.md` — git push auth failures
- `references/humanize-score-script-pitfall.md` — em-dash cap and entity-decoding bug fixes
- `references/humanize-audit-false-positives.md` — `features`/noun-sense false positives in `humanize_audit.py`
- `references/site-configs.md` — per-site branch names, directories, sitemap conventions
