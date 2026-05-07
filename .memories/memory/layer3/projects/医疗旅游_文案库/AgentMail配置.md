# AgentMail 邮箱配置记录

> 记录日期：2026-03-12
> 最后更新：2026-03-13 00:08

---

## 📧 邮箱基本信息

| 项目 | 内容 |
|------|------|
| **邮箱地址** | motionlessbottle950@agentmail.to |
| **显示名称** | Demi |
| **API Key** | am_us_1e6de2cdfc317699736a58a1ca8ef07e64edcc841457f119d89b1989239d0d94 |
| **API Base URL** | https://api.agentmail.to/v0 |

---

## 🔧 API 端点

### 发送邮件
```
POST /v0/inboxes/{inbox_id}/messages/send
Headers:
  Authorization: Bearer {API_KEY}
  Content-Type: application/json

Body:
{
  "to": "recipient@example.com",
  "subject": "Email Subject",
  "text": "Email body content"
}
```

### 更新显示名称
```
PATCH /v0/inboxes/{inbox_id}
Headers:
  Authorization: Bearer {API_KEY}
  Content-Type: application/json

Body:
{
  "display_name": "Demi"
}
```

### 获取邮件列表
```
GET /v0/inboxes/{inbox_id}/messages
Headers:
  Authorization: Bearer {API_KEY}
```

---

## 📁 相关文件

| 文件 | 用途 |
|------|------|
| `auto_reply_bot.py` | 自动回复脚本 |
| `auto_reply_template.txt` | 第1封邮件模板（咨询表单） |
| `recommendation_email_template.txt` | 第2封邮件模板（智能推荐） |
| `smart_recommendation.py` | 医院匹配逻辑 |

---

## ⚙️ 自动回复配置

### 排除列表（已手动联系的客户）
```python
EXCLUDED_EMAILS = {
    "williamkemp08@hotmail.com",
    "robin62005@hotmail.com",
    "manisha@appsdeveloper.in",
    "cinvea7@gmail.com",
    "muskan66singh@outlook.com",
    "shivanisco1@outlook.com"
}
```

### 功能特性
- ✅ 每个邮箱只回复一次
- ✅ 跳过排除列表中的客户
- ✅ 跳过自己发送的邮件
- ✅ 跳过系统邮件（noreply/notify）

---

## 💰 定价体系

### 产品1: Starter Guide ($30)
- 医院详细对比
- 医生资质介绍
- 治疗时间线
- 费用明细
- 签证要求
- 患者见证

### 产品2: Standard Package ($299)
包含 Starter Guide 所有内容，外加：
- 医院预约安排
- 病历翻译
- 术前视频咨询
- 机场接送协调
- 24/7 WhatsApp 客服
- 术后跟进

### 产品3: Premium Upgrades（自选）
| 服务 | 价格 | 说明 |
|------|------|------|
| On-ground support | $150/day | 现场陪同、翻译、后勤 |
| Medical translator | $100/day | 专职医疗翻译 |
| Airport pickup | $80/trip | 机场接送服务 |
| Accommodation booking | $50 | 家属住宿预订 |
| Post-treatment recovery | $200/week | 术后回访、与医院沟通、持续支持 |

**注意：** 现场服务（support, translator, transfers）可来到中国后再预订支付

---

## 📝 邮件模板要点

### 第1封邮件（咨询表单）
- 德米自我介绍（粤语背景）
- 5个问题收集需求
- 温暖鼓励的语气
- 24小时内人工回复承诺

### 第2封邮件（智能推荐）
- 根据专科+城市匹配医院
- 医院排名、专长、费用、等待时间
- 推销 $30 和 $299 套餐
- 自选升级服务
- 明确我们是推荐服务，医院费用直接付给医院

---

## ⚠️ 重要原则

1. **不做价格承诺** - 只提供参考价格
2. **不承诺医院服务** - 我们是推荐方，不是医院
3. **不做国家对比** - 避免敏感词（如"比美国便宜"）
4. **现场服务灵活** - 可来到中国后再支付
5. **术后回访详细** - 强调回国后与医院沟通支持

---

## 🔗 联系方式

- **邮箱**: motionlessbottle950@agentmail.to
- **WhatsApp**: +44 7947 060056
- **网站**: https://chinahospitalsguide.com

---

*保存位置: /root/.openclaw/workspace/memory/医疗旅游_文案库/AgentMail配置.md*
