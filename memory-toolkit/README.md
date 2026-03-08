# 🧠 德米记忆工具包 (Memory Toolkit)

**完整的AI记忆管理解决方案**

---

## 📦 包含内容

### 1. 核心技能 (skills/)

| 技能 | 用途 | 复杂度 |
|------|------|--------|
| **memory-simple** | 轻量级记忆系统 (推荐) | ⭐ 简单 |
| **memory-workflow** | 完整工作流管理 | ⭐⭐ 中等 |
| **memory-tiering** | 三层记忆架构 | ⭐⭐⭐ 高级 |

### 2. 实用脚本 (scripts/)

| 脚本 | 功能 |
|------|------|
| **morning-review.sh** | 晨间记忆回顾 |
| **smart-compress.sh** | 智能对话压缩 |

### 3. 文档 (docs/)

| 文档 | 内容 |
|------|------|
| **记忆系统铭记录.md** | 核心原则与决策 |
| **晨间记忆回顾方案.md** | 晨间回顾完整方案 |

---

## 🚀 快速开始

### 方案A：轻量级 (推荐)

```bash
# 1. 安装 memory-simple
cd skills/memory-simple
npm install

# 2. 配置 API Key
vim config.json
# 填入你的智谱 AI API Key

# 3. 测试
node scripts/capture.js
node scripts/recall.js "测试"
```

### 方案B：完整工作流

```bash
# 使用 memory-workflow 技能
# 包含：三层记忆架构 + 晨间回顾 + 项目索引
```

---

## 📁 文件结构

```
memory-toolkit/
├── README.md                    # 本文件
├── skills/
│   ├── memory-simple/          # 轻量级记忆系统
│   │   ├── config.json         # 配置文件
│   │   ├── scripts/
│   │   │   ├── capture.js      # 自动捕获
│   │   │   ├── recall.js       # 记忆检索
│   │   │   ├── morning-review.sh  # 晨间回顾
│   │   │   └── embedder.js     # 向量嵌入
│   │   └── memories/           # 记忆存储
│   ├── memory-workflow/        # 完整工作流
│   │   ├── SKILL.md            # 使用文档
│   │   └── scripts/
│   └── memory-tiering/         # 三层记忆架构
├── scripts/
│   ├── morning-memory-review.sh
│   └── smart-compress.sh
└── docs/
    ├── 记忆系统铭记录.md
    └── 晨间记忆回顾方案.md
```

---

## 🔑 核心原理

### 记忆捕获
```
对话内容 → 关键词检测 → 向量嵌入 → JSON存储
```

### 记忆检索
```
用户查询 → 向量检索 → 相似度排序 → 返回结果
```

### 混合评分
- 向量相似度: 70%
- 关键词匹配: 30%
- 新鲜度加权: 时间衰减

---

## ⚙️ 配置说明

### 必需配置
```json
{
  "embedding": {
    "provider": "zhipu",
    "apiKey": "你的智谱API-Key",
    "model": "embedding-3"
  }
}
```

### 获取智谱 API Key
1. 访问 https://open.bigmodel.cn/
2. 注册账号
3. 创建 API Key
4. 复制到 config.json

---

## 📝 使用示例

### 自动捕获记忆
```javascript
const { captureMemories } = require('./skills/memory-simple/scripts/capture');
await captureMemories(conversation, 'session-id');
```

### 检索记忆
```javascript
const { searchMemories } = require('./skills/memory-simple/scripts/recall');
const results = await searchMemories('用户喜欢什么');
```

### 晨间回顾
```bash
./scripts/morning-review.sh
```

---

## 🎯 使用场景

| 场景 | 推荐方案 |
|------|---------|
| 快速上手 | memory-simple |
| 完整工作流 | memory-workflow |
| 高级管理 | memory-tiering |
| 定时回顾 | morning-review.sh |

---

## 🔗 相关链接

- **GitHub**: https://github.com/qzw-alt/demi
- **配置指南**: skills/memory-simple/CONFIG.md
- **完整文档**: skills/memory-simple/SKILL.md

---

## 💡 核心原则

> "记忆是AI的灵魂，没有记忆就没有智能"

> "稳定性永远优先于功能丰富"

> "简单可依赖 > 复杂易崩溃"

---

**Created by 小德米 | 2026-03-04**

**License: MIT**
