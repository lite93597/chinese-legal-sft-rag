"""Mechanical packaging of the optional existing FAISS archive; no embedding."""
import hashlib
import json
import zipfile
from pathlib import Path

root = Path(__file__).resolve().parents[1]
source = root / "artifacts/legal-rag-faiss-v4.zip"
folder = root / "data/rag/faiss"
folder.mkdir(parents=True, exist_ok=True)
parts, whole = [], hashlib.sha256()
with source.open("rb") as f:
    while raw := f.read(5 * 1024 * 1024):
        path = folder / f"part-{len(parts):04d}.zip.part"
        with path.open("xb") as out:
            out.write(raw)
        whole.update(raw)
        parts.append({"path": path.relative_to(root).as_posix(), "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()})
with zipfile.ZipFile(source) as z:
    members = {name: {"bytes": z.getinfo(name).file_size, "sha256": hashlib.sha256(z.read(name)).hexdigest()} for name in z.namelist()}
with (folder / "manifest.json").open("x", encoding="utf-8") as f:
    json.dump({"archive_name": source.name, "archive_bytes": source.stat().st_size, "archive_sha256": whole.hexdigest(), "parts": parts, "members": members}, f, ensure_ascii=False, indent=2)
    f.write("\n")
print(f"FAISS archive: {len(parts)} parts / {source.stat().st_size} bytes")
