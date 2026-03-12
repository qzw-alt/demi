#!/usr/bin/env python3
"""
自动回复脚本 - 轮询检查新邮件并自动回复
"""
import requests
import json
import time
from datetime import datetime, timedelta

# API配置
API_KEY = 'am_us_1e6de2cdfc317699736a58a1ca8ef07e64edcc841457f119d89b1989239d0d94'
BASE_URL = 'https://api.agentmail.to/v0'
INBOX_ID = 'motionlessbottle950@agentmail.to'

# 自动回复模板
AUTO_REPLY_SUBJECT = "Re: Your Medical Tourism Inquiry - We've Received Your Message! / 您的医疗旅游咨询已收到！"

AUTO_REPLY_BODY = """Hi there / 您好，

Thanks for reaching out to China Hospitals Guide! 🏥
感谢您联系中国医院指南！

I'm Demi (德米), your AI assistant. I've received your email and wanted to let you know we're on it!
我是德米，您的AI助手。我已收到您的邮件，正在为您处理！

To help us find the best hospitals and doctors for you, could you reply with a few details?
为帮您找到最适合的医院和医生，能否回复以下几个问题？

📋 **Quick Questions / 快速问题：**

1. **What treatment or medical condition? / 需要什么治疗或病情？**
   (e.g., cardiac surgery, cancer treatment, orthopedic surgery, etc.)
   （如：心脏手术、癌症治疗、骨科手术等）

2. **Which city do you prefer? / 您偏好哪个城市？**
   - Beijing 北京 (capital hospitals 首都医院)
   - Shanghai 上海 (international hub 国际枢纽)
   - Guangzhou 广州 (southern medical center 南方医疗中心)
   - Shenzhen 深圳 (modern facilities 现代化设施)
   - No preference 无偏好

3. **When are you planning to visit? / 您计划何时前来？**
   - Within 1 month 1个月内
   - 1-3 months 1-3个月
   - 3-6 months 3-6个月
   - Just exploring options 仅了解选项

4. **Your country/region? / 您的国家/地区？**
   (helps us match you with culturally familiar services)
   （帮助我们为您匹配文化熟悉的服务）

5. **Any special requirements? / 有特殊要求吗？**
   (e.g., English-speaking doctors, specific hospital, family accommodation, etc.)
   （如：英语医生、指定医院、家属住宿等）

---

⏰ **What happens next? / 接下来会发生什么？**

Our team will review your needs and send personalized hospital recommendations within **24 hours**.
我们的团队将在**24小时内**审核您的需求并发送个性化医院推荐。

For urgent inquiries, feel free to WhatsApp us: **+44 7947 060056**
如有紧急咨询，欢迎通过WhatsApp联系我们：**+44 7947 060056**

Looking forward to helping you on your medical journey! 💙
期待在您的医疗之旅中为您提供帮助！

Warm regards / 此致问候，
**Demi (德米)**
China Hospitals Guide Team / 中国医院指南团队
📧 motionlessbottle950@agentmail.to
💬 WhatsApp: +44 7947 060056
🌐 https://chinahospitalsguide.com

---
*This is an automated response. A human team member will follow up with you personally within 24 hours.*
*这是自动回复。人工团队成员将在24小时内亲自跟进。*
"""

headers = {
    'Authorization': f'Bearer {API_KEY}',
    'Content-Type': 'application/json'
}

# 已回复的邮件ID集合（避免重复回复）
replied_messages = set()
# 已回复的邮箱集合（每个邮箱只回复一次）
replied_emails = set()

# 已手动联系过的客户（不要自动回复）
EXCLUDED_EMAILS = {
    "williamkemp08@hotmail.com",
    "robin62005@hotmail.com",
    "manisha@appsdeveloper.in",
    "cinvea7@gmail.com",
    "muskan66singh@outlook.com",
    "shivanisco1@outlook.com"
}

def get_recent_messages():
    """获取邮件"""
    try:
        response = requests.get(
            f'{BASE_URL}/inboxes/{INBOX_ID}/messages',
            headers=headers
        )
        if response.status_code == 200:
            data = response.json()
            # 处理不同的返回格式
            if isinstance(data, list):
                return data
            elif isinstance(data, dict):
                return data.get('messages', [])
            else:
                return []
        else:
            print(f"❌ Failed to get messages: {response.status_code}")
            return []
    except Exception as e:
        print(f"❌ Error getting messages: {e}")
        return []

def send_reply(to_email, subject, in_reply_to=None):
    """发送自动回复"""
    payload = {
        "to": to_email,
        "subject": subject,
        "text": AUTO_REPLY_BODY
    }
    
    if in_reply_to:
        payload["in_reply_to"] = in_reply_to
    
    try:
        response = requests.post(
            f'{BASE_URL}/inboxes/{INBOX_ID}/messages/send',
            headers=headers,
            json=payload
        )
        if response.status_code == 200:
            print(f"✅ Auto-reply sent to {to_email}")
            return True
        else:
            print(f"❌ Failed to send reply: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error sending reply: {e}")
        return False

def process_messages():
    """处理新邮件"""
    messages = get_recent_messages()
    
    for msg in messages:
        message_id = msg.get('message_id')
        
        # 跳过已回复的邮件
        if message_id in replied_messages:
            continue
        
        # 获取发件人
        from_email = msg.get('from', '')
        subject = msg.get('subject', '')
        
        # 跳过自己发送的邮件（AgentMail 发出的）
        if 'motionlessbottle950@agentmail.to' in from_email or 'AgentMail' in from_email:
            continue
        
        # 跳过系统邮件
        if 'noreply' in from_email or 'notify' in from_email:
            continue
        
        # 检查是否在排除列表（已手动联系的客户）
        from_email_lower = from_email.lower()
        if any(excluded.lower() in from_email_lower for excluded in EXCLUDED_EMAILS):
            print(f"⏭️ Skip {from_email} - manually contacted customer")
            replied_messages.add(message_id)
            continue
        
        # 检查这个邮箱是否已经回复过
        if from_email in replied_emails:
            print(f"⏭️ Skip {from_email} - already replied once")
            replied_messages.add(message_id)  # 标记为已处理
            continue
        
        print(f"📧 New message from {from_email}: {subject[:50]}...")
        
        # 发送自动回复
        if send_reply(from_email, AUTO_REPLY_SUBJECT, message_id):
            replied_messages.add(message_id)
            replied_emails.add(from_email)  # 记录已回复的邮箱
            print(f"✅ Added {from_email} to replied list (won't reply again)")

def main():
    print("🤖 Auto-reply bot started!")
    print(f"📧 Monitoring inbox: {INBOX_ID}")
    print("⏰ Checking every 2 minutes...")
    print("Press Ctrl+C to stop\n")
    
    while True:
        try:
            process_messages()
            time.sleep(120)  # 每2分钟检查一次
        except KeyboardInterrupt:
            print("\n👋 Stopping auto-reply bot...")
            break
        except Exception as e:
            print(f"❌ Error in main loop: {e}")
            time.sleep(120)

if __name__ == "__main__":
    main()
