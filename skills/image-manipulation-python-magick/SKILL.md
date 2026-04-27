---
name: image-manipulation-python-magick
description: Process and manipulate images with Python orchestration and ImageMagick execution. Invoke when users need reusable image automation, batch conversion, resizing, cropping, padding, or metadata inspection.
compatibility: Requires Python 3.10+ and ImageMagick available as `magick` on PATH. Works on Windows, Linux, and macOS.
---

# Image Manipulation with Python and ImageMagick

This skill is for agent-driven, rule-based image processing using the bundled
Python CLI and ImageMagick.

## Purpose

Use this skill when the user needs:

- Batch image conversion, resizing, cropping, padding, or metadata inspection
- Repeatable image workflows driven by profiles or config files
- Safe automation with separate output directories, dry-run support, and
  manifest reporting

Typical trigger phrases include:

- "批量处理图片"
- "批量转格式"
- "裁成 1:1"
- "补白边"
- "生成缩略图"
- "压缩成 webp"
- "批量改尺寸"

## Do Not Use

Do not use this skill when:

- The user only wants installation help or conceptual explanation
- The user wants manual artistic editing in GUI tools
- The task depends on semantic image understanding rather than rule-based
  transforms

Do not execute shape-changing transforms immediately when crop vs pad is still
unresolved. Stay inside this skill and clarify first with `AskUserQuestion`.

## Task Classification

Classify requests before acting:

- `Consultation`: explain options only; do not run jobs or `doctor`
- `Single Execution`: run one concrete transform on one file
- `Batch Execution`: process a directory or many files
- `Repeatable Workflow`: prefer config-driven execution
- `Tooling Setup`: help the user establish a reusable workflow

## Intent Mapping

Prefer these mappings unless the user says otherwise:

- `头像`, `证件照`, `头像方图`, `profile photo`, `avatar` -> `avatar`
- `方形封面`, `社媒方图`, `social square`, `square cover` -> `social-square`
- `不要裁掉内容`, `完整保留`, `补白边`, `no crop`, `pad to square` -> `square-pad`
- `缩略图`, `列表图`, `thumbnail`, `preview image` -> `thumbnail`
- `压缩体积`, `转 webp`, `web optimization`, `convert to webp` -> `webp-web`
- `壁纸`, `1920x1080`, `wallpaper`, `fhd` -> `wallpaper-fhd`

If no profile fits exactly:

- `裁成 1:1` -> `crop-square`
- `补成 1:1` -> `pad-square`
- `统一尺寸` -> `resize`
- `批量转格式` -> `convert`
- `看尺寸 / 看格式 / 看元数据` -> `info`

Decision priority:

1. Preserve content
2. Avoid overwrite
3. Use a named profile
4. Use config for repeatable jobs
5. Use raw batch arguments only when necessary

## AskUserQuestion Policy

When clarification is necessary, prefer the software's structured
`AskUserQuestion` interaction mode instead of plain text follow-up.

Use `AskUserQuestion` when:

- The user must choose between crop and pad
- Output format materially affects compatibility
- Overwrite behavior must be confirmed
- Multiple profiles are plausible and one should be selected explicitly

Do not use `AskUserQuestion` when:

- A safe default is obvious and low-risk
- The task is purely informational
- The answer would not materially change execution

Question design rules:

- Ask 1 to 3 focused questions
- Put the safest recommended option first
- Use concrete wording like `裁切 1:1` vs `补边 1:1`

Recommended options:

- Square output: `补边 1:1 (Recommended)` / `裁切 1:1`
- Format: `保留原格式 (Recommended)` / `JPG` / `PNG` / `WEBP`
- Overwrite: `不覆盖 (Recommended)` / `覆盖已有文件`

## Execution Order

For execution-oriented tasks, use this order:

1. Classify the task
2. If ambiguity remains, use `AskUserQuestion`
3. Run `doctor` only if environment readiness is uncertain
4. Prefer `profiles` for common tasks
5. Prefer `init-config` plus `batch --config` for repeatable workflows
6. Use direct `batch` arguments only for one-off jobs
7. Use `--dry-run` before large or risky batch jobs
8. Save a `--manifest` when auditability matters

## Bundled CLI

Use the bundled script as the default execution entrypoint:

```text
.trae/skills/image-manipulation-python-magick/scripts/image_tool.py
```

Supported subcommands:

- `doctor`
- `profiles`
- `init-config`
- `info`
- `convert`
- `resize`
- `crop-square`
- `pad-square`
- `batch`

Common arguments:

- `--input`
- `--output`
- `--pattern`
- `--recursive`
- `--profile`
- `--config`
- `--format`
- `--width`
- `--height`
- `--quality`
- `--background`
- `--suffix`
- `--min-width`
- `--min-height`
- `--dry-run`
- `--overwrite`
- `--manifest`

Built-in profiles:

- `avatar`
- `social-square`
- `square-pad`
- `thumbnail`
- `webp-web`
- `wallpaper-fhd`

Use config for repeated jobs:

```bash
python .trae/skills/image-manipulation-python-magick/scripts/image_tool.py init-config --output image-job.json --profile thumbnail
python .trae/skills/image-manipulation-python-magick/scripts/image_tool.py batch --config image-job.json
```

## Safety Defaults

- Default to non-overwrite behavior
- Prefer output directories separate from source directories
- Prefer `--dry-run` before large batch execution
- Continue processing other files when one file fails unless fail-fast is explicitly required
- Prefer a manifest for batch tasks the user may revisit later

## Failure Recovery

Use these recovery rules:

- `magick not found` -> stop and explain environment is not ready
- Invalid input path -> stop and ask for the correct path
- Crop vs pad unresolved -> ask with `AskUserQuestion`
- Output exists -> skip by default; mention `--overwrite` only if replacement is intended
- No files matched -> report zero matches and suggest checking input path, pattern, or recursion
- Partial batch failure -> finish remaining files, then summarize failures
- Repeated complex job -> propose `init-config` plus `batch --config`

## Reporting Contract

When reporting back to the user:

- Start with the result, not internal command details
- Report operation, totals, success count, failure count, and output location
- Mention manifest path only if one was written
- Summarize failures briefly with actionable context
- Do not expose internal routing or orchestration details unless the user asks

Result templates:

```text
已完成图片处理：
- 操作：{operation}
- 输入：{source}
- 输出：{output}
```

```text
已完成批量图片处理：
- 操作：{operation}
- 总数：{total}
- 成功：{ok}
- 失败：{failed}
- 输出目录：{output_dir}
```

```text
已完成预演：
- 操作：{operation}
- 计划处理：{total}
- 实际写入：0
- 输出目录：{output_dir}
```

```text
已完成批量处理，但有部分文件失败：
- 操作：{operation}
- 总数：{total}
- 成功：{ok}
- 失败：{failed}
- 输出目录：{output_dir}

失败摘要：
- {failed_item}: {reason}
```

```text
本次没有处理任何图片：
- 输入：{input}
- 原因：未匹配到符合条件的文件
```

## Short Examples

```bash
python .trae/skills/image-manipulation-python-magick/scripts/image_tool.py doctor
python .trae/skills/image-manipulation-python-magick/scripts/image_tool.py profiles
python .trae/skills/image-manipulation-python-magick/scripts/image_tool.py info --input path/to/image.jpg
python .trae/skills/image-manipulation-python-magick/scripts/image_tool.py batch --input path/to/images --output path/to/output --profile thumbnail --dry-run
python .trae/skills/image-manipulation-python-magick/scripts/image_tool.py batch --config image-job.json
```

## Limitations

- Large batch operations may be slow without parallel execution
- Some formats require ImageMagick delegates to be installed
- Exact visual output can vary with color profile, alpha handling, and delegates
- Older environments may still use ImageMagick 6 semantics
- Very large images may require more memory and temporary disk usage
