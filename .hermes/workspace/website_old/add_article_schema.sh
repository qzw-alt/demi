#!/bin/bash

# 为博客文章添加Article Schema的脚本

BLOG_DIR="/root/.openclaw/workspace/docs/blog"

cd "$BLOG_DIR"

# 定义添加Schema的函数
add_schema() {
    local file=$1
    local title=$2
    local desc=$3
    local date=$4
    
    # 检查是否已有Schema
    if grep -q "Article Schema" "$file"; then
        echo "Skipping $file (already has schema)"
        return
    fi
    
    # 创建Schema JSON
    schema="    <!-- Article Schema -->
    <script type=\"application/ld+json\">
    {
        \"@context\": \"https://schema.org\",
        \"@type\": \"Article\",
        \"headline\": \"$title\",
        \"description\": \"$desc\",
        \"image\": \"https://chinahospitalsguide.com/og-image.jpg\",
        \"author\": {
            \"@type\": \"Organization\",
            \"name\": \"China Hospitals Guide\"
        },
        \"publisher\": {
            \"@type\": \"Organization\",
            \"name\": \"China Hospitals Guide\",
            \"logo\": {
                \"@type\": \"ImageObject\",
                \"url\": \"https://chinahospitalsguide.com/logo.png\"
            }
        },
        \"datePublished\": \"$date\",
        \"dateModified\": \"$date\",
        \"mainEntityOfPage\": {
            \"@type\": \"WebPage\",
            \"@id\": \"https://chinahospitalsguide.com/blog/$file\"
        }
    }
    </script>"
    
    # 在</head>前插入Schema
    sed -i "s|</head>|${schema}\n</head>|" "$file"
    echo "Added schema to $file"
}

# 为每篇文章添加Schema
add_schema "knee-replacement-cost-china.html" "Knee Replacement Cost in China 2026 - Save 70%" "Complete guide to knee replacement surgery costs in China. Save 70% compared to US prices. Top orthopedic hospitals, recovery timeline, and patient experiences." "2026-03-02"

add_schema "hip-replacement-cost-china.html" "Hip Replacement Cost in China 2026 - Save 65-75%" "Comprehensive guide to hip replacement surgery in China. Compare costs, find top hospitals, and learn about recovery. Save 65-75% vs US prices." "2026-03-02"

add_schema "heart-surgery-cost-china.html" "Heart Surgery Cost in China 2026 - Save 75-85%" "Complete guide to cardiac surgery costs in China. Bypass surgery, valve replacement, and angioplasty at top cardiology hospitals. Save 75-85%." "2026-03-02"

add_schema "china-medical-visa-guide-2026.html" "China Medical Visa Guide 2026 - Easy Application" "Step-by-step guide to obtaining a medical visa for China. Requirements, application process, and tips for medical tourists." "2026-03-03"

echo "Schema addition complete!"
