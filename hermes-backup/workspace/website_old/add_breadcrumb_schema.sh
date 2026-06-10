#!/bin/bash

# 为页面添加BreadcrumbList Schema

WORKSPACE="/root/.openclaw/workspace/docs"

# 定义页面和面包屑路径
declare -a pages=(
    "hospitals.html|Hospitals|https://chinahospitalsguide.com/hospitals.html"
    "cost-comparison.html|Cost Comparison|https://chinahospitalsguide.com/cost-comparison.html"
    "pricing.html|Pricing|https://chinahospitalsguide.com/pricing.html"
    "contact.html|Contact|https://chinahospitalsguide.com/contact.html"
    "stories.html|Patient Stories|https://chinahospitalsguide.com/stories.html"
)

for page_info in "${pages[@]}"; do
    IFS='|' read -r filename name url <<< "$page_info"
    filepath="$WORKSPACE/$filename"
    
    if [ -f "$filepath" ]; then
        # 检查是否已有BreadcrumbList Schema
        if grep -q "BreadcrumbList Schema" "$filepath"; then
            echo "✓ $filename (已存在)"
        else
            # 创建BreadcrumbList Schema
            schema="    <!-- BreadcrumbList Schema -->\n    <script type=\"application/ld+json\">\n    {\n        \"@context\": \"https://schema.org\",\n        \"@type\": \"BreadcrumbList\",\n        \"itemListElement\": [\n            {\n                \"@type\": \"ListItem\",\n                \"position\": 1,\n                \"name\": \"Home\",\n                \"item\": \"https://chinahospitalsguide.com/\"\n            },\n            {\n                \"@type\": \"ListItem\",\n                \"position\": 2,\n                \"name\": \"$name\",\n                \"item\": \"$url\"\n            }\n        ]\n    }\n    </script>"
            
            # 在</head>前插入Schema
            sed -i "s|</head>|${schema}\n</head>|" "$filepath"
            echo "✓ $filename (已添加)"
        fi
    else
        echo "✗ $filename (文件不存在)"
    fi
done

echo ""
echo "================================"
echo "BreadcrumbList Schema 添加完成"
echo "================================"
