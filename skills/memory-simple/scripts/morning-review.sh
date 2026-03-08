#!/bin/bash
# 晨间记忆回顾脚本 - 每天早上自动执行
# 用法: ./morning-memory-review.sh

echo "🌅 晨间记忆回顾开始..."
echo "时间: $(date)"
echo ""

# 1. 读取核心记忆文件
echo "📖 读取核心记忆..."
echo "- SOUL.md (AI身份设定)"
echo "- USER.md (用户信息)"
echo "- memory/hot/HOT_MEMORY.md (当前任务)"
echo "- memory/warm/WARM_MEMORY.md (稳定配置)"
echo "- PROJECT_INDEX.md (项目索引)"
echo ""

# 2. 检查昨日工作
echo "📅 检查昨日工作日志..."
YESTERDAY=$(date -d "yesterday" +%Y-%m-%d 2>/dev/null || date -v-1d +%Y-%m-%d)
if [ -f "memory/${YESTERDAY}.md" ]; then
    echo "✅ 找到昨日日志: memory/${YESTERDAY}.md"
    echo "📊 昨日关键成果:"
    grep -E "^- \[x\]|^###.*完成|✅" "memory/${YESTERDAY}.md" | head -10
else
    echo "⚠️ 昨日日志不存在"
fi
echo ""

# 3. 检查今日待办
echo "🎯 今日待办检查..."
TODAY=$(date +%Y-%m-%d)
if [ -f "memory/${TODAY}.md" ]; then
    echo "✅ 今日日志已存在"
    echo "📋 今日待办:"
    grep -E "^- \[ \]" "memory/${TODAY}.md" | head -5
else
    echo "📝 今日日志尚未创建，建议创建: memory/${TODAY}.md"
fi
echo ""

# 4. 项目状态速览
echo "🏥 项目状态速览:"
echo "- 医疗旅游: 运营中 (7页面+6博客+3患者故事)"
echo "- 本周重点: 见 PROJECT_INDEX.md"
echo ""

# 5. 技能清单
echo "🛠️ 核心技能:"
echo "- memory-tiering, multi-search-engine, lenny-skills"
echo "- web-search, agent-browser, learning"
echo ""

echo "✅ 晨间记忆回顾完成!"
echo "🚀 准备好开始今天的工作了"
