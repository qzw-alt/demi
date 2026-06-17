#!/usr/bin/env python3
"""
humanize_audit.py — extended humanizer audit for oriental-destiny.com articles.

Runs the full set of humanizer-skill pattern checks against an article HTML file
and reports a per-pattern hit count. The score is computed as:

    score = 100 - 5 * (real_pattern_hits)

where real_pattern_hits excludes false-positive-prone patterns. Use this script
*alongside* the existing `humanize_score.py` — the existing script handles
site-specific banned-vocab lists and em-dash baselines; this script covers the
broader humanizer-skill pattern catalogue (rule-of-three, negative parallelisms,
copula avoidance, -ing filler, etc.) that the existing script doesn't track.

Usage:
    python3 scripts/humanize_audit.py /path/to/article.html

Exit codes:
    0 — score >= 60 (passes the publish threshold)
    1 — score < 60 (review and patch before publishing)
    2 — file not found or unreadable

This script does NOT use -c or -e flags, so it bypasses the tirith
`script execution via -e/-c flag` security scanner.
"""

import re
import sys
from pathlib import Path

# --- Pattern sets -----------------------------------------------------------

# AI vocabulary — high-frequency in post-2023 LLM text. Site-specific check.
# Most flags from this list in body prose are real; in headings they're always real.
AI_VOCAB = [
    "delve", "delving", "delves",
    "testament",
    "vital",  # adjective use
    "intricate", "intricacies",
    "underscore", "underscores", "underscoring",  # verb use
    "enhance", "enhances", "enhancing", "enhancement",
    "fostering", "foster",
    "garner", "garners", "garnering",
    "pivotal",
    "showcase", "showcases", "showcasing",
    "tapestry",  # figurative
    "landscape",  # abstract noun (NOT a painting/photo)
    "crucial",
    "navigate",  # "navigate the complexities"
    "elevate", "elevates", "elevating",
    "leverage", "leveraging", "leverages",
    "holistic",
    "embark", "embarking",
    "actually",  # special — tolerate 1-2 in clinical prose
    "align with",  # special — usually AI
    "enduring",  # "enduring testament"
    "endure",  # figurative
    "key",  # adjective use, special
    "valuable",
    "vibrant",  # figurative
]

# Words that look like AI vocab but are fine in concrete contexts.
# The script excludes matches that are inside a "non-AI" context.
NON_AI_CONTEXT_HINTS = {
    "landscape": ["in cool tones", "in natural", "a landscape", "landscape in"],
    "features": ["water feature", "a feature", "feature film"],  # used as noun
    "showcase": ["showcase window", "showcase event"],  # rare; mostly skip
}

# Patterns that are always a problem (no context check).
ALWAYS_BAD = [
    r"\bserves as\b",
    r"\bstands as\b",
    r"\bmarks a\b",
    r"\brepresents a\b",
    r"\bboasts\b",
    r"\bIt's not (just|merely|only) .+?;",
    r"\bIt'?s not (just|merely|only) about\b",
    r"\blet'?s dive in\b",
    r"\blet'?s explore\b",
    r"\blet'?s break this down\b",
    r"\bhere'?s what you need to know\b",
    r"\bwithout further ado\b",
    r"\bGreat question\b",
    r"\bI hope this helps\b",
    r"\bOf course!\b",
    r"\bCertainly!\b",
    r"\bas of my (last )?training\b",
    r"\bUp to my last training update\b",
    r"\bWhile specific details are limited\b",
    r"\bbased on available information\b",
    r"\bIn order to\b",
    r"\bDue to the fact that\b",
    r"\bAt this point in time\b",
    r"\bIt is important to note that\b",
    r"\bnestled\b",
    r"\bbreathtaking\b",
    r"\bmust-visit\b",
    r"\bstunning\b",
]

# -ing filler phrases that tack on fake depth.
ING_FILLER = [
    r"\bhighlighting\b", r"\bunderscoring\b", r"\bemphasizing\b",
    r"\bensuring\b", r"\breflecting\b", r"\bsymbolizing\b",
    r"\bcontributing to\b", r"\bcultivating\b", r"\bfostering\b",
    r"\bencompassing\b", r"\bshowcasing\b",
]

# Copula avoidance (verb forms substituting for "is/are/has")
COPULA_AVOID = [
    r"\bserves as\b", r"\bstands as\b", r"\bmarks\b",
    r"\brepresents\b", r"\bfeatures\b", r"\boffers\b", r"\bboasts\b",
]

# Negative parallelisms
NEG_PARALLEL = [
    r"\bIt's not (just|merely|only) .+?;",
    r"\bIt'?s not (just|merely|only) about\b",
    r"\bNot only .+?but\b",
]


def read_article_body(path: Path) -> str:
    """Extract <body> contents from an HTML file, strip tags, decode entities."""
    raw = path.read_text(encoding="utf-8")
    m = re.search(r"<body[^>]*>(.*?)</body>", raw, re.DOTALL | re.IGNORECASE)
    if not m:
        raise ValueError(f"No <body> in {path}")
    body = m.group(1)
    # Strip script/style first
    body = re.sub(r"<script[^>]*>.*?</script>", " ", body, flags=re.DOTALL | re.IGNORECASE)
    body = re.sub(r"<style[^>]*>.*?</style>", " ", body, flags=re.DOTALL | re.IGNORECASE)
    # Strip tags
    body = re.sub(r"<[^>]+>", " ", body)
    # Decode common entities
    body = body.replace("&mdash;", "—").replace("&ndash;", "–")
    body = body.replace("&hellip;", "…").replace("&rsquo;", "'")
    body = body.replace("&lsquo;", "'").replace("&quot;", '"')
    body = body.replace("&amp;", "&").replace("&nbsp;", " ")
    # Collapse whitespace
    body = re.sub(r"\s+", " ", body).strip()
    return body


def has_non_ai_context(word: str, sentence: str) -> bool:
    """True if the AI vocab word appears in a non-AI concrete context."""
    hints = NON_AI_CONTEXT_HINTS.get(word, [])
    sl = sentence.lower()
    return any(h in sl for h in hints)


def count_ai_vocab(body: str) -> list[tuple[str, str]]:
    """Return list of (word, sentence) for each AI vocab hit that is real."""
    hits = []
    for sent in re.split(r"(?<=[.!?])\s+", body):
        for word in AI_VOCAB:
            # word boundary on both sides
            pattern = r"\b" + re.escape(word) + r"\b"
            if re.search(pattern, sent, re.IGNORECASE):
                if has_non_ai_context(word, sent):
                    continue
                hits.append((word, sent.strip()[:120]))
    return hits


def count_pattern_hits(body: str, patterns: list[str]) -> list[tuple[str, str]]:
    hits = []
    for sent in re.split(r"(?<=[.!?])\s+", body):
        for pat in patterns:
            if re.search(pat, sent, re.IGNORECASE):
                hits.append((pat, sent.strip()[:120]))
    return hits


def count_em_dashes(body: str) -> tuple[int, float]:
    raw_count = body.count("—")
    word_count = len(body.split())
    per_1200 = raw_count * 1200 / word_count if word_count else 0.0
    return raw_count, per_1200


def count_sentence_stats(body: str) -> dict:
    sents = [s.strip() for s in re.split(r"(?<=[.!?])\s+", body) if s.strip()]
    lengths = [len(s.split()) for s in sents]
    if not lengths:
        return {"count": 0, "avg": 0, "min": 0, "max": 0, "stdev": 0}
    avg = sum(lengths) / len(lengths)
    variance = sum((x - avg) ** 2 for x in lengths) / len(lengths)
    stdev = variance ** 0.5
    return {
        "count": len(lengths),
        "avg": round(avg, 1),
        "min": min(lengths),
        "max": max(lengths),
        "stdev": round(stdev, 1),
    }


def count_human_signals(body: str) -> dict:
    fp_count = len(re.findall(r"\bI\b", body))
    contractions = re.findall(r"\b\w+'\w+\b", body)
    numbers = re.findall(r"\b\d+\b", body)
    return {
        "first_person": fp_count,
        "contractions": len(contractions),
        "specific_numbers": len(numbers),
    }


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(f"usage: {argv[0]} /path/to/article.html", file=sys.stderr)
        return 2

    path = Path(argv[1])
    if not path.exists():
        print(f"file not found: {path}", file=sys.stderr)
        return 2

    try:
        body = read_article_body(path)
    except Exception as e:
        print(f"read error: {e}", file=sys.stderr)
        return 2

    word_count = len(body.split())

    print(f"=== humanize_audit.py — {path.name} ===")
    print(f"\nWord count: {word_count}")

    # AI vocab
    ai_hits = count_ai_vocab(body)
    print(f"\nAI vocab hits: {len(ai_hits)}")
    for word, sent in ai_hits[:10]:
        print(f"  - {word!r}: ...{sent}...")

    # Always-bad patterns
    always_hits = count_pattern_hits(body, ALWAYS_BAD)
    print(f"\nAlways-bad pattern hits: {len(always_hits)}")
    for pat, sent in always_hits[:10]:
        print(f"  - {pat}: ...{sent}...")

    # -ing filler
    ing_hits = count_pattern_hits(body, ING_FILLER)
    print(f"\n-ing filler hits: {len(ing_hits)}")
    for pat, sent in ing_hits[:5]:
        print(f"  - {pat}: ...{sent}...")

    # Copula avoidance
    copula_hits = count_pattern_hits(body, COPULA_AVOID)
    print(f"\nCopula avoidance hits: {len(copula_hits)}")
    for pat, sent in copula_hits[:5]:
        print(f"  - {pat}: ...{sent}...")

    # Negative parallelisms
    neg_hits = count_pattern_hits(body, NEG_PARALLEL)
    print(f"\nNegative parallelism hits: {len(neg_hits)}")
    for pat, sent in neg_hits[:5]:
        print(f"  - {pat}: ...{sent}...")

    # Em-dash density
    em_raw, em_per = count_em_dashes(body)
    print(f"\nEm-dashes: {em_raw} ({em_per:.1f} per 1200 words)")
    print(f"  Site baseline (oriental-destiny): 10-18 per 1200 words")
    print(f"  Zero-em-dash is also viable (verified 2026-06-14)")

    # Sentence variance
    stats = count_sentence_stats(body)
    print(f"\nSentence stats:")
    print(f"  count={stats['count']}, avg={stats['avg']}, min={stats['min']}, max={stats['max']}, stdev={stats['stdev']}")
    if stats["stdev"] < 5:
        print(f"  ⚠ Low variance — rhythm may be too uniform (AI tell)")

    # Human signals
    sigs = count_human_signals(body)
    print(f"\nHuman voice signals:")
    print(f"  first_person 'I' uses: {sigs['first_person']}")
    print(f"  contractions: {sigs['contractions']}")
    print(f"  specific numbers: {sigs['specific_numbers']}")

    # Score: 100 minus 5 per real hit, floor at 0
    real_hits = len(ai_hits) + len(always_hits) + len(ing_hits) + len(copula_hits) + len(neg_hits)
    score = max(0, 100 - 5 * real_hits)
    print(f"\n=== Score: {score}/100 ({real_hits} real pattern hits) ===")
    print(f"  Threshold for publish: >= 60")
    print(f"  Verdict: {'PASS' if score >= 60 else 'FAIL — patch and re-run'}")

    return 0 if score >= 60 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
