#!/bin/bash
# 智能摘要脚本 - Smart Compress
# 将工作日志压缩为关键信息

set -e

# 配置
WORKSPACE="${1:-$(pwd)}"
MEMORY_DIR="$WORKSPACE/memory"
DATE=$(date +%Y-%m-%d)

echo "🗜️  Smart Compress - 智能摘要"
echo "==============================="
echo ""

# 检查输入文件
INPUT_FILE="${2:-$MEMORY_DIR/$DATE.md}"
if [ ! -f "$INPUT_FILE" ]; then
    echo "❌ 错误: 输入文件不存在: $INPUT_FILE"
    exit 1
fi

echo "📄 输入文件: $INPUT_FILE"
echo ""

# 统计原始大小
ORIGINAL_SIZE=$(wc -c < "$INPUT_FILE")
echo "📊 原始大小: $ORIGINAL_SIZE 字符"
echo ""

# 创建输出文件
OUTPUT_FILE="${INPUT_FILE%.md}.summary.md"
echo "📝 输出文件: $OUTPUT_FILE"
echo ""

# 提取关键信息
echo "🔍 提取关键信息..."
echo ""

# 提取决策点
echo "  📌 提取决策点..."
DECISIONS=$(grep -E "(决定|策略|选择|采用|方案|确定)" "$INPUT_FILE" | head -5 || echo "")

# 提取成果
echo "  ✅ 提取成果..."
ACHIEVEMENTS=$(grep -E "^- \[x\]|完成|添加|更新|创建|提交" "$INPUT_FILE" | head -10 || echo "")

# 提取待办
echo "  📋 提取待办..."
TODOS=$(grep -E "^- \[ \]|待办|TODO|下一步" "$INPUT_FILE" | head -5 || echo "")

# 提取GitHub提交
echo "  💾 提取提交记录..."
COMMITS=$(grep -E "`[a-f0-9]{7}`|commit" "$INPUT_FILE" | head -5 || echo "")

# 提取关键洞察
echo "  💡 提取关键洞察..."
INSIGHTS=$(grep -E "洞察|教训|经验|关键|重要" "$INPUT_FILE" | head -3 || echo "")

echo ""

# 生成摘要文件
echo "📝 生成摘要文件..."

cat > "$OUTPUT_FILE" << EOF
# $(basename "$INPUT_FILE" .md) 摘要

> 生成时间: $(date '+%Y-%m-%d %H:%M')> 原始文件: $(basename "$INPUT_FILE")> 压缩率: 计算中...

---

## 🎯 关键决策

$(if [ -n "$DECISIONS" ]; then echo "$DECISIONS"; else echo "- 无关键决策记录"; fi)

---

## ✅ 完成成果

$(if [ -n "$ACHIEVEMENTS" ]; then echo "$ACHIEVEMENTS"; else echo "- 无完成成果记录"; fi)

---

## 📋 待办事项

$(if [ -n "$TODOS" ]; then echo "$TODOS"; else echo "- 无待办事项"; fi)

---

## 💾 GitHub提交

$(if [ -n "$COMMITS" ]; then echo "$COMMITS"; else echo "- 无提交记录"; fi)

---

## 💡 关键洞察

$(if [ -n "$INSIGHTS" ]; then echo "$INSIGHTS"; else echo "- 无关键洞察记录"; fi)

---

*此文件由 smart-compress.sh 自动生成*
*查看完整内容请访问: $(basename "$INPUT_FILE")*
EOF

# 计算压缩率
COMPRESSED_SIZE=$(wc -c < "$OUTPUT_FILE")
COMPRESSION_RATE=$(( (ORIGINAL_SIZE - COMPRESSED_SIZE) * 100 / ORIGINAL_SIZE ))

# 更新压缩率
sed -i "s/压缩率: 计算中.../压缩率: ${COMPRESSION_RATE}% (${ORIGINAL_SIZE} → ${COMPRESSED_SIZE} 字符)/" "$OUTPUT_FILE"

echo ""
echo "==============================="
echo "✅ 摘要生成完成!"
echo ""
echo "📊 压缩统计:"
echo "  原始大小: $ORIGINAL_SIZE 字符"
echo "  摘要大小: $COMPRESSED_SIZE 字符"
echo "  压缩率: ${COMPRESSION_RATE}%"
echo ""
echo "📄 输出文件: $OUTPUT_FILE"
echo ""

# 显示摘要内容
echo "📝 摘要内容预览:"
echo "==============================="
head -30 "$OUTPUT_FILE"
echo "..."
echo ""
