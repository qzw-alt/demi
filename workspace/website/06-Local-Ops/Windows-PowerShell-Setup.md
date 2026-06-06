# Windows PowerShell 环境配置指南

> 大德米 Windows 专用配置
> PowerShell 替代 Bash，完全本地操作
> 最后更新：2026-03-15

---

## 环境检查清单

### 1. 基础工具检查

```powershell
# 检查 PowerShell 版本（需要 5.1+ 或 7.x）
$PSVersionTable.PSVersion

# 检查 Git
Get-Command git

# 检查 Python（可选）
Get-Command python

# 检查 Node.js（可选）
Get-Command node
```

### 2. OpenClaw 配置

```powershell
# 检查 OpenClaw 版本
openclaw --version

# 更新到最新版
openclaw update
# 或
npm update -g openclaw
```

### 3. 工作目录结构

```powershell
# 标准目录结构（Windows）
C:\Users\[用户名]\
└── .openclaw\
    ├── workspace\              # 工作区
    │   ├── memory\            # 记忆系统
    │   │   ├── hot\          # 每日活跃
    │   │   ├── warm\         # 稳定配置
    │   │   └── cold\         # 长期归档
    │   ├── skills\           # 技能目录
    │   ├── scripts\          # PowerShell 脚本
    │   └── CLI-Anything\     # CLI-Anything 仓库（视频制作核心）
    └── config\               # 配置文件
```

---

## PowerShell 基础配置

### 1. 执行策略设置

```powershell
# 查看当前执行策略
Get-ExecutionPolicy

# 设置为 RemoteSigned（允许本地脚本运行）
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser

# 验证
Get-ExecutionPolicy -List
```

### 2. 创建 PowerShell 配置文件

```powershell
# 创建配置文件（如果不存在）
if (!(Test-Path $PROFILE)) {
    New-Item -ItemType File -Path $PROFILE -Force
}

# 编辑配置文件
notepad $PROFILE
```

### 3. 配置文件内容

```powershell
# 添加到 $PROFILE

# 设置编码为 UTF-8
$OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# 自定义别名
Set-Alias -Name ll -Value Get-ChildItem
Set-Alias -Name which -Value Get-Command
Set-Alias -Name touch -Value New-Item

# 工作目录快捷方式
function workspace { Set-Location C:\Users\$env:USERNAME\.openclaw\workspace }
function home { Set-Location $env:USERPROFILE }

# 晨检快捷命令
function morning { 
    & "C:\Users\$env:USERNAME\.openclaw\workspace\scripts\morning-check.ps1"
}

# 显示系统信息
function sysinfo {
    Write-Host "OS: $((Get-CimInstance Win32_OperatingSystem).Caption)"
    Write-Host "PowerShell: $($PSVersionTable.PSVersion)"
    Write-Host "User: $env:USERNAME"
    Write-Host "Date: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
}

# 欢迎消息
Write-Host "Welcome, $env:USERNAME!" -ForegroundColor Cyan
Write-Host "Type 'workspace' to go to work directory" -ForegroundColor Gray
Write-Host "Type 'morning' to start daily check" -ForegroundColor Gray
```

### 4. 重新加载配置

```powershell
# 重新加载配置文件
. $PROFILE
```

---

## 推荐的 Windows 软件

### 开发工具
```powershell
# 使用 winget 安装（Windows 10/11 自带）

# Git
winget install Git.Git

# VS Code
winget install Microsoft.VisualStudioCode

# Python
winget install Python.Python.3.11

# Node.js
winget install OpenJS.NodeJS

# PowerShell 7（新版）
winget install Microsoft.PowerShell
```

### 视频制作工具（CLI-Anything 重点）
```powershell
# FFmpeg（视频处理核心）
winget install Gyan.FFmpeg

# OBS Studio（录制）
winget install OBSProject.OBSStudio

# DaVinci Resolve（剪辑）
winget install BlackmagicDesign.DaVinciResolve

# HandBrake（转码）
winget install HandBrake.HandBrake
```

### 效率工具
```powershell
# PowerToys（微软官方工具集）
winget install Microsoft.PowerToys

# QuickLook（空格预览）
winget install QL-Win.QuickLook

# Everything（文件搜索）
winget install voidtools.Everything
```

---

## 文件权限管理

### 1. 查看权限

```powershell
# 查看文件权限
Get-Acl "C:\Users\$env:USERNAME\.openclaw\workspace"

# 查看特定文件
Get-Acl "C:\Users\$env:USERNAME\.openclaw\workspace\memory\hot\HOT_MEMORY.md" | Format-List
```

### 2. 修改权限

```powershell
# 获取当前 ACL
$path = "C:\Users\$env:USERNAME\.openclaw\workspace"
$acl = Get-Acl $path

# 添加当前用户完全控制权限
$user = $env:USERNAME
$rule = New-Object System.Security.AccessControl.FileSystemAccessRule(
    $user, "FullControl", "ContainerInherit,ObjectInherit", "None", "Allow"
)
$acl.SetAccessRule($rule)
Set-Acl $path $acl

Write-Host "Permissions updated for $path" -ForegroundColor Green
```

### 3. 加密敏感文件

```powershell
# 加密 API Keys 文件
$file = "C:\Users\$env:USERNAME\.openclaw\workspace\.api_keys"
if (Test-Path $file) {
    (Get-Item $file).Encrypt()
    Write-Host "File encrypted: $file" -ForegroundColor Green
}
```

---

## 环境变量配置

### 1. 用户环境变量

```powershell
# 添加 OpenClaw 到 PATH
$userPath = [Environment]::GetEnvironmentVariable("Path", "User")
if ($userPath -notlike "*openclaw*") {
    [Environment]::SetEnvironmentVariable(
        "Path", 
        "$userPath;C:\Users\$env:USERNAME\.openclaw\bin", 
        "User"
    )
    Write-Host "Added OpenClaw to PATH" -ForegroundColor Green
}

# 添加 FFmpeg 到 PATH（视频处理）
$userPath = [Environment]::GetEnvironmentVariable("Path", "User")
if ($userPath -notlike "*ffmpeg*") {
    [Environment]::SetEnvironmentVariable(
        "Path", 
        "$userPath;C:\Program Files\FFmpeg\bin", 
        "User"
    )
    Write-Host "Added FFmpeg to PATH" -ForegroundColor Green
}
```

### 2. 自定义环境变量

```powershell
# 设置 OPENCLAW_HOME
[Environment]::SetEnvironmentVariable(
    "OPENCLAW_HOME", 
    "C:\Users\$env:USERNAME\.openclaw", 
    "User"
)

# 设置 WORKSPACE
[Environment]::SetEnvironmentVariable(
    "WORKSPACE", 
    "C:\Users\$env:USERNAME\.openclaw\workspace", 
    "User"
)

# 验证
Get-ChildItem Env: | Where-Object { $_.Name -like "*OPENCLAW*" -or $_.Name -like "*WORKSPACE*" }
```

---

## 系统优化

### 1. 性能优化

```powershell
# 禁用不必要的启动项
Get-CimInstance Win32_StartupCommand | Select-Object Name, Command, Location

# 查看内存使用
Get-CimInstance Win32_OperatingSystem | Select-Object TotalVisibleMemorySize, FreePhysicalMemory

# 查看磁盘空间
Get-Volume | Select-Object DriveLetter, FileSystemLabel, SizeRemaining, Size
```

### 2. 快速操作

```powershell
# 清空回收站
Clear-RecycleBin -Force

# 清空临时文件
Remove-Item "$env:TEMP\*" -Recurse -Force -ErrorAction SilentlyContinue

# 刷新 DNS
Clear-DnsClientCache

# 查看网络连接
Get-NetTCPConnection | Select-Object LocalAddress, LocalPort, RemoteAddress, State
```

---

## 故障排除

### 问题1: PowerShell 脚本无法运行

```powershell
# 错误信息：无法加载脚本，因为在此系统上禁止运行脚本
# 解决：
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser

# 验证
Get-ExecutionPolicy
```

### 问题2: 命令找不到

```powershell
# 检查 PATH
$env:Path -split ";"

# 重新加载环境变量
$env:Path = [Environment]::GetEnvironmentVariable("Path", "Machine") + ";" + [Environment]::GetEnvironmentVariable("Path", "User")
```

### 问题3: 权限不足

```powershell
# 以管理员身份运行 PowerShell
# 方法1：右键 PowerShell → 以管理员身份运行
# 方法2：命令行
Start-Process powershell -Verb runAs
```

### 问题4: 中文显示乱码

```powershell
# 设置编码
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

# 或在脚本开头添加
chcp 65001 | Out-Null
```

---

## PowerShell 常用命令速查

```powershell
# 文件操作
New-Item -ItemType File -Path "file.txt"      # 创建文件
New-Item -ItemType Directory -Path "folder"   # 创建目录
Copy-Item "source" "dest"                      # 复制
Move-Item "source" "dest"                      # 移动
Remove-Item "path" -Recurse -Force            # 删除
Test-Path "path"                               # 检查存在

# 文本操作
Get-Content "file.txt"                         # 读取
Set-Content "file.txt" "content"              # 写入
Add-Content "file.txt" "new line"             # 追加
Select-String "pattern" "file.txt"            # 搜索

# 进程管理
Get-Process                                    # 查看进程
Stop-Process -Name "process"                  # 结束进程
Stop-Process -Id 1234                         # 通过ID结束

# 服务管理
Get-Service                                    # 查看服务
Start-Service "service"                       # 启动
Stop-Service "service"                        # 停止
Restart-Service "service"                     # 重启

# 网络测试
Test-Connection google.com -Count 4           # Ping
Test-NetConnection -ComputerName localhost -Port 8080  # 端口测试

# 压缩解压
Compress-Archive -Path "folder" -DestinationPath "archive.zip"    # 压缩
Expand-Archive -Path "archive.zip" -DestinationPath "folder"      # 解压
```

---

## 下一步：安装 CLI-Anything

配置完 Windows 环境后，下一步是安装 CLI-Anything 用于视频制作。

详见：[CLI-Anything Windows 用法](CLI-Anything-Windows-Usage.md)

---

**配置完成后，运行 `morning` 命令验证环境！**

---

*大德米 Windows 专用*
*PowerShell 版本*
*最后更新：2026-03-15*
