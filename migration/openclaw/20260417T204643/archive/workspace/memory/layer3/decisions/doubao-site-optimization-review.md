# 豆包网站优化建议 — 审核结果

> 来源：豆包（用户用豆包分析网站后分享）
> 日期：2026-04-08
> 状态：已审核，待实施

---

## 数据现状

**医院数量**：34家
**当前字段**：name / city / district / phone / rank / airport / tags / image
**缺失字段**：Specialties（专科）、International Service（国际服务）、JCI认证、Official Tel、Official Name

---

## 建议采纳情况

| # | 建议内容 | 采纳 | 状态 |
|---|---------|------|------|
| 1 | Homepage Slogan | ✅ | 待实施 |
| 2 | By Specialty 导航 | ✅ | 待实施（需要建页面） |
| 3 | 医院新增 Specialties + International Service 字段 | ✅ | **需核对后实施** |
| 4 | Contact 页面文案 | ✅ | 待实施 |
| 5 | Footer 文案 | ✅ | 待实施 |
| 6 | 每家医院15词英文描述 | ⭐ 高优先 | 待实施 |
| 7 | By Specialty 页面完整内容 | ⭐ 高优先 | 待实施 |
| 8 | SEO 关键词列表 | 中优先 | 可选 |

---

## 实施优先级排序

### P0（必须做，价值清晰）
1. **Homepage Slogan** → 加到 index.html 标题下方
2. **Contact 页面文案** → 替换现有内容
3. **Footer 一句话** → 替换现有

### P1（高价值，需时间）
4. **医院 Specialties + International Service**
   - 豆包给的 Specialties 需要逐条核对（无法100%确认真实性）
   - 建议：从 tag 反推 Specialties，优先处理已有数据的医院
   
5. **By Specialty 页面**
   - 对应8个分类：Heart / Cancer / Orthopedics / Neuro / Fertility / Eye / Women & Children / Checkup
   - 每个分类建一个页面，聚合相关医院

### P2（锦上添花）
6. 每家医院15词描述 → 配合 Specialties 字段一起做

---

## 待伟烨确认事项

1. **Contact 页面**：现在放的是哪个页面？（contact.html 还是 contact-new.html）
2. **WhatsApp/Telegram 号码**：Contact 页面留哪个联系方式？
3. **豆包的 Specialties**：要我去网上核查一遍，还是先用 tag 反推？

---

## 文件位置

- 医院数据：`website/hospitals.html`（JavaScript 内嵌）
- 首页： `website/index.html`
- Contact： `website/contact.html`
- Footer： 各页面底部
