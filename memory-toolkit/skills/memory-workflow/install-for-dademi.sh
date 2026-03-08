#!/bin/bash
# Memory Workflow Skill - 一键安装脚本 (for 大德米)
# Usage: ./install-for-dademi.sh

set -e

echo "🧠 Memory Workflow Skill - 安装向导"
echo "===================================="
echo ""

# 检查是否在正确的目录
if [ ! -f "SKILL.md" ]; then
    echo "❌ 错误: 请在 memory-workflow 目录中运行此脚本"
    exit 1
fi

# 获取工作区路径
WORKSPACE="${1:-$(cd ../.. && pwd)}"
echo "📁 工作区路径: $WORKSPACE"
echo ""

# 1. 复制 skill 到工作区
echo "📦 安装 skill..."
mkdir -p "$WORKSPACE/skills"
cp -r . "$WORKSPACE/skills/memory-workflow"
echo "✅ Skill 已安装到: $WORKSPACE/skills/memory-workflow"
echo ""

# 2. 运行初始化
echo "🔧 初始化记忆系统..."
cd "$WORKSPACE/skills/memory-workflow"
./scripts/init.sh "$WORKSPACE"
echo ""

# 3. 提示更新 AGENTS.md
echo "📝 请手动更新 AGENTS.md"
echo ""
echo "在 AGENTS.md 的 'Every Session' 部分添加:"
echo ""
echo "3. Read \`memory/hot/HOT_MEMORY.md\`"
echo "4. Read \`memory/warm/WARM_MEMORY.md\`"
echo "5. Read \`PROJECT_INDEX.md\`"
echo ""

# 4. 提示设置 cron
echo "⏰ 设置晨间回顾 cron 任务:"
echo ""
echo "openclaw cron add \\"
echo "  --name '晨间记忆回顾' \\"
echo "  --cron '0 30 22 * * *' \\"
echo "  --message '执行晨间记忆回顾' \\"
echo "  --announce"
echo ""

# 5. 完成
echo "===================================="
echo "✅ 安装完成!"
echo ""
echo "下一步:"
echo "1. 更新 AGENTS.md 添加记忆读取规则"
echo "2. 配置 WARM_MEMORY.md 你的偏好"
echo "3. 配置 PROJECT_INDEX.md 你的项目"
echo "4. 设置 cron 任务 (可选)"
echo ""
echo "🎉 大德米可以开始使用记忆工作流了!"
echo ""
