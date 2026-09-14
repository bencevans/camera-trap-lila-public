# LILA public metadata generator

Run from the repository root:

```console
uv run --project filter filter \
  --lila-root /data/lila/azure/lila-wildlife \
  --output-dir dist
```

The command regenerates all 108 exports across 34 datasets and the complete root
README from the pinned `src/filter/catalog.json` and `src/filter/introduction.md`. It does not
read the existing README for catalog entries or statistics. No downloads are
needed: metadata and images come from the supplied local mirror. Combined archives
are selectively unpacked into `data/<dataset>/` (override with `--data-root`).
Only the configured metadata and its referenced images are extracted; video,
depth and unrelated supplementary files stay in the source ZIPs. Existing files
are CRC-checked and reused; conflicting files are not overwritten. Extraction
uses temporary files and atomic renames, so it can safely be rerun. Use
`--skip-extraction` when these files have already been unpacked (manually or by
a prior run); images are still checked with Pillow, but archive CRC comparison
is skipped. Missing extracted images are then filtered like missing mirror files.

The mirror is assumed to contain the publicly released imagery; an incomplete mirror will
exclude additional images. Missing local files are not probed on the network.

Each image must open and verify with Pillow. Image, annotation, category and
object order are preserved. Annotations are retained only when their image is
retained; unused categories are removed. The referenced variant also removes
images with no retained annotation. IDs, filenames and all other fields remain
unchanged.

Each labelset is loaded into memory; the combined Serengeti export needs tens of
gigabytes of RAM during JSON serialization. Use a machine with sufficient memory
for the full catalog.

Eight processes share 128 image-reading threads by default. Use `--processes`
and `--workers` to tune concurrency. Image reads use an explicit 8 KiB buffer
to avoid Python's much larger default read buffer on NFS. Pillow 10.2.0 is
pinned for consistent image validation.
`dist/image-validity.sqlite3` caches Pillow results by absolute image root,
filename, size and nanosecond modification time.
Files are checked for changes on each run; missing images are always retried.
Use a fresh `--cache` path for a completely independent scan. Interrupted scans
retain committed validation results; rerun the same command to use them.

`dist/summary.json` records statistics, image validation counts and SHA-256
hashes of the extracted JSON. Each completed labelset checkpoints its summary.
The command rewrites the root README and also saves `dist/README.md` once all
exports finish. There are no comparisons against previous releases or READMEs.

Two historical README quirks are deliberately preserved for existing output
consistency:
category grids repeat each fifth category at the next row's start, and the
referenced table rows reuse public location/sequence counts. The report contains
the actual referenced counts. These quirks affect documentation only.

To add datasets, edit `src/filter/catalog.json`: add a dataset name, LILA page
URL, stable `id`, relative image directory, and one or more labelsets with source
URL and output slug. Keep IDs stable when changing display names. The image paths were pinned from the
[LILA CSV manifest](https://lila.science/wp-content/uploads/2023/06/lila_camera_trap_datasets.csv)
supplied during reconstruction and the
[camera-trap dataset index](https://lila.science/category/camera-traps/). Explicit
configuration avoids silent changes when the upstream manifest gains datasets
or changes names. Set `--release v3` (or another tag) to generate new download
links. Adding datasets does not require modifying Python code.

The catalog now targets `v3`; generating links does not create a GitHub release.
Duck Pictures in Wetlands, iWildCam 2022 and Lindenthal are included. iWildCam
has separate training and test labelsets; its test metadata has no released
annotations or categories. We preserve that images-only schema, and its referenced
export therefore contains zero images. Lindenthal's train/test exports preserve
bounding boxes, segmentation polygons and tracking attributes without conversion.
NZ Thermal is the only pending dataset: its video/track schema is outside this
still-image workflow.

To regenerate only selected datasets and reuse the other existing exports and
`summary.json` statistics:

```console
uv run --project filter filter \
  --dataset 'Duck Pictures in Wetlands' \
  --dataset 'iWildCam 2022' \
  --dataset 'Lindenthal Camera Traps'
```

Dataset names must match the catalog exactly. This requires a previous output
summary and both exports for every unselected labelset. Unselected datasets are
**not rescanned**, even if their source metadata or imagery changed during a
mirror update. Omit `--dataset` to refresh the entire catalog. The complete README and `dist/manifest.json`
are generated in either case. Archive-backed entries specify `archive`,
`archive_prefix`, `local_directory`, and each labelset's `source_member` and
optional image-root override `image_base`. Their Original links point to the
combined ZIP, with the metadata member documented below the labelset heading.

Tests:

```console
uv run --project filter python -m unittest discover -s filter/tests -v
```

## Machine-readable manifest

`dist/manifest.json` (schema version 1) contains stable dataset IDs, labelset IDs,
LILA homepages, license/citation reference pages, named statistics, image-validation
counts, unavailable categories, and both filtered packages for each labelset.
Each package has its release download URL, filename, output-relative path, ZIP
size, JSON member name and SHA-256 of the uncompressed JSON.

Each labelset's `sources` contains `azure`, `s3` and `gcs` entries. These provide
HTTP download URLs and Azure/S3/Google storage URIs for metadata and imagery.
For combined archives, `metadata.member` and `images.member_prefix` identify ZIP
members; these are not individually hosted blob URLs. `local_inputs` identifies
paths relative to one of the manifest's `local_roots`. Pending datasets are
listed separately with reasons and known original sources. Licenses must still be checked on the linked
LILA pages; the manifest does not grant a common license to all datasets.

The manifest is derived from the pinned catalog and the completed export summary;
cloud mirror URLs are not probed during generation. The S3 HTTPS endpoint uses
path-style addressing to avoid the dotted bucket name's TLS hostname mismatch.
Release URLs are intended publication locations, not confirmation of publication.

To rebuild documentation and the manifest without scanning or rewriting packages:

```console
uv run --project filter filter --documents-only
```

This requires completed summary entries and packages for the entire current
catalog. As with `--dataset`, existing statistics/checksums are reused; it does
not validate changed input data or externally modified packages.
