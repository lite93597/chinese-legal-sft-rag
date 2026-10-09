"""Export the final local SFT/RAG data without changing model-facing text."""
import argparse
import collections
import gzip
import hashlib
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROTECTED = {"messages", "content", "article_text", "answer", "question", "instruction", "source_input", "quote", "retrieval_content"}
PATH_KEYS = {"path", "file", "raw_path", "input_file", "source_raw_path", "source", "source_file", "source_path"}


def digest(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def clean(value, key=""):
    if key == "prior_exclusion_reason":
        return "历史排除说明含原个人信息，公开副本省略；训练与检索文本不变。"
    if key in PROTECTED:
        return value
    if isinstance(value, dict):
        return {k: clean(v, k) for k, v in value.items()}
    if isinstance(value, list):
        return [clean(v) for v in value]
    if isinstance(value, str) and key in PATH_KEYS and (re.match(r"^[A-Za-z]:[\\/]", value) or value.startswith(("/root/", "/home/"))):
        return value.replace("\\", "/").rsplit("/", 1)[-1]
    return value


def encode(row):
    return (json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n").encode("utf-8")


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8", newline="\n") as f:
        json.dump(value, f, ensure_ascii=False, indent=2)
        f.write("\n")


def shards(rows, prefix):
    """Bound binary blobs to 500 KiB for the connected GitHub upload API."""
    folder = ROOT / "data" / prefix
    folder.mkdir(parents=True, exist_ok=True)
    files, batch, size = [], [], 0
    stream_hash = hashlib.sha256()
    count = 0

    def emit(batch):
        compressed = gzip.compress(b"".join(batch), compresslevel=6, mtime=0)
        if len(compressed) > 500 * 1024 and len(batch) > 1:
            midpoint = len(batch) // 2
            emit(batch[:midpoint])
            emit(batch[midpoint:])
            return
        path = folder / f"part-{len(files):04d}.jsonl.gz"
        with path.open("xb") as f:
            f.write(compressed)
        files.append({"path": path.relative_to(ROOT).as_posix(), "rows": len(batch), "bytes": len(compressed), "sha256": digest(path)})

    for row in rows:
        raw = encode(row)
        stream_hash.update(raw)
        count += 1
        batch.append(raw)
        size += len(raw)
        if size >= 4 * 1024 * 1024:
            emit(batch)
            batch, size = [], 0
    if batch:
        emit(batch)
    return {"rows": count, "serialized_jsonl_sha256": stream_hash.hexdigest(), "files": files}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", type=Path, required=True)
    parser.add_argument("--upstream-notices", type=Path, required=True)
    args = parser.parse_args()
    if (ROOT / "manifest.json").exists():
        raise SystemExit("Release already exists; do not overwrite it.")
    sft = args.project / "data/sft-v4-reviewed-20261006"
    index = args.project / "outputs/index/v211-applicability"
    expected = {sft / "train.jsonl": "a79466d60df3ad0b7cc0ceb6111b61b8171bc303b182c13a9be161693386661d", sft / "validation.jsonl": "0e2fb1ba7091406a9eafb882c092daf004b1ed9b6056fdd86775f7456eb51b33", index / "metadata.json": "9891c6b33bd074ed4ac3505901ce31aeaa46aef2892d155fa5c4e48fb4b12a47", index / "law.index": "67c892792636e697ee5b2ce78d72321e639d3d78a9fc0090d57f5958ef405966"}
    for path, sha in expected.items():
        if digest(path) != sha:
            raise ValueError(f"Source has changed: {path.name}")
    manifest = {"release": "legal-v4-data-20261009", "format": "UTF-8 JSONL, gzip shards", "scope": "Final V4 SFT splits and all actual RAG chunks/parent units; not model weights or benchmark answer files", "datasets": {}, "source_files": [{"name": p.name, "bytes": p.stat().st_size, "sha256": sha} for p, sha in expected.items()], "transformations": ["Preserve every SFT row, split, order, message and context document text", "Preserve every RAG chunk, order, ID, content and article_text", "Replace absolute local paths in engineering metadata with source basenames", "Derive parent corpus by article_id from full article_text; no retraining, resplitting or re-embedding"], "limitations": "Mixed upstream rights; retained status labels are not permission grants. Limited pattern checks are not full anonymization or legal certification."}
    statistics = {"sft": {}, "rag": {}}
    for split, total in (("train", 15242), ("validation", 1923)):
        rows = [json.loads(line) for line in (sft / f"{split}.jsonl").open(encoding="utf-8")]
        assert len(rows) == total
        public = [clean(row) for row in rows]
        for original, exported in zip(rows, public):
            assert original["id"] == exported["id"]
            assert original.get("messages") == exported.get("messages")
            for key in ("answer", "question", "instruction", "source_input", "context_documents"):
                assert original.get(key) == exported.get(key)
        stats = {field: dict(collections.Counter(str(r.get(field, "not_recorded")) for r in rows)) for field in ("task_type", "domain", "redistribution_status", "research_use_status")}
        stats["rows"] = total
        statistics["sft"][split] = stats
        manifest["datasets"][f"sft/{split}"] = shards(public, f"sft/{split}")
        print(f"SFT {split}: {total} rows", flush=True)
    chunks = json.loads((index / "metadata.json").read_text(encoding="utf-8"))
    assert len(chunks) == 51017
    public_chunks = [clean(row) for row in chunks]
    parents = {}
    for original, exported in zip(chunks, public_chunks):
        assert original["content"] == exported["content"]
        assert original["metadata"]["article_text"] == exported["metadata"]["article_text"]
        key = exported["metadata"]["article_id"]
        if key in parents:
            assert parents[key]["content"] == exported["metadata"]["article_text"]
        else:
            metadata = {k: v for k, v in exported["metadata"].items() if k not in {"article_text", "part_index"}}
            parents[key] = {"id": key, "content": exported["metadata"]["article_text"], "metadata": metadata}
    assert len(parents) == 37748
    manifest["datasets"]["rag/chunks"] = shards(public_chunks, "rag/chunks")
    manifest["datasets"]["rag/corpus"] = shards(parents.values(), "rag/corpus")
    statistics["rag"] = {"chunks": len(chunks), "parent_units": len(parents), "chunk_layers": dict(collections.Counter(r["metadata"]["layer"] for r in chunks)), "parent_layers": dict(collections.Counter(r["metadata"]["layer"] for r in parents.values()))}
    print(f"RAG: {len(chunks)} chunks / {len(parents)} parent units", flush=True)
    write_json(ROOT / "statistics.json", statistics)
    write_json(ROOT / "manifest.json", manifest)
    # Preserve upstream conditions verbatim; copying these does not grant new rights.
    notices = ROOT / "licenses/upstream"
    notices.mkdir(parents=True, exist_ok=True)
    selected = {"lawyer-llama-README.md": "upstream_licenses/01_法律咨询_LawyerLLaMA/README.md", "lawyer-llama-LICENSE.txt": "upstream_licenses/01_法律咨询_LawyerLLaMA/LICENSE", "hanfei-README.md": "recovery_12_admission_v22/license_evidence/hanfei_README.md", "hanfei-LICENSE.txt": "recovery_12_admission_v22/license_evidence/hanfei_LICENSE", "fuzi-README.md": "recovery_12_admission_v22/license_evidence/fuzi_dataset_README.md"}
    for target, source in selected.items():
        destination = notices / target
        if destination.exists():
            raise FileExistsError(destination)
        shutil.copyfile(args.upstream_notices / source, destination)
    # Optional binary index: keep separate from ordinary text data in the repository.
    artifacts = ROOT / "artifacts"
    artifacts.mkdir(exist_ok=True)
    import zipfile
    with zipfile.ZipFile(artifacts / "legal-rag-faiss-v4.zip", "x", compression=zipfile.ZIP_DEFLATED, compresslevel=1) as archive:
        archive.write(index / "law.index", "law.index")
        archive.writestr("metadata.json", json.dumps(public_chunks, ensure_ascii=False, separators=(",", ":")))
        archive.writestr("index_info.json", json.dumps({"dimension": 1024, "vectors": 51017, "metric": "inner_product", "normalized": True, "embedding_model": "BAAI/bge-large-zh-v1.5", "max_embedding_length": 512, "source_index_sha256": expected[index / "law.index"], "metadata_scope": "Public path-sanitized copy; array order unchanged"}, ensure_ascii=False, indent=2))
    print("Release data and optional FAISS archive ready", flush=True)


if __name__ == "__main__":
    main()
