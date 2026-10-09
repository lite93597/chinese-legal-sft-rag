# Chinese Legal SFT + RAG Dataset

[中文说明](README.md) · [Data format](docs/DATA_FORMAT.md) · [Sources and rights](docs/SOURCES_AND_LICENSES.md)

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

## Reported development-mini results

Each condition covers1,351 questions /54 tasks across LawBench, DISC and LexEval. Task macro averages on a0–100 scale:

| Condition | LawBench | DISC | LexEval |
| --- | ---: | ---: | ---: |
| Base | 58.2262 | 68.8181 | 65.4444 |
| RAG | 58.0692 | **72.7925** | 64.6759 |
| SFT | 62.3346 | 65.9464 | **68.3203** |
| SFT+RAG | **63.2988** | 69.8364 | 67.7204 |

These are development subsets, not official full-benchmark or independent blind-test scores. No aggregate across benchmarks, statistical significance or legal correctness guarantee is claimed. LLM grading is not lawyer review. Corpus cutoff and supplemental dates are recorded separately; publication date is not a guarantee of current law.

If useful for your SFT/RAG or legal-agent research, please consider starring the repository. Report issues using example IDs or `article_id`, without disclosing private identity information.
