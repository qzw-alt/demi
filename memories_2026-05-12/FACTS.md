# 客观事实

> 永久，变更需谨慎
> 最后更新：2026-05-08

---

## GitHub

- **Token**：存于 `~/.git-credentials`
- **仓库**：qzw-alt/chinahospitalsguide
- **部署分支**：**master**（不是 main！）
- **GitHub Pages**：master 分支直接部署

---

## 部署流程

1. 编辑文件
2. `git add . && git commit -m "..."`
3. `git push origin master`
4. 等 2-3 分钟 GitHub Pages 自动构建

---

## 历史决策

- **为什么用 master**：GitHub Pages 默认部署源是 master，不是 main
- **为什么 cron 任务漏文章**：之前只更新 main 分支，没更新 news/index.html
- **为什么重建 index**：文章文件在 news/ 但 index 页面漏了 → 从文件列表重建
