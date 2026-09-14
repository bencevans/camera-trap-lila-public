import tempfile
import unittest
from pathlib import Path

from filter.manifest import AZURE, DEFAULT_MIRRORS, build_manifest, source_locations


class ManifestTests(unittest.TestCase):
    def test_cloud_sources_for_loose_images(self):
        dataset = {"image_base": "sample/images"}
        label = {"source": AZURE + "sample/metadata.json.zip"}
        sources = source_locations(dataset, label, DEFAULT_MIRRORS)
        self.assertEqual(set(sources), {"azure", "s3", "gcs"})
        self.assertEqual(
            sources["s3"]["metadata"]["uri"],
            "s3://us-west-2.opendata.source.coop/agentmorris/lila-wildlife/sample/metadata.json.zip",
        )
        self.assertTrue(
            sources["s3"]["metadata"]["url"].startswith(
                "https://s3.us-west-2.amazonaws.com/"
            )
        )
        self.assertEqual(
            sources["gcs"]["images"]["base_uri"],
            "gs://public-datasets-lila/sample/images/",
        )
        self.assertEqual(sources["azure"]["images"]["storage"], "individual_objects")

    def test_archived_sources_identify_members_not_loose_blob_urls(self):
        url = AZURE + "sample/sample.zip"
        dataset = {"archive": url, "archive_prefix": "sample/", "image_base": "train"}
        label = {
            "source": url,
            "source_member": "metadata/test.json",
            "image_base": "test",
        }
        for source in source_locations(dataset, label, DEFAULT_MIRRORS).values():
            self.assertEqual(source["metadata"]["member"], "sample/metadata/test.json")
            self.assertEqual(source["images"]["member_prefix"], "sample/test/")
            self.assertEqual(source["images"]["storage"], "zip_members")
            self.assertNotIn("base_url", source["images"])

    def test_complete_manifest_has_packages_counts_and_pending_reason(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            label = {
                "name": "Training",
                "slug": "stable--train",
                "source": AZURE + "sample/metadata.json",
            }
            dataset = {
                "id": "stable",
                "name": "Display name",
                "url": "https://example.org",
                "image_base": "sample/images",
                "labelsets": [label],
            }
            result = {
                "original": [2, 1, 3, 0, 1, 1],
                "public": [1, 1, 2, 0, 1, 1],
                "referenced": [1, 1, 1, 0, 1, 1],
                "image_validation": {"valid": 2, "missing": 1},
                "unavailable_categories": [],
                "exports": {},
            }
            for suffix in ["public", "public.referenced"]:
                filename = f"stable--train.{suffix}.json.zip"
                (output / filename).write_bytes(b"test package")
                result["exports"][filename] = {"json_sha256": "a" * 64}
            catalog = {
                "datasets": [dataset],
                "pending_datasets": [
                    {
                        "id": "pending",
                        "name": "Video",
                        "url": "https://example.org/video",
                        "reason": "Video schema",
                    }
                ],
            }
            manifest = build_manifest(
                catalog,
                {label["slug"]: result},
                "v3",
                output,
                Path("/mirror"),
                Path("data"),
            )
            self.assertEqual(manifest["schema_version"], 1)
            self.assertEqual(
                manifest["counts"],
                {"datasets": 1, "labelsets": 1, "packages": 2, "pending_datasets": 1},
            )
            self.assertEqual(manifest["datasets"][0]["id"], "stable")
            generated = manifest["datasets"][0]["labelsets"][0]
            self.assertEqual(generated["statistics"]["referenced"]["images"], 1)
            package = generated["packages"]["referenced"]
            self.assertEqual(
                package["json_member"], "stable--train.public.referenced.json"
            )
            self.assertEqual(package["size_bytes"], 12)
            self.assertEqual(package["json_sha256"], "a" * 64)
            self.assertIn("/v3/", package["url"])
            self.assertEqual(manifest["pending_datasets"][0]["reason"], "Video schema")


if __name__ == "__main__":
    unittest.main()
