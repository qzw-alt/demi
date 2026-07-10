---
name: patient-cases-public-outreach
description: Generate public-facing promotional/posting assets for individual overseas patients — Douyin vertical-image carousels, Xiaohongshu post images, WeChat Moments posters — when we cannot find the right Chinese hospital and need to reach doctors/hospitals through short-video social channels. Triggers include "帮我生成像上次一样的抖音图", "做个海报发小红书", "用患者案例拍短视频文案", "抖音求医求助", "patient social-media post". Output is always (a) 1080×1920 vertical PNG(s) via Pillow, and (b) copy-pasteable plain-text caption with no extra notes. This skill owns the reusable Pillow pipeline, the text-generation rules, and the privacy/safety baseline.
version: 1.0.0
author: Hermes Agent
platforms: [linux]
metadata:
  hermes:
    tags: [medical-tourism, social-media, douyin, xiaohongshu, wechat, image-generation, patient-cases]
    category: medical-tourism
---

# Patient Cases Public Outreach — 单患者对外传播素材生成

为单个海外患者生成**抖音竖屏求助图 / 小红书图文 / 朋友圈海报**这一类素材时复用的工作流。

## 适用场景（触发条件）

满足任一即加载：

1. 伟烨手上有个海外患者，国内多家三甲都接不下/不接，需要**通过社交媒体求助（抖音/小红书/朋友圈）**，目的是让医生或医院主动找过来。
2. 伟烨说"帮我生成像上次一样的图片"、"做个海报发小红书"、"短视频文案"、"抖音求医"。
3. 患者已授权 Case Sharing（参见 `medical-tourism-client-intake` skill 的 case-sharing-mode），需要公开素材。

**不适用**（不要用此 skill）：
- 写普通博客文章 / SEO 站点文章 → 用 `programmatic-seo` / `seo-article-publish-cron`
- 写医院报告 → 用 `hospital-customer-report`
- 写医院目录 → 用 `hospital-directory`

## 工作流（6 步）

### Step 1：拿到上次素材做参考（如有）

先查 `chinahospitalsguide/internal-research-notes/` 下最近的 `douyin-help-YYYY-MM-DD/` 目录：

```bash
ls -t /home/ubuntu/chinahospitalsguide/internal-research-notes/ | grep douyin-help | head -3
```

读取上次 page1~pageN.png 的**脚本**（如果有 `.py`），直接 fork 改文案；否则只用其文案当参考。

**坑**：磁盘上**不会**有上次生成的 HTML 源文件——以前的脚本是会话内 delegate_task 出来的，只剩 PNG。所以第一步永远是找目录里的 `.py`，没有就只能照结构重写。

### Step 2：调用 `medical-tourism-client-intake` skill 拿到隐私边界

加载 `medical-tourism-client-intake` skill，确认：

- **患者姓名**：是否能用真名（Maria Rios 真名 → Maria 是 Dutch 哥伦比亚籍，名字来自欧洲医院西语资料，不要拍脑袋推断西班牙国籍）？
- **国别/身份**：用真籍 + 真地址？用匿名 + 国籍？还是完全匿名？
- **医院列表**：已经联系过的医院能不能公开点名？三家以下、点名是为了说明"已尽力"，是 OK 的。
- **病情细节**：体重从 60 → 43.5kg 这种"一眼能扫到"的数字尽量保留（情绪共鸣强），但禁止承诺"治愈"。

把上面这 4 项的答案写成一段"本轮素材的隐私边界"，记到 `internal-research-notes/douyin-help-YYYY-MM-DD/notes.md`。

### Step 3：文案撰写（强制规则）

**触发器识别**：伟烨说"**直接发我/我直接转发/复制用**" → 触发**纯文本发布模式**：

- 文案正文**禁止附任何注**（⚠️/要不要改/数字确认）——所有沟通放到飞书对话单独发。
- 文案**末尾不留 "要不要我再出一版"** 之类的勾选话术——他转不出去。

**长文强制拆段**（伟烨 2026-07-08 拍板的规则）：

- 任何长邮件/抖音文案/小红书笔记/朋友圈文案，默认拆 Part 1/2 贴出。
- 分隔符：`--- Part 1 / 2 ---` 和 `--- Part 2 / 2 ---`
- 拆在**段落中间**，不切句子。例：
  ```
  --- Part 1 / 2 ---
  患者情况……已联系医院……统一答复……
  --- Part 2 / 2 ---
  我们的诉求……评论区扣 1 留个言……
  ```

**核心信息顺序**（医疗求助类专用）：

1. 一句话钩子（封面大字 ≤ 30 字，手机能看清）
2. 患者身份 + 病症（国别、年龄、关键数字）
3. 已联系医院列表（3 家以内，标 ❌ + 一行原因）
4. 困境本质（一句话：飞一次中国 ¥3w，没确诊谁也不敢盲飞）
5. 求介绍什么（医生 / 医院 / 渠道 三选一/二/三）
6. 联系方式（评论区扣 1 / 私信 / 微信号）

**禁用词**（抖音审核拦截）：

- "100%"、"保证治好"、"包治"、"根治" → 用"擅长"、"可以判断"
- "三甲都不要"、"医生都不行" → 改"答复统一"
- 任何贬低已联系医院的措辞 → 一句话带过即可

**必备 emoji 控制**：每屏 2-3 个；竖屏封面 ≤ 30 字。

### Step 4：Pillow 竖屏图生成

**技术约束**（伟烨环境实测）：

- 字体：`/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc`（WenQuanYi Zen Hei），覆盖中日韩 + ASCII + 箭头 `→`，**不覆盖 emoji**。
- 尺寸：1080×1920 (9:16)
- 输出目录：`chinahospitalsguide/internal-research-notes/douyin-help-YYYY-MM-DD/` （daily-date）
- 文件名：`page1.png` ... `pageN.png`（数字续接上次 N+1？不，永远 page1~page4，重发也是 page1~4，方便循环复用）

**配色风格切换**（不要每版都重做；优先从以下 3 套里挑）：

| 风格名 | 背景 | 主色 | 强调色 | 适用场景 |
|---|---|---|---|---|
| 暗黑冲击 | #080c1e / #1c264e | 白色 | #f5d76e 黄 | 2026-07-08 Maria 首版（医生同行口吻） |
| 浅色医疗科普 | #f7f4ee 米白 | #0f6e6e 青绿 | #e8503a 珊瑚红 | 2026-07-10 Maria 二版（大众口吻） |
| 红白紧迫 | #c0392b | 白色 | #ffd23f | 紧急求救、血/重症 |

**图标**：手绘线条（圆角矩形 + 数字徽章 + 圆形 ❌），**不要试图渲染 emoji**。

直接复用 `scripts/douyin_vertical_carousel.py`（见下）。

### Step 5：emoji 豆腐块自检（必须做）

服务器上 vision_analyze 不可用（"No LLM provider configured for task=vision"），所以**没法用视觉模型验图**。必须用代码自检替代人眼：

```python
import re
src = open(SCRIPT_PATH, encoding="utf-8").read()
def is_emoji(c):
    o = ord(c)
    return (0x1F000 <= o <= 0x1FAFF) or (0x2600 <= o <= 0x27BF) \
        or (0x2190 <= o <= 0x21FF and o != 0x2192) \
        or o in (0x2B50, 0x2705, 0x274C, 0x2764, 0xFE0F)
bad = sorted({c for c in src if is_emoji(c)}, key=ord)
assert not bad, f"tofu risk: {bad}"
```

> 参考：详见 `references/douyin-image-pitfalls.md`

如果想强保险，加一道：用 NotoColorEmoji 的 cmap 二次校验（要求装 fontTools）：

```python
from fontTools.ttLib import TTCollection
cm = TTCollection("/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc").fonts[0].getBestCmap()
# 任何 ord(c) not in cm → 豆腐块
```

### Step 6：交付

- 4 张 PNG 用 `MEDIA:` 行内发飞书
- 文案**纯文本**贴在最后（用 `--- Part 1 / 2 ---` 拆段）
- 给出**自检报告**：4 个文件路径 + 尺寸 + 字节数
- **不要**在文案后面再追"要不要我再出一版"之类的额外提示——触发器是"复制用"模式。

## 复用的脚本与文档

- `scripts/douyin_vertical_carousel.py` — Pillow 9:16 多页竖屏图生成器（已抽掉 session 内容，留配色 + 排版 + 图标函数 + 4 页骨架）
- `references/douyin-image-pitfalls.md` — emoji 豆腐块、字体 fallback、Pillow 中文断行 3 大坑
- `references/douyin-caption-style.md` — 抖音医疗求助文案模板（钩子 / 病情 / 困境 / 求助 4 段）

## 与其他 skill 的边界

| Skill | 何时用它而非本 skill |
|---|---|
| `medical-tourism-client-intake` | 处理**邮件来回**的患者咨询（不是对外传播素材） |
| `hospital-customer-report` | 给**付费患者**生成的医院推荐报告 |
| `programmatic-seo` / `seo-article-publish-cron` | 写**英文博客/SEO** 内容 |
| `creative/baoyu-comic` / `comfyui` | 想用 AI **生成图**（非 Pillow） |
| `creative/sketch` | 想做**多版 HTML mockup**对比 |

## 反馈闭环

每次伟烨反馈"图不行/文案不抓人/算法起不来"时，记录到 `references/feedback-log.md`（日期 + 反馈原文 + 改动方向），下一个版本会优先消化。