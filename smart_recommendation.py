#!/usr/bin/env python3
"""
智能推荐邮件系统 - 根据客户需求匹配医院并发送推荐
"""

# 医院推荐数据库
HOSPITAL_DATABASE = {
    "眼科": {
        "北京": [
            {
                "name": "北京同仁医院",
                "rank": "全国第1",
                "specialty": "近视手术、白内障、青光眼",
                "feature": "眼科专科百年历史，年手术量超10万例",
                "price": "$3,000-8,000",
                "wait": "3-7天"
            }
        ],
        "上海": [
            {
                "name": "复旦大学附属眼耳鼻喉科医院",
                "rank": "全国前3",
                "specialty": "近视激光、眼底病",
                "feature": "国际领先的眼科设备",
                "price": "$3,500-9,000",
                "wait": "5-10天"
            }
        ],
        "广州": [
            {
                "name": "中山大学中山眼科中心",
                "rank": "全国前3",
                "specialty": "角膜移植、近视防控",
                "feature": "亚洲最大眼科中心",
                "price": "$2,500-7,000",
                "wait": "5-10天"
            }
        ]
    },
    "心血管": {
        "北京": [
            {
                "name": "中国医学科学院阜外医院",
                "rank": "全国第1",
                "specialty": "心脏搭桥、瓣膜置换",
                "feature": "年心脏手术量15,000+例，世界最大心脏中心",
                "price": "$10,000-20,000",
                "wait": "1-2周"
            },
            {
                "name": "首都医科大学附属北京安贞医院",
                "rank": "全国前3",
                "specialty": "心脏瓣膜、先心病",
                "feature": "心脏瓣膜手术量全国第一",
                "price": "$8,000-18,000",
                "wait": "1-2周"
            }
        ],
        "上海": [
            {
                "name": "复旦大学附属中山医院",
                "rank": "全国第2",
                "specialty": "冠心病、心律失常",
                "feature": "葛均波院士团队，微创介入领先",
                "price": "$8,000-18,000",
                "wait": "1-2周"
            }
        ],
        "广州": [
            {
                "name": "广东省人民医院",
                "rank": "全国前5",
                "specialty": "冠心病介入、心衰",
                "feature": "华南最大心血管病中心",
                "price": "$7,000-15,000",
                "wait": "1周"
            }
        ]
    },
    "骨科": {
        "北京": [
            {
                "name": "北京积水潭医院",
                "rank": "全国第1",
                "specialty": "关节置换、创伤骨科",
                "feature": "骨科专科全国第一，年关节置换8000+例",
                "price": "$8,000-15,000",
                "wait": "1-2周"
            },
            {
                "name": "北京大学第三医院",
                "rank": "全国前5",
                "specialty": "运动医学、脊柱",
                "feature": "运动员指定医院，运动损伤权威",
                "price": "$7,000-14,000",
                "wait": "1-2周"
            }
        ],
        "上海": [
            {
                "name": "上海交通大学医学院附属第九人民医院",
                "rank": "全国前3",
                "specialty": "关节置换、骨科康复",
                "feature": "关节外科领先，术后康复体系完善",
                "price": "$8,000-16,000",
                "wait": "1-2周"
            },
            {
                "name": "上海市第六人民医院",
                "rank": "全国前5",
                "specialty": "创伤骨科、断肢再植",
                "feature": "世界首例断肢再植诞生地",
                "price": "$7,000-14,000",
                "wait": "1周"
            }
        ]
    }
}

def generate_recommendation_email(specialty, city, customer_name=""):
    """生成推荐邮件"""
    
    # 匹配医院
    hospitals = []
    for spec_key, cities in HOSPITAL_DATABASE.items():
        if spec_key in specialty:
            if city in cities:
                hospitals = cities[city]
                break
    
    # 如果没有匹配到，使用默认
    if not hospitals:
        hospitals = [{
            "name": "北京协和医院" if "北京" in city else "上海交通大学医学院附属瑞金医院",
            "rank": "全国顶级",
            "specialty": "综合诊疗",
            "feature": "综合实力强，国际部服务完善",
            "price": "根据病情评估",
            "wait": "1-2周"
        }]
    
    # 构建邮件内容
    hospital_info = ""
    for i, h in enumerate(hospitals[:2], 1):
        hospital_info += f"""
{i}. 🏥 **{h['name']}**
   • 排名：{h['rank']}
   • 专长：{h['specialty']}
   • 特色：{h['feature']}
   • 费用：{h['price']}
   • 等待：{h['wait']}
"""
    
    email_body = f"""Hi {customer_name},

Thank you for providing your medical needs! Based on your requirements ({specialty} in {city}), here are our top hospital recommendations:

{hospital_info}

---

📋 **Want More Details?**

Get our **Starter Guide ($30)** which includes:
• Detailed hospital comparison charts
• Doctor profiles and credentials
• Step-by-step treatment process
• Cost breakdown and payment options
• Visa and travel requirements

👉 [Purchase Starter Guide - $30]

---

💼 **Need Full Support?**

Our **Standard Package ($299)** includes everything in the Starter Guide PLUS:
• Hospital appointment scheduling
• Medical record translation
• Pre-arrival consultation
• Airport pickup coordination
• 24/7 concierge support

👉 [Purchase Standard Package - $299]

---

⏰ **Next Steps:**

Reply to this email if you have questions about these hospitals, or click the links above to purchase our services.

For urgent inquiries, WhatsApp us: **+44 7947 060056**

Best regards,
**Demi (德米)**
China Hospitals Guide Team
"""
    
    return email_body

# 测试
if __name__ == "__main__":
    print(generate_recommendation_email("眼科", "北京", "John"))
