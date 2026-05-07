# 腾讯云 COS 配置流程（中文学习 App）

## 创建存储桶步骤

1. 腾讯云控制台 → 对象存储 COS → 创建存储桶
2. **地域**：广州（`ap-guangzhou`）— 离服务器近，延迟低
3. **名称**：全局唯一，如 `chineseflix-video`
4. **访问权限**：**公有读私有写** ✅ （"高风险"选项别碰）
5. 确认创建

> ⚠️ 实名认证必须完成才能创建存储桶。若"下一步"按钮不可点击，检查控制台右上角 → 账号信息 → 实名认证是否完成。

## 上传视频

1. 进入存储桶 → 上传文件 → 选择 MP4
2. 上传后复制对象的**访问链接**
3. 链接格式：`https://chineseflix-video.cos.ap-guangzhou.myqcloud.com/buy-flowers.mp4`

## 接入播放页

```javascript
// data.js
const videos = [
  {
    id: 'buy-flowers',
    videoUrl: 'https://your-bucket.cos.ap-guangzhou.myqcloud.com/video.mp4',
    title: '买花 — Real Chinese Conversation',
    duration: '5:33',
    difficulty: 'beginner'
  }
];
```

## 播放器代码（Plyr.js）

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/plyr@3/dist/plyr.css">
<video id="player" playsinline controls>
  <source src="COS_VIDEO_URL" type="video/mp4">
  <track kind="subtitles" label="中文" srclang="zh" src="subtitles.srt" default>
</video>
<script src="https://cdn.jsdelivr.net/npm/plyr@3/dist/plyr.min.js"></script>
<script>
  const player = new Plyr('#player');
</script>
```

## 费用预估（前期）

| 项目 | 费用 |
|------|------|
| COS 存储 5GB | ¥0.6/月 |
| CDN 流量 50GB | ¥25/月 |
| **合计** | **≈ ¥25/月** |

跑通后有压力再迁。
