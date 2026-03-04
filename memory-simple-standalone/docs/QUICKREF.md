# 🧠 memory-simple 快速参考

## 安装
```bash
cd ~/.openclaw/workspace/skills/
# 复制 memory-simple 文件夹
# 编辑 config.json 填入 API Key
```

## 核心 API

### 捕获记忆
```javascript
const { captureMemories, manualStore } = require('./scripts/capture');

// 自动捕获
await captureMemories(conversation, 'session-id');

// 手动存储
await manualStore('内容', 'type', { source: 'manual' });
```

### 检索记忆
```javascript
const { searchMemories, getRecentMemories, formatMemoriesForContext } = require('./scripts/recall');

// 语义检索
const results = await searchMemories('查询内容', {
  topK: 5,
  minSimilarity: 0.7,
  sessionId: 'session-id'
});

// 获取最近记忆
const recent = getRecentMemories(5, 'session-id');

// 格式化为上下文
const context = formatMemoriesForContext(results);
```

## 记忆类型

| 类型 | 用途 |
|------|------|
| `preference` | 用户偏好 |
| `decision` | 重要决定 |
| `important` | 重要信息 |
| `general` | 一般信息 |

## 触发关键词

- 中文：喜欢、讨厌、记得、记住、重要、决定、选择
- 英文：love, hate, remember, important, decide, choose, prefer

## 配置项

```json
{
  "embedding": {
    "apiKey": "your-api-key"
  },
  "capture": {
    "enabled": true,
    "minContentLength": 10,
    "maxContentLength": 500
  },
  "recall": {
    "topK": 5,
    "minSimilarity": 0.7
  }
}
```

## 文件位置

- 全局记忆：`memories/global.json`
- 会话记忆：`memories/sessions/{session-id}.json`

## 最佳实践

1. **捕获时机**：对话结束时自动捕获
2. **检索时机**：对话开始时检索上下文
3. **内容优化**：具体、简洁、避免模糊
4. **定期清理**：系统自动，也可手动

## 故障排除

| 问题 | 解决 |
|------|------|
| 无记忆捕获 | 检查关键词、长度、enabled |
| 检索不到 | 降低 minSimilarity、检查文件 |
| API 错误 | 检查 API Key、网络、额度 |

---

**完整文档：** 参见 SKILL.md
