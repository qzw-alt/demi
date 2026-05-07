# Kimi 2.5 API 调用指南

## 前置准备
1. Python 3.8+
2. Kimi 2.5 API Key（从 https://kimi.moonshot.cn/console/api-keys 获取）
3. 安装 OpenClaw 库

## 方式1：命令行快速配置
```bash
openclaw onboard
```
- 选择模型提供商：Moonshot AI
- 选择具体模型：Kimi Code (K2.5)
- 粘贴 API Key

## 方式2：Python代码调用
```python
from openai import OpenAI

client = OpenAI(
    api_key="你的Kimi API Key",
    base_url="https://api.moonshot.cn/v1"
)

response = client.chat.completions.create(
    model="moonshot-v1-8k",  # Kimi 2.5
    messages=[{"role": "user", "content": "你好"}]
)
print(response.choices[0].message.content)
```

## 关键说明
- 模型标识：moonshot-v1-8k（8k上下文）
- 计费：49元套餐，按Token消耗
- 注意：需要 Kimi Code API Key，不是网页版对话Key
