# Python + ImageMagick 图片处理工具

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue)
![ImageMagick](https://img.shields.io/badge/ImageMagick-required-orange)

[English README](./README.md) | [报告问题](https://github.com/MorningStar0709/image-manipulation-python-magick/issues/new?template=bug-report.yml) | [功能建议](https://github.com/MorningStar0709/image-manipulation-python-magick/issues/new?template=feature-request.yml)

这是一个基于 Python 主控、由 ImageMagick 执行实际图像处理的规则化图片处理工具仓库。

仓库同时提供可直接调用的 CLI，以及可放入 Trae 环境中的 skill 定义，适合做格式转换、尺寸调整、居中裁成方图、补边成方图、元数据查看，以及可重复执行的批处理任务。

## 一眼看懂

- 仓库地址：`MorningStar0709/image-manipulation-python-magick`
- 核心 CLI：`skills/image-manipulation-python-magick/scripts/image_tool.py`
- skill 定义：`skills/image-manipulation-python-magick/SKILL.md`
- 适用场景：规则化、可重复的图片处理任务，而不是手工 GUI 修图

想了解这个工具适合谁用、能解决什么问题？查看 [使用场景](./use-cases.zh-CN.md)。(中文 | [English](./use-cases.md))

## 项目特点

- 仅依赖 Python 标准库，图像处理由 ImageMagick 完成
- 既支持单次命令，也支持基于 JSON 配置的可重复批处理
- 内置头像、社媒方图、补边方图、缩略图、WEBP 导出、FHD 壁纸等常用 profile
- 默认更安全：不覆盖已有文件、支持 `--dry-run` 预演、支持 `--manifest` 产出清单
- 兼容 Windows、Linux、macOS，只要系统可用 `magick`

## 仓库结构

```text
.
|-- README.md
|-- README.zh-CN.md
|-- LICENSE
|-- CONTRIBUTING.md
|-- examples/
|   `-- thumbnail-job.json
`-- skills/
    `-- image-manipulation-python-magick/
        |-- SKILL.md
        `-- scripts/
            `-- image_tool.py
```

## 仓库提供了什么

这个仓库包含两个紧密相关的部分：

- 可直接运行的 Python CLI：`skills/image-manipulation-python-magick/scripts/image_tool.py`
- 面向 Trae 的 skill 定义：`skills/image-manipulation-python-magick/SKILL.md`

如果你是直接在这个仓库中使用脚本，请使用下面示例中的 `skills/...` 路径。

如果你是把它安装为 Trae skill，则这些文件可以放到本地环境的 `.trae/skills/...` 目录下。

## 环境要求

- Python 3.10 或更高版本
- 已安装 ImageMagick，且系统中可调用 `magick`

CLI 会优先从 `PATH` 中查找 `magick`。在 Windows 上，它还会额外检查若干常见安装目录。

## 快速开始

检查环境是否就绪：

```bash
python skills/image-manipulation-python-magick/scripts/image_tool.py doctor
```

查看内置 profile：

```bash
python skills/image-manipulation-python-magick/scripts/image_tool.py profiles
```

查看单张图片信息：

```bash
python skills/image-manipulation-python-magick/scripts/image_tool.py info --input path/to/image.jpg
```

将一张图片转换为 WEBP：

```bash
python skills/image-manipulation-python-magick/scripts/image_tool.py convert --input path/to/image.png --output path/to/output.webp
```

调整单张图片尺寸：

```bash
python skills/image-manipulation-python-magick/scripts/image_tool.py resize --input path/to/image.jpg --output path/to/resized.jpg --width 1280 --height 720
```

将单张图片居中裁成方图：

```bash
python skills/image-manipulation-python-magick/scripts/image_tool.py crop-square --input path/to/image.jpg --output path/to/square.jpg
```

将单张图片补边成方图：

```bash
python skills/image-manipulation-python-magick/scripts/image_tool.py pad-square --input path/to/image.png --output path/to/padded.png --background white
```

## 批量处理

先用内置 profile 做一次预演：

```bash
python skills/image-manipulation-python-magick/scripts/image_tool.py batch ^
  --input path/to/images ^
  --output path/to/output ^
  --profile thumbnail ^
  --recursive ^
  --dry-run
```

实际批量转成 WEBP，并输出 manifest：

```bash
python skills/image-manipulation-python-magick/scripts/image_tool.py batch ^
  --input path/to/images ^
  --output path/to/output ^
  --action convert ^
  --format webp ^
  --suffix _web ^
  --quality 85 ^
  --recursive ^
  --manifest path/to/output/manifest.json
```

使用 JSON 配置来执行可重复任务：

```bash
python skills/image-manipulation-python-magick/scripts/image_tool.py init-config --output image-job.json --profile thumbnail
python skills/image-manipulation-python-magick/scripts/image_tool.py batch --config image-job.json
```

仓库中附带了一个示例配置文件：`examples/thumbnail-job.json`。

## 支持的命令

CLI 提供以下子命令：

- `doctor`：检查 Python 和 ImageMagick 是否可用
- `profiles`：列出内置处理 profile
- `init-config`：生成一个起始 JSON 配置文件
- `info`：查看图片尺寸和基础元数据
- `convert`：转换单张图片格式
- `resize`：调整单张图片尺寸
- `crop-square`：将单张图片居中裁成方图
- `pad-square`：将单张图片补边成方图
- `batch`：对目录或单张图片执行批处理

## 内置 Profile

- `avatar`：生成头像或个人资料图片用的居中方形 JPG
- `social-square`：生成社媒方图或封面图用的居中方形 JPG
- `square-pad`：完整保留内容，并补边到方形 PNG 画布
- `thumbnail`：生成适合列表或画廊的缩略图
- `webp-web`：批量转成适合网页使用的 WEBP
- `wallpaper-fhd`：调整到 `1920x1080` 的全高清壁纸尺寸

## 输出与安全策略

- 默认跳过已存在的输出文件
- 大批量任务可先通过 `--dry-run` 做预演
- 批处理可通过 `--manifest` 写出 JSON 清单
- 支持 `--min-width` 和 `--min-height` 做阈值过滤
- 除非显式指定 `--fail-fast`，否则单个文件失败不会中断整个批处理

## 配置文件示例

```json
{
  "tool_version": "0.2.0",
  "profile": "thumbnail",
  "input": "path/to/images",
  "output": "path/to/output",
  "recursive": true,
  "pattern": "*.png",
  "manifest": "path/to/output/manifest.json",
  "action": "resize",
  "width": 427,
  "height": 240,
  "suffix": "_thumb",
  "quality": 85
}
```

## 典型使用场景

- 快速生成统一风格的头像或资料图
- 为社媒内容批量生成方图
- 将 PNG 或 JPG 图片批量转换为 WEBP
- 批量生成列表页或相册用缩略图
- 将输出写到独立目录，避免污染源目录
- 将常用批处理任务保存为 JSON 配置长期复用

## 当前限制

- 某些图片格式依赖宿主环境中的 ImageMagick delegates
- 颜色配置、透明通道处理和不同 delegates 可能导致视觉结果略有差异
- 超大图片会占用更多内存和临时磁盘空间
- 当前仓库以脚本形式分发，并未封装成 PyPI 安装包

## 贡献

欢迎提交改进。可参考 [CONTRIBUTING.md](./CONTRIBUTING.md)。

## 社区文件

- 安全策略：[SECURITY.md](./SECURITY.md)
- 行为规范：[CODE_OF_CONDUCT.md](./CODE_OF_CONDUCT.md)
- PR 模板：[pull_request_template.md](./.github/pull_request_template.md)
- 变更记录：[CHANGELOG.md](./CHANGELOG.md)
- 路线图：[ROADMAP.md](./ROADMAP.md)

## 许可证

本项目采用 [MIT License](./LICENSE) 开源。
