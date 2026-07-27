# chinahospitalsguide · 改后 audit 速查表

> 这是 `weiye-collaboration-style` 的 support file。
> 触发场景：伟烨说"已修改完了 / 你再帮我审计一下 / 你看看是不是改完了"。

---

## 🚦 操作原则（来自 v1.1.0 反模式 5）

**不要全量重扫**。**只对上次报告里的 N 个问题做 diff** + 发现新增的"非上次范围"问题时**单独标注**。

---

## 📋 标准 checklist

```bash
# 1. sync
cd ~/chinahospitalsguide
git fetch origin 2>&1 | tail -3
git rev-list --left-right --count origin/master...master  # 落后多少 commit
git pull origin master 2>&1 | tail -10
git log --oneline <上次audit时的commit>..origin/master   # 伟烨这段做了什么
```

### 2. 对照上次报告的 N 个问题重扫

| 上次标的问题 | 这次怎么扫 |
|---|---|
| WhatsApp 残留 | `re.findall(r'(wa\.me/|whatsapp://|api\.whatsapp)', ...)` —— **严格 pattern**，区分"提到 WhatsApp"和"WhatsApp 链接" |
| `/treatments/` 死链 | `re.findall(r'(?:href\|src)="[^"]*?/treatments/[^"]*"', ...)` |
| 旧档名残留（如 Pre-Arrival）| 区分"\bPre-Arrival\s+Coordination\b"（档名）vs "pre-arrival phase"（描述性）|

### 3. **核验**：扫描数字异常高（>50%）= 大概率 false positive

如果扫出 "X 文件有 Y"，**先抽 2-3 个文件验证**：

```bash
# 例：扫到 158 文件含 WhatsApp，先看 3 个：
for f in <3个文件>; do
  echo "=== $f ==="
  grep -E 'wa\.me/|whatsapp' "$f" | head -3
done
```

如果发现"提到 WhatsApp 文字但无链接"在计数 = false positive，**用更精确 regex 重扫**。

---

## 📊 报告格式

跟上次报告**同样的结构**，但**只重扫上次问题**：

```
# audit 报告 · 改完后

## 上次的问题修复情况

| 上次问题 | 修复情况 | 详情 |
|---|---|---|
| WhatsApp 残留 (158 文件) | ✅ 完全修复 | 0 文件含 wa.me/ 链接 |
| /treatments/ 死链 (10 文件) | ✅ 完全修复 | 0 引用 + 加了 _redirects 兜底 |
| Pre-Arrival 旧档名 (46 处) | 🟢 大幅修复 (剩 14 文件) | 全部在 reports/*.html（scripts/generate-report.js 硬编码） |

## Bonus 发现（新问题，不在上次范围）

1. **mobile-bottom-bar .njk 没 include**：35 .html 有 bar，0 .njk include → 下次 build 会丢
2. **commit 7ac5d98 的 _redirects 模式**（删 treatments 时的双保险）值得记录在红线里
```

---

## 🚨 触发"全量 audit"的判断

| 场景 | 动作 |
|---|---|
| 伟烨说"已修改完了" + 上次有完整报告 | **diff-style audit**（本 checklist）|
| 伟烨说"全面审计一下" / "完整审查" | **全量 audit**（第一次或很久没审计）|
| 上一份报告已 7+ 天 / 议题已变 | **全量 audit** |
| 距离上次 audit < 7 天 + 议题未变 | **diff-style audit** |

---

## 🔍 chinahospitalsguide 特定 .njk 列表（每次必看）

| 模板 | 文件 |
|---|---|
| 主页 | `index.njk` |
| 关于 | `about.njk` |
| 服务详情 | `services.njk` |
| 价目 | `pricing.njk` |
| 医院 | `hospitals.njk` |
| 流程 | `how-it-works.njk` |
| 联系（旧） | `contact.njk` |
| 联系（新） | `contact-new.njk` |

每次 audit 必看它们跟实际编译出的 .html **是否一致**。如果 .html 跟 .njk 内容差异大，**意味着有人手改了 .html 但没改 .njk，下次 build 会丢**。

---

## 📁 关联文件

- `weiye-collaboration-style/SKILL.md` v1.1.0 → 红线 9-12
- `medical-tourism-site-ops/SKILL.md` → 静态站 deploy + build 流程
