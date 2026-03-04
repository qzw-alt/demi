#!/bin/bash
# 工作流演示 - Workflow Demo
# 展示技能精通化的效果

echo "🎯 技能精通化演示"
echo "=================="
echo ""

echo "场景: 用户说 '研究一下医院排名'"
echo ""

# 模拟意图识别
echo "🔍 Step 1: 意图识别"
echo "   输入: '研究一下医院排名'"
echo "   识别结果: workflow:research"
echo "   置信度: 95%"
echo ""

# 模拟工作流执行
echo "🚀 Step 2: 执行研究工作流"
echo ""

echo "   [1/4] 广度搜索 (multi-search-engine)"
echo "   → 搜索: '中国医院排名 2024 复旦版'"
echo "   → 获取: 10个来源的概览信息"
echo "   ✓ 完成 (3秒)"
echo ""

echo "   [2/4] 深度分析 (tavily-search)"  
echo "   → 深度搜索: TOP10医院详细信息"
echo "   → 验证: 关键数据来源"
echo "   ✓ 完成 (5秒)"
echo ""

echo "   [3/4] 总结归纳 (summarize)"
echo "   → 提取: 关键发现和洞察"
echo "   → 生成: 结构化摘要"
echo "   ✓ 完成 (2秒)"
echo ""

echo "   [4/4] 记录保存 (doc-write)"
echo "   → 保存到: memory/research/医院排名_2026-03-04.md"
echo "   → 更新: PROJECT_INDEX.md"
echo "   ✓ 完成 (1秒)"
echo ""

echo "=================="
echo "✅ 工作流执行完成!"
echo ""
echo "📊 统计:"
echo "   总时间: 11秒"
echo "   使用技能: 4个"
echo "   用户指令: 1次"
echo "   输出: 完整研究报告"
echo ""
echo "对比传统方式:"
echo "   传统: 用户需要4次指令，手动协调"
echo "   工作流: 用户1次指令，自动完成"
echo "   效率提升: 300%"
echo ""
