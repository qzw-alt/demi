import re, os
from datetime import datetime

blog_dir = "blog"
idx = f"{blog_dir}/index.html"

with open(idx) as f:
    content = f.read()

blog_grid_start = content.find('<div class="blog-grid">')
last_card = content.rfind('<div class="blog-card">')
after = content[last_card:]
card_close = after.find('</div>', 150, 300)
blog_grid_end = last_card + card_close + len('</div>')

header = content[:blog_grid_start]
footer = content[blog_grid_end:]

files = [f for f in os.listdir(blog_dir) if f.endswith('.html') and f != 'index.html']
articles = []
for fname in files:
    path = f"{blog_dir}/{fname}"
    with open(path) as f:
        txt = f.read()
    title_m = re.search(r'<title>([^<]+)</title>', txt)
    title = title_m.group(1).replace(' - China Hospitals Guide','').strip() if title_m else fname
    desc_m = re.search(r'<meta name="description" content="([^"]+)"', txt)
    excerpt = desc_m.group(1)[:180] if desc_m else ''
    slug = fname[:-5]
    date_match = re.match(r'^(\d{4})-(\d{2})-(\d{2})', fname)
    dt = datetime(int(date_match.group(1)), int(date_match.group(2)), int(date_match.group(3))) if date_match else datetime(2026,1,1)
    articles.append({'fname': fname, 'title': title, 'excerpt': excerpt, 'date': dt, 'slug': slug})

articles.sort(key=lambda x: x['date'], reverse=True)

cat_colors = {
    'City Guide': ('#1e3c72','#4f7dd8'), 'Cancer Treatment': ('#8B0000','#dc143c'),
    'Eye Care': ('#006400','#228B22'), 'Dental Care': ('#00b4db','#0083b0'),
    'Orthopedics': ('#8B4513','#D2691E'), 'Cardiac Surgery': ('#dc143c','#FF6347'),
    'Neurosurgery': ('#4B0082','#9370DB'), 'Plastic Surgery': ('#c84b31','#e85d4a'),
    'Fertility': ('#c2185b','#e91e63'), 'Regenerative Medicine': ('#1565C0','#42A5F5'),
    'Medical Tourism': ('#1e3c72','#2a5298'), 'Expat Guide': ('#00695c','#00897b'),
    'Travel Guide': ('#F57C00','#FFB74D'), 'Hospital Guide': ('#17345f','#2a5298'),
    'Cost Guide': ('#2E7D32','#66BB6A'), 'Health Screening': ('#00695c','#00897b'),
    'TCM & Wellness': ('#8e44ad','#c39bd3'), 'Patient Story': ('#D4AF37','#FFD700'),
    'Medical Guide': ('#1e3c72','#6b8dd6'),
}

cat_map = {
    'cataract':'Eye Care','lasik':'Eye Care','dental':'Dental Care',
    'ivf':'Fertility','fertility':'Fertility','orthopedic':'Orthopedics',
    'spine':'Orthopedics','joint':'Orthopedics','knee':'Orthopedics','hip':'Orthopedics',
    'cardiac':'Cardiac Surgery','heart':'Cardiac Surgery',
    'brain':'Neurosurgery','neurosurgery':'Neurosurgery','tumor':'Neurosurgery',
    'bone-marrow':'Cancer Treatment','car-t':'Cancer Treatment',
    'stem-cell':'Regenerative Medicine','plastic':'Plastic Surgery','rhinoplasty':'Plastic Surgery',
    'hair':'Hair Restoration','weight-loss':'Weight Loss Surgery','bariatric':'Weight Loss Surgery',
    'kidney':'Nephrology','dialysis':'Nephrology','epilepsy':'Neurology','deep-brain':'Neurosurgery',
    'proton':'Cancer Treatment','cancer':'Cancer Treatment',
    'tcm':'TCM & Wellness','hainan':'TCM & Wellness','baduanjin':'TCM & Wellness',
    'how-to-see':'City Guide','hospitals-in-':'City Guide',
    'japan':'International','thailand':'Comparison',
    'why-choose':'Medical Tourism','why-international':'Medical Tourism',
    'foreigners':'Expat Guide','giving-birth':'Expat Guide',
    'medical-visa':'Travel Guide','visa-free':'Travel Guide',
    'jci':'Hospital Guide','cost-comparison':'Cost Guide','china-vs-usa':'Cost Guide',
    'china-hospital':'Hospital Guide','how-to-choose':'Hospital Guide',
    'how-to-book':'Hospital Guide','how-to-prepare':'Travel Guide',
    'patient-story':'Patient Story','health-screening':'Health Screening',
}

def get_cat(slug):
    for k,v in cat_map.items():
        if k in slug: return v
    return 'Medical Guide'

cards = []
for a in articles:
    c1,c2 = cat_colors.get(get_cat(a['slug']),('#1e3c72','#6b8dd6'))
    initials = ''.join([w[0] for w in a['title'].split()[:2]])[:3]
    read_time = max(5, min(15, len(a['title'])//10+7))
    card = f'<div class="blog-card"><div class="blog-image" style="background:linear-gradient(135deg,{c1} 0%,{c2} 100%);">{initials}</div><div class="blog-content"><div class="blog-category">{get_cat(a["slug"])}</div><h3 class="blog-title"><a href="{a["fname"]}">{a["title"]}</a></h3><p class="blog-excerpt">{a["excerpt"]}</p><div class="blog-meta"><span>{a["date"].strftime("%B %Y")}</span><span>{read_time} min read</span></div><a href="{a["fname"]}" class="read-more">Read Article</a></div></div>'
    cards.append(card)

new_grid = '<div class="blog-grid">\n            ' + '\n            '.join(cards) + '\n        </div>'
with open(idx, 'w') as f:
    f.write(header + new_grid + footer)
print(f"Regenerated {len(cards)} blog cards")
