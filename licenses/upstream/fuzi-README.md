---
license: apache-2.0
task_categories:
- text-generation
language:
- zh
tags:
- legal
---

<p align="center">
🐱 <a href="https://github.com/irlab-sdu/fuzi.mingcha" target="_blank">Github Repo</a> <br>
</p>

- 模型 huggingface 链接：https://huggingface.co/datasets/SDUIRLab/fuzi-mingcha-v1_0

- 数据 huggingface 链接：https://huggingface.co/datasets/SDUIRLab/fuzi-mingcha-v1_0-data

- GitHub 链接：https://github.com/irlab-sdu/fuzi.mingcha

- 数据 魔搭链接：https://www.modelscope.cn/datasets/furyton/fuzi-mingcha-v1_0-data

- 模型 魔搭链接：https://www.modelscope.cn/models/furyton/fuzi-mingcha-v1_0


# 夫子•明察司法大模型微调训练数据归档

## 数据信息

数据集主要分为四类：1. 通用微调数据集；2. 基于法条的问答数据集；3. 案例检索、案例分析类数据集；4. 三段论判决数据集。

| Directory | Filename | Num Samples |
| --- | --- | --- |
| . | oaast_sft_zh.json | 689 |
| alpaca | alpaca_data_zh_51k.json | 5,000 |
| alpaca | alpaca_gpt4_data_zh.json | 5,000 |
| belle | belle.jsonl | 10,000 |
| cail2021_rc | cail_21_rc.jsonl | 4,200 |
| cail2022_summarization.wo_art | cail_22_summarization.jsonl | 5,750 |
| case_retrieval | new_candidates.jsonl | 9,208 |
| case_retrieval | new_pretrain.jsonl | 6,026 |
| case_retrieval | new_query.jsonl | 107 |
| case_retrieval | query.jsonl | 107 |
| hanfei | zh_law_conversation_v2.jsonl | 20,000 |
| hanfei | zh_law_instruction_v2.jsonl | 20,000 |
| lawGPT_zh | lawgpt4analyse_v2.jsonl | 15,000 |
| lawGPT_zh | lawgpt4answer_v2.jsonl | 10,000 |
| lawGPT_zh | lawgpt4fatiao_v2.jsonl | 10,000 |
| lawyerllama | lawyer_llama_4analyse_v1.jsonl | 1,000 |
| lawyerllama | lawyer_llama_4answer_v1.jsonl | 1,000 |
| lawyerllama | lawyer_llama_4fatiao_v1.jsonl | 1,000 |
| lawyerllama_counsel | legal_advice.json | 3,000 |
| lawyerllama_counsel | legal_counsel_v2.json | 5,000 |
| OL_CC | OL_CC.jsonl | 10006 |
| pretrain_judge_w_article | judge_w_article_v6.jsonl | 15,000 |
| pretrain_small_law | complement.json | 12,000 |
| pretrain_small_law | pretrain_case.json | 52 |
| pretrain_small_law | query_item.json | 20,000 |
| syllogism[1] | legal_article.json | 11,237 |
| syllogism[1] | syllogism.json | 11,237 |

注 1：利用三段论推理来选择和评估当事人的论点是一种常见的做法。三段论中包含大前提、小前提和结论三个部分，应用到法律领域中时，大前提通常是由相关法条构成的法律依据，小前提通常时由犯罪要件构成的案情分析结果，结论通常是由最终适用的法条和判决结果构成。在实践中，三段论是法官广泛使用的法律推理的标准形式，以确保逻辑论点是合理和无可争辩的。我们自主构建的三段推理判决数据已经发表在 EMNLP 2023 [1]，详细的数据构建方法及数据集内容请参考[论文代码](https://github.com/dengwentao99/SLJA)。

[1]. Wentao Deng, Jiahuan Pei, Keyi Kong, Zhe Chen, Furu Wei, Yujun Li, Zhaochun Ren, Zhumin Chen, and Pengjie Ren. 2023. [Syllogistic Reasoning for Legal Judgment Analysis](https://aclanthology.org/2023.emnlp-main.864). In Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing, pages 13997–14009, Singapore. Association for Computational Linguistics.

## 数据来源

- `case_retrieval` 目录下的数据集通过爬取的裁判文书数据进行构建，结合 ChatGPT 构建部分 query。

- `pretrain_*` 目录下的数据由预训练数据（裁判文书、法律法规等）构造完成。

- `syllogism` 目录下数据来源见注 1。

- 其他数据收集整理和筛选于网络公开信息，请点击以下标签对应的链接查看更多信息。

  - [alpaca](https://github.com/Instruction-Tuning-with-GPT-4/GPT-4-LLM)

  - [belle](https://huggingface.co/datasets/BelleGroup/train_1M_CN)

  - [cail2021_rc](https://github.com/china-ai-law-challenge/CAIL2021)

  - [cail2022_summarization.wo_art](https://github.com/china-ai-law-challenge/CAIL2022)

  - [hanfei](https://github.com/siat-nlp/HanFei)

  - [lawGPT_zh](https://github.com/LiuHC0428/LAW-GPT)

  - [lawyerllama, lawyerllama_counsel](https://github.com/AndrewZhe/lawyer-llama/tree/main/data)

  - [OL_CC](https://data.baai.ac.cn/details/OL-CC)

若数据开源造成任何协议问题请联系我们进行删除。

## 如何使用

若您想将数据集用于您的模型训练，您可以克隆本仓库，以下命令为 huggingface 网站提供的提示。

```bash
# Make sure you have git-lfs installed (https://git-lfs.com)
git lfs install

# When prompted for a password, use an access token with write permissions.
# Generate one from your settings: https://huggingface.co/settings/tokens
git clone https://huggingface.co/datasets/SDUIRLab/fuzi-mingcha-v1_0-data
```

请确保您的磁盘空间足够存储数据集，数据集大小约为 1.12GB。

我们推荐使用 [LLaMA-Factory 框架](https://github.com/hiyouga/LLaMA-Factory/blob/main/README_zh.md#%E5%A6%82%E4%BD%95%E4%BD%BF%E7%94%A8) 进行训练，我们提供了 `dataset_info.json` 文件，使用方法见 [LLaMA-Factory](https://github.com/hiyouga/LLaMA-Factory/blob/main/README_zh.md#%E6%95%B0%E6%8D%AE%E5%87%86%E5%A4%87)。


## 致谢

本项目基于如下开源项目展开，在此对相关项目和开发人员表示感谢：

- [Alpaca](https://github.com/tatsu-lab/stanford_alpaca)
- [BELLE](https://github.com/LianjiaTech/BELLE)
- [ChatGLM-6B](https://github.com/THUDM/ChatGLM-6B)
- [ChatGLM-Efficient-Tuning](https://github.com/hiyouga/ChatGLM-Efficient-Tuning)
- [Lawyer LLaMA](https://github.com/AndrewZhe/lawyer-llama)
- [LaWGPT](https://github.com/pengxiao-song/LaWGPT)
- [JEC-QA](https://jecqa.thunlp.org/)
- [PKU Opendata](https://opendata.pku.edu.cn/dataset.xhtml?persistentId=doi:10.18170/DVN/OLO4G8)
- [LawRefBook](https://github.com/RanKKI/LawRefBook)
- [CAIL 2018-2021](https://github.com/china-ai-law-challenge)
- [HanFei](https://github.com/siat-nlp/HanFei)
- [BAAI](https://data.baai.ac.cn/details/OL-CC)

## 声明

本项目的内容仅供学术研究之用，不得用于商业或其他可能对社会造成危害的用途。
在涉及第三方代码的使用时，请切实遵守相关的开源协议。
本项目中大模型提供的法律问答、判决预测等功能仅供参考，不构成法律意见。
如果您需要法律援助等服务，请寻求专业的法律从业者的帮助。

## 协议

本仓库的代码依照 [Apache-2.0](LICENSE) 协议开源，我们对 ChatGLM-6B 模型的权重的使用遵循 [Model License](https://github.com/THUDM/ChatGLM-6B/blob/main/MODEL_LICENSE)。

## 引用

如果本项目有帮助到您的研究，请引用我们：

```
@misc{fuzi.mingcha,
  title={fuzi.mingcha},
  author={Shiguang Wu, Zhongkun Liu, Zhen Zhang, Zheng Chen, Wentao Deng, Wenhao Zhang, Jiyuan Yang, Zhitao Yao, Yougang Lyu, Xin Xin, Shen Gao, Pengjie Ren, Zhaochun Ren, Zhumin Chen}
  year={2023},
  publisher={GitHub},
  journal={GitHub repository},
  howpublished={\url{https://github.com/irlab-sdu/fuzi.mingcha}},
}
```

```
@inproceedings{deng-etal-2023-syllogistic,
    title        = {Syllogistic Reasoning for Legal Judgment Analysis},
    author       = {Deng, Wentao  and Pei, Jiahuan  and Kong, Keyi  and Chen, Zhe  and Wei, Furu  and Li, Yujun  and Ren, Zhaochun  and Chen, Zhumin  and Ren, Pengjie},
    year         = 2023,
    month        = dec,
    booktitle    = {Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing},
    publisher    = {Association for Computational Linguistics},
    address      = {Singapore},
    pages        = {13997--14009},
    doi          = {10.18653/v1/2023.emnlp-main.864},
    url          = {https://aclanthology.org/2023.emnlp-main.864},
    editor       = {Bouamor, Houda  and Pino, Juan  and Bali, Kalika}
}
```

---

联系方式：

E-Mail: shiguang.wu@mail.sdu.edu.cn

