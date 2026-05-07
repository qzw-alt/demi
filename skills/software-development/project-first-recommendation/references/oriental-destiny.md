# Oriental Destiny — Feng Shui / BaZi Website

**Path:** `/root/.hermes/workspace/oriental-destiny/`

## What it is
Premium Feng Shui service targeting English-speaking users worldwide. Offers BaZi (八字/Eight Characters) readings, jade/crystal product recommendations.

## Tech Stack
- **Pure static HTML** — no backend, no server
- **bazi_engine.js** — 1215 lines, deterministic BaZi calculation engine (client-side JS)
- **report_focus.js** — static copy/content for 5 focus areas (career, wealth, love, protection, balance)
- **reading_state.js** — localStorage state management
- **landing_page.html, instant_reading.html, full_bazi_reading.html, report_demo.html** — static pages

## Key Files
| File | Purpose |
|---|---|
| `bazi_engine.js` | Core engine: 四柱排盘, 十神, 五行强度, 十二长生, 藏干 |
| `report_focus.js` | Static English copy for 5 life focus areas |
| `instant_reading.html` | Free instant reading (form → static result) |
| `full_bazi_reading.html` | Paid full reading page |
| `report_demo.html` | Crystal/bracelet product recommendation demo |

## Architecture
```
User Input → bazi_engine.js (排盘) → 静态文案填充 → HTML页面
```

No AI layer exists yet. All content is template-based static copy.

## User's Direction (as of 2026-05-02)
- Target: English-speaking users globally
- Goal: Add AI layer using DeepSeek V4
- Two-layer plan:
  - **Compute layer**: DeepSeek for complex Five Elements reasoning
  - **Interpretation layer**: DeepSeek for personalized English copy generation
- API costs: self-funded
- Execution: Via Claude Code

## AI Upgrade Files (generated 2026-05-02)
| File | Status |
|---|---|
| `docs/TECH_SPEC.md` | Complete architecture spec |
| `api_deepseek.js` | DeepSeek API wrapper (framework done) |
| `ai_bazi_layer.js` | AI inference + generation layer (framework done) |
| `prompts/system_analyze.txt` | Compute layer prompt (framework) |
| `prompts/system_reading.txt` | Interpretation layer prompt (framework) |
| `prompts/user_analyze.txt` | Compute layer user template |
| `prompts/user_reading.txt` | Interpretation layer user template |

**Pending:**
- Confirm `bazi_engine.js` export function name (`window.BaziEngine.calculateBaZi` assumed)
- Obtain DeepSeek API key
- Integrate into HTML pages
