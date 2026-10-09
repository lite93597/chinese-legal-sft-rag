# 数据层：中文法律SFT与RAG数据

[仓库首页](../README.md) · [模型与实验层](../experiments/README.md)

这里回答“有哪些数据、怎样下载和读取、来源与使用条件是什么”。模型训练、RAG运行流程、评分和实验结果由独立的 `experiments/` 维护。

## 已发布内容

| 数据 | 数量 | 目录 |
| --- | ---: | --- |
| SFT训练样本 | 15,242 | [sft/train](sft/train/) |
| SFT验证样本 | 1,923 | [sft/validation](sft/validation/) |
| RAG完整资料单元 | 37,748 | [rag/corpus](rag/corpus/) |
| RAG检索块 | 51,017 | [rag/chunks](rag/chunks/) |
| 可恢复FAISS索引 | 51,017个1024维向量 | [rag/faiss](rag/faiss/) |

保留原训练/验证划分、样本ID、顺序及模型可见文本。完整资料单元不等于同等数量的法律文件，检索块与其父资料也不能相加计数。

## 下载和使用入口

- [下载与快速读取](../README.md#下载与快速使用)
- [SFT单轮、带法源和多轮案例](../README.md#sft数据示例)
- [RAG字段与完整资料读取](../README.md#rag数据与检索示例)
- [FAISS恢复与最小检索示例](../README.md#可选直接复用faiss索引)
- [字段说明](../docs/DATA_FORMAT.md)
- [来源与许可](../docs/SOURCES_AND_LICENSES.md)
- [分片清单与哈希](../manifest.json) · [数据统计](../statistics.json)

在仓库根目录可运行 `python scripts/verify.py` 检查数据分片。该命令验证数据完整性，不训练模型、不测评生成效果。

## 与实验层的边界

`scripts/load_data.py`、`scripts/verify.py` 和 `scripts/restore_index.py` 是数据读取/恢复工具，不是完整的SFT训练或模型评测程序。后续新增训练代码、推理程序和实验结果放在 `experiments/`，不改变本层数据路径。

数据保留混合上游条件和未确认的再分发状态，不具有全包MIT/Apache或可商用授权。运行训练程序或公开实验结果，不会自动补齐数据与模型的使用权利。
