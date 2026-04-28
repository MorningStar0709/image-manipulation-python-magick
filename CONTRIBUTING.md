# Contributing

Thanks for considering a contribution to this project.

## Scope

Useful contributions include:

- bug fixes in the CLI or profile behavior
- documentation improvements
- safer defaults and better error reporting
- additional reusable profiles
- cross-platform compatibility improvements

## Development Notes

- Keep the CLI dependency-light and prefer the Python standard library
- Preserve the current design: Python orchestration plus ImageMagick execution
- Favor safe defaults such as non-overwrite behavior and explicit output paths
- Keep command output structured and machine-readable where practical
- Update documentation when behavior or examples change

## Suggested Workflow

1. Fork the repository and create a topic branch.
2. Make focused changes with clear commit messages.
3. Verify the CLI help output and any changed behavior locally.
4. Update `README.md` and `README.zh-CN.md` if user-facing behavior changes.
5. Open a pull request with a concise summary and validation notes.

## Validation

At minimum, validate the commands relevant to your changes, for example:

```bash
python skills/image-manipulation-python-magick/scripts/image_tool.py --help
python skills/image-manipulation-python-magick/scripts/image_tool.py profiles
python skills/image-manipulation-python-magick/scripts/image_tool.py doctor
python -m unittest discover -s tests -p "test_*.py"
```

If your changes affect batch behavior, also validate a `--dry-run` batch example.

## Style

- Prefer readable, stable implementations over overly clever shortcuts
- Keep changes small and easy to review
- Avoid unrelated refactors in the same pull request
