"""Portable catalog of original cloud sources and generated metadata packages."""

from pathlib import Path
from urllib.parse import quote

AZURE = "https://lilawildlife.blob.core.windows.net/lila-wildlife/"
RELEASE = "https://github.com/bencevans/camera-trap-lila-public/releases/download/"
COUNT_FIELDS = (
    "annotations",
    "categories",
    "images",
    "bounding_boxes",
    "locations",
    "sequences",
)
DEFAULT_MIRRORS = {
    "azure": {"url_base": AZURE, "uri_base": AZURE},
    "s3": {
        "url_base": "https://s3.us-west-2.amazonaws.com/us-west-2.opendata.source.coop/agentmorris/lila-wildlife/",
        "uri_base": "s3://us-west-2.opendata.source.coop/agentmorris/lila-wildlife/",
    },
    "gcs": {
        "url_base": "https://storage.googleapis.com/public-datasets-lila/",
        "uri_base": "gs://public-datasets-lila/",
    },
}


def counts(values):
    if len(values) != len(COUNT_FIELDS):
        raise ValueError("unexpected statistics shape")
    return dict(zip(COUNT_FIELDS, values))


def source_locations(dataset, label, mirrors):
    url = label["source"]
    if not url.startswith(AZURE):
        raise ValueError(f"unsupported source URL: {url}")
    relative = url.removeprefix(AZURE)
    image_base = label.get("image_base", dataset["image_base"]).rstrip("/") + "/"
    sources = {}
    for provider, mirror in mirrors.items():
        metadata = {
            "url": mirror["url_base"] + quote(relative, safe="/"),
            "uri": mirror["uri_base"] + relative,
            "format": "zip" if relative.endswith(".zip") else "json",
        }
        if dataset.get("archive"):
            metadata["member"] = (
                dataset.get("archive_prefix", "") + label["source_member"]
            )
            images = {
                "storage": "zip_members",
                "archive_url": metadata["url"],
                "archive_uri": metadata["uri"],
                "member_prefix": dataset.get("archive_prefix", "") + image_base,
            }
        else:
            images = {
                "storage": "individual_objects",
                "base_url": mirror["url_base"] + quote(image_base, safe="/"),
                "base_uri": mirror["uri_base"] + image_base,
            }
        sources[provider] = {"metadata": metadata, "images": images}
    return sources


def build_manifest(catalog, results, release, output_dir, lila_root, data_root):
    mirrors = catalog.get("cloud_mirrors", DEFAULT_MIRRORS)
    manifest = {
        "schema_version": 1,
        "release": release,
        "dataset_index": catalog.get("dataset_index"),
        "source_catalog": catalog.get("manifest_source"),
        "local_roots": {
            "lila_root": str(lila_root),
            "data_root": str(data_root),
            "output_dir": str(output_dir),
        },
        "validation": "Local file exists and passes Pillow.Image.open + verify; cached by size and mtime.",
        "datasets": [],
        "pending_datasets": [],
    }
    identifiers = set()
    for dataset in catalog["datasets"]:
        identifier = dataset.get("id", dataset["labelsets"][0]["slug"].split("--")[0])
        if identifier in identifiers:
            raise ValueError(f"duplicate dataset ID: {identifier}")
        identifiers.add(identifier)
        entry = {
            "id": identifier,
            "name": dataset["name"],
            "homepage": dataset["url"],
            "status": "exported",
            "license_and_citation": {"see": dataset["url"]},
            "labelsets": [],
        }
        for label in dataset["labelsets"]:
            result = results[label["slug"]]
            label_entry = {
                "id": label["slug"],
                "name": label["name"],
                "unlabeled": label.get("unlabeled", False),
                "sources": source_locations(dataset, label, mirrors),
                "statistics": {
                    variant: counts(result[variant])
                    for variant in ("original", "public", "referenced")
                },
                "image_validation": result["image_validation"],
                "unavailable_categories": result["unavailable_categories"],
                "packages": {},
            }
            if label.get("note"):
                label_entry["note"] = label["note"]
            if dataset.get("archive"):
                prefix = dataset["local_directory"] + "/"
                local_inputs = {
                    "root": "data_root",
                    "metadata": prefix + label["source_member"],
                    "images": prefix + label.get("image_base", dataset["image_base"]),
                }
            else:
                local_inputs = {
                    "root": "lila_root",
                    "metadata": label["source"].removeprefix(AZURE),
                    "images": label.get("image_base", dataset["image_base"]),
                }
            label_entry["local_inputs"] = local_inputs
            for variant, suffix in [
                ("public", "public"),
                ("referenced", "public.referenced"),
            ]:
                filename = f"{label['slug']}.{suffix}.json.zip"
                export = result["exports"][filename]
                label_entry["packages"][variant] = {
                    "file_name": filename,
                    "path": filename,
                    "url": f"{RELEASE}{release}/{filename}",
                    "format": "zip",
                    "json_member": filename.removesuffix(".zip"),
                    "json_sha256": export["json_sha256"],
                    "size_bytes": (Path(output_dir) / filename).stat().st_size,
                }
            entry["labelsets"].append(label_entry)
        manifest["datasets"].append(entry)
    for dataset in catalog.get("pending_datasets", []):
        entry = {
            "id": dataset["id"],
            "name": dataset["name"],
            "homepage": dataset["url"],
            "status": "pending",
            "reason": dataset["reason"],
        }
        if dataset.get("source") and dataset.get("media_base"):
            entry["media_type"] = dataset["media_type"]
            sources = source_locations(
                {"image_base": dataset["media_base"]},
                {"source": dataset["source"]},
                mirrors,
            )
            entry["sources"] = {
                provider: {"metadata": source["metadata"], "media": source["images"]}
                for provider, source in sources.items()
            }
        manifest["pending_datasets"].append(entry)
    manifest["counts"] = {
        "datasets": len(manifest["datasets"]),
        "labelsets": sum(len(d["labelsets"]) for d in manifest["datasets"]),
        "packages": sum(
            len(l["packages"]) for d in manifest["datasets"] for l in d["labelsets"]
        ),
        "pending_datasets": len(manifest["pending_datasets"]),
    }
    return manifest
