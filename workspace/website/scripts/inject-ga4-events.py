#!/usr/bin/env python3
"""
Inject ga4-events.js script reference into all pages.

Replaces inline GA4 event tracking code (when present) with external script reference.
Adds script reference to pages that have gtag.js but no event tracking.

Targets:
  - index.html
  - blog/index.html
  - blog/*.html (90+ article pages)
  - news/*.html (if has gtag.js)

Skips:
  - docs/ (archive)
  - blog-export/, blog-articles/, templates/, api/, 医疗旅游/ (archive/non-prod)
  - report-*.html (dynamic patient reports — leave alone)
"""
import os
import re
from pathlib import Path

ROOT = Path('/home/ubuntu/.hermes/workspace/website')

# Inline block to remove (the old inlined event tracking code in index.html + blog/index.html)
# Match the comment marker through to closing </script> of the inline block
INLINE_PATTERN = re.compile(
    r'\n\s*//\s*={3,}\s*GA4 EVENT TRACKING.*?</script>',
    re.DOTALL
)

# External script to inject AFTER the gtag config
SCRIPT_TAG = '\n    <script src="ga4-events.js" defer></script>'


def should_process(path: Path) -> bool:
    """Decide whether this HTML file needs GA4 events injected."""
    rel = str(path.relative_to(ROOT))
    # Skip archive / non-prod directories
    skip_prefixes = (
        'docs/', 'blog-export/', 'blog-articles/',
        'templates/', 'api/', '医疗旅游/', '_site/', 'node_modules/'
    )
    if rel.startswith(skip_prefixes):
        return False
    # Skip dynamic patient reports
    if rel.startswith('report-'):
        return False
    # Only .html files
    if path.suffix != '.html':
        return False
    # Must currently have gtag.js to be in scope
    try:
        content = path.read_text(encoding='utf-8')
    except Exception:
        return False
    return 'googletagmanager.com/gtag' in content


def inject(path: Path) -> str:
    """Return 'injected' | 'already-has-script' | 'no-gtag' | 'skipped'."""
    content = path.read_text(encoding='utf-8')
    rel = str(path.relative_to(ROOT))

    # 1. If already has external ga4-events.js, skip
    if 'ga4-events.js' in content:
        return 'already-has-script'

    # 2. If has inline tracking, remove it and add external
    if 'GA4 EVENT TRACKING' in content:
        new_content = INLINE_PATTERN.sub('', content)
        # Insert external script after the </script> of gtag config block
        new_content = re.sub(
            r"(gtag\('config', 'G-[A-Z0-9]+';\s*\n\s*</script>)",
            r"\1" + SCRIPT_TAG,
            new_content,
            count=1
        )
        path.write_text(new_content, encoding='utf-8')
        return 'replaced-inline'

    # 3. If has gtag.js but no event tracking, add external script
    if 'googletagmanager.com/gtag' in content:
        new_content = re.sub(
            r"(gtag\('config', 'G-[A-Z0-9]+';\s*\n\s*</script>)",
            r"\1" + SCRIPT_TAG,
            content,
            count=1
        )
        path.write_text(new_content, encoding='utf-8')
        return 'injected'

    return 'no-gtag'


def main():
    stats = {'replaced-inline': [], 'injected': [], 'already-has-script': [], 'no-gtag': [], 'skipped': []}

    for path in ROOT.rglob('*.html'):
        if not should_process(path):
            stats['skipped'].append(str(path.relative_to(ROOT)))
            continue
        result = inject(path)
        stats[result].append(str(path.relative_to(ROOT)))

    print("=" * 60)
    print(f"REPLACED INLINE (had old code): {len(stats['replaced-inline'])}")
    for p in stats['replaced-inline']:
        print(f"  - {p}")
    print()
    print(f"INJECTED (added script ref):    {len(stats['injected'])}")
    for p in stats['injected']:
        print(f"  + {p}")
    print()
    print(f"ALREADY HAD SCRIPT:             {len(stats['already-has-script'])}")
    print(f"NO GTAG (skipped):              {len(stats['no-gtag'])}")
    for p in stats['no-gtag']:
        print(f"  ? {p}")
    print()
    print(f"SKIPPED (archive/non-prod):    {len(stats['skipped'])}")


if __name__ == '__main__':
    main()