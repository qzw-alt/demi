# Memory Workflow Skill - 简化版 (一键部署)

> 版本: v1.0.0-lite
> 适用: 快速部署，最小配置

---

## 🚀 超快速安装 (3步)

### Step 1: 下载并解压
```bash
cd ~/.openclaw/workspace
curl -L https://github.com/qzw-alt/demi/raw/master/skills/memory-workflow-lite.tar.gz | tar -xz
```

### Step 2: 一键初始化
```bash
bash memory-workflow-lite/install.sh
```

### Step 3: 更新 AGENTS.md
添加这3行到 `Every Session` 部分：
```markdown
3. Read `memory/hot/HOT_MEMORY.md`
4. Read `memory/warm/WARM_MEMORY.md`  
5. Read `PROJECT_INDEX.md`
```

✅ **完成！** 记忆系统已启用

---

## 📁 简化版结构

```
memory-workflow-lite/
├── install.sh          # 一键安装脚本
├── README.md           # 本文件
└── templates/
    ├── HOT_MEMORY.md   # 热记忆模板
    ├── WARM_MEMORY.md  # 温记忆模板
    └── PROJECT_INDEX.md # 项目索引模板
```

**总大小: < 5KB**

---

## 🎯 核心功能

| 功能 | 说明 |
|------|------|
| 🔥 HOT | 活跃任务，每次会话更新 |
| 🌡️ WARM | 稳定配置，偏好变更时更新 |
| 📋 PROJECT_INDEX | 项目速查，自动读取 |

**不包含**: 复杂脚本、cron任务、归档功能

---

## 💡 使用方式

### 每次会话自动读取
- HOT_MEMORY.md
- WARM_MEMORY.md
- PROJECT_INDEX.md

### 手动更新
```bash
# 编辑活跃任务
vim memory/hot/HOT_MEMORY.md

# 编辑项目索引
vim PROJECT_INDEX.md

# 编辑个人偏好
vim memory/warm/WARM_MEMORY.md
```

---

## 🔄 与完整版对比

| 功能 | 简化版 | 完整版 |
|------|--------|--------|
| 三层架构 | ✅ | ✅ |
| 自动读取 | ✅ (AGENTS.md) | ✅ (AGENTS.md) |
| 晨间回顾脚本 | ❌ | ✅ |
| 自动归档脚本 | ❌ | ✅ |
| Cron任务 | ❌ | ✅ |
| 安装包大小 | <5KB | ~15KB |

**简化版适合**: 快速部署，手动管理
**完整版适合**: 全自动管理

---

## 🆘 故障排除

### "文件不存在"
```bash
# 重新运行初始化
bash memory-workflow-lite/install.sh
```

### "AGENTS.md 未更新"
手动添加3行读取规则（见Step 3）

---

**极简部署，即刻使用！** 🚀
