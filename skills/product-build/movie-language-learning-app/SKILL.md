---
name: movie-language-learning-app
description: Build a language learning app where users learn by watching movies/TV with sentence-level replay, aligned subtitles, and AI pronunciation scoring. One-person company, app-first, subscription model.
category: product-build
---

# Movie-Based Language Learning App

## Product Concept
Foreigners learn target language (currently: Chinese for English speakers) through classic movies/TV shows. Users watch clips, click any subtitle sentence to replay it, follow along, and practice speaking.

**Analog:** [Lingopie](https://www.lingopie.com) — same model for English/Spanish/etc. with Netflix/TV content.

## Target User
- English-speaking foreigners wanting to learn Chinese
- Beginner to intermediate levels
- Commuters, busy professionals who want authentic, engaging content

## Content Strategy

### Tier 1: Hong Kong Cinema (highest priority)
- **Chungking Express** (重庆森林) — daily dialogue, clear pronunciation
- **In the Mood for Love** (花样年华) — slower, poetic
- **Kung Fu Hustle** (功夫) — action + comedy, widely known
- **Shaolin Soccer** (少林足球) — humor, physical comedy
- **Fallen Angels** (堕落天使) — moody, great for tone learning
- **The 36th Chamber of Shaolin** (少林三十六房) — martial arts经典

### Tier 2: Mainland/Taiwan TV
- **In the Heat of the Sun** (阳光灿烂的日子) — coming-of-age
- **Journey to the West** (西游记) — accessible classic
- **Joy of Life** (庆余年) — popular drama, engaging

### Tier 3: Contemporary
- **Eternal Sunshine of the Spotless Mind** (Mandarin dubbed)
- Douyin/哔哩哔哩 short drama clips

## Core Features (Priority Order)

### MVP (v1.0)
1. **Video player** with full-episode/film playback
2. **Clickable subtitles** — tap any sentence to replay that clip in loop
3. **Sentence-level timestamp alignment** — HARDEST technical problem
4. **Dual subtitles** — original language + English translation
5. **Play at 0.75x, 1x speed** toggle
6. **Simple progress tracking** — which sentences practiced

### Post-MVP
7. **AI pronunciation scoring** — record user's sentence, compare with original (Whisper + alignment)
8. **Vocabulary cards** — tap word to save to flashcard deck
9. **Phonetic guide** — pinyin overlay on Chinese text
10. **Community** — user-generated notes per sentence
11. **Offline download** — critical for mobile use case
12. **Daily streak / push reminders**

## Technical Architecture

### Subtitles — The Hardest Problem (updated 2025-05-03)

**⚠️ Subtitle landscape has changed:**
- 射手网 ( shooter.cn) is now an AI translation service — no longer sells raw subtitle files
- yt-dlp is needed for automated subtitle extraction — install with `pip install yt-dlp`
- OpenSubtitles (opensubtitles.org) still exists but quality varies

**Viable paths for subtitle data:**

1. **Whisper + Manual Correction** (recommended):
   - `pip install openai-whisper` to transcribe audio
   - Whisper outputs timestamped text
   - Manual spot-check and correction for key sentences (10-20 per video for MVP)
   - Time investment: ~2-3 hours per video

2. **YouTube Auto-Captions** (quickest for YouTube content):
   - Use YouTube's built-in CC captions via YouTube IFrame API
   - Extract with yt-dlp: `yt-dlp --write-auto-sub --sub-lang zh-Hans --skip-download`
   - Quality: varies, usually needs cleanup

3. **Manual transcription** (slowest but most accurate):
   - Watch video, type out each sentence, estimate timestamps
   - For MVP with 5-10 core sentences: feasible solo

**MVP subtitle approach (current session):**
- Select 5-10 minute YouTube video with authentic dialogue (not scripted)
- Manually transcribe 10-20 core sentences with timestamps
- Build MVP around these 10-20 sentences first
- Full alignment comes later

**Format: Custom JSON subtitle object:**
```javascript
{
  start: 0.5,      // seconds (float)
  end: 3.2,        // seconds (float)
  original: '你好，我想买一束花。',
  translation: 'Hello, I want to buy a bouquet of flowers.',
  pinyin: 'nǐ hǎo, wǒ xiǎng mǎi yí shù huā.',
  difficulty: 'beginner'  // beginner/intermediate/advanced
}
```

**Recommended first video:**
- YouTube ID: `SGS8sfH11yg`
- Title: "Real Chinese Conversation: Buy Flowers" by MandarinMoon
- Duration: 5:33 (perfect for MVP)
- Channel focuses on practical, authentic dialogue with CC subtitles
- Alternative shorter videos: `rV02wNVDHUg` (food & drink, HSK1-2), `l5eMUEGHv5Y` (slow Chinese, beginner)

### Tech Stack (updated 2026-05-03)
- **Frontend**: HTML + CSS + Vanilla JS (lightest, fastest to build)
- **Video player**: Plyr.js (open source, clean UI, native subtitle support) — CDN: `https://cdn.jsdelivr.net/npm/plyr@3/dist/plyr.min.js`
- **Subtitle format**: SRT or custom JSON
- **Audio recording**: Browser MediaRecorder API (native, no library needed)
- **AI scoring**: Future — Azure Speech SDK or OpenAI Realtime API
- **Backend**: Supabase (auth, payments, progress sync) — but MVP uses localStorage only
- **Hosting**: GitHub Pages (free, instant deploy)

### Video Hosting — Tencent Cloud COS (CRITICAL for China market)
> ⚠️ YouTube Embed does NOT work in China. All target users (Chinese speakers) will have blocked access. Must use self-hosted video from day 1.
>
> Setup guide: `references/tencent-cos-setup.md`

**Storage: Tencent Cloud COS (对象存储)**
- Pricing: ~¥0.118/GB/month; new users get 50GB free
- Choose **"公有读私有写"** (public read, private write) — correct setting
- COS link format: `https://your-bucket.cos.ap-guangzhou.myqcloud.com/video.mp4`

**Player: Plyr.js with native HTML5 `<video>`**
```html
<video>
  <source src="COS_VIDEO_URL" type="video/mp4">
  <track kind="subtitles" src="subtitles.srt" srclang="zh" label="中文" default>
</video>
```

**Build Order (revised — user prefers App):
> **App-first is preferred** for this product — offline, background audio, push notifications, and voice recording permissions are critical for a language learning app and require native.

- **Phase 1**: Web MVP first (validate fast, ~1-2 weeks)
- **Phase 2**: Capacitor wrap or Flutter rewrite to App
- Video hosting stays on Tencent Cloud COS regardless of platform

### Deployed Resources
- **GitHub repo**: `qzw-alt/chinese-learning-app` (https://github.com/qzw-alt/chinese-learning-app)
- **GitHub Pages**: `https://qzw-alt.github.io/chinese-learning-app/` (live demo)

## Business Model

```
Phase 1: Free
  - 1-2 free films
  - No AI scoring, basic tracking
  - Goal: acquire users, validate content

Phase 2: Subscription
  - $4.99/month or $39.99/year
  - Full library access
  - AI pronunciation scoring
  - Offline downloads
  - Streaks + progress

Phase 3: Content Expansion
  - More films, TV series
  - User request queue
  - Community captions

Phase 4: Ads
  - Free tier with ads (interstitial after every 3 sentences)
  - Subsidized subscription option
```

## Competitors
- **Lingopie** (overseas) — closest model, Netflix/TV content
- **HelloChinese / Duolingo Chinese** — gamified, no video
- **The Chairman's Bao / Du Chinese** — reading only, no video
- **看美剧学英语** (微信文章 user referenced) — Chinese domestic market

## One-Person Company Constraints
- Outsource subtitle alignment (Fiverr/Upwork ~$200-500/film)
- Start with public domain / fair use content
- Use Supabase for backend (low cost, fast)
- Build MVP in 2-3 months solo
- Test with 5 films first before expanding library

## File Locations
- Spec: `/root/.hermes/workspace/chinese-learning-app/SPEC.md`
- Tech notes: `/root/.hermes/workspace/chinese-learning-app/`
