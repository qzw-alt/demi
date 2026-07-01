#!/usr/bin/env node
/**
 * generate-report.js — Integrated Hospital Report Generator
 *
 * Auto-matches hospitals from keywords, generates pricing comparison,
 * and wraps everything in a warm, complete patient report.
 *
 * Usage:
 *   Quick match:     node generate-report.js "knee replacement"
 *   With city:       node generate-report.js "knee replacement" Beijing
 *   Premium report:  node generate-report.js --name "John Smith" --case "knee replacement" --city Beijing
 *   Basic US:        node generate-report.js --name "Maria" --case "knee replacement" --basic
 *
 * Output: reports/report-{name-or-keywords}-{timestamp}.html
 */

const fs = require("fs");
const path = require("path");

// ========== DATA ==========
const KEYWORD_TAG_MAP = {
  "心脏":["cardiology","heart-surgery"],"心血管":["cardiology","heart-surgery"],
  "搭桥":["cardiology","heart-surgery"],"支架":["cardiology"],
  "heart":["cardiology","heart-surgery"],"cardiac":["cardiology","heart-surgery"],
  "bypass":["cardiology","heart-surgery"],"stent":["cardiology"],
  "骨科":["orthopedics","joint-replacement","spine-surgery","sports-medicine"],
  "关节":["orthopedics","joint-replacement"],"膝关节":["orthopedics","joint-replacement"],
  "髋关节":["orthopedics","joint-replacement"],"脊柱":["orthopedics","spine-surgery"],
  "orthopedic":["orthopedics","joint-replacement"],"joint":["orthopedics","joint-replacement"],
  "knee":["orthopedics","joint-replacement"],"hip":["orthopedics","joint-replacement"],
  "spine":["orthopedics","spine-surgery"],
  "神经外科":["neurosurgery","neurology"],"脑":["neurosurgery"],
  "neurosurgery":["neurosurgery","neurology"],"brain":["neurosurgery"],"neuro":["neurosurgery","neurology"],
  "肿瘤":["oncology","cancer-surgery","radiotherapy"],"癌症":["oncology","cancer-surgery","radiotherapy"],
  "cancer":["oncology","cancer-surgery","radiotherapy"],"tumor":["oncology","cancer-surgery"],
  "oncology":["oncology","cancer-surgery"],"proton":["oncology","radiotherapy"],
  "眼科":["ophthalmology","lasik","cataract"],"白内障":["ophthalmology","cataract"],
  "近视":["ophthalmology","lasik"],"eye":["ophthalmology"],"cataract":["ophthalmology","cataract"],
  "lasik":["ophthalmology","lasik"],
  "试管":["fertility","maternity"],"生殖":["fertility","maternity","obstetrics"],
  "ivf":["fertility","maternity"],"fertility":["fertility","maternity"],
  "血液":["hematology"],"白血病":["hematology"],"blood":["hematology"],"leukemia":["hematology"],
  "牙科":["dental","oral-surgery","cosmetic-dental"],"dental":["dental","oral-surgery"],"teeth":["dental","oral-surgery"],
  "肝":["general"],"liver":["general"],
  "肾":["kidney-disease"],"kidney":["kidney-disease"],
  "消化":["gastroenterology"],"肠胃":["gastroenterology"],"gastro":["gastroenterology"],
  "呼吸":["respiratory"],"肺":["respiratory"],"lung":["respiratory"],"respiratory":["respiratory"],
  "泌尿":["urology"],"urology":["urology"],
  "胡桃夹":["thoracic-surgery","general"],"nutcracker":["thoracic-surgery","general"],
  "胸外科":["thoracic-surgery"],"thoracic":["thoracic-surgery"],
  "血管":["cardiology","general"],"vascular":["cardiology","general"],
  "儿科":["pediatrics","childrens-health"],"儿童":["pediatrics","childrens-health"],
  "整形":["plastic-surgery"],"plastic":["plastic-surgery"],"cosmetic":["plastic-surgery"],
  "中医":["tcm"],"tcm":["tcm"],
  "综合":["general","all-specialties"],"全科":["general","all-specialties"],
  "general":["general","all-specialties"],
};

const PRICE_DB = {
  "膝关节置换":{cn:"$8,000 - $12,000",us:"$35,000 - $50,000",save:"70%"},
  "knee":{cn:"$8,000 - $12,000",us:"$35,000 - $50,000",save:"70%"},
  "髋关节置换":{cn:"$9,000 - $14,000",us:"$50,000+",save:"65%"},
  "hip":{cn:"$9,000 - $14,000",us:"$50,000+",save:"65%"},
  "脊柱":{cn:"$12,000 - $25,000",us:"$80,000+",save:"65%"},
  "spine":{cn:"$12,000 - $25,000",us:"$80,000+",save:"65%"},
  "心脏搭桥":{cn:"$15,000 - $25,000",us:"$100,000 - $200,000",save:"80%"},
  "bypass":{cn:"$15,000 - $25,000",us:"$100,000 - $200,000",save:"80%"},
  "valve":{cn:"$18,000 - $30,000",us:"$150,000 - $300,000",save:"80%"},
  "心脏":{cn:"$15,000 - $25,000",us:"$100,000 - $200,000",save:"80%"},
  "heart":{cn:"$15,000 - $25,000",us:"$100,000 - $200,000",save:"80%"},
  "cardiac":{cn:"$15,000 - $25,000",us:"$100,000 - $200,000",save:"80%"},
  "癌症":{cn:"$15,000 - $50,000",us:"$100,000 - $300,000",save:"70%"},
  "cancer":{cn:"$15,000 - $50,000",us:"$100,000 - $300,000",save:"70%"},
  "肿瘤":{cn:"$15,000 - $50,000",us:"$100,000 - $300,000",save:"70%"},
  "质子":{cn:"$25,000 - $40,000",us:"$150,000+",save:"75%"},
  "proton":{cn:"$25,000 - $40,000",us:"$150,000+",save:"75%"},
  "脑":{cn:"$15,000 - $30,000",us:"$100,000+",save:"75%"},
  "brain":{cn:"$15,000 - $30,000",us:"$100,000+",save:"75%"},
  "neurosurgery":{cn:"$15,000 - $30,000",us:"$100,000+",save:"75%"},
  "ivf":{cn:"$6,000 - $12,000",us:"$25,000+",save:"65%"},
  "试管":{cn:"$6,000 - $12,000",us:"$25,000+",save:"65%"},
  "fertility":{cn:"$6,000 - $12,000",us:"$25,000+",save:"65%"},
  "骨髓移植":{cn:"$30,000 - $60,000",us:"$200,000+",save:"75%"},
  "bone marrow":{cn:"$30,000 - $60,000",us:"$200,000+",save:"75%"},
  "dental":{cn:"¥8,000 - ¥25,000 / 颗",us:"$3,000 - $5,000 / 颗",save:"60%"},
  "种植牙":{cn:"¥8,000 - ¥25,000 / 颗",us:"$3,000 - $5,000 / 颗",save:"60%"},
  "白内障":{cn:"$1,500 - $3,000",us:"$5,000+",save:"60%"},
  "cataract":{cn:"$1,500 - $3,000",us:"$5,000+",save:"60%"},
  "lasik":{cn:"$1,000 - $2,000",us:"$4,000+",save:"65%"},
  "肝移植":{cn:"$30,000 - $60,000",us:"$300,000+",save:"80%"},
  "liver":{cn:"$30,000 - $60,000",us:"$300,000+",save:"80%"},
  "肾移植":{cn:"$25,000 - $50,000",us:"$250,000+",save:"80%"},
  "kidney":{cn:"$25,000 - $50,000",us:"$250,000+",save:"80%"},
};

const CITY_MAP = {
  "北京":"Beijing","上海":"Shanghai","广州":"Guangzhou","深圳":"Shenzhen",
  "成都":"Chengdu","杭州":"Hangzhou","天津":"Tianjin","西安":"Xi'an",
  "南京":"Nanjing","济南":"Jinan",
};

function esc(s) { return String(s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/\"/g,"&quot;"); }

function parseCSVLine(line) {
  const r=[]; let c="", q=false;
  for(let i=0;i<line.length;i++){const ch=line[i];if(ch==='"')q=!q;else if(ch===','&&!q){r.push(c.trim());c="";}else c+=ch;}
  r.push(c.trim()); return r;
}

function loadHospitals(csvPath) {
  const text = fs.readFileSync(csvPath,"utf-8").replace(/^\uFEFF/,"");
  const lines = text.trim().split("\n");
  const headers = lines[0].split(",").map(h=>h.trim());
  return lines.slice(1).map(line=>{
    const cols=parseCSVLine(line);
    const obj={};
    headers.forEach((h,i)=>{obj[h]=(cols[i]||"").trim();});
    obj.Tags=obj.Tags?obj.Tags.split(",").map(t=>t.trim().toLowerCase()):[];
    obj.Trust_Score=parseFloat(obj.Trust_Score)||0;
    return obj;
  });
}

function splitChineseTokens(keywords) {
  const r=[]; for(const kw of keywords){r.push(kw);if(/^[\u4e00-\u9fff]+$/.test(kw)&&kw.length>=3){for(let i=0;i<=kw.length-2;i++){const sub=kw.substring(i,i+2);if(KEYWORD_TAG_MAP[sub])r.push(sub);}}}return [...new Set(r)];
}

function matchTags(keywords, hospitalTags) {
  let score=0; const matched=[];
  for(const kw of keywords){const kl=kw.toLowerCase();if(KEYWORD_TAG_MAP[kl]){for(const tt of KEYWORD_TAG_MAP[kl]){if(hospitalTags.includes(tt)){score+=2;if(!matched.includes(tt))matched.push(tt);}}}if(hospitalTags.includes(kl)){score+=3;if(!matched.includes(kl))matched.push(kl);}}
  return {score,matched};
}

function findPrice(keywords) {
  for(const kw of keywords){const kl=kw.toLowerCase();for(const [pk,pv] of Object.entries(PRICE_DB)){if(kl.includes(pk.toLowerCase())||pk.toLowerCase().includes(kl))return pv;}}
  return null;
}

function screenHospitals(hospitals, keywords, cityFilter=null, minTrust=0.75) {
  const results=[];
  for(const h of hospitals){if(cityFilter&&h.City.toLowerCase()!==cityFilter.toLowerCase())continue;if(h.Trust_Score<minTrust)continue;const {score,matched}=matchTags(keywords,h.Tags);if(score>0)results.push({hospital:h,score,matched_tags:matched});}
  results.sort((a,b)=>(b.score+b.hospital.Trust_Score*2)-(a.score+a.hospital.Trust_Score*2));
  return results;
}

function generateTextReport(results, keywords, city, budget) {
  city=city||"No limit"; const priceInfo=findPrice(keywords);
  const now=new Date().toISOString().slice(0,16).replace("T"," ");
  let out="";
  out+="=".repeat(60)+"\n";
  out+="  China Hospitals Guide — Personalized Hospital Report\n";
  out+="=".repeat(60)+"\n";
  out+="  Generated: "+now+"\n";
  out+="  Condition: "+keywords.join(", ")+"\n";
  out+="  City: "+city+"\n";
  if(budget)out+="  Budget: "+budget+"\n";
  out+="  Matched: "+results.length+" hospitals\n\n";
  if(priceInfo){out+="[PRICE REFERENCE]\n  China: "+priceInfo.cn+"\n  US/UK: "+priceInfo.us+"\n  Save: "+priceInfo.save+"\n\n";}
  out+="[RECOMMENDED HOSPITALS]\n";
  results.forEach((r,i)=>{
    const h=r.hospital;
    out+="\n"+(i+1)+". "+h.Name_ZH+" ("+h.Name_EN+")\n";
    out+="   City: "+h.City+" | "+h.Rank+"\n";
    out+="   Phone: "+h.Phone+"\n";
    out+="   Website: "+h.Website+"\n";
    out+="   Address: "+h.Address+"\n";
  });
  out+="\n"+"=".repeat(60)+"\n";
  out+="  chinahospitalsguide.com | Prices are estimates\n";
  out+="=".repeat(60)+"\n";
  return out;
}

// ========== WARM CONTENT (新增) ==========
function generateCoverLetter(name) {
  if (!name) return '';
  return `
    <div class="card">
      <div class="card-title">🌿 一封写给你的信</div>
      <div style="background:#f8faff;border-radius:14px;padding:28px;border:1px solid #e0e8f2;">
        <p>你好，${esc(name)}，</p>
        <p style="margin-top:12px;">感谢你选择 China Hospitals Guide。</p>
        <p style="margin-top:12px;">我们知道，读到这份报告的时候，你心里装的不是"排名第几"的问题——而是更真实的那些：</p>
        <ul style="margin-top:12px;padding-left:20px;">
          <li><strong>"我去了中国，真的有人接我吗？"</strong></li>
          <li><strong>"医生能跟我直接沟通吗？"</strong></li>
          <li><strong>"如果出了问题，谁帮我协调？"</strong></li>
          <li><strong>"在一个陌生的国家住院几周，我应付得来吗？"</strong></li>
        </ul>
        <p style="margin-top:12px;">这份报告，就是为了回答这些真实的问题而写的。</p>
        <p style="margin-top:12px;">我们根据你的病情，从全国51家顶级医院中筛选出了最适合你的医院。每一家都附上了详细的信息和就诊指导。</p>
        <p style="margin-top:12px;">如果你读完还有任何担心的问题——哪怕是很小的，"医院附近有没有清真餐厅"、"周末能不能做检查"——都欢迎随时问我们。</p>
        <p style="margin-top:16px;">祝你早日康复。</p>
        <p><strong>—— China Hospitals Guide 团队</strong></p>
      </div>
    </div>`;
}

function generateHowToUse() {
  return `
    <div class="card">
      <div class="card-title">📖 如何使用这份报告</div>
      <table style="width:100%;border-collapse:collapse;margin:12px 0;font-size:0.9rem;">
        <tr><th style="padding:10px 12px;border:1px solid #e5eaf1;background:#f8faff;font-weight:600;color:#1e3c72;width:60px;">步骤</th><th style="padding:10px 12px;border:1px solid #e5eaf1;background:#f8faff;font-weight:600;color:#1e3c72;">做什么</th></tr>
        <tr><td style="padding:10px 12px;border:1px solid #e5eaf1;">第1步</td><td style="padding:10px 12px;border:1px solid #e5eaf1;">下面是根据你的情况筛选的推荐医院</td></tr>
        <tr><td style="padding:10px 12px;border:1px solid #e5eaf1;">第2步</td><td style="padding:10px 12px;border:1px solid #e5eaf1;">看看每家医院的"一句话性格"和关键信息</td></tr>
        <tr><td style="padding:10px 12px;border:1px solid #e5eaf1;">第3步</td><td style="padding:10px 12px;border:1px solid #e5eaf1;">对照你的病情和预算，选择1-2家联系</td></tr>
        <tr><td style="padding:10px 12px;border:1px solid #e5eaf1;">第4步</td><td style="padding:10px 12px;border:1px solid #e5eaf1;">参考交通指南，开始规划行程</td></tr>
        <tr><td style="padding:10px 12px;border:1px solid #e5eaf1;">第5步</td><td style="padding:10px 12px;border:1px solid #e5eaf1;">如需深入帮助，查看升级服务</td></tr>
      </table>
    </div>`;
}

function generateFAQ(isPremium) {
  return `
    <div class="card">
      <div class="card-title">❓ 常见问题</div>
      <div class="faq-item">
        <h3>Q: 我不会说中文，在医院怎么沟通？</h3>
        <p>中国顶尖医院的国际部都配备双语协调员。许多资深医生有海外培训经历，能用英语交流。手机翻译app可辅助日常沟通。</p>
      </div>
      <div class="faq-item">
        <h3>Q: 费用和我的国家相比怎么样？</h3>
        <p>详见上面的价格对比。总体而言，在中国顶级医院治疗的费用比美国/英国同等品质的服务节省 60-80%。</p>
      </div>
      <div class="faq-item">
        <h3>Q: 如果回国后出现并发症怎么办？</h3>
        <p>出院时你会收到中英双语病历摘要。${isPremium ? '我们的服务包含远程随访协调，你可随时与主治医生保持联系。' : '许多医院支持通过微信或邮件进行远程随访。'}</p>
      </div>
      <div class="faq-item">
        <h3>Q: 我可以用信用卡支付吗？</h3>
        <p>大多数医院的国际部接受 Visa/Mastercard。我们建议来中国前下载支付宝并绑定你的国际信用卡——中国基本已实现无现金化。</p>
      </div>
      <div class="faq-item">
        <h3>Q: 我的家人可以陪同吗？</h3>
        <p>可以，1-2名家属可以陪同。所有主要医院附近都有酒店和短租公寓。</p>
      </div>
      ${isPremium ? '' : `
      <div class="faq-item">
        <h3>Q: 这份报告和 ¥399 的升级版有什么区别？</h3>
        <p>这份 ¥49 报告给你精准的医院推荐。¥399 升级版提供全程协调服务——代发病历、翻译、跟进、接机、治疗期间协调、出院文件整理、回国后随访衔接。</p>
      </div>
      `}
    </div>`;
}

function generateServiceFlow(isPremium) {
  if (!isPremium) return '';
  return `
    <div class="card" id="pricing">
      <div class="card-title">🚀 我们的服务流程</div>
      <p style="margin-bottom:16px;">以下是购买升级版（¥399）后，我们将为你做的事情：</p>

      <div style="margin:16px 0;padding:14px 18px;background:#f8faff;border-radius:10px;font-size:0.88rem;">
        <p><strong>费用说明：</strong></p>
        <p><span class="tag-inc" style="display:inline-block;background:#d1fae5;color:#065f46;padding:1px 8px;border-radius:4px;font-size:0.72rem;font-weight:600;">✅ ¥399 已包含</span> — 无需额外付费</p>
        <p><span class="tag-ext" style="display:inline-block;background:#fef3c7;color:#92400e;padding:1px 8px;border-radius:4px;font-size:0.72rem;font-weight:600;">💰 需额外付费</span> — 按实际产生的服务收费</p>
        <p style="margin-top:6px;"><strong>🏥 医院治疗费用直接付给医院，不经我们手。</strong></p>
      </div>

      <h3 style="font-size:1rem;color:var(--primary);margin:20px 0 10px;">第1步：需求确认（1-2天）</h3>
      <p style="font-size:0.88rem;color:#555;"><strong>你做什么：</strong> 告诉我们病情和需求，提供已有病历资料。</p>
      <p style="font-size:0.88rem;color:#555;"><strong>我们做什么：</strong></p>
      <ul style="font-size:0.88rem;color:#555;padding-left:20px;margin-bottom:10px;">
        <li><span class="tag-inc">✅ ¥399 已包含</span> 一对一顾问对接，了解你的具体情况</li>
        <li><span class="tag-inc">✅ ¥399 已包含</span> 从51家医院中筛选最适合你的2-3家</li>
        <li><span class="tag-inc">✅ ¥399 已包含</span> 如不满意，重新匹配</li>
      </ul>
      <p style="font-size:0.85rem;color:var(--text-light);padding:8px 12px;background:#f8faff;border-radius:8px;">📦 你拿到的：双方确认后的最终推荐方案</p>

      <h3 style="font-size:1rem;color:var(--primary);margin:20px 0 10px;">第2步：医院对接（3-7天）</h3>
      <p style="font-size:0.88rem;color:#555;"><strong>你做什么：</strong> 确认选择的医院，提供完整病历和影像资料。</p>
      <p style="font-size:0.88rem;color:#555;"><strong>我们做什么：</strong></p>
      <ul style="font-size:0.88rem;color:#555;padding-left:20px;margin-bottom:10px;">
        <li><span class="tag-inc">✅ ¥399 已包含</span> 翻译整理病历，发送给医院国际部</li>
        <li><span class="tag-inc">✅ ¥399 已包含</span> 跟进评估进度，确保3-7个工作日内拿到回复</li>
        <li><span class="tag-inc">✅ ¥399 已包含</span> 中英文病历翻译协调</li>
        <li><span class="tag-inc">✅ ¥399 已包含</span> 同时对接多家医院，对比评估结果和报价</li>
      </ul>
      <p style="font-size:0.85rem;color:var(--text-light);padding:8px 12px;background:#f8faff;border-radius:8px;">📦 你拿到的：正式收治确认 + 费用估算清单 + 建议治疗时间</p>

      <h3 style="font-size:1rem;color:var(--primary);margin:20px 0 10px;">第3步：行前准备（1-4周）</h3>
      <p style="font-size:0.88rem;color:#555;"><strong>我们做什么：</strong></p>
      <ul style="font-size:0.88rem;color:#555;padding-left:20px;margin-bottom:10px;">
        <li><span class="tag-inc">✅ ¥399 已包含</span> 协调医院出具医疗邀请函，指导签证材料</li>
        <li><span class="tag-inc">✅ ¥399 已包含</span> 锁定具体入院日期</li>
        <li><span class="tag-inc">✅ ¥399 已包含</span> 推荐合适住宿</li>
        <li><span class="tag-inc">✅ ¥399 已包含</span> 行前清单（药品、证件、生活用品）</li>
        <li><span class="tag-inc">✅ ¥399 已包含</span> 接机安排</li>
      </ul>
      <p style="font-size:0.85rem;color:var(--text-light);padding:8px 12px;background:#f8faff;border-radius:8px;">📦 你拿到的：医院邀请函 + 签证材料清单 + 行前准备清单 + 接机确认信息</p>

      <h3 style="font-size:1rem;color:var(--primary);margin:20px 0 10px;">第4步：抵达中国（治疗期间）</h3>
      <ul style="font-size:0.88rem;color:#555;padding-left:20px;margin-bottom:10px;">
        <li><span class="tag-inc">✅ ¥399 已包含</span> 医院沟通衔接，确保治疗按计划进行</li>
        <li><span class="tag-inc">✅ ¥399 已包含</span> 突发问题协调（7×24小时紧急联系电话）</li>
        <li><span class="tag-ext">💰 需额外付费</span> 家属生活协助</li>
      </ul>

      <h3 style="font-size:1rem;color:var(--primary);margin:20px 0 10px;">第5步：出院与回国</h3>
      <ul style="font-size:0.88rem;color:#555;padding-left:20px;margin-bottom:10px;">
        <li><span class="tag-inc">✅ ¥399 已包含</span> 中英双语病历摘要整理</li>
        <li><span class="tag-inc">✅ ¥399 已包含</span> 出院带药说明翻译</li>
        <li><span class="tag-inc">✅ ¥399 已包含</span> 复查预约（如需）</li>
        <li><span class="tag-inc">✅ ¥399 已包含</span> 远程随访衔接——回国后与主治医生保持联系</li>
        <li><span class="tag-ext">💰 需额外付费</span> 回国航旅协助</li>
      </ul>

      <h3 style="font-size:1rem;color:var(--primary);margin:20px 0 10px;">第6步：回国后跟进</h3>
      <ul style="font-size:0.88rem;color:#555;padding-left:20px;margin-bottom:10px;">
        <li><span class="tag-ext">💰 需额外付费</span> 远程随访通道（按年/按次）</li>
        <li><span class="tag-ext">💰 需额外付费</span> 复查资料传递</li>
        <li><span class="tag-ext">💰 需额外付费</span> 长期健康档案</li>
      </ul>
    </div>`;
}

function generateOneLiner(name_zh, rank) {
  const rank_lower = (rank || '').toLowerCase();
  if (rank_lower.includes('#1') || rank_lower.includes('top 3')) return 'Top-tier specialized hospital in China';
  if (rank_lower.includes('top')) return 'Highly ranked, strong reputation in this field';
  return 'Well-regarded hospital with relevant expertise';
}

// ========== TRANSPORT GUIDE ==========
const TRANSPORT_GUIDES = {
  "Beijing": {
    desc: "北京有两个国际机场。首都机场(PEK)在东边——多数医院靠近这个机场。大兴机场(PKX)在南边。预约时问清楚医生在哪个院区，再决定飞哪个。",
    taxi: "PEK→市中心 ¥120-200，PKX→市中心 ¥200-350。建议用滴滴App（英文界面）。",
    metro: "PEK机场线 ¥25 到东直门/三元桥。PKX机场线 ¥35 到草桥。",
    tip: "如果是去协和（东单）、同仁（崇文门），PKX机场线到草桥后打车更近。"
  },
  "Shanghai": {
    desc: "上海有两个机场。浦东(PVG)是主国际机场，距市中心50-70分钟。虹桥(SHA)距市中心20-30分钟。",
    taxi: "PVG→市区 ¥150-250，SHA→市区 ¥50-100。",
    metro: "PVG磁悬浮¥50到龙阳路（7分钟），换2号线到市区。SHA直接坐10号线。",
    tip: "如果可选，优先选飞虹桥的航班。市区三甲医院分布在浦西为主。"
  },
  "Guangzhou": {
    desc: "白云机场(CAN)是唯一主机场，距市中心40-60分钟。",
    taxi: "CAN→市区 ¥120-200。",
    metro: "3号线北延段从机场到体育西路约40分钟。",
    tip: "广州地铁方便，如住宿可选地铁沿线。"
  },
  "Shenzhen": {
    desc: "宝安机场(SZX)是主机场，距市中心35-50分钟。",
    taxi: "SZX→市中心 ¥80-150。",
    metro: "11号线从机场到福田站约30分钟。",
    tip: "深圳地铁覆盖广，建议选地铁附近住宿。"
  },
  "Chengdu": {
    desc: "成都用天府机场(TFU)和双流机场(CTU)。天府是主机场，距市区60-80分钟。双流距市区30-40分钟。",
    taxi: "TFU→市区 ¥150-250，CTU→市区 ¥50-100。",
    metro: "18号线从天府到火车南站约50分钟。双流直接坐10号线。",
    tip: "如果可选，优先选飞双流的航班。华西医院靠近市区。"
  },
  "Xi'an": {
    desc: "咸阳机场(XIY)是唯一机场，距市区50-65分钟。",
    taxi: "XIY→市区 ¥100-150。",
    metro: "14号线转2号线可达市区。",
    tip: "唐都医院在东郊，机场→唐都约50-60分钟，比去市中心近。"
  },
  "Hangzhou": {
    desc: "萧山机场(HGH)距市区40-50分钟。",
    taxi: "HGH→市区 ¥100-180。",
    metro: "1号线/7号线从机场到市区。",
    tip: "杭州地铁方便，医院多在市区。"
  },
  "Tianjin": {
    desc: "滨海机场(TSN)距市区30-50分钟。",
    taxi: "TSN→市区 ¥60-120。",
    metro: "2号线从机场到天津站。",
    tip: "天津到北京高铁30分钟，可选其中任一城市主导治疗。"
  },
  "Nanjing": {
    desc: "禄口机场(NKG)距市区45-60分钟。",
    taxi: "NKG→市区 ¥120-200。",
    metro: "S1号线从机场到南京南站约40分钟。",
    tip: "南京地铁覆盖好，医院多在鼓楼区。"
  },
  "Jinan": {
    desc: "遥墙机场(TNA)距市区40-50分钟。",
    taxi: "TNA→市区 ¥80-120。",
    metro: "无直达地铁。建议打车或预约接机。",
    tip: "济南市内交通以打车为主。"
  }
};

function generateTransportGuide(city) {
  const guide = TRANSPORT_GUIDES[city];
  if (!guide) return '';
  return `
    <div class="card">
      <div class="card-title">✈️ ${esc(city)} 城市交通指南</div>
      <p>${guide.desc}</p>
      <p style="margin-top:8px;"><strong>🚕 出租车/网约车：</strong> ${guide.taxi}</p>
      <p><strong>🚇 地铁：</strong> ${guide.metro}</p>
      <p><strong>💡 提示：</strong> ${guide.tip}</p>
    </div>`;
}

function generateChecklist() {
  return `
    <div class="card">
      <div class="card-title">📋 行前准备清单</div>
      <p style="margin-bottom:12px;">以下是基础清单。如需更详细的指南，可升级到完整协调服务。</p>
      <div style="background:#f8faff;border-radius:10px;padding:16px;font-size:0.88rem;">
        <p><strong>必带的材料：</strong></p>
        <ul style="padding-left:20px;margin:6px 0 12px;">
          <li>原始病历 + 影像资料（CT/MRI光盘或U盘，DICOM格式最佳）</li>
          <li>正在服用的药物（带足量 + 英文说明书）</li>
          <li>护照（有效期6个月以上）</li>
          <li>医院邀请函（用于入境和签证）</li>
          <li>信用卡（Visa/Mastercard）+ 少量人民币现金</li>
          <li>手机开通国际漫游或到达后购买中国电话卡</li>
          <li>转换插头（中国标准：两脚扁型，220V）</li>
        </ul>
        <p><strong>💡 提示：</strong>出发前下载支付宝App，绑定你的国际信用卡——到了中国后，从便利店到药店到餐厅都可以扫码支付，比现金方便百倍。</p>
      </div>
    </div>`;
}

function generateUpgradeSection() {
  return `
    <div class="card">
      <div class="card-title">⭐ 升级服务</div>
      <p style="margin-bottom:12px;">如果你看完上面的医院介绍，觉得"还是不知道怎么开始"，以下是我们的完整协调服务内容：</p>
      <table style="width:100%;border-collapse:collapse;margin:12px 0;font-size:0.88rem;">
        <tr><th style="padding:10px 12px;border:1px solid #e5eaf1;background:#f8faff;font-weight:600;color:#1e3c72;">阶段</th><th style="padding:10px 12px;border:1px solid #e5eaf1;background:#f8faff;font-weight:600;color:#1e3c72;">服务内容</th></tr>
        <tr><td style="padding:10px 12px;border:1px solid #e5eaf1;font-weight:600;">需求确认</td><td style="padding:10px 12px;border:1px solid #e5eaf1;">一对一顾问对接、精准匹配、定制调整</td></tr>
        <tr><td style="padding:10px 12px;border:1px solid #e5eaf1;font-weight:600;">医院对接</td><td style="padding:10px 12px;border:1px solid #e5eaf1;">代发病历、翻译协调、跟进回复、多院对比报价</td></tr>
        <tr><td style="padding:10px 12px;border:1px solid #e5eaf1;font-weight:600;">行前准备</td><td style="padding:10px 12px;border:1px solid #e5eaf1;">签证材料指导、预约锁定、住宿建议、接机安排</td></tr>
        <tr><td style="padding:10px 12px;border:1px solid #e5eaf1;font-weight:600;">治疗期间</td><td style="padding:10px 12px;border:1px solid #e5eaf1;">医院沟通衔接、突发问题协调、紧急联系电话</td></tr>
        <tr><td style="padding:10px 12px;border:1px solid #e5eaf1;font-weight:600;">出院回国</td><td style="padding:10px 12px;border:1px solid #e5eaf1;">中英文病历整理、用药说明、复查预约、远程随访衔接</td></tr>
      </table>
      <p style="font-size:0.88rem;color:var(--primary);font-weight:600;margin-top:8px;">如果你已经确定要来中国治病，希望有人全程帮你搞定——请考虑升级到「Pre-Arrival Coordination（¥399）」。</p>
    </div>`;
}

// ========== INTEGRATED HTML REPORT ==========
function generateHtmlReport(results, keywords, city, budget, opts) {
  city=city||"No limit";
  const priceInfo=findPrice(keywords);
  const dateStr=new Date().toLocaleDateString("en-US",{year:"numeric",month:"long",day:"numeric"});
  const title=keywords.slice(0,3).join(" / ");
  const customerName = opts.name || '';
  const isPremium = opts.premium || false;
  const safeTitle = (opts.name || keywords.slice(0,3).join("-")).toLowerCase().replace(/[^a-z0-9]+/g,'-').replace(/-+/g,'-').replace(/^-|-$/g,'');

  const priceHtml = priceInfo ? `
    <div class="card">
      <div class="card-title">💰 费用对比</div>
      <div style="display:flex;gap:0;border-radius:14px;overflow:hidden;box-shadow:0 2px 10px rgba(0,0,0,0.04);">
        <div style="flex:1;padding:28px 20px;text-align:center;background:linear-gradient(135deg,#e8f5e9,#c8e6c9);">
          <div style="font-size:1.8rem;margin-bottom:4px;">🇨🇳</div>
          <div style="font-size:0.72rem;text-transform:uppercase;letter-spacing:0.06em;font-weight:700;color:#888;margin-bottom:6px;">中国预计成本</div>
          <div style="font-size:1.4rem;font-weight:800;color:var(--primary);">${esc(priceInfo.cn)}</div>
          <div style="font-size:0.78rem;color:#888;margin-top:4px;">世界一流医院</div>
        </div>
        <div style="display:flex;align-items:center;justify-content:center;background:#fff;padding:0 12px;min-width:80px;">
          <div style="width:68px;height:68px;border-radius:50%;background:linear-gradient(135deg,var(--accent),#c0392b);color:#fff;display:flex;flex-direction:column;align-items:center;justify-content:center;font-size:0.65rem;line-height:1.2;text-align:center;">
            节省<br><strong style="font-size:0.9rem;display:block;">${esc(priceInfo.save)}</strong>
          </div>
        </div>
        <div style="flex:1;padding:28px 20px;text-align:center;background:linear-gradient(135deg,#fff3e0,#ffe0b2);">
          <div style="font-size:1.8rem;margin-bottom:4px;">🇺🇸</div>
          <div style="font-size:0.72rem;text-transform:uppercase;letter-spacing:0.06em;font-weight:700;color:#888;margin-bottom:6px;">美国/英国典型成本</div>
          <div style="font-size:1.4rem;font-weight:800;color:var(--primary);">${esc(priceInfo.us)}</div>
          <div style="font-size:0.78rem;color:#888;margin-top:4px;">质量相当</div>
        </div>
      </div>
    </div>` : "";

  const cardsHtml = results.slice(0,3).map((r,i)=>{
    const h=r.hospital;
    const trust=Math.round(h.Trust_Score*100);
    const tc=trust>=90?"#27ae60":trust>=80?"#f39c12":"#e74c3c";
    const badgeLabels = ["🥇 首选推荐","🥈 备选推荐","🥉 第三选择"];
    const badge=i<3?`<div style="display:inline-block;background:linear-gradient(135deg,var(--primary),var(--secondary));color:#fff;padding:4px 14px;border-radius:12px;font-size:0.7rem;font-weight:700;letter-spacing:0.04em;margin-bottom:12px;">${badgeLabels[i]}</div>`:'';
    const intl=h.International==="True"?'<span class="cert intl">🌐 国际部</span>':'';
    const jci=h.JCI==="True"?'<span class="cert jci">✅ JCI 认证</span>':'';
    const oneLiner = generateOneLiner(h.Name_ZH, h.Rank);
    const priceInfo = findPrice(keywords);
    const airportInfo = h.Airport_Info || '暂无数据';
    return `
    <div class="h-card" style="margin-bottom:24px;">
      ${badge}
      <div class="h-name" style="font-size:1.2rem;font-weight:700;color:var(--primary);">${esc(h.Name_ZH)}</div>
      <div class="h-name-en" style="font-size:0.88rem;color:var(--text-light);margin-bottom:8px;">${esc(h.Name_EN)}</div>
      <div style="margin-bottom:14px;padding-left:12px;border-left:3px solid var(--secondary);font-style:italic;color:#555;font-size:0.9rem;">💬 ${esc(oneLiner)}</div>

      <table style="width:100%;border-collapse:collapse;margin:8px 0;font-size:0.88rem;">
        <tr><td style="padding:6px 10px;border:1px solid #e5eaf1;background:#f8faff;font-weight:600;color:#555;width:90px;">排名/评级</td><td style="padding:6px 10px;border:1px solid #e5eaf1;">${esc(h.Rank||'N/A')}</td></tr>
        <tr><td style="padding:6px 10px;border:1px solid #e5eaf1;background:#f8faff;font-weight:600;color:#555;">地址</td><td style="padding:6px 10px;border:1px solid #e5eaf1;">${esc(h.Address||'')}</td></tr>
        <tr><td style="padding:6px 10px;border:1px solid #e5eaf1;background:#f8faff;font-weight:600;color:#555;">电话</td><td style="padding:6px 10px;border:1px solid #e5eaf1;">📞 ${esc(h.Phone||'')}</td></tr>
        <tr><td style="padding:6px 10px;border:1px solid #e5eaf1;background:#f8faff;font-weight:600;color:#555;">网站</td><td style="padding:6px 10px;border:1px solid #e5eaf1;"><a href="${esc(h.Website||'')}" style="color:var(--secondary);">${esc(h.Website||'')}</a></td></tr>
        <tr><td style="padding:6px 10px;border:1px solid #e5eaf1;background:#f8faff;font-weight:600;color:#555;">国际部</td><td style="padding:6px 10px;border:1px solid #e5eaf1;">${intl} ${jci}</td></tr>
        <tr><td style="padding:6px 10px;border:1px solid #e5eaf1;background:#f8faff;font-weight:600;color:#555;">机场交通</td><td style="padding:6px 10px;border:1px solid #e5eaf1;">✈️ ${esc(airportInfo)}</td></tr>
      </table>

      ${priceInfo ? `<div style="margin-top:12px;padding:12px;background:#e8f5e9;border-radius:8px;">
        <p style="font-size:0.9rem;"><strong>💰 费用参考：</strong> 中国约 ${priceInfo.cn} · 美国约 ${priceInfo.us} · 节省 ${priceInfo.save}</p>
      </div>` : ''}

      ${r.matched_tags.length ? `<div style="margin-top:10px;"><span class="h-tag">${r.matched_tags.join('</span><span class="h-tag">')}</span></div>` : ''}
    </div>`;}).join("");

  const extraHtml = results.length > 5 ? `<p style="margin-top:12px;color:#666;">+ ${results.length - 5} more hospitals matched. <a href="#full-list" onclick="document.getElementById('fullList').style.display='block';return false;">Show all</a></p><div id="fullList" style="display:none;">${results.slice(5).map((r,i)=>{const h=r.hospital;return `<p style="padding:4px 0;">${i+6}. ${esc(h.Name_ZH)} — ${esc(h.Rank||'')}</p>`;}).join("")}</div>` : '';

  const textReport = generateTextReport(results, keywords, city);

  const coverHtml = generateCoverLetter(customerName);
  const howToUseHtml = generateHowToUse();
  const transportHtml = generateTransportGuide(city);
  const checklistHtml = generateChecklist();
  const upgradeHtml = isPremium ? '' : generateUpgradeSection();
  const serviceHtml = generateServiceFlow(isPremium);
  const faqHtml = generateFAQ(isPremium);

  const titlePrefix = customerName ? `Your Hospital Report — ${esc(customerName)}` : `Medical Report: ${esc(title)}`;
  const badgeText = isPremium ? '<span class="hero-badge" style="background:#f59e0b;color:#1a1a2e;border-color:#f59e0b;">PREMIUM REPORT</span>' : '<span class="hero-badge">PERSONALIZED MEDICAL REPORT</span>';

  return `<!DOCTYPE html><html lang="zh-CN">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>${esc(titlePrefix)} — China Hospitals Guide</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:wght@600;700&display=swap" rel="stylesheet">
<style>
  :root{--primary:#1a3a6b;--secondary:#2a5298;--accent:#e85d5d;--accent-light:#ff8e8e;--text:#2d3748;--text-light:#718096;--bg:#f7fafc;}
  *{margin:0;padding:0;box-sizing:border-box;}
  body{font-family:'Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;color:var(--text);background:var(--bg);line-height:1.7;}
  .report{max-width:960px;margin:0 auto;}
  .hero{padding:150px 24px 80px;background:linear-gradient(135deg,rgba(12,24,48,0.95),rgba(30,60,114,0.92));color:#fff;text-align:center;position:relative;overflow:hidden;}
  .hero::before{content:'';position:absolute;inset:0;background:url('data:image/svg+xml,<svg width="60" height="60" viewBox="0 0 60 60" xmlns="http://www.w3.org/2000/svg"><circle cx="30" cy="30" r="1" fill="rgba(255,255,255,0.06)"/></svg>') repeat;pointer-events:none;}
  .hero-inner{position:relative;z-index:1;max-width:820px;margin:0 auto;}
  .hero-kicker{display:inline-block;margin-bottom:22px;padding:8px 16px;border-radius:999px;border:1px solid rgba(255,255,255,0.28);background:rgba(255,255,255,0.08);font-size:0.78rem;letter-spacing:0.08em;text-transform:uppercase;}
  .hero h1{font-family:'Playfair Display',Georgia,serif;font-size:clamp(2rem,5vw,3.6rem);font-weight:700;line-height:1.1;margin-bottom:16px;}
  .hero-sub{font-size:1.05rem;color:rgba(255,255,255,0.8);margin-bottom:32px;max-width:560px;margin-left:auto;margin-right:auto;}
  .hero-stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:12px;max-width:640px;margin:0 auto;}
  .hero-stat{background:rgba(255,255,255,0.08);border:1px solid rgba(255,255,255,0.14);border-radius:14px;padding:14px 10px;text-align:center;}
  .hero-stat .stat-label{font-size:0.65rem;text-transform:uppercase;letter-spacing:0.06em;color:rgba(255,255,255,0.6);margin-bottom:4px;}
  .hero-stat .stat-value{font-size:0.95rem;font-weight:600;color:#fff;}
  .hero-badge{display:none;}
  .content{max-width:820px;margin:-32px auto 0;padding:0 16px 48px;}
  .card{background:#fff;border-radius:18px;padding:32px 28px;margin-bottom:20px;box-shadow:0 4px 16px rgba(15,23,42,0.06);border:1px solid rgba(30,60,114,0.07);}
  .card-title{font-family:'Playfair Display',Georgia,serif;font-size:1.15rem;color:var(--primary);margin-bottom:16px;padding-bottom:10px;border-bottom:2px solid #eef2f7;}
  .price-row{display:flex;gap:0;border-radius:14px;overflow:hidden;box-shadow:0 2px 10px rgba(0,0,0,0.04);}
  .price-box{flex:1;padding:28px 20px;text-align:center;}
  .price-box.cn{background:linear-gradient(135deg,#e8f5e9,#c8e6c9);}
  .price-box.us{background:linear-gradient(135deg,#fff3e0,#ffe0b2);}
  .price-flag{font-size:1.8rem;margin-bottom:4px;}
  .price-label{font-size:0.72rem;text-transform:uppercase;letter-spacing:0.06em;font-weight:700;color:#888;margin-bottom:6px;}
  .price-value{font-size:1.4rem;font-weight:800;color:var(--primary);}
  .price-save-wrap{display:flex;align-items:center;justify-content:center;background:#fff;padding:0 12px;min-width:80px;}
  .save-badge{width:68px;height:68px;border-radius:50%;background:linear-gradient(135deg,var(--accent),#c0392b);color:#fff;display:flex;flex-direction:column;align-items:center;justify-content:center;font-size:0.65rem;line-height:1.2;text-align:center;}
  .save-badge strong{font-size:0.9rem;display:block;}
  .h-card{background:#fff;border:1px solid #eef2f7;border-radius:16px;padding:24px;margin-bottom:16px;position:relative;transition:box-shadow .15s;}
  .h-card:hover{box-shadow:0 4px 20px rgba(0,0,0,0.04);}
  .top-pick{position:absolute;top:-10px;right:20px;background:linear-gradient(135deg,var(--primary),var(--secondary));color:#fff;padding:4px 14px;border-radius:12px;font-size:0.7rem;font-weight:700;letter-spacing:0.04em;}
  .top-pick.alt{background:linear-gradient(135deg,#2d7d46,#3a9d5a);}
  .h-name{font-size:1.05rem;font-weight:700;color:var(--primary);}
  .h-name-en{font-size:0.8rem;color:var(--text-light);margin-bottom:10px;}
  .h-tags{margin:10px 0 0;display:flex;flex-wrap:wrap;gap:4px;}
  .h-tag{background:#eef2f7;color:#555;padding:2px 10px;border-radius:4px;font-size:0.76rem;}
  .badge{display:inline-block;padding:2px 10px;border-radius:4px;font-size:0.76rem;margin:0 2px 2px 0;}
  .badge-intl,.cert.intl{background:#e3f2fd;color:#1565c0;}
  .badge-jci,.cert.jci{background:#e8f5e9;color:#2e7d32;}
  .steps{counter-reset:step;}
  .step{position:relative;padding:14px 16px 14px 52px;border-left:3px solid #d1d9e6;margin-bottom:0;}
  .step:last-child{border-color:transparent;}
  .step-num{position:absolute;left:12px;top:12px;width:28px;height:28px;background:var(--primary);color:#fff;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:0.8rem;font-weight:700;}
  .faq-item{padding:16px;margin-bottom:12px;background:#f8faff;border-radius:10px;}
  .faq-item h4{font-size:0.9rem;color:var(--primary);margin-bottom:4px;}
  .faq-item p,.faq-item ul{font-size:0.85rem;color:#555;margin:0;}
  .faq-item ul{padding-left:18px;margin-top:4px;}
  .faq-item li{margin-bottom:2px;}
  .dl-grid{display:grid;grid-template-columns:auto 1fr;gap:4px 18px;font-size:0.88rem;}
  .dl-key{color:var(--text-light);}
  .dl-val{color:var(--text);}
  .dl-val a{color:var(--secondary);text-decoration:none;}
  .tag-inc{display:inline-block;background:#d1fae5;color:#065f46;padding:1px 8px;border-radius:4px;font-size:0.72rem;font-weight:600;}
  .tag-ext{display:inline-block;background:#fef3c7;color:#92400e;padding:1px 8px;border-radius:4px;font-size:0.72rem;font-weight:600;}
  .dl-box{background:#f8faff;border-radius:10px;padding:16px;margin-top:14px;font-size:0.88rem;color:#555;}
  .dl-box p{margin-bottom:6px;}
  .toolbar{position:sticky;top:0;z-index:100;background:rgba(255,255,255,0.92);backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px);border-bottom:1px solid #e5eaf1;padding:10px 20px;display:flex;justify-content:flex-end;gap:10px;}
  .toolbar button{padding:8px 18px;border-radius:8px;border:1px solid #d1d9e6;background:#fff;cursor:pointer;font-size:0.82rem;font-weight:500;color:var(--primary);transition:all .15s;}
  .toolbar button:hover{background:var(--primary);color:#fff;border-color:var(--primary);}
  .toolbar .btn-primary{background:var(--primary);color:#fff;border-color:var(--primary);}
  .toolbar .btn-primary:hover{background:#0f2a4f;}
  .dload-section{text-align:center;padding:32px 20px 24px;background:#fff;border-radius:18px;box-shadow:0 4px 16px rgba(15,23,42,0.06);border:1px solid rgba(30,60,114,0.07);}
  .dload-section p{color:var(--text-light);font-size:0.88rem;margin-bottom:12px;}
  .btn-dload{display:inline-block;background:var(--primary);color:#fff;padding:14px 32px;border-radius:10px;text-decoration:none;font-weight:600;font-size:0.95rem;transition:background .15s;}
  .btn-dload:hover{background:#0f2a4f;}
  .disclaimer{background:#fff8e1;border-left:4px solid #f5a623;padding:14px 18px;border-radius:0 8px 8px 0;font-size:0.8rem;color:#856404;margin-top:20px;}
  .footer{text-align:center;padding:32px 20px;color:var(--text-light);font-size:0.82rem;}
  .footer a{color:var(--primary);text-decoration:none;font-weight:600;}
  .p{margin-bottom:10px;color:var(--text);font-size:0.92rem;}
  .p:last-child{margin-bottom:0;}
  .quote{border-left:3px solid var(--secondary);padding:12px 16px;margin:12px 0;background:#f8faff;border-radius:0 8px 8px 0;font-style:italic;color:#555;font-size:0.9rem;}
  hr{border:none;border-top:1px solid #eef2f7;margin:20px 0;}
  @media(max-width:640px){
    .hero{padding:120px 16px 60px;}
    .hero-inner{padding:0 4px;}
    .hero h1{font-size:1.75rem;}
    .hero-sub{font-size:0.92rem;margin-bottom:24px;}
    .content{padding:0 12px 36px;}
    .card{padding:24px 18px;border-radius:14px;}
    .price-row{flex-direction:column;}
    .price-save-wrap{padding:12px;}
    .dl-grid{grid-template-columns:1fr;}
    .toolbar{justify-content:center;flex-wrap:wrap;}
  }
  @media print{body{background:#fff;}.toolbar{display:none!important;}.hero{-webkit-print-color-adjust:exact;}.h-card{break-inside:avoid;}}
</style>
</head>
<body>
<div class="toolbar">
  <button onclick="window.print()">🖨️ Print / PDF</button>
  <button class="btn-primary" onclick="downloadTxt()">📥 Download Full Report</button>
</div>
<div class="report">
  <div class="hero">
    <div class="hero-inner">
      <div class="hero-kicker">PERSONALIZED MEDICAL REPORT</div>
      <h1>${esc(customerName ? `Your Medical Travel Report` : `Medical Travel Report: ${esc(title)}`)}</h1>
      <p class="hero-sub">${customerName ? `Personalized report for ${esc(customerName)}` : 'Hospital matching and cost comparison for your condition'}</p>
      <div class="hero-stats">
        ${customerName ? `<div class="hero-stat"><div class="stat-label">PATIENT</div><div class="stat-value">${esc(customerName)}</div></div>` : ''}
        <div class="hero-stat"><div class="stat-label">CONDITION</div><div class="stat-value">${esc(keywords.join(', '))}</div></div>
        ${city && city !== 'No limit' ? `<div class="hero-stat"><div class="stat-label">CITY</div><div class="stat-value">${esc(city)}</div></div>` : ''}
        <div class="hero-stat"><div class="stat-label">MATCHED</div><div class="stat-value">${results.length} hospitals</div></div>
        <div class="hero-stat"><div class="stat-label">REPORT DATE</div><div class="stat-value">${dateStr}</div></div>
      </div>
    </div>
  </div>
  <div class="content">
    <!-- Cover letter -->
    ${coverHtml}

    <!-- How to use -->
    ${howToUseHtml}

    <!-- Price comparison -->
    ${priceHtml ? `${priceHtml}` : ''}

    <!-- Hospital cards -->
    <div class="card">
      <div class="card-title">🏆 推荐医院（共${results.length}家）</div>
      ${cardsHtml}
      ${extraHtml}
    </div>

    <!-- Transport guide -->
    ${transportHtml}

    <!-- Pre-departure checklist -->
    ${checklistHtml}

    <!-- Upgrade section (basic only) -->
    ${upgradeHtml}

    <!-- Service flow (premium only) -->
    ${serviceHtml}

    <!-- FAQ -->
    ${faqHtml}

    <!-- Download section -->
    <div class="dload-section">
      <p>📥 <strong>下载完整报告</strong> — 包含所有医院信息、费用明细、行动指南和行前准备清单。</p>
      <a id="dloadBtn" class="btn-dload" href="#" onclick="downloadTxt();return false;">⬇ 下载完整报告 (.txt)</a>
    </div>

    <div class="disclaimer">
      <strong>📋 重要提示：</strong> 价格为基于典型病例和已公布数据的估算值。实际费用因诊断、医院和治疗方案而异。请直接联系医院获取个性化报价。本报告仅供参考，不构成医疗建议。
    </div>
  </div>
  <div class="footer">
    <p>由 <a href="https://chinahospitalsguide.com">ChinaHospitalsGuide.com</a> 生成 — 为中国医疗旅游提供一站式支持</p>
    <p style="margin-top:4px;">📧 contact@chinahospitalsguide.com | 数据覆盖：51家医院 · 10个城市</p>
  </div>
</div>
<script>
function downloadTxt(){var c=document.querySelector('.content');if(!c)return;var t='';c.querySelectorAll('h1,h2,h3,h4,p,li,blockquote').forEach(function(e){if(e.closest('.toolbar')||e.closest('.footer'))return;var txt=e.textContent.trim();if(txt.length>4)t+=txt+'\n\n';});var b=new Blob([t.trim()],{type:'text/plain;charset=utf-8'});var u=URL.createObjectURL(b);var a=document.createElement('a');a.href=u;a.download='report-'+document.title.replace(/[^a-z0-9]/gi,'-').replace(/--+/g,'-').replace(/^-|-$/g,'')+'.txt';document.body.appendChild(a);a.click();document.body.removeChild(a);URL.revokeObjectURL(u);}
</script>
</body>
</html>`;
}

// ========== CLI ==========
function parseArgs(argv) {
  const r = { keywords: [], city: null, name: null, premium: false, basic: false };
  for (let i = 0; i < argv.length; i++) {
    if (argv[i] === '--name' && argv[i+1]) { r.name = argv[i+1]; i++; }
    else if (argv[i] === '--case' && argv[i+1]) { r.keywords.push(argv[i+1]); i++; }
    else if (argv[i] === '--city' && argv[i+1]) { r.city = argv[i+1]; i++; }
    else if (argv[i] === '--premium') { r.premium = true; }
    else if (argv[i] === '--basic') { r.basic = true; }
    else if (!argv[i].startsWith('--')) { r.keywords.push(argv[i]); }
  }
  return r;
}

const opts = parseArgs(process.argv.slice(2));
if (opts.keywords.length === 0) {
  console.log("Usage:");
  console.log('  Quick match:   node generate-report.js "knee replacement" [city]');
  console.log('  Premium:       node generate-report.js --name "John" --case "knee replacement" --premium');
  console.log('  Basic:         node generate-report.js --name "Maria" --case "knee replacement" --basic');
  console.log('  Chinese:       node generate-report.js "心脏搭桥" 上海');
  process.exit(0);
}

const csvPath = path.join(__dirname, "..", "data", "hospital-directory-51.csv");
const hospitals = loadHospitals(csvPath);

const joinKeywords = opts.keywords.join(" ");
let keywords = joinKeywords.replace(/[,，]/g, " ").split(/\s+/).filter(Boolean);
keywords = splitChineseTokens(keywords);

let city = opts.city || null;
if (city) { city = CITY_MAP[city] || city; }

let results = screenHospitals(hospitals, keywords, city);
if (results.length === 0) {
  results = screenHospitals(hospitals, keywords, null, 0.7);
}

if (results.length > 0) {
  const isPremium = opts.premium || (opts.name && !opts.basic);
  const reportOpts = { name: opts.name, premium: isPremium };
  const html = generateHtmlReport(results, keywords, city || "No limit", null, reportOpts);
  const safeName = opts.name
    ? opts.name.toLowerCase().replace(/[^a-z0-9]+/g,'-').replace(/-+/g,'-').replace(/^-|-$/g,'')
    : keywords.slice(0,3).join("-").replace(/[/\\]/g,"-");
  const ts = Date.now();
  const htmlFile = "report-" + safeName + "-" + ts + ".html";
  const outPath = path.join(__dirname, "..", "reports", htmlFile);
  fs.writeFileSync(outPath, html, "utf8");
  console.log("✅ Report generated: reports/" + htmlFile);
  console.log("   " + results.length + " hospitals matched");
  console.log("   Type: " + (opts.name ? (isPremium ? "Premium ($399)" : "Basic ($49)") : "Quick match"));
} else {
  console.log("❌ No hospitals found. Try different keywords.");
}
