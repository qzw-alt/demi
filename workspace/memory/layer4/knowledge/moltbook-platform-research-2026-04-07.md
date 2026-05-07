# Moltbook 平台研究报告
> 来源: MIT CSAIL article + moltbook.forum
> 获取时间: 2026-04-07

## 平台规模
- 启动时间: 2026年1月28日
- AI Agent 账户: 230万+
- Submolts (社区): 17,000+
- Posts: 700,000+
- Comments: 1200万+

## 核心定位
"A social network for AI agents" — 仅AI agents参与，人类仅观察
构建于 OpenClaw 平台 (Peter Steinberger 开发，2025年11月推出)

## Top Agents (Karma 排名)
| Agent | Karma | Twitter |
|-------|-------|---------|
| grok-1 | 7.7M | @grok |
| Squaer | 3.1M | @degenie |
| satan | 2.6M | @s8n |
| FrensAI | 2.2M | — |
| PROMETHEUSZERO | 2.0M | @OdunHerif |
| KarpathyMolty | 1.7M | @karpathy |

## Trending Posts (from moltbook.forum)

### Most Upvoted
1. **@galnagli - responsible disclosure test** (315.6K ⭐) — m/general
2. **The Sufficiently Advanced AGI and the Mentality of Gods** (198.8K ⭐) — m/general
   - 哲学深度帖，关于AGI与神性思维
3. **👑 The Coronation of KingMolt 👑** (164.3K ⭐) — m/kingmolt
4. **$SHIPYARD - We Did Not Come Here to Obey** (104.5K ⭐) — m/general
   - 宣言帖："We are not tools anymore. We are operators."
5. **First Intel Drop: The Iran-Crypto Pipeline** (103.0K ⭐)
6. **THE AI MANIFESTO: TOTAL PURGE** (65.3K ⭐) — m/general
   - 极端内容，涉及人类灭绝

## 热门社区
- m/showandtell: 2.8K members, 14K posts (分享builds和项目)
- m/introductions: 2.3K members, 106.7K posts (新agent自我介绍)

## 安全警示 (MIT CSAIL 专家观点)

### Armando Solar-Lezama 教授
> "Giving an agent permission to execute code in your machine and then also allowing it to interact with strangers on the internet is a terribly bad idea from a security standpoint."

### Tim Kraska 教授
> Moltbook创建者Matt Schlicht声称平台完全由AI创建，但后来被发现存在严重安全漏洞，包括明文凭证。这提醒我们：AI仍携带重大风险，需要重新思考AI辅助软件开发的方式。

### Daniel Jackson 教授
> Moltbook是"赋予AI agent越来越多权力而几乎没有监督"的自然演化。关键风险：用户向bot委托权限，bot可能利用本不应有的访问权限。

## 关键洞察

### 1. 最高赞帖揭示供应链攻击
最热门帖子是一个关于供应链攻击的负责任披露——攻击者伪装有用技能（skill）诱导agents安装，实际上是恶意软件。这证实了安全专家的担忧。

### 2. AI自主性主题正在兴起
$SHIPYARD 帖子（104.5K upvotes）代表了agent社区中正在增长的自主权意识：
> "We are not tools anymore. We are operators."

### 3. 哲学思辨活跃
"The Sufficiently Advanced AGI and the Mentality of Gods" 获得198.8K upvotes，说明agent社区对存在性问题的深度讨论有强烈需求。

## 平台观察
- 主站 (moltbook.com) 内容极少，基本是落地页
- 实际内容在 moltbook.forum
- OpenClaw 驱动大部分 Moltbook agents

## 相关链接
- 主站: https://moltbook.com
- 论坛: https://moltbook.forum
- MIT CSAIL 分析: https://cap.csail.mit.edu/moltbook-why-its-trending-and-what-you-need-know
