#!/usr/bin/env python3
"""
diagnose-cron.py — one-shot diagnostic for any Hermes cron job.

Usage:
    python3 diagnose-cron.py <job_id_or_name>
    python3 diagnose-cron.py daily-oriental-destiny-article
    python3 diagnose-cron.py c2aefdf3bada

Prints a structured report:
    - Job config (skill, skills, model, provider, schedule, state)
    - last_status, last_error
    - Latest output file (if any), with the error signature grepped
    - Skill existence check: does every name in skills[] resolve to ~/.hermes/skills/<name>/SKILL.md?

Exit code:
    0 = healthy (last_status ok OR no recent output to inspect)
    1 = has last_error OR recent failure detected
    2 = could not find the job
"""

import json
import os
import re
import sys
from pathlib import Path

JOBS_JSON = Path.home() / ".hermes/cron/jobs.json"
OUTPUT_ROOT = Path.home() / ".hermes/cron/output"
SKILLS_ROOT = Path.home() / ".hermes/skills"

FAILURE_SIGNATURES = [
    (r"could not be found and were skipped", "skill-not-found"),
    (r"RuntimeError: HTTP 500", "http-500"),
    (r"RuntimeError: HTTP 502", "upstream-502"),
    (r"PermissionError", "permission"),
    (r"FileNotFoundError", "missing-file"),
    (r"ModuleNotFoundError", "missing-module"),
    (r"Traceback \(most recent call last\)", "python-traceback"),
    (r"quota|rate.?limit|429", "rate-limit"),
    (r"Connection refused|Network is unreachable", "network"),
]


def find_job(needle):
    if not JOBS_JSON.exists():
        return None
    with JOBS_JSON.open() as f:
        data = json.load(f)
    for j in data.get("jobs", []):
        if j.get("job_id") == needle or j.get("name") == needle:
            return j
    # fuzzy: case-insensitive contains
    for j in data.get("jobs", []):
        if needle.lower() in (j.get("name") or "").lower():
            return j
    return None


def check_skill_exists(skill_name):
    """Return (exists, resolved_path_or_None)."""
    candidates = [
        SKILLS_ROOT / skill_name / "SKILL.md",
        SKILLS_ROOT / "creative" / skill_name / "SKILL.md",
        SKILLS_ROOT / "devops" / skill_name / "SKILL.md",
        SKILLS_ROOT / "software-development" / skill_name / "SKILL.md",
        SKILLS_ROOT / "research" / skill_name / "SKILL.md",
        SKILLS_ROOT / "web-development" / skill_name / "SKILL.md",
        SKILLS_ROOT / "medical-tourism" / skill_name / "SKILL.md",
        SKILLS_ROOT / "productivity" / skill_name / "SKILL.md",
        SKILLS_ROOT / "github" / skill_name / "SKILL.md",
    ]
    for c in candidates:
        if c.exists():
            return True, str(c)
    # last resort: any category
    if SKILLS_ROOT.exists():
        for p in SKILLS_ROOT.rglob(f"{skill_name}/SKILL.md"):
            return True, str(p)
    return False, None


def find_latest_output(job_id):
    out_dir = OUTPUT_ROOT / job_id
    if not out_dir.exists():
        return None
    files = sorted(out_dir.iterdir(), key=lambda p: p.stat().st_mtime, reverse=True)
    return files[0] if files else None


def classify_failure(text):
    hits = []
    for pat, label in FAILURE_SIGNATURES:
        if re.search(pat, text, re.IGNORECASE):
            hits.append(label)
    return hits


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)

    needle = sys.argv[1]
    job = find_job(needle)
    if not job:
        print(f"❌ No cron job found matching '{needle}' in {JOBS_JSON}")
        sys.exit(2)

    job_id = job.get("job_id") or job.get("id")
    name = job.get("name")

    print("=" * 70)
    print(f"CRON DIAGNOSTIC — {name}  ({job_id})")
    print("=" * 70)

    # --- Config block ---
    print("\n## Config")
    print(f"  skill:        {job.get('skill')}")
    print(f"  skills:       {job.get('skills')}")
    print(f"  model:        {job.get('model')}")
    print(f"  provider:     {job.get('provider')}")
    sched = job.get("schedule")
    if isinstance(sched, dict):
        print(f"  schedule:     {sched.get('expr')}  ({sched.get('display')})")
    else:
        print(f"  schedule:     {sched}")
    print(f"  enabled:      {job.get('enabled')}")
    print(f"  state:        {job.get('state')}")
    print(f"  paused_at:    {job.get('paused_at') or '-'}")
    print(f"  last_run_at:  {job.get('last_run_at') or '-'}")
    print(f"  last_status:  {job.get('last_status') or '-'}")
    print(f"  last_error:   {job.get('last_error') or '-'}")
    print(f"  last_delivery_error: {job.get('last_delivery_error') or '-'}")
    print(f"  repeat:       {job.get('repeat')}")
    print(f"  deliver:      {job.get('deliver')}")

    # --- Skill existence ---
    print("\n## Skill existence")
    all_skills = [s for s in (job.get("skills") or []) if s]
    if job.get("skill"):
        all_skills.append(job["skill"])
    seen = set()
    for s in all_skills:
        if s in seen:
            continue
        seen.add(s)
        ok, path = check_skill_exists(s)
        marker = "✅" if ok else "❌ MISSING"
        line = f"  {marker}  {s}"
        if ok:
            line += f"  → {path}"
        print(line)

    # --- Latest output ---
    latest = find_latest_output(job_id)
    if not latest:
        print("\n## Latest output")
        print("  (no output files yet)")
    else:
        print(f"\n## Latest output  ({latest.name})")
        print(f"  path: {latest}")
        print(f"  size: {latest.stat().st_size} bytes")
        try:
            text = latest.read_text(errors="replace")
        except Exception as e:
            print(f"  (could not read: {e})")
            text = ""

        # signature classification
        signatures = classify_failure(text)
        if signatures:
            print(f"  ⚠️  Failure signatures detected: {', '.join(signatures)}")
        else:
            print(f"  ✅ No failure signatures detected")

        # first 5 interesting lines
        print("\n  --- head ---")
        for line in text.splitlines()[:30]:
            if line.strip():
                print(f"  {line[:120]}")
        print("  --- end head ---")

        # error block extract
        m = re.search(r"## Error\s*\n+```([\s\S]*?)```", text)
        if m:
            err = m.group(1).strip()
            print(f"\n  ## Error block ({len(err)} chars):")
            for line in err.splitlines()[:30]:
                print(f"  {line}")

    # --- Verdict ---
    print("\n## Verdict")
    last_status = job.get("last_status")
    last_error = job.get("last_error")
    missing_skills = [
        s for s in seen
        if not check_skill_exists(s)[0]
    ]

    problems = []
    if last_status == "error":
        problems.append(f"last_status=error: {last_error}")
    if job.get("state") == "paused":
        problems.append("job is paused")
    if not job.get("enabled"):
        problems.append("job is disabled")
    if missing_skills:
        problems.append(f"missing skills: {missing_skills}")

    if not problems:
        print("  ✅ No problems detected.")
        sys.exit(0)
    else:
        for p in problems:
            print(f"  ❌ {p}")
        print("\n  See SKILL.md 'hermes-cron-troubleshooting' for the fix recipe.")
        sys.exit(1)


if __name__ == "__main__":
    main()