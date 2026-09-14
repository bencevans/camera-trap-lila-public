import hashlib
import json
import tempfile
import unittest
from argparse import Namespace
from pathlib import Path

from filter.cli import (
    AZURE,
    ImageValidator,
    filtered,
    load,
    local_path,
    payload_hash,
    render_readme,
    run,
    stats,
    unavailable,
    write,
)
from PIL import Image


class FilterTests(unittest.TestCase):
    def test_generator_writes_exports_summary_and_replaces_readme(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            mirror = root / "mirror"
            mirror.mkdir()
            Image.new("RGB", (4, 4)).save(mirror / "public.jpg")
            data = {
                "images": [
                    {"id": 1, "file_name": "public.jpg"},
                    {"id": 2, "file_name": "missing.jpg"},
                ],
                "annotations": [{"id": 1, "image_id": 1, "category_id": 1}],
                "categories": [{"id": 1, "name": "animal"}],
            }
            (mirror / "metadata.json").write_text(json.dumps(data))
            catalog = {
                "release": "v3",
                "datasets": [
                    {
                        "name": "Example",
                        "url": "https://example.org",
                        "image_base": ".",
                        "labelsets": [
                            {
                                "name": "Metadata",
                                "slug": "example--metadata",
                                "source": AZURE + "metadata.json",
                            }
                        ],
                    }
                ],
            }
            (root / "catalog.json").write_text(json.dumps(catalog))
            (root / "introduction.md").write_text("# Example introduction\n")
            readme = root / "README.md"
            readme.write_text("Old README that should be replaced")
            output = root / "exports"
            run(
                Namespace(
                    catalog=root / "catalog.json",
                    introduction=root / "introduction.md",
                    lila_root=mirror,
                    output_dir=output,
                    cache=root / "cache.sqlite3",
                    workers=2,
                    processes=2,
                    readme=readme,
                    release=None,
                )
            )
            for suffix in ["public", "public.referenced"]:
                exported = load(output / f"example--metadata.{suffix}.json.zip")
                self.assertEqual(exported["images"], data["images"][:1])
                self.assertEqual(exported["annotations"], data["annotations"])
            summary = load(output / "summary.json")
            self.assertEqual(
                summary["labelsets"]["example--metadata"]["image_validation"][
                    "missing"
                ],
                1,
            )
            self.assertEqual(readme.read_bytes(), (output / "README.md").read_bytes())
            self.assertIn("# Example introduction", readme.read_text())
            self.assertIn("/v3/", readme.read_text())
            manifest = load(output / "manifest.json")
            self.assertEqual(manifest["counts"]["packages"], 2)
            # A selected run must preserve unselected outputs and use their saved statistics.
            before = (output / "example--metadata.public.json.zip").read_bytes()
            (mirror / "metadata.json").write_text("changed unselected metadata")
            (mirror / "second.json").write_text(json.dumps(data))
            second = json.loads(json.dumps(catalog["datasets"][0]))
            second["name"] = "Second"
            second["labelsets"][0]["slug"] = "second--metadata"
            second["labelsets"][0]["source"] = AZURE + "second.json"
            catalog["datasets"].append(second)
            (root / "catalog.json").write_text(json.dumps(catalog))
            args = Namespace(
                catalog=root / "catalog.json",
                introduction=root / "introduction.md",
                lila_root=mirror,
                output_dir=output,
                cache=root / "cache.sqlite3",
                workers=2,
                processes=2,
                readme=readme,
                release=None,
                dataset=["Second"],
            )
            run(args)
            self.assertEqual(
                before, (output / "example--metadata.public.json.zip").read_bytes()
            )
            self.assertEqual(load(output / "manifest.json")["counts"]["packages"], 4)
            self.assertIn("### Second", readme.read_text())
            # Documents-only must not read the changed source data or rewrite packages.
            args.dataset = None
            args.documents_only = True
            run(args)
            self.assertEqual(
                before, (output / "example--metadata.public.json.zip").read_bytes()
            )

    def test_corrupt_png_is_filtered_without_crashing(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / "bad.png"
            Image.new("RGB", (4, 4)).save(path)
            content = bytearray(path.read_bytes())
            marker = content.index(b"IDAT")
            length = int.from_bytes(content[marker - 4 : marker], "big")
            content[marker + 4 + length] ^= 1
            path.write_bytes(content)
            data = {
                "images": [{"id": 1, "file_name": "bad.png"}],
                "annotations": [],
                "categories": [],
            }
            public, referenced = filtered(data, root)
            self.assertEqual(public["images"], [])
            self.assertEqual(referenced["images"], [])

    def test_filters_without_mutating_or_reordering_metadata(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            Image.new("RGB", (2, 2)).save(root / "good.jpg")
            Image.new("RGB", (2, 2)).save(root / "unreferenced.jpg")
            (root / "bad.jpg").write_text("not an image")
            data = {
                "info": {"version": "test"},
                "images": [
                    {
                        "id": "good",
                        "file_name": "good.jpg",
                        "location": "a",
                        "seq_id": "s",
                    },
                    {"id": "bad", "file_name": "bad.jpg"},
                    {"id": "missing", "file_name": "missing.jpg"},
                    {"id": "unreferenced", "file_name": "unreferenced.jpg"},
                ],
                "annotations": [
                    {
                        "id": 1,
                        "image_id": "good",
                        "category_id": 1,
                        "bbox": [0, 0, 1, 1],
                    },
                    {"id": 2, "image_id": "bad", "category_id": 2},
                ],
                "categories": [{"id": 1, "name": "animal"}, {"id": 2, "name": "human"}],
                "custom": {"untouched": True},
            }
            before = json.dumps(data)
            public, referenced = filtered(data, root)
            self.assertEqual(
                [x["id"] for x in public["images"]], ["good", "unreferenced"]
            )
            self.assertEqual([x["id"] for x in referenced["images"]], ["good"])
            self.assertEqual([x["id"] for x in public["annotations"]], [1])
            self.assertEqual([x["id"] for x in public["categories"]], [1])
            self.assertEqual(stats(public), [1, 1, 2, 1, 1, 1])
            self.assertEqual(json.dumps(data), before)
            self.assertEqual(list(public), list(data))
            self.assertEqual(public["custom"], data["custom"])
            self.assertEqual(
                unavailable(data, public),
                "<!--\nUnavailable categories:\n- "
                + chr(96)
                + "2"
                + chr(96)
                + " human\n-->",
            )

    def test_cache_reopens_changed_images_and_rechecks_missing_files(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "bad.jpg").write_text("not an image")
            images = [
                {"id": 1, "file_name": "bad.jpg"},
                {"id": 2, "file_name": "missing.jpg"},
            ]
            validator = ImageValidator(root / "cache.sqlite3", workers=2, processes=2)
            try:
                selected, counts = validator.select(images, root)
                self.assertEqual(selected, [])
                self.assertEqual((counts["invalid"], counts["missing"]), (1, 1))
                _, counts = validator.select(images, root)
                self.assertEqual(counts["cache_hits"], 1)
                Image.new("RGB", (4, 4)).save(root / "bad.jpg")
                Image.new("RGB", (4, 4)).save(root / "missing.jpg")
                selected, counts = validator.select(images, root)
                self.assertEqual(selected, images)
                self.assertEqual(counts["opened"], 2)
            finally:
                validator.close()
            validator = ImageValidator(root / "cache.sqlite3", workers=2, processes=2)
            try:
                selected, counts = validator.select(images, root)
                self.assertEqual(selected, images)
                self.assertEqual(counts["cache_hits"], 2)
            finally:
                validator.close()

    def test_renderer_uses_catalog_statistics_and_pending_datasets(self):
        catalog = {
            "datasets": [
                {
                    "name": "Seattle(ish) Camera Traps",
                    "url": "https://example.org/dataset",
                    "labelsets": [
                        {
                            "name": "Metadata",
                            "source": "https://example.org/metadata",
                            "slug": "seattleish--metadata",
                        }
                    ],
                }
            ],
            "pending_datasets": [
                {
                    "name": "Pending",
                    "url": "https://example.org/pending",
                    "reason": "Not mirrored.",
                }
            ],
        }
        results = {
            "seattleish--metadata": {
                "original": [10, 3, 8, 0, 2, 4],
                "public": [9, 2, 7, 0, 2, 4],
                "referenced": [9, 2, 6, 0, 2, 4],
                "unavailable_categories": [],
            }
        }
        rendered = render_readme(catalog, "# Introduction", results, "v3")
        self.assertTrue(rendered.startswith("# Introduction\n"))
        self.assertIn("(#seattleish-camera-traps)", rendered)
        self.assertIn("/v3/seattleish--metadata.public.json.zip", rendered)
        self.assertIn("|10|3|8|0|2|4|", rendered)
        self.assertIn("|9|2|6|0|2|4|", rendered)
        self.assertIn("[Pending](https://example.org/pending): Not mirrored.", rendered)

    def test_zip_preserves_json_data_and_serialization(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "test.public.json.zip"
            data = {"z": [{"name": "Orinoquía", "id": "001"}], "a": 0.25}
            write(data, path)
            self.assertEqual(load(path), data)
            self.assertEqual(
                payload_hash(path),
                hashlib.sha256(json.dumps(data, indent=2).encode()).hexdigest(),
            )

    def test_paths_cannot_escape_mirror(self):
        for relative in ["../private.jpg", "/private.jpg", "nested/../../private.jpg"]:
            with self.assertRaises(ValueError):
                local_path(Path("/mirror"), relative)


if __name__ == "__main__":
    unittest.main()
