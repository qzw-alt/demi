# 🤖 AI 团队架构方案

> 创建时间：2026-03-13  
> 创建者：德米 & 伟烨  
> 版本：v1.0

---

## 🎯 核心理念

构建一个**全自动 AI 内容生产与分发团队**，实现从文案创作到内容发布的端到端自动化。

---

## 👥 团队架构

```
┌─────────────────────────────────────────────────────────────┐
│                      伟烨（人类指挥官）                        │
│                         ↓ 提出需求                            │
├─────────────────────────────────────────────────────────────┤
│                      德米（AI 指挥官）                         │
│                    统筹规划、任务分配、质量审核                  │
└─────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        ↓                     ↓                     ↓
┌───────────────┐   ┌─────────────────┐   ┌─────────────────┐
│   豆包妹妹     │   │   内容生产 Agent  │   │   内容分发 Agent  │
│  （文案写手）   │   │  （Mac + 本地软件） │   │ （Agent Browser） │
├───────────────┤   ├─────────────────┤   ├─────────────────┤
│ • 脚本创作     │   │ • GIMP          │   │ • 知乎           │
│ • 博客文章     │   │ • Kdenlive      │   │ • 小红书         │
│ • 社媒文案     │   │ • LibreOffice   │   │ • Twitter        │
│ • 视频脚本     │   │ • 其他创意软件    │   │ • YouTube        │
│               │   │                 │   │ • 其他平台        │
│ 方式：API调用  │   │ 方式：CLI-Anything│   │ 方式：Cookie登录  │
└───────────────┘   └─────────────────┘   └─────────────────┘
```

---

## 🛠️ 核心技能栈

### 1. CLI-Anything（内容生产）
- **功能**：将任意本地软件变成 Agent 可控的 CLI 工具
- **安装位置**：本地 Mac 电脑
- **控制软件**：
  - **GIMP** - 图片处理、批量编辑、加水印
  - **Kdenlive** - 视频剪辑、自动生成视频
  - **LibreOffice** - 文档生成、PDF 转换
  - **Audacity** - 音频处理
  - **Blender** - 3D 动画（可选）
- **GitHub**：https://github.com/HKUDS/CLI-Anything

### 2. Agent Browser（内容分发）
- **功能**：浏览器自动化，控制社媒账号
- **安装位置**：本地 Mac 电脑
- **登录方式**：Cookie 持久化（一次登录，长期有效）
- **支持平台**：
  - 知乎
  - 小红书
  - Twitter/X
  - YouTube
  - 其他网页版社媒
- **优势**：本地住宅 IP，绕过服务器 IP 风控

### 3. 豆包 API（文案创作）
- **功能**：文案生成、脚本创作
- **使用方式**：API 直接调用
- **优势**：无需浏览器控制，快速稳定

---

## 🔄 工作流程

### 完整内容生产流程

```
伟烨提出需求
    ↓
德米理解并拆解任务
    ↓
├─→ 豆包妹妹：生成文案/脚本
│       ↓
│   返回：标题、正文、标签、发布文案
│
├─→ 内容生产 Agent（Mac）
│       ↓
│   根据文案制作：
│   • 配图（GIMP 批量处理）
│   • 视频（Kdenlive 自动剪辑）
│   • 文档（LibreOffice 生成 PDF）
│
└─→ 内容分发 Agent（Mac）
        ↓
    使用已保存 Cookie 自动发布：
    • 知乎文章
    • 小红书图文
    • Twitter 推文
    • YouTube 视频
        ↓
德米审核发布结果
    ↓
伟烨最终确认
```

---

## 🏗️ 实施计划

### 阶段一：前期准备（购买 Mac 后）

| 任务 | 负责人 | 说明 |
|------|--------|------|
| 安装 OpenClaw Node | 德米远程协助 | 让德米可以远程控制 Mac |
| 安装 Chrome/Firefox | 本地操作 | 浏览器环境 |
| 登录所有社媒账号 | 本地操作 | 知乎、小红书、Twitter、YouTube |
| 保存 Cookie/Session | 德米配置 | 确保登录状态持久化 |
| 安装 CLI-Anything | 德米远程安装 | 连接所有本地软件 |
| 安装创意软件 | 本地操作 | GIMP、Kdenlive、LibreOffice |

### 阶段二：自动化配置

| 任务 | 说明 |
|------|------|
| 配置 Agent Browser | 加载已保存的 Cookie |
| 配置 CLI-Anything | 测试各软件的 CLI 控制 |
| 配置豆包 API | 设置 API Key |
| 编写自动化脚本 | 端到端工作流 |

### 阶段三：测试运行

| 测试项 | 目标 |
|--------|------|
| 文案生成 | 豆包生成一篇博客文章 |
| 图片制作 | GIMP 批量处理医院图片 |
| 视频制作 | Kdenlive 自动生成宣传视频 |
| 内容发布 | Agent Browser 自动发布到各平台 |
| 端到端测试 | 从需求到发布的完整流程 |

---

## 💡 关键技术点

### Cookie 持久化方案
```bash
# 保存登录状态
agent-browser save-cookies --file zhihu_cookies.json
agent-browser save-cookies --file xiaohongshu_cookies.json

# 加载登录状态
agent-browser load-cookies --file zhihu_cookies.json
```

### 远程控制方案
| 方案 | 优先级 | 说明 |
|------|--------|------|
| OpenClaw Node | ⭐⭐⭐ 首选 | 在 Mac 安装 OpenClaw，德米直接控制 |
| SSH | ⭐⭐ 备选 | 命令行控制 |
| 定时脚本 | ⭐⭐ 备选 | Mac 本地跑 cron，德米推送任务 |

### CLI-Anything 使用示例
```bash
# 创建视频项目
cli-anything-kdenlive project new --name "MedicalTourism_Promo" --profile hd1080p30

# 导入素材
cli-anything-kdenlive bin import ./hospital_video.mp4 --name "Hospital"
cli-anything-kdenlive bin import ./voiceover.wav --name "Voice"

# 添加特效
cli-anything-kdenlive filter add 0 0 fade_in_video -p duration=2.0

# 导出视频
cli-anything-kdenlive export xml -o promo_video.kdenlive
```

---

## ✅ 优势总结

| 优势 | 说明 |
|------|------|
| **全自动** | 从文案到发布的端到端自动化 |
| **绕过风控** | 本地住宅 IP，避免服务器 IP 被封 |
| **一次配置** | 登录一次，Cookie 长期有效 |
| **灵活扩展** | 可随时添加新的软件和平台 |
| **成本可控** | 主要成本是 Mac 电脑，无额外 API 费用 |

---

## 📋 待办清单

- [ ] 购买 Mac 电脑
- [ ] 安装 OpenClaw Node
- [ ] 配置社媒账号登录
- [ ] 安装 CLI-Anything
- [ ] 安装 GIMP、Kdenlive、LibreOffice
- [ ] 配置豆包 API
- [ ] 编写自动化脚本
- [ ] 端到端测试

---

## 🔗 相关资源

- **CLI-Anything GitHub**: https://github.com/HKUDS/CLI-Anything
- **Agent Browser 文档**: `/root/.openclaw/workspace/skills/agent-browser/SKILL.md`
- **本地安装路径**: `/root/.openclaw/workspace/CLI-Anything/`

---

*最后更新：2026-03-13*  
*记录者：德米*
