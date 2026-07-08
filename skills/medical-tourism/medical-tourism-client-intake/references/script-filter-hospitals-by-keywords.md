# Database-Driven Hospital Candidate Filtering — Reusable Recipe

> 2026-07-08 由 Maria Rios / 北大第一案确立。每次新患者进来需要"哪家医院能治 X"时，跑这个流程而不是凭记忆推荐。

## ⚠️ 必读陷阱

**`terminal(cat ...)` 会把 58KB 的 hospitals.json 截到 50KB，导致 JSON parse 在中段挂掉**——这个本会话踩过 4 次。**必须用 Python `open(..., 'rb')` 读取**。

## 一键复制的脚本

```python
import json

with open("/home/ubuntu/chinahospitalsguide/api/v1/hospitals.json", "rb") as f:
    data = json.loads(f.read().decode("utf-8-sig"))  # utf-8-sig 自动剥 BOM
hosp = data["hospitals"]

# === 改这里：根据病情扩 KEYWORDS ===
KEYWORDS = {
    "nutcracker": ["nutcracker", "renal vein", "left renal", "胡桃夹"],
    "may-thurner": ["may-thurner", "iliac vein", "iliac compression", "髂静脉"],
    "vascular": ["vascular", "blood vessel", "血管"],
    "interventional": ["interventional", "介入"],
    "urology": ["urology", "泌尿"],
    # 加更多病种...
}

scoreboard = []
for h in hosp:
    blob = json.dumps(h, ensure_ascii=False).lower()
    matched = [cat for cat, kws in KEYWORDS.items() if any(k.lower() in blob for k in kws)]
    if matched:
        scoreboard.append((len(set(matched)), h, matched))

scoreboard.sort(reverse=True, key=lambda x: x[0])

print(f"命中医院数: {len(scoreboard)} / {len(hosp)}\n")
for score, h, matched in scoreboard[:20]:
    print(f"\n{'=' * 70}")
    print(f"🏥 {h.get('name','')} ({h.get('name_zh','')})")
    print(f"   城市: {h.get('city','')} / 标签: {', '.join((h.get('tags') or [])[:5])}")
    print(f"   国际部: {h.get('international', False)}  电话: {h.get('phone','')}")
    print(f"   匹配类别: {', '.join(set(matched))} (命中 {score} 类)")
    # 打印 trust.notes 里的临床重点
    trust_notes = h.get("trust", {}).get("notes", [])
    if trust_notes:
        print(f"   trust notes:")
        for n in trust_notes[:4]:
            print(f"     - {n[:200]}")
```

## 输出判读

跑完看 `命中医院数: N / 51`。按下面判读：

| 命中数 | 含义 | 给伟烨的话术 |
|--------|------|--------------|
| 0 | 主库没有这家能治 X 的医院——**要扩库或搜外部资料** | "我们的 51 家库里没有匹配的医院，我去找找北京/上海还有哪家" |
| 1 | **主库里就 1 家能做**——可选项极少，直接跟这家谈 | "主库里只有 Tangdu 一家能做，做完 Mailchimp / 邮件询单" |
| 2-3 | 有几家候选，需要按城市 / 专长 / 国际部能力选 | "主库里有 X 家候选，我按 Y 维度排序给你看" |
| 5+ | 主库有几家可以做，但需要按 patient's profile 筛选 | "主库里有 N 家，按你的病情/时间/城市偏好我筛出 3 家" |

## 当前数据库的硬约束（2026-07-08 验证过）

跑完脚本记住这些事实，避免重复踩坑：

| 病种 | 数据库命中医院数 | 备注 |
|------|------------------|------|
| Nutcracker + May Thurner 同时 | **仅 1 家** — Tangdu (Xi'an) | `trust.notes` 里写明 |
| Beijing 内能做血管介入 | **0 家** | 主库里无匹配 |
| 只接外籍 + 强血管外科 | 几乎都是军事医院（唐都、301），**军事医院对外籍有政策限制** | Maria Rios 案已踩雷 |

**如果命中数 ≥ 5 但全是军事医院 / 部队医院**：需要特别提示伟烨"外籍身份可能有政策风险"。

## 关键词扩展指南

按患者主诉添加 `KEYWORDS` 字典：

| 患者主诉 | 推荐关键词 |
|----------|-----------|
| 慢性肾病 / 透析 / 肾移植 | "kidney", "renal", "nephrology", "dialysis", "transplant" |
| 心脏瓣膜 / 搭桥 | "cardiology", "cardiac", "valve", "cabg", "心" |
| 肝脏肿瘤 / 肝移植 | "liver", "hepatobiliary", "transplant", "肝" |
| 肺癌 / 胸外科 | "thoracic", "lung", "esophagus", "肺", "胸" |
| 脑动脉瘤 / 脑血管 | "neurosurgery", "cerebrovascular", "aneurysm", "脑" |
| 骨科 / 关节置换 | "orthopedic", "joint", "knee", "hip", "骨" |
| 试管婴儿 / 不孕 | "fertility", "ivf", "reproductive", "生殖" |

中英文混搭匹配 **大幅提高命中率**（trust.notes 字段里既有英文名也有中文描述）。

## 联系信息字段速查

跑出命中医院后，下面是取联系方式的字段路径：

| 字段 | JSON 路径 | 备注 |
|------|----------|------|
| 总机 | `h["phone"]` | 北京医院多为 `010-XXXXXXXX` |
| 国际部电话 | `h["international_dept"]["phone"]` | 不是每家都有 |
| 国际部邮箱 | `h["international_dept"]["email"]` | **很少**，多为军事医院 |
| 官网 | `h["website"]` | 大多有效 |
| 机场距离 | `h["airport_info"]` | 自然语言字符串 |
| 排名 | `h["rank"]` | 一句话（如 "#1 Cardiology"） |
| 标签 | `h["tags"]` | 列表，用于按专长过滤 |
| 国际部开关 | `h["international"]` | bool |

## 不在主库怎么办？

如果 KEYWORDS 命中 0：

1. **扩展关键词**（加同义词 / 中文）
2. **查 city 维度**——把"Beijing + vascular" 放宽成 "所有城市 + vascular"，看非北京有没有
3. **查外部资料**——用 `terminal-web-research` skill 或 web 搜索补全医院列表
4. **新增医院到库**——走 `hospital-directory` skill 的新增流程（更新 `api/v1/hospitals.json` + `hospitals.html`）

**不要瞎推荐**。库外的医院没经过 trust_score 验证，直接推荐伟烨风险高。