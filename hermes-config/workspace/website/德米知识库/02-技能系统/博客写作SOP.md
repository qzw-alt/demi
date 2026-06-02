# 博客写作标准操作流程 (SOP)

> **生效日期**: 2026-03-15  
> **版本**: v1.0  
> **状态**: 已固化

---

## 🎯 标准技能组合

```
multi-search-engine → content-research-writer → humanizer
    广度搜索            协作写作框架           去AI化
```

---

## 📋 执行步骤

### Step 1: 广度搜索 (multi-search-engine)
- 使用 `web_fetch` 搜索多个来源
- 关键词覆盖：医院名称、排名、价格、患者评价
- 目标：获取全面的背景信息

### Step 2: 协作写作 (content-research-writer框架)
- 采用研究→大纲→写作→优化的流程
- 故事化开场（个人经历/案例）
- 数据支撑（价格对比、成功率）
- 实用信息（决策框架、流程指南）

### Step 3: 去AI化 (humanizer技能)

**必须调用humanizer技能进行优化！**

**操作命令**:
```bash
# 读取humanizer技能
read ~/.openclaw/workspace/skills/humanizer/SKILL.md

# 应用humanizer原则手动优化，或使用脚本自动处理
```

**核心优化点**:
- ✅ 故事化开场："When my uncle needed..."
- ✅ 口语化表达："That's more than most entire countries"
- ✅ 真实案例：具体患者姓名+地点+经历
- ✅ 直接了当：删除"comprehensive guide"等套话
- ✅ 加入细节：医生训练背景、具体手术名称
- ❌ 避免："emerged as", "pivotal moment", "testament to"

**检查清单**:
- [ ] 删除所有AI套话（emerged as, comprehensive, pivotal等）
- [ ] 添加具体人名和地点
- [ ] 使用口语化短句
- [ ] 加入真实感受和细节
- [ ] 确保读起来像真人写的

---

## 📝 文章结构模板

```
1. 故事化开场（个人/患者案例）
2. 成本对比表格
3. 医院详细介绍（3-5家）
   - 专长
   - 数据
   - 真实案例
   - 实用信息
4. 决策框架表格
5. 质量论证
6. 流程指南
7. 服务介绍
8. 联系方式
```

---

## ✅ 质量检查清单

- [ ] 开场是否故事化？
- [ ] 是否有具体患者案例？
- [ ] 价格数据是否具体？
- [ ] 是否有决策框架？
- [ ] 语言是否口语化？
- [ ] 是否删除了AI套话？
- [ ] 是否有明确的CTA（联系）？

---

## 📁 文件命名规范

```
best-[主题]-china-2026.html

示例：
- best-cancer-hospitals-china-2026.html
- best-cardiac-surgery-hospitals-china-2026.html
- best-dental-clinics-china-2026.html
```

---

## 🔄 更新记录

| 日期 | 版本 | 变更 |
|------|------|------|
| 2026-03-15 | v1.0 | 初始版本，固化新技能组合 |

---

**注意**: 此SOP为强制性标准，所有博客文章必须遵循。
