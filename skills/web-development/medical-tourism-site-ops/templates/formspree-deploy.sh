#!/bin/bash
# Formspree endpoint 一键部署 (chinahospitalsguide archetype)
#
# 用法: ./formspree-deploy.sh YOUR_FORMSPREE_ID
# 示例: ./formspree-deploy.sh xyzabcde
#
# 流程:
#   1. 全局替换 index.html + blog/index.html 内的
#      `REPLACE_WITH_YOUR_FORMSPREE_ID` 占位为真实 endpoint
#   2. git commit + push (含 rebase 处理 fast-forward 冲突)
#   3. 等 60s Cloudflare 部署
#   4. 验证 prod 实际看到新 endpoint
#
# 站点: chinahospitalsguide.com (Eleventy + GitHub Pages + Cloudflare cache)
# 当前状态 (2026-07-02): 德米注册了 Formspree, 待提供 ID 后跑这个脚本

set -e

if [ -z "$1" ]; then
    echo "❌ 用法: $0 <formspree-id>"
    echo "   例如: $0 xyzabcde"
    echo "   Endpoint 会变成: https://formspree.io/f/xyzabcde"
    exit 1
fi

FORMSPREE_ID="$1"
ENDPOINT="https://formspree.io/f/${FORMSPREE_ID}"

cd /home/ubuntu/.hermes/workspace/website

echo "📋 Formspree endpoint: $ENDPOINT"
echo

# 1. 替换 index.html + blog/index.html
echo "[1/4] 替换 endpoint 到 2 个文件..."
for f in index.html blog/index.html; do
    if grep -q "REPLACE_WITH_YOUR_FORMSPREE_ID" "$f"; then
        sed -i "s|REPLACE_WITH_YOUR_FORMSPREE_ID|${FORMSPREE_ID}|g" "$f"
        echo "  ✓ $f"
    else
        echo "  - $f (无占位, 跳过)"
    fi
done

# 2. 验证替换生效
echo
echo "[2/4] 验证替换..."
COUNT=$(grep -c "formspree.io/f/${FORMSPREE_ID}" index.html blog/index.html | awk -F: '{s+=$2} END {print s}')
echo "  endpoint 出现次数: $COUNT (期望: 2)"
if grep -q "REPLACE_WITH_YOUR_FORMSPREE_ID" index.html blog/index.html; then
    echo "❌ 仍有未替换的占位!"
    exit 1
fi
echo "  ✓ 没有遗留占位"

# 3. git commit + push (含 rebase)
echo
echo "[3/4] git commit + push..."
git add index.html blog/index.html
git commit -m "Formspree: activate newsletter subscription (ID: ${FORMSPREE_ID})

Replaced REPLACE_WITH_YOUR_FORMSPREE_ID placeholder with actual Formspree
endpoint in 2 files (index.html + blog/index.html).

Newsletter form now actually subscribes users. Submissions go to the email
configured in Formspree dashboard.

Endpoint: ${ENDPOINT}"

# 远程可能已有 commit (hermes-backup cron 等), 用 rebase 处理
git pull --rebase origin master 2>/dev/null || true
git push origin master

# 4. 等 60s 验证
echo
echo "[4/4] 等 60s 让 Cloudflare 部署..."
sleep 60

# 验证 prod 看到新 endpoint (绕过 cache)
echo
echo "=== prod 验证 ==="
for url in "https://chinahospitalsguide.com/" "https://chinahospitalsguide.com/blog/"; do
    if curl -s -H "Cache-Control: no-cache" "$url" | grep -q "${FORMSPREE_ID}"; then
        echo "  ✓ $url 含 endpoint"
    else
        echo "  ⚠ $url 不含 endpoint (可能 cache, 等 30s 再试)"
    fi
done

echo
echo "✅ Formspree 部署完成!"
echo "📧 在 Formspree 后台 https://formspree.io 看订阅数据"
echo "🔍 测试提交: 打开首页或 Blog 索引, 邮箱框填测试邮箱, 点 Subscribe"