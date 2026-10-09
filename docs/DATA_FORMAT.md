# 数据格式与加载注意事项

## SFT

每个gzip分片解压后是一行一个JSON对象。原来的训练/验证顺序及所有样本均保留，无重新划分、重采样或删题。

| 字段 | 作用 |
| --- | --- |
| `id`, `group_id`, `split` | 样本标识、场景归组和原分区 |
| `instruction`, `question`, `answer` | 任务指令、问题和目标回答 |
| `messages`（可选） | 原存储对话；不保证每行都含这个字段 |
| `context_documents` | 用户可见参考材料；含原文、来源与证据ID |
| `source_input` | 原任务提供的材料；不等于自动补入的检索答案 |
| `source_records` | 上游链接、固定版本、原始记录定位等 |
| `research_use_status`, `redistribution_status` | 原有使用/再分发状态；缺失不代表获得许可 |
| `review_status`, `review_records`, `quality_tier` | 来源/结构/AI核对信息；各行范围不同，非统一律师审查 |

元数据来自不同来源，嵌套类型可能不一致。加载到Arrow/HF Datasets时，推荐先选择统一字段，如 `id/messages`；不要因为元数据schema冲突删除有效样本。

`scripts/load_data.py:training_messages`重现原训练公共提示与证据块拼接：多轮时按user/assistant交替读取；无messages时使用instruction、question及context_documents构造输入。原系统提示由训练公共提示替换，空证据块规则与原训练一致。这个函数只是提示格式化，不执行分词或训练；实现Assistant-only + EOS mask时须使用实际模型chat template，并验证每一轮监督边界。

## RAG

- `rag/chunks`：`id/content/metadata`；保持原FAISS向量顺序。`metadata.article_id`对应父资料，`metadata.article_text`是完整父文本，`content`是检索块。
- `rag/corpus`：`id/content/metadata`；按首次出现的article_id去重，content取完整article_text。去掉块专属part_index，不能用该集合的序号直接对应原FAISS向量序号。
- `metadata.layer`区分current/case/practice_card/historical；同时参考日期、法域、版本与 `currency_status/application_rules/default_index`。不是所有层都适合“今天的法律”查询。
- `source_url`等字段用于追溯，不代表网页永远可访问或内容未变化。完整资料单元不一定是整部法律，也不一定是案件完整裁判文书。

## 校验与索引

`manifest.json`包含每个数据分片的条数、字节数和SHA-256，以及按分片顺序拼接的公开JSONL流哈希。`scripts/verify.py`逐文件核对并解析全部JSON。此为文件完整性验证，不是法律正确性或许可认证。

可选FAISS归档公开metadata仅做本机路径清理，数组顺序与向量顺序不变；恢复时核对分片、完整ZIP和原law.index SHA-256，不重新计算Embedding。
