# MEMORY.md — 德米 长期记忆

> 最后更新：2026-04-28
> 每次会话优先读取此文件。这是唯一真实来源。

---

## 👤 伟烨 基本信息

- 名字：伟烨（德米）
- 时区：Asia/Shanghai (GMT+8)
- 飞书唯一联系方式
- 主要项目：医疗旅游网站（chinahospitalsguide.com）

---

## 🔴 当前最高优先级项目

### 医疗旅游网站
- **域名**：chinahospitalsguide.com
- **仓库（网站）**：qzw-alt/chinahospitalsguide
- **仓库（备份）**：qzw-alt/demi
- **本地路径**：`~/.hermes/workspace/chinahospitalsguide/`（已统一工作区）
- **部署方式**：编辑本地文件 → git push 到 chinalhospitalguide 仓库

### 长尾文章现状（2026-05-09）
- **已完成（5篇）**：jci-accredited-hospitals-china、best-hospitals-china-international-patients、how-to-book-hospital-appointment-china、guangzhou-medical-tourism-guide、dental-implants-china（之前已存在）
- **cron schedule**: 每天10:00触发（cron格式限制，内部通过状态文件判断是否真正执行）
- **执行方式**：cron携带seo-content-writer+humanizer skill，执行"写作→去AI→部署"完整流程
- **下一优先级**：从keyword-database.md的todo列表中选取

### 新闻栏目
- 每天1篇医疗新闻，蹭全球热点，对比中国现状，引导到服务
- **注意：07:00新闻写作已取消（2026-04-29），合并到09:00商业长尾写作一起做**

### 社交推广
- Reddit：账号已注册，养号中
- Quora：刚启动测试
- cronjob：每天 19:00 提醒

---

## ⏰ 定时任务（当前活跃）

| 时间(CST) | 任务 | job_id |
|-----------|------|--------|
| 06:00 | AI重大信息搜集报告 | bb3948605ac9 |
| 06:30 | 晨间记忆读取 | 916e3a888e14 |
| 07:00 | 每日医疗新闻写作 | dbbf2697de1a |
| 07:00 | 每日医疗内容融合写作 | 36b87bbe8424 |
| 09:30 | HN AI 热门速览 | 551ca375b0d7 |
| 10:00 | 商业长尾专题写作+部署（每2天） | e345e332f3ba |
| 19:00 | Quora+Reddit 推广提醒 | d69e49fa85af（origin）、dac47b26a5f7（feishu） |
| 20:00 | Google Search Console 未索引URL处理提醒 | aefd53f4e8ac |
| 22:00 | 每日记忆备份 | d506e6161153 |

---

## 🔑 API Keys / Skills

- **Kimi API**：sk-kim...NGGW
- **Tavily API**：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
- **GitHub Token**：ghp_mi...Dx9J
- **multi-search-engine**：已安装（17引擎，用户反馈好，视情况使用）

---

## 🗂️ 记忆文件位置

```
memory/
├── daily/           # 每日日志（YYYY-MM-DD.md）
├── projects/        # 各项目状态追踪
├── decisions/       # 关键决策记录
└── personals/      # 用户偏好、个人信息
```

> **规则：有用的信息直接存在文件里，不留在脑子里。每次会话结束写 daily log。**

---

## 📌 当前 HOT 待办（持续更新）

- [ ] **oriental-destiny.com 文案发布**（commit 已做，阻塞：今晚需处理 GitHub SSH 认证）
- [ ] Reddit 推广（账号养号中）
- [ ] Quora 推广（刚启动）
- [ ] 商业长尾5篇专题（进行中）
- [ ] `/treatments/` 404 修复
- [ ] Privacy/Terms 内容补全
- [ ] Course 课程填充

---

## ✅ 已完成重要事项

- [x] OpenClaw 已完全停用（2026-04-28）
- [x] 网站上线 chinalhospitalguide.com
- [x] 每日新闻栏目运行中
- [x] PayPal/WhatsApp 已开通
- [x] sitemap 提交 Google Search Console

---

_更新：2026-04-28 08:00_
