#!/usr/bin/env python3
"""
彻底删除表单，替换为邮箱联系
"""
import re

with open('/root/.openclaw/workspace/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 找到表单部分并替换
# 从 <!-- Contact Form --> 到 <!-- Footer -->
pattern = r'(<!-- Contact Form.*?<section class="form-section" id="contact">.*?)(<!-- Footer -->)'

replacement = '''    <!-- Contact Section - 邮箱联系 -->
    <section class="form-section" id="contact">
        <h2>📧 Contact Us</h2>
        <p class="form-subtitle">Free consultation • No obligation • Reply within 24 hours</p>
        
        <div class="form-container" style="text-align: center; max-width: 600px;">
            <div style="padding: 40px 20px;">
                <div style="font-size: 4rem; margin-bottom: 20px;">✉️</div>
                <h3 style="color: #1e3c72; margin-bottom: 15px; font-size: 1.5rem;">Send us an email</h3>
                <p style="color: #666; margin-bottom: 25px; line-height: 1.6;">
                    Tell us about your medical needs and we'll get back to you with personalized recommendations within 24 hours.
                </p>
                
                <a href="mailto:motionlessbottle950@agentmail.to" style="display: inline-block; background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); color: white; padding: 18px 40px; border-radius: 30px; text-decoration: none; font-weight: bold; font-size: 1.1rem; margin-bottom: 30px;">
                    📧 motionlessbottle950@agentmail.to
                </a>
                
                <div style="background: #f8f9fa; padding: 25px; border-radius: 10px; text-align: left; margin-top: 20px;">
                    <h4 style="color: #333; margin-bottom: 15px;">Please include in your email:</h4>
                    <ul style="color: #666; line-height: 1.8; padding-left: 20px;">
                        <li>Your medical condition or treatment needed</li>
                        <li>Preferred city (Beijing/Shanghai/Guangzhou/Shenzhen)</li>
                        <li>Estimated timeline for treatment</li>
                        <li>Your country/region</li>
                    </ul>
                </div>
                
                <p style="color: #999; margin-top: 25px; font-size: 0.9rem;">
                    🔒 Your information is secure and will never be shared with third parties.
                </p>
            </div>
        </div>
    </section>
    
    <!-- Footer -->'''

# 使用更精确的方法：找到特定标记之间的内容
start_marker = '<!-- Contact Form'
end_marker = '<!-- Footer -->'

start_idx = content.find(start_marker)
end_idx = content.find(end_marker)

if start_idx != -1 and end_idx != -1:
    new_content = content[:start_idx] + replacement + content[end_idx + len(end_marker):]
    
    # 同时删除表单相关的JavaScript
    js_start = new_content.find('<script>')
    js_end = new_content.find('</script>', js_start)
    
    if js_start != -1 and js_end != -1 and 'inquiryForm' in new_content[js_start:js_end]:
        new_content = new_content[:js_start] + new_content[js_end + 9:]
    
    with open('/root/.openclaw/workspace/index.html', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("✅ Successfully replaced form with email contact")
else:
    print(f"❌ Could not find markers: start={start_idx}, end={end_idx}")
