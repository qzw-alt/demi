# Mac 环境配置指南

> 大德米 Mac 专用配置
> 本地环境设置和优化

---

## 环境检查清单

### 1. 基础工具

```bash
# 检查是否已安装
cli-anything exec "which git"
cli-anything exec "which python3"
cli-anything exec "which node"

# 如果没有，安装它们
cli-anything exec "brew install git"
cli-anything exec "brew install python@3.11"
cli-anything exec "brew install node"
```

### 2. OpenClaw 配置

```bash
# 检查 OpenClaw 版本
openclaw --version

# 更新到最新版
openclaw update
# 或
pnpm update -g openclaw
```

### 3. 工作目录结构

```bash
# 标准目录结构
/Users/[用户名]/
└── .openclaw/
    ├── workspace/           # 工作区
    │   ├── memory/          # 记忆系统
    │   │   ├── hot/
    │   │   ├── warm/
    │   │   └── cold/
    │   ├── skills/          # 技能目录
    │   └── scripts/         # 自动化脚本
    └── config/              # 配置文件
```

---

## 推荐安装的软件

### 开发工具
```bash
# 版本管理
brew install pyenv          # Python 版本管理
brew install nvm            # Node 版本管理

# 编辑器
brew install --cask visual-studio-code
brew install --cask cursor  # AI 编辑器

# 终端增强
brew install iterm2
brew install oh-my-zsh
```

### 效率工具
```bash
# 快速启动
brew install --cask raycast

# 窗口管理
brew install --cask rectangle

# 笔记工具
brew install --cask obsidian
```

### AI/开发工具
```bash
# API 测试
brew install --cask postman

# 数据库客户端
brew install --cask tableplus

# Docker
brew install --cask docker
```

---

## 环境变量配置

### 添加到 ~/.zshrc

```bash
# OpenClaw
export PATH="$HOME/.local/bin:$PATH"

# Python
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init --path)"

# Node
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"

# 自定义别名
alias ll='ls -la'
alias workspace='cd ~/.openclaw/workspace'
alias morning='powershell -File ~/.openclaw/workspace/scripts/morning-check.ps1'
```

### 应用配置

```bash
cli-anything exec "source ~/.zshrc"
```

---

## 性能优化

### 1. 终端速度

```bash
# 禁用不必要的插件
# 编辑 ~/.zshrc，注释掉不用的插件

# 减少启动时间
brew install zsh-autosuggestions
brew install zsh-syntax-highlighting
```

### 2. 文件系统

```bash
# 显示隐藏文件
cli-anything exec "defaults write com.apple.finder AppleShowAllFiles YES"
cli-anything exec "killall Finder"

# 禁用 .DS_Store 在网络驱动器
cli-anything exec "defaults write com.apple.desktopservices DSDontWriteNetworkStores true"
```

### 3. 内存管理

```bash
# 定期清理缓存
cli-anything exec "sudo purge"

# 查看内存使用
cli-anything exec "vm_stat"
```

---

## 安全设置

### 1. SSH 密钥

```bash
# 生成 SSH 密钥（用于 GitHub）
cli-anything exec "ssh-keygen -t ed25519 -C \"your_email@example.com\""

# 添加到 ssh-agent
cli-anything exec "eval \"$(ssh-agent -s)\""
cli-anything exec "ssh-add ~/.ssh/id_ed25519"

# 复制公钥到剪贴板
cli-anything exec "pbcopy < ~/.ssh/id_ed25519.pub"
```

### 2. 文件权限

```bash
# 敏感文件权限
cli-anything exec "chmod 600 ~/.ssh/id_ed25519"
cli-anything exec "chmod 644 ~/.ssh/id_ed25519.pub"

# API Keys 文件
cli-anything exec "chmod 600 ~/.openclaw/workspace/.api_keys"
```

---

## 备份策略

### 1. 工作区备份

```bash
#!/bin/bash
# backup-workspace.sh

DATE=$(date +%Y%m%d)
BACKUP_DIR="$HOME/Backups"
mkdir -p $BACKUP_DIR

# 创建备份
cd ~/.openclaw
tar -czf "$BACKUP_DIR/workspace-backup-$DATE.tar.gz" workspace/

# 保留最近7天的备份
find $BACKUP_DIR -name "workspace-backup-*.tar.gz" -mtime +7 -delete

echo "Backup completed: $BACKUP_DIR/workspace-backup-$DATE.tar.gz"
```

### 2. 配置备份

```bash
# 备份 dotfiles
cli-anything exec "tar -czf ~/Backups/dotfiles-$(date +%Y%m%d).tar.gz ~/.zshrc ~/.bash_profile ~/.gitconfig"
```

---

## 故障排除

### 问题1: 命令找不到

```bash
# 检查 PATH
echo $PATH

# 重新安装
brew reinstall [package]
```

### 问题2: 权限不足

```bash
# 修复权限
cli-anything exec "sudo chown -R $(whoami) ~/.openclaw"
```

### 问题3: 端口被占用

```bash
# 查找占用端口的进程
lsof -i :3000

# 结束进程
kill -9 [PID]
```

---

## 快速命令参考

```bash
# 系统信息
uname -a                    # 系统版本
sw_vers                     # macOS 版本
system_profiler SPHardwareDataType  # 硬件信息

# 进程管理
ps aux | grep keyword       # 查找进程
kill -9 PID                 # 强制结束

# 网络
ifconfig                    # 网络接口
ping google.com             # 测试连接
netstat -an                 # 查看端口

# 磁盘
df -h                       # 磁盘使用
du -sh directory            # 目录大小

# 文件
find . -name "*.md"         # 查找文件
grep -r "keyword" .         # 文本搜索
tail -f log.txt             # 实时查看日志
```

---

**配置完成后，运行 `morning-check.ps1` 验证环境！**

---

*大德米 Mac 专用*
*最后更新：2026-03-15*
