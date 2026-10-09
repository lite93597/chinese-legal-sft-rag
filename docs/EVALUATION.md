# 原V4消融实验说明：独立实验层入口

为区分数据发布与模型训练/评测，本页的内容已整理到独立的 [experiments/](../experiments/README.md)，保留此路径兼容旧链接。

- [SFT训练配置与实际过程](../experiments/sft/README.md)
- [RAG索引、检索与生成过程](../experiments/rag/README.md)
- [四组评测协议、结果与限制](../experiments/evaluation/README.md)
- [完整精度结果JSON](../experiments/evaluation/results/v4/summary.json)
- [216条逐任务成绩CSV](../experiments/evaluation/results/v4/task_scores.csv)

原V4结果和实验边界不变：每组1,351题、54任务的mini开发子集，不是官方全量、独立盲测或律师评审；不合成三个基准的总分，也不保证其他模型复现结果。完整训练/推理/评分源码及模型权重尚未在本仓库发布。
