"""Verify downloaded data shards with Python's standard library."""
import gzip
import hashlib
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
for name, dataset in manifest["datasets"].items():
    count, stream = 0, hashlib.sha256()
    for item in dataset["files"]:
        path = root / item["path"]
        raw = path.read_bytes()
        assert len(raw) == item["bytes"], path
        assert hashlib.sha256(raw).hexdigest() == item["sha256"], path
        decoded = gzip.decompress(raw)
        stream.update(decoded)
        records = decoded.splitlines()
        assert len(records) == item["rows"], path
        for line in records:
            json.loads(line)
        count += len(records)
    assert count == dataset["rows"], name
    assert stream.hexdigest() == dataset["serialized_jsonl_sha256"], name
    print(f"OK {name}: {count:,} records")
