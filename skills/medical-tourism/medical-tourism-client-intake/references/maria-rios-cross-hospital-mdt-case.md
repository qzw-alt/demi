# Maria Rios 案 — 单家医院 + 跨院专家 MDT 协调模板

> **建立日期**：2026-07-11
> **触发案例**：Maria Rios / Nutcracker + May-Thurner + SMAS 疑似 / 哥伦比亚籍、荷兰居住 / case-sharing 模式
> **核心洞察**：复杂并发病情的协调解法 = 单家窗口医院 + 跨院专家 MDT 远程协诊网络

---

## 患者档案（标准化结构）

```yaml
name: Maria Rios
nationality: Colombian citizen
residence: the Netherlands
contact:
  email: iosale625@gmail.com
  whatsapp: +31 615580429
disease_stack:
  - primary: Nutcracker Syndrome (left renal vein compression)
  - secondary: May-Thurner Syndrome (left common iliac vein compression)
  - suspected: Superior Mesenteric Artery Syndrome (SMAS)
history:
  duration: 4.5 years
  weight_loss: "60 kg → 43.5 kg at 1.56 m"
  life_impact: "renounced work and studies"
imaging_source: "Spain (Spanish + English reports)"
case_sharing: agreed
coordinator_mode: 0¥ Pre-Arrival Coordination (free, airport pickup not included)
```

---

## 跨院 MDT 协调邮件模板（英文，给患者）

完整模板见 `draft-final-round-maria-shanghai-mdt.md`（在 chinahospitalsguide 仓库根目录）。**邮件结构**：

### Part 1 / 2

1. **进展好消息开场**（1 段） —— "I want to share a piece of good news with you before anything else gets in the way of it."
2. **病情复杂性交代**（1 段） —— "Your case is rare and unusually layered: three different vascular / visceral conditions..."
3. **解法**：单家窗口医院 + 跨院 MDT（2 段）—— "instead of chasing individual hospitals... a single hospital that has the peer network to bring together the right specialists"
4. **具体医院介绍**（1-2 段） —— 上海第九人民医院，部门实力 + 同行资源
5. **诚实交代进度**（1 段，**关键**） —— 4 条 list：
   - 医院已收到临床资料 + 已初步了解
   - 医院同意接诊 + 准备跨专科讨论
   - 邀请外院专家进 MDT —— "Whether each invited specialist accepts is not something any hospital can promise in advance"
   - 不打包票，但承诺会一直推进

### Part 2 / 2

6. **3 个病情分别处理**（3 段）：
   - 谁负责科室
   - 大方向（技术名词 — 模糊即可）
   - "details to be explained to you directly by the operating surgeon during the upcoming video discussion"
7. **下一步**（1 段）：
   - 医生会主动线上联系
   - 影像是否已转过去 + 是否还有新的需要补
   - 保持 CC
8. **案例合作**（1 段） —— "no deadline, no script, no pressure"
9. **小请求**（1 段） —— 1-2 个具体小问题（最新影像 / 是否可达 WeChat）

---

## 措辞模板库

### "不替医生下结论"的核心句

```
The direction currently under consideration is a [minimally-invasive] [approach]
using [technique], with details to be explained to you directly by the operating
surgeon during the upcoming video discussion.

I am intentionally not specifying step-by-step what the surgical technique will
be in writing, because the right technique depends on findings your imaging will
show the team, and the surgeon should explain it to you face-to-face rather than
through me.
```

### "外院专家邀请是否答应不打包票"的诚实句

```
They will be inviting certain outside specialists into the MDT based on your
imaging. Whether each invited specialist accepts is not something any hospital
can promise in advance — that is a normal part of how these consultations work
in China, and it is one of the reasons we wanted the hospital with the right
peer connections rather than the closest one.
```

### "单家窗口医院 + 跨院同行网络"的 positive 措辞

```
the hospital has direct working relationships with the specific specialist
groups elsewhere in China who focus on each of your three conditions. That is
the part that matters most for your case.
```

**避免用**："军队医院对外籍有限制" —— 这暴露体制内部细节，**不告诉患者**

### "案例合作"标准尾段

```
In case it slipped your mind in the busyness of the last few weeks: there is no
deadline, no script, no pressure. If and when something strikes you, a note, a
photo, a short video — anything at all — we will send it back to you for
approval before anything goes anywhere.

The reason I mention it at all is that what you are living through right now
(three-condition complex case, 4.5 years of searching) is exactly what other
patients in the same situation 2am will be searching for.
```

---

## 业务定位 (chinahospitalsguide 对外卖点)

| 普通中介能给的 | 我们能给的（差异化） |
|---|---|
| 单家医院的国际部挂号 | **跨院专家 MDT 协调** |
| 单一病种治疗安排 | **多病并发的协调治疗** |
| 翻译 + 行程 | **复杂病情会诊设计** |

**这条未来要写进 pricing.html / 服务介绍 / SEO 文章。**

---

## 关键决策点（写邮件前要拍板）

1. **拆段是默认行为** —— 不要问用户"拆不拆"（2026-07-11 强化偏好）
2. **替医生下结论是禁忌** —— 写模糊措辞
3. **邀请外院专家不打包票** —— 诚实交代
4. **不发九院联系邮件** —— 伟烨 2026-07-11 明示"暂时不需要给他们发邮件"，**九院医生主动联系 Maria**
5. **案例合作段保留** —— 按之前邮件风格 "no deadline, no pressure"

---

## 失败案例（防再踩）

- ❌ **Maria Rios 早期 draft** 写成了 "We have already prepared a formal inquiry to Tangdu Hospital" —— 这是唐都时代草稿，现在医院是上海九院 + MDT 模式，必须改
- ❌ **Maria Rios 早期 draft** 假设"医生还没看资料" —— 实际伟烨已经帮她发了医院也初步评估过了，邮件要更新这条事实
- ❌ **每次都问"达芬奇用于哪条"** —— 2026-07-11 实际发生：伟烨说"我不懂，你模糊提出具体由医生解析"，结果浪费一次问答。**对策**：直接写模糊措辞，把"细节由医生解析"作为默认叙事，不让用户被反问

---

## 关联文档

- `templates/hospital-inquiry-email-en.md` —— 给医院国际部的英文问询邮件模板（**本案例不直接用**，因为伟烨明示不发九院邮件）
- `references/case-sharing-mode.md` —— case-sharing 业务规则
- `references/china-unique-medical-selling-points.md` —— Nutcracker 3D PEEK 支架 / 唐都首创的卖点
- SKILL.md `## 中国顶级三甲对国际患者的统一接诊规则` —— 主诊医院限制规则
- SKILL.md `## 军队背景三甲对外籍接诊的限制` —— 军队医院 + 协诊角色
