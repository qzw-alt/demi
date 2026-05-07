---
name: project-first-recommendation
description: Examine the actual project codebase before making any recommendations, tool choices, or architectural advice. Triggered when users ask about modifying/improving their project or choosing tools/models for it.
tags:
  - workflow
  - project-analysis
  - discovery
---

# Project-First Recommendation Skill

## Trigger Conditions
When the user asks about:
- "our project" / "我们的项目" / "our website"
- modifying, improving, or adding features to an existing project
- comparing tools/SDKs/models for their project
- making architectural decisions for their project
- Any request that starts with "what's the best way to..." or "which model should we use for..."

**DO NOT give recommendations until you have explored the project.**

---

## Core Workflow

### Step 1 — Find the project directory

```bash
# Check workspace for project directories
ls /root/.hermes/workspace/

# If user mentions a specific project name, find it
find /root/.hermes/workspace -maxdepth 3 -type d | grep -i <project-name>
```

### Step 2 — Explore structure

```bash
# List top-level files and directories
ls -la /root/.hermes/workspace/<project>/

# Find code files (JS, TS, Python, etc.)
find /root/.hermes/workspace/<project> -maxdepth 3 -type f \( -name "*.js" -o -name "*.ts" -o -name "*.py" -o -name "*.json" \) | grep -v node_modules | grep -v .git

# Read README if exists
cat /root/.hermes/workspace/<project>/README.md  # or similar
```

### Step 3 — Read key files

- `package.json` or `requirements.txt` — dependencies, tech stack
- Main entry point (e.g., `index.html`, `app.py`, `main.js`)
- Core engine/logic files (e.g., `bazi_engine.js`, `api_*.js`)
- Configuration files

### Step 4 — Summarize findings

Before making any recommendation, state:
1. What the project does
2. Current tech stack
3. Core files and their purposes
4. What you understood about the user's goal

### Step 5 — Then and only then give recommendations

---

## Pitfalls

- **DO NOT** start with model comparisons, tool comparisons, or architectural advice before exploring the project.
- **DO NOT** assume you know the project structure — always check `/root/.hermes/workspace/`.
- **DO NOT** give vague advice — ground every recommendation in what you actually found in the code.

---

## Example

User: "我想把网站的底层改成更强大的模型"

Wrong approach:
> "DeepSeek V4 is great for code generation, you should use it..."

Correct approach:
1. Explore `oriental-destiny/` directory
2. Read `bazi_engine.js`, `api_*.js`, HTML files
3. Summarize: "I see it's a pure-client JS BaZi calculator with no AI layer yet..."
4. Then ask: "你想在哪个环节引入 AI？计算层还是解读层？"

---

## Related Skills
- `plan` — write implementation plans after project exploration
- `writing-plans` — bite-sized task breakdown
- `spike` — throwaway experiments to validate ideas before building
