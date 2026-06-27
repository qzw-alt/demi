#!/usr/bin/env python3
"""
De-AI scanner for fate-YYYY-MM-DD.html articles on oriental-destiny.com.

Runs the humanizer 29-pattern audit programmatically, plus structural tells
that don't show up in word lists (parallel sentence openings, template-section
repetition, etc.). Exits non-zero if any hard-fail pattern is found, so you can
gate the publish step on a clean scan.

Usage:
    python3 de-ai-scan.py path/to/fate-YYYY-MM-DD.html [--strict]

The --strict flag also fails on stylistic mismatches (em-dash density outside
the site's measured baseline).

Site baseline (oriental-destiny.com, 2026-06-25 through 2026-06-27):
    Em dashes: 6.8 per 1,200 words (encoded as &mdash; in source).
    Body wordcount: 3,200-4,500.
    FAQ items: 5-7.
    No emojis, no curly quotes, no title-cased <h3> tags.

Author: extracted from a real 2026-06-27 cron run.
"""

import argparse
import html as html_lib
import re
import sys
import unicodedata
from pathlib import Path


# ---------- Hard-fail patterns: ship only if zero hits ----------

AI_VOCAB = [
    # Pattern 7: high-frequency AI words
    "delve", "tapestry", "testament", "underscore", "underscoring",
    "enduring", "pivotal", "intricate", "intricacies", "fostering",
    "garner", "showcase", "showcases", "showcasing", "vibrant",
    "nestled", "renowned", "breathtaking", "must-visit", "stunning",
    "groundbreaking", "beacon", "enhance", "enhancing", "crucial",
    "vital", "symbolizing", "fostering", "leverage", "leverages",
    "leveraging", "utilize", "utilizes", "utilizing", "robust",
    "seamlessly", "seamless", "harness", "elevate", "elevates",
    "elevating", "align with", "alignment with",
    # Pattern 20: collaborative communication artifacts
    "i hope this helps", "great question", "let me know if",
    "of course!", "certainly!", "you're absolutely right",
    # Pattern 25: generic positive conclusions
    "in conclusion", "the future looks bright", "exciting times lie ahead",
    "journey toward excellence", "represents a major step",
    # Pattern 27: persuasive authority tropes
    "at its core", "in reality", "what really matters", "fundamentally,",
    "the real question is", "the deeper issue", "the heart of the matter",
    # Pattern 28: signposting and announcements
    "let's dive in", "let's explore", "let's break this down",
    "here's what you need to know", "without further ado",
    # Pattern 23: filler phrases
    "in order to", "due to the fact that", "at this point in time",
    "in the event that", "has the ability to", "it is important to note",
    # Pattern 22: sycophantic
    "thank you for", "feel free to",
]

HARD_FAIL_THRESHOLD = 2  # any single word hitting 2+ times = fail


def strip_to_body(html_text: str) -> str:
    """Strip <script>, <style>, and HTML tags; return plain text body."""
    text = re.sub(r"<script.*?</script>", "", html_text, flags=re.S)
    text = re.sub(r"<style.*?</style>", "", text, flags=re.S)
    text = re.sub(r"<[^>]+>", " ", text)
    return html_lib.unescape(text)


def word_count(text: str) -> int:
    return len(re.findall(r"[A-Za-z']+", text))


def count_em_dashes(text: str) -> int:
    """Count both literal — and HTML-encoded &mdash; / &#8212;."""
    return (
        text.count("—")
        + text.count("&mdash;")
        + len(re.findall(r"&#8212;|&ndash;", text))
    )


def has_curly_quotes(text: str) -> bool:
    for ch in text:
        if ch in ("\u201c", "\u201d", "\u2018", "\u2019"):
            return True
        # detect via name as a fallback
        try:
            name = unicodedata.name(ch, "")
            if "LEFT DOUBLE QUOTATION MARK" in name or "RIGHT DOUBLE QUOTATION MARK" in name:
                return True
            if "LEFT SINGLE QUOTATION MARK" in name or "RIGHT SINGLE QUOTATION MARK" in name:
                return True
        except ValueError:
            pass
    return False


def count_emojis(text: str) -> int:
    pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"
        "\U0001F300-\U0001F5FF"
        "\U0001F680-\U0001F6FF"
        "\U0001F1E0-\U0001F1FF"
        "]+",
        flags=re.UNICODE,
    )
    return len(pattern.findall(text))


def find_negative_parallelisms(text: str) -> list:
    """Pattern 9: 'Not only X but Y' / 'It's not just X, it's Y'."""
    return re.findall(
        r"\b(?:not\s+(?:just|merely|only)|it'?s\s+not\s+(?:just|merely|only))\b[^.!?]{4,80}"
        r"(?:,\s*)?(?:but|it'?s)\b",
        text,
        flags=re.I,
    )


def find_rule_of_three_comma_lists(text: str) -> list:
    """Pattern 10: rule-of-three comma lists in single clauses.

    Conservative: matches X, Y, and Z inside a single sentence span.
    """
    return re.findall(
        r"\b[A-Za-z][a-zA-Z']{2,}\b\s*,\s*"
        r"\b[A-Za-z][a-zA-Z']{2,}\b\s*,\s*"
        r"(?:and|or)\s+\b[A-Za-z][a-zA-Z']{2,}\b",
        text,
    )


def find_ing_tail_phrases(text: str) -> list:
    """Pattern 3: tacked-on present-participle phrases at sentence ends."""
    return re.findall(
        r",\s+(?:ensuring|reflecting|symbolizing|contributing to|"
        r"highlighting|underscoring|emphasizing|showcasing|fostering|"
        r"cultivating|encompassing|garnering)\b[^.!?]{0,80}\.",
        text,
        flags=re.I,
    )


def find_passive_subjectless(text: str) -> list:
    """Pattern 13: subjectless passive fragments."""
    return re.findall(
        r"(?:^|\.\s+)(?:No\s+\w+(?:\s+\w+){0,3}\s+needed|"
        r"\w+(?:\s+\w+){0,3}\s+(?:is|are)\s+(?:preserved|saved|stored|recorded|"
        r"displayed|generated|produced|calculated|computed)\s+automatically)\.",
        text,
        flags=re.I,
    )


def find_repeated_sentence_openings(text: str, threshold: int = 3) -> list:
    """Structural tell: same sentence-starter repeated >= threshold times in one article.

    Catches the failure mode where a listicle uses the same parallel opener
    ("The popular version:", "The classical version:", ...) across many cards.
    """
    sentences = re.split(r"(?<=[.!?])\s+", text)
    opener_counts: dict = {}
    for s in sentences:
        s = s.strip()
        if len(s) < 12:
            continue
        # take the first 6 words as the "opener"
        opener = " ".join(s.split()[:6]).lower()
        opener_counts[opener] = opener_counts.get(opener, 0) + 1
    return [(op, c) for op, c in opener_counts.items() if c >= threshold]


def find_template_section_openers(text: str, threshold: int = 3) -> list:
    """Structural tell: same section opener (typically a tag like 'Mistake N' or 'Step N')
    repeated across >= threshold sibling sections.
    """
    # Look for explicit section markers
    section_re = re.compile(
        r"(?:^|\n)\s*(?:#{1,3}\s+|Mistake\s+\d+\b|Step\s+\d+\b|Tip\s+\d+\b|Section\s+\d+\b)",
        flags=re.I,
    )
    sections = section_re.findall(text)
    counts: dict = {}
    for s in sections:
        key = re.sub(r"\s+\d+", " N", s).strip().lower()
        counts[key] = counts.get(key, 0) + 1
    return [(k, c) for k, c in counts.items() if c >= threshold]


def find_ai_phrase_in_headings(html_text: str) -> list:
    """Catch AI words in headings specifically (more visible than body)."""
    headings = re.findall(r"<h[1-6][^>]*>([^<]+)</h[1-6]>", html_text)
    hits = []
    for h in headings:
        h_lower = h.lower()
        for word in AI_VOCAB:
            if word in h_lower:
                hits.append((h.strip(), word))
    return hits


def find_duplicate_intro_paragraph(html_text: str) -> list:
    """Pattern 29: heading followed by a one-line paragraph that restates the heading."""
    return re.findall(
        r"<h[23][^>]*>([^<]+)</h[23]>\s*<p>([^<]{5,80})</p>\s*<p>",
        html_text,
        flags=re.S | re.I,
    )


# ---------- Main ----------

def scan(html_path: Path, strict: bool = False) -> tuple:
    html_text = html_path.read_text(encoding="utf-8")
    body_text = strip_to_body(html_text)
    words = word_count(body_text)

    findings = {"hard_fail": [], "warn": [], "info": []}
    metrics = {}

    # 1. AI vocabulary hard-fail
    body_lower = body_text.lower()
    vocab_hits: dict = {}
    for w in AI_VOCAB:
        c = body_lower.count(w.lower())
        if c >= HARD_FAIL_THRESHOLD:
            findings["hard_fail"].append(f"AI vocab '{w}' x{c}")
        elif c == 1:
            findings["warn"].append(f"AI vocab '{w}' x1")
        if c:
            vocab_hits[w] = c
    metrics["ai_vocab"] = vocab_hits

    # 2. AI words in headings
    heading_hits = find_ai_phrase_in_headings(html_text)
    if heading_hits:
        findings["hard_fail"].append(
            f"AI word in heading: {heading_hits[0][0]!r} contains {heading_hits[0][1]!r}"
        )

    # 3. Curly quotes
    if has_curly_quotes(html_text):
        findings["hard_fail"].append("curly quotes present (Pattern 19)")

    # 4. Emojis
    emoji_count = count_emojis(html_text)
    if emoji_count > 0:
        findings["hard_fail"].append(f"{emoji_count} emoji(s) present (Pattern 18)")

    # 5. Negative parallelisms
    neg_par = find_negative_parallelisms(body_text)
    if neg_par:
        findings["warn"].append(
            f"{len(neg_par)} negative parallelism(s) (Pattern 9): {neg_par[0][:80]!r}"
        )

    # 6. Rule-of-three lists
    rot = find_rule_of_three_comma_lists(body_text)
    if rot:
        findings["warn"].append(
            f"{len(rot)} rule-of-three list(s) (Pattern 10): {rot[0]!r}"
        )

    # 7. -ing tails
    ing = find_ing_tail_phrases(body_text)
    if ing:
        findings["warn"].append(f"{len(ing)} -ing tail phrase(s) (Pattern 3)")

    # 8. Passive subjectless
    ps = find_passive_subjectless(body_text)
    if ps:
        findings["warn"].append(f"{len(ps)} subjectless passive(s) (Pattern 13)")

    # 9. Repeated sentence openings (structural)
    repeated = find_repeated_sentence_openings(body_text, threshold=3)
    if repeated:
        op, c = max(repeated, key=lambda x: x[1])
        findings["warn"].append(
            f"structural: sentence opener repeated {c}x: {op!r}. "
            f"Vary the opener across listicle cards to avoid template-feel."
        )

    # 10. Template section markers
    tmpl = find_template_section_openers(body_text, threshold=3)
    if tmpl:
        findings["warn"].append(
            f"structural: section marker repeated {tmpl[0][1]}x: {tmpl[0][0]!r}. "
            f"Vary section titles even when the numbering is consistent."
        )

    # 11. Heading + one-liner restate (Pattern 29)
    restates = find_duplicate_intro_paragraph(html_text)
    if restates:
        findings["warn"].append(f"{len(restates)} heading-restated-by-intro pattern(s) (Pattern 29)")

    # 12. Em-dash density (strict mode)
    em_dashes = count_em_dashes(html_text)
    metrics["em_dashes"] = em_dashes
    metrics["words"] = words
    metrics["em_per_1200"] = round(em_dashes / max(words, 1) * 1200, 2)
    if words > 0:
        per_1200 = em_dashes / words * 1200
        if per_1200 > 12:
            findings["warn"].append(
                f"em-dash density {per_1200:.1f}/1200 above site norm "
                f"(site baseline ~6.8, AI-saleswriting >12)"
            )
        elif per_1200 < 3 and words > 2500:
            findings["warn"].append(
                f"em-dash density {per_1200:.1f}/1200 below site norm "
                f"(LLM-terse range)"
            )
    if strict and findings["warn"]:
        findings["hard_fail"].extend(
            [f"STRICT: {w}" for w in findings["warn"]]
        )
        findings["warn"] = []

    # 13. Word count check
    if words < 2800:
        findings["warn"].append(f"low word count {words} (site norm 3200-4500)")
    elif words > 5000:
        findings["warn"].append(f"high word count {words} (site norm 3200-4500)")

    return findings, metrics


def main() -> int:
    p = argparse.ArgumentParser(description="De-AI scanner for fate-YYYY-MM-DD.html articles.")
    p.add_argument("path", type=Path)
    p.add_argument("--strict", action="store_true", help="Treat warnings as hard fails.")
    args = p.parse_args()

    findings, metrics = scan(args.path, strict=args.strict)

    print(f"=== {args.path.name} ===")
    print(f"Words:        {metrics.get('words')}")
    print(f"Em dashes:    {metrics.get('em_dashes')} ({metrics.get('em_per_1200')}/1200)")
    if metrics.get("ai_vocab"):
        nonzero = {k: v for k, v in metrics["ai_vocab"].items() if v}
        if nonzero:
            print(f"AI vocab hits: {nonzero}")
    print()

    if findings["hard_fail"]:
        print("HARD FAILS:")
        for f in findings["hard_fail"]:
            print(f"  - {f}")
    if findings["warn"]:
        print("WARNINGS:")
        for w in findings["warn"]:
            print(f"  - {w}")
    if not findings["hard_fail"] and not findings["warn"]:
        print("CLEAN — no AI tells detected.")

    return 1 if findings["hard_fail"] else 0


if __name__ == "__main__":
    sys.exit(main())
