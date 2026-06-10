#!/bin/bash

# 为博客文章添加BreadcrumbList Schema

BLOG_DIR="/root/.openclaw/workspace/docs/blog"
cd "$BLOG_DIR"

# 获取所有HTML文件（排除index.html）
for file in *.html; do
    if [ "$file" = "index.html" ]; then
        continue
    fi
    
    # 从文件名提取文章名（去掉.html）
    article_name=$(echo "$file" | sed 's/.html$//' | sed 's/-/ /g' | sed 's/\b\w/\u&/g')
    
    # 检查是否已有BreadcrumbList Schema
    if grep -q "BreadcrumbList Schema" "$file"; then
        echo "✓ $file (已存在)"
        continue
    fi
    
    # 检查是否有</head>标签
    if ! grep -q "</head>" "$file"; then
        echo "✗ $file (无</head>标签)"
        continue
    fi
    
    # 创建BreadcrumbList Schema
    schema="    <!-- BreadcrumbList Schema -->\n    <script type=\"application/ld+json\">\n    {\n        \"@context\": \"https://schema.org\",\n        \"@type\": \"BreadcrumbList\",\n        \"itemListElement\": [\n            {\n                \"@type\": \"ListItem\",\n                \"position\": 1,\n                \"name\": \"Home\",\n                \"item\": \"https://chinahospitalsguide.com/\"\n            },\n            {\n                \"@type\": \"ListItem\",\n                \"position\": 2,\n                \"name\": \"Blog\",\n                \"item\": \"https://chinahospitalsguide.com/blog/\"\n            },\n            {\n                \"@type\": \"ListItem\",\n                \"position\": 3,\n                \"name\": \"$article_name\",\n                \"item\": \"https://chinahospitalsguide.com/blog/$file\"\n            }\n        ]\n    }\n    </script>"
    
    # 在</head>前插入Schema
    sed -i "s|</head>|${schema}\n</head>|" "$file"
    echo "✓ $file (已添加)"
done

echo ""
echo "================================"
echo "博客文章Breadcrumb Schema完成"
echo "================================"
