#!/bin/bash
# GSC 周报生成 - 每周一 7:00 跑 (Asia/Shanghai)
# 输出 Markdown 报告给飞书
# 零 LLM cost (no_agent 模式, 直接 shell 跑 gsc 命令)

set -e

GSC="/home/ubuntu/.hermes/bin/gsc"

{
echo "📊 **GSC 周报** - $(date +'%Y-%m-%d %A')"
echo ""
echo "🔗 站点: chinahospitalsguide.com"
echo ""
echo "---"
echo ""
echo "## 总览 (过去 7 天)"
echo ""
$GSC summary 7 2>&1 || echo "❌ summary 失败"
echo ""
echo "---"
echo ""
echo "## Top 10 搜索词"
echo ""
$GSC top q 10 2>&1 || echo "❌ top q 失败"
echo ""
echo "---"
echo ""
echo "## 💎 改版金矿 (Top 10)"
echo ""
$GSC opportunities 2>&1 | head -25 || echo "❌ opportunities 失败"
echo ""
echo "---"
echo ""
echo "_报告自动生成于 $(date '+%Y-%m-%d %H:%M:%S') CST_"
echo ""
echo "**行动建议**:"
echo "1. 看总览 CTR 趋势 (健康线 > 3%)"
echo "2. 改版金矿里的 top 5 页面"
echo "3. 命令: \`gsc opportunities\` 看完整金矿"
} 2>&1
