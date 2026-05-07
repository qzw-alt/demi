# ChineseFlix — Language Learning App Reference

> Absorbed from `chinese-learning-app` skill — project-specific implementation detail for ChineseFlix.

## Project Overview

**ChineseFlix** — movie/short-video based Chinese (Mandarin + Cantonese) learning web app.

- **GitHub**: `qzw-alt/chinese-learning-app`
- **Website**: `https://qzw-alt.github.io/chinese-learning-app/` (GitHub Pages)
- **Target**: English speakers learning Chinese
- **App-first strategy**: Web MVP → Capacitor wrap or Flutter rewrite

## Video Sources: YouTube + COS Dual Track

```javascript
// data.js video data structure
{
  id: 'xxx',
  source: 'youtube',     // or 'mp4' (COS)
  sourceId: 'KW350JEVZ7U',  // YouTube ID or COS object key
  sourceUrl: null,       // mp4 时填 COS URL
  title: '...',
  language: 'cantonese', // 'mandarin' | 'cantonese'
  difficulty: 'beginner',
}
```

**`player.js` supports youtube / mp4 / bilibili three source types natively.**

### Why YouTube First
- Free CDN, global distribution
- Built-in subtitles (can export)
- Tencent Cloud server can access YouTube
- YouTube auto-generated subtitles + timeline are usable

### COS (Tencent Cloud Object Storage) Use Cases
- Self-produced content/Hong Kong films (YouTube inaccessible)
- Domestic China users
- Private/copyrighted content

**COS Configuration:**
- Access: **Public read, private write** (防盗写)
- Region: Guangzhou (`ap-guangzhou`)
- Bucket format: `your-bucket.cos.ap-guangzhou.myqcloud.com`

## Why Not Film/TV Originals

Final films/TV shows almost always have **hard subtitles (burned in)** — cannot be removed. Users see the original subtitles, can't do "click to learn word" feature.

**Correct direction**: Real short videos
- YouTube "learn Chinese/Cantonese" authentic dialogue clips
- Scenario-based: restaurant ordering, street directions, supermarket shopping, etc.
- Have subtitles but can be exported/processed

## Finding Videos

```bash
# Search YouTube video IDs
curl -s "https://www.youtube.com/results?search_query=关键词" | python3 -c "
import sys, re
content = sys.stdin.read()
ids = re.findall(r'\"videoId\":\"([a-zA-Z0-9_-]{11})\"', content)
seen = set()
for vid in ids:
    if vid not in seen and len(seen) < 8:
        seen.add(vid)
        print(vid)
"

# Get video titles
for vid in ID1 ID2; do
  curl -s "https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v=$vid&format=json" | \
  python3 -c "import sys,json; print(vid, '|', json.load(sys.stdin).get('title',''))"
done
```

### Confirmed Usable Videos

| Scenario | YouTube ID | Title |
|----------|------------|-------|
| 茶餐厅点餐 | `KW350JEVZ7U` | Speak Cantonese like a local in a Cantonese Restaurant |
| 日常生活 | `94LIuid2lRI` | Life of University Students in Hong Kong |
| 普通话日常 | `rl4rZbeXAdc` | Real Chinese Conversation: Order a drink |
| 买花（普通话） | `SGS8sfH11yg` | Real Chinese Conversation: Buy flowers |

## Subtitle Acquisition

### Method 1: YouTube Direct Export (Recommended)
Open CC on YouTube → Settings → Show subtitles, then:
- Screenshot subtitle area
- Or copy text and organize into JSON

### Method 2: yt-dlp (Requires Server Access to YouTube)
```bash
pip install yt-dlp
yt-dlp --write-subs --skip-download https://www.youtube.com/watch?v=KW350JEVZ7U
```

### Subtitle Format (in data.js)
```javascript
{
  id: 1,
  start: 2.0,   // seconds, 1 decimal
  end: 5.5,
  text: '你好，欢迎光临。',           // original text
  jyutping: 'nei5 hou2, fun1 jing4', // Cantonese romanization
  pinyin: 'nǐ hǎo, huān yíng',       // Mandarin pinyin
  translation: 'Hello, welcome.',     // English translation
}
```

## Local Dev Workflow

```bash
cd ~/.hermes/workspace/chinese-learning-app
git add .
git commit -m "feat: ..."
git push
# GitHub Pages auto-deploys (~1-2 minutes)
# https://qzw-alt.github.io/chinese-learning-app/
```

### GitHub Token
- Stored in `~/.git-credentials`
- Remote URL embeds token: `https://TOKEN@github.com/qzw-alt/chinese-learning-app.git`

## File Structure

```
chinese-learning-app/
├── index.html          # Homepage
├── watch.html          # Player page (core)
├── vocabulary.html     # Vocabulary notebook
├── css/style.css       # Styles
├── js/
│   ├── config.js       # Config (Supabase etc.)
│   ├── app.js          # Global Alpine state
│   ├── data.js         # Video data + subtitles + dictionary
│   ├── storage.js      # localStorage wrapper
│   ├── supabase.js     # User system
│   ├── audio.js        # Recording module
│   └── components/
│       ├── player.js   # Player factory (youtube/mp4/bilibili)
│       ├── subtitles.js # Subtitle sync + click logic
│       └── ui.js       # Modal, Toast etc.
├── content/            # Content JSON (backup)
│   ├── videos.json
│   └── subtitles/
└── SPEC.md             # Development spec document
```

## Supabase (User System)

- Project: `https://github.com/qzw-alt/chinese-learning-app/tree/main/supabase`
- Auth + database configured, no changes needed
