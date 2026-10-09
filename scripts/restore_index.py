"""Restore the optional FAISS archive, checking parts and exact members."""
import argparse
import hashlib
import json
import shutil
import zipfile
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--output", type=Path, default=Path("local-index"))
args = parser.parse_args()
root = Path(__file__).resolve().parents[1]
manifest = json.loads((root / "data/rag/faiss/manifest.json").read_text(encoding="utf-8"))
if args.output.exists():
    raise SystemExit("Output path exists; use a new folder. Nothing will be overwritten.")
args.output.mkdir(parents=True)
archive = args.output / manifest["archive_name"]
whole, total = hashlib.sha256(), 0
with archive.open("xb") as out:
    for item in manifest["parts"]:
        raw = (root / item["path"]).read_bytes()
        assert len(raw) == item["bytes"]
        assert hashlib.sha256(raw).hexdigest() == item["sha256"]
        whole.update(raw)
        total += len(raw)
        out.write(raw)
assert total == manifest["archive_bytes"]
assert whole.hexdigest() == manifest["archive_sha256"]
with zipfile.ZipFile(archive) as z:
    assert len(z.namelist()) == len(set(z.namelist()))
    assert set(z.namelist()) == {"law.index", "metadata.json", "index_info.json"}
    assert set(z.namelist()) == set(manifest["members"])
    for name, item in manifest["members"].items():
        h, size = hashlib.sha256(), 0
        with z.open(name) as source, (args.output / name).open("xb") as target:
            for block in iter(lambda: source.read(1024 * 1024), b""):
                h.update(block)
                size += len(block)
                target.write(block)
        assert size == item["bytes"] and h.hexdigest() == item["sha256"]
print(f"Verified FAISS index and metadata: {args.output.resolve()}")
