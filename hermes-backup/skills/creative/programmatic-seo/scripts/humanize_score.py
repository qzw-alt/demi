#!/usr/bin/env python3
"""
Humanize score for programmatic-seo articles.

Runs the humanizer skill's audit rules as a deterministic 0-100 score,
penalising the patterns most likely to slip into daily articles. The
oriental-destiny banned-vocab list and em-dash baseline are baked in;
override the BAN list for other sites via flags.

Usage:
    python humanize_score.py <article.html> [--site oriental-destiny] [--threshold 60]

Returns exit code 0 if score > threshold, 1 otherwise. Prints a short
breakdown so the agent can see which patterns fired.

This is a SCORING HARNESS, not a replacement for reading the humanizer
SKILL.md. The patterns that get penalised are listed in the humanizer
skill's "29 patterns" reference. If a pattern fires here, the fix is
in the skill, not in this script.
"""

import argparse
import re
import statistics
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

# Site-specific overrides
SITE_CONFIG = {
    "oriental-destiny": {
        # Banned vocab from references/oriental-destiny-deployment.md
        "banned": [
            "leverage", "leveraging", "leverages",
            "actually", "crucial", "pivotal",
            "delve", "delving", "tapestry",
            "underscore", "vibrant", "showcase",
            "intricate", "intricacies", "interplay",
            "navigate", "garner", "enduring", "enhance",
            "fostering", "valuable", "embark", "beacon",
        ],
        # Em-dash budget per ~1200 words. oriental-destiny baseline is
        # 10-18 (deliberate stylistic choice); penalty only at extremes.
        "em_dash_low": 4,
        "em_dash_high": 25,
    },
    "chinahospitalsguide": {
        "banned": [
            "leverage", "leveraging", "leverages",
            "actually", "crucial", "pivotal",
            "delve", "delving", "tapestry", "underscore",
            "vibrant", "showcase", "intricate", "interplay",
            "navigate", "garner", "enduring", "enhance",
        ],
        # Em-dash cap raised from 12 to 23 (2026-06-06 patch). The
        # old value 12 was below the verified site baseline of
        # 17-23 em-dashes per 1200 words documented in SKILL.md, so
        # every published-style article on the site was getting a
        # false "em-dashes too many" penalty. Patched after the
        # 2026-06-05 and 2026-06-06 cron runs both confirmed the
        # discrepancy (densities 10.2 and 19.4/1200 respectively).
        "em_dash_low": 4,
        "em_dash_high": 23,
    },
}

# General AI vocab from the humanizer skill's "AI Vocabulary" pattern
GENERAL_AI_VOCAB = [
    "additionally", "align with", "crucial", "delve", "emphasizing",
    "enduring", "enhance", "fostering", "garner", "highlight",
    "interplay", "intricate", "landscape", "pivotal", "showcase",
    "tapestry", "testament", "underscore", "valuable", "vibrant",
]

# Patterns from humanizer SKILL.md sections 1, 3, 6, 7, 9, 22, 23, 25
AI_PATTERNS = {
    "testament": r"\btestament\b",
    "serves_as": r"\bserves as\b",
    "stands_as": r"\bstands as\b",
    "evolving_landscape": r"\bevolving landscape\b",
    "navigate_the": r"\bnavigate the\b",
    "important_to_note": r"\bit is important to note\b",
    "in_conclusion": r"\bin conclusion\b",
    "furthermore": r"\bfurthermore\b",
    "moreover": r"\bmoreover\b",
    "in_todays": r"\bin today.?s\b",
    "in_the_heart_of": r"\bin the heart of\b",
    "nestled": r"\bnestled\b",
    "showcases": r"\bshowcases\b",
    "delve": r"\bdelve[sd]?\b",
    "leverage": r"\bleverage[sd]?\b",
    "tapestry": r"\btapestry\b",
}

FILLER_PHRASES = [
    "in order to", "due to the fact", "at this point in time",
    "in the event that", "it is important to note", "in conclusion",
    "furthermore", "moreover", "the future looks bright",
    "exciting times lie ahead", "journey toward",
]

SYCOPHANTIC = [
    "great question", "absolutely right", "excellent point",
    "i hope this helps", "let me know if you",
    "would you like", "of course!",
]


HTML_ENTITY_DECODE = {
    "&mdash;": "\u2014", "&ndash;": "\u2013", "&hellip;": "\u2026",
    "&amp;": "&", "&lt;": "<", "&gt;": ">", "&quot;": '"', "&apos;": "'",
    "&nbsp;": " ", "&rsquo;": "\u2019", "&lsquo;": "\u2018",
    "&rdquo;": "\u201d", "&ldquo;": "\u201c",
}


def decode_html_entities(text: str) -> str:
    """Decode common HTML entities so em-dash counts etc. work on entity-encoded text."""
    for entity, char in HTML_ENTITY_DECODE.items():
        text = text.replace(entity, char)
    # Numeric entities &#8212; (em-dash) etc.
    text = re.sub(r"&#(\d+);", lambda m: chr(int(m.group(1))) if int(m.group(1)) < 0x110000 else m.group(0), text)
    text = re.sub(r"&#x([0-9a-fA-F]+);", lambda m: chr(int(m.group(1), 16)) if int(m.group(1), 16) < 0x110000 else m.group(0), text)
    return text


def extract_article_body(html: str) -> str:
    """Strip HTML and grab the article body. The site's articles use
    multiple <article> blocks (one per H2 section), so concatenate ALL of
    them, not just the first. Fall back to full HTML if no <article> tags."""
    articles = re.findall(r"<article[^>]*>(.*?)</article>", html, re.DOTALL)
    if not articles:
        src = html
    else:
        src = " ".join(articles)
    text = re.sub(r"<style[^>]*>.*?</style>", " ", src, flags=re.DOTALL)
    text = re.sub(r"<script[^>]*>.*?</script>", " ", text, flags=re.DOTALL)
    text = re.sub(r"<!--.*?-->", " ", text, flags=re.DOTALL)
    text = re.sub(r"<[^>]+>", " ", text)
    text = decode_html_entities(text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def word_count(text: str) -> int:
    return len(text.split())


def count_hits(pattern: str, text: str, flags: int = re.IGNORECASE) -> int:
    return len(re.findall(pattern, text, flags))


def sentence_lengths(text: str) -> list[int]:
    sentences = re.split(r"(?<=[.!?])\s+", text)
    return [len(s.split()) for s in sentences if s.strip()]


def score(html: str, site: str = "oriental-destiny") -> dict:
    cfg = SITE_CONFIG.get(site, SITE_CONFIG["oriental-destiny"])
    text = extract_article_body(html)
    wc = word_count(text)

    score_val = 100
    notes = []

    # 1. Banned vocab (heavy penalty - site-specific)
    for w in cfg["banned"]:
        hits = count_hits(rf"\b{re.escape(w)}\b", text)
        if hits:
            score_val -= 8 * hits
            notes.append(f"BANNED '{w}' x{hits}")

    # 2. General AI vocab (lighter penalty)
    for w in GENERAL_AI_VOCAB:
        if w in cfg["banned"]:
            continue
        hits = count_hits(rf"\b{re.escape(w)}\b", text)
        if hits:
            score_val -= 5 * hits
            notes.append(f"AI-vocab '{w}' x{hits}")

    # 3. Specific AI patterns
    for label, pat in AI_PATTERNS.items():
        hits = count_hits(pat, text)
        if hits and label not in {w for w in cfg["banned"]}:
            score_val -= 4 * hits
            notes.append(f"pattern '{label}' x{hits}")

    # 4. Em-dash budget
    em = text.count("\u2014")
    if em > cfg["em_dash_high"]:
        over = em - cfg["em_dash_high"]
        score_val -= 2 * over
        notes.append(f"em-dashes too many: {em} (high={cfg['em_dash_high']})")
    elif em < cfg["em_dash_low"]:
        score_val -= 2 * (cfg["em_dash_low"] - em)
        notes.append(f"em-dashes too few: {em} (low={cfg['em_dash_low']})")

    # 5. -ing analysis tails (Pattern #3). Generous: only penalise long chains.
    tails = re.findall(r",\s+(?:[a-z]+ing)\b", text)
    if len(tails) > 6:
        score_val -= 5
        notes.append(f"many -ing tails: {len(tails)}")

    # 6. First-person voice (required for oriental-destiny)
    first_person = re.findall(
        r"\b(I|me|my|we|our|here is what I|here is how)\b", text, re.IGNORECASE
    )
    if len(first_person) < 3:
        score_val -= 15
        notes.append("missing first-person voice")

    # 7. Sentence variation
    lens = sentence_lengths(text)
    if len(lens) > 1:
        stdev = statistics.stdev(lens)
        if stdev < 5:
            score_val -= 10
            notes.append(f"low sentence variation (stdev={stdev:.1f})")
    else:
        stdev = 0

    # 8. Word count
    if wc < 600:
        score_val -= 5
        notes.append(f"low word count: {wc}")
    elif wc > 1800:
        score_val -= 5
        notes.append(f"high word count: {wc}")

    # 9. Filler phrases
    for f in FILLER_PHRASES:
        if re.search(rf"\b{re.escape(f)}\b", text, re.IGNORECASE):
            score_val -= 5
            notes.append(f"filler: '{f}'")

    # 10. Sycophantic chatbot artifacts
    for s in SYCOPHANTIC:
        if re.search(rf"\b{re.escape(s)}\b", text, re.IGNORECASE):
            score_val -= 8
            notes.append(f"sycophantic: '{s}'")

    score_val = max(0, min(100, score_val))

    return {
        "score": score_val,
        "word_count": wc,
        "em_dashes": em,
        "first_person_markers": len(first_person),
        "sentence_stdev": round(stdev, 1) if len(lens) > 1 else 0,
        "notes": notes,
    }


def verify_sitemap(path: Path) -> tuple[bool, int, list[str]]:
    """Verify sitemap.xml is well-formed and return (ok, count, first_3)."""
    try:
        tree = ET.parse(path)
        ns = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
        urls = tree.getroot().findall(f"{ns}url")
        first3 = [u.find(f"{ns}loc").text for u in urls[:3]]
        return True, len(urls), first3
    except Exception as e:
        return False, 0, [f"error: {e}"]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("article", help="Path to the .html article")
    ap.add_argument("--site", default="oriental-destiny",
                    choices=list(SITE_CONFIG.keys()))
    ap.add_argument("--threshold", type=int, default=60)
    ap.add_argument("--sitemap", help="Optional path to sitemap.xml to verify")
    args = ap.parse_args()

    p = Path(args.article)
    if not p.exists():
        print(f"ERROR: {p} not found", file=sys.stderr)
        return 2

    result = score(p.read_text(), site=args.site)
    print(f"File:        {p}")
    print(f"Site:        {args.site}")
    print(f"Word count:  {result['word_count']}")
    print(f"Em dashes:   {result['em_dashes']}")
    print(f"1st-person:  {result['first_person_markers']}")
    print(f"Sentence stdev: {result['sentence_stdev']}")
    print(f"Score:       {result['score']} / 100  (threshold {args.threshold})")
    if result["notes"]:
        print("Notes:")
        for n in result["notes"]:
            print(f"  - {n}")
    else:
        print("Notes:       (none)")

    if args.sitemap:
        ok, count, first3 = verify_sitemap(Path(args.sitemap))
        print(f"\nSitemap:     {args.sitemap}")
        print(f"  well-formed: {ok}")
        print(f"  entries:     {count}")
        print(f"  first 3:     {first3}")
        if not ok:
            return 1

    return 0 if result["score"] > args.threshold else 1


if __name__ == "__main__":
    sys.exit(main())
