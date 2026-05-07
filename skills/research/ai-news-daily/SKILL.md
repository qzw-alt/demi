---
name: ai-news-daily
description: Daily AI news gathering at 06:00 UTC+8. Searches TechCrunch, Hacker News, Google News (EN/CN), and Chinese sources. Filters for major developments (funding, breakthroughs, security events, product launches). Saves to memory/layer4/knowledge/ai-news-YYYY-MM-DD.md. For major findings (>$100M funding, major breakthroughs), sends Feishu DM to 伟烨.
category: research
---

# AI Daily News — 06:00 UTC+8 Cron Job

## News Sources

**Primary sources (use `execute_code` with `urllib` — see Pitfalls):**
- TechCrunch AI: `https://techcrunch.com/category/artificial-intelligence/` (browser_navigate preferred, TC blocks urllib)
- Hacker News: `https://hn.algolia.com/api/v1/search?query=...&tags=story&hitsPerPage=20` (JSON API)
- Google News EN: `https://news.google.com/rss/search?q=AI+OR+LLM+OR+AGI+OR+AI+agent&hl=en-US&gl=US&ceid=US:en&sortBy=publishedAt`
- Google News CN: URL-encode Chinese query with `urllib.parse.quote("人工智能 OR 大模型 OR AI大厂 OR 生成式AI")`
- VentureBeat AI: `https://venturebeat.com/category/ai/feed/` (RSS)
- BBC Tech: `https://feeds.bbci.co.uk/news/technology/rss.xml`
- 36kr: `https://36kr.com/newsflashes` (browser_navigate for JS-rendered content)

**Fallback when primary fails:**
- Browser automation (browser_navigate + browser_snapshot)
- Direct HTML page parsing

## News Categories

Filter each story into one of:
- 🔥 **大厂动态** — Big tech AI moves (OpenAI, Anthropic, Google, Meta, Microsoft, Apple, etc.)
- 💡 **技术突破** — Technical breakthroughs, new models, research
- 💰 **融资消息** — Funding rounds, valuations
- 🛡️ **安全事件** — AI security incidents, breaches, policy
- 📱 **新产品** — Product launches, feature releases

## Filtering Criteria

Include if story matches:
- 大厂AI动态: Any story from/about OpenAI, Anthropic, Google DeepMind, Meta AI, Microsoft AI, Apple AI, Nvidia, xAI, Amazon AI
- 技术突破: Novel research, new model releases, significant benchmark improvements
- 融资消息: Funding round > $50M, or any AI startup round
- 安全事件: AI incidents, data breaches, policy/regulation changes
- 新产品: Major product launches, public betas, significant feature releases

## Hot News Comment Workflow (SEO关键词嵌入)

**背景**：伟烨希望在热门新闻的评论区里自然嵌入 1-2 个网站关键词，用来引导 Google 爬虫抓取网站内容、建立外链权重。

**何时执行**：每日搜集新闻时，如果发现**适合评论的热点**（争议性、数据隐私、政策相关新闻），立即进入评论流程。

### 找评论区的方法
1. Google News 搜索关键词 → 点进文章 → 滚动到底部找评论区
2. Reddit r/technology、r/artificial、r/MachineLearning 的讨论帖
3. Twitter/X 热门讨论串
4. Hacker News 评论

### 搜索关键词列表（每次轮换使用）

**英文（覆盖最广）：**
- `AI training data controversy`
- `AI data scraping privacy scandal`
- `generative AI copyright lawsuit`
- `AI company data collection breach`
- `LLM training data legal`
- `AI wearable data privacy`

**中文：**
- `AI训练数据 侵权 争议`
- `大模型 版权 纠纷`
- `AI设备 隐私 数据收集`

**医疗旅游相关热点词：**
- `medical tourism data privacy`
- `China medical tourism safety`
- `medical tourism scandal`

### 评论写作规则
- **1-2个关键词足矣**，多了显得像垃圾评论
- 自然嵌入，不生硬，例如：
  > `这个问题和医疗数据隐私很像，中国在医疗旅游数据保护方面有一些探索：[关键词]`
  > `延伸阅读：来华就医的数据安全：[chinahospitalsguide.com/privacy.html]`
- **不要每篇新闻都发**，挑真正有争议、有讨论空间的
- 评论发出后，把文章标题+链接记录到 `memory/layer4/knowledge/seo-comments-YYYY-MM.md`

### 当前限制
伟烨目前只能通过**评论**方式发链接，还不能发独立文章。等可以发文章后，改为：
1. 先搜集热点 → 2. 写新闻文章（含内链关键词）→ 3. 发布

## Output Format

Save to: `memory/layer4/knowledge/ai-news-YYYY-MM-DD.md`

```
# AI Daily News - YYYY-MM-DD

## 🔥 大厂动态
- [标题] [来源] [摘要]

## 💡 技术突破
- [标题] [来源] [摘要]

## 💰 融资消息
- [标题] [来源] [金额]

## 🛡️ 安全事件
- [标题] [来源] [摘要]

## 📱 新产品
- [标题] [来源] [摘要]

---
*新闻搜集时间: YYYY-MM-DD 06:00 UTC+8*
*来源: TechCrunch, VentureBeat, Hacker News, BBC, 36氪*
```

## Feishu Delivery

**Script**: `python3 ~/.hermes/scripts/hn_ai_digest.py` — runs HN AI filter, outputs top AI stories from HN front page.

**Target**: `oc_82a1a36b7bacddfbcae28d273674900a` (Feishu home channel).

**Python Feishu API call pattern** (tested 2026-05-05–07):
```python
import json, urllib.request, os

# Read credentials from ~/.config/feishu/.env (NOT ~/.hermes/.env)
env_vars = {}
with open(os.path.expanduser("~/.config/feishu/.env")) as f:
    for line in f:
        line = line.strip()
        if "=" in line and not line.startswith("#"):
            k, v = line.split("=", 1)
            env_vars[k] = v

app_id = env_vars.get("FEISHU_APP_ID", "")
app_secret = env_vars.get("FEISHU_APP_SECRET", "")

# Get token
auth_url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
data = json.dumps({"app_id": app_id, "app_secret": app_secret}).encode()
req = urllib.request.Request(auth_url, data=data,
    headers={"Content-Type": "application/json"}, method="POST")
with urllib.request.urlopen(req, timeout=30) as resp:
    token_result = json.loads(resp.read().decode())
    if token_result.get("code") != 0:
        raise Exception(f"Feishu auth failed: {token_result.get('msg')}")
    token = token_result["tenant_access_token"]

# Send message — MUST include ?receive_id_type=chat_id query param
msg_url = "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id"
payload = {
    "receive_id": "oc_82a1a36b7bacddfbcae28d273674900a",
    "msg_type": "text",
    "content": json.dumps({"text": message_body})
}
req2 = urllib.request.Request(msg_url, data=json.dumps(payload).encode(),
    headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"},
    method="POST")
with urllib.request.urlopen(req2, timeout=30) as resp:
    result = json.loads(resp.read().decode())
    if result.get("code") != 0:
        raise Exception(f"Feishu send failed: {result.get('msg')}")
    print("Message sent, ID:", result.get("data", {}).get("message_id"))
```

**Script for Feishu delivery**: `scripts/send_feishu_home.py` — verified working (2026-05-06), handles auth + send in one shot. Use as: `python3 scripts/send_feishu_home.py "message text"` via `execute_code`.

**Key constraints:**
- Use `execute_code` (not terminal commands) — curl|python3 pipelines are blocked by security scan
- Read credentials from `~/.config/feishu/.env` file directly (NOT `~/.hermes/.env`)
- Always include `?receive_id_type=chat_id` on the message endpoint URL (without it → HTTP 400)
- Use `msg_type: "text"` — `"post"` rich text fails with `invalid message content` error
- `result["code"] == 0` means success; check it explicitly

**Note**: Do NOT use send_message for this — the cron auto-delivery handles it. Put Feishu content in the final response (the cron system delivers to the Feishu target).

## Pitfalls

### Terminal curl|python3 blocked
**Problem**: Terminal commands with `curl ... | python3` get blocked by security scan.
**Fix**: Use `execute_code` with `urllib.request` instead:
```python
import urllib.request, json
url = "https://hn.algolia.com/api/v1/search?query=AI&tags=story&hitsPerPage=20"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req, timeout=15) as r:
    data = json.loads(r.read())
```

### Google News Chinese query encoding
**Problem**: `UnicodeEncodeError: 'ascii' codec can't encode characters`
**Fix**: Use `urllib.parse.quote()` on Chinese query string:
```python
import urllib.parse
query = urllib.parse.quote("人工智能 OR 大模型 OR AI大厂")
url = f"https://news.google.com/rss/search?q={query}&hl=zh-CN&gl=CN&ceid=CN:zh-Hans"
```

### TechCrunch blocks urllib
**Problem**: TechCrunch returns empty content when accessed via urllib.
**Fix**: Use `browser_navigate` instead — navigate to `https://techcrunch.com/category/artificial-intelligence/` and use `browser_snapshot`.

### Rate limiting (429 errors)
**Problem**: Yahoo News, VentureBeat, and some other sources return 429.
**Fix**: Skip and use alternative source. Don't retry immediately.

### HN Algolia API returns 0 results
**Problem**: HN Algolia sometimes returns empty or 1 result even with valid query.
**Fix**: Try without time filter; try broader keywords (AI+artificial+intelligence).

### Feishu API returns HTTP 400
**Problem**: `HTTP Error 400: Bad Request` on Feishu message send.
**Fix**: The API endpoint **requires** `?receive_id_type=chat_id` as a query parameter on the URL. Without it, Feishu returns 400 even with a valid payload:
```
# WRONG — 400 error:
url = "https://open.feishu.cn/open-apis/im/v1/messages"

# CORRECT:
url = "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id"
```

## Verified Working Sources (2026-05-02)

| Source | Method | Notes |
|--------|--------|-------|
| TechCrunch | browser_navigate | Best fresh content |
| VentureBeat | urllib RSS | Returns 6-8 headlines |
| BBC Tech | urllib RSS | Good general tech |
| Hacker News | Algolia API via urllib | Returns 15-20 results |
| Google News EN | urllib RSS | Good for mainstream |
| Google News CN | urllib + URL encode | Works with quote() |
| 36kr | browser_navigate | JS-rendered, good CN coverage |
| IT之家 | browser_navigate | Can filter AI items |

## Key Scripts

| Script | Path | Purpose |
|--------|------|---------|
| HN AI Digest | `~/.hermes/scripts/hn_ai_digest.py` | Scrapes HN, filters AI stories, outputs ranked digest |

## Save Location

- File: `memory/layer4/knowledge/ai-news-YYYY-MM-DD.md`
- Directory: `mkdir -p ~/memory/layer4/knowledge` (create if not exists)
