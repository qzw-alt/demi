#!/usr/bin/env python3
"""
De-AI scanner for SEO articles.
Run as part of the humanizer audit before publishing a daily article.

Usage:
    python de-ai-scan-script.py <path-to-article.html>

Returns exit code 0 if clean, 1 if AI tells detected.

Catches the most common AI tells from the humanizer skill's 29-pattern list,
adapted for the oriental-destiny.com template (or any English SEO article).
"""

import re
import sys
from pathlib import Path

# The AI tell-word bank (extend as new patterns surface)
AI_WORDS = [
    # Vocabulary tells
    'delve', 'tapestry', 'testament', 'underscore', 'underscores', 'underscoring',
    'enduring', 'pivotal', 'intricate', 'intricacies', 'fostering', 'garner',
    'showcase', 'showcases', 'showcasing', 'vibrant', 'nestled', 'renowned',
    'breathtaking', 'must-visit', 'stunning', 'groundbreaking', 'beacon',
    'landscape ', 'enhance', 'enhancing', 'crucial', 'vital',
    'align with', 'commitment to', 'natural beauty', 'in the heart of',
    'exemplifies', 'deeply rooted', 'indelible mark', 'focal point',
    'evolving landscape', 'key turning point', 'setting the stage for',
    'symbolizing', 'contributing to', 'marking', 'shaping',
    'represents a shift', 'reflects broader',
    # Filler / chatbot tells
    'i hope this helps', 'great question', 'let me know', 'of course!',
    'certainly!', "you're absolutely right", "would you like",
    'here is a', 'in conclusion', 'the future looks bright',
    'exciting times lie ahead', 'journey toward excellence',
    # Persuasive authority tells
    'at its core', 'in reality', 'what really matters', 'fundamentally',
    'the deeper issue', 'the heart of the matter', 'the real question is',
    # Signposting / announcements
    "let's dive in", "let's explore", "let's break this down",
    'here\'s what you need to know', 'without further ado', 'now let\'s look at',
    # Excessive hedging
    'in order to', 'due to the fact that', 'at this point in time',
    # Hyphenated overuse (informational, not failure)
    # 'cross-functional', 'client-facing', 'data-driven', etc.
]

# Em-dash baseline (feng shui sites average 1-3 per 1000 words as a stylistic tic)
EM_DASH_WORDS_BASELINE = 1000  # words per em-dash that's acceptable

def scan(path: Path) -> dict:
    html = path.read_text(encoding='utf-8', errors='replace')

    # Strip HTML for body-text analysis
    text = re.sub(r'<style[^>]*>.*?</style>', ' ', html, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<script[^>]*>.*?</script>', ' ', text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<[^>]+>', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    words = text.split()
    word_count = len(words)

    lower_text = text.lower()

    # AI vocabulary scan
    found_words = {}
    for w in AI_WORDS:
        c = lower_text.count(w.lower())
        if c > 0:
            found_words[w] = c

    # Em dash count
    em_dashes = lower_text.count('—')

    # Curly quotes
    curly_double = html.count('\u201c') + html.count('\u201d')
    curly_single = html.count('\u2018') + html.count('\u2019')

    # Emojis
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"
        u"\U0001F300-\U0001F5FF"
        u"\U0001F680-\U0001F6FF"
        u"\U0001F1E0-\U0001F1FF"
        u"\u2600-\u26FF"
        u"\u2700-\u27BF"
        "]+", flags=re.UNICODE)
    emojis = len(emoji_pattern.findall(html))

    # Hyphenated overused pairs (informational)
    hyphen_pairs = ['cross-functional', 'client-facing', 'data-driven',
                    'decision-making', 'well-known', 'high-quality',
                    'real-time', 'long-term', 'end-to-end', 'third-party']
    found_hyphens = {}
    for hp in hyphen_pairs:
        c = lower_text.count(hp.lower())
        if c:
            found_hyphens[hp] = c

    # Passive-voice hints (informational only)
    # NB: hard to detect reliably in plain text; skipping auto-flag.

    # Length check
    if word_count < 3000:
        length_flag = f"SHORT: {word_count} words (typical SEO articles are 3500-5000)"
    elif word_count > 6000:
        length_flag = f"LONG: {word_count} words (typical SEO articles are 3500-5000)"
    else:
        length_flag = f"OK: {word_count} words"

    # Verdict
    has_tells = bool(found_words) or curly_double > 0 or curly_single > 0 or emojis > 0
    em_dash_density = em_dashes / max(word_count / EM_DASH_WORDS_BASELINE, 1)

    return {
        'word_count': word_count,
        'length_flag': length_flag,
        'ai_tells': found_words,
        'em_dashes': em_dashes,
        'em_dash_density': round(em_dash_density, 2),
        'curly_quotes_double': curly_double,
        'curly_quotes_single': curly_single,
        'emojis': emojis,
        'hyphen_overuses': found_hyphens,
        'has_tells': has_tells,
    }


def main():
    if len(sys.argv) != 2:
        print("Usage: python de-ai-scan-script.py <article.html>")
        sys.exit(2)

    path = Path(sys.argv[1])
    if not path.exists():
        print(f"ERROR: file not found: {path}")
        sys.exit(2)

    result = scan(path)

    print(f"=== De-AI Scan: {path.name} ===\n")
    print(f"Word count: {result['word_count']} ({result['length_flag']})")
    print(f"Em dashes: {result['em_dashes']} (density: {result['em_dash_density']}x baseline)")
    print(f"Curly quotes (double): {result['curly_quotes_double']}")
    print(f"Curly quotes (single): {result['curly_quotes_single']}")
    print(f"Emojis: {result['emojis']}")

    print("\n--- AI vocabulary tells ---")
    if result['ai_tells']:
        for w, c in sorted(result['ai_tells'].items(), key=lambda x: -x[1]):
            print(f"  {w}: {c}")
    else:
        print("  (none)")

    print("\n--- Hyphenated overuses (informational) ---")
    if result['hyphen_overuses']:
        for hp, c in sorted(result['hyphen_overuses'].items(), key=lambda x: -x[1]):
            print(f"  {hp}: {c}")
    else:
        print("  (none)")

    print("\n=== VERDICT ===")
    if result['has_tells']:
        print("FAIL: AI tells detected. Rewrite before publishing.")
        sys.exit(1)
    else:
        print("PASS: Article is clean. Safe to publish.")
        sys.exit(0)


if __name__ == '__main__':
    main()