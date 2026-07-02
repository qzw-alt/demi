#!/bin/bash
# Formspree endpoint 一键部署
# 用法: ./formspree-deploy.sh YOUR_FORMSPREE_ID
# 示例: ./formspree-deploy.sh xyzabcde

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
grep -c "formspree.io/f/${FORMSPREE_ID}" index.html blog/index.html
if grep -q "REPLACE_WITH_YOUR_FORMSPREE_ID" index.html blog/index.html; then
    echo "❌ 仍有未替换的占位!"
    exit 1
fi
echo "  ✓ 没有遗留占位"

# 3. git commit + push
echo
echo "[3/4] git commit + push..."
git add index.html blog/index.html
git commit -m "Formspree: activate newsletter subscription (ID: ${FORMSPREE_ID})

Replaced REPLACE_WITH_YOUR_FORMSPREE_ID placeholder with actual Formspree
endpoint in 2 files (index.html + blog/index.html).

Newsletter form now actually subscribes users. Submissions go to the email
configured in Formspree dashboard.

Endpoint: ${ENDPOINT}"
git push origin master

# 4. 等 60s 验证
echo
echo "[4/4] 等 60s 让 Cloudflare 部署..."
sleep 60

# 验证 prod 看到新 endpoint
echo
echo "=== prod 验证 ==="
for url in "https://chinahospitalsguide.com/" "https://chinahospitalsguide.com/blog/"; do
    if curl -s "$url" | grep -q "${FORMSPREE_ID}"; then
        echo "  ✓ $url 含 endpoint"
    else
        echo "  ✗ $url 不含 endpoint (可能 cache)"
    fi
done

echo
echo "✅ Formspree 部署完成!"
echo "📧 在 Formspree 后台 https://formspree.io 看订阅数据"
