# 医疗旅游业务自动化工作流设计

## 工作流1：潜在客户自动跟进系统

### 触发器
网站表单提交（咨询医院/价格/服务）

### 工作流程
```
[表单提交]
    ↓
[Zapier/Make 捕获数据]
    ↓
├─→ [Airtable/Notion] 添加为"新潜在客户"
├─→ [Gmail] 发送自动回复邮件（感谢+医院指南PDF）
├─→ [Slack] 通知团队："新咨询：[姓名] - [病情简述]"
└─→ [Notion] 创建跟进任务（3天内联系）
```

### 邮件模板（自动发送）
```
Subject: Your China Medical Tourism Guide is Here

Hi [Name],

Thanks for reaching out about medical treatment in China.

I've attached our free hospital guide with:
- Top-ranked hospitals by specialty
- Real 2026 pricing data
- Patient stories and outcomes

I'll personally review your case and get back to you within 24 hours.

Best,
[Your name]
```

### 工具配置
| 工具 | 用途 | 月费 |
|------|------|------|
| Zapier (Starter) | 工作流引擎 | $20 |
| Airtable | CRM/数据库 | 免费版 |
| Gmail | 自动邮件 | 免费 |
| Slack | 团队通知 | 免费 |

---

## 工作流2：博客内容自动分发

### 触发器
新博客文章发布到网站

### 工作流程
```
[新博客发布]
    ↓
[RSS feed 触发]
    ↓
├─→ [Buffer/Hootsuite] 排队到 LinkedIn/Twitter
├─→ [Mailchimp] 添加到下周邮件简报
├─→ [Notion] 更新内容日历状态为"已分发"
└─→ [Slack] 通知："新文章已自动分发"
```

### 社交媒体文案模板
```
LinkedIn:
New guide: [文章标题]

[2-3句核心观点]

[链接]

#MedicalTourism #ChinaHealthcare #Savings

Twitter:
[文章标题] 🏥💰

关键数据：
• [数据点1]
• [数据点2]

[链接]
```

---

## 工作流3：支付到账自动处理

### 触发器
Stripe/PayPal 收到付款

### 工作流程
```
[Stripe webhook: payment succeeded]
    ↓
├─→ [Airtable] 更新订单状态为"已付款"
├─→ [Gmail] 发送收据邮件（含服务详情）
├─→ [Notion] 创建服务任务（分配给协调员）
├─→ [Google Sheets] 记录收入到财务表
├─→ [Slack] 通知："新订单 $[金额] - [服务类型]"
└─→ [Calendly] 发送预约链接（如含咨询）
```

### 收据邮件模板
```
Subject: Payment Received - Order #[订单号]

Hi [Name],

Thank you for your payment of $[金额].

Order Details:
- Service: [Starter/Standard/Premium]
- Amount: $[金额]
- Date: [日期]

Next Steps:
[根据套餐类型显示不同步骤]

Receipt attached.

Questions? Reply to this email.

Best,
China Hospitals Guide Team
```

---

## 工作流4：患者故事自动收集

### 触发器
治疗完成（手动标记或定期扫描）

### 工作流程
```
[治疗完成标记]
    ↓
[延迟7天]
    ↓
├─→ [Gmail] 发送满意度调查邮件
├─→ [Airtable] 记录发送时间
└─→ [Notion] 创建"待收集故事"任务
```

### 调查邮件模板
```
Subject: How was your experience? (2 min survey)

Hi [Name],

Hope you're recovering well.

Quick favor: Would you share your experience? It helps other patients make informed decisions.

[Typeform/Google Form 链接]

As thanks, we'll send you a $50 Amazon gift card.

Best,
[Your name]
```

---

## 实施优先级

| 优先级 | 工作流 | 预计节省时间 | 难度 |
|--------|--------|-------------|------|
| P0 | 潜在客户跟进 | 5小时/周 | 低 |
| P1 | 支付到账处理 | 2小时/周 | 低 |
| P2 | 博客内容分发 | 3小时/周 | 中 |
| P3 | 患者故事收集 | 1小时/周 | 低 |

## 工具总成本
- Zapier Starter: $20/月
- 其他工具免费版: $0
- **总计: $20/月**

## ROI计算
- 每周节省: 11小时
- 每月价值（按$50/小时）: $2,200
- 投入: $20/月
- **投资回报率: 11,000%**

---

## 下一步行动
1. [ ] 注册 Zapier 账号
2. [ ] 连接 Gmail/Airtable/Slack
3. [ ] 创建第一个工作流（潜在客户跟进）
4. [ ] 测试并上线
5. [ ] 逐步添加其他工作流
