# CLI-Anything 详细运用指南

> 创建时间：2026-03-15  
> 适用对象：大德米（本地Mac环境）  
> 版本：v1.0

---

## 📋 目录

1. [CLI-Anything 简介](#cli-anything-简介)
2. [安装配置](#安装配置)
3. [核心概念](#核心概念)
4. [支持的软件](#支持的软件)
5. [使用示例](#使用示例)
6. [与Agent Browser配合](#与agent-browser配合)
7. [故障排查](#故障排查)
8. [最佳实践](#最佳实践)

---

## CLI-Anything 简介

**CLI-Anything** 是一个将任意本地软件变成 Agent 可控的 CLI 工具的框架。

### 核心功能
- 将GUI软件（GIMP、Kdenlive等）转换为命令行控制
- 支持批量处理和自动化工作流
- 与OpenClaw Agent无缝集成
- 本地执行，无需云端API

### 项目地址
- **GitHub**: https://github.com/HKUDS/CLI-Anything
- **论文**: https://arxiv.org/abs/2502.09772

---

## 安装配置

### 前置要求
- macOS系统（推荐）
- Python 3.8+
- 已安装目标软件（GIMP、Kdenlive等）

### 安装步骤

```bash
# 1. 克隆仓库
git clone https://github.com/HKUDS/CLI-Anything.git
cd CLI-Anything

# 2. 安装依赖
pip install -r requirements.txt

# 3. 安装CLI-Anything
pip install -e .

# 4. 验证安装
cli-anything --version
```

### 配置软件插件

CLI-Anything通过插件系统支持不同软件：

```bash
# 列出可用插件
cli-anything plugins list

# 安装GIMP插件
cli-anything plugins install gimp

# 安装Kdenlive插件
cli-anything plugins install kdenlive

# 安装LibreOffice插件
cli-anything plugins install libreoffice
```

---

## 核心概念

### 1. 动作（Action）
软件中的具体操作，如：
- `open` - 打开文件
- `export` - 导出文件
- `apply_filter` - 应用滤镜

### 2. 参数（Parameter）
动作的输入值，如：
- 文件路径
- 滤镜名称
- 导出格式

### 3. 工作流（Workflow）
多个动作的组合，形成完整任务：
```
打开图片 → 调整大小 → 应用滤镜 → 导出
```

---

## 支持的软件

### 图像处理

#### GIMP
```bash
# 打开图片
cli-anything gimp open ./photo.jpg

# 调整大小
cli-anything gimp resize --width 1920 --height 1080

# 应用滤镜
cli-anything gimp filter apply --name "Gaussian Blur" --radius 2.0

# 导出
cli-anything gimp export --format png --output ./output.png

# 批量处理
cli-anything gimp batch ./input_folder --action "resize:1920x1080" --output ./output_folder
```

**常用滤镜：**
- `Gaussian Blur` - 高斯模糊
- `Unsharp Mask` - 锐化
- `Color Balance` - 色彩平衡
- `Brightness-Contrast` - 亮度对比度

### 视频剪辑

#### Kdenlive
```bash
# 创建新项目
cli-anything kdenlive project new --name "Hospital_Promo" --profile hd1080p30

# 导入素材
cli-anything kdenlive clip import ./hospital_footage.mp4 --track video
cli-anything kdenlive clip import ./voiceover.mp3 --track audio

# 添加转场
cli-anything kdenlive transition add --type dissolve --duration 1.5

# 添加字幕
cli-anything kdenlive subtitle add --text "Welcome to China Hospitals Guide" --start 0:00:05 --duration 3

# 导出视频
cli-anything kdenlive render --format mp4 --quality high --output ./final_video.mp4
```

**常用转场：**
- `dissolve` - 淡入淡出
- `wipe` - 擦除
- `slide` - 滑动
- `fade` - 渐变

### 文档处理

#### LibreOffice
```bash
# 创建文档
cli-anything libreoffice document new --type writer --name "Medical_Guide"

# 插入内容
cli-anything libreoffice insert --type text --content "Welcome to China"
cli-anything libreoffice insert --type table --rows 5 --cols 3
cli-anything libreoffice insert --type image --file ./hospital.jpg

# 应用样式
cli-anything libreoffice style apply --name "Heading 1"

# 导出PDF
cli-anything libreoffice export --format pdf --output ./guide.pdf
```

### 音频处理

#### Audacity
```bash
# 打开音频
cli-anything audacity open ./voiceover.wav

# 降噪
cli-anything audacity noise_reduction --profile ./noise_profile.np

# 标准化音量
cli-anything audacity normalize --level -1.0

# 导出
cli-anything audacity export --format mp3 --quality 192 --output ./clean_audio.mp3
```

---

## 使用示例

### 示例1：批量处理医院图片

**场景**：为医疗旅游网站批量处理医院照片

```bash
#!/bin/bash
# batch_process_hospitals.sh

INPUT_DIR="./raw_hospital_photos"
OUTPUT_DIR="./processed_photos"
WATERMARK="ChinaHospitalsGuide.com"

# 创建输出目录
mkdir -p $OUTPUT_DIR

# 批量处理每张图片
for img in $INPUT_DIR/*.jpg; do
    filename=$(basename "$img")
    
    cli-anything gimp open "$img"
    cli-anything gimp resize --width 1200 --height 800 --mode crop
    cli-anything gimp filter apply --name "Unsharp Mask" --amount 0.8
    cli-anything gimp watermark add --text "$WATERMARK" --position bottom-right --opacity 50
    cli-anything gimp export --format jpg --quality 85 --output "$OUTPUT_DIR/$filename"
    cli-anything gimp close
done

echo "处理完成！共处理 $(ls $INPUT_DIR/*.jpg | wc -l) 张图片"
```

### 示例2：自动生成宣传视频

**场景**：根据文案自动生成医疗旅游宣传视频

```bash
#!/bin/bash
# generate_promo_video.sh

PROJECT_NAME="Medical_Tourism_Promo_$(date +%Y%m%d)"
OUTPUT_FILE="./promo_videos/${PROJECT_NAME}.mp4"

# 1. 创建项目
cli-anything kdenlive project new --name "$PROJECT_NAME" --profile hd1080p30

# 2. 导入素材
cli-anything kdenlive clip import ./assets/intro.mp4 --track video --position 0
cli-anything kdenlive clip import ./assets/hospital_shots.mp4 --track video --position 5
cli-anything kdenlive clip import ./assets/patient_testimonials.mp4 --track video --position 30
cli-anything kdenlive clip import ./assets/background_music.mp3 --track audio --position 0

# 3. 添加字幕（从文案文件读取）
line_number=0
while IFS= read -r line; do
    start_time=$((5 + line_number * 5))
    cli-anything kdenlive subtitle add \
        --text "$line" \
        --start "0:00:$start_time" \
        --duration 4 \
        --style "white,bold,shadow"
    ((line_number++))
done < ./scripts/video_script.txt

# 4. 添加转场
cli-anything kdenlive transition add --type dissolve --between 0,1 --duration 1
cli-anything kdenlive transition add --type dissolve --between 1,2 --duration 1

# 5. 渲染输出
cli-anything kdenlive render \
    --format mp4 \
    --codec h264 \
    --quality high \
    --output "$OUTPUT_FILE"

echo "视频生成完成：$OUTPUT_FILE"
```

### 示例3：生成PDF指南

**场景**：自动生成医院指南PDF文档

```bash
#!/bin/bash
# generate_hospital_guide.sh

HOSPITAL_NAME="北京协和医院"
OUTPUT_FILE="./guides/${HOSPITAL_NAME}_Guide.pdf"

# 创建文档
cli-anything libreoffice document new --type writer --name "$HOSPITAL_NAME Guide"

# 添加标题
cli-anything libreoffice insert --type text --content "$HOSPITAL_NAME - 国际患者指南" --style "Title"

# 添加章节
cli-anything libreoffice insert --type text --content "1. 医院简介" --style "Heading 1"
cli-anything libreoffice insert --type text --content "北京协和医院是中国最著名的综合性医院之一..." --style "Normal"

cli-anything libreoffice insert --type text --content "2. 联系方式" --style "Heading 1"
cli-anything libreoffice insert --type table --rows 4 --cols 2
cli-anything libreoffice table fill --data "电话,010-12345678|地址,北京市东城区...|邮箱,international@pumch.cn|网站,www.pumch.cn"

cli-anything libreoffice insert --type text --content "3. 就诊流程" --style "Heading 1"
cli-anything libreoffice insert --type list --ordered --items "预约登记|提交病历|视频会诊|确认行程|入院治疗"

# 插入医院图片
cli-anything libreoffice insert --type image --file ./assets/pumch_building.jpg --align center

# 导出PDF
cli-anything libreoffice export --format pdf --output "$OUTPUT_FILE"

echo "PDF指南生成完成：$OUTPUT_FILE"
```

---

## 与Agent Browser配合

### 完整工作流：从文案到发布

```
┌─────────────────────────────────────────────────────────────┐
│  步骤1: 文案生成 (豆包API)                                    │
│  - 生成博客文章/视频脚本/社媒文案                              │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  步骤2: 内容制作 (CLI-Anything)                               │
│  - GIMP: 制作配图                                            │
│  - Kdenlive: 剪辑视频                                        │
│  - LibreOffice: 生成PDF                                      │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  步骤3: 内容发布 (Agent Browser)                              │
│  - 知乎: 发布文章                                            │
│  - 小红书: 发布图文                                          │
│  - Twitter: 发布推文                                         │
│  - YouTube: 上传视频                                         │
└─────────────────────────────────────────────────────────────┘
```

### 集成脚本示例

```bash
#!/bin/bash
# full_pipeline.sh - 端到端自动化流程

CONTENT_TYPE="blog"  # blog, video, social
PLATFORM="zhihu"     # zhihu, xiaohongshu, twitter, youtube

# 1. 生成文案（调用豆包API）
echo "=== 步骤1: 生成文案 ==="
python3 generate_content.py --type $CONTENT_TYPE --topic "医疗旅游" --output ./content.txt

# 2. 制作内容
if [ "$CONTENT_TYPE" == "video" ]; then
    echo "=== 步骤2: 制作视频 ==="
    ./generate_promo_video.sh ./content.txt
    CONTENT_FILE="./output/video.mp4"
else
    echo "=== 步骤2: 制作配图 ==="
    ./batch_process_hospitals.sh
    CONTENT_FILE="./content.txt"
fi

# 3. 发布内容
echo "=== 步骤3: 发布到 $PLATFORM ==="
agent-browser state load ${PLATFORM}_cookies.json
agent-browser open https://${PLATFORM}.com

# 根据平台执行不同发布流程
case $PLATFORM in
    "zhihu")
        agent-browser click @write_article
        agent-browser fill @title_input "医疗旅游指南"
        agent-browser fill @content_editor "$(cat $CONTENT_FILE)"
        agent-browser click @publish_button
        ;;
    "xiaohongshu")
        agent-browser click @publish
        agent-browser upload @image_upload ./output/cover.jpg
        agent-browser fill @title "中国医疗旅游体验"
        agent-browser fill @content "$(cat $CONTENT_FILE | head -100)"
        agent-browser click @publish_now
        ;;
    "youtube")
        agent-browser open https://studio.youtube.com
        agent-browser click @upload
        agent-browser upload @file_input $CONTENT_FILE
        agent-browser fill @title "Medical Tourism in China - Complete Guide"
        agent-browser fill @description "$(cat $CONTENT_FILE)"
        agent-browser click @publish
        ;;
esac

echo "=== 发布完成 ==="
```

---

## 故障排查

### 常见问题

#### 1. 软件无法启动
```bash
# 检查软件是否安装
which gimp
which kdenlive

# 检查CLI-Anything配置
cli-anything config verify

# 重新安装插件
cli-anything plugins reinstall gimp
```

#### 2. 动作执行失败
```bash
# 启用调试模式
cli-anything --debug gimp open ./test.jpg

# 查看日志
tail -f ~/.cli-anything/logs/debug.log
```

#### 3. 批量处理中断
```bash
# 使用resume功能继续
cli-anything batch resume --job-id 12345

# 跳过已处理文件
cli-anything batch ./input --skip-existing --output ./output
```

### 调试技巧

```bash
# 1. 测试单个动作
cli-anything gimp --dry-run open ./test.jpg

# 2. 查看可用动作
cli-anything gimp actions list

# 3. 查看动作参数
cli-anything gimp actions describe --name resize

# 4. 录制操作过程
cli-anything record start ./debug_recording
cli-anything gimp open ./test.jpg
cli-anything record stop
```

---

## 最佳实践

### 1. 脚本模板化

为常用任务创建脚本模板：

```bash
# templates/process_image.template
cli-anything gimp open {{INPUT_FILE}}
cli-anything gimp resize --width {{WIDTH}} --height {{HEIGHT}}
cli-anything gimp filter apply --name "{{FILTER}}"
cli-anything gimp export --format {{FORMAT}} --output {{OUTPUT_FILE}}
```

### 2. 错误处理

```bash
#!/bin/bash
set -e  # 遇到错误立即退出

# 错误处理函数
error_handler() {
    echo "错误发生在第 $1 行"
    # 发送通知
    curl -X POST "https://api.notify.com/alert" -d "message=CLI-Anything任务失败"
}

trap 'error_handler $LINENO' ERR

# 主任务
cli-anything kdenlive project new --name "Test"
# ...
```

### 3. 日志记录

```bash
# 启用详细日志
export CLI_ANYTHING_LOG_LEVEL=debug
export CLI_ANYTHING_LOG_FILE=./logs/cli-anything-$(date +%Y%m%d).log

# 执行任务并记录
cli-anything gimp batch ./input --output ./output 2>&1 | tee -a $CLI_ANYTHING_LOG_FILE
```

### 4. 性能优化

```bash
# 并行处理
cli-anything batch ./input --parallel 4 --output ./output

# 使用GPU加速（如支持）
cli-anything kdenlive render --gpu --output ./video.mp4

# 缓存中间结果
cli-anything --cache ./cache_dir gimp open ./large_file.psd
```

---

## 参考资源

- **GitHub**: https://github.com/HKUDS/CLI-Anything
- **文档**: https://cli-anything.readthedocs.io
- **示例**: https://github.com/HKUDS/CLI-Anything/tree/main/examples
- **论文**: https://arxiv.org/abs/2502.09772

---

## 更新记录

| 日期 | 版本 | 更新内容 |
|------|------|---------|
| 2026-03-15 | v1.0 | 初始版本，包含GIMP/Kdenlive/LibreOffice/Audacity详细用法 |

---

*文档创建者：德米*  
*适用对象：大德米（本地Mac环境）*  
*关联文档：AI团队架构方案.md, Agent Browser SKILL.md*
