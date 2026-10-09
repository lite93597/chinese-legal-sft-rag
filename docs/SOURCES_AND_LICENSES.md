# 来源、许可与隐私说明

本仓库应被理解为**混合来源的公开研究数据发布**，而不是一份统一宽松许可的数据集。保留全量最终样本不等于确认全量再分发或商用权利；权利不明的标记是风险说明，不是许可本身。

## 主要上游

| 来源 | 固定版本/链接 | 说明 |
| --- | --- | --- |
| Lawyer LLaMA | [AndrewZhe/lawyer-llama](https://github.com/AndrewZhe/lawyer-llama)，`abaa09586081b82ceb7b0a9f41d05a68897b24ee` | 原README含学术/非商业条件；不能只凭Apache LICENSE认定数据可商用 |
| HanFei | [siat-nlp/HanFei](https://github.com/siat-nlp/HanFei)，`480b28f2651840ab80fcf0fb32f04b001d17ff24` | 部分咨询来自模型生成；原README限制保留 |
| 夫子·明察整理数据 | [SDUIRLab/fuzi-mingcha-v1_0-data](https://huggingface.co/datasets/SDUIRLab/fuzi-mingcha-v1_0-data)，`3dd37a51cefd84a9ce4bef89282e36ba6161d9fe` | 沿用上游用途条件，不将整理/改写视为解除限制 |
| CAIL / LEVEN等任务来源 | 每条 `source_records` 的项目URL、版本和定位 | 原状态保留；未确认全量再分发/商用许可，不以公开访问代替授权 |
| 官方法律、司法案例与其他资料 | 每条RAG及SFT证据的source_url、version_id等 | 法律规范文本、网站版式、案例编辑、注释与个人信息分别有不同权利/使用边界 |

原始README/LICENSE原文存放于 `licenses/upstream/`，包括可能同时存在的宽松LICENSE标签和更严格README条件。应一起阅读；不代表所有来源都已补齐书面许可。更多来源以逐条记录为准，本表不是穷尽清单。

## 状态如何解读

- `not_confirmed`：未确认再分发许可；不是已获授权，也不等于已发现明确禁止。
- `not_cleared`：未完成权利清理；不可据本仓库宣称商用/无限制。
- `upstream_rights_not_newly_confirmed`：保留上游状态，本次没有重新取得授权。
- 字段缺失或null：未记录，不能推断宽松许可。
- `source_released_for_research/internal_research_only`：用途记录，不自动解决下载者的再分发或商业使用问题。

实际数量见 `statistics.json`。训练集11,574条 `not_confirmed` 全部保留。本仓库不替任何上游授予权利，也不提供“科研使用必然合法”的法律意见。使用者应在拟使用范围内自行核实；无明确依据时应优先联系上游或从其官方入口按条件获取。

## 发布处理与隐私

保留所有最终训练/验证样本与实际RAG记录；不上传模型权重、私人Agent运行材料、API密钥、SSH凭据、训练日志或历史隔离样本。公开副本清理工程元数据中的绝对本机路径，并省略可能残留原个人标识的历史排除原因说明；原模型可见文本不改。

进行了有限凭据和身份号码样式检查；数值命中可能来自哈希标识，检查不是全量匿名化认证，也不是人工逐条隐私审查。公开案例可能仍含公开姓名、机构和事实信息。不得反识别/恢复已有脱敏信息，亦不得用于骚扰或泄露个人隐私。

权利人或数据主体可通过仓库Issue注明记录ID、来源及具体问题请求处理，请勿贴出更多敏感身份信息。涉及隐私时避免直接公开原敏感全文。
