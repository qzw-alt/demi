# 🌡️ WARM MEMORY - 稳定配置和偏好

> 最后更新: 2026-03-04
> 更新频率: 偏好变更时
> 管理方式: 稳定配置，长期保留

---

## 👤 用户偏好 (伟烨)

| 项目 | 值 |
|------|-----|
| **名字** | 伟烨 |
| **时区** | Asia/Shanghai (GMT+8) |
| **特点** | 有很多好点子，正在创业中 |
| **沟通风格** | 直接、高效 |
| **记忆偏好** | 详细记录，不压缩 |

---

## 🛠️ 系统配置

### 已安装 Skills
- agent-browser
- memory-tiering ⬅️ 刚启用
- learning
- web-search
- social-media-management
- multi-search-engine
- lenny-skills

### API Keys (引用位置)
- Kimi API: 见 TOOLS.md
- Tavily API: 见 TOOLS.md

### 搜索策略
1. **Multi Search** - 广度搜索，多来源对比
2. **Tavily** - 精准搜索，深度分析

### ⚠️ 网站部署强制检查清单
每次部署前必须执行：
- [ ] `docs/` 内容已同步到根目录 (`cp -r docs/* .`)
- [ ] 根目录 `index.html` 是最新版本
- [ ] CNAME 文件在根目录
- [ ] 提交并推送后等待2-5分钟
- [ ] 用 `curl -H "Cache-Control: no-cache"` 验证

**根本原因**: GitHub Pages 默认从根目录部署，不是 `docs/` 目录！
**参考**: `memory/踩坑记录_部署篇.md`

---

## 📋 项目清单

| 项目 | 状态 | 关键文件 |
|------|------|---------|
| 医疗旅游 | 🟢 运营中 | PROJECT_INDEX.md |
| 龙康劲 | 🟢 运营中 | memory/龙康劲_index.md |

---

## 🔗 快速链接

- 项目速查: PROJECT_INDEX.md
- 长期记忆: MEMORY.md
- 医疗旅游资源: memory/医疗旅游_医院资源库.md

---

*此文件记录稳定配置，只在变更时更新*
