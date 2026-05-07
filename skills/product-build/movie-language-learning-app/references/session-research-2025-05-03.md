# Session Research Reference — 2025-05-03

## YouTube Video Candidates Found

### Primary (used for MVP)
| Video ID | Title | Channel | Duration | Difficulty |
|---|---|---|---|---|
| `SGS8sfH11yg` | Real Chinese Conversation: Buy Flowers | MandarinMoon | 5:33 | Beginner |
- Has CC subtitles (built-in YouTube captions)
- Practical daily dialogue (flower shop scene)
- Channel focuses on authentic, real-world Mandarin

### Alternatives (not yet evaluated)
| Video ID | Title | Channel | Notes |
|---|---|---|---|
| `rl4rZbeXAdc` | Real Chinese Conversation: Order a drink | MandarinMoon | ~same series |
| `rV02wNVDHUg` | Food & Drink HSK1-2 | SELF STUDY MANDARIN | classroom style |
| `l5eMUEGHv5Y` | Slow Chinese Beginner | Chilling Chinese | slow speed |
| `ng-E83Dg-KU` | Chinese Learning Cartoon for Beginners | Hanyu Jiaocheng | cartoon |

## YouTube ID Extraction Technique
```bash
# Search YouTube and extract video IDs
curl -s "https://www.youtube.com/results?search_query=QUERY" | python3 -c "
import sys, re
content = sys.stdin.read()
ids = re.findall(r'\"videoId\":\"([a-zA-Z0-9_-]{11})\"', content)
seen = set()
for vid in ids:
    if vid not in seen and len(seen) < 10:
        seen.add(vid)
        print(vid)
"

# Get video metadata (title, author)
curl -s "https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v=VIDEO_ID&format=json" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('title',''), d.get('author_name',''))"

# Get YouTube thumbnails
# hqdefault: https://img.youtube.com/vi/VIDEO_ID/hqdefault.jpg
# maxresdefault: https://img.youtube.com/vi/VIDEO_ID/maxresdefault.jpg
```

## Subtitles Tools — What Works / What Doesn't

### ✅ WORKS
- **YouTube built-in CC**: `https://www.youtube.com/watch?v=ID` — open video, enable CC, use YouTube IFrame API to read captions
- **yt-dlp** (not installed): `pip install yt-dlp` then `yt-dlp --write-auto-sub --sub-lang zh-Hans --skip-download VIDEO_ID`
- **Whisper**: `pip install openai-whisper` — transcribes audio with timestamps
- **YouTube Transcript sites**: youtubetranscript.com (blocked in this session)
- **SubHD / 射手网**: 射手网转型为AI翻译播放器，不再提供字幕文件下载

### ❌ DOESN'T WORK
- 射手网 (shooter.cn): Now an AI translation service, no raw subtitle files
- Direct YouTube API calls for captions: Requires auth, blocked in this session
- Without yt-dlp: Hard to auto-download subtitles

## First Video Content Work

### Video: SGS8sfH11yg — "Buy Flowers"
- Channel: MandarinMoon
- Scene: Flower shop dialogue
- Used as MVP demo content
- Need to manually:
  1. Watch video with CC on
  2. Transcribe 10-20 core sentences
  3. Note timestamps
  4. Write English translations
  5. Add pinyin

### Transcription Steps
1. Open `https://www.youtube.com/watch?v=SGS8sfH11yg`
2. Enable CC (closed captions)
3. Play at 0.75x speed for accuracy
4. For each sentence: note start time, end time, Chinese text
5. Write English translation
6. Generate pinyin (can use online tool or manually)
7. Format as JSON per SPEC

## Page Development Spec Location
`/root/.hermes/workspace/chinese-learning-app/SPEC.md`

### Page Structure for MVP
```
chinese-learning-app/
├── index.html          # Home (video list)
├── watch.html          # Player + subtitle + recording
├── vocabulary.html     # Word list
├── css/
│   └── style.css
└── js/
    ├── data.js         # Video + subtitle data
    ├── app.js          # Home logic
    ├── watch.js        # Player + recording logic
    └── vocabulary.js   # Word list logic
```
