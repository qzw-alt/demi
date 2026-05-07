---
name: oriental-destiny
description: Oriental Destiny — BaZi/Feng Shui calculation engine and website (qzw-alt/oriental-destiny)
category: productivity
---

# Oriental Destiny

## 仓库
- **GitHub**: https://github.com/qzw-alt/oriental-destiny
- **本地路径**: `/root/.hermes/workspace/oriental-destiny/`
- **分支**: `main`

## 产品定位
- 面向英语用户的风水/八字测算网站
- 商业模式：免费 instant reading → 付费 full reading ($99)
- 产品：Feng Shui 手串/吊坠，通过八字解读推荐五行属性水晶

## 核心文件

### 引擎
- `bazi_engine.js` — 八字排盘引擎（1215行，纯客户端JS确定性计算）
  - 四柱排盘（年/月/日/时柱）
  - 十神、藏干、五行强度评分
  - 十二长生、生克冲合会
  - **无**：大运分析、流年动态推理
- `report_focus.js` — 报告文案模板（5个focus：career/wealth/love/protection/balance）
- `reading_state.js` — localStorage 状态管理

### 页面
- `instant_reading.html` — 免费即时解读入口
- `full_bazi_reading.html` — 付费完整解读
- `report_demo.html` — 报告预览/水晶推荐
- `kua_calculator.html` — 八卦计算器
- `checkout.html` — PayPal 付款页
- `policies.html` — 退改/隐私政策
- `products.html` — 产品介绍

### AI 升级层（新建中）
- `api_deepseek.js` — DeepSeek API 封装
- `ai_bazi_layer.js` — AI 推理 + 生成层
- `prompts/` — 提示词模板
- `docs/TECH_SPEC.md` — 完整技术规格

## AI 升级架构

```
bazi_engine.js (现有) → ai_bazi_layer.js → DeepSeek V4 API
  确定性排盘计算           AI推理+生成         自有API Key
```

### 架构原则
1. **计算层不用 LLM**：八字排盘是确定性数学，bazi_engine.js 保留
2. **DeepSeek 用于**：复杂五行链式推理 + 英文个性化文案生成
3. **API 费用**：自己承担，客户端直接调用 DeepSeek API
4. **回退机制**：API 失败时静默回退静态模板文案

### 模型选型
- **计算层推理**：`deepseek-chat`，temperature=0.3（低温度保持一致性）
- **解读层生成**：`deepseek-chat`，temperature=0.8（高温度创意生成）

## 品牌调性
- 英文面向全球用户
- 语气：专业但不冷漠，像有智慧的老师在解释
- 文案风格：Narrative，non-templated，避免 "According to your chart..."
- 颜色：--ink (#241915), --paper (#f8f1e7), --cinnabar (#a63a2c), --gold (#b78a42), --pine (#315247)

## SEO / 内容
- sitemap.xml — 13个页面
- 目标：英语用户在 Google 搜索相关关键词

## 进行中项目
- [ ] DeepSeek API 接入 Phase 1（基础设施完成）
- [ ] DeepSeek API 接入 Phase 2（计算层 + 解读层实现）
- [ ] instant_reading.html 接入 AI 解读
- [ ] checkout 信任信号增强
