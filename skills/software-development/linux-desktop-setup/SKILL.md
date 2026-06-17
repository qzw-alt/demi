---
name: linux-desktop-setup
description: Linux 桌面系统安装配置（Ubuntu/Pop!_OS）— 发行版选择、分区、驱动、中文输入法、常见问题
triggers:
  - "安装 Linux 系统"
  - "双系统"
  - "Linux 输入法"
  - "ibus"
  - "fcitx5"
  - "中文输入法"
---

# Linux 桌面系统配置（桌面版）

## 发行版选择

| 场景 | 推荐 |
|------|------|
| 新手 / 日常办公 | Ubuntu LTS、Linux Mint |
| NVIDIA 显卡 + 省心 | **Pop!_OS**（驱动开箱即用） |
| 老电脑 / 低配置 | Linux Mint XFCE、Lubuntu |
| 国内使用 + 中文 | Ubuntu 中文定制版、Deepin |

### Pop!_OS 安装注意事项

- BIOS 禁用 Secure Boot
- 推荐版本：**Pop!_OS 24.04 LTS (NVIDIA)**（支持 GTX 16xx 以上）
- 单系统全盘格式化最简单；双系统选"自定义分区"
- UEFI 引导，ESP 分区留 512MB

---

## 中文字体

```bash
sudo apt install fonts-noto-cjk  # 思源黑体/宋体
sudo apt install fonts-wqy-microhei  # 文泉驿微米黑
fc-list :lang=zh  # 列出已安装中文字体
```

---

## 输入法（ibus）

**ibus 是 Pop!_OS GNOME 桌面默认输入法框架**，不要跟 fcitx5 混用。

### 安装

```bash
sudo apt update
sudo apt install ibus-libpinyin  # 注意：包名是 ibus-libpinyin，不是 ibus-chinese
```

### 配置步骤

1. 启动 ibus-daemon（如果没自动跑）：
   ```bash
   ibus-daemon -drx &
   ```

2. 设置环境变量（通常是 ibus，如果不对才改）：
   ```bash
   im-config -n ibus
   ```

3. 注销重登录

4. 添加输入法：
   - 方法 A：`ibus-setup` → Input Method → Add → 搜 "Chinese" → 选 **Chinese (Intelligent Pinyin)**
   - 方法 B：系统设置 → 键盘 → 输入源 → + → 搜 "Chinese" → 选 "Chinese (Intelligent Pinyin)"

5. 用 Ctrl+Space 切换中英文

### 常用命令

```bash
ibus list-engine    # 查看可用引擎（注意是单数，不是 list-engines）
ibus restart        # 重启 ibus
ibus-daemon -drx &  # 手动启动 ibus
ps aux | grep ibus  # 检查是否在运行
```

### 排查流程

1. `ps aux | grep ibus` → ibus-daemon 没跑：`ibus-daemon -drx &`
2. `ibus list-engine` → 没有 Chinese 引擎：确认 `ibus-libpinyin` 装了
3. 系统设置里找不到中文选项：确保 ibus-daemon 在跑，再注销重登录
4. 环境变量检查：`echo $XMODIFIERS` 应为 `@im=ibus`

---

## 输入法（fcitx5）备选方案

如果要用 fcitx5（不是 ibus）：

```bash
sudo apt install fcitx5 fcitx5-chinese-addons fcitx5-configtool
```

环境变量要改成 fcitx5，编辑 `~/.xprofile` 或 `~/.profile`：

```bash
export GTK_IM_MODULE=fcitx5
export QT_IM_MODULE=fcitx5
export XMODIFIERS=@im=fcitx5
```

注销重登录后生效，用 `fcitx5-configtool` 配置。

---

## 常见硬件问题

### 硬盘只看到一个分区

```bash
lsblk -f                    # 查看分区和挂载状态
sudo fdisk -l /dev/sda      # 查看指定硬盘分区表
cat /proc/partitions        # 所有分区一览
sudo smartctl -a /dev/sda   # 硬盘健康检查
```

机械硬盘有分区但没挂载：
```bash
sudo mount /dev/sdb1 /mnt   # 挂载到 /mnt
sudo apt install ntfs-3g     # 如果是 NTFS 格式先装这个
```

### NVIDIA 显卡

- Pop!_OS 自带驱动，装完就能用
- 其他发行版：`sudo apt install nvidia-driver-xxx`（xxx 是版本号）
- 确认驱动装好：`nvidia-smi`

---

## 后续维护

```bash
sudo apt update && sudo apt upgrade  # 更新系统
sudo apt autoremove                 # 清理无用包
```