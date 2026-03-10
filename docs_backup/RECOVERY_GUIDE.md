# 🆘 OpenClaw 快速恢复指南

> 当系统崩溃或需要重新部署时的恢复清单
> 版本: v1.0

---

## ⚡ 5分钟快速恢复

### Step 1: 检查核心文件 (1分钟)

```bash
# 必须存在的文件
cd ~/.openclaw/workspace

ls -la \
  AGENTS.md \
  SOUL.md \
  USER.md \
  MEMORY.md \
  PROJECT_INDEX.md
```

**如果缺失**: 从 GitHub 恢复
```bash
git clone https://github.com/qzw-alt/demi.git /tmp/demi-backup
cp /tmp/demi-backup/AGENTS.md .
cp /tmp/demi-backup/SOUL.md .
# ... 复制其他缺失文件
```

### Step 2: 检查记忆系统 (1分钟)

```bash
# 检查三层记忆
ls -la memory/hot/HOT_MEMORY.md
ls -la memory/warm/WARM_MEMORY.md
ls -la PROJECT_INDEX.md
```

**如果缺失**: 重新初始化
```bash
# 使用简化版一键恢复
curl -L https://github.com/qzw-alt/demi/raw/master/skills/memory-workflow-lite.tar.gz | tar -xz
bash memory-workflow-lite/install.sh
```

### Step 3: 检查技能 (1分钟)

```bash
ls ~/.openclaw/workspace/skills/
```

**关键技能**:
- memory-workflow (或 memory-workflow-lite)
- web-search
- multi-search-engine

### Step 4: 检查 Cron 任务 (1分钟)

```bash
openclaw cron list
```

**如果缺失**: 重新创建
```bash
# 晨间回顾
openclaw cron add \
  --name "晨间记忆回顾" \
  --cron "0 30 22 * * *" \
  --message "执行晨间记忆回顾" \
  --announce
```

### Step 5: 验证 (1分钟)

```bash
# 测试读取记忆
cat memory/hot/HOT_MEMORY.md
cat PROJECT_INDEX.md

# 测试技能
openclaw skill memory-workflow --help 2>/dev/null || echo "技能未安装"
```

---

## 📦 完整备份恢复 (15分钟)

### 如果有完整备份

```bash
# 1. 停止 OpenClaw
openclaw gateway stop

# 2. 恢复备份
cp -r /path/to/backup/workspace ~/.openclaw/

# 3. 重启
openclaw gateway start
```

### 如果从 GitHub 恢复

```bash
# 1. 克隆仓库
git clone https://github.com/qzw-alt/demi.git /tmp/demi-recovery

# 2. 复制所有文件
cp -r /tmp/demi-recovery/* ~/.openclaw/workspace/

# 3. 重新安装依赖 (如果有)
# cd ~/.openclaw/workspace && npm install

# 4. 验证
openclaw status
```

---

## 🔧 常见问题恢复

### 问题1: AGENTS.md 损坏

**症状**: 不自动读取记忆文件

**恢复**:
```bash
cat > AGENTS.md << 'EOF'
# AGENTS.md - Your Workspace

## Every Session

Before doing anything else:

1. Read `SOUL.md`
2. Read `USER.md`
3. Read `memory/hot/HOT_MEMORY.md`
4. Read `memory/warm/WARM_MEMORY.md`
5. Read `PROJECT_INDEX.md`
6. Read `memory/YYYY-MM-DD.md` (today + yesterday)
7. **If in MAIN SESSION**: Also read `MEMORY.md`

Don't ask permission. Just do it.
EOF
```

### 问题2: 记忆文件丢失

**症状**: 找不到 HOT_MEMORY.md 等文件

**恢复**:
```bash
# 使用简化版快速恢复
curl -L https://raw.githubusercontent.com/qzw-alt/demi/master/skills/memory-workflow-lite/install.sh | bash
```

### 问题3: 技能丢失

**症状**: 命令不存在

**恢复**:
```bash
# 重新安装核心技能
cd ~/.openclaw/workspace/skills

# 从 GitHub 恢复
git clone https://github.com/qzw-alt/demi.git /tmp/demi
cp -r /tmp/demi/skills/* .
```

### 问题4: Cron 任务丢失

**症状**: 定时任务不执行

**恢复**:
```bash
# 查看现有任务
openclaw cron list

# 重新创建核心任务
openclaw cron add --name "晨间记忆回顾" --cron "0 30 22 * * *" \
  --message "执行晨间记忆回顾" --announce

# 医疗旅游任务 (如果有)
# ... 其他任务
```

---

## 🛡️ 预防措施

### 1. 定期 Git 提交

```bash
cd ~/.openclaw/workspace
git add -A
git commit -m "备份: $(date +%Y-%m-%d)"
git push origin master
```

### 2. 关键文件备份清单

**必须备份**:
- AGENTS.md
- SOUL.md
- USER.md
- MEMORY.md
- PROJECT_INDEX.md
- memory/hot/HOT_MEMORY.md
- memory/warm/WARM_MEMORY.md
- skills/ (自定义技能)

**可以重新生成**:
- memory/YYYY-MM-DD.md (每日日志)
- 临时文件

### 3. 自动化备份脚本

```bash
#!/bin/bash
# backup.sh - 每日自动备份

cd ~/.openclaw/workspace
git add -A
git commit -m "自动备份: $(date +%Y-%m-%d-%H:%M)"
git push origin master
echo "✅ 备份完成: $(date)"
```

添加到 cron:
```bash
openclaw cron add --name "每日备份" --cron "0 30 23 * * *" \
  --command "cd ~/.openclaw/workspace && git add -A && git commit -m '自动备份' && git push"
```

---

## 📞 紧急联系

如果无法恢复:
1. 检查 GitHub 仓库是否完好
2. 查看 OpenClaw 官方文档
3. 联系社区支持

---

## ✅ 恢复检查清单

恢复后验证:

- [ ] AGENTS.md 存在且配置正确
- [ ] SOUL.md 存在
- [ ] USER.md 存在
- [ ] MEMORY.md 存在
- [ ] PROJECT_INDEX.md 存在
- [ ] memory/hot/HOT_MEMORY.md 存在
- [ ] memory/warm/WARM_MEMORY.md 存在
- [ ] 核心技能已安装
- [ ] Cron 任务已创建
- [ ] Git 提交正常
- [ ] 测试会话能正常读取记忆

---

**记住: 定期备份是最佳恢复策略!** 💾

---

*创建时间: 2026-03-04*
*适用版本: OpenClaw 2026.2.26+*
