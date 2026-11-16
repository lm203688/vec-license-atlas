# 赛事数据红线（Virtual Embryo Challenge 2026）

只读官方两页原文：`/challenge/terms`（Terms of Use，2026-08-10 生效）与 `/challenge/rules`。下面每一条都给出原文位置，方便你自己复核。

## 原文（Terms §14 Research Use and Scientific Integrity）

> Competition datasets are provided for research and educational purposes. Any use, reuse, publication, presentation, or redistribution of the data outside the Challenge must appropriately acknowledge the Virtual Embryo Challenge and credit Dr. Neil Chi's group at the University of California, San Diego (UCSD), which generated the dataset. **As the dataset has not yet been published, any use of the data in a publication or public presentation must receive prior approval from Dr. Neil Chi and the data-generating team.** Any publication using the dataset must also appropriately credit Dr. Qingquan Zhang and Dr. Neil Chi.

拆成四句人话：

1. 数据只能用于研究与教育；
2. 任何超出赛内使用的使用、复用、发表、演示、再分发，都要致谢赛事并署名 UCSD 的 Dr. Neil Chi 团队；
3. **因为数据集尚未发表，任何进论文或公开演示的使用都要先获得 Dr. Neil Chi 与数据生成团队的批准**——不是"致谢一下就行"，是"先问、后写"；
4. 发表时还要同时署名 Dr. Qingquan Zhang 与 Dr. Neil Chi。

## 三个判决示例

| 你想做的事 | 判决 | 依据 |
|---|---|---|
| 在自己机器上训练、调参、跑本地评测，不对外 | **可以** | §14 第 1 句：研究与教育用途 |
| 把清洗后的数据子集放进自己的公开 GitHub 仓库 | **不可以** | §14 第 2 句：再分发（redistribution）需授权；且这属于未发表数据的再分发 |
| 把评测结果写成论文投出去 | **先问再写** | §14 第 3 句：publication 需 Dr. Neil Chi 与数据生成团队事先批准 |
| 在技术博客/会议 talk 里展示一张数据分布图 | **先问再写** | 同上，public presentation 同受约束 |
| 只发布方法、代码、指标，不发布任何数据或数据派生表 | **可以** | Rules：领奖只要求书面方法说明并可公开；代码不强制公开 |

## 领奖这件事的附加条件

Terms §14 第三条还有一个容易忽略的点：

> Receiving a prize is conditional on supplying a written description of how the method works, and on agreeing to its publication. Code is not required to be published; the Organisers may ask to see it privately to verify a result.

即：**拿奖的前提是交一份"方法怎么工作"的书面说明并同意其公开**；代码不强制公开，但组委会可以私下要看。所以"参赛但完全不写方法"这条路走不通。

## 可安全使用的开放数据（与本表同源）

不是所有数据都受限。下面这些按各自条款可放心用（条目在 `data/atlas.csv` 里）：

- `Tahoe-100M` — 数据卡标 CC0（本轮未直连 HF 复核，用前请自行确认一次）；
- `CELLxGENE Census` — 按每个数据集各自许可，工具侧 MIT；
- `Human Cell Atlas` — CC-BY-4.0，需署名；
- `VCC 2025 dataset` — 二手数据卡标 CC-BY-4.0，动手前核对原始条款。

**换数据的正确姿势**：先把 `vec-trust-kit` / 你的模型的输入层换成上述任一开放数据，再谈"可商用"，否则你训练出的权重天然继承赛事数据的限制。

## 一句话总结

赛事数据可以拿来做研究、做工具、做教程，**但不能替它发表**。要把成果写成论文或公开演示，先给 `virtual.embryo.moonshot@gmail.com` 发一封说明用途的邮件，等批准。
