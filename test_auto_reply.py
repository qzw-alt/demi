#!/usr/bin/env python3
"""
测试自动回复功能
"""
import requests

API_KEY = 'am_us_1e6de2cdfc317699736a58a1ca8ef07e64edcc841457f119d89b1989239d0d94'
BASE_URL = 'https://api.agentmail.to/v0'
INBOX_ID = 'motionlessbottle950@agentmail.to'

headers = {
    'Authorization': f'Bearer {API_KEY}',
    'Content-Type': 'application/json'
}

# 检查邮件
print("📧 Checking inbox...")
response = requests.get(
    f'{BASE_URL}/inboxes/{INBOX_ID}/messages',
    headers=headers
)

print(f"Status: {response.status_code}")

if response.status_code == 200:
    data = response.json()
    print(f"Response type: {type(data)}")
    
    # 处理不同的返回格式
    if isinstance(data, list):
        messages = data
    elif isinstance(data, dict):
        messages = data.get('messages', [])
    else:
        messages = []
    
    print(f"Total messages: {len(messages)}")
    
    for msg in messages:
        msg_from = msg.get('from', 'unknown')
        subject = msg.get('subject', 'No subject')
        direction = msg.get('direction', 'unknown')
        
        print(f"\n📨 From: {msg_from}")
        print(f"   Subject: {subject}")
        print(f"   Direction: {direction}")
        
        # 如果是收到的邮件且不是自动回复，就回复
        if direction == 'received' and msg_from != INBOX_ID:
            print(f"   ✅ Should reply to this message!")
        else:
            print(f"   ⏭️ Skip (sent by us or already processed)")
else:
    print(f"❌ Error: {response.text}")
