import argparse
import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "skills" / "image-manipulation-python-magick" / "scripts" / "image_tool.py"

spec = importlib.util.spec_from_file_location("image_tool", MODULE_PATH)
image_tool = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules[spec.name] = image_tool
spec.loader.exec_module(image_tool)


class ImageToolTests(unittest.TestCase):
    def test_maybe_change_suffix_keeps_original_without_format(self):
        src = Path("gallery/photo.png")
        self.assertEqual(image_tool.maybe_change_suffix(src, None), src)

    def test_derive_output_path_preserves_relative_structure_and_changes_suffix(self):
        src = Path("input/nested/photo.png")
        output = image_tool.derive_output_path(
            src=src,
            input_root=Path("input"),
            output_root=Path("output"),
            output_format="webp",
            suffix="_thumb",
        )
        self.assertEqual(output, Path("output/nested/photo_thumb.webp"))

    def test_merge_batch_settings_prefers_cli_values_over_profile_defaults(self):
        args = argparse.Namespace(
            config=None,
            profile="thumbnail",
            input="path/to/images",
            output="path/to/output",
            action=None,
            recursive=True,
            pattern=None,
            format=None,
            suffix="_custom",
            quality=77,
            background=None,
            width=512,
            height=256,
            force=False,
            fill=False,
            min_width=None,
            min_height=None,
            overwrite=False,
            dry_run=True,
            fail_fast=False,
            manifest=None,
        )

        merged = image_tool.merge_batch_settings(args)

        self.assertEqual(merged.action, "resize")
        self.assertEqual(merged.width, 512)
        self.assertEqual(merged.height, 256)
        self.assertEqual(merged.suffix, "_custom")
        self.assertEqual(merged.quality, 77)
        self.assertTrue(merged.dry_run)

    def test_handle_init_config_writes_portable_placeholder_paths(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / "image-job.json"
            args = argparse.Namespace(output=str(output), profile="thumbnail")

            exit_code = image_tool.handle_init_config(args)

            self.assertEqual(exit_code, 0)
            payload = image_tool.load_json(output)
            self.assertEqual(payload["input"], "path/to/images")
            self.assertEqual(payload["output"], "path/to/output")
            self.assertEqual(payload["manifest"], "path/to/output/manifest.json")


if __name__ == "__main__":
    unittest.main()
