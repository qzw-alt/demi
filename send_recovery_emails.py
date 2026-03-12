#!/usr/bin/env python3
"""
发送挽回邮件给6个潜在客户 - 使用正确的 AgentMail API v0
"""
import requests
import json

# API配置
API_KEY = 'am_us_1e6de2cdfc317699736a58a1ca8ef07e64edcc841457f119d89b1989239d0d94'
BASE_URL = 'https://api.agentmail.to/v0'
INBOX_ID = 'motionlessbottle950@agentmail.to'

headers = {
    'Authorization': f'Bearer {API_KEY}',
    'Content-Type': 'application/json'
}

# 客户列表
clients = [
    {"email": "Williamkemp08@hotmail.com", "name": "William"},
    {"email": "Robin62005@hotmail.com", "name": "Robin"},
    {"email": "manisha@appsdeveloper.in", "name": "Manisha"},
    {"email": "cinvea7@gmail.com", "name": "Friend"},
    {"email": "Muskan66singh@outlook.com", "name": "Muskan"},
    {"email": "ShivaniSCO1@outlook.com", "name": "Shivani"}
]

# 邮件模板
subject = "Re: Your Medical Tourism Inquiry - Technical Issue Resolved"

for client in clients:
    body = f"""Dear {client['name']},

I sincerely apologize for the delayed response.

We experienced a technical issue with our email system over the past 24 hours, 
and unfortunately, your inquiry was not delivered to our team. We have now 
resolved this issue.

We truly value your interest in China Hospitals Guide, and we would love to 
help you with your medical tourism needs.

Please reply to this email or contact us directly at:
📧 motionlessbottle950@agentmail.to
💬 WhatsApp: +44 7947 060056

As an apology for this inconvenience, we would like to offer you:
🎁 10% discount on any of our service packages

We typically respond within 24 hours and look forward to assisting you.

Best regards,
Demi (德米)
China Hospitals Guide Team
"""
    
    payload = {
        "to": client['email'],
        "subject": subject,
        "text": body
    }
    
    try:
        response = requests.post(
            f'{BASE_URL}/inboxes/{INBOX_ID}/messages/send',
            headers=headers,
            json=payload
        )
        if response.status_code == 200:
            print(f"✅ Sent to {client['email']}")
        else:
            print(f"❌ Failed to send to {client['email']}: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Failed to send to {client['email']}: {e}")

print("\nDone!")
