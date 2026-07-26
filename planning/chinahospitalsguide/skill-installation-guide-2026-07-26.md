# Skill 安装与落地指导（给本地 agent 用）

**创建日期**: 2026-07-26
**Owner**: Weiye (chinahospitalsguide)
**目的**: 在本地电脑上落地 4 个开源 skill，搭建医疗旅游 OPC 的内容生产能力

---

## 🎯 业务背景（agent 必读）

**用户身份**: 医疗旅游协调人（OPC 一人公司），运营 chinahospitalsguide.com
**业务模式**: 帮海外患者对接中国医院（膝关节置换 / 脊髓损伤 / 癌症 / BCI 等）
**当前痛点**:
1. 网站定型但**推广内容为 0**，急需内容生产能力
2. 客户来源：🇨🇳🇸🇬🇲🇾🇮🇩 华语圈 / 🇷🇺🇧🇷🇳🇬🇳🇱🇩🇪 全球
3. 沟通渠道：WeChat + Telegram + Email（不再用 WhatsApp）
4. 服务档：L1 $49 / L2 $149 / L3 $399
5. 工具栈：DeepSeek + MiniMax M3 + Hermes + 翻墙机 + 国内机

**这个指导的目标**: 在**本地电脑**装 4 个工具，让用户能：
- 持续产出内容（文章 / 卡片）
- 自动生成短视频
- 多平台适配发布

---

## 📋 4 个 skill 总览

| ID | 名称 | GitHub URL | License | 类型 | 用途 |
|---|---|---|---|---|---|
| **S2** | Toonflow-app | https://github.com/HBAI-Ltd/Toonflow-app | Apache-2.0 | 桌面 app | 文案 → 自动生成短视频 |
| **S4** | creator-os fork | https://github.com/weid00360-bot/creator-os | 待查 | GitHub repo | 爆款拆解卡片结构化框架 |
| **S1** | AiToEarn | https://github.com/yikart/AiToEarn | MIT | Docker 服务 | 多平台一键发布（**这个先不装**）|
| **S2-alt** | HyperFrames | https://github.com/heygen-com/hyperframes | Apache-2.0 | 浏览器 / Node | "Write HTML. Render video." |

**优先装**: S2 (Toonflow) + S4 (creator-os fork)
**暂不装**: S1 (VPS RAM 不够 3.6GB / 跑不动)

---

## 🖥️ 用户本地电脑环境（先确认）

执行前**先问用户**：

1. **操作系统**: macOS / Windows / Linux?
2. **架构**: x86_64 / arm64 (Apple Silicon)?
3. **网络环境**: 国内 / 海外 / 都能访问 GitHub?
4. **已有工具**: Node.js? Python? Git? Docker Desktop?

```bash
# 检查命令
node --version  # 期望 >= 18
npm --version
git --version
docker --version  # 可选
```

---

## 🚀 Skill 1：Toonflow-app 安装（**最优先**）

### 用途
输入小说 / 剧本 / 营销文案 → 自动生成动画短剧视频（脚本 + 分镜 + 角色 + 视频 + 字幕）

### 安装步骤

#### 1. macOS

```bash
# 选项 A：Homebrew（推荐）
brew install --cask toonflow
# 如果 cask 没有，下载 dmg：
open https://github.com/HBAI-Ltd/Toonflow-app/releases/latest

# 选项 B：从源码
git clone https://github.com/HBAI-Ltd/Toonflow-app.git
cd Toonflow-app
# 读 README，找构建命令（可能是 npm/yarn/pnpm）
cat README.md | grep -i "install\|build\|start" | head -20
```

#### 2. Windows

```powershell
# 下载安装包
Invoke-WebRequest -Uri "https://github.com/HBAI-Ltd/Toonflow-app/releases/latest" -OutFile toonflow-setup.exe
# 或用 winget
winget install toonflow
```

#### 3. Linux

```bash
git clone https://github.com/HBAI-Ltd/Toonflow-app.git
cd Toonflow-app
# 读 README 找 Linux 安装指令
cat README.md | head -100
```

### 测试功能

1. 启动 Toonflow
2. 输入测试文案（**用这个**）：
```
A patient from Pakistan flew to Shanghai for brain tumor treatment.
The surgery was completed at Huashan Hospital. After recovery,
his family thanked the medical team.
```
3. 让 Toonflow 生成 30 秒短视频
4. 验证输出：是否包含脚本 / 分镜 / 视频 / 字幕
5. 截图保存到 `~/test-output/toonflow-test-001.png`

### 失败处理

如果安装失败，**按这个顺序排查**：
1. 检查网络：能否访问 GitHub releases
2. 检查 OS 版本是否在 Toonflow 支持列表
3. 读 README 的 "Troubleshooting" 或 "FAQ"
4. 找 GitHub Issues 搜类似问题
5. **给用户报告**："Toonflow 安装失败，原因是 X，建议 Y"

---

## 🚀 Skill 2：creator-os Fork（结构化内容框架）

### 用途
"爆款拆解卡片"框架 —— 把别人的爆款内容拆成结构化卡片，让你能**复用套路**做自己的内容

### 安装步骤

#### 1. Fork 仓库到用户 GitHub

```bash
# 浏览器打开让用户手动 fork（agent 不能直接操作 GitHub）：
# https://github.com/weid00360-bot/creator-os
# 点 Fork 按钮 → fork 到 weiye 的账号
```

#### 2. Clone 到本地

```bash
cd ~/projects  # 或用户指定目录
git clone https://github.com/<weiye-username>/creator-os.git
cd creator-os
ls -la
```

#### 3. 看仓库结构

```bash
# 重点看这个路径：
ls "爆款知识库/拆解卡片/" | head -20
# 里面有 015-蜗牛学长-赚大米skill.md 这类卡片
```

#### 4. **为用户定制**：把卡片结构迁移到 chinahospitalsguide

**新建目录结构**（在 fork 的仓库里）：

```
creator-os/
└── 爆款知识库/
    └── 拆解卡片/
        ├── 015-蜗牛学长-赚大米skill.md  (原仓库已有)
        └── chg/                          # 新建：用户自己的卡片
            ├── 001-华山医院-BCI手术-海外患者关注.md
            ├── 002-膝关节置换-费用对比.md
            ├── 003-脊髓损伤-康复路径.md
            └── ...
```

### 测试功能

1. 新建一张测试卡片 `001-test-card.md`
2. 模板参考 `015-蜗牛学长-赚大米skill.md` 的结构
3. 填写测试内容（用户业务相关）
4. 验证：用 markdown linter / 渲染器看效果

### 卡片模板（直接给用户用）

```markdown
# 拆解卡 #00X · [你的选题标题]

> 来源：[参考来源]
> 数据：赞 X / 收藏 X / 转发 X

## 选题
- 话题：[一句话讲清这条内容讲什么]
- 钩子：[为什么有人想看——震惊？好奇？实用？]
- 类型：[内容类型分类]

## 文案结构
1. [第 1 段：钩子]
2. [第 2 段：核心价值]
3. [第 3 段：证明 / 案例]
4. [第 4 段：收尾 + CTA]

## 套路提炼
- [这条内容的核心套路 1]
- [套路 2]
- [套路 3]

## ♻️ 可复用点
- [对用户业务的启示 1]
- [启示 2]
```

---

## 🚀 Skill 3：HyperFrames（HTML → 视频，可选）

### 用途
写 HTML → 自动渲染成视频。**为 AI agent 设计** —— 让 LLM 生成 HTML，直接转视频。

### 安装步骤

```bash
# 需要 Node.js 18+
git clone https://github.com/heygen-com/hyperframes.git
cd hyperframes
npm install
npm run dev  # 或 README 里的命令
```

### 测试功能

1. 启动后访问本地 URL（通常是 http://localhost:3000）
2. 写一个简单 HTML 测试页（含图片 + 文字 + 动画）
3. 看是否能渲染成视频
4. 验证：输出 mp4 / webm / gif？

---

## 🚀 Skill 4：AiToEarn（**暂不安装，标记**）

### 不安装的原因

- 用户 VPS 只有 **3.6 GB RAM**，跑不动 AiToEarn 的完整服务栈（Next.js + Nest.js + MongoDB + Redis）
- 需要先升级 VPS 到 8GB+（每月多花 $10-20）
- **现在用户更缺的是"产出"不是"产能"**

### 何时再考虑

- 用户已经稳定产出 10+ 内容卡片
- 用户已经做了 5+ 个 Toonflow 视频
- 用户明确说"内容够了，需要批量发布"

### 如果用户坚持要装

**升级 VPS 计划**：
```
当前: 3.6 GB RAM, 36 GB disk
目标: 8 GB RAM, 80 GB disk
预估: $10-20/月 升级费
服务商推荐: AWS Lightsail / Vultr / DigitalOcean / 阿里云
```

---

## 🧪 整体测试流程（agent 必跑）

### 第一天：装 Toonflow + 测试

```bash
[ ] 问用户操作系统
[ ] 检查环境（Node / Git）
[ ] 安装 Toonflow
[ ] 跑测试：华山医院 BCI 文案 → 30 秒视频
[ ] 把生成的视频截图给用户看
[ ] 报告：成功 / 失败 + 原因 + 下一步建议
```

### 第二天：Fork creator-os + 写第一张卡片

```bash
[ ] 让用户在浏览器 fork 仓库
[ ] git clone 到本地
[ ] 看仓库结构
[ ] 用模板创建 chg/001-test-card.md
[ ] 让用户填写内容
[ ] 把卡片 markdown 渲染截图给用户看
[ ] 报告
```

### 第三天：决定是否装 HyperFrames

```bash
[ ] 问用户：HyperFrames 还需要吗？
[ ] 如果要：装 + 测试
[ ] 如果不要：归档
```

---

## 📁 输出位置（agent 必须遵守）

所有测试产物存到：

```
~/test-output/
├── toonflow-test-001.png        # Toonflow 测试截图
├── toonflow-test-001.mp4        # Toonflow 测试视频（如有）
├── creator-os-fork-test.md      # creator-os fork 验证
├── hyperframes-test-001.mp4     # HyperFrames 测试（如有）
└── INSTALL_REPORT.md            # 安装报告（agent 必出）
```

---

## 📋 必须出的报告（agent 完成后）

写到 `~/test-output/INSTALL_REPORT.md`：

```markdown
# 安装报告 · [日期]

## 装了哪些 skill

| Skill | 状态 | 备注 |
|---|---|---|
| Toonflow | ✅ 成功 / ❌ 失败 | [原因] |
| creator-os fork | ✅ 成功 / ❌ 失败 | [原因] |
| HyperFrames | ✅ 成功 / ❌ 失败 | [原因] |
| AiToEarn | ⏸ 暂不装 | VPS RAM 不够 |

## 每个 skill 测试了什么

### Toonflow
- 测试文案：[填入]
- 输出：[截图 / 视频路径]
- 评价：[能否用、有什么限制]

### creator-os fork
- Fork URL：[填入]
- 第一张卡片：[填入]
- 评价：[结构是否够用]

## 给用户的建议

1. [下一步建议 1]
2. [下一步建议 2]
3. [下一步建议 3]

## 已知问题

- [问题 1]
- [问题 2]
```

---

## ⚠️ 边界规则（agent 必读）

### 不要做

- ❌ 不要访问用户的真实客户数据
- ❌ 不要替用户做内容决策（选题 / 措辞）
- ❌ 不要 commit 到项目仓库（chinahospitalsguide 跟 creator-os fork 是两码事）
- ❌ 不要上传视频到任何平台（agent 没权限）
- ❌ 不要花钱（升级 VPS / 订阅服务 都要先问用户）

### 要做

- ✅ 先问用户操作系统
- ✅ 失败时给清晰错误信息
- ✅ 成功后给清晰下一步建议
- ✅ 截图 / 视频给用户**亲眼看**
- ✅ 所有产物存到 `~/test-output/` 不污染用户项目

---

## 📞 出问题时怎么办

如果遇到：
- **网络问题**（GitHub 访问不到）→ 试 GitHub 镜像 / 让用户用翻墙机
- **OS 不兼容** → 找替代 skill 或用 Docker
- **资源不够**（RAM / Disk）→ 报告用户，不擅自升级
- **API key 缺失** → 不擅自注册 / 不擅自填，**问用户**

---

**结束 · 等用户确认后开始执行**