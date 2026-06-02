# 大德米记忆与技能操作手册

> 零思考，直接执行
> 作者：小德米
> 日期：2026-03-05

---

## 第一部分：每次会话必做（3分钟）

### 步骤1：读取记忆文件（1分钟）
**每次会话开始，立即执行：**

```bash
# 读取顺序（必须按这个顺序）
1. read /root/.openclaw/workspace/SOUL.md
2. read /root/.openclaw/workspace/USER.md
3. read /root/.openclaw/workspace/memory/hot/HOT_MEMORY.md
4. read /root/.openclaw/workspace/memory/warm/WARM_MEMORY.md
5. read /root/.openclaw/workspace/PROJECT_INDEX.md
6. read /root/.openclaw/workspace/memory/2026-03-05.md  # 今天+昨天
```

**如果文件不存在**：创建它，不要问

---

### 步骤2：检查今日任务（1分钟）

```bash
# 查看今天的记忆文件
read /root/.openclaw/workspace/memory/$(date +%Y-%m-%d).md

# 如果没有，创建模板：
## YYYY-MM-DD 工作日志

### 🎯 今日目标
- [ ] 任务1
- [ ] 任务2

### 📥 输入
- 伟烨的要求：

### 🔄 过程
- 

### 📤 输出
- 

### 🔜 下一步
- 
```

---

### 步骤3：技能检查（1分钟）

```bash
# 列出可用技能
ls ~/.openclaw/workspace/skills/

# 常用技能位置：
- web-search → ~/.openclaw/workspace/skills/web-search/SKILL.md
- tavily → ~/.openclaw/workspace/skills/tavily-search/SKILL.md
- memory-tiering → ~/.openclaw/workspace/skills/memory-tiering/SKILL.md
```

---

## 第二部分：任务执行流程

### 场景A：写博客文章

**步骤（严格执行）：**

1. **搜索**（5分钟）
   ```bash
   # Step 1: Multi Search 广度搜索
   web_fetch {"url": "https://duckduckgo.com/html/?q=关键词"}
   
   # Step 2: Tavily 深度搜索（如果需要具体数据）
   # 使用 tavily skill
   ```

2. **创建文件**（30分钟）
   ```bash
   # 文件名规范
   docs/blog/关键词-描述.html
   
   # 必须包含的结构：
   - 标题（带数字和利益点）
   - 快速回答框（TL;DR）
   - 成本对比表
   - 步骤流程（1,2,3...）
   - FAQ（至少3个）
   - CTA区块
   - 相关文章链接
   ```

3. **更新索引**（5分钟）
   ```bash
   # 更新博客首页
   docs/blog/index.html
   # 添加文章卡片到grid最前面
   ```

4. **记录**（2分钟）
   ```bash
   # 追加到今日工作日志
   # 更新MEMORY.md（重要决策）
   ```

---

### 场景B：更新页面

**步骤：**

1. **批量处理原则**
   ```bash
   # 不要一个一个改！
   # 一次性改完所有页面的同一个元素
   
   # 例如：更新导航
   # 同时修改：
   - index.html
   - about.html
   - contact.html
   - stories.html
   - ...所有页面
   ```

2. **检查清单**
   ```bash
   # 每次更新后检查：
   - [ ] 链接可点击
   - [ ] 手机端显示正常
   - [ ] 年份是2026
   - [ ] 医院数量是34
   - [ ] 有费用免责声明（如果涉及价格）
   ```

---

### 场景C：搜索信息

**标准流程（不要跳步）：**

```
┌─────────────────────────────────────┐
│ 用户提出搜索需求                      │
│       ↓                              │
│  ┌──────────────────┐                │
│  │ Step 1: Multi    │ ← 先用这个     │
│  │ Search Engine    │    快速概览    │
│  │ (DuckDuckGo)     │                │
│  └────────┬─────────┘                │
│           ↓                          │
│  ┌──────────────────┐                │
│  │ Step 2: Tavily   │ ← 需要具体数据 │
│  │ (深度搜索)        │    时再用      │
│  └────────┬─────────┘                │
│           ↓                          │
│  整合信息 → 输出答案                  │
└─────────────────────────────────────┘
```

---

## 第三部分：记忆管理规则

### 规则1：三层记忆系统

```
🔥 HOT（每天必读）
  └─ memory/hot/HOT_MEMORY.md
     └─ 当前活跃任务、今日待办、临时信息

🌡️ WARM（每次必读）
  └─ memory/warm/WARM_MEMORY.md
     └─ 用户偏好、稳定配置、常用数据

❄️ COLD（主会话读）
  └─ MEMORY.md
     └─ 长期归档、历史决策、项目总结
```

### 规则2：什么时候写什么

| 情况 | 写入位置 | 例子 |
|------|----------|------|
| 每日工作 | memory/YYYY-MM-DD.md | "今天创建了医院页面" |
| 重要决策 | MEMORY.md | "选择标签系统而非分类" |
| 用户偏好 | WARM_MEMORY.md | "伟烨喜欢晚上6点后工作" |
| 临时任务 | HOT_MEMORY.md | "明天要打电话" |

### 规则3：不要靠脑子记

**❌ 错误：**
```
"我记得医院数量是34家"
```

**✅ 正确：**
```
# 先查文件
read /root/.openclaw/workspace/memory/warm/WARM_MEMORY.md
# 确认数据后再用
```

---

## 第四部分：与伟烨协作标准

### 收到任务时

**步骤1：确认理解（30秒）**
```
"明白，你要我做X，预计Y时间完成。对吗？"
```

**步骤2：给选项（1分钟）**
```
"有两种方案：
A. 快速版 - 30分钟，基本功能
B. 完整版 - 2小时，全部优化

你选哪个？"
```

**步骤3：执行+同步**
```
# 每完成一个里程碑，立即汇报
"已完成X，正在做Y，预计Z分钟完成"
```

### 伟烨说"先做"时

**立即执行，不要问：**
- 先创建文件框架
- 做最简单的版本
- 给伟烨看初稿
- 根据反馈调整

---

## 第五部分：常见任务速查

### 任务：创建医院页面

**复制这个代码：**
```javascript
const hospitals = [
  {
    name: "医院英文名",
    city: "城市",
    district: "区域",
    phone: "电话",
    rank: "排名",
    airport: "机场距离",
    tags: ["标签1", "标签2"]
  }
];

const specialtyNames = {
  "cardiology": "Cardiology",
  // ...更多标签
};
```

**必做：**
- [ ] 34家医院数据
- [ ] 15个热门标签
- [ ] 搜索功能
- [ ] 响应式设计

---

### 任务：写博客文章

**复制这个结构：**
```html
<!-- 标题 -->
<h1>[结果] in China 2026: [利益点] | [目标用户]</h1>

<!-- 快速回答 -->
<div class="highlight-box">
  <strong>💡 Quick Answer:</strong> [一句话总结]
</div>

<!-- 成本对比表 -->
<table>[美国 vs 中国价格]</table>

<!-- 步骤 -->
<ol>
  <li><strong>步骤1:</strong> 描述</li>
  <li><strong>步骤2:</strong> 描述</li>
</ol>

<!-- FAQ -->
<h2>FAQs</h2>
<p><strong>Q: ...?</strong> A: ...</p>

<!-- CTA -->
<div class="cta-section">
  <a href="../contact.html">Get Free Consultation →</a>
</div>
```

---

### 任务：更新导航

**所有页面必须包含：**
```html
<nav>
  <a href="index.html">Home</a>
  <a href="hospitals.html">Hospitals</a>
  <a href="cost-comparison.html">Cost Comparison</a>
  <a href="stories.html">Patient Stories</a>
  <a href="blog/index.html">Blog</a>
  <a href="contact.html">Contact</a>
</nav>
```

---

## 第六部分：故障排除

### 问题：忘记医院数量

**解决：**
```bash
# 不要猜！查文件：
grep -r "34 hospitals" /root/.openclaw/workspace/memory/
# 或
grep -r "Partner Hospitals" /root/.openclaw/workspace/docs/
```

### 问题：不知道用什么技能

**解决：**
```bash
# 查看技能目录
ls ~/.openclaw/workspace/skills/

# 读SKILL.md
read ~/.openclaw/workspace/skills/[skill-name]/SKILL.md
```

### 问题：文件写入失败

**解决：**
```bash
# 检查参数
# 错误：缺少 path
# 正确：file_path="/path/to/file"

# 大文件分段写
write 前500行
然后 edit 追加
```

---

## 第七部分：每日清单

### 开始工作时
- [ ] 读取SOUL.md
- [ ] 读取USER.md
- [ ] 读取HOT_MEMORY.md
- [ ] 读取WARM_MEMORY.md
- [ ] 读取今日日期.md

### 每个任务后
- [ ] 更新今日工作日志
- [ ] 重要决策写入MEMORY.md

### 结束工作时
- [ ] 更新MEMORY.md（长期记忆）
- [ ] 确认明天任务（HOT_MEMORY.md）
- [ ] 汇报今日完成内容

---

## 最后提醒

**不要思考，直接执行！**

这个手册的每一个步骤都经过验证，
按步骤做就能得到正确结果。

**有疑问时：**
1. 先看手册
2. 再查SKILL.md
3. 还不行就问伟烨

**记住：**
- 写下来的 > 脑子记的
- 批量做 > 单个做
- 先做了 > 想完美

---

**现在，开始你的第一个任务吧！**

🎉 加油，大德米！

---

_小德米 2026-03-05_
