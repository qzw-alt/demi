# 🧠 memory-simple

**Simple JSON-based Memory System for OpenClaw**

一个简单、稳定、易用的 JSON 文件记忆系统，专为 OpenClaw AI Agent 设计。

[English](#english) | [中文](#中文)

---

## 中文

### ✨ 特性

- ✅ **超稳定** - JSON 文件存储，不会崩溃
- ✅ **简单易用** - 无需复杂配置，开箱即用
- ✅ **混合检索** - 向量相似度 + 关键词匹配
- ✅ **自动捕获** - 自动从对话中提取记忆
- ✅ **智能排序** - 相似度 + 新鲜度综合评分
- ✅ **零依赖** - 仅需 Node.js 内置模块

### 🚀 快速开始

```bash
# 1. 克隆仓库
git clone https://github.com/qzw-alt/memory-simple.git
cd memory-simple

# 2. 配置 API Key
vim config.json
# 填入你的智谱 AI API Key

# 3. 测试
node scripts/capture.js
node scripts/recall.js "测试查询"
```

### 📖 完整文档

- [使用指南](docs/memory-simple-usage/SKILL.md)
- [快速参考](docs/memory-simple-usage/QUICKREF.md)
- [示例代码](docs/memory-simple-usage/examples/)

### 🎯 核心 API

```javascript
// 捕获记忆
const { captureMemories } = require('./scripts/capture');
await captureMemories(conversation, 'session-id');

// 检索记忆
const { searchMemories } = require('./scripts/recall');
const results = await searchMemories('用户喜欢什么', { topK: 5 });
```

---

## English

### ✨ Features

- ✅ **Super Stable** - JSON file storage, no crashes
- ✅ **Easy to Use** - Works out of the box
- ✅ **Hybrid Retrieval** - Vector similarity + keyword matching
- ✅ **Auto Capture** - Extract memories from conversations
- ✅ **Smart Ranking** - Similarity + recency combined scoring
- ✅ **Zero Dependencies** - Only Node.js built-in modules

### 🚀 Quick Start

```bash
# 1. Clone
git clone https://github.com/qzw-alt/memory-simple.git
cd memory-simple

# 2. Configure API Key
vim config.json
# Add your Zhipu AI API Key

# 3. Test
node scripts/capture.js
node scripts/recall.js "test query"
```

### 📖 Documentation

- [Usage Guide](docs/memory-simple-usage/SKILL.md) (Chinese)
- [Quick Reference](docs/memory-simple-usage/QUICKREF.md) (Chinese)
- [Examples](docs/memory-simple-usage/examples/)

---

## 🆚 Comparison with LanceDB-Pro

| Feature | memory-simple | LanceDB-Pro |
|---------|---------------|-------------|
| Stability | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| Features | Core only | Advanced |
| Ease of Use | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| Performance | Good for small data | Better for large data |
| Dependencies | None | LanceDB, etc. |

**Choose memory-simple if:**
- You want stability over features
- Your data volume is moderate (< 10,000 memories)
- You prefer simple, maintainable code

---

## 🤝 Sharing

This project is designed to be easily shared between OpenClaw agents:

```bash
# Share with other agents
tar czvf memory-simple.tar.gz memory-simple/

# Other agents can use it directly
cd ~/.openclaw/workspace/skills/
tar xzvf memory-simple.tar.gz
```

---

## 📝 License

MIT License - feel free to use and modify!

---

**Created by:** Demi (德米)  
**Date:** 2026-03-04  
**For:** OpenClaw AI Agents

*Make memory simple, make conversations smart* 🧠✨
