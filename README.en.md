# Chinese Legal SFT + RAG Dataset

[中文说明](README.md) · [Data layer](data/README.md) · [Model experiments](experiments/README.md) · [Data format](docs/DATA_FORMAT.md) · [Sources and rights](docs/SOURCES_AND_LICENSES.md)

The final legal-v4 research data: **15,242 training examples, 1,923 validation examples, 37,748 RAG parent units and 51,017 retrieval chunks**. Includes legal QA, extraction, summaries, evidence analysis and multi-turn conversations, plus105 complete-case examples from35 related scenario families.

This is a mixed-source research release, **not a blanket MIT/Apache or commercially cleared dataset**. Academic/non-commercial upstream conditions and per-record unresolved redistribution statuses are retained. Public availability does not grant rights the publisher does not hold. Check upstream conditions before use, including downstream redistribution. Code and data have separate terms.

```bash
git clone https://github.com/lite93597/chinese-legal-sft-rag.git
cd chinese-legal-sft-rag
python scripts/verify.py
```

```python
from scripts.load_data import iter_records, training_messages
row = next(iter_records("sft/train"))
messages = training_messages(row)
chunk = next(iter_records("rag/chunks"))
```

Read compressed JSONL with the Python standard library. `training_messages()` also handles the105 structured-only case examples; they must not be silently dropped. Original splits, order, IDs, messages and retrieved text are preserved. Absolute local paths in engineering metadata are reduced to source basenames; historical exclusion reasons that may retain personal identifiers are omitted. Optional FAISS archive parts can be restored with `python scripts/restore_index.py --output ./local-index`.

## Separate data and model-experiment layers

The [data layer](data/README.md) contains the datasets, index, formats and loading examples. The [experiment layer](experiments/README.md) separately documents the actual V4 SFT training, RAG pipeline, evaluation protocol and results. Dataset paths, splits and contents remain unchanged.

Recorded configurations, a training summary, benchmark results and 216 per-task scores are included. Full training/inference/grading source code and model weights are not yet published here; future additions belong in the experiment layer, not the dataset directories.

See [evaluation and results](experiments/evaluation/README.md). These are development-mini subsets, not official full-benchmark or independent blind-test scores. No aggregate across benchmarks, statistical significance or legal correctness guarantee is claimed. LLM grading is not lawyer review. Corpus cutoff and supplemental dates are recorded separately; publication date is not a guarantee of current law.

If useful for your SFT/RAG or legal-agent research, please consider starring the repository. Report issues using example IDs or `article_id`, without disclosing private identity information.
