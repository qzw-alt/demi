---
name: linux-system-setup
description: "Linux系统安装、配置与日常使用技巧（桌面发行版）"
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [linux, system-setup, installation, troubleshooting]
    related_skills: [systematic-debugging]
---

# Linux 系统安装与配置

## 推荐的 Linux 发行版

### 主流桌面发行版选择

| 发行版 | 适用场景 | 特点 |
|--------|---------|------|
| **Pop!_OS** | 游戏 / AI / NVIDIA显卡 | NVIDIA驱动开箱即用，基于Ubuntu |
| **Ubuntu LTS** | 通用 / 想学服务器Linux | 生态最成熟，资源最丰富 |
| **Linux Mint** | 新手 / 从Windows过渡 | 界面最像Windows，上手最快 |
| **Fedora** | 开发 / 最新技术栈 | RHEL前哨，技术最新 |

### NVIDIA 显卡用户
- **首选 Pop!_OS**（自带NVIDIA驱动，无需手动安装）
- 其他发行版：安装后跑 `sudo apt install nvidia-driver-xxx`（xxx为驱动版本号）

---

## 安装前注意事项

### BIOS 设置
- **禁用 Secure Boot**，否则可能无法引导
- 设置从 USB 启动（DEL/F2 进BIOS）
- 确认硬盘模式为 AHCI（不是RAID/Intel RST）

### 双系统 vs 单系统
- **单系统**：全盘格式化，最简单
- **双系统**：选"自定义分区"，预留空间给Linux，避免覆盖Windows EFI

---

## 机械硬盘不识别问题

### 排查命令

```bash
# 查看所有硬盘和分区
lsblk

# 查看完整分区表
sudo fdisk -l /dev/sda

# 检查硬盘健康
sudo smartctl -a /dev/sda

# 查看内核日志（硬盘识别问题）
dmesg | grep -i "sda\|sdb\|disk\|nvme"
```

### 常见原因
1. Windows快速启动（Fast Startup）导致分区表不完整 → 关闭Windows快速启动
2. 硬盘数据线接触不良
3. 分区表损坏 → 用 `testdisk` 扫描修复

### 挂载已识别的分区
```bash
# NTFS格式（原来Windows的盘）
sudo apt install ntfs-3g
sudo mount -t ntfs-3g /dev/sdb1 /mnt

# ext4格式
sudo mount /dev/sdb1 /mnt
```

---

## 输入法配置（Linux 中文输入）

### 方案一：fcitx5（推荐，国内Linux用户普遍使用）

```bash
# 安装
sudo apt install fcitx5 fcitx5-chinese-addons fcitx5-pinyin

# 配置环境变量
echo "GTK_IM_MODULE=fcitx
QT_IM_MODULE=fcitx
XMODIFIERS=@im=fcitx" > ~/.xprofile

# 注销重登录后配置
fcitx5-configtool  # 添加拼音输入法
```

### 方案二：ibus（Ubuntu默认）

ibus 在某些发行版（如Pop!_OS）默认配置不完整，拼音引擎可能不加载。
若使用ibus：
```bash
# 安装拼音引擎
sudo apt install ibus-libpinyin

# 重置配置
im-config -n ibus
ibus restart
```

**ibus 排查**：若 `ibus list-engine` 输出中没有拼音引擎，说明 libpinyin 未正确加载，换 fcitx5。

---

## Windows 安装 U盘制作（Linux环境下）

### 方式一：WoeUSB（单次重装推荐）

```bash
# 添加PPA并安装（包名容易混淆）
sudo add-apt-repository ppa:tomtomtom/woeusb
sudo apt update
sudo apt install woeusb woeusb-frontend-wxgtk

# 启动图形界面（注意：命令名不是 woeusb-frontend-wxgtk）
sudo woeusbgui

# 命令行烧录
sudo woeusb --device "/path/to/windows.iso" /dev/sdX
```

⚠️ **注意**：
- `/dev/sdX` 是U盘设备名（不是分区名），如 `/dev/sdb`
-烧录前先卸载U盘所有分区：`sudo umount /dev/sdb1 /dev/sdb2`
- 若遇 "Target device is currently busy"：先 `umount` 所有挂载的分区

### 方式二：Ventoy（多次重装推荐）

- 下载：https://www.ventoy.net/cn/download.html
- 安装：`sudo sh Ventoy2Disk.sh -i /dev/sdX`（X为U盘设备名）
- 把ISO文件拷贝进U盘第一个分区即可
- 支持一个U盘放多个系统镜像

---

## 日常问题排查命令

```bash
# 查看系统信息
neofetch

# 查看已安装的输入法
fcitx5 --version
ibus list-engine

# 查看硬盘挂载情况
lsblk -f

# 查看内核启动日志
dmesg | less

# 检查包是否正确安装
dpkg -l | grep package-name
```

---

## 技能状态

- ✅ Pop!_OS 安装（NVIDIA版）
- ✅ fcitx5 拼音输入法配置
- ✅ WoeUSB 安装U盘制作
- ⏳ 机械硬盘E盘未识别（待排查）