# Image Manipulation with Python and ImageMagick

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue)
![ImageMagick](https://img.shields.io/badge/ImageMagick-required-orange)

[中文说明](./README.zh-CN.md) | [Report Bug](https://github.com/MorningStar0709/image-manipulation-python-magick/issues/new?template=bug-report.yml) | [Request Feature](https://github.com/MorningStar0709/image-manipulation-python-magick/issues/new?template=feature-request.yml)

Rule-based image processing toolkit powered by Python orchestration and ImageMagick execution.

This repository packages a reusable CLI and a Trae skill for common image workflows such as format conversion, resizing, square crop, square padding, metadata inspection, and repeatable batch jobs.

## At A Glance

- Repository: `MorningStar0709/image-manipulation-python-magick`
- Primary CLI: `skills/image-manipulation-python-magick/scripts/image_tool.py`
- Skill definition: `skills/image-manipulation-python-magick/SKILL.md`
- Best for: repeatable, rule-based image workflows instead of manual GUI editing

Want to know who this tool is for and what problems it solves? Check out the [use cases](./use-cases.md). (English | [中文](./use-cases.zh-CN.md))

## Highlights

- Python standard library only, with ImageMagick used as the processing backend
- Works for one-off commands and repeatable config-driven batch workflows
- Built-in profiles for avatars, social square images, thumbnails, WEBP export, and Full HD wallpapers
- Safe defaults: non-overwrite behavior, optional dry-run, optional manifest output
- Supports Windows, Linux, and macOS when `magick` is available

## Repository Layout

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

## What This Project Provides

This repository contains two closely related parts:

- A reusable Python CLI entrypoint at `skills/image-manipulation-python-magick/scripts/image_tool.py`
- A Trae skill definition at `skills/image-manipulation-python-magick/SKILL.md`

If you are using the script directly from this repository, use the `skills/...` path shown in the examples below.

If you are installing it as a Trae skill, the same files can be placed under `.trae/skills/...` in your local environment.

## Requirements

- Python 3.10 or newer
- ImageMagick installed and available as `magick`

The CLI first tries `magick` from `PATH`, then `IMAGEMAGICK_HOME`, and on Windows it also checks a few common install directories.

## Quick Start

Check environment readiness:

```bash
python skills/image-manipulation-python-magick/scripts/image_tool.py doctor
```

List built-in profiles:

```bash
python skills/image-manipulation-python-magick/scripts/image_tool.py profiles
```

Inspect one image:

```bash
python skills/image-manipulation-python-magick/scripts/image_tool.py info --input path/to/image.jpg
```

Convert one image to WEBP:

```bash
python skills/image-manipulation-python-magick/scripts/image_tool.py convert --input path/to/image.png --output path/to/output.webp
```

Resize one image:

```bash
python skills/image-manipulation-python-magick/scripts/image_tool.py resize --input path/to/image.jpg --output path/to/resized.jpg --width 1280 --height 720
```

Crop one image to a centered square:

```bash
python skills/image-manipulation-python-magick/scripts/image_tool.py crop-square --input path/to/image.jpg --output path/to/square.jpg
```

Pad one image to a square canvas:

```bash
python skills/image-manipulation-python-magick/scripts/image_tool.py pad-square --input path/to/image.png --output path/to/padded.png --background white
```

## Batch Processing

Use `\` for line continuation in Bash or Zsh. In PowerShell, replace it with a trailing backtick.

Run a dry-run batch job with a built-in profile:

```bash
python skills/image-manipulation-python-magick/scripts/image_tool.py batch \
  --input path/to/images \
  --output path/to/output \
  --profile thumbnail \
  --recursive \
  --dry-run
```

Run a real batch conversion to WEBP and write a manifest:

```bash
python skills/image-manipulation-python-magick/scripts/image_tool.py batch \
  --input path/to/images \
  --output path/to/output \
  --action convert \
  --format webp \
  --suffix _web \
  --quality 85 \
  --recursive \
  --manifest path/to/output/manifest.json
```

Use a JSON config for repeatable jobs:

```bash
python skills/image-manipulation-python-magick/scripts/image_tool.py init-config --output image-job.json --profile thumbnail
python skills/image-manipulation-python-magick/scripts/image_tool.py batch --config image-job.json
```

An example config is available at `examples/thumbnail-job.json`.

## Commands

The CLI supports the following subcommands:

- `doctor`: check Python and ImageMagick availability
- `profiles`: list built-in processing profiles
- `init-config`: create a starter JSON config
- `info`: inspect image dimensions and metadata
- `convert`: convert one image to another format
- `resize`: resize one image
- `crop-square`: crop one image to a centered square
- `pad-square`: pad one image to a square canvas
- `batch`: batch process a directory or a single image file

## Built-In Profiles

- `avatar`: centered square JPG output for avatars or profile photos
- `social-square`: centered square JPG output for social posts or covers
- `square-pad`: preserve full content and pad to a square PNG canvas
- `thumbnail`: compact thumbnail output for galleries or lists
- `webp-web`: convert images to WEBP for web delivery
- `wallpaper-fhd`: resize to `1920x1080` for Full HD wallpapers

## Output and Safety Behavior

- Existing output files are skipped by default
- Large jobs can be previewed with `--dry-run`
- Batch jobs can write a manifest JSON with `--manifest`
- Threshold filters are supported with `--min-width` and `--min-height`
- The tool continues processing other files unless `--fail-fast` is specified

## Example Config

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

## Typical Use Cases

- Create consistent avatar and profile images
- Generate square social images quickly
- Convert PNG or JPG collections to WEBP
- Produce gallery thumbnails in bulk
- Keep source directories untouched while writing outputs elsewhere
- Store repeatable batch jobs as JSON configs

## Limitations

- Some formats depend on ImageMagick delegates installed on the host machine
- Exact visual output can vary with color profile handling, alpha behavior, and delegates
- Very large images may require more memory and temporary disk usage
- The repository is distributed as a script-based tool, not as a packaged PyPI library

## Contributing

Contributions are welcome. See [CONTRIBUTING.md](./CONTRIBUTING.md) for guidance.

## Community

- Security policy: [SECURITY.md](./SECURITY.md)
- Code of conduct: [CODE_OF_CONDUCT.md](./CODE_OF_CONDUCT.md)
- Pull request guide: [pull_request_template.md](./.github/pull_request_template.md)
- Changelog: [CHANGELOG.md](./CHANGELOG.md)
- Roadmap: [ROADMAP.md](./ROADMAP.md)

## License

This project is licensed under the [MIT License](./LICENSE).
