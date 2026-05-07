# 关键信息变更记录 CHANGELOG

> 记录所有关键信息的变更历史，append-only 追加写入
> 每次更新只追加新条目，保留完整时间线

---

## 2026-04-05 项目状态更新

- **PayPal**：✅ 已开通
- **WhatsApp**：✅ 已开通并正常使用
- **网站部署**：✅ 确认正常运行
- **Quora推广**：🔄 新增待测试渠道

---

## 战略方向决策（重要）

- 2026-03-23：**定位转型：不打"医疗旅游"赛道，改打"中国就医攻略导航"**
  - 核心词：China hospital guide, Medical coordinator China, Healthcare advisor
  - 原因：医疗旅游大机构太多，拼不过；长尾攻略词是蓝海
  - 详见：`战略方向决策_定位与内容转型.md`

- 2026-03-23：**内容方向转型：弱化省钱，强化安全/专业/服务价值**
  - 移除首页"Save 50-80%"等元数据
  - 移除"Real Patient Savings"区块
  - Services页完全重写
  - 未来新文章统一走"安全+专业+服务"方向
  - 详见：`战略方向决策_定位与内容转型.md`

## 网站仓库地址

- 2026-03-22：**从 demi 更新为 chinahospitalsguide**
  ← 原因：之前 demi 同时存储网站文件和记忆文件，导致仓库混乱。决定分开管理——demi=记忆备份，chinahospitalsguide=网站部署

## 备份仓库地址

- 2026-03-22：**demi** (https://github.com/qzw-alt/demi)
  ← 原因：专门用于备份德米的记忆和所有工作文件

## 仓库分工

- 2026-03-22：
  - `chinahospitalsguide` = 网站仓库（只上传网站文件：HTML/CSS/JS/图片等）
  - `demi` = 备份仓库（备份所有文件，含网站文件备份）
  ← 原因：之前混用一个仓库，导致网站部署和记忆备份冲突

## 部署流程

- 2026-03-22 更新：
  1. 编辑 `/root/.openclaw/workspace/website/` 里的文件
  2. 克隆 `chinahospitalsguide` 仓库
  3. 复制 website/ 下的文件到克隆目录
  4. 推送到 `chinahospitalsguide`
  5. 等待5分钟检查网站

## 记忆架构

- 2026-03-22：从旧的 HOT/WARM/COLD 升级为 4-Layer 架构
  - Layer 1: Session（会话上下文）
  - Layer 2: Short-Term（14天日志）
  - Layer 3: Long-Term（永久知识）
  - Layer 4: Reference（参考/SOP）
  ← 改进自 Moltbook m/memory 社区讨论，参考存储系统的 tiered storage 理论

## API Keys

- 2026-03-22 更新：
  - Kimi API: sk-kimi-iGuVj23Mgkz5ZSKkW9vdkVTg6PQY5FIlpTiPn8ryhrGA8jO4UyVWredtEfbDNGGW
  - Tavily API: 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

## OpenClaw 版本

- 2026-03-22：从 2026.3.11 升级到 2026.3.13
  ← 伟烨帮助升级的

## 模型版本

- 2026-03-22：更新为 minimax/MiniMax-M2.7
  ← 伟烨更新配置的

---
