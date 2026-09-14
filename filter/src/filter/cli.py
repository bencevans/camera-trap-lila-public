"""Regenerate public LILA metadata and its complete README from a pinned catalog."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sqlite3
import time
import zipfile
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from multiprocessing import get_context
from pathlib import Path, PurePosixPath

from PIL import Image, UnidentifiedImageError

PACKAGE = Path(__file__).parent
AZURE = "https://lilawildlife.blob.core.windows.net/lila-wildlife/"
RELEASE = "https://github.com/bencevans/camera-trap-lila-public/releases/download/"
HEADER = (
    "||Annotations|Categories|Images|BBoxes|Location IDs|Sequence IDs|\n|-|-|-|-|-|-|-|"
)


def local_path(root, relative):
    parts = PurePosixPath(relative)
    # Blob names are POSIX-relative. Some withheld Idaho records contain
    # literal backslashes; preserve those names instead of rewriting them.
    if parts.is_absolute() or ".." in parts.parts:
        raise ValueError(f"unsafe relative path: {relative!r}")
    return root.joinpath(*parts.parts)


def local_source(root, url):
    if not url.startswith(AZURE):
        raise ValueError(f"not a LILA Azure URL: {url}")
    return local_path(root, url.removeprefix(AZURE))


def load(path):
    if path.suffix == ".zip":
        with zipfile.ZipFile(path) as archive:
            names = [n for n in archive.namelist() if n.lower().endswith(".json")]
            if len(names) != 1:
                raise ValueError(f"expected one JSON member in {path}: {names}")
            with archive.open(names[0]) as source:
                return json.load(source)
    with path.open(encoding="utf-8-sig") as source:
        return json.load(source)


def readable(path, verify=True):
    try:
        # NFS may advertise a 1 MiB block size, which Python otherwise uses
        # as its read buffer even when Pillow needs only a small JPEG header.
        with path.open("rb", buffering=8192) as source, Image.open(source) as image:
            if verify:
                image.verify()
        return True
    except FileNotFoundError:
        return False
    except (
        UnidentifiedImageError,
        ValueError,
        SyntaxError,
        Image.DecompressionBombError,
    ):
        return False
    except OSError as error:
        # Do not turn permission failures or transient filesystem failures into
        # silently withheld images. Pillow decoder errors have no OS errno.
        if error.errno is not None:
            raise
        return False


_WORKER_THREADS = None


def _init_worker(threads):
    global _WORKER_THREADS
    _WORKER_THREADS = ThreadPoolExecutor(max_workers=threads)


def _check_file(task):
    root, name, cached = task
    path = local_path(Path(root), name)
    try:
        st = path.stat()
    except FileNotFoundError:
        return None, "missing", False
    signature = (st.st_size, st.st_mtime_ns)
    if cached is not None and tuple(cached[:2]) == signature:
        return None, "valid" if cached[2] else "invalid", True
    valid = readable(path)
    return (root, name, *signature, int(valid)), "valid" if valid else "invalid", False


def _check_batch(tasks):
    return list(_WORKER_THREADS.map(_check_file, tasks))


class ImageValidator:
    """Cache Pillow results against absolute root, filename, size and mtime.

    A file is stat'ed on every use. Changed files are reopened. Missing files are
    never negatively cached. Delete the cache to force an independent rescan.
    """

    def __init__(self, cache_path, workers, processes=8):
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        self.db = sqlite3.connect(cache_path)
        # Keep B-tree pages in memory instead of issuing random NFS reads for
        # every insertion once a multi-million-image cache outgrows 2 MiB.
        self.db.execute("PRAGMA cache_size=-524288")
        self.db.execute(
            "CREATE TABLE IF NOT EXISTS validity "
            "(root TEXT, name TEXT, size INTEGER, mtime INTEGER, valid INTEGER, "
            "PRIMARY KEY (root, name))"
        )
        self.pool = ProcessPoolExecutor(
            max_workers=processes,
            mp_context=get_context("spawn"),
            initializer=_init_worker,
            initargs=(max(1, workers // processes),),
        )
        self.root = None
        self.cached = {}

    def select(self, images, root):
        root = root.resolve()
        if root != self.root:
            self.root = root
            self.cached = {
                name: (size, mtime, valid)
                for name, size, mtime, valid in self.db.execute(
                    "SELECT name,size,mtime,valid FROM validity WHERE root=?",
                    (str(root),),
                )
            }
        if not root.is_dir():
            raise FileNotFoundError(f"image root is missing: {root}")
        counts = {"valid": 0, "missing": 0, "invalid": 0, "opened": 0, "cache_hits": 0}
        kept = []
        last_progress = time.monotonic()

        # Bound submitted work and commit in chunks, so interrupted scans resume.
        for start in range(0, len(images), 8192):
            chunk = images[start : start + 8192]
            tasks = [
                (str(root), im["file_name"], self.cached.get(im["file_name"]))
                for im in chunk
            ]
            batches = [tasks[i : i + 256] for i in range(0, len(tasks), 256)]
            outcomes = [
                outcome
                for batch in self.pool.map(_check_batch, batches)
                for outcome in batch
            ]
            records = []
            for image, (record, status, hit) in zip(chunk, outcomes):
                counts[status] += 1
                counts["cache_hits"] += int(hit)
                counts["opened"] += int(record is not None)
                if status == "valid":
                    kept.append(image)
                if record:
                    records.append(record)
                    self.cached[record[1]] = record[2:]
            self.db.executemany(
                "INSERT OR REPLACE INTO validity VALUES (?,?,?,?,?)", records
            )
            self.db.commit()
            if time.monotonic() - last_progress >= 25:
                print(
                    f"  checked {min(start + 8192, len(images)):,}/{len(images):,} images",
                    flush=True,
                )
                last_progress = time.monotonic()
        return kept, counts

    def close(self):
        self.pool.shutdown()
        self.db.close()


def filter_images(data, images):
    ids = {image["id"] for image in images}
    annotations = [a for a in data.get("annotations", []) if a["image_id"] in ids]
    category_ids = {a["category_id"] for a in annotations}
    categories = [c for c in data.get("categories", []) if c["id"] in category_ids]
    replacements = {
        "images": images,
        "annotations": annotations,
        "categories": categories,
    }
    public = {key: replacements.get(key, value) for key, value in data.items()}
    referenced_ids = {a["image_id"] for a in annotations}
    referenced = dict(public)
    referenced["images"] = [image for image in images if image["id"] in referenced_ids]
    return public, referenced


def filtered(data, image_root, verify=True):
    """Small-data helper; the command uses the bounded concurrent validator."""
    images = [
        image
        for image in data["images"]
        if readable(local_path(image_root, image["file_name"]), verify)
    ]
    return filter_images(data, images)


def stats(data):
    images, annotations = data["images"], data.get("annotations", [])
    return [
        len(annotations),
        len(data.get("categories", [])),
        len(images),
        sum("bbox" in a for a in annotations),
        len({i["location"] for i in images if i.get("location") is not None}),
        len({i["seq_id"] for i in images if i.get("seq_id") is not None}),
    ]


def missing_categories(original, public):
    used = {c["id"] for c in public.get("categories", [])}
    return [c for c in original.get("categories", []) if c["id"] not in used]


def unavailable(original, public):
    return category_note(missing_categories(original, public))


def category_note(missing):
    if not missing:
        return ""
    if len(missing) < 5:
        body = "\n".join(f"- `{c['id']}` {c['name']}" for c in missing)
    else:
        cells = [f"{c['name']} `{c['id']}`" for c in missing]
        grid = ["|  |  |  |  |  |", "|--|--|--|--|--|"]
        # Reproduce the original five-column / four-item stride, including its
        # duplicated boundary categories. This is intentional v2 compatibility.
        for start in range(0, len(cells) + 1, 4):
            grid.append(
                "| " + " | ".join((cells[start : start + 5] + ["  "] * 5)[:5]) + " |"
            )
        body = "\n".join(grid)
    return "<!--\nUnavailable categories:\n" + body + "\n-->"


def heading_anchor(name):
    return re.sub(r"[^\w\- ]", "", name.lower()).replace(" ", "-")


def render_readme(catalog, introduction, results, release):
    sections = [
        introduction.rstrip(),
        f"Machine-readable [dataset manifest]({RELEASE}{release}/manifest.json) · [Regeneration instructions](filter/README.md)",
        "## Datasets",
        "Jump To Dataset:",
    ]
    sections.append(
        "\n".join(
            f"- [{d['name']}](#{heading_anchor(d['name'])})"
            for d in catalog["datasets"]
        )
    )
    for dataset in catalog["datasets"]:
        sections += [
            f"### {dataset['name']}",
            f"See details on [lila.science]({dataset['url']})",
        ]
        for label in dataset["labelsets"]:
            result = results[label["slug"]]
            sections.append(f"#### {label['name']}")
            if label.get("note"):
                sections.append(label["note"])
            public = result["public"]
            referenced = list(result["referenced"])
            # v2 counts location/sequence IDs before the referenced-image pass.
            if not label.get("unlabeled"):
                referenced[4:] = public[4:]
            urls = [
                label["source"],
                f"{RELEASE}{release}/{label['slug']}.public.json.zip",
                f"{RELEASE}{release}/{label['slug']}.public.referenced.json.zip",
            ]
            names = ["Original", "Filtered (Public)", "Filtered (Public + Referenced)"]
            rows = [HEADER]
            for name, url, values in zip(
                names, urls, [result["original"], public, referenced]
            ):
                rows.append(
                    f"|[**{name}**]({url})|" + "|".join(f"{n:,}" for n in values) + "|"
                )
            sections.append("\n".join(rows))
            note = category_note(result["unavailable_categories"])
            if note:
                sections.append(note)
    if catalog.get("pending_datasets"):
        sections += [
            "## Datasets not yet exported",
            "These datasets are listed by LILA but are not included in these exports:",
        ]
        sections.append(
            "\n".join(
                f"- [{d['name']}]({d['url']}): {d['reason']}"
                for d in catalog["pending_datasets"]
            )
        )
    return "\n\n".join(sections) + "\n\n"


def write(data, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    info = zipfile.ZipInfo(path.name.removesuffix(".zip"), (1980, 1, 1, 0, 0, 0))
    info.compress_type = zipfile.ZIP_DEFLATED
    info.external_attr = 0o100644 << 16
    with zipfile.ZipFile(temporary, "w") as archive:
        archive.writestr(
            info, json.dumps(data, indent=2).encode("utf-8"), compresslevel=6
        )
    temporary.replace(path)


def payload_hash(path):
    with zipfile.ZipFile(path) as archive:
        names = archive.namelist()
        if len(names) != 1 or names[0] != path.name.removesuffix(".zip"):
            raise ValueError(f"unexpected archive members: {path}: {names}")
        digest = hashlib.sha256()
        with archive.open(names[0]) as source:
            while block := source.read(8 * 1024 * 1024):
                digest.update(block)
        return digest.hexdigest()


def save_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def write_documents(args, catalog, introduction, results, release):
    from .manifest import build_manifest

    manifest = build_manifest(
        catalog,
        results,
        release,
        args.output_dir,
        args.lila_root,
        getattr(args, "data_root", Path("data")),
    )
    rendered = render_readme(catalog, introduction, results, release).encode("utf-8")
    save_json(args.output_dir / "manifest.json", manifest)
    (args.output_dir / "README.md").write_bytes(rendered)
    args.readme.write_bytes(rendered)


def run(args):
    catalog = load(args.catalog)
    introduction = args.introduction.read_text(encoding="utf-8")
    labels = [(d, label) for d in catalog["datasets"] for label in d["labelsets"]]
    slugs = [label["slug"] for _, label in labels]
    if len(slugs) != len(set(slugs)):
        raise ValueError("catalog contains duplicate output slugs")
    release = args.release or catalog["release"]
    if getattr(args, "documents_only", False):
        results = load(args.output_dir / "summary.json")["labelsets"]
        write_documents(args, catalog, introduction, results, release)
        print(
            "Done: complete README and manifest generated from existing results.",
            flush=True,
        )
        return
    selected = set(getattr(args, "dataset", None) or [])
    unknown = selected - {d["name"] for d in catalog["datasets"]}
    if unknown:
        raise ValueError(f"unknown datasets: {sorted(unknown)}")
    active = [
        (d, label) for d, label in labels if not selected or d["name"] in selected
    ]
    results = {}
    if selected:
        previous = load(args.output_dir / "summary.json")["labelsets"]
        for dataset, label in labels:
            if dataset["name"] in selected:
                continue
            result = previous[label["slug"]]
            for suffix in ["public", "public.referenced"]:
                filename = f"{label['slug']}.{suffix}.json.zip"
                if (
                    filename not in result["exports"]
                    or not (args.output_dir / filename).is_file()
                ):
                    raise FileNotFoundError(f"Cannot reuse missing export: {filename}")
            results[label["slug"]] = result
    data_root = getattr(args, "data_root", Path("data"))
    paths = {}
    for dataset in catalog["datasets"]:
        selected_labels = [label for d, label in active if d is dataset]
        if not selected_labels:
            continue
        if dataset.get("archive"):
            from .archives import prepare_archive, safe_path

            root = safe_path(data_root, dataset["local_directory"])
            if not getattr(args, "skip_extraction", False):
                prepare_archive(
                    local_source(args.lila_root, dataset["archive"]),
                    root,
                    dataset,
                    selected_labels,
                )
        else:
            root = args.lila_root
        for label in selected_labels:
            source = (
                local_path(root, label["source_member"])
                if dataset.get("archive")
                else local_source(args.lila_root, label["source"])
            )
            image_root = local_path(
                root, label.get("image_base", dataset["image_base"])
            )
            if not source.is_file():
                raise FileNotFoundError(source)
            if not image_root.is_dir():
                raise FileNotFoundError(image_root)
            paths[label["slug"]] = (source, image_root)
    report = {
        "validation": "Pillow.Image.open + verify; cache keyed by size and mtime",
        "labelsets": results,
    }
    validator = ImageValidator(args.cache, args.workers, args.processes)
    try:
        for index, (dataset, label) in enumerate(active, 1):
            print(
                f"[{index}/{len(active)}] {dataset['name']} / {label['name']}",
                flush=True,
            )
            source, image_root = paths[label["slug"]]
            original = load(source)
            if (
                not label.get("unlabeled")
                and not {"images", "annotations", "categories"} <= original.keys()
            ):
                raise ValueError(f"incomplete labeled metadata: {source}")
            images, counts = validator.select(original["images"], image_root)
            public, referenced = filter_images(original, images)
            result = {
                "original": stats(original),
                "public": stats(public),
                "referenced": stats(referenced),
                "unavailable_categories": missing_categories(original, public),
                "image_validation": counts,
                "exports": {},
            }
            for suffix, data in [("public", public), ("public.referenced", referenced)]:
                path = args.output_dir / f"{label['slug']}.{suffix}.json.zip"
                write(data, path)
                digest = payload_hash(path)
                export = {"json_sha256": digest}
                result["exports"][path.name] = export
            results[label["slug"]] = result
            save_json(args.output_dir / "summary.json", report)
            print(f"  {counts}; exports written", flush=True)
            del original, images, public, referenced, data
    finally:
        validator.close()
    write_documents(args, catalog, introduction, results, release)
    save_json(args.output_dir / "summary.json", report)
    print(f"Done: {len(labels) * 2} exports; complete README generated.", flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog", type=Path, default=PACKAGE / "catalog.json")
    parser.add_argument(
        "--introduction", type=Path, default=PACKAGE / "introduction.md"
    )
    parser.add_argument(
        "--lila-root", type=Path, default=Path("/data/lila/azure/lila-wildlife")
    )
    parser.add_argument("--output-dir", type=Path, default=Path("dist"))
    parser.add_argument(
        "--cache", type=Path, default=Path("dist/image-validity.sqlite3")
    )
    parser.add_argument("--workers", type=int, default=128)
    parser.add_argument("--processes", type=int, default=8)
    parser.add_argument("--readme", type=Path, default=Path("README.md"))
    parser.add_argument("--release")
    parser.add_argument("--data-root", type=Path, default=Path("data"))
    parser.add_argument(
        "--dataset",
        action="append",
        help="Regenerate only this dataset name; reuse other exports and summary statistics. Repeatable.",
    )
    parser.add_argument(
        "--documents-only",
        action="store_true",
        help="Regenerate README and manifest from the existing summary and packages without scanning images.",
    )
    parser.add_argument(
        "--skip-extraction",
        action="store_true",
        help="Use previously unpacked archive metadata/images under --data-root; still validate images.",
    )
    args = parser.parse_args()
    if args.documents_only and args.dataset:
        parser.error("--documents-only cannot be combined with --dataset")
    if args.workers < 1 or args.processes < 1:
        parser.error("--workers and --processes must be positive")
    run(args)


if __name__ == "__main__":
    main()
