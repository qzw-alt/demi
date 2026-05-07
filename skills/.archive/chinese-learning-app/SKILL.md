---
name: chinese-learning-app
description: ChineseFlix — 用电影/短视频学中文/粤语的 Web App 项目。包括架构决策、视频来源策略、字幕获取、COS 接入、GitHub 协作流程。
category: product-build
---

# ChineseFlix — 学中文 App 项目

## 项目背景

**目标用户**：英语母语者学中文（含普通话+粤语）
**核心场景**：用真实语境（电影/短视频）逐句跟读学中文
**GitHub**: `qzw-alt/chinese-learning-app`
**网站**: `https://qzw-alt.github.io/chinese-learning-app/` (GitHub Pages)

---

## 架构决策

### 视频来源：YouTube + COS 双轨制

```javascript
// data.js 视频数据结构
{
  id: 'xxx',
  source: 'youtube',     // 或 'mp4'（COS）
  sourceId: 'KW350JEVZ7U',  // YouTube ID 或 COS 对象 key
  sourceUrl: null,       // mp4 时填 COS URL
  title: '...',
  language: 'cantonese', // 'mandarin' | 'cantonese'
  difficulty: 'beginner',
}
```

**player.js 已内置支持 youtube / mp4 / bilibili 三种来源**，不需要改代码，只需在 data.js 指定 source 类型。

### YouTube 优先的原因

- 免费 CDN，全球分发
- 内置字幕（可导出）
- 腾讯云服务器能访问 YouTube
- YouTube 自动生成字幕 + 时间轴基本可用

### COS（腾讯云对象存储）的用途

- 自制内容/港片（YouTube 无法访问的场景）
- 国内用户访问
- 私有版权内容

**COS 配置**：
- 访问权限：**公有读私有写**（防盗写）
- 地域：广州（`ap-guangzhou`）
- Bucket 格式：`your-bucket.cos.ap-guangzhou.myqcloud.com`

---

## 视频内容策略

### 不要用电影原片的原因
成品电影/剧集几乎都有**硬字幕（烧录进去）**，无法去除。用户看到的字幕是成品字幕，无法做"点击学单词"的功能。

### 正确方向：真实短视频
- YouTube 上大量"学中文/粤语"的真实对话片段
- 场景化：茶餐厅点餐、街头问路、超市购物等
- 有字幕但可导出处理

### 找视频的方法
```bash
# 搜索 YouTube 视频 ID
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

# 获取视频标题
for vid in ID1 ID2; do
  curl -s "https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v=$vid&format=json" | \
  python3 -c "import sys,json; print(vid, '|', json.load(sys.stdin).get('title',''))"
done
```

### 已确认可用的视频

| 场景 | YouTube ID | 标题 |
|---|---|---|
| 茶餐厅点餐 | `KW350JEVZ7U` | Speak Cantonese like a local in a Cantonese Restaurant |
| 日常生活 | `94LIuid2lRI` | Life of University Students in Hong Kong |
| 普通话日常 | `rl4rZbeXAdc` | Real Chinese Conversation: Order a drink |
| 买花（普通话） | `SGS8sfH11yg` | Real Chinese Conversation: Buy flowers |

---

## 字幕获取

### 方法1：YouTube 直接导出（推荐）
在 YouTube 播放页打开 CC → 设置 → 显示字幕，然后：
- 截图字幕区域
- 或复制文本整理成 JSON

### 方法2：yt-dlp（需服务器能访问 YouTube）
```bash
# 安装
pip install yt-dlp

# 下载字幕（vtt/srt）
yt-dlp --write-subs --skip-download https://www.youtube.com/watch?v=KW350JEVZ7U
```

### 字幕格式（填入 data.js）
```javascript
{
  id: 1,
  start: 2.0,   // 秒，小数点后1位
  end: 5.5,
  text: '你好，欢迎光临。',           // 原始文本
  jyutping: 'nei5 hou2, fun1 jing4', // 粤语拼音
  pinyin: 'nǐ hǎo, huān yíng',       // 普通话拼音
  translation: 'Hello, welcome.',     // 英文翻译
}
```

---

## 开发协作流程

### 本地修改 → GitHub
```bash
cd ~/.hermes/workspace/chinese-learning-app
git add .
git commit -m "feat: ..."
git push
# GitHub Pages 自动部署（约1-2分钟）
# https://qzw-alt.github.io/chinese-learning-app/
```

### GitHub Token
- Token 存在 `~/.git-credentials`
- Remote URL 嵌入 token：`https://TOKEN@github.com/qzw-alt/chinese-learning-app.git`

### 从头克隆
```bash
git clone https://github.com/qzw-alt/chinese-learning-app.git
```

---

## 文件结构

```
chinese-learning-app/
├── index.html          # 首页
├── watch.html          # 播放页（核心）
├── vocabulary.html     # 生词本
├── css/style.css       # 样式
├── js/
│   ├── config.js       # 配置（Supabase 等）
│   ├── app.js          # 全局 Alpine 状态
│   ├── data.js         # 视频数据 + 字幕 + 词典
│   ├── storage.js      # localStorage 封装
│   ├── supabase.js     # 用户系统
│   ├── audio.js        # 录音模块
│   └── components/
│       ├── player.js   # 播放器工厂（youtube/mp4/bilibili）
│       ├── subtitles.js # 字幕同步 + 点击逻辑
│       └── ui.js       # Modal、Toast 等
├── content/            # 内容 JSON（备用）
│   ├── videos.json
│   └── subtitles/
└── SPEC.md             # 开发方案文档
```

---

## Supabase 项目（用户系统）

- 项目地址：`https://github.com/qzw-alt/chinese-learning-app/tree/main/supabase`
- 已配置好 auth + database
- 无需修改，直接用

---

## 下一步

- [ ] 获取 `KW350JEVZ7U` 字幕数据（茶餐厅）
- [ ] 上传第一个 COS 视频
- [ ] 接入 COS 视频到 data.js
- [ ] 添加更多场景视频
