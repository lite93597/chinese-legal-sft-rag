# 模型评测：过程、四组结果与限制

[实验总览](../README.md) · [数据层](../../data/README.md) · [SFT](../sft/README.md) · [RAG](../rag/README.md)

本页整理已完成的原V4实验，不重新训练或生成答案，不混入V1/V2/V3结果。机读材料位于 [results/v4](results/v4/)。

## 1. 四组消融如何区分？

| 条件 | 生成模型 | 是否提供RAG资料 |
| --- | --- | --- |
| Base | 原始权重 | 否 |
| RAG | 原始权重 | 是 |
| SFT | LoRA微调后权重 | 否 |
| SFT+RAG | LoRA微调后权重 | 是 |

每组题目与任务集合相同。无RAG与有RAG输入对应同一道原题，RAG只按固定流程加入外部资料；两种权重分别实际生成，不能从旧结果复制答案或分数。同权重、完全相同实际输入只共享本轮一次fresh生成记录，不跨权重共享。

## 2. 题目规模与推理过程

| 基准mini子集 | 每组题数 | 任务数 |
| --- | ---: | ---: |
| LawBench | 500 | 20 |
| DISC | 143 | 11 |
| LexEval | 708 | 23 |
| 合计 | 1,351 | 54 |

准备2,702份对应无RAG/有RAG输入；四条件最终各有1,351题、54任务的预测。另用8个相关案例家族、16份关联输入生成两权重对照共32份实际回答。原640请求/64探针用于本轮工程运行检查，不计入基准题数，也不是额外的独立法律准确率测评。

原vLLM推理使用BF16，输入16,384、输出4,096 Tokens，调度预算4,096 Tokens，plain batch 32、submit block 128；训练长度8,192与推理输入16,384不是同一参数。采样temperature=0、top_p=1、seed=42。未为赶进度删除题目或静默裁切长问题。

## 3. 如何评分和汇总？

先按任务得到最终预测，再按原任务实现进行客观评分，需主观评价的部分通过本轮DeepSeek-v4-pro评分，最后生成每条件报告。四组共12个评分/报告阶段、180份有效收费API评分回执；这些不是180名律师的审核。这里仅公开聚合与逐任务成绩，不公开收费API凭据、私人运行日志或第三方题目答案包。

指标包括Accuracy、各类F1、ROUGE-L、ChERRANT F0.5、数值距离分和主观1–5分，具体以CSV的 `metric/scale` 为准。DISC主观分按 `score/5` 归一化；其他本轮0–1指标乘100。每个基准独立按任务等权宏平均，不按全部题目直接平均，也不把三个基准合成一个法律总分。

LawBench部分指标沿用了本项目已有实现，例如1-1/3-2使用ROUGE-L，2-2保留原Accuracy实现。下表不能直接宣传成与其他实现完全可比的“官方LawBench总分”。

## 4. 实际结果

各基准任务宏平均，0–100展示；更多小数位保存在JSON。

| 条件 | LawBench | DISC | LexEval | 输出上限命中题数 |
| --- | ---: | ---: | ---: | ---: |
| Base | 58.2262 | 68.8181 | 65.4444 | 3 |
| RAG | 58.0692 | **72.7925** | 64.6759 | 2 |
| SFT | 62.3346 | 65.9464 | **68.3203** | 2 |
| SFT+RAG | **63.2988** | 69.8364 | 67.7204 | 3 |

| 相对Base的差值（百分点） | LawBench | DISC | LexEval |
| --- | ---: | ---: | ---: |
| RAG − Base | -0.1570 | +3.9744 | -0.7684 |
| SFT − Base | +4.1084 | -2.8717 | +2.8759 |
| SFT+RAG − Base | +5.0726 | +1.0183 | +2.2761 |

本轮LawBench最佳是SFT+RAG，DISC最佳是RAG，LexEval最佳是SFT。SFT+RAG并非所有任务的最优选项，领域微调和检索可能互补，也可能带来干扰。

## 5. 下载实际成绩

- [summary.json](results/v4/summary.json)：四条件run ID、完整精度总分、分差、题数、生成时间与结果范围。
- [task_scores.csv](results/v4/task_scores.csv)：4×54=216条成绩，保留原始指标与尺度、题数、原分、归一化分及输出上限命中数；不含题目、标准答案或个人身份信息。
- [protocol.json](results/v4/protocol.json)：原四条件、题目规模、推理限制和评分口径。

使用Python标准库查看或重新汇总，不需要模型、GPU或收费API。以下在仓库根目录运行：

```python
import csv
from collections import defaultdict
from pathlib import Path

path = Path("experiments/evaluation/results/v4/task_scores.csv")
groups = defaultdict(list)
with path.open(encoding="utf-8", newline="") as f:
    for row in csv.DictReader(f):
        groups[(row["mode"], row["benchmark"])].append(float(row["normalized_score_0_100"]))
for (mode, benchmark), values in groups.items():
    print(mode, benchmark, round(sum(values) / len(values), 4))
```

## 6. 时间、案例与已知问题

原始权重pair联合生成1,897.928秒，V4权重pair为994.594秒。这包含配对请求与案例，不能拆成四个单模式用时、归为纯后端加速或证明一般设备/批次等价。

32份案例对照中，V4较少无条件断言，但仍存在法条引用、试用期、日期金额计算及追加事实遗漏。案例平均输出长度：原始权重2,915.125 Tokens，V4+RAG为773.3125；两边案例均没有因输出上限结束，不能把本轮案例遗漏一概归因于截断。回答更短也不自动代表质量更高。

这些是开发mini及开发中接触过的相关案例，不是官方全量、独立盲测、律师签核或统计显著性结论。多处改动不能被解释为单一数据因素的因果收益；使用本数据训练别的模型不保证复现结果。
