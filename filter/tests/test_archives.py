import json
import tempfile
import unittest
import zipfile
from pathlib import Path

from filter.archives import prepare_archive, safe_path
from filter.cli import filter_images, stats


class ArchiveTests(unittest.TestCase):
    def test_selective_extraction_and_existing_file_protection(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source.zip"
            metadata = {
                "images": [
                    {"id": 1, "file_name": "keep.jpg"},
                    {"id": 2, "file_name": "missing.jpg"},
                ]
            }
            with zipfile.ZipFile(source, "w") as archive:
                archive.writestr("dataset/metadata.json", json.dumps(metadata))
                archive.writestr("dataset/images/keep.jpg", b"image bytes")
                archive.writestr("dataset/images/unreferenced.jpg", b"not requested")
                archive.writestr("dataset/video.bag", b"not requested")
            dataset = {
                "name": "Example",
                "archive_prefix": "dataset/",
                "image_base": "images",
            }
            labels = [{"source_member": "metadata.json"}]
            output = root / "output"
            prepare_archive(source, output, dataset, labels)
            self.assertEqual((output / "images/keep.jpg").read_bytes(), b"image bytes")
            self.assertFalse((output / "images/unreferenced.jpg").exists())
            self.assertFalse((output / "video.bag").exists())
            prepare_archive(source, output, dataset, labels)
            (output / "images/keep.jpg").write_bytes(b"user change")
            with self.assertRaises(FileExistsError):
                prepare_archive(source, output, dataset, labels)
            self.assertEqual((output / "images/keep.jpg").read_bytes(), b"user change")

    def test_zip_extra_fields_are_safe_with_concurrent_extraction(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source.zip"
            images = [{"id": i, "file_name": f"{i}.jpg"} for i in range(64)]
            with zipfile.ZipFile(source, "w") as archive:
                archive.writestr(
                    "dataset/metadata.json", json.dumps({"images": images})
                )
                for image in images:
                    info = zipfile.ZipInfo("dataset/images/" + image["file_name"])
                    info.extra = bytes.fromhex("555405000300000000")
                    archive.writestr(info, str(image["id"]).encode() * 1000)
            output = root / "output"
            prepare_archive(
                source,
                output,
                {
                    "name": "Extra fields",
                    "archive_prefix": "dataset/",
                    "image_base": "images",
                },
                [{"source_member": "metadata.json"}],
            )
            for image in images:
                self.assertEqual(
                    (output / "images" / image["file_name"]).read_bytes(),
                    str(image["id"]).encode() * 1000,
                )

    def test_paths_reject_traversal_and_symlink_escape(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "output"
            root.mkdir()
            (root / "link").symlink_to(root.parent, target_is_directory=True)
            for name in [
                "../outside",
                "/outside",
                "a/../../outside",
                "a\\outside",
                "link/outside",
            ]:
                with self.assertRaises(ValueError):
                    safe_path(root, name)

    def test_unlabeled_split_preserves_schema_and_has_no_referenced_images(self):
        data = {
            "images": [{"id": 1, "file_name": "a.jpg", "location": 2, "seq_id": "s"}]
        }
        public, referenced = filter_images(data, data["images"])
        self.assertEqual(public, data)
        self.assertEqual(referenced, {"images": []})
        self.assertEqual(stats(public), [0, 0, 1, 0, 1, 1])
        self.assertEqual(stats(referenced), [0, 0, 0, 0, 0, 0])


if __name__ == "__main__":
    unittest.main()
