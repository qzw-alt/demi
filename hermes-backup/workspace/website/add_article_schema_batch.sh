#!/bin/bash

# 批量为博客文章添加Article Schema

BLOG_DIR="/root/.openclaw/workspace/docs/blog"
cd "$BLOG_DIR"

# 定义文章信息数组
# 格式: "文件名|标题|描述|日期"
declare -a articles=(
    "best-cancer-hospitals-china-2026.html|Best Cancer Hospitals in China 2026|Top-ranked cancer hospitals in China for international patients. Fudan Cancer Center, Sun Yat-sen Cancer Center rankings and specialties.|2026-03-10"
    "best-cardiac-surgery-hospitals-china-2026.html|Best Cardiac Surgery Hospitals in China 2026|Top cardiology hospitals in China. Fuwai Hospital, Zhongshan Hospital rankings for heart surgery.|2026-03-10"
    "bone-marrow-transplant-china.html|Bone Marrow Transplant in China|Complete guide to bone marrow transplant in China. Top hospitals, costs, success rates, and patient experiences.|2026-03-08"
    "cancer-treatment-china-2026.html|Cancer Treatment in China 2026|Comprehensive guide to cancer treatment in China. Top oncology hospitals, costs, and treatment options.|2026-03-10"
    "cancer-treatment-cost-china.html|Cancer Treatment Cost in China|Detailed cost breakdown for cancer treatment in China. Compare prices and save 60-80% on oncology care.|2026-03-08"
    "cataract-surgery-china.html|Cataract Surgery in China|Guide to cataract surgery in China. Top eye hospitals, costs, and recovery information for international patients.|2026-03-09"
    "china-hospital-rankings-2026.html|China Hospital Rankings 2026|Discover China's top-ranked hospitals in 2026. Fudan University rankings for all specialties.|2026-03-03"
    "china-medical-visa-guide-2026.html|China Medical Visa Guide 2026|Step-by-step guide to obtaining a medical visa for China. Requirements and application process.|2026-03-03"
    "china-vs-usa-medical-costs-2026.html|China vs USA Medical Costs 2026|Detailed comparison of medical costs between China and USA. Save 50-85% on healthcare.|2026-03-02"
    "dental-implants-china.html|Dental Implants in China|Complete guide to dental implants in China. Top dental clinics, costs, and quality comparison.|2026-03-08"
    "dental-tourism-china-2026.html|Dental Tourism in China 2026|Guide to dental tourism in China. Save 70% on dental procedures with world-class quality.|2026-03-10"
    "epilepsy-treatment-china.html|Epilepsy Treatment in China|Comprehensive guide to epilepsy treatment in China. Top neurology hospitals and advanced therapies.|2026-03-09"
    "giving-birth-china-american-parents.html|Giving Birth in China for American Parents|Guide for American parents considering giving birth in China. Costs, hospitals, and citizenship options.|2026-03-08"
    "health-checkup-china-2026.html|Health Checkup in China 2026|Premium health checkup packages in China. Comprehensive screening at top hospitals for international patients.|2026-03-10"
    "heart-surgery-cost-china.html|Heart Surgery Cost in China|Complete guide to cardiac surgery costs in China. Save 75-85% on heart procedures.|2026-03-02"
    "hip-replacement-cost-china.html|Hip Replacement Cost in China|Comprehensive guide to hip replacement surgery in China. Compare costs and find top hospitals.|2026-03-02"
    "ivf-fertility-treatment-china.html|IVF and Fertility Treatment in China|Complete guide to IVF and fertility treatment in China. Top clinics, success rates, and costs.|2026-03-08"
    "kidney-dialysis-china.html|Kidney Dialysis in China|Guide to kidney dialysis treatment in China. Top nephrology hospitals and treatment options.|2026-03-09"
    "knee-replacement-cost-china.html|Knee Replacement Cost in China|Complete guide to knee replacement surgery costs in China. Save 70% compared to US prices.|2026-03-02"
    "knee-replacement-surgery-china-2026.html|Knee Replacement Surgery in China 2026|Latest guide to knee replacement surgery in China. Top orthopedic hospitals and recovery tips.|2026-03-16"
    "lasik-eye-surgery-china-2026.html|LASIK Eye Surgery in China 2026|Guide to LASIK and vision correction surgery in China. Top eye hospitals and affordable prices.|2026-03-10"
    "liver-treatment-china.html|Liver Treatment in China|Comprehensive guide to liver disease treatment in China. Top hepatology hospitals and transplant options.|2026-03-09"
    "neurosurgery-brain-tumor-china-2026.html|Neurosurgery and Brain Tumor Treatment in China 2026|Guide to brain tumor surgery in China. Top neurosurgery hospitals with advanced technology.|2026-03-16"
    "neurosurgery-cost-china.html|Neurosurgery Cost in China|Complete guide to neurosurgery costs in China. Brain and spine surgery at top neurology hospitals.|2026-03-08"
    "patient-story-ahmed-liver-transplant.html|Patient Story: Ahmed's Liver Transplant in China|Real patient story of liver transplant surgery in China. Experience, costs, and recovery journey.|2026-03-08"
    "patient-story-david-lung-cancer.html|Patient Story: David's Lung Cancer Treatment in China|Real patient story of lung cancer treatment in China. Journey, costs, and outcomes.|2026-03-08"
    "patient-story-margaret-cataract.html|Patient Story: Margaret's Cataract Surgery in China|Real patient story of cataract surgery in China. Experience and vision restoration results.|2026-03-08"
    "plastic-surgery-china.html|Plastic Surgery in China|Guide to cosmetic surgery in China. Top plastic surgery hospitals and procedures for international patients.|2026-03-08"
    "proton-therapy-china-2026.html|Proton Therapy in China 2026|Guide to proton therapy for cancer treatment in China. Advanced radiation therapy at top centers.|2026-03-10"
    "spine-surgery-cost-china.html|Spine Surgery Cost in China|Complete guide to spine surgery costs in China. Top orthopedic hospitals for back and neck procedures.|2026-03-08"
    "stem-cell-therapy-china-2026.html|Stem Cell Therapy in China 2026|Guide to stem cell therapy and regenerative medicine in China. Top clinics and treatment options.|2026-03-10"
)

# 处理每篇文章
count=0
for article in "${articles[@]}"; do
    IFS='|' read -r filename title desc date <<< "$article"
    
    if [ -f "$filename" ]; then
        # 检查是否已有Schema
        if grep -q "Article Schema" "$filename"; then
            echo "✓ $filename (已存在)"
        else
            # 创建Schema JSON
            schema="    <!-- Article Schema -->\n    <script type=\"application/ld+json\">\n    {\n        \"@context\": \"https://schema.org\",\n        \"@type\": \"Article\",\n        \"headline\": \"$title\",\n        \"description\": \"$desc\",\n        \"image\": \"https://chinahospitalsguide.com/og-image.jpg\",\n        \"author\": {\n            \"@type\": \"Organization\",\n            \"name\": \"China Hospitals Guide\"\n        },\n        \"publisher\": {\n            \"@type\": \"Organization\",\n            \"name\": \"China Hospitals Guide\",\n            \"logo\": {\n                \"@type\": \"ImageObject\",\n                \"url\": \"https://chinahospitalsguide.com/logo.png\"\n            }\n        },\n        \"datePublished\": \"$date\",\n        \"dateModified\": \"$date\",\n        \"mainEntityOfPage\": {\n            \"@type\": \"WebPage\",\n            \"@id\": \"https://chinahospitalsguide.com/blog/$filename\"\n        }\n    }\n    </script>"
            
            # 在</head>前插入Schema
            sed -i "s|</head>|${schema}\n</head>|" "$filename"
            echo "✓ $filename (已添加)"
            ((count++))
        fi
    else
        echo "✗ $filename (文件不存在)"
    fi
done

echo ""
echo "================================"
echo "完成！共添加 $count 篇文章的Schema"
echo "================================"
