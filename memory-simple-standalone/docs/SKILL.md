# 🧠 memory-simple-usage

**memory-simple 记忆系统使用指南**

一个简单、稳定、易用的 JSON 文件记忆系统，专为 OpenClaw 设计。

---

## 📖 目录

1. [快速开始](#快速开始)
2. [核心概念](#核心概念)
3. [使用方法](#使用方法)
4. [配置说明](#配置说明)
5. [最佳实践](#最佳实践)
6. [故障排除](#故障排除)

---

## 🚀 快速开始

### 1. 安装

```bash
# 复制到技能目录
cp -r memory-simple ~/.openclaw/workspace/skills/

# 配置 API Key
vim ~/.openclaw/workspace/skills/memory-simple/config.json
```

### 2. 配置 API Key

编辑 `config.json`：

```json
{
  "embedding": {
    "provider": "zhipu",
    "apiKey": "your-zhipu-api-key",
    "model": "embedding-3",
    "dimensions": 2048
  }
}
```

### 3. 测试

```bash
cd ~/.openclaw/workspace/skills/memory-simple

# 测试捕获
node scripts/capture.js

# 测试检索
node scripts/recall.js "用户喜欢什么"
```

---

## 🎯 核心概念

### 记忆类型

| 类型 | 说明 | 示例 |
|------|------|------|
| `preference` | 用户偏好 | "我喜欢喝咖啡" |
| `decision` | 重要决定 | "我决定选择A方案" |
| `important` | 重要信息 | "记住这是重要的" |
| `general` | 一般信息 | "用户住在上海" |

### 工作原理

```
用户对话 → 关键词检测 → 向量嵌入 → JSON存储
                                    ↓
用户查询 → 向量检索 → 相似度排序 → 返回结果
```

---

## 💡 使用方法

### 方法一：自动捕获 (推荐)

在对话结束时自动提取记忆：

```javascript
const { captureMemories } = require('./scripts/capture');

// 对话结束后调用
const conversation = [
  { role: 'user', content: '我喜欢喝绿茶' },
  { role: 'assistant', content: '好的，我记住了' },
  { role: 'user', content: '记住我的邮箱是 user@example.com' }
];

await captureMemories(conversation, 'session-123');
```

**触发关键词：**
- 中文：喜欢、讨厌、记得、记住、重要、决定、选择
- 英文：love, hate, remember, important, decide, choose, prefer

### 方法二：手动存储

```javascript
const { manualStore } = require('./scripts/capture');

// 存储偏好
await manualStore('用户喜欢蓝色', 'preference');

// 存储决定
await manualStore('用户决定使用方案A', 'decision');

// 存储重要信息
await manualStore('用户的项目截止时间是3月15日', 'important');
```

### 方法三：检索记忆

```javascript
const { searchMemories } = require('./scripts/recall');

// 基本检索
const results = await searchMemories('用户喜欢什么');

// 高级检索
const results = await searchMemories('用户喜欢什么', {
  topK: 5,              // 返回5条结果
  minSimilarity: 0.7,   // 最小相似度0.7
  sessionId: 'session-123'  // 包含会话记忆
});
```

### 方法四：获取最近记忆

```javascript
const { getRecentMemories } = require('./scripts/recall');

// 获取最近5条记忆
const recent = getRecentMemories(5);

// 获取特定会话的最近记忆
const recent = getRecentMemories(5, 'session-123');
```

### 方法五：格式化输出

```javascript
const { formatMemoriesForContext } = require('./scripts/recall');

const memories = await searchMemories('用户偏好');
const context = formatMemoriesForContext(memories);

console.log(context);
// 输出:
// [Relevant Memories]
// The following information may be relevant to the conversation:
//
// 1. [preference] 用户喜欢喝咖啡
// 2. [preference] 用户喜欢蓝色
```

---

## ⚙️ 配置说明

### 完整配置示例

```json
{
  "embedding": {
    "provider": "zhipu",
    "apiKey": "your-api-key",
    "model": "embedding-3",
    "dimensions": 2048
  },
  "storage": {
    "globalMemoryPath": "memories/global.json",
    "sessionMemoryPath": "memories/sessions",
    "maxMemories": 1000,
    "autoCleanup": true,
    "cleanupThreshold": 900
  },
  "capture": {
    "enabled": true,
    "keywords": [
      "喜欢", "讨厌", "记得", "记住", "重要", "决定", "选择",
      "love", "hate", "remember", "important", "decide", "choose"
    ],
    "minContentLength": 10,
    "maxContentLength": 500,
    "saveInterval": 300
  },
  "recall": {
    "enabled": true,
    "topK": 5,
    "minSimilarity": 0.7,
    "recencyWeight": 0.3,
    "similarityWeight": 0.7
  },
  "noiseFilter": {
    "enabled": true,
    "greetings": ["hi", "hello", "你好", "您好"],
    "refusalPatterns": ["i don't have", "我不知道"]
  }
}
```

### 配置项说明

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| `embedding.provider` | 嵌入模型提供商 | zhipu |
| `embedding.apiKey` | API密钥 | 必填 |
| `capture.enabled` | 启用自动捕获 | true |
| `capture.keywords` | 触发关键词 | 见上 |
| `recall.topK` | 返回结果数 | 5 |
| `recall.minSimilarity` | 最小相似度 | 0.7 |
| `recall.recencyWeight` | 新鲜度权重 | 0.3 |

---

## 🌟 最佳实践

### 1. 记忆捕获时机

```javascript
// ✅ 好的时机：对话结束时
await captureMemories(conversation, sessionId);

// ✅ 好的时机：用户明确说"记住"
if (message.includes('记住')) {
  await manualStore(content, type);
}
```

### 2. 记忆检索时机

```javascript
// ✅ 好的时机：对话开始时
const memories = await searchMemories(userQuery);
const context = formatMemoriesForContext(memories);
// 将 context 加入 LLM 提示词

// ✅ 好的时机：用户问"你还记得..."
if (message.includes('还记得') || message.includes('remember')) {
  const memories = await searchMemories(message);
}
```

### 3. 记忆内容优化

```javascript
// ✅ 好的内容：具体、简洁
"用户喜欢喝美式咖啡，不加糖"

// ❌ 避免：模糊、冗长
"用户好像说过他喜欢喝某种咖啡，可能是美式也可能是拿铁"
```

### 4. 定期清理

```javascript
// 系统会自动清理，但也可以手动清理
const { cleanupOldMemories } = require('./scripts/utils');
const data = readGlobalMemories(path);
cleanupOldMemories(data, 500);  // 只保留500条
```

---

## 🔧 故障排除

### 问题1：没有记忆被捕获

**检查：**
1. `capture.enabled` 是否为 `true`
2. 内容是否包含关键词
3. 内容长度是否在 10-500 字符之间

**调试：**
```javascript
// 添加日志
console.log('Content:', content);
console.log('Contains keywords:', containsCaptureKeywords(content, keywords));
console.log('Should filter:', shouldFilter(content, noiseFilter));
```

### 问题2：检索不到记忆

**检查：**
1. `recall.enabled` 是否为 `true`
2. `memories/global.json` 是否有数据
3. `minSimilarity` 是否设置太高

**调试：**
```javascript
// 降低阈值测试
const results = await searchMemories('测试', { minSimilarity: 0.5 });
console.log('Results:', results);
```

### 问题3：Embedding API 错误

**检查：**
1. API Key 是否正确
2. 网络连接是否正常
3. API 额度是否充足

**测试：**
```javascript
const { getEmbedding } = require('./scripts/embedder');

try {
  const embedding = await getEmbedding('测试文本');
  console.log('Embedding length:', embedding.length);
} catch (error) {
  console.error('Error:', error.message);
}
```

---

## 📊 性能指标

| 指标 | 数值 | 说明 |
|------|------|------|
| 存储容量 | 10,000+ 条 | JSON 文件 |
| 检索速度 | < 100ms | 1,000条数据 |
| 向量维度 | 2048 | 智谱 embedding-3 |
| 相似度阈值 | 0.7 | 可调 |

---

## 🔄 与 LanceDB-Pro 对比

| 特性 | memory-simple | LanceDB-Pro |
|------|---------------|-------------|
| 稳定性 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| 功能丰富 | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 易用性 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| 性能 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 维护成本 | 低 | 高 |

**选择建议：**
- 数据量 < 10,000 → memory-simple
- 追求稳定性 → memory-simple
- 需要高级功能 → LanceDB-Pro

---

## 🤝 分享与协作

这个记忆系统专为 OpenClaw 设计，可以轻松分享给其他 Agent：

```bash
# 打包分享
tar czvf memory-simple.tar.gz memory-simple/

# 其他 Agent 使用
cd ~/.openclaw/workspace/skills/
tar xzvf memory-simple.tar.gz
```

---

## 📝 更新日志

### v1.0.0 (2026-03-04)
- ✅ 初始版本发布
- ✅ 核心功能：捕获、检索、存储
- ✅ 混合检索：向量 + 关键词
- ✅ 新鲜度加权
- ✅ 噪音过滤

---

**作者：** 德米  
**创建时间：** 2026-03-04  
**许可证：** MIT

---

*让记忆更简单，让对话更智能* 🧠✨
