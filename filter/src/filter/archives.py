"""Extract only metadata and referenced still images from a combined archive."""

import json
import os
import tempfile
import threading
import time
import zipfile
import zlib
from concurrent.futures import ThreadPoolExecutor
from pathlib import PurePosixPath


def safe_path(root, name):
    relative = PurePosixPath(name)
    if relative.is_absolute() or ".." in relative.parts or "\\" in name:
        raise ValueError(f"unsafe archive path: {name!r}")
    path = root.joinpath(*relative.parts)
    if not path.resolve().is_relative_to(root.resolve()):
        raise ValueError(f"archive path escapes destination: {name!r}")
    return path


def prepare_archive(source, root, dataset, labels):
    prefix = dataset.get("archive_prefix", "")
    safe_path(root, prefix)
    root.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(source) as archive:
        names = archive.namelist()
        if len(names) != len(set(names)):
            raise ValueError(f"duplicate archive member names: {source}")
        available = set(names)
        wanted = set()
        for label in labels:
            member = label["source_member"]
            safe_path(root, member)
            data = json.loads(archive.read(prefix + member))
            wanted.add(member)
            for image in data["images"]:
                relative = str(
                    PurePosixPath(label.get("image_base", dataset["image_base"]))
                    / image["file_name"]
                )
                safe_path(root, image["file_name"])
                safe_path(root, relative)
                if prefix + relative in available:
                    wanted.add(relative)
        members = sorted(wanted)
        size = sum(archive.getinfo(prefix + name).file_size for name in members)
        print(
            f"Preparing {dataset['name']}: {len(members):,} files, {size / 1e9:.2f} GB in {root}",
            flush=True,
        )

        archive_read_lock = threading.Lock()

        def extract(name):
            info = archive.getinfo(prefix + name)
            if (info.external_attr >> 16) & 0o170000 == 0o120000:
                raise ValueError(f"symlink archive member: {info.filename}")
            path = safe_path(root, name)
            if path.exists():
                crc = 0
                with path.open("rb") as existing:
                    while block := existing.read(1024 * 1024):
                        crc = zlib.crc32(block, crc)
                if path.stat().st_size != info.file_size or crc != info.CRC:
                    raise FileExistsError(f"existing file differs from archive: {path}")
                return
            path.parent.mkdir(parents=True, exist_ok=True)
            temporary = None
            try:
                with tempfile.NamedTemporaryFile(
                    dir=path.parent, prefix=".extract-", delete=False
                ) as target:
                    temporary = target.name
                    # Python 3.12's shared ZIP reader can seek relative to another
                    # thread's position while skipping local-header extra fields.
                    # Serialize reads, retain ZIP overlap/CRC checks, and allow
                    # destination writes to proceed concurrently.
                    with archive_read_lock:
                        content = archive.read(info)
                    target.write(content)
                os.replace(temporary, path)
            finally:
                if temporary and os.path.exists(temporary):
                    os.unlink(temporary)

        last = time.monotonic()
        with ThreadPoolExecutor(max_workers=8) as pool:
            for start in range(0, len(members), 1024):
                list(pool.map(extract, members[start : start + 1024]))
                if time.monotonic() - last >= 25:
                    print(
                        f"  extracted/verified {min(start + 1024, len(members)):,}/{len(members):,} files",
                        flush=True,
                    )
                    last = time.monotonic()
        print("  extraction complete", flush=True)
