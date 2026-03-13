#!/bin/bash
# 晨间记忆回顾脚本 - 每天早上自动执行
# 时间: 06:30 UTC (对应中国时间 14:30，或调整为 22:00 UTC = 06:00 CST)

echo "🌅 晨间记忆回顾开始..."
echo "时间: $(date)"
echo ""

# 1. 读取核心记忆文件
echo "📖 读取核心记忆..."
echo "- SOUL.md"
echo "- USER.md"
echo "- memory/hot/HOT_MEMORY.md"
echo "- memory/warm/WARM_MEMORY.md"
echo "- PROJECT_INDEX.md"
echo ""

# 2. 检查昨日工作
echo "📅 检查昨日工作日志..."
YESTERDAY=$(date -d "yesterday" +%Y-%m-%d)
if [ -f "memory/${YESTERDAY}.md" ]; then
    echo "✅ 找到昨日日志: memory/${YESTERDAY}.md"
    echo "📊 昨日关键成果:"
    grep -E "^###|^- \[x\]|^\*\*.*完成" "memory/${YESTERDAY}.md" | head -10
else
    echo "⚠️ 昨日日志不存在"
fi
echo ""

# 3. 检查今日待办
echo "🎯 今日待办检查..."
TODAY=$(date +%Y-%m-%d)
if [ -f "memory/${TODAY}.md" ]; then
    echo "✅ 今日日志已存在"
    grep -E "^- \[ \]" "memory/${TODAY}.md" | head -5
else
    echo "📝 今日日志尚未创建"
fi
echo ""

# 4. 项目状态检查
echo "🏥 医疗旅游项目状态:"
echo "- 网站: https://chinahospitalsguide.com"
echo "- 医院数: 40+"
echo "- 本周待办: 见 PROJECT_INDEX.md"
echo ""

echo "📱 龙康劲项目状态:"
echo "- 人设: 老秦"
echo "- 内容: 视频号每周3条"
echo ""

# 5. 邮件回复检查（重要！）
echo "📧 邮件回复检查（重要工作）..."
echo ""
echo "🔍 检查步骤:"
echo "1. 登录 AgentMail: https://agentmail.to/"
echo "   邮箱: motionlessbottle950@agentmail.to"
echo ""
echo "2. 检查新邮件:"
echo "   - 未读邮件数量"
echo "   - 客户咨询内容"
echo "   - 紧急程度判断"
echo ""
echo "3. 自动回复检查:"
echo "   - 确认 auto_reply_bot.py 运行状态"
echo "   - 检查昨日自动回复记录"
echo "   - 查看是否有客户回复了自动邮件"
echo ""
echo "4. 需要人工处理的邮件:"
echo "   - 客户已回复自动邮件（进入第2轮）"
echo "   - 复杂病情需要定制推荐"
echo "   - 投诉或特殊要求"
echo ""
echo "⚠️ 注意: 邮件回复是主要工作，务必做到:"
echo "   - 24小时内回复所有新邮件"
echo "   - 自动回复后立即跟进客户回复"
echo "   - 不要漏掉任何客户咨询"
echo ""

# 6. 技能清单
echo "🛠️ 已安装技能:"
echo "- memory-tiering (三层记忆架构)"
echo "- multi-search-engine (搜索)"
echo "- lenny-skills (86个产品技能)"
echo "- web-search, agent-browser, learning"
echo ""

echo "✅ 晨间记忆回顾完成!"
echo "🚀 准备好开始今天的工作了"
echo ""
echo "💡 今日首要任务: 检查并处理客户邮件"
