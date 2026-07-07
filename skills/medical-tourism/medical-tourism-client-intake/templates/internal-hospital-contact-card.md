# Internal Hospital Contact Card — Reusable Template

> 2026-07-07 由 Maria Rios 案确立。每次有新患者对接新医院时，先填这张卡再发邮件。
> 标准存放位置：`/home/ubuntu/chinahospitalsguide/internal-contact-cards/<hospital-id>.md`

---

## 📋 模板

```
# [医院英文名] 联系卡 — [患者姓名] 用 (内部参考)
# Last verified: YYYY-MM-DD · 信息源: chinahospitalsguide hospital-directory-51.csv + api/v1/hospitals.json + 内部新闻条目

---

## 🏥 1. [医院英文名] ([中文名])

> **首推 / 备选** — 一句话说明为什么选这家

- **英文名**: ...
- **中文名**: ...
- **地址**: ...
- **总机**: ...
- **国际部电话**: ...
- **国际部邮箱**: ...
- **官网**: ...
- **机场距离**: ... → ... 约 X 分钟
- **英文接诊能力**: ...
- **预约提前期**: ...
- **JCI**: ...
- **临床重点 (跟患者病情相关)**:
  - ...
  - ...
  - 参考价: ...
- **国际患者入院流程**: ...
- **典型住院时长**: ...
- **关键联系人**: ...

---

## 🏥 2. [备选医院英文名] ([中文名])

> **备选/兜底** — 同上结构

---

## 📋 行动建议 (本单)

1. **首选发邮件给 [首选医院] 国际部**: [邮箱]
   - 主题建议: `International Inquiry – [Disease], Remote Review Request`
   - 附件: ...
   - 正文可以贴: ...
   - 抄送 [患者本人] 邮箱让她知道进展
2. **[备选医院] 先不主动联系** — 留给 [首选] 回信说"我们排不下"时再启动
3. **同时让 [患者] 把云盘链接/密码再发一次** (云盘有时效), 24h 内能下到 DICOM
4. **谁先回就用谁**

---

## ⚠️ 数据可信度提示

- [首选医院] 的邮箱/电话: [数据源 + 核实日期]
- [备选医院] 的邮箱/电话: [数据源 + 核实日期]
- 国际部"具体对接人姓名": 目录里 [有/没有] — 打过去转接时再问
```

---

## 填表数据源（按优先级）

1. `/home/ubuntu/chinahospitalsguide/api/v1/hospitals.json` — 51+ 医院主库（信任评分、国际合作部详情）
2. `/home/ubuntu/chinahospitalsguide/hospital-directory-51.csv` — 简版 CSV
3. `/home/ubuntu/chinahospitalsguide/news/<hospital>-<topic>.html` — 内部新闻条目（往往含科室细节）
4. `/home/ubuntu/chinahospitalsguide/blog/hospitals-in-<city>-for-international-patients.html` — 城市医院指南
5. `/home/ubuntu/chinahospitalsguide/treatments/<disease>.html` — 治疗页（往往列了对应医院排名）

---

## 真实案例

### Maria Rios 案（2026-07-07）

存放在：`/home/ubuntu/chinahospitalsguide/internal-contact-cards-xi-an.md`

- **首选**：Tangdu Hospital（西安）—— Nutcracker 3D 打印 PEEK 血管外支架项目首发 28+ 案例医院
- **备选**：Xijing Hospital（西安）—— 同属第四军医大学附属，综合实力强
- **关键发现**：JSON 里 Tangdu 有详细 `international_dept` 块（phone/email/services），Xijing 没有——遇到这种情况备注"⚠️ 目录里没列，要打总机问"