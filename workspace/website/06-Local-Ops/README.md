# 06-Local-Ops 文件夹索引

> 大德米 Windows 本地操作指南
> PowerShell 版本

---

## 📄 文档列表

| 文档 | 内容 | 必读指数 | 状态 |
|------|------|---------|------|
| [Windows-PowerShell-Setup.md](Windows-PowerShell-Setup.md) | Windows环境配置、PowerShell基础、系统优化 | ⭐⭐⭐⭐⭐ | ✅ 已完成 |
| [CLI-Anything-Windows-Usage.md](CLI-Anything-Windows-Usage.md) | 视频制作自动化、批量转码、自动发布 | ⭐⭐⭐⭐⭐ | ✅ 已完成 |
| [Practical-Examples.md](Practical-Examples.md) | 备份、日志清理等通用脚本（Mac版，需适配） | ⭐⭐⭐ | ⏳ 待适配Windows |

---

## 🚀 快速开始

### 第一步：配置环境
阅读 [Windows-PowerShell-Setup.md](Windows-PowerShell-Setup.md)，完成：
- [ ] PowerShell 执行策略设置
- [ ] 安装必要软件（Git、FFmpeg、Python）
- [ ] 配置环境变量
- [ ] 创建工作目录结构

### 第二步：安装 CLI-Anything
阅读 [CLI-Anything-Windows-Usage.md](CLI-Anything-Windows-Usage.md)，完成：
- [ ] 克隆 CLI-Anything 仓库
- [ ] 安装 Python 依赖
- [ ] 测试视频处理功能

### 第三步：运行测试
```powershell
# 测试当前环境
powershell -ExecutionPolicy Bypass -File C:\Users\$env:USERNAME\.openclaw\workspace\scripts\test-cli-simple.ps1
```

---

## 🧪 环境测试结果（2026-03-15）

| 组件 | 状态 | 说明 |
|------|------|------|
| PowerShell | ✅ OK | 运行正常 |
| Git | ✅ OK | C:\Program Files\Git\cmd\git.exe |
| Python | ✅ OK | 3.11.9 |
| Workspace | ✅ OK | 目录结构完整 |
| FFmpeg | ⚠️ Not Found | 需要安装：winget install Gyan.FFmpeg |

**下一步**：安装 FFmpeg 后开始视频制作测试

---

## 📂 脚本文件

位于 `~/.openclaw/workspace/scripts/`：

| 脚本 | 用途 |
|------|------|
| `morning-check.ps1` | 每日晨检 |
| `test-cli-simple.ps1` | CLI-Anything环境测试 |
| `video-production-workflow.ps1` | 完整视频制作流程 |
| `batch-transcode.ps1` | 批量视频转码 |
| `auto-clip.ps1` | 自动剪辑视频片段 |
| `multi-publish.ps1` | 多平台自动发布 |

---

## 🔗 相关链接

- CLI-Anything 仓库：https://github.com/simonw/cli-anything
- FFmpeg 下载：https://ffmpeg.org/download.html
- PowerShell 文档：https://docs.microsoft.com/powershell

---

**Windows 环境已就绪，等待 FFmpeg 安装后开始视频制作自动化！**

---

*最后更新：2026-03-15*
