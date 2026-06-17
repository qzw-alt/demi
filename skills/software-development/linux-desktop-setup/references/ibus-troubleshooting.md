# ibus 输入法故障排查记录（Pop!_OS）

## 本次排查路径

### 问题：ibus 已装但无法添加中文输入法

**关键发现：**
- Pop!_OS 桌面默认用 ibus，不是 fcitx5
- 混用会导致环境变量冲突，`echo $XMODIFIERS` 显示 `@im=ibus` 时应该用 ibus

### 正确步骤（已验证）

```bash
# 1. 安装中文引擎（包名是 ibus-libpinyin，不是 ibus-chinese）
sudo apt install ibus-libpinyin

# 2. 如果 ibus-daemon 没跑，手动启动
ibus-daemon -drx &

# 3. 检查进程
ps aux | grep ibus
# 应看到：ibus-daemon、ibus-ui-gtk3、ibus-extension-gtk3、ibus-engine-simple

# 4. 用 ibus-setup 添加输入法
ibus-setup
# Input Method → Add → 搜 "Chinese" → 选 "Chinese (Intelligent Pinyin)"
```

### 踩过的坑

- `ibus list-engines`（复数）→ 命令打错，正确是 `ibus list-engine`（单数）
- 包名 `ibus-chinese` 不存在，正确是 `ibus-libpinyin`
- `ibus-daemon -drx &` 后显示 "已完成" 是正常的，进程已经在后台跑
- 添加输入法在 `ibus-setup` 图形界面里找，不是命令行

### 环境变量（供参考）

```
XMODIFIERS=@im=ibus
GTK_IM_MODULE=ibus
QT_IM_MODULE=ibus
LANG=zh_CN.UTF-8
```

### 切换快捷键

`Ctrl+Space` 切换中英文