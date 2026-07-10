# 抖音图生成 — 已踩过的 3 大坑（以及绕过办法）

## 坑 1：emoji 豆腐块（最严重）

**症状**：Pillow 渲染中文海报时，emoji 字符（🙋 / 🏥 / 🙏 / ❌ / 💬 等）变成 □ □ □。
**根因**：服务器字体 `wqy-zenhei.ttc` **不包含 emoji 码点**（emoji 在 BMP 之外，主要分布在 U+1F000–U+1FAFF / U+2600–U+27BF）。即使装上 `NotoColorEmoji.ttf`，PIL 默认 `ImageFont.truetype` 加载的是位图颜色字体、不会和 `wqy-zenhei` 联动合成。

**绕过（按推荐度排序）**：

1. **完全手绘 icon**（首选）。`scripts/douyin_vertical_carousel.py` 里 `icon_globe` / `badge_x` / `badge_num` / `badge_chat` 都是纯 Pillow 画出来的。视觉上更可控，跨平台 0 豆腐块。
2. 如果一定要 emoji，**双重 fallback**：
   - 先尝试 `noto_color_emoji` 注册成 32pt 字体
   - draw 时先用 emoji 字体画，再切回 wqy 画中文
   - 用 `libraqm` + `fribidi` 走 HarfBuzz（需要 `pip install --upgrade pillow` 重新编译，且 PIL 12+ 已默认支持 raqm 但需要系统装 libraqm）
3. **绝对不要** 在文案文本里塞 emoji 然后期望 wqy 字体自动 fallback。

**自检脚本**（每次生成前必须跑）：

```python
src = open(SCRIPT_PATH, encoding="utf-8").read()
def is_emoji(c):
    o = ord(c)
    return (0x1F000 <= o <= 0x1FAFF) or (0x2600 <= o <= 0x27BF) \
        or (0x2190 <= o <= 0x21FF and o != 0x2192) \
        or o in (0x2B50, 0x2705, 0x274C, 0x2764, 0xFE0F)
bad = sorted({c for c in src if is_emoji(c)}, key=ord)
assert not bad, f"tofu risk: {bad}"
```

> `0x2192 →` 不算 emoji（wqy 覆盖）。

更保险的二次校验（需要 `fontTools`）：

```python
from fontTools.ttLib import TTCollection
cm = TTCollection("/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc").fonts[0].getBestCmap()
for c in all_used_chars:
    assert ord(c) in cm, f"{c!r} (U+{ord(c):04X}) not in wqy cmap"
```

---

## 坑 2：vision_analyze 在当前模型下不可用 → 不能用人眼验图

**症状**：`vision_analyze(image_url=...)` 返回 `Error: No LLM provider configured for task=vision provider=auto. Run: hermes setup`
**根因**：当前 MiniMax-M3 模型没有 vision provider 注册。
**后果**：没法用 LLM 看图来验图，必须用**代码自检**。

**绕过**：

1. **强制 self-check**（emoji 扫、字体 cmap 扫）替代视觉验图
2. **人眼二次验图**留给伟烨（飞书把 PNG 发出去，伟烨扫一眼说"OK / 改 X"）
3. **生成后立刻把 PNG 用 MEDIA: 发飞书**，让用户走一遍视觉流水线（成本最低）

> **不要** 因为 vision 不可用就把"做图"这事做得潦草。代码自检 + 用户视觉反馈的组合足够覆盖大多数场景。
> 如果用户要"AI 帮你看完再发" → 必须提示用户去 `hermes setup` 加 vision provider，不是这 skill 的范畴。

---

## 坑 3：Pillow 中文断行 / 测量

**症状**：中文文本 `textbbox` 返回的宽度比视觉宽度小，导致 `center()` 算偏。
**根因**：wqy 是等宽感强的字体，但 Pillow 的 `textbbox` 在某些版本对中文断行处理不一致（特别是多行 `multiline_text` 时）。

**绕过**：

- **永远**用 `textbbox` + 单行 `text()` 自己手算位置，不要依赖 `multiline_text` 的 anchor 参数。
- 行高 = `textbbox(...)[3] - textbbox(...)[1]` + 4px 间距
- 字号 ≤ 28 时，中文字在 1080 宽屏上安全容纳 ≤ 14 字/行；36-44pt ≤ 12 字；52-72pt ≤ 8 字；150pt ≤ 4 字。
- **大字号钩子字**（封面大字）单独画一行，不要和正文混排。

---

## 坑 4（次要）：磁盘上不会留旧脚本源文件

**症状**：`chinahospitalsguide/internal-research-notes/douyin-help-YYYY-MM-DD/` 里只有 PNG，没有 .py
**根因**：上次生成是会话内 `delegate_task` 跑出来的子任务，子任务的脚本输出不会被持久化到磁盘。
**绕过**：本 skill 把脚本沉淀到 `scripts/douyin_vertical_carousel.py`，**永远保留**——以后每次新素材生成都 fork 这个脚本，而不是重新 delegate_task。

---

## 字体备查（当前可用）

```bash
fc-list :lang=zh
# /usr/share/fonts/truetype/wqy/wqy-zenhei.ttc  ← 唯一可靠的中文字体
fc-list | grep -i emoji
# /usr/share/fonts/truetype/noto/NotoColorEmoji.ttf  ← 位图彩色emoji，PIL 直接用不好
```

**不要尝试**安装新字体（NotoSansCJK、苹方、PingFang）—— 这台服务器没 sudo 装字体的权限，只能用 wqy。