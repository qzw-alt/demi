# 🔧 LanceDB-Pro 配置说明

## ✅ 配置已完成

### API Key 已配置
- **提供商**: 智谱 AI (Zhipu)
- **模型**: embedding-2
- **维度**: 1024
- **状态**: ✅ 已启用

### 配置文件位置
```
~/.openclaw/memory-lancedb-pro-config.json
```

### 配置内容
```json
{
  "plugins": {
    "load": {
      "paths": ["skills/memory-lancedb-pro"]
    },
    "entries": {
      "memory-lancedb-pro": {
        "enabled": true,
        "config": {
          "embedding": {
            "apiKey": "84b1936d14a84cfa83631aea1c78a56d.vQTK9kogx83kv2aQ",
            "model": "embedding-2",
            "baseURL": "https://open.bigmodel.cn/api/paas/v4",
            "dimensions": 1024
          },
          "dbPath": "~/.openclaw/memory/lancedb-pro",
          "autoCapture": true,
          "autoRecall": true,
          "retrieval": {
            "mode": "hybrid",
            "vectorWeight": 0.7,
            "bm25Weight": 0.3,
            "topK": 5
          }
        }
      }
    }
  }
}
```

---

## 🚀 下一步：合并到主配置

需要将这个配置合并到主配置文件 `~/.openclaw/openclaw.json`

### 手动合并步骤

1. **备份原配置**
```bash
cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.backup
```

2. **编辑主配置**
```bash
vim ~/.openclaw/openclaw.json
```

3. **在 `plugins` 部分添加**
```json
"plugins": {
  "load": {
    "paths": ["skills/memory-lancedb-pro"]
  },
  "entries": {
    ... 现有插件 ...
    "memory-lancedb-pro": {
      "enabled": true,
      "config": {
        "embedding": {
          "apiKey": "84b1936d14a84cfa83631aea1c78a56d.vQTK9kogx83kv2aQ",
          "model": "embedding-2",
          "baseURL": "https://open.bigmodel.cn/api/paas/v4",
          "dimensions": 1024
        },
        "dbPath": "~/.openclaw/memory/lancedb-pro",
        "autoCapture": true,
        "autoRecall": true
      }
    }
  }
}
```

4. **重启 OpenClaw**
```bash
openclaw gateway restart
```

5. **验证安装**
```bash
openclaw plugins list
openclaw memory stats
```

---

## 📝 配置说明

### 关键参数

| 参数 | 值 | 说明 |
|------|-----|------|
| `apiKey` | 你的智谱Key | 身份验证 |
| `model` | embedding-2 | 嵌入模型 |
| `baseURL` | 智谱API地址 | 服务端点 |
| `dimensions` | 1024 | 向量维度 |
| `autoCapture` | true | 自动捕获记忆 |
| `autoRecall` | true | 自动回忆记忆 |
| `mode` | hybrid | 混合检索模式 |

### 混合检索
- **vectorWeight**: 0.7 (向量搜索权重)
- **bm25Weight**: 0.3 (全文搜索权重)
- **topK**: 5 (返回前5个结果)

---

## ⚠️ 注意事项

1. **API Key 安全**: 不要泄露给他人
2. **备份配置**: 修改前备份原文件
3. **重启生效**: 配置修改后需要重启
4. **测试验证**: 重启后测试功能

---

## 🎯 预期效果

配置完成后：
- ✅ 自动捕获对话中的重要信息
- ✅ 智能检索相关历史记忆
- ✅ 向量语义搜索
- ✅ 混合检索 (向量+全文)

---

**配置完成，等待合并到主配置！** 🔧✨
