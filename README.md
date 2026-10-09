# Chinese Legal SFT + RAG Dataset｜中文法律微调与检索数据

[English](README.en.md) · [数据字段](docs/DATA_FORMAT.md) · [来源与许可](docs/SOURCES_AND_LICENSES.md) · [评测结果](docs/EVALUATION.md)

面向中文法律问答、案件分析、证据处理与多轮咨询的研究数据：**17,165条SFT样本 + 37,748条RAG资料记录 + 51,017个检索块**。

本仓库发布实际用于 legal-v4 实验的最终数据，不是只给几条示例的展示项目。保留训练/验证划分、来源链接、法条版本与逐条使用状态，提供开箱可读的压缩JSONL、字段说明与完整性校验。

> **使用前请读许可说明：**这是混合来源的公开研究数据，不是全包MIT/Apache或“可商用”数据集。部分上游仅限学术/非商业用途；训练集11,574条的 `redistribution_status` 仍为 `not_confirmed`，另外还有 `not_cleared`、未记录等状态。公开发布没有补齐这些授权，也不授予未持有的权利。请自行核查拟使用记录的上游条件；无法确认时可通过原链接获取或联系权利人。

## 为什么下载这个数据集？

- **SFT与RAG一起提供**：既有回答训练样本，也有可独立用于检索的法条、司法案例和实务资料。
- **不只单轮咨询**：包含信息抽取、摘要、规则适用、证据分析和多轮问答；补充105条完整案例样本，覆盖35个案例家族。
- **可以追溯**：保留来源、版本、上下文证据和质量/许可状态；不将AI复核冒充律师签核。
- **易于上手**：标准JSONL、gzip分片，无需Git LFS或专用下载客户端；可用Python标准库读取，也可按需加载到Hugging Face Datasets。
- **报告真实结果与边界**：有Base / SFT / RAG / SFT+RAG四组mini消融结果，不声称所有基准都由SFT+RAG获胜。

## 数据规模

| 数据 | 数量 | 位置 |
| --- | ---: | --- |
| SFT训练集 | 15,242条 | `data/sft/train/*.jsonl.gz` |
| SFT验证集 | 1,923条 | `data/sft/validation/*.jsonl.gz` |
| RAG完整资料单元 | 37,748条 | `data/rag/corpus/*.jsonl.gz` |
| RAG检索块 | 51,017条 | `data/rag/chunks/*.jsonl.gz` |

“资料单元”不等于37,748部法律：一条可能是一条法条、一个案例检索文本或一张实务卡片；检索块由资料单元切分，二者不能相加当作独立资料数量。

| RAG层 | 资料单元 | 检索块 |
| --- | ---: | ---: |
| current | 32,378 | 32,652 |
| case | 5,324 | 18,311 |
| practice_card | 20 | 28 |
| historical | 26 | 26 |

原语料截点为2026-09-27，补充材料另有2026-10-03的核对信息。发布日期不意味着全部法律已更新至2026-10-09；历史材料应仅在明确日期/版本范围内使用。

## 下载与快速使用

点击GitHub的 **Code → Download ZIP**，或克隆本仓库：

```bash
git clone https://github.com/lite93597/chinese-legal-sft-rag.git
cd chinese-legal-sft-rag
python scripts/verify.py
```

### 不安装第三方依赖也能读取

```python
from scripts.load_data import iter_records, training_messages

row = next(iter_records("sft/train"))
print(row["id"], row["task_type"])
messages = training_messages(row)
print(messages[-1]["content"])  # 最后一轮训练回答

chunk = next(iter_records("rag/chunks"))
print(chunk["content"])
print(chunk["metadata"].get("source_url"))
```

**注意：**15,143条训练样本和1,917条验证样本已有 `messages`；新增的99条训练/6条验证案例使用 `instruction/question/answer/context_documents` 结构。`training_messages()`按原V4公共提示规则组装全部记录，包含用户可见证据块，避免漏掉105条案例。原始数据分片不新增或改写这些字段。

### 使用Hugging Face Datasets

```bash
pip install datasets
```

```python
import gzip
import json
from pathlib import Path
from datasets import Dataset
from scripts.load_data import iter_records, training_messages

# 原始行保留异构来源元数据。统一到训练所需字段再建Arrow表，
# 避免直接加载全部嵌套元数据时发生schema冲突。
def examples():
    for row in iter_records("sft/train"):
        yield {"id": row["id"], "messages": training_messages(row)}

train = Dataset.from_generator(examples)
print(len(train))  # 15242
```

RAG语料可用 `iter_records("rag/corpus")` 加载到自己的向量/BM25索引。检索块顺序与原FAISS向量顺序保持一致；`metadata.article_text` 为对应完整资料单元，不能只拼碎片便声称使用了完整法条/案例。

## 可选：直接复用FAISS索引

`data/rag/faiss/` 提供可恢复的二进制归档分片，不需要重新生成51,017个向量。运行：

```bash
python scripts/restore_index.py --output ./local-index
```

归档内含 `law.index`、按原向量顺序排列的公开 `metadata.json` 和 `index_info.json`。索引为1024维、归一化向量、FAISS内积索引，使用BGE-large-zh-v1.5；它不是LLM权重，也不包含Embedding/Reranker模型权重。可选安装 `faiss-cpu` 后自行检索。

## SFT与RAG的实际使用方式

本轮SFT采用BF16 LoRA：`r=16`、`alpha=32`、`dropout=0.05`、学习率 `2e-5`、1 epoch、训练长度8192、batch 4、梯度累积2。仅Assistant回答和结束标记参与损失，用户输入与系统提示不作为监督目标。多轮记录应监督全部Assistant轮次，不只最后一轮。

原RAG使用BGE-large-zh-v1.5的1024维向量召回、Qwen3-Reranker-0.6B重排，并进行多议题与适用日期/版本处理。V4上下文策略最多4个议题、24个候选、6篇完整证据文档；输入上限16384、输出上限4096。这些是原实验配置，不是本仓库承诺的通用最优参数。BM25/RRF可由使用者自行组合；本仓库主要交付数据，不打包法律Agent应用或完整训练/评测服务。

## 四组消融结果

每组1,351题、54项任务，来自LawBench / DISC / LexEval的**mini开发子集**，不是官方全量或独立盲测。下表为各基准任务宏平均，按0–100展示：

| 条件 | LawBench | DISC | LexEval |
| --- | ---: | ---: | ---: |
| Base | 58.2262 | 68.8181 | 65.4444 |
| RAG | 58.0692 | **72.7925** | 64.6759 |
| SFT | 62.3346 | 65.9464 | **68.3203** |
| SFT+RAG | **63.2988** | 69.8364 | 67.7204 |

SFT+RAG相对Base分别提高 **5.07 / 1.02 / 2.28个百分点**，但DISC的本轮最佳是RAG，LexEval最佳是SFT。不将三个不同基准合成一个“法律总分”，不把多项改动的差异归因于单一数据改进。

评分结合任务客观指标与LLM主观评分；完整运行有180份本轮DeepSeek-v4-pro有效评分回执，不代表180名律师审核。还进行了8个案例家族、32份回答的相关案例对照；发现仍有法条引用、日期金额及追加事实遗漏等问题。详见[评测说明](docs/EVALUATION.md)。

## 目录

```text
data/sft/train/          最终训练分片
data/sft/validation/     最终验证分片
data/rag/corpus/         完整资料单元
data/rag/chunks/         所有实际检索块
data/rag/faiss/          可选FAISS归档分片
docs/                   字段、来源许可、评测说明
licenses/upstream/      所使用上游的原README/许可说明
scripts/                读取、提示组装、校验与索引恢复
manifest.json           数据分片、条数、大小、SHA-256
statistics.json         实际任务、领域、许可状态及RAG分层统计
```

公开副本将工程元数据里的本机绝对路径改为原文件名，并省略可能包含原个人信息的历史排除原因说明，保留所有训练/检索文本、样本ID、分区和顺序。原文件与公开分片序列的哈希均有记录；序列化与元数据处理后，公开分片哈希不会与原JSONL文件哈希相同。

## 使用边界与反馈

本数据仅是法律研究/开发辅助材料，不能替代律师意见；答案、检索命中和AI复核均可能错误。已有脱敏不能反推身份，有限模式扫描不等于完整匿名化认证。请遵守上游条件，勿将未确认权利当作授权，勿据此宣传“官方认证”“零幻觉”或“商业可用”。

欢迎提交Issue反馈样本问题、过时法条、错误来源和许可争议，注明记录ID或 `article_id`，不要提交额外私人身份信息。合理的权利人反馈将按具体记录处理。

如果数据对你的SFT、RAG或法律Agent研究有帮助，欢迎 **Star** 支持，也欢迎分享你的改进实验与使用经验。

引用建议：`lite93597. Chinese Legal SFT + RAG Dataset, legal-v4-data-20261009. GitHub.` 引用本仓库不替代上游来源署名和条件。
