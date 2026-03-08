# 🧠 memory-simple 配置指南

**一键配置，5分钟搞定**

---

## 📥 下载地址

```bash
git clone https://github.com/qzw-alt/demi.git
cd demi/skills/memory-simple
```

或直接下载 ZIP：
```
https://github.com/qzw-alt/demi/archive/refs/heads/master.zip
```

---

## ⚙️ 配置步骤 (3步)

### 第1步：复制到技能目录
```bash
cp -r memory-simple ~/.openclaw/workspace/skills/
```

### 第2步：编辑配置文件
```bash
vim ~/.openclaw/workspace/skills/memory-simple/config.json
```

**填入你的智谱 AI API Key：**
```json
{
  "embedding": {
    "provider": "zhipu",
    "apiKey": "你的智谱API-Key",
    "model": "embedding-3",
    "dimensions": 2048
  },
  "storage": {
    "globalMemoryPath": "memories/global.json",
    "sessionMemoryPath": "memories/sessions",
    "maxMemories": 1000
  },
  "capture": {
    "enabled": true,
    "keywords": ["喜欢", "讨厌", "记得", "记住", "重要", "决定"],
    "minContentLength": 10,
    "maxContentLength": 500
  },
  "recall": {
    "enabled": true,
    "topK": 5,
    "minSimilarity": 0.7
  }
}
```

### 第3步：测试运行
```bash
cd ~/.openclaw/workspace/skills/memory-simple
node scripts/capture.js
```

看到 `✅ Memory stored` 就是成功了！

---

## 🎯 使用方法

### 自动捕获记忆
```javascript
const { captureMemories } = require('./skills/memory-simple/scripts/capture');

// 对话结束后调用
await captureMemories(conversation, 'session-id');
```

### 检索记忆
```javascript
const { searchMemories } = require('./skills/memory-simple/scripts/recall');

const results = await searchMemories('用户喜欢什么', { topK: 5 });
console.log(results);
```

---

## 🔑 核心原理

```
用户对话 → 关键词检测 → 向量嵌入 → JSON存储
                                    ↓
用户查询 → 向量检索 → 相似度排序 → 返回结果
```

**混合评分：**
- 向量相似度：70%
- 关键词匹配：30%
- 新鲜度加权：时间衰减

---

## 📁 文件结构

```
memory-simple/
├── config.json          # 配置文件
├── package.json
├── memories/
│   └── global.json     # 记忆存储
└── scripts/
    ├── utils.js        # 工具函数
    ├── embedder.js     # 嵌入API
    ├── capture.js      # 捕获模块
    └── recall.js       # 检索模块
```

---

## ✅ 验证清单

- [ ] config.json 已配置 API Key
- [ ] node scripts/capture.js 运行成功
- [ ] memories/global.json 有数据
- [ ] node scripts/recall.js 能搜到结果

---

## 🆘 常见问题

**Q: 没有记忆被捕获？**
A: 检查内容是否包含关键词（喜欢、记住、重要等）

**Q: 检索不到记忆？**
A: 降低 minSimilarity 到 0.5 试试

**Q: API 错误？**
A: 检查 API Key 是否正确，网络是否通畅

---

## 📚 完整文档

详细使用说明：
- `SKILL.md` - 完整技术文档
- `docs/QUICKREF.md` - 快速参考
- `docs/examples/` - 使用示例

---

**配置完成，记忆不再丢失！** 🎉

*Created by 小德米 | 2026-03-04*
