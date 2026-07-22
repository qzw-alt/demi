---
name: patient-cases-public-outreach
description: Generate public-facing promotional/posting assets for individual overseas patients — Douyin vertical-image carousels, Xiaohongshu post images, WeChat Moments posters, LinkedIn image posts, peer-network celebration posts. Triggers include "帮我生成像上次一样的抖音图", "做个海报发小红书", "用患者案例拍短视频文案", "抖音求医求助", "patient social-media post", "发个朋友圈", "做个海报", "case completed 配图", "celebrate 这个 case". Two output paths — Pillow 1080×1920 PNG for 抖音 / 小红书 vertical carousels, and HTML 1080×1080 / 1080×1350 that Weiye screenshots himself for 朋友圈 / LinkedIn / Twitter image posts. HTML path is for case-completed celebration posts where the audience is hospital-side or peer-network, NOT for 求医求助. Output is always files plus a copy-pasteable plain-text caption with no extra notes. Owns the reusable Pillow pipeline, the HTML screenshot pipeline, the text-generation rules, and the privacy/safety baseline.
version: 1.1.0
author: Hermes Agent
platforms: [linux]
metadata:
  hermes:
    tags: [medical-tourism, social-media, douyin, xiaohongshu, wechat, image-generation, patient-cases, html-screenshot, friends-circle, linkedin]
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

### ⚠️ 选哪条工作流：Pillow 求助图 vs HTML 朋友圈图（2026-07-11 新增）

**触发器分流**：

| 伟烨说 | 用哪条 | 输出形态 | 受众 |
|---|---|---|---|
| "抖音求医" / "小红书" / "医生找过来" / "找不到医院" | **Pillow 路径（Step 4A）** | 1080×1920 PNG × 4-6 张 | 大众 / 短视频算法 |
| "发个朋友圈" / "做个海报" / "庆祝这个 case" / "对国内医院端资源" / "对同行人脉" | **HTML 路径（Step 4B）** | 1080×1080 / 1080×1350 HTML × 6-9 张，伟烨自己截图 | 同行 / 医生 / 医院资源方 |

**关键差异**：

- **Pillow 路径**面向"找不到医院想被看见"，叙事重情绪 + 求助腔
- **HTML 路径**面向"已经成功接诊想被认知"，叙事重方法论 + 业务能力
- **绝对不能互换**：求医帖用 HTML 风格显得冷冰冰，朋友圈庆祝帖用 Pillow 风格显得像求助（劝退医院决策者）

### ⚠️ HTML 路径的"国内医院端资源对接"叙事角度（2026-07-11 新增）

**触发器**：伟烨明示朋友圈面向"国内医院资源 / 同行人脉"，**不**面向国内患者。

**为什么这个角度重要**：在国内，99% 的病人直接挂号九院就行，**不需要中介**。朋友圈文案如果说"我们帮你挂号九院"，会被同行笑死。真正稀缺的是 **跨境患者通道的协调能力**——也就是能调跨院专家 MDT、能做多语言病例整理、能做海外 SEO。

**叙事重心**：

1. **不写"接了多少病人"**——写"完成了一个 3 病并发的复杂 case"
2. **不写"价格便宜"**——写"我们不是医院中介，是跨境患者通道共建方"
3. **不写"医院推荐"**——写"我们帮医院补跨境这一段"
4. **CTA 不能是"联系我挂号"**——CTA 是"如果你们科室有国际化患者承接需求，私信聊"

**化名策略**（与 Pillow 求助图不同）：

- 求助帖：M 女士 / 一位拉美患者（重情绪）
- 朋友圈庆祝帖：M 女士（Maria 首字母）/ "国际患者" / 隐医院名 / 病种可以模糊化为"罕见血管并发"（重方法论）

**两套都遵守**：

- ❌ 不写真名
- ❌ 不写具体联系方式 / 微信号 / 邮箱 / WeChat ID
- ❌ 不写承诺（"100% 治好""保证"）
- ✅ Maria 真实给过的 +86 157 6310 7083 / 434338480@qq.com 在伟烨工作号层面 OK，不算"患者隐私"

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

### Step 4：图片生成（按工作流分流）

#### Step 4A：Pillow 竖屏图生成（抖音/小红书 求助图）

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

#### Step 4B：HTML 朋友圈/LinkedIn 配图（HTML 截图路径，2026-07-11 新增）

**触发**：伟烨明示"朋友圈面向国内医院端资源 / 同行人脉" → 走这条。

**与 Pillow 路径的核心差异**：

- Pillow 是 agent 直接产出 PNG；HTML 是 agent 产出 HTML 文件 + 伟烨在 Chrome 自己截图
- HTML 路径适合"信息密度高、需要排版漂亮、需要微信/LinkedIn 这种社媒适配"的场景
- HTML 路径**视觉一致性由 agent 控**，截图清晰度由伟烨屏幕分辨率决定（一般 1080×1080 OK）

**技术约束**：

- **尺寸**：方图 1080×1080（朋友圈 9 图模板适配）、竖图 1080×1350（4:5 推荐，信息密度高时用）
- **字体**：HTML 里写 `-apple-system, "PingFang SC", "Microsoft YaHei", sans-serif` —— **不依赖网络字体**，伟烨截图前打开 HTML 不需要联网
- **品牌色**（已用 Maria Rios case 验证，深蓝系）：`#1e3c72` / `#0c1830` / `#17345f` / `#2a5298`，强调色 `#ff6b6b`
- **6-9 张叙事顺序**（Maria Rios 案标准模板，可复用）：
  - **图 1（封面）**：伟烨自己截图你的 hero / 品牌图
  - **图 2（病种复杂度）**：3 病并发等关键数字
  - **图 3（受众画像）**：跨境患者 4 大来源地占比
  - **图 4（合作模式）**：3 档机构合作（轻 / 中 / 重）
  - **图 5（医院端价值）**：5 项医院端不做的我们做
  - **图 6（MDT 案例脱敏）**：伟烨自己截图真实邮件 + 脱敏
  - **图 7（复盘洞见）**：3 条方法论
  - **图 8（CTA）**：合作邀请 + 私信引导
- **每张图底部固定 footer**：`CHINA HOSPITALS GUIDE · 跨境患者通道共建`（品牌锚）
- **存放路径**：`chinahospitalsguide/figma-friends-circle/`（untracked，跟其他 draft 同惯例）
- **伟烨的截图动作**：浏览器打开 HTML → 全屏 (F11 / Cmd+Ctrl+F) → Cmd+Shift+4 空格 / Win+Shift+S 选窗口 → 保存到 ~/Downloads/

**给伟烨的交付形式**（重要：触发"复制用"模式规则）：

- ❌ **不**在飞书对话里附 ⚠️ 截图注意事项、要不要改、配色建议
- ✅ **直接**给"打开 HTML → 截图"的 3 步说明 + 文件路径清单
- ✅ **等伟烨反馈"风格 OK / 某张不行"才调整**

#### Step 4B-Plus：Playwright headless 自动化 HTML→PNG（2026-07-11 跑通）

**触发**：伟烨说"你直接发图给我" / "配图你做出来我直接用" → 跳过浏览器手动截图，用 Playwright headless 自动化出 PNG。

**为什么这条存在**：HTML 路径原本要伟烨自己 Chrome 截图 → 但伟烨可能没空 / 不方便 / 嫌麻烦。**让 agent 直接出 PNG**，伟烨在飞书 `MEDIA:` 一键转发到朋友圈。

**环境前置**（一次性安装，venv 已经有 pip）：

```bash
# 在 Hermes venv 里装 playwright（PEP 668 不会拦 venv）
~/.hermes/hermes-agent/venv/bin/python -m pip install playwright

# 下载 Chromium headless shell（114MB，pyppeteer 同级，但更稳）
~/.hermes/hermes-agent/venv/bin/python -m playwright install chromium --with-deps
```

**渲染脚本**（存到 `figma-friends-circle/render-to-png.py`，每次复用）：

```python
"""
Batch render *.html to PNG using Playwright (headless Chromium).
Detects .card element dimensions, sets viewport, screenshots full-page.
"""
import asyncio, os, glob
from pathlib import Path
from playwright.async_api import async_playwright

ROOT = Path("/path/to/figma-friends-circle")
OUT = ROOT / "png"; OUT.mkdir(exist_ok=True)
HTML_FILES = sorted(glob.glob(str(ROOT / "*.html")))

async def render_one(browser, html_path):
    page = await browser.new_page(viewport={"width": 1080, "height": 1350})
    await page.goto(f"file://{html_path}", wait_until="networkidle")
    width, height = await page.evaluate("""() => {
        const card = document.querySelector('.card') || document.body;
        const r = card.getBoundingClientRect();
        return [Math.ceil(r.width), Math.ceil(r.height)];
    }""")
    await page.set_viewport_size({"width": width, "height": height})
    await page.wait_for_timeout(150)  # 让布局稳定
    out_path = OUT / f"{html_path.stem}.png"
    await page.screenshot(path=str(out_path), full_page=False)
    await page.close()
    return out_path, width, height

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        for f in HTML_FILES:
            out, w, h = await render_one(browser, Path(f))
            print(f"  ✓ {Path(f).name}  {w}x{h}  {os.path.getsize(out)/1024:.1f} KB")
        await browser.close()

asyncio.run(main())
```

**跑法**：

```bash
~/.hermes/hermes-agent/venv/bin/python ~/chinahospitalsguide/figma-friends-circle/render-to-png.py
```

**输出位置**：`figma-friends-circle/png/*.png`

**飞书交付**：每张图用 `MEDIA:/绝对/路径/xxx.png` 行内发，伟烨一键转发。

**坑 + 经验**（Maria Rios case 实测）：

- **render-to-png.py 不要写进 git**——它是 untracked 脚本，跟 HTML 同目录
- **HTML 文件里的 viewport meta 不要设置**（如 `<meta name="viewport" content="...">`），Playwright 默认按 `set_viewport_size` 来
- **`wait_until="networkidle"` 在带 Google Fonts 的 HTML 会卡 30 秒**——HTML 里只用系统字体（`-apple-system, "PingFang SC"`），不用 `@import url(...)`，渲染快且不依赖网络
- **`networkidle` 超时如果发生**，改成 `wait_until="domcontentloaded"` + `wait_for_timeout(500)` 也行
- **多张图批量渲染**：每张独立 `new_page`，关闭前 `await page.close()` —— 不要图省事复用 page

**HTML 路径 vs Playwright 自动化的取舍**：

| 维度 | HTML 路径（伟烨手动截图） | Playwright 自动化 |
|---|---|---|
| 适用 | 伟烨有空 / 想本地控制截图质量 | 伟烨直接要图 / 朋友圈发布前批量出 |
| 风险 | 浏览器兼容性问题（不同 Chrome 字号不同） | Playwright 默认无头，渲染稳定 |
| 时间 | 伟烨手动 5 分钟 | agent 自动 30 秒 |
| 优先 | 第一次出图（让伟烨看效果） | 后续批量化（定了风格后批量出） |

**默认路径**：第一次出图走 HTML（让伟烨看效果 + 拍板风格）→ 风格定下来后用 Playwright 自动化出最终 PNG（伟烨直接用）。

**配套朋友圈文案（同时产出）**：

- 长度 5-8 行（不算拆分，纯文本，不拆段）
- 4 种叙事角度，**默认甲+乙混合**（案例叙事 + 行业洞察）：
  - **甲. 案例叙事型**：上周完成 X case（信息密度高）
  - **乙. 行业洞察型**：为什么这一单难做（业务复盘）
  - **丙. 品牌定位型**：我们做的不是医院中介，是 MDT 协调
  - **丁. 团队能力型**：这单是怎么拼出来的（过程 + 团队）
- 医院端朋友圈 vs 中介朋友圈**叙事重心不一样**（见上方"⚠️ 国内医院端资源对接"那段）
- **CTA 必须清晰**：私信 / 微信直接联系，不是"欢迎咨询"

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