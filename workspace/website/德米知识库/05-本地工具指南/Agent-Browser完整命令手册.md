# Agent Browser 完整命令手册

> 创建时间：2026-03-15  
> 适用对象：大德米（本地Mac环境）  
> 版本：v1.0

---

## 快速参考卡

### 核心工作流
```bash
# 1. 打开页面
agent-browser open <URL>

# 2. 获取页面元素
agent-browser snapshot -i

# 3. 交互操作（使用@ref）
agent-browser click @e1
agent-browser fill @e2 "文本"

# 4. 关闭浏览器
agent-browser close
```

---

## 完整命令列表

### 导航命令

| 命令 | 说明 | 示例 |
|------|------|------|
| `open <URL>` | 打开网页 | `agent-browser open https://zhihu.com` |
| `back` | 后退 | `agent-browser back` |
| `forward` | 前进 | `agent-browser forward` |
| `reload` | 刷新 | `agent-browser reload` |
| `close` | 关闭浏览器 | `agent-browser close` |

### 页面分析

| 命令 | 说明 | 示例 |
|------|------|------|
| `snapshot` | 完整页面结构 | `agent-browser snapshot` |
| `snapshot -i` | 仅交互元素（推荐） | `agent-browser snapshot -i` |
| `snapshot -c` | 紧凑输出 | `agent-browser snapshot -c` |
| `snapshot -d 3` | 限制深度 | `agent-browser snapshot -d 3` |
| `snapshot -s "#main"` | CSS选择器范围 | `agent-browser snapshot -s "#content"` |

### 点击操作

| 命令 | 说明 | 示例 |
|------|------|------|
| `click @ref` | 单击 | `agent-browser click @e5` |
| `dblclick @ref` | 双击 | `agent-browser dblclick @e3` |
| `focus @ref` | 聚焦 | `agent-browser focus @e1` |
| `hover @ref` | 悬停 | `agent-browser hover @e7` |

### 输入操作

| 命令 | 说明 | 示例 |
|------|------|------|
| `fill @ref "text"` | 清空并输入 | `agent-browser fill @e2 "hello"` |
| `type @ref "text"` | 直接输入（不清空） | `agent-browser type @e2 "world"` |
| `press <key>` | 按键 | `agent-browser press Enter` |
| `press Ctrl+a` | 组合键 | `agent-browser press Control+a` |
| `select @ref "value"` | 下拉选择 | `agent-browser select @e4 "option1"` |

### 复选框/单选框

| 命令 | 说明 | 示例 |
|------|------|------|
| `check @ref` | 勾选 | `agent-browser check @e8` |
| `uncheck @ref` | 取消勾选 | `agent-browser uncheck @e8` |
| `is checked @ref` | 检查状态 | `agent-browser is checked @e8` |

### 等待命令

| 命令 | 说明 | 示例 |
|------|------|------|
| `wait @ref` | 等待元素出现 | `agent-browser wait @e10` |
| `wait 2000` | 等待毫秒 | `agent-browser wait 2000` |
| `wait --text "Success"` | 等待文本 | `agent-browser wait --text "发布成功"` |
| `wait --url "/dashboard"` | 等待URL | `agent-browser wait --url "/home"` |
| `wait --load networkidle` | 等待网络空闲 | `agent-browser wait --load networkidle` |

### 滚动操作

| 命令 | 说明 | 示例 |
|------|------|------|
| `scroll down 500` | 向下滚动 | `agent-browser scroll down 500` |
| `scroll up 300` | 向上滚动 | `agent-browser scroll up 300` |
| `scrollintoview @ref` | 滚动到元素 | `agent-browser scrollintoview @e15` |

### 获取信息

| 命令 | 说明 | 示例 |
|------|------|------|
| `get text @ref` | 获取文本 | `agent-browser get text @e1` |
| `get html @ref` | 获取HTML | `agent-browser get html @e2` |
| `get value @ref` | 获取输入值 | `agent-browser get value @e3` |
| `get attr @ref href` | 获取属性 | `agent-browser get attr @e4 href` |
| `get title` | 获取页面标题 | `agent-browser get title` |
| `get url` | 获取当前URL | `agent-browser get url` |
| `get count ".item"` | 计数元素 | `agent-browser get count ".article"` |

### 检查状态

| 命令 | 说明 | 示例 |
|------|------|------|
| `is visible @ref` | 是否可见 | `agent-browser is visible @e1` |
| `is enabled @ref` | 是否可用 | `agent-browser is enabled @e2` |

### 截图和PDF

| 命令 | 说明 | 示例 |
|------|------|------|
| `screenshot` | 截图到stdout | `agent-browser screenshot > page.png` |
| `screenshot path.png` | 保存截图 | `agent-browser screenshot screenshot.png` |
| `screenshot --full` | 全页截图 | `agent-browser screenshot --full fullpage.png` |
| `pdf output.pdf` | 保存PDF | `agent-browser pdf page.pdf` |

### 视频录制

| 命令 | 说明 | 示例 |
|------|------|------|
| `record start ./demo.webm` | 开始录制 | `agent-browser record start ./demo.webm` |
| `record stop` | 停止录制 | `agent-browser record stop` |
| `record restart ./take2.webm` | 重新开始 | `agent-browser record restart ./new.webm` |

### Cookie和存储

| 命令 | 说明 | 示例 |
|------|------|------|
| `cookies` | 获取所有cookie | `agent-browser cookies` |
| `cookies set name value` | 设置cookie | `agent-browser cookies set session abc123` |
| `cookies clear` | 清除cookie | `agent-browser cookies clear` |
| `storage local` | 获取localStorage | `agent-browser storage local` |
| `storage local key` | 获取特定键 | `agent-browser storage local user_id` |
| `storage local set k v` | 设置值 | `agent-browser storage local set theme dark` |

### 状态管理（关键！）

| 命令 | 说明 | 示例 |
|------|------|------|
| `state save auth.json` | 保存登录状态 | `agent-browser state save zhihu_auth.json` |
| `state load auth.json` | 加载登录状态 | `agent-browser state load zhihu_auth.json` |

### 会话管理

| 命令 | 说明 | 示例 |
|------|------|------|
| `--session name` | 使用独立会话 | `agent-browser --session test1 open ...` |
| `session list` | 列出会话 | `agent-browser session list` |

### 浏览器设置

| 命令 | 说明 | 示例 |
|------|------|------|
| `set viewport 1920 1080` | 设置视口 | `agent-browser set viewport 1920 1080` |
| `set device "iPhone 14"` | 模拟设备 | `agent-browser set device "iPhone 14"` |
| `set geo 37.7749 -122.4194` | 设置位置 | `agent-browser set geo 39.9042 116.4074` |
| `set offline on` | 离线模式 | `agent-browser set offline on` |
| `set headers '{"X-Key":"v"}'` | 自定义头 | `agent-browser set headers '{"Auth":"token"}'` |
| `set media dark` | 深色模式 | `agent-browser set media dark` |

### 调试命令

| 命令 | 说明 | 示例 |
|------|------|------|
| `open URL --headed` | 显示浏览器窗口 | `agent-browser open zhihu.com --headed` |
| `console` | 查看控制台 | `agent-browser console` |
| `errors` | 查看页面错误 | `agent-browser errors` |
| `highlight @ref` | 高亮元素 | `agent-browser highlight @e1` |
| `trace start` | 开始追踪 | `agent-browser trace start` |
| `trace stop trace.zip` | 保存追踪 | `agent-browser trace stop debug.zip` |

---

## 平台特定操作指南

### 知乎

```bash
# 保存登录状态（首次）
agent-browser open https://www.zhihu.com/signin
# 手动登录后...
agent-browser state save zhihu_auth.json

# 后续自动登录
agent-browser state load zhihu_auth.json
agent-browser open https://www.zhihu.com

# 发布文章
agent-browser click @write_article  # 或找到写文章按钮的ref
agent-browser fill @title_input "文章标题"
agent-browser fill @content_editor "文章内容..."
agent-browser click @publish_button
agent-browser wait --text "发布成功"
```

### 小红书

```bash
# 加载登录状态
agent-browser state load xiaohongshu_auth.json
agent-browser open https://www.xiaohongshu.com

# 发布图文
agent-browser click @publish_button
agent-browser upload @image_upload ./cover.jpg
agent-browser fill @title_input "标题"
agent-browser fill @content_editor "正文内容"
agent-browser click @publish_now
```

### Twitter/X

```bash
agent-browser state load twitter_auth.json
agent-browser open https://twitter.com

# 发推文
agent-browser click @compose_tweet
agent-browser fill @tweet_text "推文内容"
agent-browser click @tweet_button
```

### YouTube

```bash
agent-browser state load youtube_auth.json
agent-browser open https://studio.youtube.com

# 上传视频
agent-browser click @upload_button
agent-browser upload @file_input ./video.mp4
agent-browser fill @title "视频标题"
agent-browser fill @description "视频描述..."
agent-browser fill @tags "tag1, tag2, tag3"
agent-browser click @publish_button
```

---

## 实用脚本模板

### 模板1：自动发布文章

```bash
#!/bin/bash
# publish_article.sh

PLATFORM=$1      # zhihu, xiaohongshu, etc.
TITLE=$2
CONTENT=$3
AUTH_FILE="${PLATFORM}_auth.json"

# 加载认证
agent-browser state load $AUTH_FILE

# 打开平台
case $PLATFORM in
    "zhihu")
        agent-browser open https://zhuanlan.zhihu.com/write
        agent-browser fill @title_input "$TITLE"
        agent-browser fill @content_editor "$CONTENT"
        agent-browser click @publish_button
        ;;
    "xiaohongshu")
        agent-browser open https://www.xiaohongshu.com/explore
        agent-browser click @publish
        agent-browser fill @title "$TITLE"
        agent-browser fill @content "$CONTENT"
        agent-browser click @publish_now
        ;;
esac

# 等待发布完成
agent-browser wait --text "发布成功" --timeout 10000
echo "发布完成！"
```

### 模板2：批量获取数据

```bash
#!/bin/bash
# scrape_data.sh

URL=$1
SELECTOR=$2

agent-browser open $URL

# 获取所有匹配元素
COUNT=$(agent-browser get count "$SELECTOR")
echo "找到 $COUNT 个元素"

# 遍历获取文本
for i in $(seq 1 $COUNT); do
    TEXT=$(agent-browser get text "${SELECTOR}:nth-of-type($i)")
    echo "$i: $TEXT"
done
```

### 模板3：定时检查任务

```bash
#!/bin/bash
# check_notifications.sh

agent-browser state load zhihu_auth.json
agent-browser open https://www.zhihu.com/notifications

# 获取通知数量
NOTIF_COUNT=$(agent-browser get text @notification_count)

if [ "$NOTIF_COUNT" != "0" ]; then
    echo "您有 $NOTIF_COUNT 条新通知"
    # 发送提醒（可以调用API）
else
    echo "没有新通知"
fi
```

---

## 故障排查

### 元素找不到

```bash
# 1. 重新获取snapshot
agent-browser snapshot -i

# 2. 使用CSS选择器
agent-browser find ".button.primary" click

# 3. 使用文本查找
agent-browser find text "发布" click

# 4. 等待元素加载
agent-browser wait @e10 --timeout 5000
```

### 登录状态失效

```bash
# 1. 检查当前状态
agent-browser get url

# 2. 如果跳转到登录页，重新登录
agent-browser open https://www.zhihu.com/signin
# ... 手动登录 ...
agent-browser state save zhihu_auth.json
```

### 页面加载慢

```bash
# 增加超时时间
agent-browser open https://example.com --timeout 30000

# 等待网络空闲
agent-browser wait --load networkidle

# 等待特定元素
agent-browser wait @main_content --timeout 20000
```

---

## 最佳实践

1. **始终保存登录状态**
   ```bash
   agent-browser state save platform_auth.json
   ```

2. **使用--headed调试**
   ```bash
   agent-browser open URL --headed
   ```

3. **添加错误处理**
   ```bash
   agent-browser click @button || echo "点击失败"
   ```

4. **定期更新snapshot**
   - 页面导航后重新snapshot
   - 动态加载内容后重新snapshot

5. **使用JSON输出解析**
   ```bash
   agent-browser snapshot -i --json | jq '.elements[] | select(.type == "button")'
   ```

---

## 参考

- **完整文档**: `/root/.openclaw/workspace/skills/agent-browser/SKILL.md`
- **GitHub**: https://github.com/vercel-labs/agent-browser
- **CLI-Anything配合**: 见 `CLI-Anything详细运用指南.md`

---

*创建者：德米*  
*最后更新：2026-03-15*
