#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
douyin_vertical_carousel.py — 抖音/小红书/朋友圈 9:16 求助图生成器
================================================================

来源：本会话(2026-07-10) Maria Rios 二版 v2 的脚本，session 内容已剥光，
只保留：字体加载、配色切换、4 页骨架、icon 工具函数。

每次新素材生成，只需在文末 CAROUSEL_CONTENT 字典里改文字 / 配色 / 标题即可。

依赖：Pillow 12.x (>=10 即可)
字体：/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc
      — 不覆盖 emoji，所以本脚本禁止渲染任何 emoji，icon 全手绘。
"""

import os
import sys
from PIL import Image, ImageDraw, ImageFont

# ---------- 默认参数（可被命令行覆盖） ----------
W, H = 1080, 1920
FONT_PATH = "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"
DEFAULT_OUT = "/home/ubuntu/chinahospitalsguide/internal-research-notes/douyin-help-{date}"

# ---------- 配色方案 ----------
PALETTES = {
    "dark": {       # 2026-07-08 Maria 首版（医生同行口吻）
        "bg": (8, 12, 30), "card": (28, 38, 78), "primary": (245, 215, 110),
        "accent": (255, 255, 255), "ink": (245, 245, 245), "muted": (150, 165, 200),
        "rule": (245, 215, 110), "footer": (245, 215, 110),
    },
    "light_medical": {  # 2026-07-10 Maria 二版（大众口吻）
        "bg": (247, 244, 238), "card": (255, 255, 255), "primary": (15, 110, 110),
        "accent": (232, 80, 58), "ink": (31, 41, 55), "muted": (107, 114, 128),
        "rule": (223, 216, 205), "footer": (201, 162, 39),
    },
    "red_urgent": {  # 紧急求救 / 重症
        "bg": (192, 57, 43), "card": (255, 255, 255), "primary": (255, 255, 255),
        "accent": (255, 210, 63), "ink": (31, 41, 55), "muted": (255, 255, 255),
        "rule": (255, 210, 63), "footer": (255, 255, 255),
    },
}


# ---------- 字体/绘图工具 ----------
def f(size):
    return ImageFont.truetype(FONT_PATH, size)


def tw(d, txt, font):
    """text width / height"""
    b = d.textbbox((0, 0), txt, font=font)
    return b[2] - b[0], b[3] - b[1]


def center(d, txt, font, cx, y, fill):
    w, h = tw(d, txt, font)
    d.text((cx - w / 2, y), txt, font=font, fill=fill)
    return y + h


def left(d, txt, font, x, y, fill):
    d.text((x, y), txt, font=font, fill=fill)
    b = d.textbbox((0, 0), txt, font=font)
    return y + (b[3] - b[1])


def card(d, x0, y0, x1, y1, r=36, fill=(255, 255, 255), outline=None):
    d.rounded_rectangle([x0, y0, x1, y1], radius=r, fill=fill, outline=outline)


# ---------- 手绘 icon（不依赖 emoji） ----------
def icon_globe(d, cx, cy, r, col, lw=8):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=col, width=lw)
    d.ellipse([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r], outline=col, width=lw - 2)
    d.line([cx - r, cy, cx + r, cy], fill=col, width=lw - 2)
    d.line([cx - r * 0.86, cy - r * 0.5, cx + r * 0.86, cy - r * 0.5], fill=col, width=lw - 3)
    d.line([cx - r * 0.86, cy + r * 0.5, cx + r * 0.86, cy + r * 0.5], fill=col, width=lw - 3)


def badge_x(d, cx, cy, r, fill, cross=(255, 255, 255)):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fill)
    o = r * 0.42
    d.line([cx - o, cy - o, cx + o, cy + o], fill=cross, width=9)
    d.line([cx - o, cy + o, cx + o, cy - o], fill=cross, width=9)


def badge_num(d, cx, cy, r, n, fill, text_col=(255, 255, 255)):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fill)
    nf = f(int(r * 1.25))
    s = str(n)
    w, h = tw(d, s, nf)
    d.text((cx - w / 2, cy - h / 2 - r * 0.16), s, font=nf, fill=text_col)


def badge_chat(d, cx, cy, r, fill):
    d.rounded_rectangle([cx - r, cy - r * 0.8, cx + r, cy + r * 0.55],
                        radius=r * 0.35, fill=fill)
    d.polygon([(cx - r * 0.35, cy + r * 0.5),
               (cx - r * 0.05, cy + r * 0.5),
               (cx - r * 0.35, cy + r * 0.95)], fill=fill)
    for dx in (-r * 0.4, 0, r * 0.4):
        d.ellipse([cx + dx - 6, cy - r * 0.15 - 6,
                   cx + dx + 6, cy - r * 0.15 + 6], fill=(255, 255, 255))


# ---------- 页面框架 ----------
def make_base(palette, brand_top, tag_top, page_idx, total_pages):
    """所有页的顶栏/底栏/页码。"""
    img = Image.new("RGB", (W, H), palette["bg"])
    d = ImageDraw.Draw(img)
    # top bar
    d.rectangle([0, 0, W, 150], fill=palette["primary"])
    bf = f(34)
    d.text((70, 52), brand_top, font=bf, fill=(255, 255, 255))
    sf = f(30)
    w, _ = tw(d, tag_top, sf)
    d.text((W - 70 - w, 56), tag_top, font=sf, fill=(220, 220, 220))
    # rule under bar
    d.rectangle([0, 150, W, 156], fill=palette["rule"])
    # page dots
    for i in range(total_pages):
        cx = W / 2 - 60 + i * 40
        col = palette["primary"] if (i + 1) == page_idx else (205, 198, 187)
        d.ellipse([cx - 9, H - 70, cx + 9, H - 52], fill=col)
    pf = f(26)
    ptxt = f"{page_idx} / {total_pages}"
    w, _ = tw(d, ptxt, pf)
    d.text((W - 70 - w, H - 78), ptxt, font=pf, fill=palette["muted"])
    return img, d


# ---------- 默认内容（用哪个患者就改这个字典） ----------
CAROUSEL_CONTENT = {
    "brand": "CHINA HOSPITALS GUIDE",
    "tag": "海外医疗求助",
    "palette": "light_medical",     # key of PALETTES
    "pages": [
        # ---- PAGE 1: 封面钩子 ----
        {
            "kind": "cover",
            "center_icon": "globe",  # globe | none
            "kicker": "一位海外血管疾病患者的中国求医路",
            "big_lines": [("4 年半", "accent"), ("求医无门", "ink")],
            "rule": "gold",           # gold | accent | none
            "sub": "她今年才 27 岁",
            "bottom_card_lines": ["海外病历齐全 · 中英双语", "只差一个愿意先看资料的医生"],
        },
        # ---- PAGE 2: 病情简介 ----
        {
            "kind": "rows",
            "title": "她是谁",
            "rows": [
                ("27 岁女性，现居荷兰", None),
                ("左肾静脉压迫综合征", "俗称「胡桃夹综合征」"),
                ("合并左髂静脉压迫", "即 May-Thurner 综合征"),
                ("病程 4.5 年，反复不缓解", None),
                ("体重 60kg → 43.5kg", "已无法正常工作与学习"),
            ],
        },
        # ---- PAGE 3: 困境 ----
        {
            "kind": "hospitals",
            "title": "联系了 3 家三甲",
            "hospitals": [
                ("北京大学第一医院", "必须本人挂号、排队一周"),
                ("中日友好医院", "门诊部无法处理外籍预审"),
                ("空军军医大学唐都医院", "军事医院不接外籍患者"),
            ],
            "summary": ("统一答复", "本人到场 → 现场审 → 排队治疗"),
        },
        # ---- PAGE 4: 求助 ----
        {
            "kind": "asks",
            "title": "只想求一个机会",
            "asks": [
                ("血管外科擅长", "胡桃夹 + 髂静脉压迫"),
                ("接受海外邮件预审", "先看影像与病历资料"),
                ("先判断能不能接诊", "确诊后患者再飞中国"),
            ],
            "cta_lines": ["有医院 · 有医生 · 有渠道", "麻烦您留个言，帮忙转发"],
            "footer": "评论区扣 1 · 私信发完整病历影像",
        },
    ],
}


# ---------- 页面渲染器 ----------
def render_cover(d, p, palette):
    if p.get("center_icon") == "globe":
        icon_globe(d, W / 2, 360, 92, palette["primary"])
    kicker_font = f(38)
    center(d, p.get("kicker", ""), kicker_font, W / 2, 520, palette["muted"])
    y = 640
    for txt, col_key in p.get("big_lines", []):
        col = palette[col_key]
        big_font = f(150)
        center(d, txt, big_font, W / 2, y, col)
        y += 170
    if p.get("rule") == "gold":
        d.rectangle([W / 2 - 230, y - 50, W / 2 + 230, y - 38], fill=palette["rule"])
    elif p.get("rule") == "accent":
        d.rectangle([W / 2 - 230, y - 50, W / 2 + 230, y - 38], fill=palette["accent"])
    sub_font = f(72)
    center(d, p.get("sub", ""), sub_font, W / 2, 1080, palette["primary"])
    bc = p.get("bottom_card_lines") or []
    if bc:
        card(d, 110, 1300, W - 110, 1560, r=40, fill=palette["card"])
        cf = f(44)
        yy = 1360
        for line in bc:
            center(d, line, cf, W / 2, yy, palette["ink"])
            yy += 80


def render_rows(d, p, palette):
    title_font = f(78)
    left(d, p.get("title", ""), title_font, 90, 230, palette["primary"])
    d.rectangle([92, 340, 92 + 140, 350], fill=palette["accent"])
    y = 430
    main_font = f(52)
    note_font = f(38)
    for main, note in p.get("rows", []):
        ch = 150 if note else 110
        card(d, 90, y, W - 90, y + ch, r=32, fill=palette["card"])
        d.rectangle([90, y, 108, y + ch], fill=palette["primary"])
        d.text((150, y + 34), main, font=main_font, fill=palette["ink"])
        if note:
            d.text((150, y + 92), note, font=note_font, fill=palette["muted"])
        y += ch + 26


def render_hospitals(d, p, palette):
    title_font = f(70)
    left(d, p.get("title", ""), title_font, 90, 220, palette["primary"])
    d.rectangle([92, 320, 92 + 140, 330], fill=palette["accent"])
    y = 400
    name_font = f(50)
    reason_font = f(38)
    for name, reason in p.get("hospitals", []):
        ch = 200
        card(d, 90, y, W - 90, y + ch, r=32, fill=palette["card"])
        badge_x(d, 175, y + ch / 2, 52, palette["accent"])
        d.text((270, y + 46), name, font=name_font, fill=palette["ink"])
        d.text((270, y + 116), reason, font=reason_font, fill=palette["accent"])
        y += ch + 30
    s_title, s_body = p.get("summary", ("", ""))
    if s_title:
        card(d, 90, y + 10, W - 90, y + 180, r=32, fill=palette["primary"])
        sf = f(46)
        center(d, s_title, sf, W / 2, y + 40, palette["muted"])
        sf2 = f(50)
        center(d, s_body, sf2, W / 2, y + 100, palette["card"])


def render_asks(d, p, palette):
    title_font = f(66)
    left(d, p.get("title", ""), title_font, 90, 220, palette["primary"])
    d.rectangle([92, 320, 92 + 140, 330], fill=palette["accent"])
    y = 400
    main_font = f(52)
    note_font = f(40)
    for i, (main, note) in enumerate(p.get("asks", []), 1):
        ch = 175
        card(d, 90, y, W - 90, y + ch, r=32, fill=palette["card"])
        badge_num(d, 180, y + ch / 2, 56, i, palette["primary"])
        d.text((285, y + 42), main, font=main_font, fill=palette["ink"])
        d.text((285, y + 108), note, font=note_font, fill=palette["muted"])
        y += ch + 28
    cta = p.get("cta_lines") or []
    if cta:
        card(d, 90, y + 16, W - 90, y + 300, r=40, fill=palette["primary"])
        badge_chat(d, W / 2, y + 95, 46, palette["card"])
        cf = f(50)
        cy = y + 150
        for line in cta:
            center(d, line, cf, W / 2, cy, palette["card"])
            cy += 65
    if p.get("footer"):
        cf = f(38)
        center(d, p["footer"], cf, W / 2, y + 340, palette["muted"])


RENDERERS = {
    "cover": render_cover,
    "rows": render_rows,
    "hospitals": render_hospitals,
    "asks": render_asks,
}


# ---------- 主入口 ----------
def render(content=None, out_dir=None, total_pages=None):
    content = content or CAROUSEL_CONTENT
    palette = PALETTES[content["palette"]]
    pages = content["pages"]
    total = total_pages or len(pages)
    out_dir = out_dir or DEFAULT_OUT.format(date=os.popen("date +%Y-%m-%d").read().strip())
    os.makedirs(out_dir, exist_ok=True)

    outputs = []
    for idx, page in enumerate(pages, 1):
        img, d = make_base(
            palette,
            content.get("brand", "CHINA HOSPITALS GUIDE"),
            content.get("tag", "海外医疗求助"),
            idx, total,
        )
        kind = page.get("kind", "cover")
        RENDERERS[kind](d, page, palette)
        path = os.path.join(out_dir, f"page{idx}.png")
        img.save(path)
        outputs.append(path)

    # self-check: scan for emoji codepoints that would tofu
    bad = [c for c in open(__file__, encoding="utf-8").read()
           if (0x1F000 <= ord(c) <= 0x1FAFF) or (0x2600 <= ord(c) <= 0x27BF)]
    assert not bad, f"tofu-risk emoji in script: {set(bad)}"

    # report
    print("DONE")
    for p in outputs:
        im = Image.open(p)
        print(p, im.size, im.mode, os.path.getsize(p), "bytes")
    print("OUT_DIR:", out_dir)
    return outputs


if __name__ == "__main__":
    render()