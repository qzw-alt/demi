# CLI-Anything 用法指南

> 大德米专属技能 - 本地环境操作
> 最后更新：2026-03-15

---

## 什么是 CLI-Anything？

**CLI-Anything** 是一个让大德米能够执行本地系统命令的技能。

**为什么重要**：
- 小德米在服务器上运行，只能操作远程资源
- 大德米在本地运行，可以操作你的电脑
- 可以安装软件、管理文件、执行脚本

---

## 核心能力

### 1. 执行系统命令

```bash
# 执行任何命令
cli-anything exec "ls -la"
cli-anything exec "brew install node"
cli-anything exec "git status"
```

### 2. 文件管理

```bash
# 创建文件
cli-anything file create ./test.txt "内容"

# 移动文件
cli-anything file move ./old.txt ./new.txt

# 复制文件
cli-anything file copy ./source.txt ./dest.txt

# 删除文件
cli-anything file delete ./temp.txt
```

### 3. 系统信息

```bash
# 获取系统信息
cli-anything system info

# 检查磁盘空间
cli-anything system disk

# 查看环境变量
cli-anything system env
```

---

## Mac 环境专用

### Homebrew 操作

```bash
# 安装软件
cli-anything exec "brew install git"
cli-anything exec "brew install node"
cli-anything exec "brew install python@3.11"

# 更新软件列表
cli-anything exec "brew update"

# 升级已安装软件
cli-anything exec "brew upgrade"

# 搜索软件
cli-anything exec "brew search openclaw"
```

### 文件路径

Mac 常用路径：
```
/Users/[用户名]/          # 用户主目录
/Users/[用户名]/.openclaw/  # OpenClaw配置目录
/Applications/            # 应用程序
/usr/local/bin/          # 用户安装的可执行文件
/opt/homebrew/bin/       # Apple Silicon Homebrew 路径
```

### 权限管理

```bash
# 修改文件权限
cli-anything exec "chmod +x script.sh"

# 修改所有者
cli-anything exec "sudo chown user:group file.txt"

# 使用 sudo（需要密码）
cli-anything exec "sudo apt-get update"  # Linux
cli-anything exec "sudo brew install xxx"  # Mac
```

---

## Windows 环境专用

### 常用命令

```powershell
# PowerShell 命令
cli-anything exec "Get-ChildItem"
cli-anything exec "New-Item -ItemType File -Path test.txt"
cli-anything exec "Remove-Item file.txt"

# CMD 命令
cli-anything exec "cmd /c dir"
cli-anything exec "cmd /c echo hello > test.txt"
```

### 文件路径

Windows 常用路径：
```
C:\Users\[用户名]\                    # 用户主目录
C:\Users\[用户名]\.openclaw\           # OpenClaw配置目录
C:\Program Files\                     # 程序文件
C:\Users\[用户名]\AppData\Roaming\    # 应用数据
```

---

## 与 OpenClaw 原生工具的对比

| 操作 | OpenClaw原生 | CLI-Anything |
|------|-------------|--------------|
| 读取文件 | `read` | `cli-anything file read` |
| 写入文件 | `write` | `cli-anything file create` |
| 执行命令 | ❌ 不能 | ✅ 可以 |
| 安装软件 | ❌ 不能 | ✅ 可以 |
| 系统信息 | ❌ 不能 | ✅ 可以 |

**结论**：CLI-Anything 补充了 OpenClaw 的本地操作能力。

---

## 实战案例

### 案例1：安装新技能

```bash
# 检查当前技能
cli-anything exec "ls ~/.openclaw/workspace/skills/"

# 从GitHub克隆新技能
cli-anything exec "cd ~/.openclaw/workspace/skills && git clone https://github.com/xxx/new-skill.git"

# 验证安装
cli-anything exec "ls ~/.openclaw/workspace/skills/new-skill"
```

### 案例2：批量重命名文件

```bash
# Mac/Linux
cli-anything exec "cd ~/Documents && for f in *.txt; do mv \"$f\" \"old_$f\"; done"

# Windows
cli-anything exec "cd C:\Users\xxx\Documents && Get-ChildItem *.txt | Rename-Item -NewName { 'old_' + $_.Name }"
```

### 案例3：备份工作目录

```bash
# 创建备份
cli-anything exec "cd ~/.openclaw && tar -czf workspace-backup-$(date +%Y%m%d).tar.gz workspace/"

# 移动备份到安全位置
cli-anything exec "mv ~/.openclaw/workspace-backup-*.tar.gz ~/Backups/"
```

### 案例4：检查系统状态

```bash
# Mac - 检查内存使用
cli-anything exec "vm_stat"

# Mac - 检查CPU使用
cli-anything exec "top -l 1 | head -20"

# Windows - 检查系统信息
cli-anything exec "systeminfo | findstr /B /C:\"OS Name\" /C:\"Total Physical Memory\""
```

---

## 安全注意事项

### ⚠️ 危险命令（谨慎使用）

```bash
# 删除（不可逆）
rm -rf /          # ❌ 千万别运行！删除整个系统
rm -rf ~/*        # ❌ 删除用户所有文件

# 权限（可能导致系统问题）
sudo chmod -R 777 /    # ❌ 修改所有文件权限
sudo chown -R user /   # ❌ 修改所有文件所有者
```

### ✅ 安全实践

1. **先查看，再操作**
   ```bash
   # 先列出要删除的文件
   ls target_directory/
   # 确认后再删除
   rm target_directory/specific_file
   ```

2. **使用回收站**
   ```bash
   # Mac - 移动到回收站
   mv file.txt ~/.Trash/
   
   # 而不是直接删除
   rm file.txt  # ❌ 永久删除
   ```

3. **备份重要文件**
   ```bash
   # 操作前先备份
   cp important.conf important.conf.backup
   ```

---

## 常见问题

### Q: CLI-Anything 和 OpenClaw 的 `exec` 有什么区别？

A: 
- OpenClaw 的 `exec` 在沙盒环境中运行，限制较多
- CLI-Anything 直接访问本地系统，能力更强

### Q: 为什么有些命令需要 sudo/管理员权限？

A:
- 安装系统级软件需要管理员权限
- 修改系统配置需要管理员权限
- 普通用户操作自己的文件不需要

### Q: 命令执行失败怎么办？

A:
1. 检查命令语法
2. 检查路径是否正确
3. 检查是否有权限
4. 查看错误信息

### Q: 可以执行交互式命令吗？

A:
- 不建议，因为AI无法交互
- 使用非交互式替代方案
  ```bash
  # ❌ 交互式
  vim file.txt
  
  # ✅ 非交互式
  echo "content" > file.txt
  ```

---

## 快速参考卡

```bash
# 执行命令
cli-anything exec "命令"

# 文件操作
cli-anything file create/move/copy/delete

# 系统信息
cli-anything system info/disk/env

# Mac 安装
cli-anything exec "brew install xxx"

# Windows PowerShell
cli-anything exec "powershell -Command 'xxx'"

# Windows CMD
cli-anything exec "cmd /c xxx"
```

---

**记住**：CLI-Anything 让大德米拥有了"手"，可以操作本地环境。但能力越大，责任越大，谨慎使用！

---

*大德米专属文档*
*最后更新：2026-03-15*
