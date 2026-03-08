# 🧠 memory-simple

**Simple JSON-based Memory System for OpenClaw**

A lightweight, stable alternative to LanceDB-Pro. No complex dependencies, no crashes, just reliable memory storage and retrieval.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| **JSON Storage** | Simple JSON files, no database crashes |
| **Vector Search** | Semantic similarity using embeddings |
| **Keyword Search** | Basic text matching for exact queries |
| **Hybrid Scoring** | Combines similarity + recency |
| **Auto Capture** | Automatically extracts memories from conversations |
| **Noise Filter** | Filters out greetings and low-quality content |
| **Session Memory** | Separate memory spaces per session |

---

## 🚀 Quick Start

### 1. Configuration

Edit `config.json`:

```json
{
  "embedding": {
    "provider": "zhipu",
    "apiKey": "your-api-key",
    "model": "embedding-3",
    "dimensions": 2048
  }
}
```

### 2. Capture Memories

```javascript
const { captureMemories } = require('./scripts/capture');

const conversation = [
  { role: 'user', content: '我喜欢喝咖啡' },
  { role: 'user', content: '记住我的邮箱是 user@example.com' }
];

await captureMemories(conversation, 'session-id');
```

### 3. Recall Memories

```javascript
const { searchMemories } = require('./scripts/recall');

const results = await searchMemories('用户喜欢什么', {
  topK: 5,
  sessionId: 'session-id'
});

console.log(results);
```

---

## 📁 File Structure

```
memory-simple/
├── config.json              # Configuration
├── package.json
├── SKILL.md                 # This file
├── memories/
│   ├── global.json         # Global memories
│   └── sessions/           # Session-specific memories
│       ├── session-1.json
│       └── session-2.json
└── scripts/
    ├── utils.js            # Utility functions
    ├── embedder.js         # Embedding API
    ├── capture.js          # Memory capture
    └── recall.js           # Memory retrieval
```

---

## ⚙️ Configuration

### Embedding Settings

| Option | Description | Default |
|--------|-------------|---------|
| `provider` | Embedding provider | `zhipu` |
| `apiKey` | API key | Required |
| `model` | Model name | `embedding-3` |
| `dimensions` | Vector dimensions | `2048` |

### Capture Settings

| Option | Description | Default |
|--------|-------------|---------|
| `enabled` | Enable auto-capture | `true` |
| `keywords` | Trigger keywords | See config |
| `minContentLength` | Minimum content length | `10` |
| `maxContentLength` | Maximum content length | `500` |

### Recall Settings

| Option | Description | Default |
|--------|-------------|---------|
| `enabled` | Enable recall | `true` |
| `topK` | Number of results | `5` |
| `minSimilarity` | Minimum similarity threshold | `0.7` |
| `recencyWeight` | Weight for recency (0-1) | `0.3` |
| `similarityWeight` | Weight for similarity (0-1) | `0.7` |

---

## 🔧 API Reference

### Capture Module

#### `captureMemories(conversation, sessionId?)`

Automatically extracts and stores memories from conversation.

**Parameters:**
- `conversation` (Array): Array of message objects
- `sessionId` (String, optional): Session identifier

**Returns:** Promise<Array> - Captured memories

**Example:**
```javascript
const memories = await captureMemories([
  { role: 'user', content: '我喜欢喝茶' },
  { role: 'assistant', content: '好的' },
  { role: 'user', content: '记得提醒我下午开会' }
], 'session-123');
```

#### `manualStore(content, type?, metadata?)`

Manually store a memory.

**Parameters:**
- `content` (String): Memory content
- `type` (String): Memory type (preference, decision, important, general)
- `metadata` (Object): Additional metadata

**Returns:** Promise<Object> - Stored memory

**Example:**
```javascript
const memory = await manualStore(
  '用户喜欢蓝色',
  'preference',
  { source: 'manual' }
);
```

### Recall Module

#### `searchMemories(query, options?)`

Search for relevant memories.

**Parameters:**
- `query` (String): Search query
- `options` (Object):
  - `topK` (Number): Number of results
  - `minSimilarity` (Number): Minimum similarity threshold
  - `sessionId` (String): Include session memories
  - `includeGlobal` (Boolean): Include global memories

**Returns:** Promise<Array> - Matching memories with scores

**Example:**
```javascript
const results = await searchMemories('用户喜欢什么', {
  topK: 3,
  sessionId: 'session-123'
});
```

#### `getRecentMemories(limit?, sessionId?)`

Get most recent memories.

**Parameters:**
- `limit` (Number): Number of memories to retrieve
- `sessionId` (String): Session identifier

**Returns:** Array - Recent memories

#### `formatMemoriesForContext(memories)`

Format memories for injection into LLM context.

**Parameters:**
- `memories` (Array): Memories to format

**Returns:** String - Formatted context string

---

## 🎯 Memory Types

The system automatically categorizes memories:

| Type | Description | Example |
|------|-------------|---------|
| `preference` | User likes/dislikes | "我喜欢喝咖啡" |
| `decision` | Important decisions | "我决定选择A方案" |
| `important` | Important information | "记住这是重要的" |
| `general` | General facts | "用户住在上海" |

---

## 🧪 Testing

### Run Tests

```bash
cd ~/.openclaw/workspace/skills/memory-simple

# Test capture
node scripts/capture.js

# Test recall
node scripts/recall.js "用户喜欢什么"
```

### Manual Test

```javascript
const { captureMemories } = require('./scripts/capture');
const { searchMemories } = require('./scripts/recall');

async function test() {
  // Capture
  await captureMemories([
    { role: 'user', content: '我喜欢喝绿茶' }
  ]);
  
  // Recall
  const results = await searchMemories('用户喜欢什么饮料');
  console.log(results);
}

test();
```

---

## 🔒 Privacy & Security

- All data stored locally in JSON files
- No external data sharing
- API keys stored in local config
- Session isolation for privacy

---

## 🐛 Troubleshooting

### No memories being captured

1. Check `capture.enabled` is `true` in config
2. Verify content contains capture keywords
3. Check content length is within limits

### Search returns no results

1. Check `recall.enabled` is `true`
2. Verify memories exist in `memories/global.json`
3. Try lowering `minSimilarity` threshold

### Embedding API errors

1. Verify API key is correct
2. Check network connectivity
3. Review API rate limits

---

## 📝 Comparison with LanceDB-Pro

| Aspect | memory-simple | LanceDB-Pro |
|--------|---------------|-------------|
| **Stability** | ✅ Very stable | ⚠️ Can crash |
| **Complexity** | Simple | Complex |
| **Features** | Core features only | Advanced features |
| **Dependencies** | None | LanceDB, etc. |
| **Performance** | Good for small data | Better for large data |
| **Maintenance** | Easy | Requires expertise |

**Choose memory-simple if:**
- You want stability over features
- Your data volume is moderate (< 10,000 memories)
- You prefer simple, maintainable code

**Choose LanceDB-Pro if:**
- You need advanced features (MMR, complex reranking)
- You have large data volumes
- You need multi-scope isolation

---

## 🤝 Contributing

This is a custom skill for internal use. Feel free to modify and extend.

---

*Created by Demi | 2026-03-04*
