#!/usr/bin/env python3
"""
Generate the ¥49 Basic hospital report from chinahospitalsguide JSON data.
Output: hospital-directory-basic-49.md in the repo root.

Usage:
    python3 scripts/generate-basic49-report.py

Requires:
    - /home/ubuntu/chinahospitalsguide/api/v1/hospitals.json
    - One-liner dict (hardcoded below)
    - Transport guide dict (hardcoded below)

Editable selections at bottom of this file:
    - HOSPITAL_INDICES: which 3 hospitals to feature
"""
import json
import os

# === PATHS ===
REPO = '/home/ubuntu/chinahospitalsguide'
JSON_PATH = os.path.join(REPO, 'api/v1/hospitals.json')
OUTPUT = os.path.join(REPO, 'hospital-directory-basic-49.md')

LQ = '\u201c'  # left double quote
RQ = '\u201d'  # right double quote

# === TRANSPORT GUIDE (per city, markdown-ready) ===
TRANSPORT_TIPS = {
    'Beijing': [
        '**北京有两个国际机场。** PEK (Capital) 在东北方向——多数医院靠近这个机场。PKX (Daxing) 在南部。预约时问清楚医生在哪个院区，再决定飞哪个。',
        '**出租车/网约车**：Capital → 市区 ¥120-200，Daxing → 市区 ¥200-350。建议用滴滴App（英文界面），比打表便宜。',
        '**地铁**：Capital机场线 ¥25 到东直门/三元桥。Daxing机场线 ¥35 到草桥。',
        '**提示**：如果是去协和（东单）、同仁（崇文门），Daxing机场线到草桥后打车更近。',
    ],
    'Shanghai': [
        '**上海有两个机场。** PVG (浦东) 是主国际机场，距市区远。SHA (虹桥) 在市区西侧，国内航班多。',
        '**出租车/网约车**：PVG → 市区 ¥150-250（45-70min），SHA → 市区 ¥50-100（20-35min）。',
        '**地铁**：PVG 磁悬浮 ¥50 到龙阳路站（7min），换2号线可到大部分医院附近。',
        '**提示**：能飞虹桥就飞虹桥，省一半时间和交通费。',
    ],
    'Guangzhou': [
        '**白云机场 (CAN)** 是唯一主机场，距市区约40-60分钟车程。',
        '**出租车/网约车**：¥100-180 到市区，建议用滴滴。',
        '**地铁**：3号线直达体育西路，换乘可到大部分医院附近。',
        '**提示**：越秀区（中山一院、省人民医院）更近机场约40min。番禺方向要1小时+。',
    ],
    'Shenzhen': [
        '**宝安机场 (SZX)** 是唯一主机场，距南山区约30-40分钟。',
        '**出租车/网约车**：¥80-150 到市区。',
        '**地铁**：11号线到福田/南山30min。',
        '**提示**：深圳城市不大，从机场到任何医院一般不超过1小时，是全国交通最方便的城市之一。',
    ],
    'Chengdu': [
        '**成都用天府机场 (TFU)** 和双流机场 (CTU)。天府是主机场，距市区60-80分钟。双流距市区30-40分钟。',
        '**出租车/网约车**：天府 → 市区 ¥150-250，双流 → 市区 ¥50-100。',
        '**地铁**：18号线从天府到火车南站约50min。',
        '**提示**：如果可选，优先选飞双流的航班，时间和费用都省一半。华西医院靠近市区。',
    ],
    "Xi'an": [
        '**咸阳机场 (XIY)** 是唯一机场，距市区约50-65分钟。',
        '**出租车/网约车**：¥100-150 到市区。',
        '**地铁**：14号线转2号线可达市区。',
        '**提示**：唐都医院在灞桥区（东郊），机场→唐都大约50-60分钟，比去市中心近。',
    ],
    'Hangzhou': [
        '**萧山机场 (HGH)** 是主机场，距市中心约40-60分钟。',
        '**出租车/网约车**：¥100-180 到市区。',
        '**地铁**：1号线和7号线从机场到市区。',
        '**提示**：杭州城市不大，从机场到任何医院通常不超过1小时。',
    ],
    'Tianjin': [
        '**滨海机场 (TSN)** 距市区约30-50分钟。从北京坐高铁到天津也仅30分钟。',
        '**出租车/网约车**：¥50-120 到市区。',
        '**提示**：很多患者选择飞到北京然后坐高铁（30min）到天津。',
    ],
    'Nanjing': [
        '**禄口机场 (NKG)** 距市区约45-60分钟。',
        '**出租车/网约车**：¥120-200 到市区。',
        '**地铁**：S1号线转1号线到新街口。',
    ],
    'Jinan': [
        '**遥墙机场 (TNA)** 距市区约40-60分钟。',
        '**出租车/网约车**：¥80-150 到市区。',
        '**提示**：可以飞北京/上海再转高铁到济南西站（北京→济南约1.5h，上海→济南约3h）。',
    ]
}

# === ONE-LINERS (per hospital, "一句话性格") ===
ONE_LINERS = {
    'Fu Wai Hospital': f'中国心脏手术的{LQ}最高法院{RQ}\u2014\u2014{LQ}别的医院搞不定的心脏病例，最后都转到这里',
    'Anzhen Hospital': '主动脉夹层的全国王牌，越危重的病例越往这里送',
    'Zhongshan Hospital (Shanghai)': '上海滩的医疗全能选手\u2014\u2014心血管和肿瘤两手都硬',
    'Jishuitan Hospital': f'骨科界的{LQ}老佛爷{RQ}{LQ}全国最难的关节置换和脊柱手术都在这做',
    'Shanghai Sixth Hospital': '创伤骨科和运动损伤的上海首选，糖尿病足治疗也是看家本领',
    'Peking University Third Hospital': f'中国最会{LQ}接好孕{RQ}的医院\u2014\u2014生殖科全国第一，运动医学也顶级',
    'Cancer Hospital, CAMS': f'中国抗癌的{LQ}国家队{RQ}\u2014\u2014国家级癌症中心，治疗方案最权威',
    'Tiantan Hospital': '开颅手术的全国标杆\u2014\u2014神经外科领域，天坛说第二没人说第一',
    'Peking Union Medical College Hospital': f'中国医学的{LQ}百年圣殿{RQ}\u2014\u2014协和出手，全国没有不敢接的病',
    'China-Japan Friendship Hospital': f'国际诊疗经验丰富的{LQ}老牌窗口{RQ}\u2014\u2014最早接待外国患者的医院之一',
    'West China Hospital': f'中国西部医疗的{LQ}定海神针{RQ}\u2014\u2014全国综合排名第2，什么病在华西都有解',
    'Fuda Cancer Hospital': f'不想做传统放化疗？冷冻消融和纳米刀是它的独门绝技。民营医院的国际患者服务标杆',
    'Sun Yat-sen University Cancer Center': f'华南抗癌的{LQ}最高殿堂{RQ}\u2014\u2014中山肿瘤，南方癌症患者的朝圣地',
    'Beijing Tongren Hospital': '全国眼科患者的目光终点\u2014\u2014同仁医院，眼科就是它的代名词',
    'Tangdu Hospital (Fourth Military Medical University)': '军队医院出身能打硬仗\u2014\u2014胸外科全军第一，胡桃夹综合征3D支架全国独家',
}

# === WHY RECOMMENDED (per hospital) ===
WHY_RECOMMENDED = {
    'Tangdu Hospital (Fourth Military Medical University)': [
        '胸外科全国第6、全军第1，神经外科和骨科也是顶级水准',
        '胡桃夹综合征 3D 打印支架手术——全国独家技术之一，复发率 < 3%',
        '费用参考：3D支架植入术 \u00a545,000-60,000（约 $6,300-8,500）',
        '国际部已接待多位国际患者，对外国患者服务流程成熟',
    ],
    'Fu Wai Hospital': [
        '中国心血管外科的\u201c国家队\u201d，全国第1',
        '复杂心脏手术的最终转诊医院',
        '北京生活成本较高，但医疗资源集中',
    ],
    'West China Hospital': [
        '全国综合排名第2，是中国西部地区最权威的医院',
        '什么病都能接，多科室会诊能力极强',
        '神经外科、胸外科、肝胆外科、呼吸内科均为国内顶级',
        '成都生活成本低，市区很安全，可以放心住院',
    ],
}

def generate(basic_hospitals):
    """Generate the basic report markdown."""
    
    with open(JSON_PATH, encoding='utf-8') as f:
        data = json.load(f)
    
    hospitals_by_id = {h['name']: h for h in data['hospitals']}
    
    # Pick hospitals from the selection
    selected = []
    for name_or_id in basic_hospitals:
        h = hospitals_by_id.get(name_or_id)
        if h:
            selected.append(h)
    
    rec_cities = list(dict.fromkeys(h['city'] for h in selected))
    
    lines = []
    
    # --- HEADER ---
    lines.append('# \u4e2d\u56fd\u533b\u7597\u65c5\u6e38\u533b\u9662\u63a8\u8350\u62a5\u544a \u00b7 \u57fa\u7840\u7248')
    lines.append('')
    lines.append('> **China Hospitals Guide** \u2014 Hospital Match & Plan ($49)')
    lines.append('')
    lines.append('---')
    lines.append('')
    
    # --- COVER LETTER ---
    lines.append('## \U0001F33F \u81f4\u5ba2\u6237\u7684\u4e00\u5c01\u4fe1')
    lines.append('')
    lines.append('\u4f60\u597d\uff0c')
    lines.append('')
    lines.append('\u611f\u8c22\u4f60\u9009\u62e9\u6211\u4eec\u7684\u57fa\u7840\u7248\u63a8\u8350\u62a5\u544a\u3002')
    lines.append('')
    lines.append('\u8fd9\u4efd\u62a5\u544a\u5e2e\u4f60\u505a\u4e86\u4e00\u4ef6\u4e8b\uff1a\u4ece\u4e2d\u56fd51\u5bb6\u9876\u7ea7\u533b\u9662\u4e2d\u7b5b\u51fa\u6700\u9002\u5408\u4f60\u7684\uff0c\u5e76\u8ba9\u4f60\u5bf9\u5b83\u4eec\u6709\u4e00\u4e2a\u771f\u5b9e\u7684\u611f\u89c9\u3002')
    lines.append('')
    lines.append('\u5982\u679c\u4f60\u770b\u5b8c\u540e\u89c9\u5f97\u9700\u8981\u66f4\u6df1\u5165\u7684\u5e2e\u52a9\u2014\u2014\u6bd4\u5982\u5e2e\u4f60\u53d1\u75c5\u5386\u3001\u8ddf\u8fdb\u56de\u590d\u3001\u7ffb\u8bd1\u534f\u8c03\u3001\u63a5\u673a\u5b89\u6392\u2014\u2014\u6211\u4eec\u4e5f\u6709\u5b8c\u6574\u7684\u534f\u8c03\u670d\u52a1\uff08\u53c2\u89c1\u6587\u672b\u7684\u201c\u5347\u7ea7\u670d\u52a1\u201d\u90e8\u5206\uff09\u3002')
    lines.append('')
    lines.append('\u795d\u4f60\u65e9\u65e5\u5eb7\u590d\u3002')
    lines.append('')
    lines.append('*\u2014\u2014 China Hospitals Guide \u56e2\u961f*')
    lines.append('')
    lines.append('---')
    lines.append('')
    
    # --- HOW TO USE ---
    lines.append('## \U0001F4D6 \u5982\u4f55\u4f7f\u7528')
    lines.append('')
    lines.append('| \u6b65\u9aa4 | \u505a\u4ec0\u4e48 |')
    lines.append('|---|-----|')
    lines.append('| **\u7b2c1\u6b65** | \u4e0b\u9762\u662f\u6839\u636e\u4f60\u7684\u60c5\u51b5\u7b5b\u9009\u7684 2-3 \u5bb6\u533b\u9662\u63a8\u8350 |')
    lines.append('| **\u7b2c2\u6b65** | \u770b\u770b\u6bcf\u5bb6\u533b\u9662\u7684\u201c\u4e00\u53e5\u8bdd\u6027\u683c\u201d\u548c\u5173\u952e\u4fe1\u606f |')
    lines.append('| **\u7b2c3\u6b65** | \u5bf9\u7167\u4f60\u7684\u75c5\u60c5\u548c\u9884\u7b97\uff0c\u9009\u62e91-2\u5bb6\u8054\u7cfb |')
    lines.append('| **\u7b2c4\u6b65** | \u53c2\u8003\u6bcf\u4e2a\u57ce\u5e02\u7684\u4ea4\u901a\u6307\u5357\uff0c\u5f00\u59cb\u89c4\u5212\u884c\u7a0b |')
    lines.append('| **\u7b2c5\u6b65** | \u5982\u679c\u9700\u8981\u66f4\u6df1\u5165\u5e2e\u52a9\uff0c\u67e5\u770b\u201c\u5347\u7ea7\u670d\u52a1\u201d\u90e8\u5206 |')
    lines.append('')
    lines.append('---')
    lines.append('')
    
    # --- HOSPITAL CARDS ---
    lines.append('## \U0001F3E5 \u63a8\u8350\u533b\u9662')
    lines.append('')
    
    for h in selected:
        name = h['name']
        name_zh = h['name_zh']
        ol = ONE_LINERS.get(name, '')
        why = WHY_RECOMMENDED.get(name, [])
        
        lines.append(f'### {name}（{name_zh}）')
        lines.append('')
        if ol:
            lines.append(f'> \U0001F4AC *{ol}*')
            lines.append('')
        
        lines.append('| | |')
        lines.append('|---|---|')
        lines.append(f'| **\u4e13\u79d1\u4f18\u52bf** | {", ".join(h["tags"])} |')
        if h.get('rank'):
            lines.append(f'| **\u6392\u540d/\u8bc4\u7ea7** | \U0001F3C6 {h["rank"]} |')
        lines.append(f'| **\u5730\u5740** | {h.get("address", "")} |')
        lines.append(f'| **\u7535\u8bdd** | \U0001F4DE {h.get("phone", "\u2014")} |')
        if h.get('email'):
            lines.append(f'| **\u90ae\u7bb1** | \U0001F4E7 {h["email"]} |')
        lines.append(f'| **\u7f51\u7ad9** | {h.get("website", "\u2014")} |')
        if h.get('international'):
            lines.append('| **\u56fd\u9645\u90e8** | \u2705 \u6709\uff08\u53cc\u8bed\u534f\u8c03\u5458\uff09|')
        lines.append('')
        
        if why:
            lines.append('**\u4e3a\u4ec0\u4e48\u63a8\u8350\u8fd9\u5bb6\u533b\u9662\uff1a**')
            lines.append('')
            for item in why:
                lines.append(f'- {item}')
            lines.append('')
        
        lines.append('---')
        lines.append('')
    
    # --- TRANSPORT ---
    lines.append('## \u2708\uFE0F \u57ce\u5e02\u4ea4\u901a\u6307\u5357')
    lines.append('')
    lines.append('> \u4ee5\u4e0b\u662f\u63a8\u8350\u533b\u9662\u6240\u5728\u57ce\u5e02\u7684\u4ea4\u901a\u8be6\u60c5\u3002\u5982\u679c\u4f60\u9009\u62e9\u5176\u4ed6\u57ce\u5e02\uff0c\u53ef\u4ee5\u8054\u7cfb\u6211\u4eec\u83b7\u53d6\u5bf9\u5e94\u4fe1\u606f\u3002')
    lines.append('')
    for city in rec_cities:
        tips = TRANSPORT_TIPS.get(city, [])
        if tips:
            lines.append(f'### \U0001F4CD\u2708\uFE0F {city}')
            lines.append('')
            for t in tips:
                lines.append(f'- {t}')
            lines.append('')
            lines.append('---')
            lines.append('')
    
    # --- CHECKLIST ---
    lines.append('## \U0001F4CB \u884c\u524d\u51c6\u5907\u6e05\u5355')
    lines.append('')
    lines.append('\u5fc5\u5e26\u7684\u6750\u6599\uff1a')
    lines.append('- \u539f\u59cb\u75c5\u5386 + \u5f71\u50cf\u8d44\u6599\uff08CT/MRI\u5149\u76d8\u6216U\u76d8\uff09')
    lines.append('- \u6b63\u5728\u670d\u7528\u7684\u836f\u7269\uff08\u5e26\u8db3\u91cf + \u82f1\u6587\u8bf4\u660e\u4e66\uff09')
    lines.append('- \u62a4\u7167\uff08\u6709\u6548\u671f6\u4e2a\u6708\u4ee5\u4e0a\uff09')
    lines.append('- \u4fe1\u7528\u5361\uff08Visa/Mastercard\uff09+ \u5c11\u91cf\u73b0\u91d1')
    lines.append('- \u624b\u673a\u5f00\u901a\u56fd\u9645\u6f2b\u6e38\u6216\u5230\u8fbe\u540e\u4e70\u4e2d\u56fd\u7535\u8bdd\u5361')
    lines.append('- \u8f6c\u6362\u63d2\u5934\uff08\u4e2d\u56fd\u6807\u51c6\uff1a\u4e24\u811a\u6241\u578b\uff0c220V\uff09')
    lines.append('')
    lines.append('> \U0001F4E5 **\u63d0\u793a\uff1a** \u4e0b\u8f7d\u652f\u4ed8\u5b9dApp\uff0c\u7ed1\u5b9a\u56fd\u9645\u4fe1\u7528\u5361\uff0c\u5230\u4e2d\u56fd\u540e\u4ece\u4fbf\u5229\u5e97\u5230\u836f\u623f\u5230\u9910\u5385\u90fd\u53ef\u4ee5\u626b\u7801\u652f\u4ed8\u3002')
    lines.append('')
    lines.append('---')
    lines.append('')
    
    # --- UPSELL ---
    lines.append('## \u2b50 \u5347\u7ea7\u670d\u52a1\uff1a\u4ee5\u4e0b\u670d\u52a1\u5747\u5c5e\u4e8e\u300cPre-Arrival Coordination ($399)\u300d\uff0c\u57fa\u7840\u7248\u4e0d\u5305\u542b')
    lines.append('')
    lines.append('| \u9636\u6bb5 | \u670d\u52a1\u5185\u5bb9 |')
    lines.append('|-------|-----------|')
    lines.append('| **\u9700\u6c42\u786e\u8ba4** | \u4e00\u5bf9\u4e00\u987e\u95ee\u5bf9\u63a5\u3001\u7cbe\u51c6\u5339\u914d\u3001\u5b9a\u5236\u8c03\u6574 |')
    lines.append('| **\u533b\u9662\u5bf9\u63a5** | \u4ee3\u53d1\u75c5\u5386\u3001\u7ffb\u8bd1\u534f\u8c03\u3001\u8ddf\u8fdb\u56de\u590d\u3001\u591a\u9662\u5bf9\u6bd4\u62a5\u4ef7 |')
    lines.append('| **\u884c\u524d\u51c6\u5907** | \u7b7e\u8bc1\u6750\u6599\u6307\u5bfc\u3001\u9884\u7ea6\u9501\u5b9a\u3001\u4f4f\u5bbf\u5efa\u8bae\u3001\u884c\u524d\u6e05\u5355\u3001\u63a5\u673a\u5b89\u6392 |')
    lines.append('| **\u6cbb\u7597\u671f\u95f4** | \u533b\u9662\u6c9f\u901a\u8854\u63a5\u3001\u7a81\u53d1\u95ee\u9898\u534f\u8c03\u3001\u7d27\u6025\u8054\u7cfb\u7535\u8bdd |')
    lines.append('| **\u51fa\u9662\u56de\u56fd** | \u4e2d\u82f1\u6587\u75c5\u5386\u6574\u7406\u3001\u7528\u836f\u8bf4\u660e\u3001\u590d\u67e5\u9884\u7ea6\u3001\u8fdc\u7a0b\u968f\u8bbf\u8854\u63a5 |')
    lines.append('')
    lines.append('---')
    lines.append('')
    
    # --- FAQ ---
    lines.append('## \u2753 \u5e38\u89c1\u95ee\u9898')
    lines.append('')
    lines.append('### Q: \u8fd9\u4efd\u62a5\u544a\u548c $399 \u7684\u5347\u7ea7\u7248\u6709\u4ec0\u4e48\u533a\u522b\uff1f')
    lines.append('')
    lines.append('\u8fd9\u4efd $49 \u62a5\u544a\u7ed9\u4f60\u7cbe\u51c6\u7684\u533b\u9662\u63a8\u8350\u3001\u4ea4\u901a\u6307\u5357\u548c\u884c\u524d\u6e05\u5355\u3002\u4f60\u62ff\u5230\u540e\u53ef\u4ee5\u81ea\u5df1\u8054\u7cfb\u533b\u9662\u3001\u81ea\u5df1\u5b89\u6392\u884c\u7a0b\u3002 $399 \u5347\u7ea7\u7248\u662f\u6211\u4eec\u5e2e\u4f60\u505a\u8fd9\u4e00\u5207\u2014\u2014\u4ee3\u53d1\u75c5\u5386\u3001\u8ddf\u8fdb\u56de\u590d\u3001\u7ffb\u8bd1\u3001\u63a5\u673a\u3001\u6cbb\u7597\u671f\u95f4\u534f\u8c03\u3001\u51fa\u9662\u6587\u4ef6\u6574\u7406\u3001\u56de\u56fd\u540e\u968f\u8bbf\u8854\u63a5\u3002')
    lines.append('')
    lines.append('### Q: \u6211\u53ef\u4ee5\u5148\u4e70 $49\uff0c\u540e\u7eed\u518d\u5347\u7ea7\u5417\uff1f')
    lines.append('')
    lines.append('\u53ef\u4ee5\u3002 $49 \u7684\u8d39\u7528\u53ef\u4ee5\u62b5\u6263\u5347\u7ea7\u8d39\u7528\uff0c\u4f60\u53ea\u9700\u8865\u5dee\u4ef7\u5373\u53ef\u3002')
    lines.append('')
    lines.append('---')
    lines.append('')
    lines.append('*\u611f\u8c22\u4f60\u9009\u62e9 China Hospitals Guide\u3002\u795d\u4f60\u65e9\u65e5\u5eb7\u590d\u3002* \U0001F33F')
    
    content = '\n'.join(lines)
    with open(OUTPUT, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f'Done! Basic report generated: {len(content)} chars, {len(lines)} lines')
    print(f'Output: {OUTPUT}')
    print(f'Hospitals: {[h["name"] for h in selected]}')


# === EDITABLE SELECTION ===
# Pick hospitals by their "name" field in the JSON.
# These are the 3 that will appear in the report.
if __name__ == '__main__':
    generate([
        'Tangdu Hospital (Fourth Military Medical University)',
        'Fu Wai Hospital',
        'West China Hospital',
    ])
