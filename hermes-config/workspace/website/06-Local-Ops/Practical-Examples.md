# CLI-Anything 实战案例

> 大德米本地操作实际例子
> 从简单到复杂的完整演示

---

## 案例1：自动化备份系统（初级）

### 场景
每天自动备份工作目录到安全位置。

### 实现

```bash
# 创建备份脚本
cli-anything file create ~/.openclaw/backup.sh '#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="$HOME/Backups"
mkdir -p $BACKUP_DIR

# 备份工作区
cd ~/.openclaw
tar -czf "$BACKUP_DIR/workspace-backup-$DATE.tar.gz" workspace/ --exclude="node_modules" --exclude=".git"

# 保留最近10个备份
ls -t $BACKUP_DIR/workspace-backup-*.tar.gz | tail -n +11 | xargs rm -f

echo "✅ Backup completed: $BACKUP_DIR/workspace-backup-$DATE.tar.gz"
'

# 添加执行权限
cli-anything exec "chmod +x ~/.openclaw/backup.sh"

# 测试运行
cli-anything exec "~/.openclaw/backup.sh"
```

### 结果
- ✅ 自动压缩备份
- ✅ 自动清理旧备份（保留10个）
- ✅ 排除 node_modules 和 .git 节省空间

---

## 案例2：批量处理日志文件（中级）

### 场景
清理30天前的日志文件，并生成统计报告。

### 实现

```bash
# 创建处理脚本
cli-anything file create ~/.openclaw/clean-logs.sh '#!/bin/bash

LOG_DIR="~/.openclaw/workspace/logs"
REPORT_FILE="$LOG_DIR/cleanup-report-$(date +%Y%m%d).txt"

echo "=== Log Cleanup Report $(date) ===" > $REPORT_FILE
echo "" >> $REPORT_FILE

# 统计清理前
BEFORE_SIZE=$(du -sh $LOG_DIR 2>/dev/null | cut -f1)
echo "Before cleanup: $BEFORE_SIZE" >> $REPORT_FILE

# 删除30天前的日志
find $LOG_DIR -name "*.log" -mtime +30 -type f | while read file; do
    echo "Deleting: $file ($(stat -f%z "$file" 2>/dev/null || stat -c%s "$file" 2>/dev/null) bytes)" >> $REPORT_FILE
    rm "$file"
done

# 统计清理后
AFTER_SIZE=$(du -sh $LOG_DIR 2>/dev/null | cut -f1)
echo "" >> $REPORT_FILE
echo "After cleanup: $AFTER_SIZE" >> $REPORT_FILE
echo "Cleanup completed at $(date)" >> $REPORT_FILE

cat $REPORT_FILE
'

# 执行
cli-anything exec "chmod +x ~/.openclaw/clean-logs.sh"
cli-anything exec "~/.openclaw/clean-logs.sh"
```

### 结果
- ✅ 自动识别30天前的日志
- ✅ 生成详细的清理报告
- ✅ 显示清理前后的空间变化

---

## 案例3：技能自动更新系统（高级）

### 场景
检查所有已安装技能是否有更新，自动拉取最新版本。

### 实现

```bash
# 创建更新脚本
cli-anything file create ~/.openclaw/update-skills.sh '#!/bin/bash

SKILLS_DIR="~/.openclaw/workspace/skills"
REPORT=""

echo "🔍 Checking for skill updates..."
echo ""

cd "$SKILLS_DIR" || exit 1

for skill_dir in */; do
    if [ -d "$skill_dir/.git" ]; then
        skill_name=$(basename "$skill_dir")
        echo -n "📦 $skill_name: "
        
        cd "$skill_dir"
        
        # 获取当前版本
        OLD_COMMIT=$(git rev-parse --short HEAD)
        
        # 尝试拉取更新
        git fetch origin --quiet 2>/dev/null
        
        # 检查是否有更新
        LOCAL=$(git rev-parse HEAD)
        REMOTE=$(git rev-parse origin/main 2>/dev/null || git rev-parse origin/master 2>/dev/null)
        
        if [ "$LOCAL" != "$REMOTE" ]; then
            # 有更新，拉取
            git pull origin main --quiet 2>/dev/null || git pull origin master --quiet 2>/dev/null
            NEW_COMMIT=$(git rev-parse --short HEAD)
            echo "✅ Updated ($OLD_COMMIT → $NEW_COMMIT)"
            REPORT="${REPORT}Updated: $skill_name\n"
        else
            echo "⬆️  Already up to date ($OLD_COMMIT)"
        fi
        
        cd "$SKILLS_DIR"
    fi
done

echo ""
echo "🎉 Update check completed!"
[ -n "$REPORT" ] && echo -e "\nUpdated skills:\n$REPORT"
'

# 执行更新检查
cli-anything exec "chmod +x ~/.openclaw/update-skills.sh"
cli-anything exec "~/.openclaw/update-skills.sh"
```

### 结果
- ✅ 自动遍历所有技能目录
- ✅ 检查 Git 仓库更新
- ✅ 自动拉取最新代码
- ✅ 生成更新报告

---

## 案例4：系统监控仪表板（高级）

### 场景
生成系统状态报告，包括CPU、内存、磁盘使用情况。

### 实现

```bash
# 创建监控脚本
cli-anything file create ~/.openclaw/system-report.sh '#!/bin/bash

REPORT_FILE="~/.openclaw/workspace/memory/system-report-$(date +%Y%m%d-%H%M).md"

cat > $REPORT_FILE << EOF
# 系统状态报告

**生成时间**: $(date)
**主机名**: $(hostname)
**操作系统**: $(uname -s -r)

---

## 💻 CPU 信息

\`\`\`
$(sysctl -n machdep.cpu.brand_string 2>/dev/null || cat /proc/cpuinfo | grep "model name" | head -1)
CPU 核心数: $(sysctl -n hw.ncpu 2>/dev/null || nproc)
\`\`\`

## 🧠 内存使用

\`\`\`
$(vm_stat 2>/dev/null || free -h)
\`\`\`

## 💾 磁盘使用

\`\`\`
$(df -h | grep -E "/dev/disk|Filesystem")
\`\`\`

## 📊 进程 TOP 5

\`\`\`
$(ps aux | sort -rk 3,3 | head -6)
\`\`\`

## 🌐 网络状态

\`\`\`
网络接口: $(ifconfig | grep -E "^en|^eth|^wl" | wc -l) 个
活动连接: $(netstat -an 2>/dev/null | grep ESTABLISHED | wc -l || echo "N/A")
\`\`\`

## 🔋 电池状态（如果是笔记本）

\`\`\`
$(pmset -g batt 2>/dev/null || echo "Not a laptop or pmset not available")
\`\`\`

---

*报告自动生成 by CLI-Anything*
EOF

echo "✅ System report generated: $REPORT_FILE"
cat $REPORT_FILE
```

# 执行
cli-anything exec "chmod +x ~/.openclaw/system-report.sh"
cli-anything exec "~/.openclaw/system-report.sh"
```

### 结果
- ✅ 自动生成 Markdown 格式报告
- ✅ 包含 CPU、内存、磁盘、网络信息
- ✅ 保存到记忆系统，方便追踪

---

## 案例5：Git 仓库批量操作（实用）

### 场景
检查多个 Git 仓库的状态，批量提交未提交的更改。

### 实现

```bash
# 创建批量Git脚本
cli-anything file create ~/.openclaw/git-batch.sh '#!/bin/bash

WORKSPACE="~/.openclaw/workspace"
ACTION="${1:-status}"

echo "🔄 Git Batch Operation: $ACTION"
echo "================================"
echo ""

find "$WORKSPACE" -type d -name ".git" | while read gitdir; do
    repo_dir=$(dirname "$gitdir")
    repo_name=$(basename "$repo_dir")
    
    echo "📁 $repo_name"
    cd "$repo_dir"
    
    case $ACTION in
        status)
            git status --short
            ;;
        pull)
            git pull origin main 2>/dev/null || git pull origin master 2>/dev/null
            ;;
        commit)
            if [ -n "$2" ]; then
                git add -A
                git commit -m "$2" 2>/dev/null && echo "✅ Committed: $2"
            else
                echo "❌ Usage: git-batch.sh commit 'message'"
            fi
            ;;
        push)
            git push origin main 2>/dev/null || git push origin master 2>/dev/null
            ;;
        *)
            echo "Unknown action: $ACTION"
            echo "Usage: git-batch.sh [status|pull|commit|push]"
            ;;
    esac
    
    echo ""
done
'

# 使用示例
cli-anything exec "chmod +x ~/.openclaw/git-batch.sh"

# 查看所有仓库状态
cli-anything exec "~/.openclaw/git-batch.sh status"

# 批量拉取更新
cli-anything exec "~/.openclaw/git-batch.sh pull"

# 批量提交（带消息）
cli-anything exec "~/.openclaw/git-batch.sh commit 'Daily backup'"
```

### 结果
- ✅ 一键查看所有仓库状态
- ✅ 批量拉取/提交/推送
- ✅ 支持自定义提交消息

---

## 实战技巧总结

### 1. 脚本组织
```
~/.openclaw/
├── scripts/           # 生产脚本
├── backup.sh          # 备份
├── clean-logs.sh      # 清理
└── utils/             # 工具脚本
```

### 2. 错误处理
```bash
#!/bin/bash
set -e  # 遇到错误立即退出

# 或者捕获错误
command || {
    echo "Command failed"
    exit 1
}
```

### 3. 日志记录
```bash
LOG_FILE="~/.openclaw/logs/$(date +%Y%m).log"
echo "[$(date)] Action performed" >> $LOG_FILE
```

### 4. 安全执行
```bash
# 先测试，再执行
echo "Would delete: $file"
# 确认后再：
rm "$file"
```

---

**这些案例展示了 CLI-Anything 的真正威力：让大德米成为本地环境的自动化管理员！**

---

*大德米实战案例*
*最后更新：2026-03-15*
