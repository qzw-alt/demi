#!/bin/bash
# Memory Workflow Skill - 简化版一键安装
# 总大小: <5KB, 3步完成部署

set -e

echo "🧠 Memory Workflow Lite - 一键安装"
echo "==================================="
echo ""

WORKSPACE="$(pwd)"
DATE=$(date +%Y-%m-%d)

echo "📁 工作区: $WORKSPACE"
echo ""

# 创建目录
echo "📂 创建目录结构..."
mkdir -p memory/hot memory/warm
echo "✅ 目录创建完成"
echo ""

# 创建 HOT_MEMORY.md
echo "📝 创建 HOT_MEMORY.md..."
cat > memory/hot/HOT_MEMORY.md << 'EOF'
# 🔥 HOT MEMORY - 当前活跃任务

> 最后更新: DATE_PLACEHOLDER
> 更新频率: 每次会话

---

## 🎯 活跃任务

### 项目1
- **状态**: 
- **今日待办**:
  - [ ] 

---

*此文件每次会话更新，只保留当前活跃任务*
EOF
sed -i "s/DATE_PLACEHOLDER/$DATE/g" memory/hot/HOT_MEMORY.md
echo "✅ HOT_MEMORY.md 创建完成"
echo ""

# 创建 WARM_MEMORY.md
echo "📝 创建 WARM_MEMORY.md..."
cat > memory/warm/WARM_MEMORY.md << 'EOF'
# 🌡️ WARM MEMORY - 稳定配置

> 最后更新: DATE_PLACEHOLDER
> 更新频率: 偏好变更时

---

## 👤 用户配置

| 项目 | 值 |
|------|-----|
| 名称 | |
| 时区 | Asia/Shanghai |
| 风格 | |

## 🛠️ 常用技能

- memory-workflow

## 📋 项目列表

| 项目 | 状态 | 关键文件 |
|------|------|---------|
| | | PROJECT_INDEX.md |

---

*此文件记录稳定配置，只在变更时更新*
EOF
sed -i "s/DATE_PLACEHOLDER/$DATE/g" memory/warm/WARM_MEMORY.md
echo "✅ WARM_MEMORY.md 创建完成"
echo ""

# 创建 PROJECT_INDEX.md
echo "📝 创建 PROJECT_INDEX.md..."
cat > PROJECT_INDEX.md << 'EOF'
# PROJECT_INDEX - 项目速查表

> 每次会话自动读取
> 最后更新: DATE_PLACEHOLDER

---

## 🏥 项目1

### 核心信息
| 项目 | 值 |
|------|-----|
| 名称 | |
| 网站 | |
| GitHub | |

### 本周待办
- [ ] 

### 本周完成
- [x] 

---

*此文件确保每次会话都能获取最新项目状态*
EOF
sed -i "s/DATE_PLACEHOLDER/$DATE/g" PROJECT_INDEX.md
echo "✅ PROJECT_INDEX.md 创建完成"
echo ""

# 创建今日日志
echo "📝 创建今日工作日志..."
cat > memory/$DATE.md << EOF
# $DATE 工作日志

## 🎯 今日目标
- 

## 📥 输入
- 

## 🔄 过程
- 

## 📤 输出
- 

## 🔜 下一步
- 
EOF
echo "✅ $DATE.md 创建完成"
echo ""

# 完成提示
echo "==================================="
echo "✅ 安装完成!"
echo ""
echo "📝 请手动更新 AGENTS.md:"
echo "   在 'Every Session' 部分添加:"
echo ""
echo "   3. Read \`memory/hot/HOT_MEMORY.md\`"
echo "   4. Read \`memory/warm/WARM_MEMORY.md\`"
echo "   5. Read \`PROJECT_INDEX.md\`"
echo ""
echo "🎉 记忆系统已就绪!"
echo ""
